# Propuesta descripciones iTronics (iPhone seminuevos)

Fecha: 2026-11-21 · **Solo propuesta, nada publicado en Shopify.** Alcance: `vendor:ITRONICS status:active` (106 fichas). Solo cambia `descriptionHtml`; títulos y SEO title/meta no se tocan.

## Resumen

| Concepto | Cantidad |
|---|---|
| Fichas activas iTronics | 106 |
| Propuestas (iPhone) | 99 |
| SIN FUENTE (Samsung, fuera de alcance Apple) | 7 |
| iPad | 0 (no hay iPad activos) |
| Modelos de iPhone distintos | 33 |

- Fuente única de especificaciones: comparador oficial de Apple https://www.apple.com/la/iphone/compare/ (consultado 2026-11-21), extraído a `itronics_specs_modelos.json` (texto literal de Apple en `apple_textual`).
- Datos propios de cada equipo conservados tal cual: capacidad, color, batería (porcentaje o rango), "Imagen de referencia", WhatsApp 4027-3277 con el mismo enlace `wa.me/50240273277`. Ninguna ficha menciona accesorios incluidos.
- No se afirma estado estético, liberado/operador ni contenido de caja. Resistencia al agua marcada como "especificación de fábrica de Apple".
- Validación Python: 99/99 HTML bien formado, 108–128 palabras, 6 `<li>`, sin `Q`+dígitos, batería idéntica a la ficha actual.

## Archivos

| Archivo | Contenido |
|---|---|
| `itronics_propuesta.json` | `{id,title,html,fuentes,dudas}` (106; Samsung con `html: null`) |
| `itronics_respaldo.json` | `descriptionHtml` actual de las 106 (lectura de Shopify 2026-11-21; plantilla idéntica en todas, 2 muestras comparadas byte a byte) |
| `itronics_specs_modelos.json` | Tabla por modelo (33 modelos) con URL de fuente |
| `itronics_propuesta.py` | Generador (lee `itronics_actual.tsv` + `itronics_apple_compare_extract.json`) |
| `itronics_apple_compare_parse.py` | Extractor del comparador de Apple |

## Dudas para aprobar

1. **iPhone 17 Air 256GB Azul Cielo Nuevo Sellado**: Apple lo llama "iPhone Air" (la propuesta usa ese nombre en el texto; el título no se cambió). Es caja sellada, no seminuevo: se usó "Equipo en caja sellada con 30 días de garantía" porque la ficha actual dice 30 días. Confirmar garantía y si se corrige el título.
2. **iPhone SE 2020**: se escribe "iPhone SE 2020 (2.ª generación)" (nombre oficial de Apple).
3. **iPhone 16e**: el comparador de Apple no le marca compatibilidad MagSafe, así que no se menciona.
4. **7 Samsung** con vendor ITRONICS: SIN FUENTE en este lote (no son Apple). Requieren ficha oficial de samsung.com en otra tarea.

## SIN FUENTE

| Producto | Motivo |
|---|---|
| Samsung Galaxy S23 FE 128GB Grafito | No es iPhone/iPad; requiere fuente Samsung |
| Samsung Galaxy S23 FE 128GB Menta | No es iPhone/iPad; requiere fuente Samsung |
| Samsung Galaxy S23 128GB Negro | No es iPhone/iPad; requiere fuente Samsung |
| Samsung Galaxy S24 FE 128GB Gris | No es iPhone/iPad; requiere fuente Samsung |
| Samsung Galaxy S26 256GB Negro | No es iPhone/iPad; requiere fuente Samsung |
| Samsung Galaxy S24 Ultra 512GB Amarillo Titanio | No es iPhone/iPad; requiere fuente Samsung |
| Samsung Galaxy S24 Ultra 512GB Gris Titanio | No es iPhone/iPad; requiere fuente Samsung |

## Modelos y especificaciones (Apple)

