# HiFuture · fichas largas (voseo) reescritas con plantilla — PROPUESTA

**Fecha:** 2026-11-22 · **Estado:** solo propuesta, nada publicado en Shopify ni Odoo. Títulos y SEO sin cambios.

De las 13 fichas que solo se pasaron de voseo a tú, 10 tienen más de 180 palabras en Shopify (las otras 3: Alpha Azul 92, Aura2 Silver 101, Boombeat 111 — quedan fuera).

- Fuente: ficha oficial `https://hifuturegroup.com/products/<handle>` (texto de la página + imágenes de la galería). Solo se conservaron datos que estaban en la descripción actual **y** aparecen en la ficha oficial; lo demás se quitó y está en `dudas`.
- Archivos: `largas_propuesta.json` (id, title, html, palabras, palabras_antes, fuente_url, dudas) · `largas_respaldo.json` (descriptionHtml actual).
- Validación (Python): HTML bien formado, 90–180 palabras, 4–7 viñetas, cierre estándar exacto, sin voseo, sin `Q`+dígitos, sin "entrega inmediata"/"garantía de fabricante"/"el más versátil"/"precio", color del título presente → 10/10 OK.

| Producto | ID | Palabras antes → después | Fuente | Datos quitados (sin fuente o contradicen la oficial) |
|---|---|---|---|---|
| Audífonos HiFuture FlyBuds 4 ANC – Negro | `9142015492309` | 256 → 103 | [flybuds4](https://hifuturegroup.com/products/flybuds4) | driver 13 mm, transparencia, BT 5.3 (oficial 5.4), 9 h/36 h (oficial 30 h), IPX5, táctil, Android/iOS |
| Correa HiFuture Anchor-E para Smartwatch – Rosado | `9329902846165` | 214 → 91 | [anchor-e](https://hifuturegroup.com/products/anchor-e) | "smartwatch Anchor-E" (Anchor-E es la correa), grado médico/hipoalergénica, lavable, ventilación, multiposición |
| Smartwatch HiFuture Flex2 – Silver | `9142015361237` | 250 → 97 | [flex2](https://hifuturegroup.com/products/flex2) | 7 días (oficial 10), llamadas BT, SpO2, calorías, fases de sueño, carga magnética, notificaciones, Android/iOS |
| Bocina HiFuture Vocalist 100 con Micrófono – Negro | `9142016770261` | 227 → 91 | [vocalist-100](https://hifuturegroup.com/products/vocalist-100) | 30W/60W, 8 h, BT 5.0, efectos de voz, asa |
| Audífonos HiFuture Tour MKII Over-Ear ANC – Negro | `9329900454101` | 207 → 97 | [tour-mk-ll](https://hifuturegroup.com/products/tour-mk-ll) | transparencia, BT 5.3 (oficial 5.4), USB-C, arco ajustable, comparaciones de precio |
| Audífonos HiFuture Tour MKII Over-Ear ANC – Offwhite | `9329900650709` | 214 → 97 | [tour-mk-ll](https://hifuturegroup.com/products/tour-mk-ll) | transparencia, BT 5.3 (oficial 5.4), USB-C, arco ajustable, "mejor precio" |
| Smartwatch HiFuture Edge – Púrpura | `9329910874325` | 235 → 96 | [edge](https://hifuturegroup.com/products/edge) | AMOLED (oficial HD), IP68 (oficial 1 ATM), sueño por fases, notificaciones, iOS/Android |
| Smartwatch HiFuture Aura2 – Negro | `9142014279893` | 242 → 102 | [aura2](https://hifuturegroup.com/products/aura2) | estrés, notificaciones, rechazar/silenciar, natación, Android/iOS |
| Smartwatch HiFuture Edge – Negro | `9142014869717` | 245 → 96 | [edge](https://hifuturegroup.com/products/edge) | AMOLED (oficial HD), estrés, fases de sueño, carga magnética, notificaciones, carátulas, Android/iOS |
| Smartwatch HiFuture Flex2 – Negro | `9149965959381` | 243 → 95 | [flex2](https://hifuturegroup.com/products/flex2) | llamadas BT, AMOLED flexible, 7 días (oficial 10), SpO2, fases, "sumergible/piscina", notificaciones, música/cámara/linterna, iOS/Android |

## Dudas a resolver antes de publicar

1. **Correa Anchor-E (prioritario):** el texto actual dice que es "para el smartwatch HiFuture Anchor-E" y que no sirve en otros relojes. En hifuturegroup.com, Anchor-E es la **correa** (categoría Strap, cierre magnético snap-on), no un reloj. La ficha oficial no indica relojes compatibles ni ancho; por eso la propuesta **no lleva sección Compatibilidad**. Confirmar ancho (mm) y modelos compatibles con el proveedor y agregarla.
2. **Flex2 (Silver y Negro):** el texto actual dice "hasta 7 días" y "llamadas Bluetooth"; la ficha oficial dice 10 días y no menciona llamadas. Ambos se quitaron. Si se confirma, se puede agregar "hasta 10 días".
3. **Edge Púrpura / Flex2 Negro:** IP68 vs 1 ATM. Edge: oficial 1 ATM → se quitó IP68. Flex2: oficial IP68 → se mantuvo, sin "sumergible".
4. **Vocalist 100:** la ficha oficial habla de micrófono inalámbrico "dual" en la línea Vocalist; confirmar si la caja trae 1 o 2 micrófonos.
5. Datos oficiales útiles que **no** se agregaron por no estar en el texto actual (agregar solo si se aprueba ampliar): FlyBuds4 Wireless 5.4, 30 h, 4 micrófonos; Tour MKII Wireless 5.4, ANC híbrido, cable AUX; Edge 1.72" HD, aluminio, 1 ATM; Aura2 AMOLED 1.32", 1 ATM; Flex2 FHD 1.39", 10 días.

Detalle completo de cada duda en `largas_propuesta.json` → `dudas`.

## Ejemplo completo: Audífonos HiFuture FlyBuds 4 ANC – Negro (256 → 103 palabras)

Fuente: https://hifuturegroup.com/products/flybuds4

```html
<p>Los <strong>HiFuture FlyBuds 4 ANC</strong> en color Negro son audífonos true wireless con cancelación activa de ruido. Bloquean el ruido de fondo para que disfrutes tu música, podcasts y llamadas en el bus, la oficina o cualquier lugar con ruido.</p>
<h2>Características</h2>
<ul>
<li>Cancelación activa de ruido (ANC) para aislarte del entorno</li>
<li>Sonido con graves presentes, medios equilibrados y voces claras</li>
<li>Micrófonos con reducción de ruido ambiental para llamadas más claras</li>
<li>Diseño true wireless in-ear, sin cables</li>
<li>Color: Negro</li>
</ul>
<p>Producto original con 1 año de garantía. Envío a toda Guatemala con pago contra entrega, o cómpralo en nuestra tienda en zona 13, Ciudad de Guatemala.</p>
```

Dudas:

- Driver de 13 mm: la ficha oficial no lo indica (quitado).
- Modo transparencia: no aparece en la ficha oficial (quitado).
- Bluetooth 5.3: la ficha oficial dice Wireless 5.4 (quitado; no se agrega 5.4 por no estar en el texto actual).
- Batería 9 h / 36 h: la ficha oficial dice hasta 30 h de reproducción (quitado).
- IPX5, controles táctiles y compatibilidad Android/iOS: no aparecen en la ficha oficial (quitados).
- La ficha oficial dice "4-mic built-in system"; se mantiene "micrófonos con reducción de ruido" sin número.

## Ejemplo completo: Correa HiFuture Anchor-E para Smartwatch – Rosado (214 → 91 palabras)

Fuente: https://hifuturegroup.com/products/anchor-e

```html
<p>La correa <strong>HiFuture Anchor-E</strong> en color Rosado renueva el look de tu smartwatch. Es de silicona suave y flexible, se coloca en segundos y combina con looks casuales, deportivos o semiformales.</p>
<h2>Características</h2>
<ul>
<li>Ajuste rápido: se coloca en segundos</li>
<li>Silicona de alta calidad, suave con la piel y resistente</li>
<li>Flexible y cómoda para usarla durante horas seguidas</li>
<li>Apta para el ejercicio: soporta el sudor</li>
<li>Color: Rosado</li>
</ul>
<p>Producto original con 1 año de garantía. Envío a toda Guatemala con pago contra entrega, o cómpralo en nuestra tienda en zona 13, Ciudad de Guatemala.</p>
```

Dudas:

- PRIORITARIO: el texto actual dice que es para un "smartwatch HiFuture Anchor-E" y que no es compatible con otros relojes. En hifuturegroup.com Anchor-E es el nombre de la correa (categoría Strap), no de un reloj. La ficha oficial no indica modelos compatibles ni ancho de pasador, por eso no se incluye sección Compatibilidad: confirmar con el proveedor (ancho en mm y relojes compatibles) antes de publicar o agregarla.
- Silicona "de grado médico" e "hipoalergénica": la ficha oficial dice "high-quality solid silicone" (se usa eso).
- Mecanismo: el texto actual dice "deslizas la correa, sin herramientas"; la ficha oficial describe cierre magnético snap-on. Se dejó solo "se coloca en segundos" (coinciden). Recomendado agregar "cierre magnético" (no estaba en el texto actual, no se agregó).
- Lavable con agua y jabón, ventilación por textura interior y ajuste multiposición: no aparecen en la ficha oficial (quitados).
- Frases eliminadas: "el color más femenino y delicado", "la opción más accesible", "garantía de fabricante", "envío rápido".
- Color oficial: Pink; en tienda Rosado (se usa el del título).

## Cómo revertir (si se publica)

`largas_respaldo.json` tiene el `descriptionHtml` actual de las 10. Para cada producto: `productUpdate(product:{id, descriptionHtml})` con ese valor (sin tocar `seo`).
