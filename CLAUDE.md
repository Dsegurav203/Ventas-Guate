# Ventas Guate — Instrucciones para Claude

Buyitwithus, S.A. (Ventas Guate). Distribución de electrónica de consumo en Guatemala: retail (cadenas grandes), distribución y e‑commerce (Shopify: ventasguate.gt). Moneda base **GTQ**; compras/importaciones frecuentemente en **USD**.

Responde en español, directo, en tablas/listas. Sin saludos ni cierres.

## Odoo: usar SIEMPRE el CLI directo

- Usa `./odoo …` (desde la raíz del repo). **No** uses el MCP de Odoo de terceros salvo que el CLI falle y el usuario lo autorice.
- Credenciales en `.env` (ver `odoo-cli/.env.example`). Si falta `.env` o `./odoo ping` falla, detente e informa; nunca pidas la API key en el chat ni la escribas en archivos versionados.
- Docs completas del CLI: `odoo-cli/README.md`.

### Reglas de uso
1. **Solo lectura por defecto.** `create`/`write`/`unlink`/`call action_*` solo con instrucción explícita del usuario; muestra antes qué registros y valores vas a cambiar y usa `--yes` solo después de su confirmación.
2. **Agrega en el servidor**: para totales usa `./odoo group` (no bajes miles de registros para sumarlos tú).
3. Siempre `-f` con los campos necesarios y `-l` razonable. Para datos grandes: `-F csv > /ruta/archivo.csv`.
4. Fechas: calcula rangos concretos (`YYYY-MM-DD`) a partir de la fecha de hoy; no uses expresiones relativas en el dominio.
5. Si un campo da error, revísalo con `./odoo fields <modelo> <texto>` y **actualiza este archivo** con el nombre correcto.
6. Montos: indica moneda. `amount_total` de documentos en USD está en USD; para consolidar en GTQ usa campos `*_signed` / `balance` (moneda de la compañía).

### Estados clave
| Modelo | Campo | Valores |
|---|---|---|
| `sale.order` | `state` | `draft` cotización · `sent` enviada · `sale` confirmada · `cancel` |
| `purchase.order` | `state` | `draft` RFQ · `sent` · `purchase` confirmada · `cancel` |
| `account.move` | `move_type` | `out_invoice` factura cliente · `out_refund` NC cliente · `in_invoice` factura proveedor · `in_refund` NC proveedor · `entry` |
| `account.move` | `state` | `draft` · `posted` · `cancel` |
| `account.move` | `payment_state` | `not_paid` · `partial` · `in_payment` · `paid` · `reversed` |
| `stock.picking` | `picking_type_code` | `incoming` recepción · `outgoing` despacho · `internal` |

## Consultas frecuentes

Reemplaza `INI` / `FIN` por fechas (`2026-11-01`, `2026-11-30`).

### Ventas
```bash
# Ventas del periodo por mes (sin IVA, GTQ)
./odoo group sale.report -g date:month -a price_subtotal:sum,margin:sum -d '[["state","not in",["draft","sent","cancel"]],["date",">=","INI"],["date","<=","FIN"]]'

# Top clientes
./odoo group sale.report -g partner_id -a price_subtotal:sum,margin:sum -d '[["state","not in",["draft","sent","cancel"]],["date",">=","INI"],["date","<=","FIN"]]' -o "price_subtotal desc" -l 20

# Por vendedor / por equipo (retail, distribución, ecommerce)
./odoo group sale.report -g user_id -a price_subtotal:sum,margin:sum -d '[["state","not in",["draft","sent","cancel"]],["date",">=","INI"]]'
./odoo group sale.report -g team_id -a price_subtotal:sum,margin:sum -d '[["state","not in",["draft","sent","cancel"]],["date",">=","INI"]]'

# Top productos / categorías (unidades, venta, margen)
./odoo group sale.report -g product_id -a product_uom_qty:sum,price_subtotal:sum,margin:sum -d '[["state","not in",["draft","sent","cancel"]],["date",">=","INI"]]' -o "price_subtotal desc" -l 30
./odoo group sale.report -g categ_id -a price_subtotal:sum,margin:sum -d '[["state","not in",["draft","sent","cancel"]],["date",">=","INI"]]'

# Pedidos confirmados pendientes de facturar
./odoo search sale.order -d '[["state","=","sale"],["invoice_status","=","to invoice"]]' -f name,partner_id,date_order,amount_total,user_id -o "date_order asc"

# Cotizaciones abiertas (pipeline de corto plazo)
./odoo search sale.order -d '[["state","in",["draft","sent"]]]' -f name,partner_id,date_order,amount_total,user_id -o "amount_total desc" -l 50
```
Margen % = `margin / price_subtotal`. Si `margin` no existe, el módulo `sale_margin` no está instalado: usar `standard_price` del producto.

