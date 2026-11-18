# Auditoría SEO completa — ventasguate.gt — 18 nov 2026

**Fuentes:** Search Console (27 jul – 24 oct, 1,000 consultas), catálogo Shopify (export 27 oct + cambios aplicados hasta 27 oct), código del tema, búsquedas de competencia (18 nov).
**Limitaciones de esta corrida:**
- Shopify desconectado (pide volver a iniciar sesión) → el estado del catálogo es del 27 oct + cambios conocidos.
- `ventasguate.gt` no está permitido en la red de esta sesión → no se midió velocidad ni HTML renderizado en vivo.
- Ahrefs sin autorizar → volúmenes y dificultad son **estimados** a partir de impresiones de GSC y de la SERP.

## Resumen ejecutivo

El sitio tiene una base técnica aceptable (Shopify, HTML renderizado en servidor, schema de producto, breadcrumbs), y una marca que Google ya reconoce: el 80% de los clics vienen de búsquedas con "Ventas Guate". **El problema es el tráfico sin marca:** 17,188 impresiones en 90 días con 2.7% de CTR, porque la mayoría de fichas y colecciones no tienen texto ni SEO, y las categorías genéricas (audífonos, bocinas, smartwatch, estuches iPhone) están en posición 20–45.

**Mayor fortaleza:** posición 1–5 en marcas propias de distribución (Prodigee 4.9, HiFuture 4.9, "case s26 ultra guatemala" 4.7) y en seminuevos (6.8).

**Top 3 prioridades:**
1. **Skullcandy** es la marca con más demanda orgánica (2,053 impresiones, 114 consultas) y casi no tiene clics (35) → SEO de fichas y colección.
2. **Categorías genéricas en página 3–5** (audífonos 45.6, bocina bluetooth 45.1, smartwatch 34–38, estuches iPhone 20.7) → texto de colección + enlaces internos desde el blog.
3. **Echo Dot 5 a Q599** mientras Walmart lo tiene en Q475 y Pacifiko en Q499. Con 152 unidades, ningún SEO compensa una diferencia de Q100–124.

**Evaluación general:** *Necesita trabajo* — no hay problemas críticos de indexación, pero el contenido no compite fuera de la marca.

## Oportunidades de keywords

Dificultad estimada según quién aparece arriba (marketplaces y retailers grandes = difícil).

| Keyword | Dif. est. | Oportunidad | Posición actual | Intención | Contenido recomendado |
|---|---|---|---|---|---|
| skullcandy guatemala / skullcandy dime 3 / smokin buds | Fácil | **Alta** | 7–10 | Transaccional | Colección Skullcandy con texto + fichas con SEO (en parte hecho) |
| iphone reacondicionado guatemala | Moderada | **Alta** | 6.8 | Comercial | Guía (borrador listo) + texto en `/collections/seminuevos` |
| iphone usados guatemala / iphone seminuevo | Moderada | **Alta** | 6.5–10.8 | Comercial | Misma guía + FAQ |
| precio iphone 11 pro max guatemala (+3 variantes) | Moderada | **Alta** | 33–37 | Transaccional | Fichas de seminuevos con "precio" en el title (hecho en 3) |
| prodigee / prodigee guatemala | Fácil | **Alta** | 4.3–4.9 | Navegacional | Mejorar CTR: title/meta (hecho) + comparativa de modelos |
| case s26 ultra guatemala / case samsung s26 ultra | Fácil | **Alta** | 4.7–7.7 | Transaccional | Texto en `/collections/s26-cases` |
| alexa / alexa guatemala | Moderada | **Alta** | 10.3 / 18.5 | Comercial | Texto en `/collections/alexa` + guía "qué Alexa comprar" |
| alexa 510 / alexa 5.0 | Fácil | Media | 6–7.5 | Transaccional | "Echo Dot 5 (Alexa 5.0)" en título y texto de la ficha |
| govee guatemala / govee tv backlight | Fácil | Media | 8.3 | Transaccional | Guía Govee + texto en colección |
| popsocket guatemala | Fácil | Media | 4.8–6.9 | Transaccional | Hecho (title/meta); falta texto de colección |
| smartwatch para mujer guatemala | Moderada | **Alta** | 38.4 | Comercial | Hecho texto de colección; falta guía y enlaces internos |
| reloj para correr / reloj gps guatemala | Moderada | **Alta** | 27–35 | Comercial | Guía "smartwatch para correr con GPS" |
| smartwatch guatemala / relojes inteligentes guatemala | Difícil | Media | 34–36 | Comercial | Colección (hecho) + enlaces + reseñas |
| estuches iphone guatemala / case iphone guatemala | Moderada | **Alta** | 19.5–20.7 | Transaccional | Texto en `/collections/cases-iphone` con "estuche / case / forro" |
| fundas de iphone | Difícil | Media | 10.8 | Transaccional | Pilar "Guía de fundas para iPhone" |
| jbl endurance peak 3 / jbl tour one m2 | Fácil | Media | 7.5–7.9 | Transaccional | Hecho (fichas); repetir en catálogo JBL |
| jbl guatemala | Moderada | Media | 27.6 | Navegacional | Texto en `/collections/jbl` |
| magsafe guatemala | Moderada | Media | 19.5 | Comercial | Texto en `/collections/magsafe` + guía "Qué es MagSafe" |
| audífonos (genérico) | Difícil | Baja | 45.6 | Comercial | No atacar directo: long-tail ("audífonos open ear", "audífonos con cancelación de ruido guatemala") |
| audífonos open ear | Fácil | **Alta** | — | Informativa | Guía (empuja FlexClip, 948 u.) |
| bocina bluetooth (genérico) | Difícil | Baja | 45.1 | Comercial | Long-tail: "bocina con micrófono karaoke guatemala" (Vocalist 100) |
| power bank magsafe guatemala | Moderada | Media | 46 ("power bank") | Comercial | Texto en `/collections/powerbanks` |
| regalos tecnológicos navidad guatemala | Moderada | **Alta (estacional)** | nuevo | Comercial | Publicado 27 oct |
| echo dot 5 precio guatemala | Moderada | Media | — | Transaccional | Solo si el precio compite (ver hallazgo de precio) |

