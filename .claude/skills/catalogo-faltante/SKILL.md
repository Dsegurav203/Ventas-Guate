---
name: catalogo-faltante
description: Encuentra productos muy vendidos en Odoo que no se venden en la tienda en línea (ocultos, en borrador, archivados, sin stock exportado o inexistentes) y los reactiva con criterio. Usar cuando pidan "productos ocultos", "qué falta en la tienda", "reactivar productos", "por qué sale agotado en línea", "stock no se refleja".
---

# Catálogo faltante en la tienda

Sigue `ECOMMERCE_SEO.md` (importado en `CLAUDE.md`). Referencia: `seo/top100/CATALOGO_FALTANTE.md`, `inactivos_shopify.json`, `reactivacion.json`.

## 1. Cruce Odoo ↔ Shopify
- Ventas 12 meses: `seo/top100/odoo_top_productos.py`.
- Excluir lo que no se vende en línea (ej. Protection Pro: requiere instalación en punto; muestras).
- Clasificar: A) existe en Shopify pero UNLISTED/DRAFT/ARCHIVED; B) no existe.

## 2. Diagnóstico de stock
- El conector exporta stock solo de las bodegas en `shopify.location.ept` → `export_stock_warehouse_ids` (hoy BD3, TVGDC, OFI BODEGA 13).
- Stock exportable por producto: leer `free_qty` de `product.product` con `context={"warehouse_id": id}` para cada bodega exportada.
- Si un producto tiene stock en otra bodega (ej. APW), reportarlo; agregar bodegas solo con aprobación de Diego.

## 3. Reactivar (tras aprobación)
Criterio aprobado: stock exportable > 0, precio > Q1 y con foto. Archivados que son duplicados ya fusionados: no reactivar.
- `productUpdate(product:{id, status: ACTIVE})` + `publishablePublish(id, input:[{publicationId: <Tienda online>}])` (consultar `publications{ nodes{ id catalog{title} } }`).
- Sin foto → pasar a la habilidad `imagenes-catalogo`.
- Productos inexistentes (B): crearlos desde el conector de Odoo (no directo en Shopify) para que queden sincronizados.
- Registrar en `CATALOGO_FALTANTE.md`.
