# Propuesta descripciones Prodigee (ventasguate.gt)

**Estado: SOLO PROPUESTA — nada aplicado en Shopify ni Odoo.** Fecha: 2026-11-21. Esperando "aprobado".

## Resumen

| Concepto | Cantidad |
|---|---|
| Productos Prodigee activos en Shopify | 418 |
| Publicados en tienda en línea con descripción vacía o < 60 palabras (candidatas) | 94 |
| Propuestas redactadas | 64 (48 con inventario > 0) |
| SIN FUENTE (no se redactan) | 30 |
| Fase siguiente (sobre el tope de 120) | 0 |

Palabras por ficha: 90–119. Validado con `validar_prodigee.py`: HTML bien formado, plantilla (intro → Características 4–7 viñetas → Compatibilidad → cierre estándar), SEO title ≤ 60, meta ≤ 155, sin `Q`+dígitos. Títulos sin cambio.

**Fuente:** `prodigee.com/products.json` está bloqueado desde la nube (HTTP 441). Se usaron solo afirmaciones de fichas hermanas Prodigee ya publicadas en la tienda (misma línea; ids en `fuentes` de cada ficha). Donde la hermana es de otra generación de equipo no se trasladan datos sensibles (MagSafe, pies de caída); ver `dudas`.

Archivos: `prodigee_propuesta.json` (64), `prodigee_sin_fuente.json` (30), `prodigee_respaldo.json` (94: html + SEO actuales), `generar_prodigee.py`, `validar_prodigee.py`.

## Propuestas por línea

| Línea | Fichas | Hermana(s) fuente |
|---|---|---|
| neo | 11 | 9142004941013 Prodigee Safetee Neo iPhone 14 Plus Ruby; 9149922345173 Prodigee Safetee Neo iPhone 14 Plus Limón |
| superstar_old | 9 | 9149925949653 Prodigee Superstar iPhone 15/14/13 Clear; 9141946810581 Prodigee Superstar iPhone 17 Air Clear (cortes precisos) |
| superglass_cam | 7 | 9400708104405 Prodigee Super Glass Camera iPhone 17 Pro / Pro Max Orange; 9271505879253 Prodigee Super Glass Camera Galaxy S26 / S26 Plus; 9170874106069 descripción actual (protector de cámara, vidrio templado, fácil instalación) |
| safeteeflow | 6 | 9149922050261 Prodigee Safetee Flow iPhone 16 Night Frost; 9149921493205 Prodigee Safetee Flow iPhone 12 Pro Max Night; 9149921263829 Prodigee Safetee Flow Galaxy S25 Desert |
| magneteek | 3 | 9149920116949 Prodigee Magneteek iPhone 16 Pro Max Blanco; 9149920215253 Prodigee Magneteek iPhone 16E/15/14/13 Blanco |
| rockee | 3 | 9142022471893 Prodigee Rockee iPhone 13 Pro Rosado |
| kickit17 | 2 | 9141945204949 Prodigee Kickit iPhone 17 Air Negro; 9141945270485 Prodigee Kickit iPhone 17 Pro Clear; 9149960487125 descripción actual (stand, MagSafe, doble material) |
| jogger18 | 2 | 9391673966805 Prodigee Jogger iPhone 18 Pro Max/17 Pro Max Army; 9141944942805 Prodigee Jogger iPhone 17 Pro Midnight |
| flow17 | 2 | 9141943566549 Prodigee Flow iPhone 17 Blush Frost (hermana); 9141943501013 Prodigee Flow iPhone 17 Air Blush Frost; 9141943632085 Prodigee Flow iPhone 17 Desert |
| superstar_new | 2 | 9141946810581 Prodigee Superstar iPhone 17 Air Clear; 9391674261717 Prodigee Superstar iPhone 18 Pro Max/17 Pro Max Space |
| balance16 | 2 | 9142431482069 Prodigee Balance iPhone 16 Negro; 9142431613141 Prodigee Balance iPhone 16 Pro Negro |
| jogger_s26 | 2 | 9271505617109 descripción actual Jogger Galaxy S26 Ultra Midnight; 9271505518805 descripción actual Jogger Galaxy S26 Ultra Army; 9141944942805 Prodigee Jogger iPhone 17 Pro Midnight (línea) |
| smooth | 2 | 9142022570197 Prodigee Safetee Smooth iPhone 12 Pro Max Smoke |
| superhero | 1 | 9141946745045 Prodigee Super Hero iPhone 17 Smoke; 9141946319061 Prodigee Super Hero iPhone 17 Pro Clear |
| revolve | 1 | 9170873909461 Prodigee Revolve iPad 10TH Gen 10.9 Negro |
| balance_old | 1 | 9142431187157 Prodigee Balance iPhone 15 Pro Lavender; 9309628924117 descripción actual (grado militar, carga inalámbrica, pantalla 6.1) |
| pampas | 1 | 9149920739541 Prodigee Pampas iPhone 16 Pro Max Breeze; 9149920706773 Prodigee Pampas iPhone 16 Pro Ice |
| kickit_old | 1 | 9149918871765 Prodigee Kickit iPhone 16 Rosado; 9149918675157 Prodigee Kickit iPhone 15 Pro Rosado |
| kickit14plus | 1 | 9400707449045 Prodigee Kickit iPhone 14 Plus Negro; 9149918871765 Prodigee Kickit iPhone 16 Rosado |
| slim_galaxy | 1 | 9150255136981 Prodigee Safetee Slim Galaxy S20 Ultra Blanco |
| glow_galaxy | 1 | 9149916184789 Prodigee Glow Galaxy S23 Clear; 9149916250325 Prodigee Glow Galaxy S23 Plus Clear |
| formula_galaxy | 1 | 9149915693269 Prodigee Formula iPhone 16 Pro Max Gris; 9149915594965 Prodigee Formula iPhone 16 Gris |
| hero_iphone | 1 | 9149916971221 Prodigee Hero iPhone 15 Pro Clear; 9149917429973 Prodigee iPhone 16 Pro Hero Clear |
| hero_galaxy | 1 | 9149916840149 Prodigee Hero Galaxy S24 Clear; 9149916905685 Prodigee Hero Galaxy S24 Plus Clear |

