"""Cruce semanal de inventario Odoo ↔ Shopify (ventasguate.gt).

Uso (lo corre la tarea programada semanal, ver seo/inventario/PROCESO.md):
  1) python3 odoo-cli/reports/stock_shopify_cruce.py ids DIR
       → DIR/ids_odoo.json: lotes de 100 variant_id de Shopify con existencia libre en Odoo.
  2) Guardar en DIR/paginas/*.json las respuestas (campo "data") de Shopify con este nodo de variante:
       { legacyResourceId inventoryPolicy inventoryQuantity
         product{ legacyResourceId status title onlineStoreUrl } inventoryItem{ legacyResourceId tracked } }
     a) productVariants(first:100, after:$c, query:"inventory_quantity:>0") paginado (riesgo de sobreventa)
     b) nodes(ids:[gid://shopify/ProductVariant/<id> …]) por cada lote de ids_odoo.json (falta en web)
  3) python3 odoo-cli/reports/stock_shopify_cruce.py comparar DIR
       → DIR/ajustes.json, DIR/resumen.md, DIR/detalle.csv
  La tienda tiene una sola ubicación (Tienda Ventas Guate), así que inventoryQuantity = disponible.

Fuente de verdad: Odoo. Cantidad a publicar = existencia libre (quantity − reserved) en las bodegas
que se publican: BD3, TVGDC y OFIBD (ver ECOMMERCE_SEO.md). Solo lectura en Odoo.

Salida (DIR, por defecto seo/inventario/AAAA-MM-DD):
  ajustes.json        → lotes para inventorySetQuantities (con changeFromQuantity = valor actual de Shopify)
  resumen.md          → diferencias, riesgo de sobreventa, productos sin ligar, capas a productos archivados
  detalle.csv         → todas las variantes con diferencia
Excluye: fichas "Reserva" (inventario manual a propósito) y variantes con inventoryPolicy CONTINUE.
"""
import collections, csv, datetime, json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts"))
from odoo_rpc import call  # noqa: E402

TIENDA = "gid://shopify/Location/84277264597"
BODEGAS = ["BD3", "TVGDC", "OFI"]
LOTE = 200


def shopify(carpeta):
    vistos = {}
    for nombre in sorted(os.listdir(carpeta)):
        if not nombre.endswith(".json"):
            continue
        d = json.load(open(os.path.join(carpeta, nombre), encoding="utf-8"))
        d = d.get("data", d)
        nodos = (d.get("productVariants") or {}).get("nodes") or d.get("nodes") or []
        for n in nodos:
            if not n or "legacyResourceId" not in n:
                continue
            p, inv = n.get("product") or {}, n.get("inventoryItem") or {}
            vistos[str(n["legacyResourceId"])] = {
                "variant_id": str(n["legacyResourceId"]), "policy": n.get("inventoryPolicy"),
                "product_id": str(p.get("legacyResourceId", "")), "titulo": p.get("title", ""),
                "status": p.get("status"), "publicado": bool(p.get("onlineStoreUrl")),
                "inventory_item_id": str(inv.get("legacyResourceId", "")), "tracked": inv.get("tracked"),
                "available": n.get("inventoryQuantity") or 0,
            }
    return list(vistos.values())


