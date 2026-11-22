# Registro de publicación · fichas iTronics, Prodigee y Tucano

**Fechas:** 2026-11-21 (lotes 00–08) y 2026-11-22 (lotes 09–25 y metas SEO) · **Aprobación:** Diego Segura (21/11/2026; continuación autorizada el 22/11/2026) · **Estado:** COMPLETO

## Respaldo previo
- `respaldo_previo_publicacion_2026-11-21.json`: `descriptionHtml`, `seo` y `updatedAt` leídos de Shopify justo antes de publicar. Cubre las 208 fichas de las 3 propuestas más la Saddle Bag Tucano. En `solo_meta_seo` están las 2 fichas Tucano con precio en la meta (Saddle Bag y Travel Adapter 100W).
- Comparación con `*_respaldo.json` (espacios normalizados): **209/209 iguales**.
- Antes de retomar el 22/11 se volvió a leer el `updatedAt` de las 136 fichas pendientes. Todas tenían un valor igual o anterior a 2026-11-21T20:54:08Z, es decir, ninguna cambió después del respaldo.
- No se omitió ninguna ficha por cambios.

## Aplicado (productUpdate en lotes de 8, 26 lotes)
| Marca | Campos | Aplicadas | userErrors |
|---|---|---|---|
| iTronics (seminuevos) | solo `descriptionHtml` | **99** (las 7 con html nulo no se tocaron) | 0 |
| Prodigee | `descriptionHtml` + `seo.title` + `seo.description` | **64** | 0 |
| Tucano | `descriptionHtml` + `seo.title` + `seo.description` | **45** | 0 |
| **Total** | | **208** | **0** |

- No se cambió el título del producto ni otros campos.
- El lote 09 fue rechazado en la confirmación el 21/11. Se reintentó el 22/11 con autorización expresa de Diego y se aplicó sin errores.
- Al publicar el SEO de las propuestas se eliminaron los precios de las metas de Prodigee y Tucano: Balance lavanda, Rolltop, Crossbody azul y verde, Desk Pad, Gommo Sleeve, Isotta, City Backpack y Shopper.

## Metas SEO sin precio (paso 3)
| Ficha | Antes | Después |
|---|---|---|
| Tucano Let Me Out Foldable Saddle Bag Negro (`9386244473045`) | "…Saddle Bag negro en liquidación a Q275 (antes Q649). Liviano y resistente al agua. Compra en Ventas Guate." | "Bolso plegable Tucano Let Me Out Saddle Bag negro. Liviano y resistente al agua. Compra en Ventas Guate." (103 caracteres) |
| Tucano Travel Adapter Gan 100W Blanco (`9149956128981`) | "…laptop, tablet y celular. ✓ Original. Q365." | "Adaptador de viaje Tucano GaN 100W universal en Guatemala. Carga rápida para laptop, tablet y celular. ✓ Original." (115 caracteres) |

**Incidente corregido:** en el Travel Adapter, enviar `seo` solo con `description` dejó `seo.title` en null. Se restauró de inmediato con el valor del respaldo ("Adaptador Tucano GaN 100W Universal Blanco Guatemala") y se verificó que quedó bien. La Saddle Bag ya tenía `seo.title` null antes del cambio.
**Lección:** con `productUpdate`, `seo` reemplaza el objeto completo, así que hay que enviar siempre `title` y `description` juntos.

## Verificación (lectura posterior)
- Prodigee: KickIt iPhone 17 Negro, Balance 15/14/13 Lavanda y Glow S23 Ultra coinciden con la propuesta en descripción y SEO.
- Tucano: Gommo Sleeve 16" negro, Gommo Roll-Top azul y Work Out 4 negra coinciden con la propuesta en descripción y SEO.
- iTronics: iPhone 8 Plus 64GB, 13 128GB Verde, 16e 128GB Blanco y 16 128GB Negro tienen la descripción correcta y el SEO sin cambios.
- Shopify solo agrega saltos de línea entre `<li>` en el HTML. El título del producto no cambió en ninguna.

## Cómo revertir
Para cada id, aplicar `productUpdate(product:{id, descriptionHtml, seo:{title, description}})` con los valores de `respaldo_previo_publicacion_2026-11-21.json` → `productos[]`. En iTronics basta con `descriptionHtml`, porque su SEO no se tocó. Las 2 metas del paso 3 están en `solo_meta_seo` y en `productos[]` (Saddle Bag). Al revertir hay que enviar siempre `title` y `description` juntos.
