"""Aplica en Odoo los títulos nuevos de Shopify y marca liquidación con una etiqueta.

Uso (credenciales en variables de entorno, nunca en el repo):
    export ODOO_URL=https://ventasguate.odoo.com ODOO_DB=... ODOO_USER=... ODOO_API_KEY=...
    python3 odoo_sync_titulos.py            # simulación: solo muestra qué cambiaría
    python3 odoo_sync_titulos.py --aplicar  # escribe en Odoo

Entrada: titulos_respaldo_y_nuevos.csv (misma carpeta).
Qué hace por cada fila:
  1. Busca la capa Shopify (shopify.product.template.ept) por shopify_tmpl_id = product_id.
  2. Escribe el título nuevo en la capa Shopify (name) y en product.template (name).
  3. Si la fila es de liquidación, agrega la etiqueta de producto "Liquidación" (product.tag).
Genera odoo_sync_resultado.csv con lo que hizo (o haría) por fila.
"""
import csv
import os
import sys
import json
import ssl
import urllib.request

APLICAR = "--aplicar" in sys.argv
AQUI = os.path.dirname(os.path.abspath(__file__))

url, db = os.environ["ODOO_URL"], os.environ["ODOO_DB"]
user, key = os.environ["ODOO_USER"], os.environ["ODOO_API_KEY"]
_ca = "/root/.ccr/ca-bundle.crt"
_ctx = ssl.create_default_context(cafile=_ca) if os.path.exists(_ca) else ssl.create_default_context()


def _rpc(service, method, *args):
    body = json.dumps({"jsonrpc": "2.0", "method": "call", "id": 1,
                       "params": {"service": service, "method": method, "args": list(args)}}).encode()
    req = urllib.request.Request(f"{url}/jsonrpc", body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, context=_ctx, timeout=120) as r:
        res = json.load(r)
    if res.get("error"):
        raise RuntimeError(json.dumps(res["error"])[:800])
    return res["result"]


uid = _rpc("common", "authenticate", db, user, key, {})
if not uid:
    sys.exit("No se pudo autenticar en Odoo")


def call(model, method, *args, **kw):
    return _rpc("object", "execute_kw", db, uid, key, model, method, list(args), kw)


filas = list(csv.DictReader(open(os.path.join(AQUI, "titulos_respaldo_y_nuevos.csv"), encoding="utf-8")))
ids_shopify = [f["product_id"] for f in filas]

# Capas Shopify en bloque
capas = {}
for i in range(0, len(ids_shopify), 500):
    for c in call("shopify.product.template.ept", "search_read",
                  [["shopify_tmpl_id", "in", ids_shopify[i:i + 500]]],
                  fields=["id", "name", "shopify_tmpl_id", "product_tmpl_id"], context={"active_test": False}):
        capas[c["shopify_tmpl_id"]] = c

# Respaldo: productos sin capa Shopify -> product.template por SKU (default_code)
SKUS = {}
cat = os.environ.get("CATALOGO_JSON")
if cat and os.path.exists(cat):
    for p in json.load(open(cat)):
        v = p["variants"]["nodes"]
        if v and v[0].get("sku"):
            SKUS[p["id"].split("/")[-1]] = v[0]["sku"]
faltan = [SKUS[f["product_id"]] for f in filas if f["product_id"] not in capas and f["product_id"] in SKUS]
por_sku = {}
for i in range(0, len(faltan), 500):
    for pp in call("product.product", "search_read", [["default_code", "in", faltan[i:i + 500]]],
                   fields=["default_code", "product_tmpl_id"], context={"active_test": False}):
        por_sku.setdefault(pp["default_code"], set()).add(tuple(pp["product_tmpl_id"]))
tmpl_names = {}
ids_t = sorted({t[0] for v in por_sku.values() if len(v) == 1 for t in v})
for i in range(0, len(ids_t), 500):
    for t in call("product.template", "read", ids_t[i:i + 500], fields=["name"], context={"active_test": False}):
        tmpl_names[t["id"]] = t["name"]

tag_id = None
if any(f["liquidacion"] == "1" for f in filas):
    t = call("product.tag", "search", [["name", "=", "Liquidación"]])
    if t:
        tag_id = t[0]
    elif APLICAR:
        tag_id = call("product.tag", "create", {"name": "Liquidación"})

out = csv.writer(open(os.path.join(AQUI, "odoo_sync_resultado.csv"), "w", newline="", encoding="utf-8"))
out.writerow(["product_id", "capa_id", "product_tmpl_id", "nombre_odoo_anterior", "titulo_nuevo", "liquidacion", "estado"])
ok = sin_capa = 0
for f in filas:
    c = capas.get(f["product_id"])
    capa_id = c["id"] if c else ""
    if c and c["product_tmpl_id"]:
        tmpl_id, tmpl_name = c["product_tmpl_id"]
        via = "capa"
    else:
        cand = por_sku.get(SKUS.get(f["product_id"]), set())
        if len(cand) != 1:
            sin_capa += 1
            out.writerow([f["product_id"], "", "", "", f["titulo_nuevo"], f["liquidacion"],
                          "sin coincidencia" if not cand else "SKU ambiguo"])
            continue
        tmpl_id = next(iter(cand))[0]
        tmpl_name = tmpl_names.get(tmpl_id, "")
        via = "sku"
    estado = f"simulado ({via})"
    if APLICAR:
        if c:
            call("shopify.product.template.ept", "write", [c["id"]], {"name": f["titulo_nuevo"]})
        vals = {"name": f["titulo_nuevo"]}
        if f["liquidacion"] == "1" and tag_id:
            vals["product_tag_ids"] = [(4, tag_id)]
        call("product.template", "write", [tmpl_id], vals)
        estado = f"aplicado ({via})"
    ok += 1
    out.writerow([f["product_id"], capa_id, tmpl_id, tmpl_name, f["titulo_nuevo"], f["liquidacion"], estado])

print(f"{'Aplicados' if APLICAR else 'A aplicar'}: {ok} | sin coincidencia en Odoo: {sin_capa} | etiqueta Liquidación id: {tag_id}")
