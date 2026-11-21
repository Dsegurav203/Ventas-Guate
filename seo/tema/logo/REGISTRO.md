# Logo móvil (21/11/2026)
- Problema: el logo móvil del tema (`favicon-mobil.png`) era un JPEG de 100×50 con fondo blanco; en el encabezado oscuro se veía pequeño y con un recuadro blanco.
- Cambio (tema MAIN "Fix Buscador + Error Popup", commit 586e5db): nuevo `assets/logo-movil-blanco.png` (450×100, transparente, "ventas" en blanco, "guate" azul y el ícono verde originales) y en `sections/header.liquid` el bloque `mobile_logo` usa ese archivo con un tamaño máximo de 170×34 px en pantallas de 798 px o menos.
- Pendiente: publicar el tema (theme_publish). El mismo publish lleva los cambios del 19/11 (schema ElectronicsStore, blog, CLS del sidebar, popup).
- Reversión: volver a `src="{{ section.settings.logo_mobile | img_url: '410x' }}"` y quitar el `<style>` agregado. Archivo anterior: `favicon-mobil.png` en esta carpeta.
