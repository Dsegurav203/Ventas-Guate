# Auditoría SEO catálogo — ventasguate.gt — 2026-10-27

Fuente: Shopify Admin API (exportación completa). Sitio público no auditado (crawl bloqueado desde este entorno) → pendiente: velocidad, Core Web Vitals, robots/sitemap, schema renderizado.

## Inventario

| Métrica | Valor |
|---|---|
| Productos totales | 2,578 |
| Activos | 1,766 |
| Publicados en tienda online | 1,224 |
| Publicados con stock | **991** (universo prioritario) |
| Colecciones | 147 (solo ~19 con SEO) |
| Páginas | 2 (Contact, Marcas) |

## Hallazgos — 991 productos publicados con stock

| # | Problema | Productos | % | Impacto |
|---|---|---|---|---|
| 1 | Imágenes sin `alt` | 3,118 / 3,457 imgs | 90% | Alto — Google Images / Shopping |
| 2 | Sin SEO title → Google muestra título del producto en MAYÚSCULAS | 831 | 83% | Alto — CTR |
| 3 | Título de producto TODO MAYÚSCULAS | 870 | 87% | Alto — CTR, legibilidad |
| 4 | Descripción < 50 palabras | 696 | 70% | Alto — thin content |
| 5 | Sin meta description | 684 | 69% | Medio — CTR |
| 6 | Descripción vacía | 487 | 49% | Alto — no rankea |
| 7 | Productos `productType` vacío o "All" | 128 | 12% | Medio — feed Google Shopping / filtros |
| 8 | Meta rota: "Buy in Guatemala", "Guatemala Precio Guatemala", texto en inglés | 119 | 12% | Medio — se ve mal en SERP |
| 9 | Handles duplicados (`-1`, `-2`) → productos clonados compitiendo | 65 | 6% | Alto — canibalización |
| 10 | Sin imágenes | 37 | 3% | Alto — no convierte, sin Shopping |
| 11 | Alt "Cubo de carga Wemiss 45W" copiado en imágenes de power banks | 11 | — | Bajo — alt incorrecto |

Solo **37 de 991** productos pasan todos los checks. **676** fallan 4+.

## Hallazgos estructurales

| Problema | Detalle | Acción |
|---|---|---|
| Vendor = razón social del proveedor | `MOTEKTEAM INC` (Prodigee), `FUTURE ACCESS TECHNOLOGY CO., LIMITED` (HiFuture), `TARGUS US LLC`, `ETERNITY WIRELESS`, `GT ZKIN S.A.`, `Ventas Guate 1`. Shopify usa vendor como `brand` en el feed de Google y, en temas estándar (Dawn), en el schema Product | Cambiar vendor a la **marca** (Prodigee, HiFuture, Targus…). Expone además a tus proveedores ante competidores |
| Colecciones internas indexables | `destacados-prueba` (1,226), `precio-regular` (1,128), `promo-2do-articulo-15-precio-regular` (1,859), `globofilter-…-index` (2,578), `sale14/15/16`, `midnightsale` | `noindex` vía metafield `seo.hidden = 1` o template sin indexar |
| Colecciones vacías (0 productos) | almacenamiento, apple, applewatch, click, computo, controles, fold-8, holders, hp, ipads-seminuevas, ohsnap, spigen, viaje | Llenar o despublicar (soft 404) |
| Colecciones duplicadas | `targus` vs `targus-1`; `iphone13` vs `iphone-13`; `iphone14` vs `iphone`; `iphone12` vs `iphone-12-pro-max`; `backbone` vs `backbone-1`; `cases` vs `fundas` | Consolidar + redirect 301 |
| Colecciones clave sin SEO | `iphone-1` (281), `cases-samsung` (139), `iphone-17-pro`, `17-pro-max`, `iphone-18`, `cases-iphone-17`, `carga`, `cables`, `powerbanks`, `smart-home`, `true-wireless`, `targus` | Title + meta + 150-300 palabras de texto |
| Handle `iphone` = "iPhone 14" | Desperdicia la URL más valiosa | Renombrar a `iphone-14` + redirect; `iphone` → colección general |
| Solo 2 páginas | Falta: Sobre nosotros, Envíos, Garantía, Devoluciones, Tienda zona 13 (NAP), Preguntas frecuentes | Crear — señales E-E-A-T y SEO local |
| SEO title inconsistente | Algunos terminan en "\| Ventas Guate", otros no; uso de "—" mezclado | Plantilla única |

## Plantillas recomendadas

```text
SEO title (≤60):   {Tipo} {Marca} {Modelo} {Color} | Ventas Guate
Meta (140-155):    {Tipo} {Marca} {Modelo} en Guatemala. {Beneficio clave}. ✓ Original ✓ Garantía ✓ Envío a todo GT. Q{precio}.
Alt imagen:        {Tipo} {Marca} {Modelo} {Color} – vista {frontal|lateral|en uso}
Título producto:   Funda Prodigee KickIt iPhone 17 Pro Max Negro   (Title Case, tipo primero)
```

## Plan de ejecución (orden por ROI)

| Semana | Acción | Alcance | Método |
|---|---|---|---|
| 1 | Vendor → marca real | ~991 | Bulk edit Shopify (filtrar por vendor) |
| 1 | `noindex` colecciones internas + despublicar vacías | ~20 colecciones | Manual |
| 1 | Unificar duplicados `-1` (merge variantes, redirect 301) | 65 | Manual, empezar por los de más stock |
| 2 | SEO title + meta + alt, top 200 por stock | 200 | Generado por Claude vía API, revisión humana |
| 2 | SEO de 12 colecciones clave | 12 | Claude |
| 3-4 | Descripciones ≥ 120 palabras para los 487 vacíos | 487 | Claude por lotes de 50, por marca |
| 3-4 | Title Case en títulos de producto | 870 | Claude + bulk API |
| 4 | Páginas Envíos / Garantía / Nosotros / Tienda zona 13 + schema LocalBusiness | 5 | Claude |
| Continuo | Regla: ningún producto se publica sin title, meta, alt, descripción ≥ 80 palabras | — | Checklist para el equipo de carga |

## KPIs a seguir (Search Console + Shopify)

| KPI | Línea base | Meta 90 días |
|---|---|---|
| % productos con stock 100% OK | 3.7% (37/991) | 80% |
| % imágenes con alt | 10% | 95% |
| Clics orgánicos / mes | medir en GSC | +40% |
| CTR orgánico promedio | medir en GSC | +1.5 pp |
| Páginas indexadas válidas | medir en GSC | = productos publicados + colecciones útiles |
| Ventas canal orgánico | medir en Shopify Analytics | +25% |

## Archivos

- `catalogo_seo_fixlist.csv` — 991 productos con stock, ordenados por inventario, con columna `problemas` (`sin_title`, `sin_meta`, `meta_rota`, `desc_corta`, `alt_faltante`, `sin_imagen`).
