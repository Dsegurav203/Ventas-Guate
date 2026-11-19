# Alt text: registro de aplicación (18–19/11/2026)

| Concepto | Resultado |
|---|---|
| Entradas aplicadas (lotes alt_01 a alt_66) | 6,589 |
| Errores de Shopify (userErrors) | 0 |
| Lote 09 reaplicado con erratas corregidas | 100 imágenes, 0 errores |
| Imágenes compartidas entre productos | 121 imágenes (398 entradas) |
| Corrección de imágenes compartidas | 121 con texto común al modelo/familia, 0 errores |

- Respaldo y textos por imagen: `alts_respaldo_y_nuevos.csv` (alt_anterior / alt_nuevo).
- Imágenes compartidas: `alts_imagenes_compartidas.csv`. Una imagen usada por varios productos solo puede tener un alt; se dejó un texto común sin color o capacidad (por ejemplo "iPhone 16 Seminuevo", "Pulsera para Apple Watch", "Smartwatch - imagen de referencia").
- Para revertir: aplicar `alt_anterior` con `fileUpdate(files:[{id, alt}])`.