## Todas las propuestas (orden por inventario)

| Inv. | Producto | SEO title | Dudas |
|---|---|---|---|
| 175 | Prodigee Kickit iPhone 17 Negro | Funda Prodigee KickIt iPhone 17 Negro | Ventas Guate | — |
| 138 | Prodigee Super Glass Camera iPhone 17 Negro | Prodigee Super Glass Camera iPhone 17 Negro | Color se refiere al aro del protector; verificar en foto. |
| 128 | Prodigee Superstar iPhone 16 Rosado | Funda Prodigee Superstar iPhone 16 Rosado | Ventas Guate | No se afirma MagSafe ni prueba de caídas: la única hermana iPhone 16 con ese dato (16 Pro Max Rosado) no está publicada. |
| 122 | Prodigee Superstar iPhone 16 Pro Rosado | Funda Prodigee Superstar iPhone 16 Pro Rosado | Ventas Guate | Igual que Superstar iPhone 16: sin MagSafe/caídas por falta de hermana publicada. |
| 107 | Prodigee Jogger iPhone 18 Pro Max/17 Pro Max Midnight New | Funda Prodigee Jogger iPhone 18 Pro Max/17 Pro Max Midnight | Título termina en 'New'; no se cambia en esta fase. |
| 101 | Prodigee Superstar iPhone 16 Clear | Funda Prodigee Superstar iPhone 16 Transparente | Sin MagSafe/caídas por falta de hermana publicada iPhone 16. |
| 96 | Prodigee Super Glass Camera iPhone 17 Air Black | Prodigee Super Glass Camera iPhone 17 Air Negro | Título dice 'Black'; se usó 'Negro'. Verificar color del aro en foto. |
| 94 | Prodigee Flow iPhone 17 Blush Frost | Funda Prodigee Flow iPhone 17 Blush Frost | Ventas Guate | — |
| 81 | Prodigee Super Glass Camera iPhone 17 Silver | Prodigee Super Glass Camera iPhone 17 Plateado | Título dice 'Silver'. |
| 80 | Prodigee Superstar iPhone 16 Pro Clear | Funda Prodigee Superstar iPhone 16 Pro Transparente | Sin MagSafe/caídas por falta de hermana publicada iPhone 16. |
| 78 | Prodigee Superstar iPhone 18/17 Pro Rain | Funda Prodigee Superstar iPhone 18 Pro/17 Pro Rain | Hermana publicada es la versión Pro Max (Space); mismas afirmaciones de línea. |
| 65 | Prodigee Kickit iPhone 17 Air Clear | Funda Prodigee KickIt iPhone 17 Air Transparente | — |
| 54 | Prodigee Safetee Neo Mag iPhone 13 Menta | Funda Prodigee Safetee Neo iPhone 13 Menta | Ventas Guate | Título dice 'Neo Mag': no se afirma MagSafe/imanes porque ninguna hermana Neo publicada lo indica. Confirmar con producto físico. |
| 48 | Prodigee Super Glass Camera iPhone 17 Air Glitter Silver | Prodigee Super Glass Camera iPhone 17 Air | — |
| 47 | Prodigee Superstar iPhone 16 Plus Rosado | Funda Prodigee Superstar iPhone 16 Plus Rosado | Sin MagSafe/caídas por falta de hermana publicada iPhone 16. |
| 47 | Prodigee Flow iPhone 17 Air Night Frost | Funda Prodigee Flow iPhone 17 Air Night Frost | Ventas Guate | — |
| 46 | Prodigee Jogger iPhone 18/17 Pro Burgundy | Funda Prodigee Jogger iPhone 18 Pro/17 Pro Burgundy | — |
| 45 | Prodigee Super Glass Camera iPhone 17 Air Silver | Prodigee Super Glass Camera iPhone 17 Air Plateado | Título dice 'Silver'. |
| 43 | Prodigee Super Glass Camera iPhone 17 Glitter Silver | Prodigee Super Glass Camera iPhone 17 Plateado con brillo | — |
| 42 | Prodigee Superstar iPhone 17 Air Space | Funda Prodigee Superstar iPhone 17 Air Space | Ventas Guate | Color 'Space' tal como en el título; verificar en foto si es negro/gris translúcido. |
| 36 | Prodigee Super Hero iPhone 16 Pro Clear | Funda Prodigee Super Hero iPhone 16 Pro Transparente | Hermanas Super Hero son iPhone 17; no se afirma MagSafe ni prueba de 10 ft para iPhone 16 Pro. |
| 26 | Prodigee Superstar iPhone 15 Pro Rosado | Funda Prodigee Superstar iPhone 15 Pro Rosado | Ventas Guate | — |
| 26 | Prodigee Safetee Neo iPhone 15/14/13 Lemon | Funda Prodigee Safetee Neo iPhone 15/14/13 Lemon | — |
| 25 | Prodigee Safetee Neo iPhone 13 Limón | Funda Prodigee Safetee Neo iPhone 13 Limón | Ventas Guate | — |
| 17 | Prodigee Safetee Flow iPhone 16 Pro Max Night Frost | Funda Prodigee Safetee Flow iPhone 16 Pro Max Night Frost | — |
| 15 | Prodigee Safetee Neo iPhone 15/14/13 Ruby | Funda Prodigee Safetee Neo iPhone 15/14/13 Ruby | — |
| 15 | Prodigee Magneteek iPhone 16 Pro Max Negro | Funda Prodigee Magneteek iPhone 16 Pro Max Negro | — |
| 13 | Prodigee Safetee Neo Mag iPhone 13 Pro Peach | Funda Prodigee Safetee Neo iPhone 13 Pro Peach | 'Neo Mag': no se afirma MagSafe sin fuente. |
| 12 | Prodigee Revolve iPad 11 Pro Negro | Funda Prodigee Revolve iPad 11 Pro Negro | Ventas Guate | Hermana es Revolve iPad 10.ª gen; mismas funciones de línea. Confirmar generación exacta del 'iPad 11 Pro' (y que tenga ranura para Apple Pencil) antes de publicar. |
| 11 | Prodigee Superstar iPhone 16 Plus Clear | Funda Prodigee Superstar iPhone 16 Plus Transparente | Sin MagSafe/caídas por falta de hermana publicada iPhone 16. |
| 10 | Prodigee Balance iPhone 16 Clear | Funda Prodigee Balance iPhone 16 Transparente | Ventas Guate | — |
| 5 | Prodigee Balance iPhone 15/14/13 Lavanda | Funda Prodigee Balance iPhone 15/14/13 Lavanda | Meta actual menciona precio de liquidación; la nueva no lleva precio. |
| 4 | Prodigee Superstar iPhone 15/14/13 Rosado | Funda Prodigee Superstar iPhone 15/14/13 Rosado | — |
| 3 | Prodigee Safetee Neo Mag iPhone 13 Peach | Funda Prodigee Safetee Neo iPhone 13 Peach | Ventas Guate | 'Neo Mag': no se afirma MagSafe sin fuente. |
| 3 | Prodigee Jogger Galaxy S26 Ultra Midnight | Funda Prodigee Jogger Galaxy S26 Ultra Midnight | 'Carga inalámbrica MagSafe' viene del texto actual del producto; Galaxy no usa MagSafe nativo, confirmar si trae imanes. |
| 2 | Prodigee Safetee Flow iPhone 11 Pro Passion | Funda Prodigee Safetee Flow iPhone 11 Pro Passion | — |
| 2 | Prodigee Safetee Neo Mag iPhone 13 Pro Menta | Funda Prodigee Safetee Neo iPhone 13 Pro Menta | 'Neo Mag': no se afirma MagSafe sin fuente. |
| 2 | Prodigee Safetee Smooth iPhone 12 Pro Max Gris | Funda Prodigee Safetee Smooth iPhone 12 Pro Max Gris | — |
| 1 | Prodigee Superstar iPhone 12 Pro Max Rosado | Funda Prodigee Superstar iPhone 12 Pro Max Rosado | — |
| 1 | Prodigee Safetee Flow Night 11 Pro | Funda Prodigee Safetee Flow iPhone 11 Pro Night | Título 'Prodigee Safetee Flow Night 11 Pro' no dice 'iPhone'; no se cambia el título. |
| 1 | Prodigee Safete Flow iPhone 12 Pro Max Passion | Funda Prodigee Safetee Flow iPhone 12 Pro Max Passion | Título con errata 'Safete'; no se cambia en esta fase. |
| 1 | Prodigee Safetee Neo iPhone 14 Pro Ruby | Funda Prodigee Safetee Neo iPhone 14 Pro Ruby | Ventas Guate | — |
| 1 | Prodigee Safetee Neo iPhone 14 Pro Limón | Funda Prodigee Safetee Neo iPhone 14 Pro Limón | — |
| 1 | Prodigee Rockee iPhone 12-12 Pro Menta | Funda Prodigee Rockee iPhone 12/12 Pro Menta | Ventas Guate | — |
| 1 | Prodigee Rockee iPhone 12-12 Pro Rosado | Funda Prodigee Rockee iPhone 12/12 Pro Rosado | Ventas Guate | — |
| 1 | Prodigee Rockee Series iPhone 13 Rosado | Funda Prodigee Rockee iPhone 13 Rosado | Ventas Guate | — |
| 1 | Prodigee Pampas iPhone 16 Pro Max Ice | Funda Prodigee Pampas iPhone 16 Pro Max Ice | Ventas Guate | — |
| 1 | Prodigee Jogger Galaxy S26 Ultra Army | Funda Prodigee Jogger Galaxy S26 Ultra Army | Ventas Guate | 'Carga inalámbrica MagSafe' viene del texto actual; confirmar si trae imanes. |
| 0 | Prodigee Kickit iPhone 15/14/13 Rosado | Funda Prodigee KickIt iPhone 15/14/13 Rosado | Ventas Guate | Sin hermana publicada 15/14/13; se usaron solo afirmaciones comunes de la línea KickIt (16 Rosado, 15 Pro Rosado). |
| 0 | Prodigee Kick It iPhone 14 Plus Rosado | Funda Prodigee KickIt iPhone 14 Plus Rosado | Ventas Guate | — |
| 0 | Prodigee Super Glass Camera iPhone 17 Pro/Pro Max Negro | Prodigee Super Glass Camera iPhone 17 Pro/17 Pro Max Negro | — |
| 0 | Prodigee Safetee Flow Galaxy S25 Ultra Night Frost | Funda Prodigee Safetee Flow Galaxy S25 Ultra Night Frost | Afirmación de 3 materiales viene de hermanas iPhone de la línea; la hermana Galaxy solo dice protección y bordes elevados. |
| 0 | Prodigee Safetee Flow Galaxy S25 Ultra Desert | Funda Prodigee Safetee Flow Galaxy S25 Ultra Desert | Afirmación de 3 materiales viene de hermanas iPhone de la línea. |
| 0 | Prodigee Safetee Neo iPhone 14 Pro Max Lila | Funda Prodigee Safetee Neo iPhone 14 Pro Max Lila | — |
| 0 | Prodigee Safetee Neo 14 Pro Max Ruby | Funda Prodigee Safetee Neo iPhone 14 Pro Max Ruby | Título no dice 'iPhone' ('Safetee Neo 14 Pro Max Ruby'); no se cambia. |
| 0 | Prodigee Safetee Smooth iPhone 14 Pro Negro | Funda Prodigee Safetee Smooth iPhone 14 Pro Negro | — |
| 0 | Prodigee Magneteek iPhone 14 Pro Max Negro | Funda Prodigee Magneteek iPhone 14 Pro Max Negro | — |
| 0 | Prodigee Magneteek iPhone 13 Pro Max Negro | Funda Prodigee Magneteek iPhone 13 Pro Max Negro | — |
| 0 | Prodigee Balance iPhone 16 Pro Max Negro | Funda Prodigee Balance iPhone 16 Pro Max Negro | — |
| 0 | Prodigee Safetee Slim Galaxy S22 Plus Negro | Funda Prodigee Safetee Slim Galaxy S22 Plus Negro | — |
| 0 | Prodigee Glow Galaxy S23 Ultra Clear | Funda Prodigee Glow Galaxy S23 Ultra Transparente | — |
| 0 | Prodigee Formula Galaxy S25 Ultra Gris | Funda Prodigee Formula Galaxy S25 Ultra Gris | Ventas Guate | Hermanas Formula son iPhone 16 con MagSafe; en Galaxy no se afirma MagSafe. |
| 0 | Prodigee Hero iPhone 14 Pro Clear | Funda Prodigee Hero iPhone 14 Pro Transparente | — |
| 0 | Prodigee Hero S24 Ultra Clear | Funda Prodigee Hero Galaxy S24 Ultra Transparente | Título dice 'Hero S24 Ultra' sin 'Galaxy'; no se cambia. |