| Modelo | Fichas | Chip | Pantalla | Biometría | Conector | MagSafe | Agua |
|---|---|---|---|---|---|---|---|
| iPhone 8 Plus | 2 | A11 Bionic | Retina HD LCD de 5.5 pulgadas | Touch ID | Lightning | No | IP67, hasta 1 metro por 30 minutos |
| iPhone X | 2 | A11 Bionic | Super Retina HD OLED de 5.8 pulgadas | Face ID | Lightning | No | IP67, hasta 1 metro por 30 minutos |
| iPhone XS | 3 | A12 Bionic | Super Retina HD OLED de 5.8 pulgadas | Face ID | Lightning | No | IP68, hasta 2 metros por 30 minutos |
| iPhone XS Max | 1 | A12 Bionic | Super Retina HD OLED de 6.5 pulgadas | Face ID | Lightning | No | IP68, hasta 2 metros por 30 minutos |
| iPhone XR | 4 | A12 Bionic | Liquid Retina HD LCD de 6.1 pulgadas | Face ID | Lightning | No | IP67, hasta 1 metro por 30 minutos |
| iPhone SE 2020 | 1 | A13 Bionic | Retina HD LCD de 4.7 pulgadas | Touch ID | Lightning | No | IP67, hasta 1 metro por 30 minutos |
| iPhone 11 | 6 | A13 Bionic | Liquid Retina HD LCD de 6.1 pulgadas | Face ID | Lightning | No | IP68, hasta 2 metros por 30 minutos |
| iPhone 11 Pro | 7 | A13 Bionic | Super Retina XDR OLED de 5.8 pulgadas | Face ID | Lightning | No | IP68, hasta 4 metros por 30 minutos |
| iPhone 11 Pro Max | 6 | A13 Bionic | Super Retina XDR OLED de 6.5 pulgadas | Face ID | Lightning | No | IP68, hasta 4 metros por 30 minutos |
| iPhone 12 mini | 2 | A14 Bionic | Super Retina XDR OLED de 5.4 pulgadas | Face ID | Lightning | Sí | IP68, hasta 6 metros por 30 minutos |
| iPhone 12 | 5 | A14 Bionic | Super Retina XDR OLED de 6.1 pulgadas | Face ID | Lightning | Sí | IP68, hasta 6 metros por 30 minutos |
| iPhone 12 Pro | 3 | A14 Bionic | Super Retina XDR OLED de 6.1 pulgadas | Face ID | Lightning | Sí | IP68, hasta 6 metros por 30 minutos |
| iPhone 12 Pro Max | 5 | A14 Bionic | Super Retina XDR OLED de 6.7 pulgadas | Face ID | Lightning | Sí | IP68, hasta 6 metros por 30 minutos |
| iPhone 13 mini | 3 | A15 Bionic | Super Retina XDR OLED de 5.4 pulgadas | Face ID | Lightning | Sí | IP68, hasta 6 metros por 30 minutos |
| iPhone 13 | 1 | A15 Bionic | Super Retina XDR OLED de 6.1 pulgadas | Face ID | Lightning | Sí | IP68, hasta 6 metros por 30 minutos |
| iPhone 13 Pro | 2 | A15 Bionic | Super Retina XDR OLED de 6.1 pulgadas | Face ID | Lightning | Sí | IP68, hasta 6 metros por 30 minutos |
| iPhone 13 Pro Max | 3 | A15 Bionic | Super Retina XDR OLED de 6.7 pulgadas | Face ID | Lightning | Sí | IP68, hasta 6 metros por 30 minutos |
| iPhone 14 | 1 | A15 Bionic | Super Retina XDR OLED de 6.1 pulgadas | Face ID | Lightning | Sí | IP68, hasta 6 metros por 30 minutos |
| iPhone 14 Plus | 5 | A15 Bionic | Super Retina XDR OLED de 6.7 pulgadas | Face ID | Lightning | Sí | IP68, hasta 6 metros por 30 minutos |
| iPhone 14 Pro | 2 | A16 Bionic | Super Retina XDR OLED de 6.1 pulgadas | Face ID | Lightning | Sí | IP68, hasta 6 metros por 30 minutos |
| iPhone 15 | 4 | A16 Bionic | Super Retina XDR OLED de 6.1 pulgadas | Face ID | USB-C | Sí | IP68, hasta 6 metros por 30 minutos |
| iPhone 15 Plus | 3 | A16 Bionic | Super Retina XDR OLED de 6.7 pulgadas | Face ID | USB-C | Sí | IP68, hasta 6 metros por 30 minutos |
| iPhone 15 Pro | 1 | A17 Pro | Super Retina XDR OLED de 6.1 pulgadas | Face ID | USB-C | Sí | IP68, hasta 6 metros por 30 minutos |
| iPhone 15 Pro Max | 4 | A17 Pro | Super Retina XDR OLED de 6.7 pulgadas | Face ID | USB-C | Sí | IP68, hasta 6 metros por 30 minutos |
| iPhone 16e | 1 | A18 | Super Retina XDR OLED de 6.1 pulgadas | Face ID | USB-C | No | IP68, hasta 6 metros por 30 minutos |
| iPhone 16 | 6 | A18 | Super Retina XDR OLED de 6.1 pulgadas | Face ID | USB-C | Sí | IP68, hasta 6 metros por 30 minutos |
| iPhone 16 Plus | 1 | A18 | Super Retina XDR OLED de 6.7 pulgadas | Face ID | USB-C | Sí | IP68, hasta 6 metros por 30 minutos |
| iPhone 16 Pro | 1 | A18 Pro | Super Retina XDR OLED de 6.3 pulgadas | Face ID | USB-C | Sí | IP68, hasta 6 metros por 30 minutos |
| iPhone 16 Pro Max | 6 | A18 Pro | Super Retina XDR OLED de 6.9 pulgadas | Face ID | USB-C | Sí | IP68, hasta 6 metros por 30 minutos |
| iPhone 17e | 1 | A19 | Super Retina XDR OLED de 6.1 pulgadas | Face ID | USB-C | Sí | IP68, hasta 6 metros por 30 minutos |
| iPhone 17 Air | 1 | A19 Pro | Super Retina XDR OLED de 6.5 pulgadas | Face ID | USB-C | Sí | IP68, hasta 6 metros por 30 minutos |
| iPhone 17 Pro | 2 | A19 Pro | Super Retina XDR OLED de 6.3 pulgadas | Face ID | USB-C | Sí | IP68, hasta 6 metros por 30 minutos |
| iPhone 17 Pro Max | 4 | A19 Pro | Super Retina XDR OLED de 6.9 pulgadas | Face ID | USB-C | Sí | IP68, hasta 6 metros por 30 minutos |

