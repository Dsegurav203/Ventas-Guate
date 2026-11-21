"""Liga variantes de Shopify sin capa del conector a productos de Odoo por SKU / código de barras.

Uso:
  python3 seo/inventario/ligar_por_sku.py DIR            → propuesta (solo lectura): DIR/ligar_propuesta.json
  python3 seo/inventario/ligar_por_sku.py DIR --aplicar  → crea capas y escribe DIR/ligar_aplicado.json + DIR/ligar_ajustes.json

DIR/paginas/skus_*.json: respuestas `data` de Shopify con
  nodes(ids){ ... on ProductVariant { legacyResourceId sku title product{ legacyResourceId title } inventoryItem{ legacyResourceId } } }
DIR/paginas/*.json (resto): fotos de inventario del cruce (para la cantidad actual en Shopify).

Reglas:
- Coincidencia exacta de SKU (sin "L" inicial de los códigos viejos) contra default_code o barcode de product.product activo.
- Debe haber un único producto en Odoo y sin capa de variante existente para la instancia 1.
- Un producto de Shopify se liga a una sola plantilla de Odoo: si sus variantes apuntan a plantillas distintas, se omite.
- Si ya existe capa de plantilla para ese producto de Shopify, se reutiliza.
"""
import collections, json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts"))
from odoo_rpc import call  # noqa: E402

D = sys.argv[1]
APLICAR = "--aplicar" in sys.argv
CTX = {"active_test": False}
BODEGAS = ["BD3", "TVGDC", "OFI"]

variantes, actual = [], {}
for f in sorted(os.listdir(f"{D}/paginas")):
    d = json.load(open(f"{D}/paginas/{f}"))
    d = d.get("data", d)
    nodos = (d.get("productVariants") or {}).get("nodes") or d.get("nodes") or []
    for n in nodos:
        if not n:
            continue
        if f.startswith("skus_"):
            variantes.append(n)
        elif "inventoryQuantity" in n:
            actual[str(n["legacyResourceId"])] = n["inventoryQuantity"] or 0

locs = [l["id"] for l in call("stock.location", "search_read",
        [["usage", "=", "internal"], "|", "|"] + [["complete_name", "ilike", b] for b in BODEGAS], fields=["id"])]

prop, omitidos = [], []
for v in variantes:
    sku = (v.get("sku") or "").strip()
    cod = sku[1:] if sku[:1] == "L" and sku[1:].isdigit() else sku
    base = {"variant_id": str(v["legacyResourceId"]), "sku": sku, "titulo": v["product"]["title"],
            "shopify_tmpl_id": str(v["product"]["legacyResourceId"]),
            "inventory_item_id": str(v["inventoryItem"]["legacyResourceId"])}
    if not cod:
        omitidos.append({**base, "motivo": "sin SKU en Shopify"}); continue
    pp = call("product.product", "search_read", ["|", ["default_code", "=", cod], ["barcode", "=", cod], ["active", "=", True]],
              fields=["id", "display_name", "product_tmpl_id", "default_code"])
    if not pp and cod != sku:
        pp = call("product.product", "search_read", ["|", ["default_code", "=", sku], ["barcode", "=", sku], ["active", "=", True]],
                  fields=["id", "display_name", "product_tmpl_id", "default_code"])
    if len(pp) != 1:
        omitidos.append({**base, "motivo": f"{len(pp)} productos en Odoo con ese código"}); continue
    p = pp[0]
    if call("shopify.product.product.ept", "search_count", [["product_id", "=", p["id"]], ["shopify_instance_id", "=", 1]], context=CTX):
        omitidos.append({**base, "motivo": "el producto de Odoo ya está ligado a otra variante (posible duplicado en Shopify)",
                         "odoo": p["display_name"]}); continue
    prop.append({**base, "product_id": p["id"], "odoo": p["display_name"], "product_tmpl_id": p["product_tmpl_id"][0],
                 "default_code": p["default_code"] or cod})

