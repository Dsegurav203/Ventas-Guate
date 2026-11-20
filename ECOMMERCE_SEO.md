# Ventas Guate · ecommerce y SEO (ventasguate.gt)

Contexto y reglas para cualquier sesión de Claude que trabaje en la tienda en línea **ventasguate.gt** (Shopify) y su catálogo en **Odoo 18** (ventasguate.odoo.com). Empresa: Buyitwithus, S.A. (Ventas Guate). Responsable de ecommerce: Luis Hernández. Dueño: Diego Segura.

Responder en español, directo, con tablas o viñetas. Textos para clientes con "tú".

## Reglas obligatorias

1. **Aprobación antes de escribir** en Shopify u Odoo: mostrar qué cambia (tabla o archivo de propuesta) y esperar un "aprobado". Leer es libre.
2. **Respaldo antes de cambiar**: guardar el valor anterior en `seo/<tema>/…respaldo….json|csv` y registrar lo aplicado en un `.md` de la misma carpeta. Todo debe ser reversible.
3. **No inventar datos**: especificaciones solo de la fuente oficial del fabricante o de un producto hermano ya publicado. Si no hay fuente, no se escribe (marcar "SIN FUENTE").
4. **Sin precios** en descripciones, metas SEO ni textos de colección (cambian y quedan desactualizados).
5. **Títulos**: marca + modelo + compatibilidad + color, con mayúscula inicial (nunca TODO EN MAYÚSCULAS, nunca prefijos como "L-"). Todo cambio de título en Shopify se replica en Odoo (ver "Sincronización").
6. **Conector Odoo→Shopify**: nunca exportar con "Set Basic Detail" (sobrescribe títulos y descripciones de la tienda).
7. **Tema**: editar solo el tema publicado (role MAIN; hoy "Fix Buscador + Error Popup", `gid://shopify/OnlineStoreTheme/187700674773` — verificar con la consulta de temas). Si alguien editó el tema en el editor de Shopify después de un `theme_commit`, `theme_publish` se rechaza (`changed_on_shopify`): **no forzar**; aplicar el cambio en Admin → Editar código.
8. **Credenciales** solo en variables de entorno (`ODOO_URL`, `ODOO_DB`, `ODOO_USER`, `ODOO_API_KEY`) o `.env` (está en `.gitignore`). Nunca en archivos del repo ni en mensajes.
9. **No tocar DNS** ni políticas legales por API (no hay permiso `write_legal_policies`; se editan a mano en Admin → Configuración → Políticas).
10. Commits en español, con respaldo y registro; no crear PR salvo que se pida.

## Datos oficiales del negocio (usar tal cual)

| Dato | Valor |
|---|---|
| Dirección | 9a Calle 15-45 zona 13, Edificio Trafalgar, Oficina 102, Ciudad de Guatemala |
| Horario | Lunes a jueves 9:00–18:00 · Viernes 9:00–17:00 · Sábado 9:00–13:00 |
| WhatsApp | 4027-3277 (`https://wa.me/50240273277`) · Correo pedidos@ventasguate.gt |
| Envío | Ciudad de Guatemala mismo día Q25 · Interior próximo día Q35 · pago contra entrega · entrega garantizada y respaldada |
| Garantía | Nuevos 1 año (defectos de fabricación) · Seminuevos 30 días · Devoluciones 15 días sin abrir · Ofertas sin cambio ni devolución |
| Marcas oficiales | JBL, Reebok, Prodigee, LAUT, LOGiiX, Tucano, Targus, Sudio, OhSnap, Nimbus9, Click, Mello, Protection Pro, Reelcharge |
| Otros canales | Pacifiko, Kemik, Max, Walmart, Guatemala Digital |
| Fundada | 2011 · NIT 7606692-4 |

Cierre estándar de descripciones: `Producto original con 1 año de garantía. Envío a toda Guatemala con pago contra entrega, o cómpralo en nuestra tienda en zona 13, Ciudad de Guatemala.` (seminuevos: 30 días).

