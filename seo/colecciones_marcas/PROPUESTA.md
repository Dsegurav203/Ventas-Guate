# Colecciones de marca: LAUT, Sudio, OhSnap, Mello, Reelcharge

Propuesta del 2026-11-21. **Solo propuesta: no se ha escrito nada en Shopify.** Datos leídos de Shopify ese día.

| Marca | Acción | Handle | Publicados (activos en tienda en línea) | Con stock | SEO title | Meta | Palabras |
|---|---|---|---|---|---|---|---|
| LAUT | crear | laut | 19 | 19 | 53 | 141 | 184 |
| Sudio | no_crear | sudio | 0 | 0 | – | – | – |
| OhSnap | actualizar | ohsnap | 15 | 11 | 57 | 143 | 157 |
| Mello | crear | mello | 14 | 14 | 59 | 137 | 152 |
| Reelcharge | crear | reelcharge | 8 | 8 | 60 | 148 | 158 |

## Hallazgos

- **Vendor inconsistente**: solo LAUT (11 de 19) y OhSnap usan el vendor de la marca. Mello está como `MELLO DISTRIBUTION`; Reelcharge y 8 LAUT como `Ventas Guate`. Una condición solo `vendor = <Marca>` dejaría Reelcharge vacía y LAUT incompleta. Por eso cada colección nueva usa **ANY**: vendor EQUALS la marca (y variantes) **o** título STARTS_WITH la marca. Alternativa más limpia: normalizar el vendor de esos productos (ver `seo/vendor_a_marca.csv`) y dejar solo la regla de vendor.
- **OhSnap** existe pero `ventasguate.gt/collections/ohsnap` da 404: no está publicada en la tienda en línea. Hay que publicarla (`publishablePublish`) además de actualizar el texto. El texto actual menciona el control MCON, que no está publicado.
- `collectionCreate` crea las colecciones **sin publicar**: después de crearlas, `publishablePublish` en la tienda en línea.
- **Sudio**: 0 productos en Shopify y en Odoo → no crear.

## Mutación propuesta (no ejecutada)

```graphql
mutation($c: CollectionCreateInput!){ collectionCreate(collection:$c){ collection{ id handle } userErrors{ field message } } }
# variables c = {title, handle, descriptionHtml, seo:{title, description}, sortOrder: BEST_SELLING,
#   sources:[{source:{title:"Marca", targetType: PRODUCTS, inclusion: <condicion de propuesta.json>}}]}
# OhSnap: collectionUpdate(collection:{id, descriptionHtml, seo}) + publishablePublish
```

## LAUT (crear)

- **Handle**: `laut` · **Título visible**: LAUT
- **SEO title** (53): LAUT Guatemala: fundas, iPad y AirPods | Ventas Guate
- **Meta** (141): Accesorios LAUT originales en Guatemala: fundas iPhone 17 Pro y Pro Max, teclados y folios para iPad, estuches AirPods. Envío a todo el país.
- **Condición**: `{"matchType": "ANY", "conditions": [{"productVendor": {"matchType": "ANY", "relation": "EQUALS", "values": ["LAUT"]}}, {"productTitle": {"matchType": "ANY", "relation": "STARTS_WITH", "values": ["LAUT"]}}]}`
- **Enlaces** (verificados, responden 200): /collections/17-pro-max, /collections/iphone-17-pro, /collections/ipads
- **Notas**: 11 productos con vendor LAUT + 8 con vendor 'Ventas Guate' (Huex MacBook Air 13.6 Negro, Huex Protect AirPods Pro3 Light Pink, Luxedge 17 Pro x2, Huex Protect AirPods 4, Zentry AirPods 4, Typefolio 2.0 iPad 11 y Pro 11). Por eso la condición agrega 'título empieza con LAUT'. Activos con stock pero sin publicar en tienda en línea: Huex MacBook Neo 13 Pink/Yellow, Links 2.0 Apple Watch Silver, Huex Protect MacBook Air 13 Black.

