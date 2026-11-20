"""Aplica los nombres nuevos de seo/handoff/capas_L/respaldo_y_propuesta.csv a las capas del conector Shopify en Odoo."""
import csv, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "scripts"))
from odoo_rpc import call
AQUI = os.path.dirname(os.path.abspath(__file__))
modelo = {"plantilla": "shopify.product.template.ept", "variante": "shopify.product.product.ept"}
ok = err = 0
for r in csv.DictReader(open(os.path.join(AQUI, "respaldo_y_propuesta.csv"), encoding="utf-8")):
    try:
        call(modelo[r["capa"]], "write", [int(r["id"])], {"name": r["nombre_nuevo"]})
        ok += 1
    except Exception as e:
        err += 1; print("error", r["capa"], r["id"], str(e)[:200])
ctx = {"active_test": False}
quedan_t = call("shopify.product.template.ept", "search_count", [["name", "=like", "L-%"]], context=ctx)
quedan_v = call("shopify.product.product.ept", "search_count", [["name", "=like", "L-%"]], context=ctx)
print(f"aplicados {ok}, errores {err}; quedan con L-: plantillas {quedan_t}, variantes {quedan_v}")
