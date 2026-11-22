# Registro de publicación · fichas iTronics, Prodigee y Tucano

**Fecha:** 2026-11-21/22 · **Aprobación:** Diego Segura (21/11/2026) · **Estado:** PARCIAL (detenida)

## Respaldo previo
- `respaldo_previo_publicacion_2026-11-21.json`: `descriptionHtml` + `seo` + `updatedAt` leídos de Shopify justo antes de publicar, de las 208 fichas de las 3 propuestas + Saddle Bag Tucano; en `solo_meta_seo`, las 2 fichas Tucano con precio en la meta (Saddle Bag y Travel Adapter 100W).
- Comparación con `*_respaldo.json` (espacios normalizados): **209/209 iguales**. No se omitió ninguna ficha por cambios desde la propuesta.

## Aplicado (productUpdate, solo `descriptionHtml`)
| Marca | Propuestas con html | Aplicadas | Pendientes |
|---|---|---|---|
| iTronics (seminuevos) | 99 (7 con html nulo, no se tocan) | **72** (lotes 00–08) | 27 |
| Prodigee (`descriptionHtml` + SEO) | 64 | 0 | 64 |
| Tucano (`descriptionHtml` + SEO) | 45 | 0 | 45 |

- userErrors en los lotes aplicados: **0** (72/72 OK).
- El lote 09 (8 fichas iTronics: iPhone 16 128GB Negro, Verde azulado, Ultramar, Rosa, Blanco; 16 256GB Negro; 16 Plus 256GB Ultramar; 16 Pro Max 256GB Titanio blanco) fue **denegado por el usuario** en la confirmación de la herramienta. Se detuvo la publicación ahí; no se reintentó.

## No hecho (pendiente de decisión)
- 136 fichas restantes (lotes 09–25): 27 iTronics, 64 Prodigee, 45 Tucano.
- Meta SEO sin precio (paso 3), NO aplicada. Valores propuestos:
  - Tucano Let Me Out Foldable Saddle Bag Negro (`gid://shopify/Product/9386244473045`): actual "Bolso plegable Tucano Let Me Out Saddle Bag negro en liquidación a Q275 (antes Q649). Liviano y resistente al agua. Compra en Ventas Guate." → propuesta "Bolso plegable Tucano Let Me Out Saddle Bag negro. Liviano y resistente al agua. Compra en Ventas Guate."
  - Tucano Travel Adapter Gan 100W Blanco (`gid://shopify/Product/9149956128981`): actual "Adaptador de viaje Tucano GaN 100W universal en Guatemala. Carga rápida para laptop, tablet y celular. ✓ Original. Q365." → propuesta "Adaptador de viaje Tucano GaN 100W universal en Guatemala. Carga rápida para laptop, tablet y celular. ✓ Original."
- Otras metas con precio vistas en el respaldo (se corregirían con la SEO de la propuesta Tucano/Prodigee si se publica): Prodigee Balance lavanda (Q115), Tucano Gommo Rolltop azul (Q215), Let Me Out Crossbody azul (Q165) y verde (Q155), Desk Pad azul (Q95), Gommo Sleeve Superslim 16 gris (Q399), Gommo Sleeve 13/14 negro (Q299), Isotta Superslim 16 (Q599), Gommo City Backpack azul/gris (Q699), Gommo Shopper azul (Q549) y negro (Q149).

## Verificación
- iTronics: se leyeron 3 fichas publicadas (iPhone 8 Plus 64GB Gris, iPhone 13 128GB Verde, iPhone 16e 128GB Blanco) y el texto coincide con la propuesta (Shopify solo agrega saltos de línea entre `<li>`). Título y SEO sin cambios.
- Prodigee y Tucano: sin verificar porque no se publicó nada de esas marcas.

## Cómo revertir
Para cada id aplicado, `productUpdate(product:{id, descriptionHtml})` con el valor de `respaldo_previo_publicacion_2026-11-21.json` → `productos[]` (las 72 aplicadas son las primeras 72 entradas de iTronics, en el mismo orden). El SEO de iTronics no se modificó.