## Problemas on-page

| Página | Problema | Severidad | Arreglo |
|---|---|---|---|
| Todo el sitio | Error Liquid al pie de cada página (`section 'popup-beneficios'` no existe) | **Crítico** | Quitar la línea en `layout/theme.liquid` (copia del tema) |
| Todo el sitio | `<meta name="robots" content="index,follow">` fijo en todas las plantillas | Alto | Quitar; noindex condicional para búsqueda y tags |
| ~800 productos con stock | Sin SEO title (estado 27 oct: 831 de 991; hoy ~790 tras los arreglos) | Alto | Lotes de 25 por stock e impresiones |
| ~450 productos con stock | Descripción vacía | Alto | Plantillas por modelo (como OhSnap) |
| 90% de las imágenes | Sin alt | Alto | Alt base por producto, en lote |
| `/collections/skullcandy` | 630 impresiones, CTR 1.7%, pos. 12.7 | Alto | Reescribir title/meta y texto |
| `/collections/cases`, `/collections/cases-iphone` | 1,429 y 707 impresiones, pos. 14–16 | Alto | Texto con "estuche/case/forro" + FAQ |
| `/collections/audio`, `/collections/bocinas` | pos. 25–35 | Medio | Texto de categoría + enlaces desde guías |
| `/collections/all` | 2,630 impresiones, CTR 0.9% | Medio | Es la página "todos los productos": dar title/meta o noindex |
| Producto (schema) | `brand` como `Thing`, código de barras como `mpn` | Medio | `Brand` + `gtin` (copia del tema) |
| Producto (schema) | Sin `shippingDetails` ni `hasMerchantReturnPolicy` → Merchant listings 0 clics | Medio | Necesita costo y tiempo de envío confirmados |
| `og:title` producto | Usa título del producto, no el SEO title | Bajo | Ajuste en `social-meta-info.liquid` |

## Brechas de contenido

| Tema | Por qué importa | Formato | Prioridad | Esfuerzo |
|---|---|---|---|---|
| Skullcandy: cuál comprar (Dime 3, Smokin Buds, Sesh ANC, Method 360, Crusher) | 2,053 impresiones, la marca de audio con más demanda | Comparativa | Alta | Media jornada |
| iPhone reacondicionado: qué revisar | 912 impr. sumando reacondicionado/seminuevo/usados; competidores (iSmart, Backfone, Celovendo) compiten con garantía de 90 días a 12 meses | Guía (borrador listo) | Alta | Quick win (faltan 3 datos de Diego) |
| Smartwatch para correr con GPS | 244 impr. en pos. 27–35 | Guía | Alta | Media jornada |
| Audífonos open ear | Empuja 948 u. de FlexClip | Guía | Alta | 2 h |
| Qué Alexa comprar / casa inteligente con Alexa | 1,032 impr. "alexa" | Guía + combo | Media | 2 h |
| Govee: tiras LED y TV Backlight | 591 impr. | Guía | Media | 2 h |
| Guía de fundas para iPhone (pilar) | "fundas de iphone" pos. 10.8; Top Móvil y Celovendo tienen colecciones por modelo con texto | Pilar | Media | Varios días |
| Páginas de confianza: Envíos, Garantía, Tienda zona 13 | Competidores destacan envío gratis, cuotas, garantía por escrito | Páginas fijas | Alta | 2 h (faltan datos de envío) |

## Checklist técnico

