---
name: velocidad-tema
description: Mide la velocidad móvil de ventasguate.gt (LCP, CLS, peso), encuentra la causa y prepara correcciones en el tema Turbo. Usar cuando pidan "velocidad", "PageSpeed", "Core Web Vitals", "la página está lenta", "salta la pantalla", "popup".
---

# Velocidad del tema

Sigue `CLAUDE.md` (tema publicado, no forzar publicación). Referencia: `seo/tema/VELOCIDAD_2026-11-19.md`.

## 1. Medir
- PageSpeed Insights API (`/pagespeedonline/v5/runPagespeed?strategy=mobile`) si hay cuota.
- Si no: Playwright con `devices['Moto G4']`, CPU x4 y red 1.6 Mbps/150 ms; `PerformanceObserver` para `largest-contentful-paint` (guardar el elemento) y `layout-shift` (guardar `sources`). Páginas: inicio, una colección con filtros, un producto.
- Metas: LCP < 2.5 s, CLS < 0.1.

## 2. Causas ya conocidas
- Popup `snippets/sale16-popup.liquid` abría a 1.2 s y se volvía el LCP → abrir al 40% de scroll o a los 20 s, imagen `loading="lazy" fetchpriority="low"`.
- Filtros `snippets/sidebar.liquid` abiertos que el JS cerraba en móvil (CLS 0.57) → script inline al final del snippet que quita `open` en ≤ 798 px.
- Pendiente mayor: `styles.css` 396 KB bloqueante, jQuery + vendors.js (~600 KB JS), píxel de Facebook 204 KB.

## 3. Probar antes de tocar el tema
Inyectar la corrección con `page.addInitScript` en Playwright sobre el sitio en vivo y comparar CLS/LCP antes y después; verificar que la interacción (abrir filtros, cerrar popup) siga funcionando.

## 4. Aplicar
- `theme_bash` sobre el tema MAIN → `theme_commit` → `theme_publish` solo con "sí" explícito.
- Si `theme_publish` devuelve `changed_on_shopify`, no forzar: entregar los pasos con el código exacto para aplicarlos en Admin → Tienda online → Temas → Editar código (tarea en Odoo al encargado).
- Volver a medir y registrar en `seo/tema/`.
