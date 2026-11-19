"""Top productos por venta (12 meses) desde Odoo sale.report y su ID en Shopify. Salida: top_odoo.json"""
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
dom = [["state", "not in", ["draft", "sent", "cancel"]], ["date", ">=", "2025-11-19"]]
g = call("sale.report", "read_group", dom, ["product_tmpl_id", "price_subtotal:sum", "product_uom_qty:sum"], ["product_tmpl_id"],
         orderby="price_subtotal desc", lazy=False, limit=250)
ids = [x["product_tmpl_id"][0] for x in g if x["product_tmpl_id"]]
tm = {t["id"]: t for t in call("product.template", "read", ids, fields=["name", "type", "default_code", "sale_ok"], context={"active_test": False})}
capas = {}
for c in call("shopify.product.template.ept", "search_read", [["product_tmpl_id", "in", ids]], fields=["product_tmpl_id", "shopify_tmpl_id"], context={"active_test": False}):
    capas.setdefault(c["product_tmpl_id"][0], c["shopify_tmpl_id"])
out = []
for x in g:
    if not x["product_tmpl_id"]: continue
    i = x["product_tmpl_id"][0]; t = tm.get(i, {})
    out.append({"tmpl_id": i, "name": t.get("name"), "type": t.get("type"), "sku": t.get("default_code"),
                "ventas_q": round(x["price_subtotal"], 2), "unidades": x["product_uom_qty"], "shopify_id": capas.get(i)})
json.dump(out, open("top_odoo.json", "w"), ensure_ascii=False, indent=1)
print(len(out), sum(1 for o in out if o["shopify_id"]))
for o in out[:40]: print(o["ventas_q"], o["unidades"], o["type"], o["shopify_id"], o["name"])
