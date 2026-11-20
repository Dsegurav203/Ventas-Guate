# Velocidad del tema (19/11/2026)

Medición: Playwright, Moto G4, CPU x4, red 1.6 Mbps / 150 ms (PageSpeed API sin cuota ese día).

| Página | LCP | CLS | Peso | Requests | Causa principal |
|---|---|---|---|---|---|
| Inicio | 7.1 s | 0.08 | 2.5 MB | 131 | El LCP es la imagen del **popup** (abre a 1.2 s) |
| Colección (cases-iphone) | 1.5 s | **0.57** | 3.3 MB | 203 | Filtros del sidebar abiertos y luego cerrados por JS en móvil |
| Producto | 1.4 s | 0.00 | 1.6 MB | 113 | OK |

Umbrales de Google: LCP < 2.5 s, CLS < 0.1.

## Cambios (tema en vivo "Fix Buscador + Error Popup", guardados, pendientes de publicar)
1. `snippets/sidebar.liquid`: script inline al final que cierra los filtros en móvil antes del primer pintado. Probado: CLS 0.57 → 0 y los filtros siguen abriendo al tocar.
2. `snippets/sale16-popup.liquid`: popup abre al 40% de scroll (o a los 20 s) en vez de 1.2 s; imagen con `loading="lazy" fetchpriority="low"`. Quita el popup como LCP y el "intersticial intrusivo".
3. (pendiente de antes) `store-schema` + JSON-LD del blog.

## Siguientes (requieren más trabajo)
- JS: jquery 87 KB + vendors 422 KB + sections/app; Facebook pixel 204 KB.
- CSS `styles.css` 396 KB render-blocking.
- 600 KB de `link` (preloads) en inicio/producto.
- Publicación del tema rechazada otra vez (changed_on_shopify, 19/11). Pasos 6-7 de velocidad enviados a Luis en tarea #15.
