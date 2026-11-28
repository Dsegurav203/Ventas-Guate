# Blog "Guías" · borradores noviembre 2026

**Estado: BORRADORES. Nada publicado en Shopify.** Fecha: 2026-11-28. Blog destino: `gid://shopify/Blog/99227795669` (`/blogs/guias`). Pedido por Diego Segura.

## Archivos

| Archivo | Artículo | Palabras | Enlaces internos |
|---|---|---|---|
| `01_hifuture.html` | HiFuture en Guatemala: guía de smartwatches y audífonos | 816 | 16 |
| `02_prodigee.html` | Dónde comprar Prodigee en Guatemala: distribuidor oficial | 796 | 23 |
| `03_funda_original_vs_generica.html` | Funda original vs funda genérica: por qué vale la pena | 970 | 13 |
| `04_cargadores_certificados.html` | Cargadores certificados: GaN, PD, Qi2 y por qué importan | 1,015 | 24 |

`propuesta.json`: título, handle, SEO title (≤ 60), meta (≤ 155), resumen (≤ 200), etiquetas, fuentes, `afirmaciones_sin_fuente` (vacío) y notas por artículo.

## Método

- Formato y estructura igualados a los 2 artículos existentes del blog (intro, H2, tablas/listas, preguntas frecuentes, enlaces a colecciones). Diferencias a propósito: **tú** (los existentes usan voseo) y **sin precios** (regla de ECOMMERCE_SEO.md).
- Datos de producto solo de: sitio oficial del fabricante (hifuturegroup.com, iamprodigee.com/products.json, itslaut.com, logiix.ca) o fichas publicadas en ventasguate.gt (`/products.json`, 1,331 productos leídos el 2026-11-28).
- Explicaciones técnicas generales (GaN, PD, PPS, Qi2, MagSafe, MFi, UL, CE, FCC, RoHS, MIL-STD-810) sin atribuir certificaciones a productos que no las declaran.
- 63 enlaces internos únicos verificados con `curl` → todos HTTP 200 (sin redirecciones).
- Datos del negocio (dirección, horario, WhatsApp, envío, garantía) de ECOMMERCE_SEO.md.

## Descartado por falta de fuente

- HiFuture "la marca más vendida / del momento": reemplazado por "una de las marcas que más buscan nuestros clientes" (Search Console).
- HiFuture Vela 14 días de batería e IP68 (ficha publicada): la página oficial dice hasta 7 días y no menciona IP68. Se usó 7 días. **Revisar la ficha del Vela.**
- Ultra3 sin enlace: no está publicado en la tienda.
- PPS, MFi, UL, CE, FCC: ningún cargador publicado lo declara en su ficha ni en el sitio oficial. El único cable MFi de Prodigee (USB-A a Lightning) no está publicado; el publicado (USB-C a Lightning) no indica MFi.
- GaN en LOGiiX Power Plus 65W Slim Duo y Power Plus 45W Duo: el SKU no coincide con un producto GaN en logiix.ca (45W Duo = LGX-13778, solo PD; 65W Slim Duo = LGX-13659, no aparece). GaN en Prodigee Energee 40W: la ficha no lo dice.
- Samsung kit 25W: ficha vacía, no se menciona PPS ni Super Fast Charging.
- LAUT Luxedge 6 pies: la página oficial no da cifra.
- Nimbus9 "garantía de por vida" (ficha): no se usó; contradice la garantía de 1 año de la tienda.
- Prodigee Super Glass "dureza 9H" (ficha): no se usó; el sitio oficial no lo indica.

## Para publicar (cuando Diego apruebe)

1. `articleCreate` en el blog 99227795669 con `title`, `handle`, `body` (contenido del .html), `summary`, `tags`, `isPublished:false` primero para revisar la vista previa.
2. SEO: metacampos `global.title_tag` y `global.description_tag`.
3. Registrar aquí fecha, id del artículo y quién aprobó.

## Aplicado

_(nada todavía)_
