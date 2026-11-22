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
