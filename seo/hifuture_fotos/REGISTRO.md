# HiFuture: fotos para productos sin imagen (22/11/2026)

Aprobado por Diego Segura. Fuente: catálogo oficial `https://hifuturegroup.com/products.json?limit=250` (66 productos; imagen de la variante de color + imágenes generales revisadas visualmente). Normalizadas a 1200×1200 JPEG < 350 KB en `seo/hifuture_fotos/<shopify_id>/`. Alt = título del producto. No se cambiaron títulos, precios, descripciones ni publicación.

## Detección
Shopify, vendor/título HiFuture, estado ACTIVE, `mediaCount` = 0: **12 productos**. (Además 3 ARCHIVED sin foto, fuera de alcance: Active2 Black 6972576183224, Aura Gold 6972576181190, Zone2 Rose Gold 6972576181169.)

## Aplicado en Shopify (10 productos, 32 imágenes, todas READY)

| Shopify id | Producto | SKU | Inv. | Fuente (handle oficial / imágenes) | Fotos |
|---|---|---|---|---|---|
| 9613271236821 | Audífonos HiFuture SoniCore ANC – Azul | 6972576182975 | 40 | /products/soniccore · SonicCore_pro7 (variante Blue), SonicCore_pro2, SonicCore_pro3 | 3 |
| 9613273563349 | Smartwatch HiFuture Evo3 – Negro | 6972576183408 | 50 | /products/evo3 · EVO3_PRO_1 (Black), EVO3_PRO_8, EVO3_PRO_6, EVO3_PRO_4 (grupo) | 4 |
| 9613273628885 | Smartwatch HiFuture Evo3 – Rose Gold | 6972576183422 | 0 | /products/evo3 · EVO3_PRO_2 (RoseGolden), EVO3_PRO_9, EVO3_PRO_4 (grupo) | 3 |
| 9613273694421 | Smartwatch HiFuture Evo3 – Silver | 6972576183415 | 18 | /products/evo3 · EVO3_PRO_3 (Silver), EVO3_PRO_7 (IP68), EVO3_PRO_4 (grupo) | 3 |
| 9613273727189 | Bocina HiFuture Lino S – Negro | 6972576182838 | 34 | /products/lino-s · linoS_pro10 (Black), linoS_pro4, linoS_pro3 | 3 |
| 9613273792725 | Bocina HiFuture Lino S – Azul | 6972576182869 | 16 | /products/lino-s · linoS_pro9 (Blue), linoS_pro3 | 2 |
| 9613273858261 | Bocina HiFuture Lino S – Verde | 6972576182845 | 17 | /products/lino-s · linoS_pro11 (Green), linoS_pro1, linoS_pro4 | 3 |
| 9613274153173 | Bocina HiFuture Passion S – Negro | 6972576182951 | 33 | /products/passion-s · PassionS_pro_3.png (Black), PassionS_pro2, PassionS_pro7, PassionS_pro3 | 4 |
| 9613274218709 | Bocina HiFuture Passion S – Latte | 6972576182944 | 35 | /products/passion-s · PassionS_pro_4.png (Latte), PassionS_pro5, PassionS_pro1 | 3 |
| 9613274349781 | Audífonos HiFuture Sonify2 Open Ear – Navy Blue | 6972576183255 | 24 | /products/sonify2 · SONIFY2_PRO_1 (Blue), SONIFY2_PRO_8, SONIFY2_PRO_7, SONIFY2_PRO_4 | 4 |

URL base de las fotos: `https://cdn.shopify.com/s/files/1/0719/4630/5835/files/<archivo>` (catálogo de hifuturegroup.com). Archivo local: `<orden>_<handle>_<posición en products.json>.jpg`.

## Odoo
Las 12 plantillas ya tenían `image_1920` → **no se escribió nada** (respaldo/estado en `respaldo_odoo.json`). Observaciones: Lino S Azul (tmpl 14180) tiene imagen 400×400 con marco negro; Lino S Verde/Passion S Negro 300×300; Evo3 Rose Gold 500×500. Se podrían reemplazar por la foto oficial si se aprueba.

## Sin subir (pendiente)

| Shopify id | Producto | SKU | Inv. | Motivo |
|---|---|---|---|---|
| 9613274284245 | Audífonos HiFuture Sonify2 Open Ear – Negro | 6972576183248 | 29 | **Conflicto de color**: en Odoo el código 6972576183248 es "Sonify2 … Latte" (y su foto es Latte); HiFuture solo ofrece Sonify2 en Latte y Blue (no existe negro). Corregir título de Shopify a Latte (confirmar con producto físico) y luego subir SONIFY2_PRO_2. |
| 15529159065813 | HiFuture Wm200 Micrófono Inalámbrico Grey | 6972576183545 | 20 | **SIN FUENTE**: el WM200 no está en hifuturegroup.com (products.json y /products/wm200 → 404). Odoo tiene foto de la caja (origen desconocido); no se usó. |

## Errores
Ninguno (32 uploads HTTP 201; 10 productUpdate sin userErrors).

## 22/11/2026 (aprobado por Diego)
- Odoo: reemplazada image_1920 (foto oficial) en Lino S Verde (14179), Lino S Azul (14180), Passion S Negro (14177), Evo3 Rose Gold (14183). Respaldo de las anteriores en `odoo_respaldo_imagenes/`.
- Active2 Black (Shopify 9613273432277): reactivado (ARCHIVED → ACTIVE), título "Smartwatch HiFuture Active2 – Negro" (también en capa 4269 y product.template 13901; respaldo `respaldo_titulo_active2.json`), 4 fotos oficiales (hifuturegroup.com/products/active-2: pro2, pro4, pro8, pro3) y publicado en Tienda online. Sin descripción todavía.
- Sonify2 (Shopify 9613274284245, SKU 6972576183248): Diego confirmó que en bodega solo hay Azul y Latte → la ficha "Negro" era Latte. Título "Audífonos HiFuture Sonify2 Open Ear – Latte" (Shopify, capa y product.template), handle `hifuture-sonify2-open-ear-latte` con 301 desde el anterior, SEO title Latte, descripción en tú con cierre estándar, 4 fotos oficiales Latte (SONIFY2_PRO_2, _5, _3, _6).