## 5 ejemplos

### iPhone 8 Plus 64GB Gris Espacial Seminuevo
`gid://shopify/Product/15499682578645`

```html
<p>iPhone 8 Plus de 64GB en color gris espacial, seminuevo revisado por nuestro equipo técnico. Combina el chip A11 Bionic con una pantalla Retina HD LCD de 5.5 pulgadas.</p>
<h2>Características</h2><ul>
  <li>Batería del equipo: 100%.</li>
  <li>Almacenamiento de 64GB.</li>
  <li>Sistema de dos cámaras de 12 MP: principal y teleobjetivo.</li>
  <li>Touch ID: sensor de huellas en el botón de inicio.</li>
  <li>Conector Lightning.</li>
  <li>Resistencia al agua IP67, hasta 1 metro por 30 minutos (especificación de fábrica de Apple).</li>
</ul>
<h2>Garantía y entrega</h2><p>Seminuevo con 30 días de garantía. Imagen de referencia: si quieres ver fotos reales del equipo, escríbenos por <a href="https://wa.me/50240273277?text=Hola%2C%20quiero%20ver%20fotos%20reales">WhatsApp al 4027-3277</a>. Envío a toda Guatemala con pago contra entrega, o cómpralo en nuestra tienda en zona 13, Ciudad de Guatemala.</p>
```

### iPhone XS 64GB Gris Espacial Seminuevo
`gid://shopify/Product/15499702042837`

```html
<p>iPhone XS de 64GB en color gris espacial, seminuevo revisado por nuestro equipo técnico. Combina el chip A12 Bionic con una pantalla Super Retina HD OLED de 5.8 pulgadas.</p>
<h2>Características</h2><ul>
  <li>Batería del equipo: 91-100%.</li>
  <li>Almacenamiento de 64GB.</li>
  <li>Sistema de dos cámaras de 12 MP: principal y teleobjetivo.</li>
  <li>Face ID: desbloqueo con reconocimiento facial.</li>
  <li>Conector Lightning.</li>
  <li>Resistencia al agua IP68, hasta 2 metros por 30 minutos (especificación de fábrica de Apple).</li>
</ul>
<h2>Garantía y entrega</h2><p>Seminuevo con 30 días de garantía. Imagen de referencia: si quieres ver fotos reales del equipo, escríbenos por <a href="https://wa.me/50240273277?text=Hola%2C%20quiero%20ver%20fotos%20reales">WhatsApp al 4027-3277</a>. Envío a toda Guatemala con pago contra entrega, o cómpralo en nuestra tienda en zona 13, Ciudad de Guatemala.</p>
```

