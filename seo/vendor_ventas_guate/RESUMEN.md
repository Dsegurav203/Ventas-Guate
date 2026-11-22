# Productos Shopify con vendor "Ventas Guate" — marca propuesta

Fecha: 2026-11-21 · Solo lectura (no se cambió nada en Shopify ni Odoo). Detalle: `lista.csv`.

- Productos activos con vendor "Ventas Guate": **273**
- Publicados en la tienda en línea (onlineStoreUrl): **50**
- Sin marca identificable (REVISAR): **37**
- Fuente de la marca: capa del conector 23 · SKU/código de barras 211 · título 2 · REVISAR 37

Criterio: 1) `shopify.product.template.ept` (shopify_tmpl_id) → `product.template.brand_id`; 2) SKU (sin "L" inicial si el resto son dígitos) en `product.product.default_code` o `barcode` → `brand_id`; 3) primera(s) palabra(s) del título si coincide con una marca de `product.brand`; si no, REVISAR.

| Marca propuesta | Productos | Publicados |
|---|---:|---:|
| Targus | 24 | 0 |
| LOGiiX | 18 | 1 |
| Mybat | 16 | 3 |
| Prodigee | 16 | 0 |
| Click | 15 | 0 |
| Nimbus9 | 15 | 1 |
| Laut | 12 | 8 |
| Hyper | 10 | 0 |
| Moft | 9 | 0 |
| Planet Buddies | 9 | 0 |
| Defunc | 8 | 0 |
| Gadget Guard | 8 | 0 |
| Amazon | 6 | 4 |
| Zizo | 6 | 0 |
| Apple | 5 | 0 |
| Sympl | 5 | 0 |
| Matter | 4 | 0 |
| Naztech | 4 | 0 |
| Artscase | 3 | 0 |
| Popsockets | 3 | 0 |
| Silicone Case | 3 | 3 |
| Urbanista | 3 | 0 |
| Ballistic | 2 | 2 |
| Kingston | 2 | 0 |
| Ohsnap | 2 | 0 |
| Samsung | 2 | 0 |
| Solo | 2 | 0 |
| Spigen | 2 | 0 |
| Wild Flag | 2 | 2 |
| Adventurer | 1 | 0 |
| Aircomm | 1 | 0 |
| Anker | 1 | 0 |
| Argom | 1 | 0 |
| Arq1 | 1 | 0 |
| Aukey | 1 | 0 |
| Broadlink | 1 | 0 |
| Gear | 1 | 1 |
| Itskins | 1 | 1 |
| Jlab | 1 | 0 |
| Mcdodo | 1 | 0 |
| Mopoint | 1 | 0 |
| Rock | 1 | 0 |
| Speck | 1 | 0 |
| Torras | 1 | 1 |
| Tp-Link | 1 | 0 |
| Uag | 1 | 1 |
| Unno | 1 | 0 |
| White Diamonds | 1 | 0 |
| Woodcessories | 1 | 0 |
| REVISAR | 37 | 22 |

## REVISAR

Observaciones (no aplicadas, solo para decidir):
- **Reelcharge (8, publicados, 60 u c/u)**: no existe en `product.brand` ni se encontraron sus SKU en Odoo; es marca oficial, habría que crearla.
- Pistas por título sin marca en Odoo: Duo JLAB Studio + → Jlab; Pack Gadget Guard → Gadget Guard; Maybat Pro → MyBat (typo); Cellhelmet, Spidercase, Qie, Simple no existen en `product.brand`.
- Combos (6) y genéricos (adaptadores, vidrios, pulseras, Watchband, Waterproof Bag, Sticky Pad) no tienen marca única: decidir vendor genérico.
- "Gear" (Gear 4 Bridgetown) viene de la capa; la marca correcta sería Gear4.

