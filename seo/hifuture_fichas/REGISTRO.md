# Registro · fichas HiFuture publicadas en Shopify

**Fecha:** 2026-11-22 (~03:02–03:07 UTC) · **Aprobó:** Diego Segura · **Aplicó:** Claude (Admin GraphQL `productUpdate`, 6 lotes, 0 userErrors)

## Qué se aplicó
- **44 fichas publicadas** desde `propuesta.json`: `descriptionHtml` = `html`; `seo` = `{title: seo_title, description: seo_description}` (siempre ambos juntos). Títulos de producto **no** se tocaron.
  - 31 reescrituras (fuente hifuturegroup.com) + 13 ajustes de voseo a "tú".
- **Vendor corregido a "HiFuture"** en los 10 productos que tenían `FUTURE ACCESS TECHNOLOGY CO., LIMITED`: 9 de las fichas + **WM200** (`15529159065813`, solo vendor; sin descripción por no tener fuente).
- Búsqueda `vendor:'FUTURE ACCESS TECHNOLOGY CO., LIMITED'` después del cambio: **0 productos**.

## Omitidas
- **HiFuture WM200 Micrófono Inalámbrico Grey** (`15529159065813`): SIN FUENTE (no existe ficha WM200 en hifuturegroup.com). Solo se corrigió el vendor.
- Ninguna ficha se omitió por cambios posteriores: el respaldo fresco coincidió con `respaldo.json` en las 45.

## Verificación
- Las 45: vendor = HiFuture; SEO title/description = propuesta (45/45 coinciden).
- `descriptionHtml` idéntico a la propuesta en 4 fichas revisadas: ColorBuds3 Pearl White, MusicSoul 200, FlyBuds 4 ANC Negro, Lyra Silver Grey.

## Pendientes detectados (texto ya publicado, venía así en la propuesta)
- Correa Anchor-E Rosado: errata "No compatibble con otros smartwatches".
- Vocalist 100 Negro: viñeta "True Wireless Stereo (emparejá dos)" sigue en voseo.

## Cómo revertir
`respaldo_previo_publicacion.json` tiene el estado leído justo antes de publicar (descriptionHtml, seo, vendor, updatedAt). Para cada producto: `productUpdate(product:{id, descriptionHtml, seo:{title, description}, vendor})` con esos valores (enviar `seo.title` y `seo.description` juntos). Las 10 fichas con vendor FUTURE ACCESS tenían `descriptionHtml` vacío y `seo` nulo.