## 5 ejemplos completos

### Prodigee Kickit iPhone 17 Negro (inv. 175, 102 palabras)

- **SEO title** (52): Funda Prodigee KickIt iPhone 17 Negro | Ventas Guate
- **Meta** (119): Funda Prodigee KickIt para iPhone 17 color Negro: soporte integrado, MagSafe y caídas de 1.8 m. Envío a toda Guatemala.
- **Fuentes:** Fichas hermanas publicadas en ventasguate.gt (ids Shopify): 9141945204949 Prodigee Kickit iPhone 17 Air Negro; 9141945270485 Prodigee Kickit iPhone 17 Pro Clear; 9149960487125 descripción actual (stand, MagSafe, doble material)
- **Dudas:** —

```html
<p>La funda Prodigee KickIt para iPhone 17 en color Negro tiene soporte integrado para ver videos y hacer videollamadas manos libres. Protege tu iPhone 17 sin descuidar su diseño.</p>
<h2>Características</h2>
<ul>
<li>Soporte integrado (kickstand) de aluminio para usar tu teléfono en horizontal.</li>
<li>Compatible con MagSafe y accesorios magnéticos.</li>
<li>Doble material: TPU flexible y policarbonato.</li>
<li>Protección contra caídas de hasta 6 ft (1.8 m).</li>
<li>Acabado soft-touch.</li>
<li>Cortes precisos para botones, puertos y cámaras.</li>
<li>Color: Negro.</li>
</ul>
<h2>Compatibilidad</h2>
<ul>
<li>iPhone 17</li>
</ul>
<p>Producto original con 1 año de garantía. Envío a toda Guatemala con pago contra entrega, o cómpralo en nuestra tienda en zona 13, Ciudad de Guatemala.</p>
```