### Facturación y cuentas por cobrar
```bash
# Facturación del mes (publicada, neto de NC)
./odoo group account.move -g invoice_date:month -a amount_untaxed_signed:sum,amount_total_signed:sum -d '[["move_type","in",["out_invoice","out_refund"]],["state","=","posted"],["invoice_date",">=","INI"]]'

# Cartera por cobrar por cliente
./odoo group account.move -g partner_id -a amount_residual_signed:sum -d '[["move_type","in",["out_invoice","out_refund"]],["state","=","posted"],["payment_state","in",["not_paid","partial"]]]' -o "amount_residual_signed desc"

# Facturas vencidas (hoy = HOY)
./odoo search account.move -d '[["move_type","=","out_invoice"],["state","=","posted"],["payment_state","in",["not_paid","partial"]],["invoice_date_due","<","HOY"]]' -f name,partner_id,invoice_date,invoice_date_due,amount_total,amount_residual,currency_id -o "invoice_date_due asc" -l 200

# Antigüedad de saldos (detalle a nivel de apunte contable)
./odoo search account.move.line -d '[["account_type","=","asset_receivable"],["parent_state","=","posted"],["reconciled","=",false]]' -f move_name,partner_id,date,date_maturity,amount_residual -l 2000 -F csv
```
Buckets de antigüedad: calcula `HOY - date_maturity` → Corriente, 1‑30, 31‑60, 61‑90, +90.

### Cuentas por pagar
```bash
./odoo group account.move -g partner_id -a amount_residual_signed:sum -d '[["move_type","in",["in_invoice","in_refund"]],["state","=","posted"],["payment_state","in",["not_paid","partial"]]]'
./odoo search account.move -d '[["move_type","=","in_invoice"],["state","=","posted"],["payment_state","in",["not_paid","partial"]],["invoice_date_due","<=","FIN"]]' -f name,partner_id,invoice_date_due,amount_residual,currency_id -o "invoice_date_due asc"
```

### Flujo de caja
```bash
# Cobros y pagos del periodo
./odoo group account.payment -g payment_type,date:week -a amount_company_currency_signed:sum -d '[["state","not in",["draft","canceled","cancel"]],["date",">=","INI"]]'
# Saldos de bancos/caja
./odoo search account.journal -d '[["type","in",["bank","cash"]]]' -f name,type,currency_id,default_account_id
./odoo group account.move.line -g account_id -a balance:sum -d '[["account_id.account_type","=","asset_cash"],["parent_state","=","posted"]]'
```
Proyección 30/60/90: CxC por vencer (por `invoice_date_due`) − CxP por vencer − gastos fijos.

### Inventario
```bash
# Existencias por producto en ubicaciones internas
./odoo group stock.quant -g product_id -a quantity:sum,reserved_quantity:sum -d '[["location_id.usage","=","internal"]]' -l 500

# Valor de inventario (costo)
./odoo search product.product -d '[["type","in",["product","consu"]],["qty_available",">",0]]' -f default_code,name,categ_id,qty_available,standard_price,list_price -l 2000 -F csv

# Quiebres / bajo stock (pronosticado)
./odoo search product.product -d '[["sale_ok","=",true],["virtual_available","<=",0]]' -f default_code,name,qty_available,virtual_available -l 200

# Lento movimiento: productos con stock y sin ventas desde INI
#  1) productos vendidos:  ./odoo group sale.report -g product_id -a product_uom_qty:sum -d '[["state","not in",["draft","sent","cancel"]],["date",">=","INI"]]' -F json
#  2) productos con stock: consulta de valor de inventario
#  → diferencia = lento movimiento; ordenar por qty_available * standard_price
```
Valor inventario = Σ `qty_available × standard_price`. Rotación = costo de venta del periodo / inventario promedio.

