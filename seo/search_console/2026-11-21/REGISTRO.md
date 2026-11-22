# Registro · redirecciones 404 (aprobado por Diego 2026-11-22)

- Fuente: drilldown "Not found (404)" de Search Console (1,000 ejemplos → 451 productos; 40 ya publicados de nuevo).
- Propuesta: `redirecciones_404_propuesta.csv` (415).
- Aplicado: **404 redirecciones 301 creadas** (`aplicado/redir_resp_*.json`).
  - 11 ya tenían redirección previa ("Path has already been taken"), se dejaron como estaban.
  - 4 LOGiiX Cabrio iPad apuntaban a `/collections/ipads-seminuevas` (que es a su vez una redirección) → creadas hacia `/collections/logiix`.
- Las redirecciones de Shopify solo actúan si la URL da 404: un producto republicado (Flow) se muestra normal.
- Revertir: `urlRedirectDelete(id)` con los IDs de `aplicado/`.
- IDs LOGiiX: 776892154069, 776892186837, 776892219605, 776892252373 (gid://shopify/UrlRedirect/…).