### Prodigee Super Glass Camera iPhone 17 Negro (inv. 138, 109 palabras)

- **SEO title** (43): Prodigee Super Glass Camera iPhone 17 Negro
- **Meta** (148): Protector de cámara Prodigee Super Glass Camera para iPhone 17: cristal templado contra rayones y golpes, fácil instalación. Envío a toda Guatemala.
- **Fuentes:** Fichas hermanas publicadas en ventasguate.gt (ids Shopify): 9400708104405 Prodigee Super Glass Camera iPhone 17 Pro / Pro Max Orange; 9271505879253 Prodigee Super Glass Camera Galaxy S26 / S26 Plus; 9170874106069 descripción actual (protector de cámara, vidrio templado, fácil instalación)
- **Dudas:** Color se refiere al aro del protector; verificar en foto.

```html
<p>El Prodigee Super Glass Camera protege los lentes de la cámara trasera de tu iPhone 17 contra rayones, golpes y desgaste diario. Su cristal templado de alta resistencia cuida uno de los componentes más importantes de tu teléfono.</p>
<h2>Características</h2>
<ul>
<li>Cristal templado de alta resistencia.</li>
<li>Cubre los lentes de la cámara trasera.</li>
<li>Diseño delgado que no afecta la calidad de tus fotos y videos.</li>
<li>Fácil instalación con ajuste preciso al módulo de cámara.</li>
<li>Protección contra rayones, golpes y suciedad.</li>
<li>Color: Negro.</li>
</ul>
<h2>Compatibilidad</h2>
<ul>
<li>iPhone 17</li>
</ul>
<p>Producto original con 1 año de garantía. Envío a toda Guatemala con pago contra entrega, o cómpralo en nuestra tienda en zona 13, Ciudad de Guatemala.</p>
```

