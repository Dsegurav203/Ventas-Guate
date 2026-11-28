# Lote 2 fotos adicionales (Prodigee, LAUT, LOGiiX) – propuesta 2026-11-28
- Fuentes oficiales confirmadas por Diego: iamprodigee.com, itslaut.world / itslaut.com, logiix.ca (catálogos `products.json`).
- 60 productos de `prioridad.csv` (≤1 foto, con stock, no resueltos en lote 1). Emparejados por SKU del fabricante (`product.product.default_code` en Odoo ↔ `sku` del catálogo) y revisados viendo cada foto (modelo, número de cámaras, color).
- Resultado: 42 productos con 104 fotos nuevas; 18 sin fuente (motivo en `propuesta_fotos/propuesta.json`). Dudas de modelo/color en el campo `duda`.
- Hojas de contacto: `propuesta_fotos/hoja_01..05.jpg` (gris = actual, verde = propuesta).
- Aprobado por Diego y aplicado el 2026-11-28 (ver abajo), excepto 4 LAUT pendientes.

## 2026-11-28 · Fotos aplicadas en Shopify (aprobado por Diego)
Fuente: `propuesta_fotos/propuesta.json`. Respaldo del media previo (id, alt, posición, url): `respaldo_media_2026-11-28.json`. Detalle aplicado: `aplicado_2026-11-28.json`.
Método: stagedUploadsCreate (IMAGE/POST, 94 subidas HTTP 201) → productUpdate(product:{id}, media:[…]). **94 fotos nuevas en 38 productos, todas READY**, sin fallas ni reintentos. Las nuevas quedan después de la foto existente; en los 4 productos que no tenían foto (LAUT Holo iPhone 16 Pro Max Pearl, LAUT Huex Protect AirPods Pro 2022 Frost, LAUT Huex MacBook Neo 13" Black, LOGiiX Vibrance Braid USB-A to USB-C White) la primera nueva quedó como principal (verificado featuredMedia).

**Pendientes, NO se tocaron** (esperan decisión de Diego, ver campo `duda` en propuesta.json): LAUT Typefolio Keyboard Case Universal 9 a 11 Pulgadas Negro (2 fotos) · LAUT Crystal Matter iPhone 13 Pro Negro (2) · LAUT Crystal Matter iPhone 13 Pro Rojo (2) · LAUT Novi Sport Apple Watch 38/40/41mm Black (4).

| Producto | Fotos antes → después | Media nuevos (gid://shopify/MediaImage/…) |
|---|---|---|
| Prodigee Safetee Flow iPhone 15 Pro Desert | 1 → 3 | 47310221738197, 47310221770965 |
| Prodigee Safetee Flow Galaxy S25 Plus Night Frost | 1 → 4 | 47310221836501, 47310221869269, 47310221902037 |
| Prodigee Safetee Neo iPhone 15 Pro Fuchsia | 1 → 3 | 47310221934805, 47310221967573 |
| Prodigee Safetee Neo iPhone 15 Pro Ocean | 1 → 3 | 47310222000341, 47310222033109 |
| Prodigee Superstar iPhone 16 Pro Rosado | 1 → 4 | 47310222065877, 47310222098645, 47310222131413 |
| Prodigee Safetee Flow iPhone 16 Desert | 1 → 4 | 47310222164181, 47310222196949, 47310222229717 |
| Prodigee Super Glass Camera iPhone 17 Air Black | 1 → 4 | 47310222295253, 47310222328021, 47310222360789 |
| Prodigee Superstar Galaxy S25 Plus Clear | 1 → 4 | 47310222393557, 47310222426325, 47310222459093 |
| Prodigee Superstar Galaxy S25 Clear | 1 → 4 | 47310222491861, 47310222524629, 47310222557397 |
| Prodigee Super Glass Camera iPhone 17 Silver | 1 → 3 | 47310222655701, 47310222688469 |
| Prodigee Super Glass Camera Galaxy S26 / S26 Plus | 1 → 4 | 47310222721237, 47310222754005, 47310222786773 |
| Prodigee Safetee Neo Mag iPhone 13 Menta | 1 → 4 | 47310222852309, 47310222885077, 47310222917845 |
| Prodigee Magneteek iPhone 16 Pro Negro | 1 → 4 | 47310224326869, 47310224359637, 47310224392405 |
| Prodigee Safetee Neo iPhone 15 Pro Max Lila | 1 → 3 | 47310224425173, 47310224457941 |
| Prodigee Magneteek iPhone 16 Pro Blanco | 1 → 4 | 47310224490709, 47310224523477, 47310224556245 |
| LAUT Luxedge iPhone 17 Pro Luxe Brown | 1 → 4 | 47310224589013, 47310224621781, 47310224654549 |
| LAUT Holo iPhone 16 Pro Max Pearl | 0 → 2 | 47310224687317, 47310224720085 |
| Prodigee Super Glass Camera iPhone 17 Glitter Silver | 1 → 3 | 47310225047765, 47310225080533 |
| LAUT Luxedge iPhone 17 Pro Slate Black | 1 → 4 | 47310225146069, 47310225178837, 47310225211605 |
| LAUT Huex Protect AirPods Pro 2022 Frost | 0 → 2 | 47310191100117, 47310191132885 |
| Prodigee Safetee Flow Galaxy S25 Plus Desert | 1 → 4 | 47310191198421, 47310191231189, 47310191263957 |
| Prodigee Safetee Neo iPhone 15 Pro Ruby | 1 → 3 | 47310191296725, 47310191329493 |
| Prodigee Magneteek iPhone 12-12 Pro Negro | 1 → 3 | 47310191395029, 47310191427797 |
| LAUT Huex Protect AirPods 4 Black | 1 → 4 | 47310191460565, 47310191493333, 47310191526101 |
| Prodigee Safetee Neo iPhone 15 Pro Lemon | 1 → 3 | 47310191558869, 47310191591637 |
| Prodigee Safetee Neo iPhone 14 Plus Menta | 1 → 3 | 47310191624405, 47310191657173 |
| Prodigee Super Glass Galaxy S26 Ultra Privacy | 1 → 4 | 47310191722709, 47310191755477, 47310191788245 |
| Prodigee Safetee Neo iPhone 15/14/13 Lemon | 1 → 3 | 47310191853781, 47310191886549 |
| Prodigee Superstar iPhone 15 Pro Rosado | 1 → 3 | 47310191952085, 47310191984853 |
| Prodigee Safetee Neo iPhone 13 Limón | 1 → 4 | 47310192050389, 47310192083157, 47310192115925 |
| Prodigee Pampas Galaxy S25 Ice | 1 → 4 | 47310192148693, 47310192181461, 47310192214229 |
| LAUT Huex MacBook Neo 13" Black | 0 → 1 | 47310192279765 |
| Prodigee Safetee Flow Galaxy S25 Desert | 1 → 4 | 47310192312533, 47310192345301, 47310192378069 |
| Prodigee Super Hero Galaxy S25 Clear | 1 → 4 | 47310192476373, 47310192509141, 47310192541909 |
| Prodigee Safetee Neo iPhone 15 Pro Max Lemon | 1 → 3 | 47310192902357, 47310192935125 |
| Prodigee Safetee Neo iPhone 15/14/13 Ruby | 1 → 3 | 47310193000661, 47310193033429 |
| Prodigee Magneteek iPhone 16 Pro Max Negro | 1 → 4 | 47310193131733, 47310193164501, 47310193197269 |
| LOGiiX Vibrance Braid USB-A to USB-C White | 0 → 1 | 47310193262805 |

- Reversión: borrar los media nuevos de la tabla con `productDeleteMedia(productId, mediaIds)` (o `fileDelete`). La foto original de cada producto no se modificó ni se movió.
