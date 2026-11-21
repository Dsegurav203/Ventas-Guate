# Auditoría SEO completa · ventasguate.gt · 21/11/2026

Fuentes: Shopify Analytics (90 días), rastreo propio (24 páginas, sitemap, /products.json, Playwright iPhone 13), búsqueda web (índice EE.UU.; demanda/dificultad = estimación), Search Console 27-jul a 24-oct (AUDITORIA_SEO_2026-11.md). Sin Ahrefs/Semrush conectado.

## Resumen
- Búsqueda orgánica: 3,958 sesiones en 90 días (8.5% del tráfico), crece de ~650/mes (may) a ~1,300/mes (jul–nov). Convierte 0.51% vs 0.10% de social. 21 pedidos / Q5,600 en 90 días.
- 55% de la búsqueda entra a la portada (búsqueda de marca). Fuera de "Prodigee" (pos. 4–5) y "seminuevos" (pos. 6–7), no estamos en top 10 de términos genéricos.
- Fortaleza: schema de producto con Offer + envío + devoluciones (mejor que Max), sin errores 404, HTTPS ok.
- Prioridades: (1) contenido escaso: 1,064/1,338 productos <100 palabras y 88/142 colecciones sin texto; (2) colecciones vacías noindex enlazadas desde menú/portada + doble meta robots; (3) CLS móvil 0.65 en colecciones (corrección lista, pendiente de publicar en el tema).
- Diagnóstico: base técnica sana, falta contenido y autoridad de marca.

## Tráfico (90 días)
| Fuente | Sesiones | Conversión | Pedidos |
|---|---|---|---|
| Social | 29,596 | 0.10% | 29 |
| Directo | 13,044 | 0.41% | 54 |
| Búsqueda | 3,958 | 0.51% | 20 |
Móvil = 93% de sesiones (conversión 0.21% vs 0.41% escritorio).

Top entradas desde búsqueda: / (2,165), /collections/seminuevos (197, rebote 65%), cases-iphone (107), prodigee (84), s26-cases (83), Govee TV Backlight (71, rebote 86%), cases (59), popsockets (42), reserva iPhone Duo (41), alexa (41), ipads-seminuevas (39, colección vacía), /policies/contact-information (29, ya no está en el footer).

## Keywords (estimación)
| Keyword | Dificultad | Oportunidad | Posición VG | Intención | Página |
|---|---|---|---|---|---|
| prodigee guatemala | Fácil | Alta | 4–5 | Navegacional | Colección + comparativa |
| iphone seminuevo guatemala | Moderada | Alta | 6–7 | Comercial | Guía + colección seminuevos |
| funda/laut guatemala | Fácil | Alta | No hay página | Transaccional | Colección LAUT nueva |
| smartwatch reebok guatemala | Fácil | Alta | s/d | Transaccional | Colección con texto |
| sudio / ohsnap / logiix guatemala | Fácil | Alta | Sin colección (Sudio, OhSnap) | Transaccional | Colecciones de marca |
| mochila tucano guatemala | Fácil | Alta | s/d (colección sin texto) | Transaccional | Colección Tucano |
| case iphone 18 pro max guatemala | Fácil–moderada | Alta | s/d | Transaccional | Colección por modelo |
| fundas iphone 17 guatemala | Moderada | Alta | 19–21 | Transaccional | Colección por modelo |
| cargador magsafe guatemala | Moderada | Media | 19.5 | Transaccional | Colección + texto |
| correas apple watch guatemala | Moderada | Media | s/d | Transaccional | Colección + tabla de tallas |
| mochila targus laptop guatemala | Moderada | Media | s/d | Transaccional | Marca + guía por tamaño |
| jbl guatemala | Difícil | Media | 27.6 | Comercial | Landing JBL con texto |
| bocina jbl charge 6 precio guatemala | Moderada | Media | s/d | Transaccional | Ficha |
| regalos tecnológicos navidad guatemala | Moderada | Media (estacional) | publicado | Comercial | Actualizar guía + enlazar en portada |
| cuál es la mejor funda para iphone 17 pro max | Moderada | Media | — | Informacional | Guía pilar |
| cómo saber si un cargador es original | Moderada | Media | — | Informacional | Guía |
| qué cargador comprar para iphone 17/18 | Fácil | Media | — | Comercial | Guía |
| power bank guatemala | Difícil | Media | 46 | Transaccional | Colección + comparativa |
| audífonos bluetooth guatemala | Difícil | Baja | 45.6 | Comercial | Pilar por presupuesto |
| iphone 18 precio guatemala | Difícil | Baja | s/d | Comercial | Guía + reservas |
| apple watch guatemala precio | Difícil | Baja | s/d | Comercial | Colección + guía |
| audífonos open ear | Fácil | Baja | — | Informacional | Blog |

