---
name: imagenes-catalogo
description: Busca la foto oficial de productos sin imagen, la normaliza, la carga en Odoo (image_1920) y la sube a Shopify cuando el producto ya existe allá. Usar cuando pidan "fotos", "imágenes faltantes", "productos sin foto", "carga imágenes en Odoo/Shopify".
---

# Imágenes del catálogo

Sigue `CLAUDE.md`. Referencia: `seo/imagenes/` (resultado LAUT, notas).

## 1. Detectar faltantes
- Odoo: `product.template` activos de la marca con `image_128` vacío (leer `image_128`, nunca `image_1920` en búsquedas masivas).
- Shopify: productos con `mediaCount{count}` = 0. Si Odoo ya tiene imagen real (verla), basta subirla a Shopify.

## 2. Fuente
1. Archivos del proveedor que entregue el equipo.
2. Producto hermano en Odoo con imagen.
3. Catálogo oficial del fabricante (`/products.json` en tiendas Shopify; LAUT itslaut.com coincide por código de barras con el EAN de Odoo; LOGiiX logiix.ca).
4. Si nada sirve: dejar pendiente (no usar fotos de otras tiendas).

## 3. Validar y normalizar
- Descargar, convertir a 1200×1200 fondo blanco JPEG < 350 KB (Pillow) y **ver la imagen** antes de cargar: mismo modelo, mismo color, sin marcas de agua. Si el nombre de Odoo contradice el código de barras (color o talla), reportarlo en vez de cargar.
- Muestras o productos sin código de barras: no cargar sin confirmación.

## 4. Cargar
- Odoo (tras aprobación): `product.template.write([id], {"image_1920": <base64>})`; verificar que `image_128` ya no esté vacío.
- Shopify: `stagedUploadsCreate` (IMAGE, POST) → `curl` con todos los parámetros devueltos (`--form-string`) y `-F file=@…` al final (esperar 201) → `productUpdate(product:{id, media:[{originalSource: resourceUrl, mediaContentType: IMAGE, alt: título}]})` → confirmar estado READY. Ojo: archivos .jpg que en realidad son WebP deben convertirse a JPEG real.
- Registrar en `seo/imagenes/NOTAS.md`.
