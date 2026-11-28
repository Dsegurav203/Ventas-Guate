# Corrección de las 2 guías ya publicadas (blog `guias`) · PROPUESTA, no aplicada

Fecha: 2026-11-28. Pedido por Diego Segura. Blog `gid://shopify/Blog/99227795669`.

Respaldo = body publicado (tomado de `/blogs/guias.atom`, verificado byte a byte contra la página en vivo). Propuesto = respaldo + cambios de abajo; nada más cambia (enlaces, tablas, preguntas frecuentes, estructura intactos).

| Artículo | id | Respaldo | Propuesto |
|---|---|---|---|
| Regalos tecnológicos de Navidad en Guatemala 2026: ideas por presupuesto | gid://shopify/Article/635092435157 | `regalos-tecnologicos-navidad-guatemala_respaldo.html` | `regalos-tecnologicos-navidad-guatemala_propuesto.html` |
| ¿Qué audífonos Skullcandy comprar? Comparativa 2026 | gid://shopify/Article/635312144597 | `que-audifonos-skullcandy-comprar_respaldo.html` | `que-audifonos-skullcandy-comprar_propuesto.html` |

## Dirección

Ambos ya dicen **"Edificio Plaza Trafalgar"**: sin cambio.

## 1. Regalos de Navidad

| Tipo | Antes | Después |
|---|---|---|
| Voseo | Si buscás un regalo | Si buscas un regalo |
| Voseo | los podés ver en nuestra tienda | los puedes ver en nuestra tienda |
| Voseo | Escribinos al +502 4027-3277 | Escríbenos al +502 4027-3277 |
| Precio | ordenados por presupuesto, desde **Q249**. | ordenados de menor a mayor presupuesto. |
| Precio | H2 "Regalos hasta Q300" | "Regalos económicos" |
| Precio | H2 "Regalos de Q300 a Q600" | "Regalos de presupuesto medio" |
| Precio | H2 "Regalos de Q600 a Q1,000" | "Regalos que se notan" (el párrafo dice "Para un regalo que se note") |
| Precio | H2 "Regalos de más de Q1,000" | "Regalos premium" |
| Precio | Columna "Precio" en las 4 tablas (27 celdas, Q249 a Q3,999) | Eliminada; quedan "Regalo" y "Para quién" |

Fuera del body (se cambian con `articleUpdate` si se aprueba):

| Campo | Actual | Propuesto |
|---|---|---|
| summary | `<p>Ideas de regalos tecnológicos para Navidad 2026 en Guatemala, de Q249 a Q4,000: audífonos, smartwatches, bocinas, Alexa y power banks originales con 1 año de garantía.</p>` | `<p>Ideas de regalos tecnológicos para Navidad 2026 en Guatemala, de regalos económicos a premium: audífonos, smartwatches, bocinas, Alexa y power banks originales con 1 año de garantía.</p>` |
| Título, SEO title, meta | sin montos | sin cambio |

## 2. Skullcandy

| Tipo | Antes | Después |
|---|---|---|
| Precio + voseo | Skullcandy tiene audífonos desde Q249 hasta Q1,899, … para que elijás en 2 minutos | Skullcandy tiene audífonos para todos los presupuestos, … para que elijas en 2 minutos |
| Voseo | Encabezados "Si buscás…" / "Comprá" | "Si buscas…" / "Compra" |
| Voseo | Si viajás en bus, trabajás … o volás seguido … no tenés que subir | Si viajas … trabajas … vuelas … no tienes que subir |
| Voseo | lo podés ajustar … es el que querés probar | lo puedes ajustar … es el que quieres probar |
| Voseo | si los perdés | si los pierdes |
| Voseo | ¿Buscás otra marca? Mirá también | ¿Buscas otra marca? Mira también |
| Precio | Columna "Precio" en las 3 tablas (21 celdas) | Eliminada |
| Precio | 7 montos entre paréntesis en viñetas: "Smokin' Buds 360 (Q399):", "Dime 360 (Q599):", "Sesh ANC Active (Q599):", "Icon ANC (Q830):", "Method 360 ANC (Q1,235):", "Push Play Active (Q499):", "Push 720 Open (Q1,709):" | Solo el nombre: "Smokin' Buds 360:", etc. |

Título, summary, SEO title y meta no tienen montos: sin cambio ("precio en Guatemala" sin cifra se deja).

Comprobación: 0 montos `Q\d` y 0 formas de voseo en los 2 propuestos.

## Observaciones (no se cambiaron, para decidir)

- Regalos recomienda **Skullcandy Dime 3** (tabla y "Para adolescentes"); la guía Skullcandy dice que el Dime 3 se agotó y el reemplazo es el Dime 360.
- Smokin' Buds: Regalos dice "hasta 20 h de batería total"; Skullcandy dice "hasta 32 h". Revisar contra la ficha.
- Regalos usa en la tabla "Para quién" frases como "a precio de entrada" y "Nuestro accesorio más vendido": sin montos, se dejaron.

## Para aplicar (cuando Diego apruebe)

`articleUpdate(id, article:{body: <contenido de *_propuesto.html>})` (+ `summary` en Regalos). Revertir con el `_respaldo.html`. Registrar fecha en `../REGISTRO.md`.