## Plantilla de contenido

- **Producto**: `<p>` intro 1–2 frases → `<h2>Características</h2>` + 4–7 viñetas verificadas → `<h2>Compatibilidad</h2>` (si aplica) → cierre estándar. 90–180 palabras. SEO title ≤ 60 caracteres (termina en "| Ventas Guate" si cabe), meta ≤ 155.
- **Colección**: intro con la palabra clave → H2 por modelo/marca/uso → enlaces a colecciones relacionadas → `<h2>Preguntas frecuentes</h2>` (2–4). 90–200 palabras.
- **Imagen**: 1200×1200, fondo blanco, JPEG < 350 KB, sin marcas de agua; validar modelo y color viéndola antes de cargar.

## Fuentes oficiales de fabricante (catálogo JSON de Shopify)

| Marca | Fuente |
|---|---|
| LOGiiX | `https://logiix.ca/products.json?limit=250` |
| LAUT | `https://www.itslaut.com/products.json?limit=250` (el código de barras coincide con el EAN de Odoo) |
| HiFuture | `https://hifuturegroup.com/pages/...` (descargar con curl) |
| Tucano | `https://www.tucano.com` (buscar por EAN) |
| Prodigee | `prodigee.com` suele estar bloqueado desde la nube; usar productos hermanos ya publicados |

## Sincronización Shopify ↔ Odoo

- Capa del conector: `shopify.product.template.ept` (`name`, `shopify_tmpl_id`, `product_tmpl_id`). Al cambiar un título: escribir `name` en la capa **y** en `product.template`. Script de referencia: `seo/top100/odoo_titulos_fase1.py`.
- Productos sin capa: emparejar por SKU (`product.product.default_code`).
- Inventario hacia Shopify: bodegas **BD3, TVGDC y OFI BODEGA 13** (`shopify.location.ept` id 1). APW queda fuera a propósito.
- Reservas (colección `reservas`, etiqueta `Reserva`): las fichas "Reserva iPhone …" llevan inventario manual sin SKU a propósito para permitir reservar; no ponerlas en 0. Cualquier otro producto con etiqueta `Reserva` y sin stock en Odoo se saca de la colección.
- Liquidación: etiqueta de producto "Liquidación" (product.tag id 1) + categoría PdV "Liquidación" (pos.category id 10) en Odoo; etiqueta `liquidacion` en Shopify.
- Consultas y cambios puntuales en Odoo: usar el CLI `./odoo` (ver `CLAUDE.md` y `odoo-cli/README.md`). Scripts masivos de catálogo en `seo/`: JSON-RPC con `urllib` vía `scripts/odoo_rpc.py` (en la nube: CA `/root/.ccr/ca-bundle.crt`; `xmlrpc` no respeta el proxy).

## Notas de la API de Shopify (Admin GraphQL 2026-10)

- Documento máximo 16,384 caracteres: mandar el contenido en `variables`, no dentro del query.
- `productUpdate(product: ProductUpdateInput)`; imágenes nuevas con `productUpdate(product:{id, media:[…]})` tras `stagedUploadsCreate` (`productCreateMedia` ya no existe).
- `collectionUpdate(collection: CollectionUpdateInput)`; `collectionCreate` usa `sources` (ruleSet/input obsoletos).
- Alt text: `fileUpdate(files:[{id, alt}])` hasta 100 por llamada. Imágenes compartidas entre productos: alt neutro (sin color/talla).
- Ocultar de Google: metafield `seo.hidden` = 1 (number_integer). Al borrar una página, crear `urlRedirectCreate` 301.
- Conexiones: máximo 100 por página.

## Dónde está cada cosa

Ver `ONBOARDING.md` (guía para Luis), `CLAUDE.md` (Odoo, KPIs, seguridad) y la carpeta `seo/` (un subdirectorio por tema, con respaldo, propuesta y registro de lo aplicado). Habilidades del proyecto en `.claude/skills/`.