def odoo():
    ctx = {"active_test": False}
    capas = call("shopify.product.product.ept", "search_read", [["shopify_instance_id", "=", 1]],
                 fields=["variant_id", "inventory_item_id", "product_id", "active", "default_code"], context=ctx)
    pids = list({c["product_id"][0] for c in capas if c["product_id"]})
    prods = {p["id"]: p for p in call("product.product", "read", pids, fields=["active", "display_name"], context=ctx)}
    locs = [l["id"] for l in call("stock.location", "search_read",
            [["usage", "=", "internal"], "|", "|"] + [["complete_name", "ilike", b] for b in BODEGAS], fields=["id"])]
    libre = collections.Counter()
    for q in call("stock.quant", "search_read", [["location_id", "child_of", locs], ["product_id", "in", pids]],
                  fields=["product_id", "quantity", "reserved_quantity"]):
        libre[q["product_id"][0]] += q["quantity"] - q["reserved_quantity"]
    por_variante = {}
    for c in capas:
        if not c["variant_id"] or not c["product_id"]:
            continue
        pid = c["product_id"][0]
        prev = por_variante.get(c["variant_id"])
        if prev and prev["capa_activa"] and not c["active"]:
            continue
        por_variante[c["variant_id"]] = {
            "product_id": pid, "nombre": prods.get(pid, {}).get("display_name", ""), "capa_activa": c["active"],
            "odoo_activo": prods.get(pid, {}).get("active", False), "libre": max(0, int(libre[pid])),
        }
    return por_variante


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("ids", "comparar"):
        sys.exit(__doc__)
    salida = sys.argv[2]
    hoy = datetime.date.today().isoformat()
    os.makedirs(os.path.join(salida, "paginas"), exist_ok=True)
    od = odoo()
    if sys.argv[1] == "ids":
        ids = sorted(v for v, o in od.items() if o["libre"] > 0 and o["odoo_activo"])
        lotes = [ids[i:i + 100] for i in range(0, len(ids), 100)]
        json.dump(lotes, open(f"{salida}/ids_odoo.json", "w"))
        print(f"{len(ids)} variantes con existencia libre en Odoo → {len(lotes)} lotes en {salida}/ids_odoo.json")
        return
    sh = shopify(os.path.join(salida, "paginas"))

    ajustes, detalle = [], []
    sin_ligar, archivados, sin_nivel = [], [], []
    for v in sh:
        if v["status"] not in ("ACTIVE", "UNLISTED") or "reserva" in v["titulo"].lower() or v["policy"] == "CONTINUE":
            continue
        o = od.get(v["variant_id"])
        if not o:
            sin_ligar.append(v)
            continue
        if not o["odoo_activo"]:
            archivados.append({**v, **o})
        if not v["tracked"]:
            sin_nivel.append({**v, **o})
            continue
        objetivo = o["libre"] if o["odoo_activo"] else 0
        if objetivo != v["available"]:
            tipo = "sobreventa" if v["available"] > objetivo else "falta_en_web"
            detalle.append({**v, **o, "objetivo": objetivo, "tipo": tipo})
            ajustes.append({"inventoryItemId": f"gid://shopify/InventoryItem/{v['inventory_item_id']}",
                            "locationId": TIENDA, "quantity": objetivo, "changeFromQuantity": v["available"]})

    lotes = [ajustes[i:i + LOTE] for i in range(0, len(ajustes), LOTE)]
    json.dump(lotes, open(f"{salida}/ajustes.json", "w"), indent=1)
    campos = ["tipo", "titulo", "available", "objetivo", "publicado", "nombre", "variant_id",
              "inventory_item_id", "odoo_activo"]
    with open(f"{salida}/detalle.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, campos, extrasaction="ignore")
        w.writeheader()
        w.writerows(sorted(detalle, key=lambda r: (r["tipo"], -abs(r["objetivo"] - r["available"]))))

    sv = [d for d in detalle if d["tipo"] == "sobreventa"]
    fw = [d for d in detalle if d["tipo"] == "falta_en_web"]
    L = [f"# Cruce de inventario Odoo ↔ Shopify · {hoy}", "",
         "| Indicador | Variantes | Unidades |", "|---|---|---|",
         f"| Variantes revisadas (stock en Shopify o en Odoo) | {len(sh)} | |",
         f"| Falta en web (Odoo > Shopify) | {len(fw)} | {sum(d['objetivo'] - d['available'] for d in fw)} |",
         f"| Riesgo de sobreventa (Shopify > Odoo) | {len(sv)} | {sum(d['available'] - d['objetivo'] for d in sv)} |",
         f"| Sin ligar al conector | {len(sin_ligar)} | |",
         f"| Ligadas a producto archivado en Odoo | {len(archivados)} | |",
         f"| Sin seguimiento de inventario en la tienda | {len(sin_nivel)} | |", "",
         f"Ajustes preparados: {len(ajustes)} en {len(lotes)} lote(s) → `ajustes.json`.", ""]
    for titulo, filas, cols in [
        ("Riesgo de sobreventa (top 30)", sorted(sv, key=lambda d: d["objetivo"] - d["available"])[:30], ("titulo", "available", "objetivo")),
        ("Falta en web (top 30)", sorted(fw, key=lambda d: d["available"] - d["objetivo"])[:30], ("titulo", "available", "objetivo")),
        ("Sin ligar al conector (publicados)", [v for v in sin_ligar if v["publicado"]], ("titulo", "variant_id", "available")),
        ("Ligadas a producto archivado en Odoo (publicados)", [v for v in archivados if v["publicado"]], ("titulo", "nombre", "available")),
    ]:
        if not filas:
            continue
        L += [f"## {titulo}", "", "| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
        L += ["| " + " | ".join(str(r.get(c, "")) for c in cols) + " |" for r in filas]
        L.append("")
    open(f"{salida}/resumen.md", "w", encoding="utf-8").write("\n".join(L))
    print("\n".join(L[:12]))
    print(f"→ {salida}")


if __name__ == "__main__":
    main()