### Prodigee Superstar iPhone 16 Rosado (inv. 128, 105 palabras)

- **SEO title** (56): Funda Prodigee Superstar iPhone 16 Rosado | Ventas Guate
- **Meta** (125): Funda Prodigee Superstar para iPhone 16 color Rosado: TPU resistente, grip firme y acabado brillante. Envío a toda Guatemala.
- **Fuentes:** Fichas hermanas publicadas en ventasguate.gt (ids Shopify): 9149925949653 Prodigee Superstar iPhone 15/14/13 Clear; 9141946810581 Prodigee Superstar iPhone 17 Air Clear (cortes precisos)
- **Dudas:** No se afirma MagSafe ni prueba de caídas: la única hermana iPhone 16 con ese dato (16 Pro Max Rosado) no está publicada.

```html
<p>La funda Prodigee Superstar para iPhone 16 en color Rosado tiene un brillo sutil que resalta tu iPhone mientras lo protege en el día a día. Su grip evita que se te resbale de la mano.</p>
<h2>Características</h2>
<ul>
<li>Material TPU resistente.</li>
<li>Grip para un agarre firme sin que se resbale.</li>
<li>Destellos en la parte interna para un acabado brillante.</li>
<li>Bordes elevados en pantalla y cámara para mayor protección.</li>
<li>Cortes precisos para botones, puertos y cámaras.</li>
<li>Color: Rosado.</li>
</ul>
<h2>Compatibilidad</h2>
<ul>
<li>iPhone 16</li>
</ul>
<p>Producto original con 1 año de garantía. Envío a toda Guatemala con pago contra entrega, o cómpralo en nuestra tienda en zona 13, Ciudad de Guatemala.</p>
```