## Problemas en página
| Página | Problema | Severidad | Corrección |
|---|---|---|---|
| Menú/portada | 7 colecciones vacías noindex enlazadas (computo, viaje, holders, ipads-seminuevas, almacenamiento, applewatch, controles) | Crítico | Llenarlas o quitarlas del menú y portada; redirigir 301 |
| Colecciones ocultas (iphone-1, targus-1…) | Doble meta robots (index y noindex) | Alto | Corregir condición en theme.liquid |
| 1,064 productos | <100 palabras (513 con 0): Tucano 73/75, iTronics 106/106, Master Case 48/48, Prodigee 233/303 | Alto | Lotes de fichas (skill seo-ficha-producto) |
| 88 colecciones | Sin texto (tucano, maletines, motorola, ipads, iphone-13…) | Alto | Lotes de textos (skill seo-coleccion) |
| Fichas | Sin AggregateRating ni BreadcrumbList; EAN en sku, sin gtin | Alto | App de reseñas + snippet breadcrumb + gtin |
| Seminuevos | itemCondition = NewCondition | Medio | UsedCondition/RefurbishedCondition por etiqueta |
| Fichas | merchantReturnDays 2 (política: 15) | Medio | Corregir snippet schema |
| Preguntas frecuentes / colecciones con FAQ | Sin FAQPage | Medio | JSON-LD FAQPage |
| Blog | Sin Article/BlogPosting; títulos 74–77 car.; sin meta | Medio | Schema + títulos ≤60 |
| Organization | sameAs con 23 vacíos | Medio | Limpiar en ajustes del tema |
| 121 productos | Precio (Q) dentro de la descripción | Medio | Quitar (regla 4) |
| /products/reserva-iphone-18-ultra | Handle "18 ultra" vs título "iPhone Duo" | Medio | Corregir título/handle + 301 |
| 228 productos | Handle "l-…" | Medio | Cambiar handle + 301 en lotes (con descripciones) |
| 24 grupos | Títulos de producto duplicados | Medio | Diferenciar por color/modelo |
| Portada | 3 H1, 35 imágenes sin alt | Medio | Un H1; alt en banners |
| /collections/tucano | Meta vacía, 0 palabras | Medio | Texto + meta (Especial 50% activo) |
| /policies/contact-information | Recibe tráfico de Google | Bajo | Enlazar a /pages/contact desde la política |

