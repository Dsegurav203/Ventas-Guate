"""Crea en Odoo la tarea para Luis Hernandez: aplicar ficha de tienda (schema) y corrección del blog en el tema."""
import base64, html, json, os, ssl, sys, urllib.request
AQUI = os.path.dirname(os.path.abspath(__file__))
url, db = os.environ["ODOO_URL"], os.environ["ODOO_DB"]
user, key = os.environ["ODOO_USER"], os.environ["ODOO_API_KEY"]
_ca = "/root/.ccr/ca-bundle.crt"
_ctx = ssl.create_default_context(cafile=_ca) if os.path.exists(_ca) else ssl.create_default_context()
def _rpc(service, method, *args):
    body = json.dumps({"jsonrpc": "2.0", "method": "call", "id": 1, "params": {"service": service, "method": method, "args": list(args)}}).encode()
    with urllib.request.urlopen(urllib.request.Request(f"{url}/jsonrpc", body, {"Content-Type": "application/json"}), context=_ctx, timeout=120) as r:
        res = json.load(r)
    if res.get("error"):
        raise RuntimeError(json.dumps(res["error"])[:800])
    return res["result"]
uid = _rpc("common", "authenticate", db, user, key, {})
def call(m, meth, *a, **kw):
    return _rpc("object", "execute_kw", db, uid, key, m, meth, list(a), kw)

snippet = open(os.path.join(AQUI, "store-schema.liquid"), encoding="utf-8").read()
linea = "{%- if template.name == 'index' -%}{%- render 'store-schema' -%}{%- endif -%}"
desc = f"""
<p><b>Objetivo:</b> que Google y las IA (ChatGPT, Gemini) lean los datos de la tienda (dirección, horario, WhatsApp, NIT, 14 marcas oficiales) y que los artículos del blog tengan datos estructurados válidos. El cliente no ve ningún cambio visual.</p>
<p><b>Tiempo estimado:</b> 5–10 minutos. <b>Tema:</b> el publicado, <b>"Fix Buscador + Error Popup"</b>.</p>
<h3>Paso 1: abrir el editor de código</h3>
<ol>
<li>Shopify Admin → <b>Tienda online → Temas</b>.</li>
<li>En el tema publicado ("Fix Buscador + Error Popup") → botón <b>"…"</b> → <b>Editar código</b>.</li>
</ol>
<h3>Paso 2: crear el snippet</h3>
<ol>
<li>En la carpeta <b>Snippets</b> → <b>Agregar un nuevo snippet</b> → nombre: <code>store-schema</code> → Crear.</li>
<li>Pegar <b>todo</b> el código del adjunto <b>store-schema.liquid</b> (también abajo) y <b>Guardar</b>.</li>
</ol>
<h3>Paso 3: llamar el snippet desde theme.liquid</h3>
<ol>
<li>Abrir <b>Layout → theme.liquid</b>.</li>
<li>Buscar (Ctrl+F) <code>&lt;/head&gt;</code>.</li>
<li>Justo en la línea de arriba de <code>&lt;/head&gt;</code> pegar:<br><code>{html.escape(linea)}</code></li>
<li><b>Guardar</b>.</li>
</ol>
<h3>Paso 4: corregir los datos del blog</h3>
<ol>
<li>Abrir <b>Sections → article-template.liquid</b> (alrededor de la línea 351).</li>
<li>Reemplazar estas 3 líneas:
<ul>
<li><code>"articleBody": "{{{{ article.content | strip_html | escape }}}}",</code><br>por<br><code>"articleBody": {{{{ article.content | strip_html | strip_newlines | json }}}},</code></li>
<li><code>"headline": "{{{{ article.title }}}}",</code><br>por<br><code>"headline": {{{{ article.title | json }}}},</code></li>
<li><code>"description": "{{{{ article.excerpt | strip_html | escape }}}}",</code><br>por<br><code>"description": {{{{ article.excerpt | strip_html | strip_newlines | json }}}},</code></li>
</ul></li>
<li><b>Guardar</b>.</li>
</ol>
<h3>Paso 5: verificar</h3>
<ol>
<li>Abrir <a href="https://search.google.com/test/rich-results">https://search.google.com/test/rich-results</a> y probar <b>https://ventasguate.gt</b>: debe aparecer <b>ElectronicsStore</b> (o "Negocio local") sin errores.</li>
<li>Probar también una guía del blog (ej. https://ventasguate.gt/blogs/guias): <b>Article</b> sin errores.</li>
<li>Comentar en esta tarea "Listo" con captura del resultado.</li>
</ol>
<p><b>Importante:</b> no tocar otros archivos. Si algo falla, deshacer con el botón <b>"Versiones anteriores"</b> del archivo en el editor.</p>
<h3>Código del snippet store-schema</h3>
<pre>{html.escape(snippet)}</pre>
"""
vals = {
    "name": "Web: agregar ficha de tienda (schema) y corrección del blog en el tema de Shopify",
    "user_ids": [(6, 0, [8])],
    "description": desc,
    "date_deadline": "2026-11-21",
    "priority": "1",
}
if "--crear" not in sys.argv:
    print("Simulación. Usar --crear"); sys.exit(0)
tid = call("project.task", "create", vals)
att = call("ir.attachment", "create", {"name": "store-schema.liquid", "datas": base64.b64encode(snippet.encode()).decode(),
                                      "res_model": "project.task", "res_id": tid, "mimetype": "text/plain"})
call("project.task", "message_post", [tid], body="Luis, te asigné esta tarea con el paso a paso. Fecha límite: viernes 21/11. — Diego",
     attachment_ids=[att], message_type="comment", subtype_xmlid="mail.mt_comment", partner_ids=[13])
print(call("project.task", "read", [tid], fields=["id", "name", "user_ids", "date_deadline", "project_id"]))
