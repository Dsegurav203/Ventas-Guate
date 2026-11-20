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
fix = json.load(open("fase1_titulos_corregidos.json"))
for gid, (viejo, nuevo) in fix.items():
    sid = gid.split("/")[-1]
    capas = call("shopify.product.template.ept", "search_read", [["shopify_tmpl_id", "=", sid]], fields=["id", "name", "product_tmpl_id"], context={"active_test": False})
    for c in capas:
        call("shopify.product.template.ept", "write", [c["id"]], {"name": nuevo})
        call("product.template", "write", [c["product_tmpl_id"][0]], {"name": nuevo})
    print(sid, len(capas), "→", nuevo)
