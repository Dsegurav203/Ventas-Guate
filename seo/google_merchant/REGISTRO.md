# Google & YouTube (Merchant Center) — registro

**Fecha:** 2026-11-22 · **Aprobó:** Diego Segura · **Canal:** Google & YouTube (`gid://shopify/Publication/194347630805`)
**Lista y motivos:** `seo/google_merchant/publicar_google.json`

## Criterio
- `status:active published_status:published` (activos y publicados en Tienda online): **1,181** revisados.
- Inventario total > 0, o variante con política CONTINUE + etiqueta `venta-sin-stock` (6 casos, incluidos: Govee TV Backlight 3 Lite, iPhone Pocket Negro, 2 Spidercase S25 FE, Funda Galaxy S21 Ultra, Echo Studio).
- `mediaCount ≥ 1`, precio > 0.
- Sin etiquetas `no-web`, `pendiente-publicar-odoo`, `Out of stock` (0 productos activos/publicados las tienen).
- Título no empieza con "Reserva".

## Resultado
| Concepto | Cantidad |
|---|---|
| Publicados en Google & YouTube (`publishablePublish`, 23 lotes de ≤50) | **1,133** |
| Errores (`userErrors`) | 0 |
| Excluidos: sin imagen (mediaCount = 0) | 30 |
| Excluidos: precio simbólico Q1.00 (placeholder) | 17 |
| Excluidos: título "Reserva …" | 1 |
| Excluidos: etiquetas no-web / pendiente-publicar-odoo / Out of stock | 0 |
| Excluidos: sin stock y sin CONTINUE/venta-sin-stock | 0 |

**Precio Q1.00:** cumplen "precio > 0" literal, pero Q1 es un precio de relleno (HiFuture Flex3/Flybuds4/Lyra/Passion M/MusicSoul200, Smartwatch HiFuture Active2, Targus Chromatic Sleeve ×5, LAUT Links 2.0 y Huex MacBook Air). Publicarlos mostraría Q1 en Google; se dejaron fuera hasta corregir precio.

## Verificación
- `productsCount(query:"status:active published_status:published publication_ids:194347630805")` = **1,150** = 1,133 publicados + 17 excluidos que **ya estaban en el canal antes** de esta corrida.
- Muestra con `publishedOnPublication`: publicados = true; excluidos con precio Q1 = false.
- Nota: `published_status:'Google & YouTube:published'` devuelve 0 siempre (sintaxis no soportada); usar `publication_ids:194347630805`.
- El canal tiene **1,577** productos en total (cualquier estado): ya había publicaciones previas a esta corrida.

## Pendientes / alertas
1. **17 excluidos ya estaban en Google antes** (no los publicó esta corrida): 16 sin imagen (Master Case Redmi 14C/14C ×4, MyBat Stealth S22+, Prodigee Safetee Transforme 13, Safetee Flow Night 11 Pro, Clear Fit A53/A72/A14, 6 iPad seminuevos) y **Reserva iPhone Duo 256GB Blanco**. Diego puede quitarlos desde Admin (Producto → Canales de venta → desmarcar Google & YouTube).
2. ~430 productos del canal no están activos/publicados en la tienda (1,577 − 1,150): revisar en Merchant Center; Google no los muestra si no están en la tienda online, pero conviene limpiarlos.
3. Corregir precio de los 17 con Q1 y cargar imagen a los 30 sin foto; luego publicarlos.

## Cómo revertir
El agente no puede despublicar. Diego: Shopify Admin → Productos → seleccionar → **Más acciones → Excluir de canales de venta → Google & YouTube**, o desactivar el canal completo en Configuración → Apps y canales de venta.

## 22/11/2026 · Precios Q1.00 corregidos (urgente)
- 17 productos publicados en la web tenían precio Q1.00 (placeholder de creación): Active2, LAUT Links 2.0 y Huex Protect MacBook Air, 5 Targus Chromatic Sleeve, HiFuture Flex3 ×2, Flybuds4 AI ×2, Lyra ×2, MusicSoul200, Passion M ×2.
- Se aplicó el precio de lista de Odoo (`precios_odoo_q1.json`): Q249–Q1,799. No hubo pedidos a Q1 desde el 20/11.
- Luego se publicaron en el canal Google & YouTube.
- Regla: todo producto nuevo en Shopify debe revisarse por precio antes de publicarse.

---

# GTIN en variantes de Shopify (barcodes) — registro

**Fecha:** 2026-11-22 · **Aprobó:** Diego Segura · **Propuesta:** `BARCODES.md` / `barcodes_propuesta.json` (solo `aplicar=true`, casos a y b)
**Resultado por variante:** `barcodes_aplicado.jsonl` (`variant_id`, `product_id`, `sku`, `antes`, `despues`, `error`, `lote`)

## Método
- `productVariantsBulkUpdate(productId, variants:[{id, barcodes:[{type, value}]}])`, una llamada por producto, agrupadas con alias (prueba de 3 variantes; luego 1 documento de 40 y 20 documentos de 80 alias + 1 de 36). `barcodes` reemplaza la lista completa: queda **solo el GTIN**.
- Tipo: `UPC` (12 díg.) 1,357 · `EAN` (13 díg.) 323. Casos: (a) barcode vacío 366 · (b) código interno reemplazado 1,314.
- `bulkOperationRunMutation` está bloqueado por la política del conector Shopify; por eso se usaron alias.

## Resultado
| Concepto | Cantidad |
|---|---|
| Variantes actualizadas | **1,680** (1,679 productos) |
| Errores (`userErrors`) | 0 |
| No tocadas (alertas: duplicados/combos) | 69 (siguen `aplicar=false`) |

Prueba inicial (releída): Prodigee Blackout `52237137314005` → UPC 810192100804 (antes `iPh17P-6 9-BLOT-BLK`); HiFuture `52237240828117` → EAN 6974772421926 (antes vacío); SKU `L4251993300844` `52237242400981` → EAN 4251993300844 (antes `53568`).

## Verificación
- Muestra aleatoria de 20 variantes (semilla 20261122) con `nodes(ids)`: 20/20 con `barcodes = [GTIN propuesto]` y tipo correcto.

## Cómo revertir
- El valor anterior está en `barcode_actual` de `barcodes_propuesta.json` (y `antes` en `barcodes_aplicado.jsonl`).
- Por variante: `productVariantsBulkUpdate(productId, variants:[{id, barcodes:[{value:"<antes>"}]}])` (sin `type`, como estaban); si `antes` es null → `barcodes: []`.
- Riesgo pendiente: si el conector Odoo→Shopify exporta `barcode`, podría volver a escribir el código interno. Revisar la próxima exportación (cron 96) y, si pasa, cargar el GTIN en `product.product.barcode` de Odoo.

## 2026-11-22 · Quitar de Google & YouTube (17 productos)
- 16 sin imagen + Reserva iPhone Duo, ya estaban en el canal. `publishableUnpublish` bloqueado por el MCP → etiqueta `quitar-google` aplicada a los 17 para que Diego los excluya en Admin (Productos → filtro etiqueta `quitar-google` → Seleccionar todo → Más acciones → Excluir de canales de venta → Google & YouTube).
- Reversible: quitar la etiqueta (`tagsRemove`) y volver a incluir el canal.
