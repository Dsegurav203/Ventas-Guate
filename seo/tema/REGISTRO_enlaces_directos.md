# Enlaces de producto directos (aprobado por Diego 2026-11-28)
- Motivo: Search Console "Alternate page with proper canonical tag" 3,497 (66% de la muestra = /collections/X/products/Y generadas por `| within: collection`).
- Cambio: `product.url | within: collection` → `product.url` y `variant.url | within: collection` → `variant.url` en sections/product-recently-viewed-template, snippets/collection-swatch, product-details, product-slider, product-thumbnail, product.liquid.
- Commit en tema live 188396634325 (bda4fbaf…) y copia "Ventas Guate 28-nov (enlaces directos)" 188632694997 con el cambio. theme_publish rechazado ("Only agent-created themes"): Diego publica la copia desde Admin → Online Store → Themes.
- Revertir: publicar "Ventas Guate 22-nov (encabezado marcas)" o re-agregar `| within: collection`.
