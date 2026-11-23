# MOFT Carry Sleeve + Hyper HD Flex 9: publicación en ventasguate.gt (2026-11-23)

Aprobado por Diego Segura. Respaldo del estado previo: `respaldo_2026-11-23.json`. Textos aplicados: `contenido.py`.
Antes: vendor "Ventas Guate", sin tipo, sin descripción, sin SEO, sin imagen, etiqueta `pendiente-publicar-odoo`, sin publicar en ningún canal.

## Cambios aplicados en Shopify

| Producto (id) | SKU/barcode · ref. fabricante | Título final | Vendor / tipo | Media | Precio | Stock |
|---|---|---|---|---|---|---|
| 15480774623445 | 6975820900790 · MB002-1-16-PEWH | MOFT Carry Sleeve para Laptop 15 y 16 Pulgadas Beach White | MOFT / Sleeves | MediaImage/47193839599829 | Q549 (sin cambio) | 19 (= Odoo) |
| 15480774656213 | 6972243542309 · MB002-1-13B-BK | MOFT Carry Sleeve para Laptop 14 Pulgadas Negro | MOFT / Sleeves | MediaImage/47193841729749 | Q499 (sin cambio) | 38 (= Odoo) |
| 15480774688981 | 6972243546932 · MB002-1-16-BK | MOFT Carry Sleeve para Laptop 15 y 16 Pulgadas Negro | MOFT / Sleeves | MediaImage/47193913524437 | Q549 (sin cambio) | 19 (= Odoo) |
| 15480775409877 | 6975820900820 · MB002-1-13B-PEWH | MOFT Carry Sleeve para MacBook Air 13 y Laptop 14 Pulgadas Beach White | MOFT / Sleeves | MediaImage/47193913589973 | Q499 (sin cambio) | 40 (= Odoo) |
| 15480780521685 | 810156700729 · HD4103BUGL | Hyper HyperDrive Flex Dock USB-C 9 Puertos Dual 4K HDMI Blanco y Azul | Hyper / Periféricos | MediaImage/47193913721045 | Q1.00 → **Q449.00** (lista Odoo) | 18 → **4** (BD3/Stock libre en Odoo) |

- Descripción según plantilla (intro, Características, Compatibilidad, cierre estándar), 158–179 palabras, sin precios.
- SEO title ≤ 60 y meta ≤ 155 enviados juntos. Etiquetas: se quitó `pendiente-publicar-odoo`; se conservó `cat-sleeves` / `cat-perifericos`.
- Inventario Hyper: `inventorySetQuantities` (available, correction, Location 84277264597, changeFrom 18 → 4). MOFT ya coincidían con Odoo (stock.quant interno libre en BD3), no se tocaron.
- Publicados en Tienda online (Publication/164168564949) y Google & YouTube (Publication/194347630805).
- No se tocó el "Hyper HD Flex 5 Port Dock".

## Imágenes
- Fuente: `image_1920` de Odoo (product.product 13947–13951, 14566). Revisadas: modelo y color coinciden con las fotos de variante del fabricante.
- MOFT: una misma foto por color (negro para 14" y 16"; Beach White para 14" y 16"), igual que en moft.com. El fondo era gris claro (#F3F3F3): se cambió a blanco y se recortó/centró. 1200×1200 JPEG, 39–57 KB.
- Hyper: fondo ya blanco; 1200×1200 JPEG, 29 KB. Alt text con modelo y color.

## Fuentes de especificaciones
- MOFT: https://www.moft.com/products/moft-carry-sleeve (página de producto: 3 en 1, ángulos 15°/25° con elevación 50/80 mm, cuero vegano PU + fibra de vidrio reciclada, almacenamiento de neopreno, compatibilidad y medidas máximas por talla) y `moft.us/products.json` (SKU MB002-1-13B = talla 14", MB002-1-16 = talla 16").
- Hyper: https://www.hypershop.com/products/hyperdrive-flex-9-port-usb-c-hub (Specifications: 2× HDMI 4K60, USB-C PD 100 W, 2× USB-C 5 Gbps, USB-A 5 Gbps, SD/microSD 104 MB/s, audio 3.5 mm, 136×42×14.93 mm, 99 g, 75 % plástico reciclado, requisitos MST/DP Alt Mode). Modelo HD4103BUGL = color "Brilliant Blue" (cuerpo blanco con detalles azules).
- Ningún producto quedó SIN FUENTE.

## Observaciones / pendientes
- **Talla del SKU 6975820900820 (MB002-1-13B-PEWH)**: Odoo lo llama "13.3\" MacBook Air", pero según el fabricante el código 13B es la talla 14" (le queda a MacBook Air 13.3"/13.6"). El título en Shopify refleja ambas cosas. Conviene confirmar físicamente la etiqueta de la caja.
- **Odoo sin actualizar** (esta tarea era solo lectura en Odoo): replicar los 5 títulos nuevos en `product.template` y en la capa `shopify.product.template.ept` (regla 5 de ECOMMERCE_SEO.md) y, si aplica, la marca/vendor.
- Hyper Flex 9 en Odoo se llama "White"; el fabricante lo vende como "Brilliant Blue" (blanco con azul).

## 2026-11-23 · Odoo (aprobado por Diego)
- Títulos replicados en product.template (es_GT y en_US): ids 14024, 14025, 14026, 14028, 14643 (`odoo_titulos_plan.json` con el nombre anterior).
- Capas del conector creadas por SKU para las 5 variantes (`ligar/ligar_aplicado.json`), stock ya igual a Odoo (sin ajustes).
