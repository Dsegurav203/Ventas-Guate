# Fotos LAUT y publicación en ventasguate.gt (22/11/2026)

Aprobado por Diego Segura el 22/11/2026. Solo se agregaron imágenes y se publicó en la tienda en línea (`gid://shopify/Publication/164168564949`). No se cambiaron títulos, precios, descripción ni Odoo.

## Fuente
Catálogo oficial `https://www.itslaut.com/products.json?limit=250&page=1..2` (286 productos). En este catálogo el campo `barcode` viene vacío, así que el emparejamiento se hizo por **SKU de LAUT = `default_code` de Odoo** (el SKU de Shopify es el EAN, que coincide con el `barcode` de Odoo).

| Shopify id | Título | SKU Shopify (EAN) | Odoo `default_code` / `barcode` | Producto LAUT (handle / variante) | Imágenes (archivo oficial) | Publicado |
|---|---|---|---|---|---|---|
| 15480771379413 | LAUT Huex MacBook Neo 13" Pink | 4895206950015 | L_MBN_HX_P / 4895206950015 | `huex-for-macbook-neo` / MacBook Neo 13-inch (2026) / PINK | 1: L_MBN_HX-LS03 (única foto oficial de ese color) | Sí |
| 15480771412181 | LAUT Huex MacBook Neo 13" Yellow | 4895206950008 | L_MBN_HX_Y / 4895206950008 | `huex-for-macbook-neo` / MacBook Neo 13-inch (2026) / YELLOW | 1: L_MBN_HX-LS04 (única foto oficial de ese color) | Sí |
| 15480775442645 | LAUT Links 2.0 Apple Watch 42/44/45/49mm Silver | 4895206934008 | L_AWL_L2_SL / 4895206934008 | `links-2-0-watch-strap-for-apple-watch-series-1-8-se-ultra` / 49/46/45/44mm / Silver | 3: L_AW_LI2_SL01, SL02, SL03 | Sí |
| 15480775475413 | LAUT Huex Protect MacBook Air 13" (2022) Black | 4895206937269 | L_MA22_HPT_BK / 4895206937269 | `huex-protect-case-for-macbook-pro-macbook-air` / MacBook Air 13-inch (2022 Model) / FROST BLACK | 3: L_MA22_HPT_BK04, BK05, BK06 | Sí |

## Proceso
- Originales (2000×2000) en `raw/<id>/`; normalizadas 1200×1200, fondo blanco, JPEG q88 (47–164 KB) en `<id>/`. Revisadas visualmente: modelo y color correctos, sin marcas de agua.
- `stagedUploadsCreate` (IMAGE/POST/image/jpeg) → curl 201 ×8 → `productUpdate(product:{id}, media:[…])` con alt = título → estado READY.
- `publishablePublish` sin errores; `publishedOnPublication = true` en los 4.
- Inventario en Shopify al publicar: Pink 20, Yellow 20, Links 2.0 Silver 50, Huex Protect MA22 Black 15.

## Reversión
Despublicar: `publishableUnpublish(id, input:[{publicationId:"gid://shopify/Publication/164168564949"}])`. Quitar fotos: `productDeleteMedia` (antes no tenían media: `mediaCount = 0`).

## Pendiente
- En Odoo no se revisó ni cambió `image_1920` (no se pidió); si faltan, se pueden cargar con los mismos archivos de `<id>/`.
