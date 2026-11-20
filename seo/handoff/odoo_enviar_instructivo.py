"""Envía por correo desde Odoo el instructivo de liquidación a los usuarios internos.

Uso:
    python3 odoo_enviar_instructivo.py            # muestra destinatarios, no envía
    python3 odoo_enviar_instructivo.py --enviar   # envía
Credenciales: ODOO_URL, ODOO_DB, ODOO_USER, ODOO_API_KEY (variables de entorno).
"""
import base64
import json
import os
import ssl
import sys
import urllib.request

ENVIAR = "--enviar" in sys.argv
AQUI = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(AQUI, "Instructivo_Liquidacion_VentasGuate.pdf")
# Usuarios técnicos o externos que no reciben el correo
EXCLUIR = {"api-dropship@ventasguate.com", "claude.lectura@ventasguate.com", "soporte@noduu.com"}

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


def call(model, method, *args, **kw):
    return _rpc("object", "execute_kw", db, uid, key, model, method, list(args), kw)


usuarios = call("res.users", "search_read", [["share", "=", False], ["active", "=", True]],
                fields=["name", "login", "email", "partner_id"])
dest = [u for u in usuarios if (u["login"] or "").lower() not in EXCLUIR and u["email"]]
print(f"Destinatarios ({len(dest)}):")
for u in dest:
    print(f"  - {u['name']} <{u['email']}>")

ASUNTO = "Cambio en productos de liquidación: ya no llevan \"L-\" (instructivo y spiff)"
CUERPO = """
<p>Equipo:</p>
<p>Desde hoy, <b>18 de noviembre de 2026</b>, los productos de liquidación <b>ya no llevan "L-" en el nombre</b>, ni en Odoo ni en la tienda en línea.</p>
<p><b>Cómo se identifican ahora:</b></p>
<ul>
  <li><b>Odoo (Ventas, Inventario, Compras):</b> etiqueta de producto <b>Liquidación</b>. En la lista de productos, escriban "Liquidación" en el buscador y elijan <i>Buscar Etiquetas de producto</i>.</li>
  <li><b>Punto de Venta (todas las tiendas):</b> categoría <b>Liquidación</b> en la barra de categorías de la caja.</li>
  <li><b>Tienda en línea:</b> ventasguate.gt/collections/liquidacion</li>
</ul>
<p><b>Spiff de liquidación:</b> desde hoy, una venta cuenta como liquidación si el producto tiene la etiqueta o la categoría de PdV <b>Liquidación</b>, no por el "L-". El adjunto explica paso a paso cómo sacar el reporte por vendedor en Punto de Venta y en Ventas.</p>
<p><b>Reglas:</b> no volver a escribir "L-" en los nombres. Para poner un producto en liquidación, agréguenle la etiqueta y la categoría; para sacarlo, quítenlas. El nombre y el código no cambian.</p>
<p>Adjunto el instructivo completo (PDF, 2 páginas). Cualquier duda, conmigo.</p>
<p>Diego Segura</p>
"""

if not ENVIAR:
    print("\nSimulación: no se envió nada. Use --enviar para enviar.")
    sys.exit(0)

att = call("ir.attachment", "create", {
    "name": "Instructivo_Liquidacion_VentasGuate.pdf",
    "datas": base64.b64encode(open(PDF, "rb").read()).decode(),
    "mimetype": "application/pdf",
})
mail_id = call("mail.mail", "create", {
    "subject": ASUNTO,
    "body_html": CUERPO,
    "recipient_ids": [(6, 0, [u["partner_id"][0] for u in dest])],
    "attachment_ids": [(6, 0, [att])],
    "auto_delete": False,
})
call("mail.mail", "send", [mail_id])
estado = call("mail.mail", "read", [mail_id], fields=["state", "failure_reason", "email_from"])
print("Correo:", estado)
