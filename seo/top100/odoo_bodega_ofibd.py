"""Agrega OFI BODEGA 13 (id 26) a las bodegas que exportan stock a Shopify y calcula stock exportable de productos ocultos."""
import json, os, ssl, sys, urllib.request
url, db, user, key = (os.environ[k] for k in ("ODOO_URL", "ODOO_DB", "ODOO_USER", "ODOO_API_KEY"))
_ctx = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
def _rpc(s, m, *a):
    b = json.dumps({"jsonrpc": "2.0", "method": "call", "id": 1, "params": {"service": s, "method": m, "args": list(a)}}).encode()
    with urllib.request.urlopen(urllib.request.Request(f"{url}/jsonrpc", b, {"Content-Type": "application/json"}), context=_ctx, timeout=180) as r:
        res = json.load(r)
    if res.get("error"): raise RuntimeError(json.dumps(res["error"])[:400])
    return res["result"]
uid = _rpc("common", "authenticate", db, user, key, {})
call = lambda m, meth, *a, **kw: _rpc("object", "execute_kw", db, uid, key, m, meth, list(a), kw)
loc = call("shopify.location.ept", "read", [1], fields=["export_stock_warehouse_ids"])[0]
print("antes:", loc["export_stock_warehouse_ids"])
if "--aplicar" in sys.argv and 26 not in loc["export_stock_warehouse_ids"]:
    call("shopify.location.ept", "write", [1], {"export_stock_warehouse_ids": [(4, 26)]})
print("después:", call("shopify.location.ept", "read", [1], fields=["export_stock_warehouse_ids"])[0]["export_stock_warehouse_ids"])
# stock exportable (free_qty en BD3, TVGDC, OFIBD) de productos ocultos
A = json.load(open("inactivos_shopify.json"))
for x in A:
    pp = call("product.product", "search", [["product_tmpl_id", "=", x["tmpl_id"]]], context={"active_test": False})
    tot = 0
    for wh in (1, 2, 26):
        tot += sum(q["free_qty"] for q in call("product.product", "read", pp, fields=["free_qty"], context={"warehouse_id": wh}))
    x["stock_exportable"] = tot
json.dump(A, open("inactivos_shopify.json", "w"), ensure_ascii=False, indent=1)
print(sum(1 for x in A if x["stock_exportable"] > 0), "de", len(A), "con stock exportable")
