# Technical SEO Audit — ventasguate.gt — 2026-10-27

**Fuente**: código del tema publicado "Fix Galería + Popups" (Turbo 9.5.1, Out of the Sandbox) + Shopify Admin API.
**No medido** (crawl externo bloqueado desde este entorno): Core Web Vitals reales, TTFB, status codes en vivo. Correr PageSpeed Insights + Search Console → Cobertura.

**Score estimado: 58/100**

| Área | Score | Resumen |
|---|---|---|
| Crawlability | 60 | robots.txt default de Shopify (OK). Robots meta forzado a `index,follow` en todo el sitio |
| Indexation | 45 | Colecciones internas/vacías/duplicadas indexables, 115 productos clonados, tags indexables |
| Performance | 55 | 818 KB CSS+JS de terceros, jQuery + InstantClick, CSS bloqueante 396 KB |
| Mobile | 65 | Viewport OK. Popup full-screen a 1.2 s en home y colecciones promo |
| Security | 90 | HTTPS Shopify, HSTS por defecto |
| Structured data | 50 | Product con `brand` = razón social del proveedor, sin Organization/WebSite |

## Crawlability

| # | Hallazgo | Archivo | Severidad |
|---|---|---|---|
| C1 | `<meta name="robots" content="index,follow">` fijo en **todas** las plantillas (search, cart, cuenta, colecciones filtradas por tag, paginadas). Choca con el `noindex` que Shopify inyecta cuando se oculta un recurso → señales contradictorias | `layout/theme.liquid:6` | Alta |
| C2 | No existe `templates/robots.txt.liquid` → robots.txt default de Shopify (bloquea /cart, /checkout, /search, filtros `+`). Aceptable | — | OK |
| C3 | Sitemap automático de Shopify: incluye las 147 colecciones, incluidas internas y vacías | `/sitemap.xml` | Alta |
| C4 | `{% section 'popup-beneficios' %}` llama a una sección que **no existe** → Shopify imprime `Liquid error: ... 'popup-beneficios' is not a valid section type` al pie de **cada página** | `layout/theme.liquid` (final del body) | Alta |

## Indexation

| # | Hallazgo | Cantidad | Severidad |
|---|---|---|---|
| I1 | Colecciones internas indexables: `destacados-prueba` (1,226), `precio-regular` (1,128), `promo-2do-articulo-15-precio-regular` (1,859), `globofilter-best-selling-products-index` (2,578), `frontpage` | 5 | Crítica |
| I2 | Colecciones vacías → soft 404: almacenamiento, apple, applewatch, click, computo, controles, fold-8, holders, hp, ipads-seminuevas, ohsnap, spigen, viaje | 13 | Alta |
| I3 | Redirect `/collections/computado` → `/collections/computo` (vacía) | 1 | Media |
| I4 | Colecciones duplicadas: `targus`/`targus-1`, `iphone13`/`iphone-13`, `iphone14`/`iphone`(=iPhone 14), `backbone`/`backbone-1`, `cases`/`fundas` | 5 pares | Alta |
| I5 | Productos clonados con handle `-1`, `-2` publicados (ej. `hifuture-flex-clip-open-ear-audifono-negro` y `…-negro-1`, ambos con stock) | 115 | Alta |
| I6 | Páginas `/collections/x/tag` indexables por C1, título "Tagged …" | — | Media |
| I7 | Solo 3 redirects 301 en toda la tienda tras años de cambios de handles | 3 | Media |

## Performance

| # | Hallazgo | Archivo | Severidad |
|---|---|---|---|
| P1 | `styles.css` 396 KB bloqueante (comentado: async causaba CLS). Purgar CSS sin usar | `assets/styles.css` | Alta |
| P2 | `vendors.js` 422 KB + `jquery.min.js` 87 KB (preload) + `sections.js` + `utilities.js` + `instantclick` | `layout/theme.liquid` | Alta |
| P3 | Script lazy-load pone `loading="lazy"` a **todas** las `<img>` tras DOMContentLoaded — no ayuda (ya se están descargando) y puede afectar la imagen LCP. Usar `loading="lazy"` en Liquid solo bajo el fold + `fetchpriority="high"` en la imagen principal | `layout/theme.liquid` | Media |
| P4 | Popup "Mientras más agregás" (≈200 líneas CSS/HTML inline) dentro de `theme.liquid` | `layout/theme.liquid` | Baja |
| P5 | Beacon a `app.outofthesandbox.com` (solo en editor) | `layout/theme.liquid` | Baja |
| P6 | 7 temas en la tienda (6 copias sin publicar) — riesgo operativo, no SEO | Admin → Temas | Baja |

## Mobile

| # | Hallazgo | Severidad |
|---|---|---|
| M1 | Popup full-screen con overlay y bloqueo de scroll a los **1.2 s** en home y colecciones `sale14/15/16`, `smartwatch` → "intrusive interstitial" de Google. Subir a ≥ 8 s o disparar con scroll 50% / exit intent; en mobile, usar banner inferior | Alta |
| M2 | Popup inline en `17-pro-max-1` aparece de inmediato (sin delay) | Alta |

## Structured Data

