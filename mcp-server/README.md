# MCP propio de Odoo — Ventas Guate

Conector remoto para el **chat de claude.ai** (web, escritorio, móvil). Reemplaza al MCP de terceros.

- Cada persona conecta **su** usuario de Odoo + su API key: Odoo aplica sus permisos.
- Inicio de sesión OAuth 2.1 con registro dinámico (lo que pide claude.ai). Sin base de datos: todo va cifrado con `MCP_SECRET_KEY`.
- Solo lectura por defecto. `MCP_ALLOW_WRITE=1` agrega `odoo_create`, `odoo_write` y `odoo_set_image_from_url`, **solo en los modelos de `MCP_WRITE_MODELS`** (productos por defecto; separar con `;`). Odoo igual valida permisos.
- Herramientas: `odoo_whoami`, `odoo_search`, `odoo_count`, `odoo_read`, `odoo_group`, `odoo_fields`, `odoo_models`, `odoo_name_search` (+ `odoo_create`, `odoo_write`, `odoo_set_image_from_url` con escritura).

## Variables

| Variable | Valor |
|---|---|
| `ODOO_URL` | `https://ventasguate.odoo.com` |
| `ODOO_DB` | `rocketgithub-ventasguate-odoo-sh-main-5436798` |
| `MCP_PUBLIC_URL` | URL pública del servicio, ej. `https://odoo-mcp-xxxx.a.run.app` |
| `MCP_SECRET_KEY` | Clave Fernet: `python3 -c "from cryptography.fernet import Fernet;print(Fernet.generate_key().decode())"`. Guardarla como secreto. Cambiarla cierra todas las sesiones. |
| `MCP_ALLOW_WRITE` | `0` (piloto) o `1` |

## Despliegue en Google Cloud Run (~US$0–10/mes con 5 usuarios)

```bash
# Paquete listo para Cloud Shell: ver deploy-cloudshell.sh (Dockerfile en la raíz del paquete)
gcloud run deploy odoo-mcp-vg --source . \
  --region us-central1 --no-invoker-iam-check --min-instances 0 --max-instances 2 \
  --set-env-vars ODOO_URL=https://ventasguate.odoo.com,ODOO_DB=rocketgithub-ventasguate-odoo-sh-main-5436798,MCP_ALLOW_WRITE=0 \
  --set-secrets MCP_SECRET_KEY=odoo-mcp-secret:latest
# luego fijar la URL pública que devolvió el deploy:
gcloud run services update odoo-mcp-vg --region us-central1 --update-env-vars MCP_PUBLIC_URL=https://<url-del-servicio>
```
`--no-invoker-iam-check` es necesario: la protección la da el OAuth del propio servidor (sin token válido, `/mcp` responde 401).

## Alta en claude.ai (una vez, administrador de la organización)

Configuración de la organización → Conectores → Agregar conector personalizado → URL `https://<url-del-servicio>/mcp`.
Cada persona: en el chat, Conectores → "Odoo Ventas Guate" → Conectar → página "Conectar Odoo" → su correo de Odoo + su API key.

## Revocar acceso

- Una persona: revocar su API key en Odoo (efecto inmediato; su sesión muere al renovar, máx. 8 h).
- Todos: cambiar `MCP_SECRET_KEY`.

## Prueba de punta a punta

```bash
MCP_SECRET_KEY=<fernet> MCP_PUBLIC_URL=http://localhost:8765 PORT=8765 MCP_ALLOW_LOCAL_REDIRECTS=1 python3 mcp-server/server.py &
TEST_LOGIN=<correo> TEST_KEY=<api key> python3 mcp-server/test_flow.py http://localhost:8765
```
Resultado 2026-11-18 contra Odoo real: 16/16 pruebas pasan (OAuth, PKCE, rechazo de redirect ajeno y key incorrecta, 401 sin token, herramientas).