### Prodigee Jogger iPhone 18 Pro Max/17 Pro Max Midnight New (inv. 107, 110 palabras)

- **SEO title** (59): Funda Prodigee Jogger iPhone 18 Pro Max/17 Pro Max Midnight
- **Meta** (142): Funda Prodigee Jogger para iPhone 18 Pro Max/17 Pro Max color Midnight: agarre táctico, MagSafe y caídas de hasta 3 m. Envío a toda Guatemala.
- **Fuentes:** Fichas hermanas publicadas en ventasguate.gt (ids Shopify): 9391673966805 Prodigee Jogger iPhone 18 Pro Max/17 Pro Max Army; 9141944942805 Prodigee Jogger iPhone 17 Pro Midnight
- **Dudas:** Título termina en 'New'; no se cambia en esta fase.

```html
<p>La funda Prodigee Jogger para iPhone 18 Pro Max y 17 Pro Max en color Midnight es deportiva y resistente, con agarre táctico y acabado soft-touch. Ideal si buscas protección de alto rendimiento para el uso diario.</p>
<h2>Características</h2>
<ul>
<li>Material TPU flexible y policarbonato resistente.</li>
<li>Compatible con MagSafe gracias a sus imanes integrados.</li>
<li>Protección contra caídas de hasta 10 ft (3 m).</li>
<li>Acabado soft-touch.</li>
<li>Agarre táctico antideslizante.</li>
<li>Cortes precisos para botones, puertos y cámaras.</li>
<li>Color: Midnight.</li>
</ul>
<h2>Compatibilidad</h2>
<ul>
<li>iPhone 18 Pro Max</li>
<li>iPhone 17 Pro Max</li>
</ul>
<p>Producto original con 1 año de garantía. Envío a toda Guatemala con pago contra entrega, o cómpralo en nuestra tienda en zona 13, Ciudad de Guatemala.</p>
```

