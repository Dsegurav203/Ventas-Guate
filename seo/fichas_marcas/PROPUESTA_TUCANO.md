# Propuesta · descripciones Tucano (ventasguate.gt)

**Estado: SOLO PROPUESTA (2026-11-21).** No se hizo ninguna mutación en Shopify ni escritura en Odoo. Publicar solo tras "aprobado" de Diego, siguiendo `.claude/skills/seo-ficha-producto/SKILL.md` (lotes de 8–10 con `productUpdate`, contenido en `variables`).

## Resumen

| Concepto | Cantidad |
|---|---|
| Fichas Tucano activas en Shopify | 83 |
| Publicadas en tienda online | 77 |
| Candidatas (publicadas, descripción vacía o < 60 palabras) | **73** |
| Con propuesta (fuente oficial verificada) | **45** (31 con inventario > 0) |
| SIN FUENTE (no se redacta) | **28** (11 con inventario > 0) |
| Excluidas por tener ya ≥ 60 palabras | 4 (Gommo City negra, Gommo Roll-Top 15.6" negra, Travel Adapter GaN 65W y 100W) |

**Fuente:** catálogo oficial Tucano en Shopify, `https://tucano.com/es-es/products/<handle>.json` (textos en español del fabricante) e `it-it` para códigos de barras (`www.tucano.com` redirige a `tucano.com`, que sí responde desde la nube). 20 propuestas con EAN `8020252…` coinciden exactamente con el código de barras oficial; las de UPC `844668…` (versión América) no están en el catálogo europeo y se emparejaron por **modelo + tamaño + color** (anotado en `dudas`).

**Formato:** `<p>` intro → `<h2>Características</h2>` 5–6 viñetas → `<h2>Compatibilidad</h2>` (si aplica) → cierre estándar. 90–122 palabras, "tú", sin precios ni promoción (la promo 50% no se menciona). Validado con Python: HTML bien formado, SEO title ≤ 60, meta ≤ 155, sin `Q`+dígito, sin "descuento/oferta/liquidación". Títulos sin cambio.

**Nota:** 11 de las fichas propuestas tienen hoy meta SEO con precios (`Q699`, `liquidación a Q165 (antes Q449)`, etc.); la propuesta los reemplaza. Fuera de la propuesta quedan con precio en la meta: Let Me Out Saddle Bag (SIN FUENTE) y Travel Adapter GaN 100W (`Q365`, excluida por longitud); conviene limpiar solo su meta.

## Propuestas (ordenadas por inventario)

| # | Producto | Inv. | Palabras | SEO title | Emparejamiento |
|---|---|---|---|---|---|
| 1 | Tucano Gommo Sleeve 16 Pulgadas Negro | 71 | 92 | Funda Tucano Gommo Sleeve 16" negro | Ventas Guate | EAN exacto |
| 2 | Tucano Isotta Superslim Bag 16 Pulgadas Negro | 47 | 90 | Maletín Tucano Isotta Superslim 16" negro | Ventas Guate | EAN exacto |
| 3 | Tucano Gommo Sleeve 16 Pulgadas Gris | 46 | 92 | Funda Tucano Gommo Sleeve 16" gris | Ventas Guate | EAN exacto |
| 4 | Tucano Gommo borsa superslim 16 Pulgadas Gris | 43 | 93 | Maletín Tucano Gommo Super Slim 16" gris | Ventas Guate | EAN exacto |
| 5 | Tucano Gommo Sleeve 13/14 Pulgadas Negro | 42 | 93 | Funda Tucano Gommo Sleeve 13"/14" negro | Ventas Guate | EAN exacto |
| 6 | Tucano Gommo Backpack Rolltop Blue | 40 | 100 | Mochila Tucano Gommo Roll-Top azul 15.6" | Ventas Guate | modelo+color |
| 7 | Tucano Universal Pencil Black | 36 | 114 | Lápiz Tucano Universal Pencil negro | Ventas Guate | modelo+color |
| 8 | Tucano Gommo Shoulder Bag Grey | 35 | 91 | Bandolera Tucano Gommo gris antirradiación | Ventas Guate | EAN exacto |
| 9 | Tucano Isotta Superslim Bag 16 Pulgadas Rosado | 31 | 90 | Maletín Tucano Isotta Superslim 16" rosado | Ventas Guate | EAN exacto |
| 10 | Tucano Gommo City Backpack Azul | 29 | 104 | Mochila Tucano Gommo City azul para laptop 15.6" | EAN exacto |
| 11 | Tucano Isotta Superslim Bag 13-14 Pulgadas Negro | 26 | 91 | Maletín Tucano Isotta Superslim 13"/14" negro | Ventas Guate | EAN exacto |
| 12 | Tucano Let Me Out Foldable Crossbody Azul | 25 | 95 | Bolso Tucano Let Me Out Crossbody azul | Ventas Guate | modelo+color |
| 13 | Tucano Let Me Out Foldable Crossbody Negro | 22 | 95 | Bolso Tucano Let Me Out Crossbody negro | Ventas Guate | modelo+color |
| 14 | Tucano Gommo City Backpack Gris | 21 | 104 | Mochila Tucano Gommo City gris para laptop 15.6" | EAN exacto |
| 15 | Tucano Isotta Superslim Bag 13"/14" Purple | 21 | 91 | Maletín Tucano Isotta Superslim 13"/14" morado | EAN exacto |
| 16 | Tucano Alunno iPad 10TH Gener Sky Blue | 20 | 109 | Funda Tucano Alunno iPad 10.ª gen celeste | Ventas Guate | modelo+color |
| 17 | Tucano Tasto iPad 10.9" a 11" Black | 20 | 121 | Funda Tucano Tasto teclado iPad 10.9" negra | Ventas Guate | modelo+color |
| 18 | Tucano Modo Premium Backpack 16 Pulgadas Negro | 18 | 113 | Mochila Tucano Modo Premium 16" negra | Ventas Guate | EAN exacto |
| 19 | Tucano Briefcase Modo Premium Black | 14 | 111 | Maletín Tucano Modo Premium negro 15.6" | Ventas Guate | EAN exacto |
| 20 | Tucano Neoprene Desk Pad Pink | 14 | 99 | Desk pad Tucano de neopreno rosado | Ventas Guate | EAN exacto |
| 21 | Tucano Gommo Shopper Bag Azul | 13 | 95 | Bolso Tucano Gommo Shopper azul para laptop 14" | EAN exacto |
| 22 | Tucano Isotta Superslim Bag 13-14 Pulgadas Rosado | 13 | 91 | Maletín Tucano Isotta Superslim 13"/14" rosado | EAN exacto |
| 23 | Tucano Gommo Shopper Bag Negro | 11 | 95 | Bolso Tucano Gommo Shopper negro para laptop 14" | EAN exacto |
| 24 | Tucano Neoprene Desk Pad Blue | 11 | 99 | Desk pad Tucano de neopreno azul | Ventas Guate | EAN exacto |
| 25 | Tucano Mini Support Stand | 11 | 101 | Soporte Tucano Mini Support Stand para laptop | Ventas Guate | modelo+color |
| 26 | Tucano Modo Premium Backpack 14" Black | 9 | 113 | Mochila Tucano Modo Premium 14" negra | Ventas Guate | modelo+color |
| 27 | Tucano Facile Plus Universal para Tablet 11 Pulgadas Rojo | 9 | 101 | Funda Tucano Facile Plus tablet 11" rojo | Ventas Guate | modelo+color |
| 28 | Tucano Gommo borsa superslim 13"/14" Gris | 8 | 94 | Maletín Tucano Gommo Super Slim 13"/14" gris | Ventas Guate | EAN exacto |
| 29 | Tucano Let Me Out Shopper Bag Blue | 2 | 95 | Bolso Tucano Let Me Out Shopper azul | Ventas Guate | modelo+color |
| 30 | Tucano Let Me Out Foldable Crossbody Verde | 1 | 95 | Bolso Tucano Let Me Out Crossbody verde | Ventas Guate | modelo+color |
| 31 | Tucano Alunno para iPad 10MA Generación Amarillo | 1 | 109 | Funda Tucano Alunno iPad 10.ª gen amarillo | Ventas Guate | modelo+color |
| 32 | Tucano Modo Premium Backpack 14 Pulgadas Negro | 0 | 113 | Mochila Tucano Modo Premium 14" negra | Ventas Guate | EAN exacto |
| 33 | Tucano Active Pencil2 para iPad Blanco | 0 | 107 | Lápiz Tucano Active Pencil 2 para iPad blanco | Ventas Guate | modelo+color |
| 34 | Tucano Facile Plus Universal para Tablet 11 Pulgadas Negro | 0 | 101 | Funda Tucano Facile Plus tablet 11" negro | Ventas Guate | modelo+color |
| 35 | Tucano Alunno iPad Case 10TH Black | 0 | 109 | Funda Tucano Alunno iPad 10.ª gen negro | Ventas Guate | modelo+color |
| 36 | Tucano Gancio Case W/Keyboard Universal 11" Azul | 0 | 92 | Funda Tucano Gancio con teclado tablet 11" azul | modelo+color |
| 37 | Tucano Binario Backpack 15.6" W/Ags Blue | 0 | 122 | Mochila Tucano Binario AGS azul 15.6" | Ventas Guate | modelo+color |
| 38 | Tucano Lato2 Backpack 13.3/14" Black | 0 | 111 | Mochila Tucano Lato 2 14" negra | Ventas Guate | modelo+color |
| 39 | Tucano Lato2 Backpack 13.3/14" Blue | 0 | 111 | Mochila Tucano Lato 2 14" azul | Ventas Guate | modelo+color |
| 40 | Tucano Funda Offroad para Laptop 15.6'' Negro | 0 | 93 | Funda Tucano Offroad 15.6" negra | Ventas Guate | modelo+color |
| 41 | Tucano Mochila Ted 14'' Verde | 0 | 91 | Mochila Tucano Ted 14" verde | Ventas Guate | modelo+color |
| 42 | Tucano Smilza Superslim Funda para Computadora 14 Pulgadas Azul | 0 | 95 | Maletín Tucano Smilza Superslim 14" azul | Ventas Guate | modelo+color |
| 43 | Tucano Smilza Superslim Funda para Computadora 14 Pulgadas Negra | 0 | 95 | Maletín Tucano Smilza Superslim 14" negra | Ventas Guate | modelo+color |
| 44 | Tucano Workout 4 Mochila para Computador 14 Pulgadas Azul | 0 | 113 | Mochila Tucano Work Out 4 14" azul | Ventas Guate | modelo+color |
| 45 | Tucano Workout 4 Mochila para Computador 14 Pulgadas Negro | 0 | 113 | Mochila Tucano Work Out 4 14" negra | Ventas Guate | modelo+color |

## 5 ejemplos

### Tucano Gommo Sleeve 16 Pulgadas Negro (inv. 71)

- **SEO title** (50): Funda Tucano Gommo Sleeve 16" negro | Ventas Guate
- **Meta** (150): Funda Tucano Gommo Sleeve negro para laptops de 15.6" y MacBook Pro de 16": material engomado impermeable y bolsillo exterior. Envío a toda Guatemala.
- **Fuente:** https://tucano.com/es-es/products/bfgom1516

```html
<p>La funda Tucano Gommo Sleeve 16" negro protege tu laptop con un material engomado impermeable y un diseño limpio. Ideal para meterla en tu mochila o llevarla sola a reuniones y clases.</p>
<h2>Características</h2>
<ul>
<li>Material engomado impermeable.</li>
<li>Compartimento acolchado exclusivo para el equipo.</li>
<li>Orejetas antideslizantes en las esquinas para sujetar la laptop.</li>
<li>Bolsillo exterior práctico para accesorios.</li>
<li>Color: negro.</li>
</ul>
<h2>Compatibilidad</h2>
<ul>
<li>Laptops de 15.6"</li>
<li>MacBook Pro de 16"</li>
</ul>
<p>Producto original con 1 año de garantía. Envío a toda Guatemala con pago contra entrega, o cómpralo en nuestra tienda en zona 13, Ciudad de Guatemala.</p>
```

### Tucano Isotta Superslim Bag 16 Pulgadas Negro (inv. 47)

- **SEO title** (56): Maletín Tucano Isotta Superslim 16" negro | Ventas Guate
- **Meta** (136): Maletín slim Tucano Isotta negro de PU efecto piel para laptops de 15.6" y MacBook Pro de 16", con bolsillo exterior y correa removible.
- **Fuente:** https://tucano.com/es-es/products/bsiso1516

```html
<p>El maletín Tucano Isotta Superslim 16" negro es un bolso delgado de PU suave con efecto piel. Lleva tu laptop con elegancia en la mano o al hombro, sin bultos.</p>
<h2>Características</h2>
<ul>
<li>PU suave con efecto piel.</li>
<li>Diseño delgado (slim).</li>
<li>Compartimento interno único para la laptop.</li>
<li>Bolsillo exterior para accesorios.</li>
<li>Correa para el hombro removible.</li>
<li>Color: negro.</li>
</ul>
<h2>Compatibilidad</h2>
<ul>
<li>Laptops de 15.6"</li>
<li>MacBook Pro de 16"</li>
</ul>
<p>Producto original con 1 año de garantía. Envío a toda Guatemala con pago contra entrega, o cómpralo en nuestra tienda en zona 13, Ciudad de Guatemala.</p>
```

### Tucano Gommo Sleeve 16 Pulgadas Gris (inv. 46)

- **SEO title** (49): Funda Tucano Gommo Sleeve 16" gris | Ventas Guate
- **Meta** (149): Funda Tucano Gommo Sleeve gris para laptops de 15.6" y MacBook Pro de 16": material engomado impermeable y bolsillo exterior. Envío a toda Guatemala.
- **Fuente:** https://tucano.com/es-es/products/bfgom1516

```html
<p>La funda Tucano Gommo Sleeve 16" gris protege tu laptop con un material engomado impermeable y un diseño limpio. Ideal para meterla en tu mochila o llevarla sola a reuniones y clases.</p>
<h2>Características</h2>
<ul>
<li>Material engomado impermeable.</li>
<li>Compartimento acolchado exclusivo para el equipo.</li>
<li>Orejetas antideslizantes en las esquinas para sujetar la laptop.</li>
<li>Bolsillo exterior práctico para accesorios.</li>
<li>Color: gris.</li>
</ul>
<h2>Compatibilidad</h2>
<ul>
<li>Laptops de 15.6"</li>
<li>MacBook Pro de 16"</li>
</ul>
<p>Producto original con 1 año de garantía. Envío a toda Guatemala con pago contra entrega, o cómpralo en nuestra tienda en zona 13, Ciudad de Guatemala.</p>
```

### Tucano Gommo borsa superslim 16 Pulgadas Gris (inv. 43)

- **SEO title** (55): Maletín Tucano Gommo Super Slim 16" gris | Ventas Guate
- **Meta** (146): Maletín slim Tucano Gommo gris para laptops de 15.6" y MacBook Pro de 16": material engomado impermeable y correa desmontable. Envío en Guatemala.
- **Fuente:** https://tucano.com/es-es/products/bsgom1314

```html
<p>El maletín Tucano Gommo Super Slim 16" gris es un portalaptop superdelgado de material engomado impermeable. Protege tu equipo sin agregar volumen y lo llevas en la mano o al hombro.</p>
<h2>Características</h2>
<ul>
<li>Material engomado impermeable.</li>
<li>Compartimento único acolchado.</li>
<li>Orejetas antideslizantes en las esquinas para sujetar el equipo.</li>
<li>Bolsillo exterior práctico para accesorios.</li>
<li>Correa para el hombro desmontable.</li>
<li>Color: gris.</li>
</ul>
<h2>Compatibilidad</h2>
<ul>
<li>Laptops de 15.6"</li>
<li>MacBook Pro de 16"</li>
</ul>
<p>Producto original con 1 año de garantía. Envío a toda Guatemala con pago contra entrega, o cómpralo en nuestra tienda en zona 13, Ciudad de Guatemala.</p>
```

### Tucano Gommo Sleeve 13/14 Pulgadas Negro (inv. 42)

- **SEO title** (54): Funda Tucano Gommo Sleeve 13"/14" negro | Ventas Guate
- **Meta** (154): Funda Tucano Gommo Sleeve negro para laptops de hasta 14" y MacBook Air de 15": material engomado impermeable y bolsillo exterior. Envío a toda Guatemala.
- **Fuente:** https://tucano.com/es-es/products/bfgom1516

```html
<p>La funda Tucano Gommo Sleeve 13"/14" negro protege tu laptop con un material engomado impermeable y un diseño limpio. Ideal para meterla en tu mochila o llevarla sola a reuniones y clases.</p>
<h2>Características</h2>
<ul>
<li>Material engomado impermeable.</li>
<li>Compartimento acolchado exclusivo para el equipo.</li>
<li>Orejetas antideslizantes en las esquinas para sujetar la laptop.</li>
<li>Bolsillo exterior práctico para accesorios.</li>
<li>Color: negro.</li>
</ul>
<h2>Compatibilidad</h2>
<ul>
<li>Laptops de hasta 14"</li>
<li>MacBook Air de 15"</li>
</ul>
<p>Producto original con 1 año de garantía. Envío a toda Guatemala con pago contra entrega, o cómpralo en nuestra tienda en zona 13, Ciudad de Guatemala.</p>
```

## Dudas a revisar antes de aprobar

- **Tucano Gommo Backpack Rolltop Blue**: UPC 844668134871 (versión América) no está en el catálogo europeo; emparejado por modelo/color con BKGOMRT15-B y con la ficha hermana negra ya publicada.
- **Tucano Universal Pencil Black**: SKU de Shopify con prefijo "L" (L844668125183); UPC no está en el catálogo europeo, emparejado por modelo (MA-USTY-BK).
- **Tucano Let Me Out Foldable Crossbody Azul**: El catálogo europeo solo lista el color verde militar (BLMOCB-VM); el modelo es el mismo, el color se toma del título.
- **Tucano Let Me Out Foldable Crossbody Negro**: El catálogo europeo solo lista el color verde militar (BLMOCB-VM); el modelo es el mismo, el color se toma del título.
- **Tucano Alunno iPad 10TH Gener Sky Blue**: UPC 844668124049 no está en el catálogo europeo; emparejado por modelo y color (Azzurro / IPD1022AL-Z). La descripción oficial en línea es de la versión iPad 10.2"; se asumen las mismas características para la versión iPad 10.
- **Tucano Tasto iPad 10.9" a 11" Black**: Fuente oficial = versión con teclado italiano (IPD109TAS-TK-IT); no se menciona la distribución del teclado. El título dice "10.9 a 11": el fabricante solo confirma iPad Air 10.9". Revisar empaque antes de publicar.
- **Tucano Mini Support Stand**: UPC 844668114002 no está en el catálogo europeo; emparejado por modelo ("Mini Stand per laptop", MA-MINIST). Confirmar con la foto que son los dos soportes adhesivos de aluminio.
- **Tucano Modo Premium Backpack 14" Black**: Ficha duplicada de la Modo Premium 14" negra (otra ficha con EAN 8020252194557). Emparejada por modelo; confirmar que es la misma versión.
- **Tucano Facile Plus Universal para Tablet 11 Pulgadas Rojo**: UPC 844668068985 no está en el catálogo europeo; emparejado por modelo y tamaño (TAB-FAP10, tabletas de hasta 11").
- **Tucano Let Me Out Shopper Bag Blue**: UPC 844668105987 no está en el catálogo europeo; emparejado por modelo y color (BLMOSH-B, azul).
- **Tucano Let Me Out Foldable Crossbody Verde**: El catálogo europeo solo lista el color verde militar (BLMOCB-VM); el modelo es el mismo, el color se toma del título.
- **Tucano Alunno para iPad 10MA Generación Amarillo**: UPC 844668124063 no está en el catálogo europeo; emparejado por modelo y color (Giallo / IPD1022AL-Y). La descripción oficial en línea es de la versión iPad 10.2"; se asumen las mismas características para la versión iPad 10.
- **Tucano Active Pencil2 para iPad Blanco**: UPC 844668135793 no está en el catálogo europeo; emparejado por modelo/color con "Tucano Pencil 2" blanco (MA-STY2-W). Verificar la compatibilidad exacta con el modelo de iPad del cliente.
- **Tucano Facile Plus Universal para Tablet 11 Pulgadas Negro**: UPC 844668068961 no está en el catálogo europeo; emparejado por modelo y tamaño (TAB-FAP10, tabletas de hasta 11").
- **Tucano Alunno iPad Case 10TH Black**: UPC 844668124025 no está en el catálogo europeo; emparejado por modelo y color (Nero / IPD1022AL-BK). La descripción oficial en línea es de la versión iPad 10.2"; se asumen las mismas características para la versión iPad 10.
- **Tucano Gancio Case W/Keyboard Universal 11" Azul**: UPC 844668096056 no está en el catálogo europeo; emparejado por modelo y color (TAB-GA10, azul, tabletas de hasta 11"). La fuente es la versión con teclado italiano: no se menciona distribución del teclado.
- **Tucano Binario Backpack 15.6" W/Ags Blue**: UPC 844668119342 no está en el catálogo europeo; emparejado por modelo y color (Binario Gravity AGS, blu scuro).
- **Tucano Lato2 Backpack 13.3/14" Black**: UPC 844668097213 no está en el catálogo europeo; emparejado por modelo y color (BKLT14).
- **Tucano Lato2 Backpack 13.3/14" Blue**: UPC 844668095486 no está en el catálogo europeo; emparejado por modelo y color (BKLT14).
- **Tucano Funda Offroad para Laptop 15.6'' Negro**: UPC 844668117652 no está en el catálogo europeo; emparejado por modelo, tamaño y color (BFCAR1516-BK).
- **Tucano Mochila Ted 14'' Verde**: UPC 844668112305 no está en el catálogo europeo; emparejado por modelo (BKTED1314); el fabricante lista "verde militare".
- **Tucano Smilza Superslim Funda para Computadora 14 Pulgadas Azul**: UPC 844668076621 no está en el catálogo europeo; emparejado por modelo, tamaño y color (BSM1314).
- **Tucano Smilza Superslim Funda para Computadora 14 Pulgadas Negra**: UPC 844668076645 no está en el catálogo europeo; emparejado por modelo, tamaño y color (BSM1314).
- **Tucano Workout 4 Mochila para Computador 14 Pulgadas Azul**: UPC 844668119601 no está en el catálogo europeo; emparejado por modelo y color (WO4BK-MB14-B).
- **Tucano Workout 4 Mochila para Computador 14 Pulgadas Negro**: UPC 844668119588 no está en el catálogo europeo; emparejado por modelo y color (WO4BK-MB14-AX (antracita)). El fabricante lo llama antracita, el título dice negro.

## SIN FUENTE (no se redactó)

| Producto | Inv. | SKU | Motivo |
|---|---|---|---|
| Tucano Let Me Out Backpack Black | 35 | 844668105963 | Let Me Out Backpack: tucano.com solo tiene Let Me Out Shopper y Crossbody. |
| Tucano Scrivo Keyboard Spanish Blue | 28 | 844668127101 | Scrivo Keyboard: modelo no aparece en tucano.com. |
| Tucano Let Me Out Foldable Backpack Negro | 14 | 844668105901 | Let Me Out Foldable Backpack: sin ficha oficial. |
| Tucano Let Me Out Foldable Saddle Bag Negro | 7 | 844668106083 | Let Me Out Saddle Bag: sin ficha oficial (texto actual menciona "resistente al agua" sin fuente; SEO actual contiene precios). |
| Tucano Tasto iPad 10TH Black | 6 | 844668125046 | Tasto iPad 10.ª gen: el catálogo oficial solo tiene Tasto para iPad Air 10.9" (teclado italiano); no se confirma la versión iPad 10. |
| Tucano Vento Case Universal para Tablet 9 a 10 Pulgadas Azul | 6 | 844668051772 | Vento: modelo no aparece en tucano.com (it/es/en). |
| Tucano Let Me Out Foldable Duffle Negro | 5 | 844668106021 | Let Me Out Duffle: sin ficha oficial. |
| Tucano Let Me Out Foldable Backpack Azul | 3 | 844668105925 | Let Me Out Foldable Backpack: sin ficha oficial. |
| Tucano Let Me Out Weekender Bag Blue | 1 | 844668106045 | Let Me Out Weekender: sin ficha oficial. |
| Tucano Scrivo Teclado Bluetooth con Stand Azul | 1 | 844668096278 | Scrivo con stand: modelo no aparece en tucano.com. |
| Tucano Active Pencil Stylus | 1 | 844668121192 | Active Pencil Stylus (UPC 844668121192): no se puede asociar con seguridad a Pencil 2/3 ni Universal Pencil. |
| Tucano Funda iPad 10.2 / 10.5 Rosado | 0 | 844668102900 | Funda iPad 10.2/10.5 rosado: no se identifica el modelo (no dice cuál). |
| Tucano Mouse Inalámbrico Ergonómico Negro | 0 | 844668133591 | Mouse ergonómico: el único ergonómico oficial es vertical (MA-WMV); el título no lo confirma. |
| Tucano Binario Backpack 15.6l Anthracite Negro | 0 | 844668116891 | Binario 15.6 antracita sin "AGS" en el título: la ficha oficial es Binario Gravity AGS; podría ser otra versión. |
| Tucano Ergonomic Lumbar Cushion | 0 | 844668115979 | Cojín lumbar ergonómico: no aparece en tucano.com. |
| Tucano Goal Backpack 15.6 Brown | 0 | 844668116693 | Goal: el oficial es para 13"/14" pero el título dice 15.6"; conflicto de tamaño. |
| Tucano Goal Backpack 15.6 Gray | 0 | 844668116952 | Goal: el oficial es para 13"/14" pero el título dice 15.6"; conflicto de tamaño. |
| Tucano Let Me Out Foldable Duffle Verde | 0 | 844668106656 | Let Me Out Duffle verde: sin ficha oficial. |
| Tucano Let Me Out Mochila | 0 | 844668106618 | Let Me Out Mochila: sin ficha oficial. |
| Tucano Mouse Inalámbrico Negro | 0 | 844668127163 | Mouse inalámbrico: modelo no identificado en tucano.com. |
| Tucano Soft Troelly Mochila Negra | 0 | 844668132051 | Soft Trolley mochila: modelo no identificado en tucano.com. |
| Tucano Top Slevee Mbp 13" Petroleum Blue | 0 | 844668067377 | Top Sleeve MBP 13" Petroleum Blue: la línea Top actual no tiene 13" en ese color; versión descontinuada. |
| Tucano Tugo M Cabin Luggage 15.6" PC Black | 0 | 844668023106 | Tugò M Cabin 15.6" (UPC antiguo 844668023106): la ficha actual Tugò M es de una generación más nueva; no se garantiza que coincidan. |
| Tucano Unico Case Universal para Tablet 11 Pulgadas Negro | 0 | 844668096414 | Unico: modelo no aparece en tucano.com. |
| Tucano Universo Case Universal para Tablet Samsung 10.5 Pulgadas Amarillo | 0 | 844668115177 | Universo: modelo no aparece en tucano.com. |
| Tucano Universo Case Universal para Tablet Samsung 10.5 Pulgadas Negro | 0 | 844668115139 | Universo: modelo no aparece en tucano.com. |
| Tucano Vento Case Universal para Tablet 11 Pulgadas Negro | 0 | 844668051758 | Vento: modelo no aparece en tucano.com. |
| Tucano Workout 4 Mochila para Computador 16 Pulgadas Negro | 0 | 844668119564 | Work Out 4 mochila 16": el oficial solo tiene mochila 13"/14" y funda (sleeve) 16". |

Opciones para SIN FUENTE: pedir ficha técnica a Tucano América / distribuidor (UPC 844668…), o despublicar las que están en 0 y descontinuadas.

## Archivos
- `tucano_propuesta.json`: `{id, title, inventario, html, seo_title, seo_description, fuentes, dudas}` (45).
- `tucano_respaldo.json`: `descriptionHtml` y `seo` actuales de las 73 candidatas (leído 2026-11-21; volver a leer justo antes de publicar).
