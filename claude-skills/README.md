# Skills de claude.ai para Odoo (conector propio "Odoo Ventas Guate")

Copias versionadas de las skills de Odoo, migradas del conector de terceros (Pantalytics) al MCP propio (`mcp-server/`).

| Herramienta anterior | Herramienta nueva |
|---|---|
| record_search / record_get | odoo_search / odoo_read |
| record_aggregate | odoo_group |
| record_export | odoo_export (usar `/.id` para ids numéricos) |
| record_create / records_create | odoo_create (dict o lista, máx. 200) |
| record_update | odoo_write |
| method_execute | odoo_action (solo administradores) |
| message_post | odoo_post_note |
| binary_field_set | odoo_attach_from_url (o odoo_write image_1920 para administradores) |
| — | odoo_register_payment, odoo_set_image_from_url |

Subir a claude.ai: Configuración → Capacidades → Skills → eliminar la versión anterior → subir el `.zip` de `dist/`.
