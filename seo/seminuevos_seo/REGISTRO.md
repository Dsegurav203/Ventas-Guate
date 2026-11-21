# Registro · SEO de seminuevos (Shopify) · 2026-11-21

Aprobado por Diego Segura. Ejecutado con Admin GraphQL (`productUpdate` con alias, 4 lotes). Solo se cambiaron `title` y `seo` (title, description).

## Resumen

| Concepto | Cantidad |
|---|---|
| Productos activos con "seminuevo" en el respaldo | 100 |
| Productos actualizados | 98 (lotes de 25 + 25 + 25 + 23) |
| A · títulos corregidos (mayúsculas / SE / 16e / 17e) | 6 |
| B · SEO title + meta nuevos (antes vacíos) | 98 |
| Sin cambios (ya tenían SEO: iPad 7ma Gen, iPad Air 2) | 2 |
| Sin patrón | 0 |
| userErrors | 0 |

Títulos A aplicados:

| Antes | Después |
|---|---|
| IPHONE 15 PRO 256GB TITANIO NATURAL SEMINUEVO | iPhone 15 Pro 256GB Titanio Natural Seminuevo |
| IPHONE 15 PRO MAX 256GB TITANIO NATURAL SEMINUEVO | iPhone 15 Pro Max 256GB Titanio Natural Seminuevo |
| IPHONE 15 PRO MAX 1TB TITANIO NEGRO SEMINUEVO | iPhone 15 Pro Max 1TB Titanio Negro Seminuevo |
| iPhone Se 2020 64GB Rojo Seminuevo | iPhone SE 2020 64GB Rojo Seminuevo |
| iPhone 16E 128GB Blanco Seminuevo | iPhone 16e 128GB Blanco Seminuevo |
| iPhone 17E 256GB Rosa Seminuevo | iPhone 17e 256GB Rosa Seminuevo |

**Pendiente:** replicar estos 6 títulos en Odoo (`product.template.name` y capa `shopify.product.template.ept`), según la regla de sincronización de `ECOMMERCE_SEO.md`.

## Nota

En 17 productos el SEO title propuesto era igual al título del producto (cuando con " | Ventas Guate" pasaba de 60 caracteres). Shopify guarda ese caso como `seo.title = null` y en la tienda muestra el título del producto, así que el resultado es el mismo.

## Verificación

Se volvieron a leer 11 productos: los 6 de títulos A y 5 al azar (iPhone 11 Pro 256GB Oro, 13 Pro Max 512GB Azul Sierra, 17 Pro 256GB Azul Profundo, 16 Pro Max 1TB Titanio Negro, 12 128GB Azul). Todos coinciden con `aplicar_resumen.json`.

## Archivos

- `respaldo_2026-11-21.json`: estado anterior (id, title, handle, seo) de los 100 productos.
- `generar.py`: genera los lotes y el resumen a partir del respaldo.
- `lote_1.json` … `lote_4.json`: variables `ProductUpdateInput` enviadas.
- `aplicar_resumen.json`: lo aplicado por producto (antes / después).

## Cómo revertir

Por cada producto de `aplicar_resumen.json`, tomar su registro en `respaldo_2026-11-21.json` y ejecutar
`productUpdate(product:{id, title:<title del respaldo>, seo:{title:<seo.title>, description:<seo.description>}})`.
En el respaldo, `seo` de estos 98 productos era `null`/`null`; con `""` se vacía el campo.

- Odoo: no aplica. Los seminuevos no existen en Odoo (verificado por nombre y SKU ITR-), así que no hay títulos que replicar.
