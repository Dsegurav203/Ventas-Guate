# Títulos Prodigee: registro de lo aplicado (22/11/2026)

Aprobado por Diego Segura (dueño) el 22/11/2026. Regla 5 de `ECOMMERCE_SEO.md`.

## Alcance
- Revisados: todos los productos Shopify `vendor:Prodigee status:active` (419, paginado por título).
- Corregidos: **29** (detalle antes/después en `PROPUESTA.md` y `propuesta.json`).
- Solo se cambió `title`. Handles, SEO, descripciones e inventario sin cambios.

## Criterio
- Títulos en MAYÚSCULAS, sin "Prodigee" al inicio, con "para", "pro max" en minúscula o "PRODIGEE … para Samsung".
- Erratas: Balancce, Prodigeee, Safete, Fuschsia, Magsafee, "Galaxy 25" (SKU Odoo `SGS25-…`), "5mAh" (SKU Odoo `TEEK-PWR-TG-5K`), "10TH".
- Compatibilidad faltante: "Hero S24 Ultra" → Galaxy; "Safetee Neo 14 Pro Max" / "Safetee Flow Night 11 Pro" → iPhone.
- Colores: solo los del título original o confirmados por el SKU interno de Odoo (`STN` Stone, `MDN` Midnight, `BLK` Negro, `SMK` Smoke, `CLR` Clear, `FLW-NGT` Night Frost). "Prodigee Glow iPhone 17 Pro Max" y "Prodigee Glow Galaxy S26 Ultra" quedan sin color (sin fuente).

## Aplicado
1. Shopify: `productUpdate(product:{id,title})` en 2 lotes con alias (20 + 9). 29/29 sin `userErrors`.
2. Odoo: `name` escrito en la capa `shopify.product.template.ept` (búsqueda por `shopify_tmpl_id`, `active_test` False) y en `product.template` (contexto `es_GT` y `en_US`). 29/29 con capa; ninguno requirió emparejar por SKU.
3. Respaldo de nombres anteriores de Odoo (capa + plantilla en ambos idiomas): `respaldo_odoo.json`. Valores anteriores de Shopify: campo `antes` en `propuesta.json`.

## Verificación (Shopify = capa = plantilla)
| Shopify id | Título |
|---|---|
| 9141943861461 | Prodigee Safetee Flow iPhone 17 Pro Max Night Frost |
| 9141944877269 | Prodigee Jogger iPhone 17 Pro Max Stone |
| 9271506731221 | Prodigee Superstar Galaxy S26 Ultra Clear |
| 9142431645909 | Prodigee Balance Galaxy S25 Ultra Lavanda |
| 9150016946389 | Prodigee Safetee Flow iPhone 11 Pro Night |

## Observaciones
- En Odoo varias plantillas decían "iPhone 18 Pro Max/17 Pro Max" (formato de las fichas hermanas en Shopify); por instrucción quedaron como "iPhone 17 Pro Max". Si se prefiere la compatibilidad doble, es un cambio aparte.
- 9141946450133 quedó "Azul" como en Shopify, aunque el SKU Odoo dice `SHR-NVY` (Navy).
- Duplicados de SKU no tocados: "Prodigee Glow Galaxy S26 Ultra" (9384873132245) y "Prodigee Galaxy S26 Ultra Glow" (9271505223893) comparten 810192102693; "MagPower to-Go + Watch V2" aparece dos veces (810023958864).
- Fuera de alcance (no cambiados): orden de palabras tipo "Prodigee iPhone 16 Glow", "Galaxy S23 KickIt Rose", "Kick It", "6FT/1FT".

## Reversión
Shopify: reescribir `antes` de `propuesta.json`. Odoo: reescribir `capas[].name` y `product_template[id][lang]` de `respaldo_odoo.json`.
- 22/11: restaurada la compatibilidad "iPhone 18 Pro Max/17 Pro Max" en 11 fundas (Odoo la tenía; la corrección la había quitado) en Shopify, capa y plantilla. Super Hero 9141946450133: Azul → Navy (código SHR-NVY). Detalle en restaurar_18.json.