```html
<p>Encuentra accesorios <strong>LAUT Guatemala</strong> originales: fundas para iPhone 17 Pro y 17 Pro Max, teclados y folios para iPad, estuches para AirPods y protectores para MacBook Air.</p>
<h2>Fundas para iPhone</h2>
<p>Crystal Matter X y Luxedge para iPhone 17 Pro Max, y Luxedge para iPhone 17 Pro. Mira más opciones en <a href="/collections/17-pro-max">fundas iPhone 17 Pro Max</a> y <a href="/collections/iphone-17-pro">fundas iPhone 17 Pro</a>.</p>
<h2>iPad y MacBook</h2>
<p>Teclados Typefolio 2.0 para iPad 10.9", iPad 11" e iPad Pro 11" (M4), Typefolio y Prestige Folio universales de 9 a 11 pulgadas, Prestige Folio Mg para iPad Air 13", Little Buddy para iPad 10.9" y Huex para MacBook Air 13.6". Ver <a href="/collections/ipads">accesorios para iPad</a>.</p>
<h2>AirPods</h2>
<p>Estuches Huex Protect y Zentry para AirPods Pro 3 y AirPods 4.</p>
<h2>Preguntas frecuentes</h2>
<p><strong>¿Los productos LAUT son originales?</strong><br>Sí. LAUT es una de las marcas oficiales que distribuimos en Guatemala.</p>
<p><strong>¿Tienen garantía?</strong><br>Sí, 1 año por defectos de fabricación.</p>
<p><strong>¿Hacen envíos?</strong><br>Sí, a toda Guatemala con pago contra entrega: Ciudad de Guatemala el mismo día e interior al día siguiente. También puedes comprar en nuestra tienda en zona 13, Ciudad de Guatemala.</p>
```

## Sudio (no_crear)

No hay ningún producto Sudio en Shopify (ni por vendor ni por título) ni en Odoo (product.template por nombre o brand_id). Crear la colección cuando haya al menos 4 productos publicados.

## OhSnap (actualizar)

- **Handle**: `ohsnap` · **Título visible**: OhSnap
- **SEO title** (57): OhSnap Guatemala: grips MagSafe y soportes | Ventas Guate
- **Meta** (143): Grips, billeteras y soportes MagSafe OhSnap originales en Guatemala: Snap Grip, Grip Stand, Grip Wallet y Snap Car Mount. Envío a todo el país.
- **Condición**: `{"actual": "Etiqueta = OhSnap (TAGGED_WITH) + 15 selecciones manuales; se mantiene. Opcional: agregar 'título empieza con OhSnap' para incluir Snap Grip Wine Noir y MCON cuando se publiquen."}`
- **Enlaces** (verificados, responden 200): /collections/magsafe, /collections/auto
- **Notas**: La colección existe pero responde 404 en ventasguate.gt/collections/ohsnap: no está publicada en la tienda en línea (publicar con publishablePublish). El texto actual menciona el control MCON, que no está publicado (activo con 48 unidades, sin canal tienda en línea, vendor 'Ventas Guate'); igual 'Ohsnap Snap Grip Wine Noir' (21 u.). Sin stock: Snap Grip Blazed Sunset, Gator Fade, Orchid Slap y Pick Me Pink.

```html
<p>Accesorios magnéticos <strong>OhSnap Guatemala</strong> originales para tu teléfono: grips, billeteras con grip y soporte, y soporte para carro, todos compatibles con MagSafe.</p>
<h2>Snap Grip y Grip Stand</h2>
<p>El Snap Grip MagSafe viene en varios colores y diseños, como Black, Rose, Insomnia Blue, Retro Wave y Silver Fox. El Grip Stand agrega soporte vertical, en Black y Overexposed.</p>
<h2>Grip Wallet y Snap Car Mount</h2>
<p>Grip Wallet es billetera con grip y soporte (Black, Cranberry Smash y Orchid Slap). Snap Car Mount es el soporte magnético para carro. Mira más en <a href="/collections/magsafe">accesorios MagSafe</a> y <a href="/collections/auto">accesorios para carro</a>.</p>
<h2>Preguntas frecuentes</h2>
<p><strong>¿Los productos OhSnap son originales?</strong><br>Sí. OhSnap es una de las marcas oficiales que distribuimos en Guatemala.</p>
<p><strong>¿Tienen garantía?</strong><br>Sí, 1 año por defectos de fabricación.</p>
<p><strong>¿Hacen envíos?</strong><br>Sí, a toda Guatemala con pago contra entrega: Ciudad de Guatemala el mismo día e interior al día siguiente. También puedes comprar en nuestra tienda en zona 13, Ciudad de Guatemala.</p>
```

## Mello (crear)