## Técnico
| Revisión | Estado | Detalle |
|---|---|---|
| robots.txt / sitemap | Pass | 1,462 URL, estándar Shopify |
| llms.txt | Warning | Plantilla genérica, no describe el negocio |
| HTTPS / mixto / HSTS | Pass | 0 recursos http |
| Enlaces rotos | Pass | 60/60 = 200 |
| Canonical / paginación | Pass | Correctos |
| Meta robots | Fail | Doble meta en colecciones ocultas |
| CLS móvil | Fail | Colección 0.647, producto 0.298 (corrección del sidebar lista desde 19/11, falta publicar; galería pendiente) |
| LCP | Warning | Portada 2.3 s en laboratorio; el LCP es la imagen del popup |
| Peso | Warning | 3–4.8 MB, 216–285 requests, 1.4–1.8 MB de JS; Google Maps en portada (475 KB); GTM 550 KB; imágenes descargadas 2 veces |
| Datos estructurados | Warning | Product/Offer ok; faltan reseñas, breadcrumb, FAQPage, Article, ElectronicsStore (pendiente tarea #15) |
| Móvil / viewport | Pass | Responsive |

## Competencia
| Dimensión | Ventas Guate | Pacifiko | Intelaf | Max | Mejor |
|---|---|---|---|---|---|
| Catálogo | 1,338 fichas / 142 colecciones | Marketplace masivo | 3,803 fichas / 240 marcas | ~820 URLs | Pacifiko |
| Páginas de marca con "Guatemala" | Parcial, sin texto | Sí (incluye LAUT) | 240 | Parcial | Intelaf |
| Blog | 2 artículos | ~10 | No | Activo, guías "vs" y "cuánto cuesta" | Max |
| Schema ficha | Product, Offer, envío, devolución | + AggregateRating | + envío, devolución | Product, Offer | Pacifiko |
| Funciones de SERP | Ninguna | Estrellas, precio, sitelinks | Precio/envío | PAA, artículos | Pacifiko |
| Nichos sin competencia | Prodigee, HiFuture, Reebok, LAUT, Sudio, OhSnap, seminuevos | — | — | — | Ventas Guate |

## Plan
**Esta semana (rápido)**
1. Quitar/llenar las 7 colecciones vacías del menú y portada + 301 (Alto, 1 h, Luis en editor de tema).
2. Publicar corrección CLS del sidebar (Alto, 30 min, tarea #15 de Luis).
3. Texto + meta de /collections/tucano y título "Mochilas y maletines Tucano en Guatemala" (Alto, 1 h; promo activa).
4. Corregir schema: merchantReturnDays 15, itemCondition seminuevos, sameAs vacíos (Medio, 1 h, código de tema).
5. Corregir ficha reserva-iphone-18-ultra (Medio, 15 min).
6. Quitar precios de las 121 descripciones (Medio, 2 h, script con aprobación).

**Este trimestre**
1. Colecciones de marca nuevas con texto: LAUT, Sudio, OhSnap, Mello, Reelcharge + "Guatemala" en el título de todas las de marca (Alto, 1–2 días).
2. Textos de las 88 colecciones sin texto, por sesiones (Alto, 3–4 días en lotes).
3. Fichas: lote Prodigee (233), Tucano (73), Master Case, iTronics; handles "l-" con 301 en los mismos lotes (Alto, multi-día).
4. Reseñas de producto (app Judge.me/Shopify Product Reviews) → estrellas en Google (Alto; depende de aprobar app).
5. Blog: 2 guías/mes. Primeras: "Prodigee: qué modelo elegir", "iPhone seminuevo en Guatemala: qué revisar", "Mejor funda para iPhone 17/18", "Cómo saber si un cargador es original", "Mochila por tamaño de laptop (Tucano/Targus)", "JBL Charge 6 vs Flip 7" (Medio–Alto).
6. Velocidad fase 2: Google Maps solo en /pages/contact, revisar GTM, galería de producto (CLS 0.30) (Medio).
7. Search Console: revisar posiciones a las 4 y 8 semanas; conectar Ahrefs/Similarweb para datos de Guatemala.

## Verificación en vivo (21/11/2026 tarde, tras publicar tema "21-nov (SEO + logo móvil)")
| Punto | Estado | Detalle |
|---|---|---|
| Colecciones vacías en menú | Corregido | Menú depurado |
| /collections/tucano texto + meta | Corregido | 658 palabras, título 55, meta 150 |
| ElectronicsStore en portada | Corregido | sameAs sin vacíos en portada |
| Reserva iPhone Duo | Corregido | Handle + 301 |
| Organization sameAs (resto del sitio) | Pendiente | 25 entradas, 23 vacías (ajustes del tema) |
| Doble meta robots (iphone-1 y ocultas) | Pendiente | index,follow + noindex,nofollow |
| merchantReturnDays | Pendiente | 2 (política 15) |
| itemCondition seminuevos | Pendiente | NewCondition |
| gtin / AggregateRating / Breadcrumb en ficha | Pendiente | Ausentes |
| H1 portada | Pendiente | 3 H1 (Smartwatches, Smarthome, Cómputo); portada con 60 palabras |
| Alt de imágenes | Pendiente | Portada 18/45 sin alt; fichas 2–4 |
| CLS móvil | Parcial | Seminuevos 0.06 ok; portada 0.33, Tucano 0.23, ficha LAUT 0.38 (galería) |
| Meta description de fichas sin texto | Pendiente | Fichas sin descripción salen sin meta (HiFuture Passion M, LAUT Huex) |
| Títulos en mayúsculas en seminuevos | Pendiente | "IPHONE 15 PRO MAX 1TB…" |
| Blog | Parcial | Article + Breadcrumb ok; título 74 car.; /blogs/guias sin meta |
| robots.txt / sitemap / llms / agents.md | Ok | Shopify estándar + agents.md |
