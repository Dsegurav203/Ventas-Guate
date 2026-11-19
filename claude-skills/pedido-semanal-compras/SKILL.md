---
name: "pedido-semanal-compras"
description: Agente de compras de los lunes de Ventas Guate — usando el conector Odoo Ventas Guate (MCP propio) (ventasguate.odoo.com) revisa inventario y rotación, sugiere pedidos por marca, crea las órdenes de compra en BORRADOR por proveedor asignadas a Mayra González y le notifica internamente a logistica@ventasguate.com. USAR SIEMPRE que alguien diga "revisión de los lunes", "pedido semanal", "sugerido de compras", "qué hay que pedir", "rotación de inventario", "reabastecer", "reorden", "días de inventario", "quiebres de stock", "qué marcas pedir", o cuando corra la tarea programada de los lunes, aunque no mencione órdenes de compra.
---

# Pedido semanal de compras — Ventas Guate (vía conector Odoo Ventas Guate)

Tres pasos en orden: **1) Consultar Odoo por el conector + calcular → 2) Crear OC en borrador → 3) Notificar a logística.**
No se necesitan credenciales: todo pasa por el conector Odoo Ventas Guate del usuario. El script solo hace cálculos y Excel.
Prohibido: `button_confirm`, `action_rfq_send`, mensajes a proveedores o clientes, notas que no sean `mail.mt_note`.

## 0. Verificar conexión
`odoo_search` en `res.company` → debe ser **BUYITWITHUS, S.A.** Si sale otra (p. ej. nadu-tech), detenerse y avisar.

## 1. Consultar (conector) y guardar
Fechas: `D90` = hoy−90, `D28` = hoy−28. Guardar cada respuesta tal cual en `/home/claude/pedido/<archivo>` con `create_file` (JSON completo del tool; `odoo_export` devuelve una lista JSON de filas: guardarla igual aunque el archivo se llame `.csv`, el script la lee).

Parámetros del conector: `odoo_group(model, groupby=[…], aggregates=["campo:sum",…], domain, limit)` · `odoo_export(model, fields=[…], domain, order, limit≤2000)` · `odoo_search(model, domain, fields, limit≤500)`.

| # | Tool | Modelo | Dominio | groupby / fields | Archivo |
|---|---|---|---|---|---|
| A | odoo_group | stock.move | `[["state","=","done"],["location_dest_id.usage","=","customer"],["date",">=",D90],["product_id.brand_id","!=",126],["product_id.name","not ilike","APPLE IPHONE"],["product_id.purchase_ok","=",true]]` | groupby `product_id`, agg `product_uom_qty:sum`, limit 2000 | ventas_90.json |
| B | odoo_group | stock.move | igual con `D28` | igual | ventas_28.json |
| C | odoo_group | stock.quant | `[["location_id.complete_name","in",UBIC],["product_id","in",IDS]]` (+ hijas: usar `child_of` sobre ids de ubicación si hace falta) | groupby `product_id`, agg `quantity:sum`, `reserved_quantity:sum` | stock.json |
| D | odoo_group | purchase.order.line | `[["state","=","purchase"],["product_id","in",IDS]]` | groupby `product_id`, agg `product_qty:sum`, `qty_received:sum` | transito.json |
| E | odoo_group | purchase.order.line | `[["state","in",["draft","sent"]],["order_id.origin","!=",TAG],["product_id","in",IDS]]` | groupby `product_id`, agg `product_qty:sum` | borradores.json |
| F | odoo_export | purchase.order.line | `[["state","in",["purchase","done"]],["product_id","in",IDS]]`, order `id desc` | `product_id/.id, partner_id/.id, partner_id, currency_id/.id, currency_id, price_unit` | proveedores.csv |
| G | odoo_export | product.product | `[["id","in",IDS]]` | `.id, default_code, name, brand_id, standard_price, purchase_ok, seller_ids/partner_id/.id, seller_ids/partner_id, seller_ids/currency_id/.id, seller_ids/currency_id, seller_ids/price` | productos.csv |
| H | odoo_group (opcional) | sale.order.line | `[["state","in",["sale","done"]],["order_id.date_order",">=",D90],["product_id","in",IDS]]` | groupby `product_id, order_partner_id`, agg `product_uom_qty:sum` | clientes.json |
| I | odoo_group (opcional) | stock.quant | ubicaciones `Con/*`, `TOPC/*` | igual que C | consignacion.json |

