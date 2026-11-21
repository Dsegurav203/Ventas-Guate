# Arreglos de la semana (auditoría SEO 21/11/2026)

| Cambio | Estado | Respaldo / reversión |
|---|---|---|
| Colección Tucano: condición "proveedor = Tucano" agregada (1 → 91 productos); proveedor Tucano en Isotta 13-14 rosado y Alunno amarillo | Aplicado | Quitar la condición de proveedor (la condición original metafield custom.brand = Tucano se conserva) |
| Colección Tucano: texto, SEO title/meta e imagen (banner 50%) | Aplicado | Antes: sin texto, sin SEO, sin imagen |
| Menú principal: quitadas Almacenamiento, Computo, Holders, Viaje (0 productos) e iPads Seminuevas; agregadas Carga MagSafe, Mochilas y maletines Tucano, Smartwatch, Targus | Aplicado | `menu_principal_respaldo_2026-11-21.json` |
| Ficha reserva: handle `reserva-iphone-18-ultra` → `reserva-iphone-duo-256gb-blanco` (301 automático), proveedor Apple, SEO title | Aplicado | Revertir handle/proveedor |
| 270 descripciones sin precios ni envío Q35 | **Aplicado 21/11/2026** (aprobado por Diego; 270 aplicados, 0 omitidos, 0 errores; log `descripciones_precios_aplicado.json`) | `descripciones_precios_propuesta.json` / `_respaldo.json` |
| Tema: copia "Ventas Guate 21-nov (SEO + logo móvil)" (gid 188380643541) del tema en vivo con: logo móvil blanco, schema ElectronicsStore, JSON-LD blog, CLS sidebar, popup diferido, banner Tucano primera diapositiva | **Publicado por Diego 21/11/2026**. Verificado en vivo: logo 153×34, ElectronicsStore presente, CLS colección 0 | El tema actual "Fix Buscador + Error Popup" queda sin cambios como respaldo |