| # | Hallazgo | Archivo | Severidad |
|---|---|---|---|
| S1 | `brand.name = product.vendor` → publica "MOTEKTEAM INC", "Sand Sports, Corp", "Abboud Training Corporation", **"DIEGO ANDRES SEGURA VILLAGRAN"** (57 productos) como marca. Expone proveedores y tu nombre personal | `snippets/product__structured-data.liquid` | Crítica |
| S2 | `brand.@type = Thing` → debe ser `Brand` | mismo | Media |
| S3 | `barcode` enviado como `mpn` → debe ser `gtin13`/`gtin12` | mismo | Media |
| S4 | Sin `itemCondition`, `shippingDetails`, `hasMerchantReturnPolicy`, sin array de imágenes → no elegible para todos los rich results de Merchant Listings | mismo | Media |
| S5 | Sin schema `Organization` + `WebSite` (SearchAction) en el sitio | `layout/theme.liquid` | Media |
| S6 | Sin `LocalBusiness` (tienda zona 13, horario, teléfono) | — | Media |
| S7 | `og:title` y `twitter:title` = título de producto en MAYÚSCULAS, no el SEO title | `snippets/social-meta-info.liquid` | Baja |
| S8 | ItemList y BreadcrumbList en colecciones: OK | `sections/collection-template.liquid` | OK |

## International

- Solo `es` publicado, un market `gt`. `lang` dinámico. OK. 5 locales extra en el tema sin uso (no afecta).

## Priority Fixes

1. **[Critical]** S1 Vendor → marca — guardar proveedor en metafield `custom.proveedor`, luego vendor = marca (`vendor_a_marca.csv`, 2,458 mapeados, 120 por revisar).
2. **[Critical]** I1 Ocultar colecciones internas — metafield `seo.hidden = 1` (las saca del sitemap + noindex). No borrar: alimentan descuentos y filtros.
3. **[High]** C1 Quitar `index,follow` fijo; noindex condicional para search / tags / paginación > 1.
4. **[High]** C4 Quitar `{% section 'popup-beneficios' %}`.
5. **[High]** I2 Despublicar 13 colecciones vacías del canal Online Store + redirect 301 a la colección madre.
6. **[High]** I5 Unificar 115 clones: conservar el de más ventas, redirect 301 del resto, archivar.
7. **[High]** M1/M2 Retrasar popups (≥ 8 s o scroll) y versión banner en mobile.
8. **[Medium]** S2-S6 Reescribir `product__structured-data` + agregar Organization/WebSite/LocalBusiness.
9. **[Medium]** I4 Consolidar colecciones duplicadas + 301.
10. **[Medium]** P1-P3 Performance: purgar CSS, quitar lazy-load JS global, `fetchpriority` en LCP.

## Cómo se ejecuta

| Fix | Vía | Riesgo |
|---|---|---|
| 1, 2, 5, 6, 9 | Admin API (productos/colecciones/redirects) | Bajo — reversible; respaldo previo en `products.jsonl` |
| 3, 4, 7, 8, 10 | Copia del tema → edito → tú previsualizas → tú publicas | Nulo hasta publicar (API no permite escribir en tema live) |

## Estado de ejecución — Paso 1 (2026-10-27)

| Fix | Estado | Detalle |
|---|---|---|
| S1 Vendor → marca | ✅ Hecho | 2,458 productos verificados (export completo, 0 fallos). Proveedor original en metafield `custom.proveedor` (definición "Proveedor" creada) |
| S1 pendientes | ⏳ Diego | 120 productos sin marca clara: `vendor_a_marca.csv` columna `revisar = SI` (PULSERA, COMBO, GADGET, RESERVA, genéricos). Siguen con razón social: Ventas Guate (41), Ventas Guate 1 (12), MIRGOR USA LLC (9), Cali Peninsula East Corp (3), DIEGO ANDRES SEGURA VILLAGRAN (2), CAMACHO PHONES CORP (2), MATTER BRANDS (2), Imeqmo (1) |
| S1 proveedor = marca | ⏳ Diego | 14 productos donde vendor ya era la marca → proveedor quedó = marca (SwitchEasy, Solo New York, Tucano, MagEasy). Corregir a mano |
| I2 Colecciones vacías — noindex | ✅ Hecho | `seo.hidden = 1` en las 13 → fuera de sitemap + noindex |
| I2 Redirects 301 | ✅ Creados | 13 nuevos + `/collections/computado` corregido → `conectividad-1`. **Se activan al despublicar** |
| I2 Despublicar | ⏳ Diego | API bloquea despublicar. Admin → Productos → Colecciones → seleccionar las 13 → "Excluir de canales de venta" → Tienda online |
| Menús | ⏳ Diego | Main menu enlaza a ipads-seminuevas, almacenamiento, computo, holders, viaje; menú Gaming → controles. Funcionan vía 301, pero conviene quitarlos/reapuntarlos |

### Redirects creados

| Colección vacía | → Destino |
|---|---|
| holders | auto |
| almacenamiento, computo, hp, (computado) | conectividad-1 |
| viaje | maletines |
| apple | iphone-1 |
| click, spigen | cases |
| ipads-seminuevas | seminuevos |
| controles | gaming-1 |
| applewatch | pulseras-applewatch |
| ohsnap | magsafe (⚠ hay 8 productos OhSnap: mejor llenar la colección y borrar el redirect) |
| fold-8 | z-fold |
