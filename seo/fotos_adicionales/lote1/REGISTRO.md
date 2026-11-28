# Lote 1 fotos / Merchant Center (aprobado por Diego 2026-11-27)
1. Vendor corregido en 63 productos que decían "Ventas Guate" (marca tomada del título). 7 sin marca identificable quedan igual (Silicón Case ×3, Adaptadores ×2, Waterproof Bag, Vidrio templado). Respaldo/propuesta: `vendor_propuesta_y_respaldo.json` (antes = "Ventas Guate").
2. 104 seminuevos iTronics con ≤1 foto: etiqueta `quitar-google` (`itronics_quitar_google.json`); Diego los excluye del canal Google & YouTube en Admin (publishableUnpublish bloqueado por API).
3. Fotos adicionales top 50 (sin iTronics): propuesta lista 2026-11-27 en `propuesta_fotos/` (propuesta.json + hoja_01..05.jpg). 12 productos con 30 fotos oficiales (LAUT, LOGiiX, Spigen y hermanos Prodigee publicados); 38 sin fuente con motivo. Pendiente aprobación de Diego; no se ha subido nada.
- 2026-11-28: Diego excluyó del canal Google & YouTube los 121 productos con etiqueta quitar-google (verificado: 0 publicados en Google).

## 2026-11-28 · Fotos adicionales aplicadas en Shopify (aprobado por Diego)
Fuente: `propuesta_fotos/propuesta.json`. Respaldo del media previo: `respaldo_media_2026-11-28.json`. Método: stagedUploadsCreate (IMAGE/POST, 30 subidas HTTP 201) → productUpdate(media). 30 fotos nuevas en 12 productos, todas READY. Las nuevas quedan después de la foto existente (excepto Superstar).

| Producto | Fotos antes → después | Media nuevos (gid://shopify/MediaImage/…) |
|---|---|---|
| Spigen Core Armor iPhone 15 Pro Negro | 1 → 4 | 47309884981461, 47309885014229, 47309885046997 |
| LAUT Typefolio 2.0 Keyboard iPad 10.9" (2022) Black | 1 → 4 | 47309885079765, 47309885112533, 47309885145301 |
| Prodigee Super Glass Camera iPhone 17 Negro | 1 → 2 | 47309885178069 (el 17 Air Black no se tocó) |
| LAUT Typefolio 2.0 Keyboard iPad 11" (2024) Black | 1 → 4 | 47309885210837, 47309885243605, 47309885276373 |
| LAUT Zentry AirPods 4 Negro | 1 → 4 | 47309885309141, 47309885341909, 47309885374677 |
| Prodigee Superstar iPhone 16 Rosado | 1 → 4 | 47309885440213, 47309885472981, 47309885505749 |
| LAUT Huex Protect AirPods Pro3 Frost | 0 → 3 | 47309885538517, 47309885571285, 47309885604053 |
| LAUT Shield iPhone 16E Negro | 0 → 3 | 47309885636821, 47309885669589, 47309885702357 |
| LAUT Huex Protect AirPods Pro3 Bronze | 0 → 3 | 47309885735125, 47309885767893, 47309885800661 |
| LAUT Holo iPhone 16 Pro Pearl | 0 → 2 | 47309885833429, 47309885866197 |
| LAUT Huex Protect AirPods Pro3 Light Pink | 1 → 3 | 47309885898965, 47309885931733 |
| LOGiiX Phantom Glass Super Tempered Anti Reflective iPhone 17 Pro Clear | 0 → 1 | 47309885964501 |

- **Reorden Superstar iPhone 16 Rosado**: productReorderMedia movió la foto vieja (39131580399829, muestra iPhone Pro) a la posición 3 (última). Principal ahora = 47309885440213 (nueva 01). Verificado featuredMedia. La foto vieja no se borró.
- Reversión: borrar los media nuevos (productDeleteMedia / fileDelete) y, en el Superstar, mover 39131580399829 a posición 0.