### Compras e importaciones
```bash
# Compras confirmadas por proveedor
./odoo group purchase.order -g partner_id -a amount_total:sum -d '[["state","=","purchase"],["date_order",">=","INI"]]'

# OC con mercadería pendiente de recibir
./odoo search purchase.order -d '[["state","=","purchase"],["receipt_status","!=","full"]]' -f name,partner_id,date_order,date_planned,amount_total,currency_id

# Recepciones pendientes
./odoo search stock.picking -d '[["picking_type_code","=","incoming"],["state","not in",["done","cancel"]]]' -f name,partner_id,origin,scheduled_date,state

# Tasa de cambio USD registrada
./odoo search res.currency.rate -d '[["currency_id.name","=","USD"]]' -f name,rate,inverse_company_rate -o "name desc" -l 5
```

### Despachos / logística
```bash
./odoo search stock.picking -d '[["picking_type_code","=","outgoing"],["state","in",["confirmed","waiting","assigned"]]]' -f name,partner_id,origin,scheduled_date,state -o "scheduled_date asc"
```

### CRM (leads con retailers)
```bash
./odoo group crm.lead -g stage_id -a expected_revenue:sum -d '[["type","=","opportunity"],["active","=",true]]'
./odoo search crm.lead -d '[["type","=","opportunity"],["active","=",true]]' -f name,partner_id,stage_id,expected_revenue,probability,user_id,date_deadline -o "expected_revenue desc" -l 50
```

### Clientes y productos
```bash
./odoo call res.partner name_search -k '{"name":"NOMBRE","limit":10}'
./odoo search res.partner -d '[["customer_rank",">",0]]' -f name,vat,phone,email,city,user_id,property_payment_term_id -l 500 -F csv
./odoo search product.template -d '[["default_code","=","SKU"]]' -f name,default_code,barcode,list_price,standard_price,categ_id,qty_available
```

## KPIs estándar (reporte semanal/mensual)
| KPI | Fuente |
|---|---|
| Venta neta y margen % (total, por canal, vendedor, cliente, categoría) | `sale.report` |
| Facturación neta | `account.move` out_invoice − out_refund |
| CxC total, vencida y % vencida; DSO = CxC / venta diaria promedio | `account.move` / `account.move.line` |
| CxP por vencer 30 días | `account.move` in_invoice |
| Caja/bancos | `account.move.line` asset_cash |
| Valor inventario, días de inventario, quiebres, lento movimiento | `product.product`, `stock.quant`, `sale.report` |
| Compras en tránsito | `purchase.order` receipt_status ≠ full |
| Pipeline CRM ponderado = Σ expected_revenue × probability | `crm.lead` |

## Datos de esta instancia (verificado 2026-11-18)
- **Odoo 18.0 Enterprise en Odoo.sh**, protocolo `xmlrpc`. Compañía única: BUYITWITHUS, S.A., moneda GTQ.
- Módulos: sale_margin, sale_stock_margin, pos_sale, pos_sale_margin, crm, purchase, stock, mrp, website_sale, point_of_sale, account_accountant, l10n_gt, l10n_gt_edi (FEL).
- **Ventas confirmadas en `sale.report`**: `["state","not in",["draft","sent","cancel"]]`. Incluye POS (kioscos) porque `pos_sale` está instalado; los pedidos POS aparecen con estados propios (`invoiced`, `paid`, `done`). No usar `state = sale` en `sale.report` porque excluye POS.
- **Marca**: `brand_id` (many2one a `product.brand`, ~132 marcas), existe en `product.template` y `product.product`. Ignorar los campos Studio `x_studio_marca*` / `x_studio_brand_vg` (duplicados/legacy).
  - `sale.report` no acepta `product_id.brand_id` en groupby. Ventas por marca en 2 pasos:
    1. `./odoo group sale.report -g product_id -a price_subtotal:sum,margin:sum,product_uom_qty:sum -d '<dominio>' -l 5000 -F json`
    2. `./odoo search product.product -d '[["id","in",[IDS]]]' -f brand_id -l 5000 -F json` (con `"active_test": false` si hay archivados vía `call … search_read -k`), luego sumar por marca.
  - Filtrar ventas de una marca: `["product_id.brand_id.name","=","MARCA"]` sí funciona en el dominio.
