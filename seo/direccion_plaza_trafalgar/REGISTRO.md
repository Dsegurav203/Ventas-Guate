# Dirección oficial: "Edificio Plaza Trafalgar"

Aprobado por Diego Segura (dueño) el 2026-11-28. Dirección correcta: **9a Calle 15-45 zona 13, Edificio Plaza Trafalgar, Oficina 102, Ciudad de Guatemala**.

## Aplicado en Shopify (2026-11-28 ~15:06 UTC)

Reemplazo exacto `Edificio Trafalgar` → `Edificio Plaza Trafalgar` en el `body` de cada página (`pageUpdate`). Nada más cambió (diff = solo las líneas con la dirección).

| Página | id | Ocurrencias | Respaldo | Verificación en vivo |
|---|---|---|---|---|
| /pages/contact | gid://shopify/Page/579387949269 | 1 (+2 en meta description autogenerada) | `respaldo_contact.html` | body exacto en el HTML publicado; 0 "Edificio Trafalgar", 3 "Plaza Trafalgar" |
| /pages/garantia | gid://shopify/Page/595822444757 | 1 | `respaldo_garantia.html` | OK, 0 / 1 |
| /pages/envios | gid://shopify/Page/595822411989 | 1 | `respaldo_envios.html` | OK, 0 / 1 |
| /pages/preguntas-frecuentes | gid://shopify/Page/595823722709 | 2 (texto + JSON-LD FAQPage) | `respaldo_preguntas-frecuentes.html` | OK, 0 / 2 |
| /pages/sobre-ventas-guate | gid://shopify/Page/596193018069 | 1 | `respaldo_sobre-ventas-guate.html` | OK, 0 / 1 |

`aplicado_<handle>.html` = body publicado. Verificación: `curl --cacert /root/.ccr/ca-bundle.crt https://ventasguate.gt/pages/<handle>` contiene el archivo `aplicado_` completo, byte a byte (el CDN tardó ~1–2 min en refrescar).

Revertir: `pageUpdate(id, page:{body: <contenido de respaldo_<handle>.html>})`.

## Pendiente: aún dice "Edificio Trafalgar" (no se tocó)

| Lugar | Detalle | Cómo corregir |
|---|---|---|
| Tema publicado (inicio `/`) | JSON-LD de la portada: `"streetAddress": "9a Calle 15-45 zona 13, Edificio Trafalgar, Oficina 102"` (solo en `/`; las páginas no lo muestran) | Editar en el tema (Admin → Editar código o duplicado + publicación por Diego), regla 7 |
| Colección `seminuevos` (iPhone Seminuevos) | descriptionHtml | `collectionUpdate` con aprobación |
| Colección `mondo` (Mondo) | descriptionHtml | idem |
| Colección `reservas` (Reservas iPhone) | descriptionHtml | idem |

Ya dicen "Plaza Trafalgar": colecciones `hifuture`, `skullcandy`, `smartwatch`; los 2 artículos publicados del blog `guias`.

Productos: 0 de 3,089 (Admin `productsCount(query:"Trafalgar")` = 0; la búsqueda por defecto incluye la descripción) y 0 de 1,331 publicados en `/products.json`.
