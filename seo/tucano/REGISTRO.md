# Especial Tucano 50% · ventasguate.gt (aprobado por Diego 2026-11-20)

Vigencia: hasta el 31/12/2026 o agotar existencias. Solo tienda en línea (Odoo/POS sin cambio de precio).

## Aplicado 2026-11-20
| Paso | Detalle |
|---|---|
| Inventario | 46 variantes en Shopify = existencia Odoo en BD3 + TVGDC + OFI BODEGA 13 (886 u). El conector no había enviado el stock de OFI BODEGA 13 (solo envía al haber movimiento). |
| Precios | precio = 50% del precio de lista Odoo (redondeado hacia abajo), precio tachado (compareAt) = precio de lista. 10 productos ya tenían precio menor (algunos bajo costo) y quedaron exactamente al 50%. |
| Publicación | 46 fichas publicadas en Tienda online; Modo Premium 14" (precio estaba en Q1.00) y Gommo slim 13/14 gris pasaron de UNLISTED a ACTIVE. |
| Etiqueta | `especial-tucano-50` en las 46 fichas. |
| Duplicados | 8 fichas viejas (mismo SKU, no ligadas al conector) ARCHIVADAS + redirección 301 a la ficha ligada (ver `duplicados.tsv`). |
| Fotos Shopify | 4 fotos oficiales (tucano.com) en: Isotta 13/14 morado, Isotta 13/14 rosado, Let Me Out Shopper azul, Modo Premium 16", Alunno amarillo. |
| Fotos Odoo | image_1920 en Isotta morado, LMO Shopper azul, Alunno amarillo, Gommo Rolltop azul, LMO Crossbody azul. |
| Artes | `artes/` (hero escritorio y móvil, banner de colección, post y story). Colocación en el tema: manual (tema MAIN bloqueado por API). |

## Respaldo y reversión
- Estado previo de Shopify: `shopify_respaldo_2026-11-20.tsv`; Odoo: `odoo_tucano_2026-11-20.json`.
- Al terminar: `revertir_precios_2027-01-01.json` (precio y compareAt anteriores). Recomendado: regresar al precio de lista Odoo y quitar compareAt, no a los precios viejos bajo costo.
- Pendiente: 3 fichas sin ligar al conector (Isotta 13/14 rosado, Alunno amarillo, Gommo slim 13/14 gris): su inventario no se actualiza solo.
