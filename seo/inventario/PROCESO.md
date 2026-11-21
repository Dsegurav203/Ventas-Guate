# Cruce semanal de inventario Odoo ↔ Shopify (aprobado por Diego 2026-11-21)

Lunes 5:31 Guatemala, tarea programada. Fuente de verdad: **Odoo**, existencia libre (cantidad − reservada) en BD3, TVGDC y OFIBD. Shopify tiene una sola ubicación: Tienda Ventas Guate (`gid://shopify/Location/84277264597`).

## Por qué existe
La exportación automática del conector (cron 96) solo envía productos con movimientos nuevos. Productos ligados después de recibir mercadería, o sin movimientos desde la última exportación, quedan desfasados (21/11/2026: 47 productos con existencia salían agotados, p. ej. LAUT Huex AirPods 352 u.).

## Pasos
1. `D=seo/inventario/$(date +%F)`; `python3 odoo-cli/reports/stock_shopify_cruce.py ids $D`
2. Guardar en `$D/paginas/` las respuestas `data` de Shopify con el nodo
   `legacyResourceId inventoryPolicy inventoryQuantity product{ legacyResourceId status title onlineStoreUrl } inventoryItem{ legacyResourceId tracked }`:
   - `odoo_NN.json`: `nodes(ids:[…])` por cada lote de `$D/ids_odoo.json`
   - `shop_NN.json`: `productVariants(first:100, after:$c, query:"inventory_quantity:>0")` paginado
   (usar un subagente para no saturar el contexto)
3. `python3 odoo-cli/reports/stock_shopify_cruce.py comparar $D` → `resumen.md`, `detalle.csv`, `ajustes.json`
4. Aplicar cada lote de `ajustes.json` con `inventorySetQuantities` (`name:"available"`, `reason:"correction"`, `@idempotent(key:"vg-cruce-<fecha>-<n>")`). `changeFromQuantity` = valor leído: si Shopify cambió entre la lectura y el ajuste (venta en curso), esa línea falla y se deja para la próxima semana.
   - **Detenerse y pedir confirmación a Diego** si hay > 300 ajustes, o algún ajuste > 200 unidades, o la sobreventa total > 500 unidades (indica un problema de fondo, no un desfase).
5. Commit de `$D` (sin `paginas/`) y mensaje a Diego: tabla del resumen + sin ligar + ligados a archivados.

## Excluidos
Fichas "Reserva" (inventario manual a propósito), variantes con política CONTINUE, productos DRAFT/ARCHIVED.

## Pendientes que el cruce reporta (no corrige solo)
- Variantes publicadas sin capa del conector → ligar por SKU/código de barras (crear `shopify.product.template.ept` + `shopify.product.product.ept`, ver `seo/agotados/capas_creadas_2026-11-21.json`).
- Variantes ligadas a productos archivados en Odoo → ocultar de la tienda (Diego/Luis en Admin).

## Registro
- 2026-11-21: primer cruce aplicado (154 ajustes). Ligadas 72 variantes publicadas por SKU (`2026-11-21/ligar_aplicado.json`) y corregidas 39 cantidades (p. ej. Protection Pro Ultra HD Small 1,775 → 319, Omni TC Small 825 → 0). Omitidas 154: 113 sin código en Odoo (102 son iPhone por número de serie/IMEI), 24 cuyo producto de Odoo ya está ligado a otra ficha (duplicados en Shopify, p. ej. HiFuture FlexClip), 17 sin SKU en Shopify. Detalle en `2026-11-21/ligar_propuesta.json`.