## Detalle
| Producto | ID | Tipo | Vendor |
|---|---|---|---|
| Audífonos HiFuture Colorbuds3 – Pearl White | `9329910022357` | reescritura | — |
| HiFuture Lyra Health Tracker Sin Pantalla Black | `15529158836437` | reescritura | FUTURE ACCESS → HiFuture |
| Audífonos HiFuture SoniCore ANC – Negro | `9613271302357` | reescritura | — |
| Audífonos HiFuture SonicAir – Negro | `9456737124565` | reescritura | — |
| Smartwatch HiFuture Evo3 – Negro | `9613273563349` | reescritura | — |
| Audífonos HiFuture SoniCore ANC – Azul | `9613271236821` | reescritura | — |
| HiFuture Lyra Health Tracker Sin Pantalla Silver Grey | `15529158869205` | reescritura | FUTURE ACCESS → HiFuture |
| Audífonos HiFuture Colorbuds3 – Titanium | `9329910513877` | reescritura | — |
| Bocina HiFuture Passion S – Latte | `9613274218709` | reescritura | — |
| Bocina HiFuture Lino S – Negro | `9613273727189` | reescritura | — |
| HiFuture Flybuds4 Ai ANC True Wireless Latte | `15529158803669` | reescritura | FUTURE ACCESS → HiFuture |
| Bocina HiFuture Passion S – Negro | `9613274153173` | reescritura | — |
| HiFuture Flybuds4 Ai ANC True Wireless Black | `15529158770901` | reescritura | FUTURE ACCESS → HiFuture |
| Audífonos HiFuture Sonify2 Open Ear – Navy Blue | `9613274349781` | reescritura | — |
| HiFuture Flex3 Smartwatch Ultra Slim Metallic Grey | `15529158672597` | reescritura | FUTURE ACCESS → HiFuture |
| HiFuture Flex3 Smartwatch Ultra Slim Titanium | `15529158705365` | reescritura | FUTURE ACCESS → HiFuture |
| Audífonos HiFuture VibeMate Open Ear – Latte | `9613272678613` | reescritura | — |
| Smartwatch HiFuture Vortex Sport – Latte | `9456737321173` | reescritura | — |
| Audífonos HiFuture VibeMate Open Ear – Negro | `9613272514773` | reescritura | — |
| Smartwatch HiFuture Evo3 – Silver | `9613273694421` | reescritura | — |
| Bocina HiFuture Lino S – Verde | `9613273858261` | reescritura | — |
| Bocina HiFuture Lino S – Azul | `9613273792725` | reescritura | — |
| Audífonos HiFuture SonicAir – Blanco | `9456737255637` | reescritura | — |
| HiFuture Passion M Lifestyle Wireless Bocina Black | `15529158967509` | reescritura | FUTURE ACCESS → HiFuture |
| HiFuture Passion M Lifestyle Wireless Bocina Latte | `15529159033045` | reescritura | FUTURE ACCESS → HiFuture |
| HiFuture MUSICSOUL200 Karaoke Wireless Bocina Metallic Grey | `15529158934741` | reescritura | FUTURE ACCESS → HiFuture |
| Bocina HiFuture Orbit – Negro | `9613270876373` | reescritura | — |
| Audífonos HiFuture FutureMate Open Ear – Gris | `9142015656149` | reescritura | — |
| Smartwatch HiFuture Vortex Sport – Black | `9456737288405` | reescritura | — |
| Audífonos HiFuture VibeMate Open Ear – Hot Pink | `9613272580309` | reescritura | — |
| Smartwatch HiFuture Evo3 – Rose Gold | `9613273628885` | reescritura | — |
| Audífonos HiFuture FlyBuds 4 ANC – Negro | `9142015492309` | voseo | — |
| Correa HiFuture Anchor-E para Smartwatch – Rosado | `9329902846165` | voseo | — |
| Smartwatch HiFuture Flex2 – Silver | `9142015361237` | voseo | — |
| Bocina HiFuture Vocalist 100 con Micrófono – Negro | `9142016770261` | voseo | — |
| Audífonos HiFuture Tour MKII Over-Ear ANC – Negro | `9329900454101` | voseo | — |
| Audífonos HiFuture Tour MKII Over-Ear ANC – Offwhite | `9329900650709` | voseo | — |
| Smartwatch HiFuture Edge – Púrpura | `9329910874325` | voseo | — |
| Bocina HiFuture Alpha – Azul | `9142014083285` | voseo | — |
| Smartwatch HiFuture Aura2 – Negro | `9142014279893` | voseo | — |
| Smartwatch HiFuture Edge – Negro | `9142014869717` | voseo | — |
| Smartwatch HiFuture Flex2 – Negro | `9149965959381` | voseo | — |
| HiFuture Aura2 Smartwatch Silver | `9329904648405` | voseo | — |
| Bocina HiFuture Boombeat Outdoor – Negro | `9329907335381` | voseo | — |
| HiFuture Wm200 Micrófono Inalámbrico Grey | `15529159065813` | SIN FUENTE (no publicada) | FUTURE ACCESS → HiFuture |
- 22/11: corregidas erratas posteriores: Anchor-E Rosado ("compatibble" → "No es compatible") y Vocalist 100 Negro ("emparejá" → "empareja").