### iPhone 13 128GB Verde Seminuevo
`gid://shopify/Product/15499722784981`

```html
<p>iPhone 13 de 128GB en color verde, seminuevo revisado por nuestro equipo técnico. Combina el chip A15 Bionic con una pantalla Super Retina XDR OLED de 6.1 pulgadas.</p>
<h2>Características</h2><ul>
  <li>Batería del equipo: 100%.</li>
  <li>Almacenamiento de 128GB.</li>
  <li>Sistema de dos cámaras de 12 MP: principal y ultra gran angular.</li>
  <li>Face ID: desbloqueo con reconocimiento facial.</li>
  <li>Conector Lightning y compatibilidad con accesorios MagSafe.</li>
  <li>Resistencia al agua IP68, hasta 6 metros por 30 minutos (especificación de fábrica de Apple).</li>
</ul>
<h2>Garantía y entrega</h2><p>Seminuevo con 30 días de garantía. Imagen de referencia: si quieres ver fotos reales del equipo, escríbenos por <a href="https://wa.me/50240273277?text=Hola%2C%20quiero%20ver%20fotos%20reales">WhatsApp al 4027-3277</a>. Envío a toda Guatemala con pago contra entrega, o cómpralo en nuestra tienda en zona 13, Ciudad de Guatemala.</p>
```

### iPhone 15 128GB Rosa Seminuevo
`gid://shopify/Product/15499725570261`

```html
<p>iPhone 15 de 128GB en color rosa, seminuevo revisado por nuestro equipo técnico. Combina el chip A16 Bionic con una pantalla Super Retina XDR OLED de 6.1 pulgadas.</p>
<h2>Características</h2><ul>
  <li>Batería del equipo: 88-98%.</li>
  <li>Almacenamiento de 128GB.</li>
  <li>Sistema de dos cámaras: principal de 48 MP y ultra gran angular.</li>
  <li>Face ID: desbloqueo con reconocimiento facial.</li>
  <li>Conector USB-C y compatibilidad con accesorios MagSafe.</li>
  <li>Resistencia al agua IP68, hasta 6 metros por 30 minutos (especificación de fábrica de Apple).</li>
</ul>
<h2>Garantía y entrega</h2><p>Seminuevo con 30 días de garantía. Imagen de referencia: si quieres ver fotos reales del equipo, escríbenos por <a href="https://wa.me/50240273277?text=Hola%2C%20quiero%20ver%20fotos%20reales">WhatsApp al 4027-3277</a>. Envío a toda Guatemala con pago contra entrega, o cómpralo en nuestra tienda en zona 13, Ciudad de Guatemala.</p>
```

### iPhone 17 Pro Max 256GB Azul Profundo Seminuevo
`gid://shopify/Product/15499754602709`

```html
<p>iPhone 17 Pro Max de 256GB en color azul profundo, seminuevo revisado por nuestro equipo técnico. Combina el chip A19 Pro con una pantalla Super Retina XDR OLED de 6.9 pulgadas.</p>
<h2>Características</h2><ul>
  <li>Batería del equipo: 93%.</li>
  <li>Almacenamiento de 256GB.</li>
  <li>Sistema de cámaras Pro Fusion de 48 MP: principal, ultra gran angular y teleobjetivo.</li>
  <li>Face ID: desbloqueo con reconocimiento facial.</li>
  <li>Conector USB-C y compatibilidad con accesorios MagSafe.</li>
  <li>Resistencia al agua IP68, hasta 6 metros por 30 minutos (especificación de fábrica de Apple).</li>
</ul>
<h2>Garantía y entrega</h2><p>Seminuevo con 30 días de garantía. Imagen de referencia: si quieres ver fotos reales del equipo, escríbenos por <a href="https://wa.me/50240273277?text=Hola%2C%20quiero%20ver%20fotos%20reales">WhatsApp al 4027-3277</a>. Envío a toda Guatemala con pago contra entrega, o cómpralo en nuestra tienda en zona 13, Ciudad de Guatemala.</p>
```

## Para publicar (tras "aprobado")

Lotes de 8–10 con `productUpdate(product:{id, descriptionHtml})` y el contenido en `variables`, solo las 99 con `html`. Reversión: `itronics_respaldo.json`.
