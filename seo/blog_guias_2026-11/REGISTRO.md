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
- ~~HiFuture Vela 7 días~~ y ~~Ultra3~~: ver "Cambios 2026-11-28" abajo.
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

## Cambios 2026-11-28 (aprobados por Diego Segura; siguen como borradores, nada publicado)

1. **Dirección**: "Edificio Trafalgar" → "Edificio Plaza Trafalgar" en las 4 guías (1 ocurrencia cada una).
2. **HiFuture Vela**: se usan los datos de la ficha publicada en ventasguate.gt (Diego decidió dejar la ficha como está): AMOLED, GPS integrado, IP68, frecuencia cardíaca y SpO2, más de 100 modos deportivos, **hasta 14 días** de batería. Brújula y altímetro se mantienen (sitio oficial, no contradice la ficha). Se quitaron "Super AMOLED 1.43"", "Syntra AI" y "2 GB para música" de la fila de la tabla (Syntra sigue explicado en la sección de términos, fuente oficial).
3. **Ultra3 → Ultra4 Pro**: en hifuturegroup.com el único modelo Ultra4 es **ULTRA4 PRO** (`/products/ultra4-pro`, en `products.json` desde 2026-11-18; body vacío, datos tomados del HTML de la página). Datos usados: AMOLED 1.95", GPS integrado con mapas sin conexión, brújula y altímetro, resistencia al agua 50 m, más de 170 modos deportivos, llamadas desde la muñeca, hasta 15 días de batería. No hay ficha del Ultra4 en ventasguate.gt (Admin, 0 resultados) → mención sin enlace + "confirma disponibilidad por WhatsApp". También se agregó a la viñeta de GPS y a la pregunta frecuente "¿Cuál smartwatch HiFuture tiene GPS?". Si el producto que llegará se llama solo "Ultra4" (sin Pro), ajustar el nombre.
4. **Prodigee Mag Chill Station**: confirmado, la guía 4 ya usa la descripción de nuestra ficha ("Prodigee Mag Chill Station Qi2: hasta 15W para el teléfono"; ficha: estación de carga inalámbrica 4 en 1, Qi2 magnético, 15W smartphone). Sin cambio.
5. `propuesta.json`: fuente `ultra3` → `ultra4-pro`; notas actualizadas (Vela, Ultra4 Pro, dirección, Mag Chill).
6. `borradores_guias.html` regenerado con el mismo formato (generador verificado: con los archivos anteriores reproduce byte a byte la versión previa; enlaces relativos → `https://ventasguate.gt/…`).

## Corrección de las 2 guías ya publicadas (propuesta, NO aplicada)

Carpeta `correccion_existentes/`: respaldo y propuesta de "Regalos tecnológicos de Navidad…" y "¿Qué audífonos Skullcandy comprar?" (voseo → tú, sin precios; la dirección ya decía Plaza Trafalgar). Detalle en `correccion_existentes/CAMBIOS.md`.

## Aplicado

_(nada todavía)_
