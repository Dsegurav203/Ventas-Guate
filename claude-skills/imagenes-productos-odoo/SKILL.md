---
name: imagenes-productos-odoo
description: Busca, normaliza y carga imágenes de producto en Odoo ventasguate.odoo.com (image_1920) a partir del código UPC/EAN, SKU o nombre; genera una imagen provisional estándar cuando no hay foto. USAR SIEMPRE que Diego pida imágenes, fotos, "buscar imagen del código", productos sin imagen, cargar fotos a Odoo, preparar productos nuevos para Shopify/ventasguate.gt, o después de crear productos con creacion-productos-odoo.
---

# Imágenes de producto

## Estándar de imagen
1200×1200 px, fondo blanco, producto centrado al 90 %, JPEG < 350 KB, sin marcas de agua ni logos de otras tiendas. Script: `scripts/img_producto.py`.

## Orden de búsqueda (parar en la primera fuente válida)
1. **Archivos de Diego/proveedor** subidos al chat o en `/mnt/user-data/uploads`.
2. **Odoo**: otra variante/color o producto hermano con imagen (`product.template` mismo modelo, `image_1920 != false`). Ojo: no traer `image_1920` en búsquedas masivas — pesa mucho; leerlo solo para el id elegido.
3. **Navegador** (Claude in Chrome, si está conectado): buscar `<MARCA> <MODELO> <COLOR>` y el UPC en el sitio oficial de la marca o Google Imágenes; preferir el sitio oficial o Amazon. Mostrar a Diego las 2–3 mejores URLs candidatas y usar la que apruebe.
4. **URL pegada por Diego**.
5. **Tarjeta provisional**: `img_producto.py card "<MARCA>" "<MODELO>" "<UPC>" out.jpg` y etiquetar el producto para reemplazo (listar en pendientes).

Nota: el scraping directo de buscadores desde el contenedor devuelve resultados basura/bloqueados (probado nov-2026); no usarlo como fuente.

## Validación de la imagen
Ver la imagen (`view`) antes de cargar y confirmar: mismo modelo, mismo color, sin texto de otra tienda. Si el color no coincide, no cargar.

## Carga a Odoo
**Con URL (lo normal):** mostrar tabla `id | nombre | fuente (URL)` y con "sí" llamar
`odoo_set_image_from_url(record_id=<id>, url=<url>, model="product.template")`. El servidor descarga, normaliza al estándar
(1200×1200, fondo blanco, producto al 90 %, JPEG < 350 KB) y devuelve una miniatura: **revisarla** (mismo modelo y color) y
atender el aviso de baja resolución si aparece.

**Archivo subido al chat o tarjeta provisional (sin URL), solo administradores de Odoo:**
1. `python3 img_producto.py url <ruta> /home/claude/<upc>.jpg` (o `card …`)
2. `python3 img_producto.py b64 /home/claude/<upc>.jpg` → valor base64.
3. Con "sí": `odoo_write(model="product.template", ids=[<id>], values={"image_1920": "<b64>"})`.

Confirmar leyendo `["id","name","image_128"]` con `odoo_read` (image_128 no debe ser false; no traer image_1920).

## Salida
| id | producto | UPC | fuente | estado (cargada / provisional / pendiente) |