| shopify_id | Título | Publicado | Inventario | SKU |
|---|---|---|---:|---|
| 15480764072149 | Adaptador 1 Puerto 3.5mm a 2 Puertos Audio y Micrófono | no | 3 | 9000000000887 |
| 15480759779541 | Adaptador Splitter Lightning a Doble Lightning | no | 1 | G102 |
| 15480763089109 | Adopted Leather Wrap iPhone 6/6S Plus Blanco | no | 1 | 819312013062 |
| 15480763613397 | AirPods Adaptador Sport de Silicón | no | 3 | 50200001 |
| 9533674127573 | Cellhelmet Powerbank con Cable 3000mAh Blanco | si | 1 | 811341032465 |
| 9265380720853 | Combo 8 Bombillos Smart Amazon Basics RGB – Compatibles con Alexa | si | 9 |  |
| 9574363889877 | Combo Balance iPhone 15 Pro Max | si | 5 |  |
| 9574349766869 | Combo Itskins iPhone 15 Pro Max | si | 5 |  |
| 9350587351253 | Combo MagSafe | no | 0 |  |
| 9574329876693 | Combo Mophie iPhone 15 Pro Max | si | 5 |  |
| 9350586630357 | Combo Smart Fitness: Smartwatch Kieslect KS Mini + Baseus Eli Sport | si | 2 |  |
| 9261317718229 | Duo JLAB Studio + | si | 2 |  |
| 15480776261845 | Flat Mini Cable C-C Back | no | 1 | 810098739061 |
| 15420254322901 | Funda Galaxy S21 Ultra | si | 0 |  |
| 15480763842773 | Maybat Pro Vidrio Templado iPhone 13 Pro Max Privacy | no | 1 | L885126693493 |
| 9356552634581 | Pack - Gadget Guard Vidrio templado iPhone 15/14/13 - Pack de 5 unidades | si | 12 |  |
| 15480762728661 | Qie Enabler Micro USB | no | 3 | 10108 |
| 15546869711061 | Reelcharge Cargador de Pared Smart 45W Tipo C Gris | si | 60 | 850083897307 |
| 15546869809365 | Reelcharge Fusion Powerbank 5000mAh + Cargador 65W Blanco | si | 60 | 850083897277 |
| 15546869776597 | Reelcharge Fusion Powerbank 5000mAh + Cargador 65W Negro | si | 60 | 850083897260 |
| 15546869743829 | Reelcharge Holder Inalámbrico Rejilla 15W Cable Retractil Negro | si | 60 | 850083897086 |
| 15546869907669 | Reelcharge Reelsafe Glass Powerbank Magnético 5000mAh Gris | si | 60 | 850083897222 |
| 15546870005973 | Reelcharge Reelsafe Glass Powerbank Magnético 5000mAh Plata | si | 60 | 850083897239 |
| 15546869874901 | Reelcharge Reelsafe Powerbank 10000mAh Semi Solido Gris | si | 60 | 850083897208 |
| 15546869842133 | Reelcharge Reelsafe Powerbank 5000mAh Semi Solido Gris | si | 60 | 850083897185 |
| 15480773902549 | Simple Smart Tag 4 Pack White | no | 2 | 810135814560 |
| 9377151025365 | Spidercase Funda Magnética para Samsung Galaxy S25 FE | si | 0 |  |
| 9378100183253 | Spidercase Funda Magnética para Samsung Galaxy S25 FE - Negro | si | 0 |  |
| 15480767742165 | Sticky Pad Negro | no | 9 | 24243 |
| 15480769118421 | Vidrio Templado Cámaras 12 Pro Max | no | 2 | 20257 |
| 15480771608789 | Vidrio Templado Gorilla Glass iPhone 17 Pro Max | no | 10 | 6727 |
| 9389089456341 | Watch Pulsera para Apple Watch 38/40mm Fuscia | si | 1 | 95123119250 |
| 9389089489109 | Watch Pulsera para Apple Watch 42/44mm Amarillo | si | 0 | 95123119225 |
| 9389089521877 | Watch Pulsera para Apple Watch 42/44mm Rosado | si | 1 | 95123119475 |
| 15480762892501 | Watchband Milannesse Loop 38/40 Mm Lila Gold | no | 1 | WBM09 |
| 15480762925269 | Watchband Milannesse Loop 42/44 Mm Rose Gold | no | 1 | WBM08 |
| 15480762958037 | Waterproof Bag | no | 1 | 1020026510023 |