- **Exclusión de Apple: SOLO por marca** — `brand_id != 126` (Apple) + `name not ilike "APPLE IPHONE"` (equipos sin marca cargada). **Prohibido** excluir por `iphone`, `ipad`, `airpods`, `macbook` o `apple` en el nombre: elimina los cases y accesorios de Prodigee, Laut, LOGiiX, Click, Nimbus9, etc. (error W47).
- **Marca para agrupar**: exportar `brand_id` en G; si está vacío, el script usa la primera palabra del nombre.
- **No comprables**: `purchase_ok = False` (productos "L-" de liquidación y marcas retiradas como PopSockets) quedan fuera desde el dominio.
- A ya trae `__count` (movimientos); el script exige ≥ 3 movimientos en 90 días para pedir (si no, alerta "venta concentrada").
- Límites del conector: `odoo_group` devuelve todos los grupos; `odoo_export` hasta 2000 filas por llamada (si F o G llegan a 2000, partir `IDS` en bloques y unir); `odoo_search` hasta 500.
- En `odoo_export` usar `/.id` (id numérico de la base) y no `/id` (que devuelve el id externo `__export__…`).
- `IDS` = product_id de A. `UBIC` = `config/parametros.json` → `ubicaciones_vendibles` (BD3/Stock, BD3/Input, OFIBD/BODEGA ATICO, TVGDC/Stock). Nunca GPP (garantías) ni MUESTRAS.
- `TAG` = `SUGERIDO SEMANAL <AAAA-Www>` (semana ISO).
- Si un resultado trae `has_more: true`, paginar con `offset` y unir antes de guardar.
- Muerto (stock sin venta) es opcional semanal; para incluirlo, repetir C sin filtro de IDS y agregar esos ids a G.

- **PO de cliente pendientes (opcional)**: si el usuario sube POs de clientes vencidas/por entregar, mapear `# de parte` → producto (product.supplierinfo.product_code, o por nombre) y guardar `pendientes_cliente.json` = `{"<product_id>": qty}`. Se suman a la necesidad aunque el producto no tenga venta en 90 d. Partes sin producto en Odoo → Alertas.

Luego:
```bash
python /mnt/skills/user/pedido-semanal-compras/scripts/calcular.py /home/claude/pedido
```
Genera en `/home/claude/pedido/salida/`: `sugerido.json`, `po_payload.json` (una OC por proveedor+moneda), `correo.html`, `Sugerido_Compras_<semana>.xlsx`. La lógica está en `references/logica.md`; los parámetros por marca en `config/parametros.json`.

**Mostrar al usuario el resumen por proveedor antes del paso 2** (en la tarea programada se continúa directo).

## 2. Crear OC en borrador (conector)
Por cada elemento de `po_payload.json`:
1. `odoo_search` `purchase.order` con `[["origin","=",TAG],["partner_id","=",P],["currency_id","=",C],["state","in",["draft","sent"]]]`.
   - Existe → `odoo_write` con `{"order_line": [[5,0,0], ...lineas]}` (reemplaza, no duplica).
   - No existe → `odoo_create` `purchase.order` con `vals` (todas las OC en una sola llamada).
2. Releer `name`, `amount_untaxed` y comparar contra `total` (±0.01).
3. `odoo_post_note` en la OC: `body` = `nota_html`, `html` = true, `internal` = true, `partner_ids` = `[2762]` (Mayra González, user 30).

## 3. Notificar a logística
1. `correo.html` reemplazando `{OC_i}` por link `https://ventasguate.odoo.com/web#id=<id>&model=purchase.order&view_type=form (NO usar /odoo/purchase/: da 404 en esta versión)` con el nombre de la OC.
2. `odoo_create` en `mail.mail`: `subject` "Sugerido de compras <semana> — N OC en borrador", `body_html`, `email_to` logistica@ventasguate.com, `auto_delete` false.
3. `odoo_action` (model `mail.mail`, method `send`) sobre ese id y releer `state` (debe ser `sent`; si es `exception`, reportar `failure_reason`).
No usar `odoo_post_note` con `partner_ids` para el resumen: Odoo no notifica al autor (el usuario conectado).
Entregar el Excel al usuario con `present_files`.

## Respuesta
Sin saludos. Primero: total por moneda, # OC creadas, # quiebres. Tabla: OC | proveedor | marcas | líneas | monto. Top 10 alertas. Capital en lento/muerto.

## Reglas
- APPLE fuera (mayoreo por oportunidad). Garantías y muestras fuera. Consignación se informa, no cuenta como disponible.
- Nunca sugerir productos con venta 90d = 0.
- Productos sin proveedor no entran a OC → Alertas.
- Lead time no confirmado en config = alerta "Lead time por confirmar"; no inventar.
- Mínimo de compra por proveedor (`config.minimo_usd_por_proveedor`, p. ej. Targus $20,000): si la OC no lo alcanza, NO se crea; queda en "Retenidas por mínimo" con su monto acumulado.
- Antes de crear OC, revisar OC en borrador abiertas del mismo proveedor (facturas de importación en proceso, p. ej. "INV-...") y descontarlas como entrantes.
