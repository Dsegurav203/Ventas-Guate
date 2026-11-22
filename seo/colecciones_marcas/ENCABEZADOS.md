# Encabezado de marca en colecciones (estilo TechStop) · 22/11/2026

- Tema: "Ventas Guate 22-nov (encabezado marcas)" `gid://shopify/OnlineStoreTheme/188396634325` (copia del tema publicado; Diego publica desde Admin).
- Código: `snippets/brand-header.liquid` + `sections/collection-template.liquid` (si la colección tiene metacampos de marca: banner + tarjeta con H1, subtítulo y "acerca"; el texto SEO largo pasa debajo de los productos; sin metacampos la colección queda igual).
- Metacampos de colección (definidos, editables en Admin → Colección → Metacampos): `custom.marca_subtitulo`, `custom.marca_acerca`, `custom.marca_banner` (imagen).
- Cargados 22/11: JBL, LOGiiX, Nimbus9, Prodigee, Reebok, Skullcandy (texto e imagen tomados de TechStop, `techstop_encabezados.json`, tuteo); Tucano solo banner. Título de colección "PRODIGEE" → "Prodigee".
- Pendiente texto con fuente oficial: Tucano, HiFuture, Targus, OhSnap, LAUT, Mello, Reelcharge, Protection Pro.

## Reelcharge (22/11/2026)
- Marca creada en Odoo (`product.brand` id 265). Vendor "Ventas Guate" → "Reelcharge" en los 8 productos de Shopify.
- Colección nueva `/collections/reelcharge` (id 536141463765, automática vendor = Reelcharge, más vendidos), publicada en la tienda en línea, con SEO y texto de la propuesta.
- Portada especial: `banner-marca-reelcharge.jpg` (2400×750) hecha con la foto oficial de reelcharge.com + logo + texto en español (`seo/colecciones_marcas/reelcharge_portada/`). Área de marca con la historia oficial (reelcharge.com/pages/our-story).

## Targus y Apple (22/11/2026)
- Apple (`/collections/apple`, id 505692225749): la condición era solo el metacampo de marca (vacío) → 0 productos. Se agregó "vendor = Apple" (matchType ANY) → 58.
- Targus (`/collections/targus`, título contiene TARGUS + inventario > 0): mostraba solo lo publicado. 37 de 56 sin publicar. Publicados 6 con fotos y stock (Classic Topload Grey, Protek iPad Blue, Safe Fit 360, Strata Slipcase, Versavu teclado, Folding Keyboard). 24 sin fotos/descripción (vendor "Ventas Guate"): propuesta en `seo/targus_fichas/`.

## LAUT y Mello (22/11/2026)
- Vendor corregido: 12 LAUT ("Ventas Guate" → "LAUT") y 14 Mello ("MELLO DISTRIBUTION" → "Mello").
- Colecciones nuevas publicadas: `/collections/laut` (id 536141594837) y `/collections/mello` (id 536141627605), automáticas por vendor, más vendidos, con texto y SEO de `propuesta.json`.
- 4 LAUT con stock sin publicar por no tener fotos: Huex MacBook Neo Pink y Yellow, Links 2.0 Silver, Huex Protect MacBook Air Black.
- Marcas en Odoo ya existen: Laut (127), Mello (264).
