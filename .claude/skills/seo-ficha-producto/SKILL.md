---
name: seo-ficha-producto
description: Redacta y publica descripciones, título SEO y meta de productos de ventasguate.gt con datos verificados del fabricante, por lotes y con aprobación. Usar cuando pidan "descripciones de productos", "fichas", "top vendidos", "mejorar productos", "SEO de producto" o "fase N" del top 100.
---

# Fichas de producto SEO

Sigue las reglas de `ECOMMERCE_SEO.md` (importado en `CLAUDE.md`) (aprobación, respaldo, sin precios, sin inventar).

## 1. Elegir productos
- Por ventas: `python3 seo/top100/odoo_top_productos.py` (Odoo `sale.report`, 12 meses, incluye PdV) → mapea a Shopify por capa del conector y SKU.
- Diagnóstico de cada producto en Shopify (`descriptionHtml`, `seo`): palabras, si tiene `<h2>`, compatibilidad, cierre de garantía/envío, precios en el texto.
- Prioridad: vacíos o < 60 palabras → luego 60–150 palabras.

## 2. Fuente de datos (en este orden)
1. Catálogo oficial del fabricante (ver tabla en `CLAUDE.md`). Emparejar por EAN/código de barras cuando se pueda.
2. Producto hermano ya publicado en la tienda (mismo modelo, otro color): reutilizar solo sus afirmaciones.
3. Especificaciones públicas ampliamente documentadas (ej. cargador Apple 20W).
Sin fuente → no publicar; anotar "SIN FUENTE" en `dudas`.

## 3. Redactar
Plantilla de `CLAUDE.md`: intro → `<h2>Características</h2>` → `<h2>Compatibilidad</h2>` → cierre estándar. 90–180 palabras. SEO title ≤ 60, meta ≤ 155. Corregir `vendor` si dice "Ventas Guate" o un proveedor en vez de la marca.
Guardar `seo/top100/faseN_propuesta.json` con `{id, title, html, seo_title, seo_description, vendor_nuevo, fuentes, dudas}` y un `PROPUESTA_FASEN.md` legible para aprobar. Validar con Python: HTML bien formado, longitudes, sin `Q\d` (precios).

## 4. Publicar (tras "aprobado")
- Respaldo: `faseN_respaldo.json` con html/seo/título anteriores.
- Lotes de 8–10 con `productUpdate` y el contenido en `variables` (límite 16,384 caracteres del documento):
  `mutation($p0: ProductUpdateInput!, …){ p0: productUpdate(product:$p0){ product{id title vendor} userErrors{field message} } … }`
- Si cambió algún título: replicarlo en Odoo (capa + plantilla) con un script como `seo/top100/odoo_titulos_fase1.py`.
- Verificar leyendo 2–3 productos y registrar en `seo/top100/README.md`.
