# Página /pages/marcas (22/11/2026)
- Antes: 19 tarjetas fijas; enlaces rotos (/collections/protection-pro y /collections/amazon no existían); HP vacía; faltaban LAUT, Mello, Reelcharge, Reebok, OhSnap, Function101, Govee, Bitty Boomers.
- Ahora: 26 tarjetas (nuevo body en `nuevo.json`), 0 enlaces rotos. Amazon → /collections/alexa. HP quitada.
- Creada colección `protection-pro` (id 536141791445, título empieza con "Protection Pro" + stock > 0) y publicada. Publicada `ohsnap` (antes daba 404).
- Sin logo (tarjeta con nombre): LAUT, Reelcharge, Mello, OhSnap, Function101. JBL muestra foto de audífonos en vez de logo (ya estaba así).
- La página es HTML fijo: al crear una marca nueva hay que agregar su tarjeta aquí.

## 22/11/2026 (2)
- Revisión de existencia por marca (productos publicados disponibles): sin nada → HP, Click, Protection Pro (sus productos no están publicados). Quitada la tarjeta de Protection Pro (25 tarjetas).
- Despublicar colecciones por API está bloqueado: HP, Click y Protection Pro quedan ocultas de Google (`seo.hidden` = 1); despublicarlas en Admin.
- Marcas con 1–2 productos: Sony 1, Master Case 1, Mophie 1, Solo 1, Motorola 1, MyBat 2, Hypergear 2, Kieslect 2.
- Ojo: "Protection Pro Lamina Ultra Extra Small Matte" mostraba 280 u. tras el cruce del 21/11 y hoy está en 0 en Shopify; revisar en el cruce del lunes.

## 22/11/2026 (3) · Logos oficiales
Fuentes oficiales: LAUT, Reelcharge, Mello, OhSnap y Function101 en los sitios de cada marca; JBL en la sala de prensa de Harman (jbl.com bloquea descargas automáticas). Los archivos procesados están en `logos/<marca>.png`: se recortaron los márgenes, se dejó un ancho máximo de 400 px y fondo transparente.

| Marca | Fuente | Proceso | Archivo Shopify (MediaImage) |
|---|---|---|---|
| LAUT | itslaut.com/cdn/shop/files/LAUT_Logo_GoogleShopping_2000x1000px.png | recorte + 400 px | 47152595140821 · logo-laut.png |
| Reelcharge | reelcharge.com/cdn/shop/files/RC.png | recorte + 400 px | 47152595173589 · logo-reelcharge.png |
| Mello | mellodistribution.com/cdn/shop/files/mellologo.png (header) | recorte (359 px) | 47152595206357 · logo-mello.png |
| OhSnap | ohsnap.com/cdn/shop/files/logo-white.svg (header) | SVG blanco pasado a #111 y renderizado con Chromium | 47152595239125 · logo-ohsnap.png |
| Function101 | function101.com/cdn/shop/files/Image_2-14-26_at_7.45_AM.jpg (logo del header) | fondo blanco → transparente | 47152595271893 · logo-function101.png |
| JBL | news.harman.com → iprsoftwaremedia.com/…/JBL Logo_thmb.png (sala de prensa Harman) | recorte, 300 px (cuadro naranja oficial) | 47152595304661 · logo-jbl.png |

- URL CDN: `https://cdn.shopify.com/s/files/1/0764/0940/5653/files/logo-<marca>.png?v=1795314766`.
- Página 582676906197 (`pageUpdate` 02:33 UTC): las tarjetas `<b>Nombre</b>` de LAUT, Reelcharge, Mello, OhSnap y Function101 ahora llevan `<img … alt="<Marca> Guatemala" width="130" height="60" loading="lazy">`. JBL cambió de la foto de los audífonos TOUR ONE M2 a logo-jbl.png.
- Respaldo del body anterior: `respaldo_body_2026-11-22.html`. Body nuevo: `nuevo_body_logos.html`. Para revertir, aplicar el respaldo con `pageUpdate`.
- Verificación: captura de la tienda en vivo en `logos/captura.png`; las 6 imágenes cargan. Ya no queda ninguna tarjeta sin logo.
- Nota: el logo de Reelcharge es muy ancho y queda pequeño en la tarjeta (130 px); se lee, pero se podría usar uno sin el lema "Power. Simplified." si se quiere más grande.