### Prodigee Safetee Neo Mag iPhone 13 Menta (inv. 54, 101 palabras)

- **SEO title** (57): Funda Prodigee Safetee Neo iPhone 13 Menta | Ventas Guate
- **Meta** (134): Funda Prodigee Safetee Neo para iPhone 13 color Menta: funda resistente con esquinas reforzadas contra caídas. Envío a toda Guatemala.
- **Fuentes:** Fichas hermanas publicadas en ventasguate.gt (ids Shopify): 9142004941013 Prodigee Safetee Neo iPhone 14 Plus Ruby; 9149922345173 Prodigee Safetee Neo iPhone 14 Plus Limón
- **Dudas:** Título dice 'Neo Mag': no se afirma MagSafe/imanes porque ninguna hermana Neo publicada lo indica. Confirmar con producto físico.

```html
<p>La funda Prodigee Safetee Neo para iPhone 13 en color Menta es una funda resistente con esquinas reforzadas que protegen tu teléfono de las caídas del día a día. Sus cortes precisos te dan acceso completo a botones, puertos y cámara, así que no tienes que quitarla para cargar o tomar fotos.</p>
<h2>Características</h2>
<ul>
<li>Esquinas reforzadas contra caídas.</li>
<li>Acceso completo a puertos y cámara.</li>
<li>Cortes precisos para botones, puertos y cámaras.</li>
<li>Color: Menta.</li>
</ul>
<h2>Compatibilidad</h2>
<ul>
<li>iPhone 13</li>
</ul>
<p>Producto original con 1 año de garantía. Envío a toda Guatemala con pago contra entrega, o cómpralo en nuestra tienda en zona 13, Ciudad de Guatemala.</p>
```

## SIN FUENTE (no se redactan)

