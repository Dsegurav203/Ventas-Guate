---
name: "creacion-productos-odoo"
description: Crea y valida productos en Odoo ventasguate.odoo.com con el estándar de Ventas Guate (nombre MARCA MODELO COLOR, UPC/EAN, SKU, categoría, precios, impuestos, proveedor) evitando duplicados. USAR SIEMPRE que Diego pida crear productos, dar de alta códigos, "códigos nuevos", cargar catálogo, productos de una factura/póliza que no existen en Odoo, revisar productos mal creados, o corregir nombre/código/categoría de un producto. También para auditar productos basura creados con nombre = código de barras, categoría "All" o precio 1.
---

# Creación de productos — estándar Ventas Guate

Odoo es la fuente maestra; Shopify (ventasguate.gt) se alimenta de Odoo. Nunca crear en Shopify primero.

## Estándar de campos (`product.template`)
| Campo | Regla | Ejemplo real |
|---|---|---|
| `name` | MAYÚSCULAS: `MARCA MODELO VARIANTE COLOR`, sin códigos en el nombre | SKULLCANDY DIME 360 SHAPE BONE |
| `default_code` | UPC/EAN (12–13 dígitos) — convención actual | 810145322710 |
| `barcode` | SKU del fabricante — convención actual | S2DPW-T001 |
| `categ_id` | Categoría real del árbol (nunca `1 All`) | 212 Audio / Audifonos in ear / True wireless |
| `type` / `is_storable` | `consu` + `true` | |
| `list_price` | **OBLIGATORIO** precio público de referencia con IVA en GTQ. Se publica automático en ventasguate.gt → NUNCA crear en 0 o 1.00. Si Diego no da precio, calcular sugerido: costo unit estimado c/IVA ÷ (1 − margen Tarifa Pública de la marca), terminación 9; marcarlo "propuesto" en el resumen | 599.00 |
| `taxes_id` | `[2]` IVA ventas | |
| `supplier_taxes_id` | `[1]` IVA compras (la OC de importación va sin impuestos a nivel línea) | |
| `seller_ids` | proveedor + `product_code` del proveedor + precio USD | |
| `uom_id` | 1 Units | |
| `image_1920` | vía skill `imagenes-productos-odoo` | |

⚠️ Swap pendiente: Diego planea intercambiar `default_code` ↔ `barcode` en todo el catálogo para usar la app Barcode. Cuando se ejecute, invertir las dos filas de la tabla. Preguntar si ya se hizo si hay duda.

## Antes de crear (anti-duplicados)
Buscar cada código en `product.product` con dominio:
`["|","|","|",["default_code","=",c],["barcode","=",c],["seller_ids.product_code","=",c],["name","ilike",c]]`
incluyendo `active=false` (`context active_test=false` o dominio `["active","in",[true,false]]`).
- Existe → usar ese id. Si está archivado, proponer reactivar.
- Existe con datos basura (nombre = código, categ All, precio 1) → proponer corregir en vez de crear otro.
- No existe → candidato a crear.

## Procedimiento
1. Armar tabla de candidatos con todos los campos del estándar. Categoría: buscar `product.category` por `complete_name ilike` y proponer la más específica; si dudosa, preguntar.
2. Mostrar tabla; crear solo con "sí". Usar `odoo_create(model="product.template", values=[…])` en lote (máx. 200 por llamada).
3. Releer los creados y confirmar ids.
4. Pasar ids al skill `imagenes-productos-odoo`.

## Control de precio público (bloqueante)
- Antes de crear: ningún registro sale con `list_price` ≤ 1.
- Margen Tarifa Pública por marca (sobre precio, con costo+IVA): HiFuture 55 %, Prodigee 70 %; otras marcas: usar margen promedio de productos hermanos de la marca en Odoo.
- Después de cada póliza/costeo: buscar `list_price <= 1` en los productos de la póliza y corregir con el sugerido del costeo final.
- Si aparecen productos de otros usuarios con precio Q1 y stock, reportarlos como alerta (riesgo de venta web a Q1).

## Control de permisos
Usuarios autorizados para crear productos: Diego Segura, Henry Galindo, Luis Hernández, Auxiliar Contable, Mayra González. Si en una auditoría aparecen productos creados por otros usuarios (ej. "Auxiliar de bodega"), listarlos como alerta con id, nombre, fecha y creador.

## Auditoría rápida de productos basura
Dominio: `["|",["categ_id","=",1],["list_price","<=",1]]` (campos `name, default_code, barcode, categ_id, list_price, create_uid, create_date`, sin `image_1920`) y además filtrar en Python los nombres compuestos solo por dígitos o con patrón `[código] ...`. Reportar tabla y proponer corrección o fusión.