por_prod = collections.defaultdict(list)
for x in prop:
    por_prod[x["shopify_tmpl_id"]].append(x)
final = []
for sid, xs in por_prod.items():
    if len({x["product_tmpl_id"] for x in xs}) > 1:
        omitidos += [{**x, "motivo": "variantes del mismo producto de Shopify apuntan a plantillas distintas en Odoo"} for x in xs]
    else:
        final += xs

libre = collections.Counter()
if final:
    for q in call("stock.quant", "search_read", [["product_id", "in", [x["product_id"] for x in final]], ["location_id", "child_of", locs]],
                  fields=["product_id", "quantity", "reserved_quantity"]):
        libre[q["product_id"][0]] += q["quantity"] - q["reserved_quantity"]
for x in final:
    x["qty_libre"] = max(0, int(libre[x["product_id"]]))
    x["qty_shopify"] = actual.get(x["variant_id"])

json.dump({"ligar": final, "omitidos": omitidos}, open(f"{D}/ligar_propuesta.json", "w"), ensure_ascii=False, indent=1)
print(f"ligar {len(final)} · omitidos {len(omitidos)}")
print(collections.Counter(o["motivo"].split(" (")[0] for o in omitidos).most_common())
if not APLICAR:
    sys.exit(0)

hechos, ajustes = [], []
for sid, xs in collections.defaultdict(list, {k: [x for x in final if x["shopify_tmpl_id"] == k] for k in {x["shopify_tmpl_id"] for x in final}}).items():
    t = call("shopify.product.template.ept", "search_read", [["shopify_tmpl_id", "=", sid], ["shopify_instance_id", "=", 1]],
             fields=["id", "product_tmpl_id", "active"], context=CTX)
    if t and t[0]["product_tmpl_id"] and t[0]["product_tmpl_id"][0] != xs[0]["product_tmpl_id"]:
        for x in xs:
            hechos.append({**x, "resultado": "omitido: capa de plantilla existente apunta a otra plantilla"})
        continue
    if t:
        tid = t[0]["id"]
        if not t[0]["active"]:
            call("shopify.product.template.ept", "write", [tid], {"active": True})
    else:
        tid = call("shopify.product.template.ept", "create", [{
            "name": xs[0]["odoo"].split("] ", 1)[-1], "shopify_instance_id": 1, "product_tmpl_id": xs[0]["product_tmpl_id"],
            "shopify_tmpl_id": sid, "exported_in_shopify": True, "total_variants_in_shopify": len(xs)}])
        tid = tid[0] if isinstance(tid, list) else tid
    for i, x in enumerate(xs, 1):
        vid = call("shopify.product.product.ept", "create", [{
            "name": x["odoo"].split("] ", 1)[-1], "shopify_instance_id": 1, "product_id": x["product_id"],
            "shopify_template_id": tid, "default_code": x["default_code"], "variant_id": x["variant_id"],
            "inventory_item_id": x["inventory_item_id"], "exported_in_shopify": True, "check_product_stock": "deny",
            "inventory_management": "shopify", "taxable": True, "sequence": i}])
        vid = vid[0] if isinstance(vid, list) else vid
        hechos.append({**x, "capa_plantilla": tid, "capa_variante": vid, "resultado": "ligado"})
        if x["qty_shopify"] is not None and x["qty_shopify"] != x["qty_libre"]:
            ajustes.append({"inventoryItemId": f"gid://shopify/InventoryItem/{x['inventory_item_id']}",
                            "locationId": "gid://shopify/Location/84277264597",
                            "quantity": x["qty_libre"], "changeFromQuantity": x["qty_shopify"]})
json.dump(hechos, open(f"{D}/ligar_aplicado.json", "w"), ensure_ascii=False, indent=1)
json.dump(ajustes, open(f"{D}/ligar_ajustes.json", "w"), indent=1)
print(f"ligados {sum(1 for h in hechos if h['resultado'] == 'ligado')} · ajustes de inventario {len(ajustes)}")