- **Handle**: `mello` · **Título visible**: Mello
- **SEO title** (59): Mello Guatemala: fundas iPhone Duo y vidrios | Ventas Guate
- **Meta** (137): Accesorios Mello originales en Guatemala: fundas iPhone Duo, vidrio templado, protectores de cámara y cables USB-C. Envío a todo el país.
- **Condición**: `{"matchType": "ANY", "conditions": [{"productVendor": {"matchType": "ANY", "relation": "EQUALS", "values": ["Mello", "MELLO DISTRIBUTION"]}}, {"productTitle": {"matchType": "ANY", "relation": "STARTS_WITH", "values": ["Mello"]}}]}`
- **Enlaces** (verificados, responden 200): /collections/iphone-duo, /collections/cables
- **Notas**: Los 14 publicados tienen vendor 'MELLO DISTRIBUTION' (no 'Mello'). Hay 15 duplicados en borrador con vendor 'Ventas Guate' (no afectan: la colección solo muestra activos publicados). Stock bajo: iPhone Duo Púrpura (2) y Rosado (4).

```html
<p>Accesorios <strong>Mello Guatemala</strong> originales para proteger y cargar tu iPhone: fundas y vidrios para iPhone Duo, protectores de cámara y cables USB-C.</p>
<h2>Fundas iPhone Duo</h2>
<p>Fundas Mello para iPhone Duo en Clear, Negro, Azul, Púrpura y Rosado, además del modelo Ch64 en negro. Ver <a href="/collections/iphone-duo">accesorios iPhone Duo</a>.</p>
<h2>Vidrios y protectores de cámara</h2>
<p>Vidrio templado clear y de privacidad, y protectores de cámara 2 en 1 y completo en plata y azul.</p>
<h2>Cables</h2>
<p>Cables USB-C a Lightning y USB-C a USB-C en blanco. Más opciones en <a href="/collections/cables">cables USB-C y Lightning</a>.</p>
<h2>Preguntas frecuentes</h2>
<p><strong>¿Los productos Mello son originales?</strong><br>Sí. Mello es una de las marcas oficiales que distribuimos en Guatemala.</p>
<p><strong>¿Tienen garantía?</strong><br>Sí, 1 año por defectos de fabricación.</p>
<p><strong>¿Hacen envíos?</strong><br>Sí, a toda Guatemala con pago contra entrega: Ciudad de Guatemala el mismo día e interior al día siguiente. También puedes comprar en nuestra tienda en zona 13, Ciudad de Guatemala.</p>
```

## Reelcharge (crear)

- **Handle**: `reelcharge` · **Título visible**: Reelcharge
- **SEO title** (60): Reelcharge Guatemala: powerbanks y cargadores | Ventas Guate
- **Meta** (148): Power banks y cargadores Reelcharge originales en Guatemala: Reelsafe, Reelsafe Glass magnético, Fusion y cargador 45W tipo C. Envío a todo el país.
- **Condición**: `{"matchType": "ANY", "conditions": [{"productVendor": {"matchType": "ANY", "relation": "EQUALS", "values": ["Reelcharge"]}}, {"productTitle": {"matchType": "ANY", "relation": "STARTS_WITH", "values": ["Reelcharge"]}}]}`
- **Enlaces** (verificados, responden 200): /collections/powerbanks, /collections/cubos, /collections/auto
- **Notas**: Los 8 publicados tienen vendor 'Ventas Guate': sin la regla por título la colección quedaría vacía.

```html
<p>Carga tu teléfono donde estés con <strong>Reelcharge Guatemala</strong>: power banks, cargador de pared tipo C y holder inalámbrico para carro.</p>
<h2>Power banks</h2>
<p>Reelsafe de 5000 y 10000 mAh semi sólido, Reelsafe Glass magnético de 5000 mAh en gris y plata, y Fusion, que une power bank de 5000 mAh y cargador de 65 W, en negro y blanco. Ver <a href="/collections/powerbanks">power banks</a>.</p>
<h2>Cargadores</h2>
<p>Cargador de pared Smart de 45 W tipo C y holder inalámbrico de 15 W para la rejilla del carro, con cable retráctil. Más en <a href="/collections/cubos">cargadores de pared</a> y <a href="/collections/auto">accesorios para carro</a>.</p>
<h2>Preguntas frecuentes</h2>
<p><strong>¿Los productos Reelcharge son originales?</strong><br>Sí. Reelcharge es una de las marcas oficiales que distribuimos en Guatemala.</p>
<p><strong>¿Tienen garantía?</strong><br>Sí, 1 año por defectos de fabricación.</p>
<p><strong>¿Hacen envíos?</strong><br>Sí, a toda Guatemala con pago contra entrega: Ciudad de Guatemala el mismo día e interior al día siguiente. También puedes comprar en nuestra tienda en zona 13, Ciudad de Guatemala.</p>
```