- **Equipos de venta = canales (reconfigurado 2026-11-18)**. Activos:
  | id | Equipo | Líder | Miembros |
  |---|---|---|---|
  | 3 | Retail (tienda física + chats redes) | Luis Hernandez | Luis Hernandez, Ventas Guate Trafalgar (caja Design Center) |
  | 14 | E-commerce (ventasguate.gt / Shopify, sitios web) | Luis Hernandez | Luis Hernandez |
  | 5 | Distribución – Mayoreo | Henry Galindo | Henry, Estuardo Pineda, Luis Guevara, Luis Alfredo Cantoral, Mayra González (captura) |
  | 1 | Distribución – Dropship (plataformas digitales) | Henry Galindo | Fernando Aguilar |
  - Metas mensuales de facturación (`invoiced_target`, sin IVA): Mayoreo Q1,000,000 (mínimo); Dropship Q200,000; Retail y E-commerce sin definir. Avance = facturación neta del mes (`account.move` out_invoice − out_refund, `amount_untaxed_signed`) incluyendo equipos archivados mapeados al canal.
  - Pedidos nuevos: `team_id` ya es el canal. Canal "Distribución" = equipos 5 + 1.
  - Pedidos confirmados antes del 2026-11-18 conservan el equipo viejo (archivado): usar el mapeo histórico de abajo. Para incluir archivados en consultas sobre `crm.team` usar `["active","in",[true,false]]`.
  - Respaldo del estado previo: `ir.attachment` id 356230.
  - **Luis Antonio Chicas Franco** (usuario 18, archivado): su cartera pasó a **Estuardo Pineda** (359) el 2026-11-18 — clientes, cotizaciones abiertas, oportunidades y facturas por cobrar (respaldo `ir.attachment` 356231). Ventas históricas siguen a nombre de Chicas; para análisis de cartera de Estuardo sumar ambos usuarios.
- **Mapeo histórico** (equipos archivados → canal):
  | Canal | Sub-canal | Responsable | Equipos históricos (`crm.team` id) |
  |---|---|---|---|
  | Retail (tienda física) | — | — | Point of Sale (3), Tiendas (13), Kioscos K-02 (8), K-49 (7), K-08 (6), Chats Redes FB/IG/WhatsApp (20) |
  | E-commerce | ventasguate.gt | — | Ventasguate.gt (14), Website (2) |
  | Distribución | Mayoreo | Henry Galindo (gerente, también vende); vendedores Estuardo Pineda, Luis Guevara, Luis Alfredo Cantoral | Henry Galindo (9), Luis Guevara (12), Estuardo Pineda (21), Luis Alfredo Cantoral (17), Distribuciòn y Mayoreo (5, 10), Distribucion Rudy (11, ex-empleado) |
  | Distribución | Dropship / plataformas digitales | Fernando Aguilar, bajo Henry | Fernando Aguilar (1) |
  | Otros | Ex-empleado | Sebastian Hernandez (no labora) | Sebastian Hernandez (18) |
  | No es canal de venta | Contabilidad y logística | Glenda Ixcayau (contadora general); Wilver, Mayra González | GLENDA MIROSLAVA IXCAYAU VICENTE (19) |
  - Reporte por canal: `./odoo group sale.report -g team_id … -F json` y sumar con este mapeo. Vendedor = `user_id`, nunca `team_id`.
  - Usuarios que no son vendedores en `user_id`: Ventas Guate Trafalgar, VG Miraflores 1, VG PORTALES (cajas POS), Bodega Central, Auxiliar de bodega, OdooBot, Mayra González y Wilver (contabilidad/logística), Diego Segura. Pedidos con estos usuarios se atribuyen al canal por `team_id`, no a un vendedor.
- **⚠️ Margen POS en devoluciones está mal calculado** (`pos_sale_margin`): en reembolsos el margen resta el costo en vez de sumarlo (ej. nov-2026: devoluciones −Q71.8k venta, −Q125.3k margen; lo correcto ≈ −Q18.2k). Para margen de Retail: agrupar ventas (`product_uom_qty > 0`) y devoluciones (`< 0`) por separado y corregir devoluciones con `margen_real = 2 × price_subtotal − margin`.
- **⚠️ Error de captura sep-2026**: pedido POS `Ventas Guate Design Center/25487` (2026-09-26) y su reembolso: iPhone 18 Pro Max con cantidad 15,495 (se digitó el precio como cantidad). Margen −Q142M cada uno. Excluir ambos de cualquier análisis de margen.

## Contexto de negocio (no reportar como anomalía)
- **Cancelaciones altas desde oct‑2026**: limpieza intencional de pedidos abiertos sin movimiento. Para análisis de ventas, excluir `cancel` y no tratar ese volumen como pérdida.
- **Margen POS nov‑2026**: el 8% reportado inicialmente estaba distorsionado por el error de margen en devoluciones; real ≈ 22%. Mezcla Apple + combos de liquidación explica margen menor al de distribución. Separar Apple y liquidación antes de concluir.
