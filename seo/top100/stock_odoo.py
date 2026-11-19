import json, os, ssl, urllib.request
url, db, user, key = (os.environ[k] for k in ("ODOO_URL", "ODOO_DB", "ODOO_USER", "ODOO_API_KEY"))
_ctx = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
def _rpc(s, m, *a):
    b = json.dumps({"jsonrpc": "2.0", "method": "call", "id": 1, "params": {"service": s, "method": m, "args": list(a)}}).encode()
    with urllib.request.urlopen(urllib.request.Request(f"{url}/jsonrpc", b, {"Content-Type": "application/json"}), context=_ctx, timeout=180) as r:
        res = json.load(r)
    if res.get("error"): raise RuntimeError(json.dumps(res["error"])[:600])
    return res["result"]
uid = _rpc("common", "authenticate", db, user, key, {})
call = lambda m, meth, *a, **kw: _rpc("object", "execute_kw", db, uid, key, m, meth, list(a), kw)
A = json.load(open("inactivos_shopify.json")); B = json.load(open("no_existen_shopify.json"))
ids = [x["tmpl_id"] for x in A + B]
st = {t["id"]: t for t in call("product.template", "read", ids, fields=["qty_available", "list_price", "image_1920"] and ["qty_available", "list_price"], context={"active_test": False})}
# imagen presente?
img = {t["id"]: bool(t.get("image_128")) for t in call("product.template", "read", ids, fields=["image_128"], context={"active_test": False})}
for grp, L in (("A", A), ("B", B)):
    for x in L:
        s = st[x["tmpl_id"]]; x["odoo_stock"] = s["qty_available"]; x["odoo_precio"] = s["list_price"]; x["odoo_img"] = img[x["tmpl_id"]]
json.dump(A, open("inactivos_shopify.json", "w"), ensure_ascii=False, indent=1)
json.dump(B, open("no_existen_shopify.json", "w"), ensure_ascii=False, indent=1)
for grp, L in (("A inactivos en Shopify", A), ("B no existen", B)):
    print("##", grp, len(L), "con stock Odoo>0:", sum(1 for x in L if x["odoo_stock"] > 0))
    for x in L:
        print(f"  {x['ventas_q']:>10,.0f} stock {x['odoo_stock']:>6.0f} Q{x['odoo_precio']:>8.0f} img:{'s' if x['odoo_img'] else 'n'} {x.get('status','-'):8} {x['name'][:60]}")
