---
name: seo-coleccion
description: Escribe y publica el texto, preguntas frecuentes, título y SEO de colecciones de ventasguate.gt, priorizadas por sesiones; también oculta de Google colecciones de campaña. Usar cuando pidan "texto de colección", "categorías", "colecciones principales", "ocultar colección de Google" o una colección nueva.
---

# Colecciones SEO

Sigue `CLAUDE.md`. Referencia completa del trabajo hecho: `seo/colecciones/` (`build_textos.py`, `textos_colecciones.json`, `APLICADO.md`, respaldo CSV).

## 1. Priorizar
- Sesiones por página de entrada (ShopifyQL): `FROM sessions SHOW sessions, conversion_rate GROUP BY landing_page_path SINCE -90d UNTIL today ORDER BY sessions DESC LIMIT 400`.
- Inventario de colecciones: `collections(first:100){ id handle title productsCount{count} descriptionHtml seo{title description} hidden:metafield(namespace:"seo",key:"hidden"){value} }` (paginar).
- Excluir campañas y temporales (sale14/15/16, midnightsale, galaxy-week mientras esté activa).

## 2. Redactar con datos reales
- Productos activos de cada colección: `collectionByIdentifier(identifier:{handle:"…"}){ products(first:60, sortKey:BEST_SELLING){ nodes{ title vendor status } } }`.
- Mencionar solo modelos y marcas activos. Intro con la palabra clave ("fundas iPhone 17 en Guatemala") → H2 por modelo/marca/uso → enlaces a colecciones relacionadas → `<h2>Preguntas frecuentes</h2>` usando los datos oficiales de `CLAUDE.md`.
- Título visible claro en español ("Fundas Galaxy S26", no "S26 cases"). SEO title ≤ 70, meta ≤ 155, sin precios.
- Generar la propuesta con un script tipo `seo/colecciones/build_textos.py` y un `.md` para aprobar.

## 3. Publicar (tras "aprobado")
- Respaldo CSV de título/descripción/SEO actuales.
- `mutation($c0: CollectionUpdateInput!, …){ c0: collectionUpdate(collection:$c0){ collection{handle title} userErrors{field message} } … }` con variables, lotes de 10.
- Verificar leyendo las colecciones y registrar en `APLICADO.md`.

## Ocultar o eliminar
- Ocultar de Google (campañas, pruebas): `metafieldsSet` con `namespace:"seo", key:"hidden", type:"number_integer", value:"1"`.
- Eliminar solo si está vacía y no está en menús; crear antes `urlRedirectCreate` 301 hacia la colección equivalente.