| Inv. | Producto | Motivo |
|---|---|---|
| 86 | Prodigee Tile iPhone 18 Pro Max/17 Pro Max Iridescent | Tile iPhone 18/17 Pro Max: sin hermana Tile con descripción. |
| 54 | Prodigee Sparkle Leemonchelo iPhone 14 Pro Blanco | Sparkle Leemonchelo: no hay hermana publicada con descripción. |
| 21 | Prodigee Folio Mag Wallet iPhone 15 Pro Max Negro | Folio Mag Wallet: solo existe su propio texto corto (folio con tarjetas); sin hermana. |
| 19 | Prodigee PowerStrap 1FT Sand | PowerStrap 1FT: sin hermana con descripción. |
| 18 | Prodigee Sparkle Leemonchelo iPhone 14 Plus Blanco | Sparkle Leemonchelo: no hay hermana publicada con descripción. |
| 17 | Prodigee Billetera Universal Grande Negro | Billetera Universal: solo texto propio genérico (tamaño/color); sin especificaciones. |
| 17 | Prodigee PowerStrap 1FT Midnight | PowerStrap 1FT: sin hermana con descripción; no se inventan potencia ni conectores. |
| 16 | Prodigee Billetera Universal Extra Grande Negro | Billetera Universal: solo texto propio genérico (tamaño/color); sin especificaciones. |
| 15 | Prodigee Sidekick iPhone 15 Pro Max Negro | Sidekick: sin hermana con descripción. |
| 14 | Prodigee Strap & Go Cuerda Universal para Celular Negro | Strap & Go: sin hermana con descripción. |
| 12 | Prodigee Cross-It Strap Gris | Cross-It Strap: sin hermana con descripción. |
| 12 | Prodigee Cross-It Strap Sage | Cross-It Strap: sin hermana con descripción. |
| 11 | Prodigee PowerStrap 4FT Midnight | PowerStrap 4FT: sin hermana con descripción. |
| 10 | Prodigee Strap & Go Cuerda Universal para Celular Negro Dorado | Strap & Go: sin hermana con descripción. |
| 8 | Prodigee Cross-It Strap Negro | Cross-It Strap: sin hermana con descripción. |
| 4 | Prodigee Safetee Transforme iPhone 13 Negro | Safetee Transforme: solo 2 afirmaciones en su texto actual; sin hermana. |
| 2 | Prodigee Magwallet Ease Negro | Magwallet Ease: la hermana Magwallet Pop es otro modelo. |
| 1 | Prodigee Tesla Soporte Universal Mag Negro | Tesla Soporte Universal Mag: la única hermana (Tesla Soporte Universal para Carro) no está publicada y es otra versión. |
| 1 | Prodigee Energee to Go Powerbank Wireless 10000mAh | Energee to Go Powerbank Wireless 10000mAh: sin hermana; no se inventan potencias. |
| 1 | Prodigee Safetee Steel iPhone 13 Pro Max Blanco | Safetee Steel: sin hermana con descripción. |
| 1 | Prodigee Cubo de Carga Dual 20W Negro | Cubo de Carga Dual 20W: la hermana Ultra Slim 20W es de un puerto; no aplica. |
| 1 | Prodigee Handsfree Vent Negro | Handsfree Vent: la hermana Handsfree Magnet Pro es otro modelo y no está publicada. |
| 0 | Prodigee Sparkle Leemonchelo iPhone 14 Pro Max Blanco | Sparkle Leemonchelo: no hay hermana publicada con descripción. |
| 0 | Prodigee MagPower 2 Go MagSafe 10000 mAh Negro | MagPower 2 Go 10000 mAh: hermanas MagPower to-Go 10K se contradicen (USB-C 20 W vs 30 W); no se puede asegurar cuál es. |
| 0 | Prodigee MagPower to Go Powerbank 5mAh Negro | MagPower to Go 5mAh: capacidad del título ambigua (¿5,000 mAh / Slim 5K?); sin fuente segura. |
| 0 | Prodigee Safetee Steel iPhone 14 Pro Blanco | Safetee Steel: sin hermana con descripción. |
| 0 | Prodigee Safetee Steel iPhone 14 Pro Negro | Safetee Steel: sin hermana con descripción. |
| 0 | Prodigee Hands Free Soporte Universal Negro | Hands Free Soporte Universal (escritorio): sin hermana. |
| 0 | Prodigee Energee Magstand Base de Carga Inalámbrica Negro | Energee Magstand: sin hermana (Mag Station 2 en 1 es otro producto). |
| 0 | Prodigee the Sleeve Funda para MacBook Negro | The Sleeve funda MacBook: sin hermana; tamaño de MacBook no indicado. |

Para cerrarlas: conseguir ficha oficial (PDF/caja del proveedor, o prodigee.com desde una red no bloqueada) y redactar en una fase posterior.

## Para publicar (tras "aprobado")

1. Respaldo ya guardado en `prodigee_respaldo.json`.
2. Lotes de 8–10 con `productUpdate` (descriptionHtml + seo), contenido en `variables`.
3. Verificar 2–3 fichas y registrar lo aplicado en este README/registro.