| Check | Estado | Detalle |
|---|---|---|
| HTTPS | ✅ Pass | Shopify |
| HTML renderizado en servidor | ✅ Pass | Tema Turbo (Liquid) |
| Sitemap | ✅ Pass | Automático de Shopify; enviado en GSC |
| robots.txt | ⚠️ Warning | Default de Shopify, no verificado en vivo (sin acceso de red) |
| Meta robots | ❌ Fail | `index,follow` fijo en todas las plantillas |
| Error visible en páginas | ❌ Fail | `popup-beneficios` |
| Colecciones internas indexables | ⚠️ Warning | `destacados-prueba`, `precio-regular`, `promo-2do-articulo-15`, `globofilter` siguen sin noindex (no se aprobó) |
| Colecciones vacías | ⚠️ Warning | 12 con noindex + 301 listos; faltan despublicar (Diego) |
| Duplicados | ⚠️ Mejorado | FlexClip, Echo Spot, Echo Dot unificados; quedan ~110 handles `-1` |
| Schema Product | ⚠️ Warning | Brand `Thing`, sin gtin, sin envío/devolución |
| Schema Organization / LocalBusiness | ❌ Fail | Borrador listo; faltan horario y WhatsApp |
| Core Web Vitals | ⚠️ No medido | Sin acceso al sitio. GSC: escritorio en posición 15 vs móvil 7.8 → revisar Experiencia en GSC |
| Popups | ⚠️ Warning | A 1.2 s, pantalla completa en móvil (home y promos) |
| Productos a Q0/Q1 visibles | ✅ Resuelto | 33 ocultos, 15 insumos desactivados |

## Competencia

| Dimensión | Ventas Guate | Top Móvil | Celovendo | iSmart / Backfone (seminuevos) | Walmart / Pacifiko (Alexa) |
|---|---|---|---|---|---|
| Foco | Distribución de marca + accesorios + seminuevos | Fundas y accesorios premium (CASETiFY, OtterBox, Spigen) | Fundas por modelo + seminuevos | iPhone seminuevo | Marketplace general |
| Colecciones por modelo de iPhone con texto | Parcial | ✅ | ✅ ("Estuches para iPhone 17 Pro Max en Guatemala") | — | — |
| Propuesta visible | Garantía 1 año | Originales + envío gratis > Q250 | Cuotas | Garantía 90 días–12 meses, envío gratis | Precio |
| Blog / guías | 1 artículo (nov) | No visto | No visto | No visto | No |
| Echo Dot 5 | **Q599** | — | — | — | **Q475–Q499** |
| Marcas exclusivas (Prodigee, HiFuture, Reebok) | ✅ Sin competencia visible | ❌ | ❌ | — | ❌ |

**Lectura:** en fundas genéricas y Alexa competís contra retailers grandes con mejor precio o más autoridad. Donde ganás es en las **marcas que distribuís** (Prodigee, HiFuture, Skullcandy, Reebok) y en **seminuevos**: ahí hay que concentrar contenido.

## Plan priorizado

### Quick wins (esta semana)

| Acción | Impacto | Esfuerzo | Depende de |
|---|---|---|---|
| Revisar precio del Echo Dot 5 (Q599 vs Q475–Q499 en Walmart/Pacifiko) | Alto | 15 min | Diego (margen) |
| Volver a conectar Shopify en claude.ai | — | 2 min | Diego |
| Despublicar 12 colecciones vacías (activa los 301) | Medio | 10 min | Diego |
| Corregir correo en política de contacto (.com → .gt) | Medio | 5 min | Diego |
| SEO title/meta + texto en `/collections/skullcandy` y fichas Skullcandy (114 consultas) | Alto | 2 h | Shopify conectado |
| Texto en `/collections/s26-cases`, `/collections/cases-iphone`, `/collections/alexa` | Alto | 2 h | Shopify conectado |
| Publicar guía de iPhone reacondicionado | Alto | 30 min | 3 datos de Diego |
| Pedir indexación en GSC de las páginas cambiadas | Medio | 15 min | Diego |

### Inversiones estratégicas (este trimestre)

| Acción | Impacto | Esfuerzo | Depende de |
|---|---|---|---|
| Copia del tema con arreglos técnicos (popup-beneficios, robots, schema Brand/gtin/Organization, popups a 8 s) | Alto | 1 día | Diego publica la copia |
| SEO + descripciones en lotes de 25 para ~790 productos con stock, por impresiones y stock | Alto | 4–6 semanas | Aprobación por lote |
| Guías: Skullcandy, smartwatch GPS, open ear, Alexa, Govee, pilar de fundas | Alto | 1 por semana | — |
| Páginas Envíos, Garantía, Tienda zona 13 + schema LocalBusiness + Google Business Profile | Alto | 1 día | Horario, WhatsApp, envío |
| Unificar los ~110 productos duplicados `-1` | Medio | 1 semana | Conteo físico de SKUs duplicados |
| Pedir a Prodigee, HiFuture, Skullcandy y Reebok que listen a Ventas Guate como distribuidor en Guatemala (backlinks de autoridad) | Alto | 2 h + seguimiento | Diego |
| Merchant listings gratis (schema de envío y devolución) | Medio | 2 h | Costo y tiempo de envío |
