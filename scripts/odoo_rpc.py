"""Cliente mínimo de Odoo por JSON-RPC (funciona detrás del proxy de la nube).

Uso:
    from odoo_rpc import call
    call("product.template", "search_read", [["name", "ilike", "laut"]], fields=["id", "name"], limit=5)

Credenciales en variables de entorno: ODOO_URL, ODOO_DB, ODOO_USER, ODOO_API_KEY.
Cada persona usa su propio usuario y clave de API (los cambios quedan a su nombre).
"""
import json
import os
import ssl
import time
import urllib.error
import urllib.request

URL = os.environ["ODOO_URL"].rstrip("/")
DB = os.environ["ODOO_DB"]
USER = os.environ["ODOO_USER"]
KEY = os.environ["ODOO_API_KEY"]
_CA = "/root/.ccr/ca-bundle.crt"
_CTX = ssl.create_default_context(cafile=_CA) if os.path.exists(_CA) else ssl.create_default_context()


def _rpc(service, method, *args, intentos=5):
    body = json.dumps({"jsonrpc": "2.0", "method": "call", "id": 1,
                       "params": {"service": service, "method": method, "args": list(args)}}).encode()
    for i in range(intentos):
        try:
            req = urllib.request.Request(f"{URL}/jsonrpc", body, {"Content-Type": "application/json"})
            with urllib.request.urlopen(req, context=_CTX, timeout=180) as r:
                res = json.load(r)
            if res.get("error"):
                raise RuntimeError(json.dumps(res["error"])[:800])
            return res["result"]
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            if i == intentos - 1:
                raise
            time.sleep(5 * (i + 1))


UID = _rpc("common", "authenticate", DB, USER, KEY, {})
if not UID:
    raise SystemExit("No se pudo autenticar en Odoo (revisa ODOO_USER / ODOO_API_KEY)")


def call(model, method, *args, **kw):
    """execute_kw: call('res.partner', 'search_read', domain, fields=[...], limit=10)."""
    return _rpc("object", "execute_kw", DB, UID, KEY, model, method, list(args), kw)
