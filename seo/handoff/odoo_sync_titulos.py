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
import xmlrpc.client

APLICAR = "--aplicar" in sys.argv
AQUI = os.path.dirname(os.path.abspath(__file__))

url, db = os.environ["ODOO_URL"], os.environ["ODOO_DB"]
user, key = os.environ["ODOO_USER"], os.environ["ODOO_API_KEY"]
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, user, key, {})
if not uid:
    sys.exit("No se pudo autenticar en Odoo")
m = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object", allow_none=True)


def call(model, method, *args, **kw):
    return m.execute_kw(db, uid, key, model, method, list(args), kw)


filas = list(csv.DictReader(open(os.path.join(AQUI, "titulos_respaldo_y_nuevos.csv"), encoding="utf-8")))
ids_shopify = [f["product_id"] for f in filas]

# Capas Shopify en bloque
capas = {}
for i in range(0, len(ids_shopify), 500):
    for c in call("shopify.product.template.ept", "search_read",
                  [["shopify_tmpl_id", "in", ids_shopify[i:i + 500]]],
                  fields=["id", "name", "shopify_tmpl_id", "product_tmpl_id"]):
        capas[c["shopify_tmpl_id"]] = c

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
    if not c or not c["product_tmpl_id"]:
        sin_capa += 1
        out.writerow([f["product_id"], "", "", "", f["titulo_nuevo"], f["liquidacion"], "sin capa Shopify en Odoo"])
        continue
    tmpl_id, tmpl_name = c["product_tmpl_id"]
    estado = "simulado"
    if APLICAR:
        call("shopify.product.template.ept", "write", [c["id"]], {"name": f["titulo_nuevo"]})
        vals = {"name": f["titulo_nuevo"]}
        if f["liquidacion"] == "1" and tag_id:
            vals["product_tag_ids"] = [(4, tag_id)]
        call("product.template", "write", [tmpl_id], vals)
        estado = "aplicado"
    ok += 1
    out.writerow([f["product_id"], c["id"], tmpl_id, tmpl_name, f["titulo_nuevo"], f["liquidacion"], estado])

print(f"{'Aplicados' if APLICAR else 'A aplicar'}: {ok} | sin capa Shopify: {sin_capa} | etiqueta Liquidación id: {tag_id}")
