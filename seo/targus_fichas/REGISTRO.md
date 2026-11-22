# Fichas Targus: registro de lo aplicado (2026-11-22)

Aprobado por Diego Segura el 22/11/2026. Fuente: `propuesta.json` (las 22 fichas en estado "listo"). Respaldo previo de Shopify en `respaldo.json`. Respaldo de títulos de Odoo en `respaldo_odoo_titulos.json`.

## Resumen

| Concepto | Resultado |
|---|---|
| Productos actualizados en Shopify | 22 de 22, sin `userErrors` |
| Imágenes subidas | 85 (stagedUploadsCreate en 5 lotes, 85/85 HTTP 201), orden 1..4, alt = título final |
| Descripción, SEO title, meta y vendor "Targus" | 22 |
| Títulos cambiados en Shopify | 7 |
| Títulos replicados en Odoo (`shopify.product.template.ept.name` y `product.template.name` en es_GT y en_US) | 7, verificados |
| No se tocaron | AKP11US-61BL (15480780685525) y AKB867ES (15480782225621), ambos SIN FUENTE |
| Errores | Ninguno |

Nota: el vendor ya era "Targus" en las 22 cuando se aplicó el cambio (alguien lo había cambiado después de `respaldo.json`, que dice "Ventas Guate"). No se cambió el estado, las etiquetas (`pendiente-publicar-odoo`) ni la publicación en canales de venta.

## Títulos cambiados (Shopify y Odoo)

| Parte Odoo | Shopify ID | Título anterior | Título nuevo | Capa / template Odoo |
|---|---|---|---|---|
| AMM174AMGL | 15480780456149 | Targus Activen Stylus iPad White | Targus Active Stylus iPad White | 4631 / 14641 |
| THZ784GL-70 | 15480780718293 | Targus Safe Fit 6.8-9" 360° Rotating Tablet Black | Targus Safe Fit 6.8-9" 360° Rotating Tablet Case Black | 4633 / 14649 |
| TSS898-93 | 15480780914901 | Targus 15-16" Business Cacual Slipcase Black | Targus 15-16" Business Casual Slipcase Black | 4640 / 14655 |
| TBB663GL-90 | 15480781996245 | Targus Pro-Tek(R) 16" Backpack Black | Targus Pro-Tek 16" Tech Backpack Black | 4636 / 14658 |
| AKB871US-51 | 15480782323925 | Targus Sustainable Ergonomic Wireless EcoSmart Keyboard | Targus Sustainable Ergonomic Wireless EcoSmart Keyboard Black | 4630 / 14666 |
| AWE81US-54 | 15480782356693 | Targus Chill Mat 4-Port Hub Blueberry | Targus 17" Chill Mat+ with 4-Port Hub Black | 4619 / 14667 |
| TBS975GL-90 | 15480782422229 | Targus 15-16" Chromatic Sleeve Black | Targus 15-16" Puffer Sleeve Black | 4628 / 14669 |

Excepciones de color:
- **AWE81US** (Chill Mat 4-Port Hub): Diego confirmó que es negro; se usó el título nuevo propuesto y la descripción sin cambios.
- **AWE57US** (Gaming Chill Mat, 15480782389461): se dejó el título actual "Targus Gaming Chill Mat Black". La descripción y el SEO no mencionan color. El alt de las imágenes usa el título actual.

## Productos aplicados (22)

| Shopify ID | Parte Odoo | Título final | Imágenes |
|---|---|---|---|
| 15480775606485 | TBB617GL-90 | Targus Mobile Elite Backpack 15/16" Black | 4 |
| 15480780325077 | APA11606TT-90 | Targus 65W Multi Port Charger White | 4 |
| 15480780423381 | TSB710US-92 | Targus 16” Ascend Backpack Black | 4 |
| 15480780456149 | AMM174AMGL | Targus Active Stylus iPad White | 4 |
| 15480780488917 | AWE69US-53 | Targus Laptop Chill Mat Black | 4 |
| 15480780619989 | TBS98202GL | Targus Chromatic Sleeve 13-14" Blue | 4 |
| 15480780718293 | THZ784GL-70 | Targus Safe Fit 6.8-9" 360° Rotating Tablet Case Black | 4 |
| 15480780816597 | TBS98304GL-70 | Targus 15-16" Chromatic Sleeve Grey | 4 |
| 15480780882133 | TBS98207GL-70 | Targus 13-14" Chromatic Sleeve Purple | 4 |
| 15480780914901 | TSS898-93 | Targus 15-16" Business Casual Slipcase Black | 3 |
| 15480781930709 | TSB89104US-92 | Targus 15.6" Sport Backpack Black | 4 |
| 15480781996245 | TBB663GL-90 | Targus Pro-Tek 16" Tech Backpack Black | 2 |
| 15480782029013 | AMP06704AMGL | Targus Control Plus EcoSmart Presenter with Laser Grey | 4 |
| 15480782061781 | TBS98205GL-70 | Targus 13-14" Chromatic Sleeve Green | 4 |
| 15480782094549 | TBS98302GL-70 | Targus 15-16" Chromatic Sleeve Blue | 4 |
| 15480782127317 | TBS98307GL-70 | Targus 15-16" Chromatic Sleeve Purple | 4 |
| 15480782192853 | TBS98305GL-70 | Targus 15-16" Chromatic Sleeve Green | 4 |
| 15480782291157 | TBS98204GL-70 | Targus 13-14" Chromatic Sleeve Grey | 4 |
| 15480782323925 | AKB871US-51 | Targus Sustainable Ergonomic Wireless EcoSmart Keyboard Black | 4 |
| 15480782356693 | AWE81US-54 | Targus 17" Chill Mat+ with 4-Port Hub Black | 4 |
| 15480782389461 | AWE57US | Targus Gaming Chill Mat Black | 4 |
| 15480782422229 | TBS975GL-90 | Targus 15-16" Puffer Sleeve Black | 4 |

Verificación (consulta posterior): 15480775606485, 15480782356693 y 15480782389461 tienen 4 imágenes READY con el alt correcto, y su título, descripción y SEO coinciden con la propuesta.

## Cómo revertir

1. **Shopify**: para cada producto de `respaldo.json`, `productUpdate(product:{id, title, vendor, descriptionHtml, seo:{title, description}})` con los valores guardados ahí (antes: descripción vacía, SEO nulo, sin imágenes). Las imágenes se borran con `productDeleteMedia` o `fileUpdate(... referencesToRemove)` usando los IDs de `product.media`.
2. **Odoo**: para cada registro de `respaldo_odoo_titulos.json`, escribir `capa_name` en `shopify.product.template.ept` (`capa_id`), y `name_es_GT` / `name_en_US` en `product.template` (`product_tmpl_id`) con `context={"lang": "es_GT"}` y `{"lang": "en_US"}`.
