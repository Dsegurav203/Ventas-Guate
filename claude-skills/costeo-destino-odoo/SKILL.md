---
name: "costeo-destino-odoo"
description: Registra y valida costos en destino (landed costs / stock.landed.cost) de importaciones en Odoo ventasguate.odoo.com — DAI, flete aéreo/marítimo, gastos de póliza, almacenaje (cuenta ajena), logística, manejo de documentos y ajuste por diferencia de tasa DUCA vs Odoo. USAR SIEMPRE que Diego diga costear, costeo, costo en destino, landed cost, prorratear gastos, "LC/2026", cargar DAI, cargar flete, ajustar costo de importación, o pida el costo unitario final de una recepción importada.
---

# Costeo en destino — Odoo Ventas Guate

## Configuración fija (verificada en Odoo nov-2026)
- Modelo: `stock.landed.cost` · `target_model = picking` · diario `account_journal_id = 8` ("Valoración del inventario")
- Cuenta de líneas: `383` (1.1.3.01.01.04 Inventario en Tránsito)
- `split_method = by_current_cost_price` en todas las líneas
- `vendor_bill_id` vacío (práctica actual)

### Productos de costo (usar `product.product` id)
| Concepto | product_id | Código | Nombre en Odoo |
|---|---|---|---|
| DAI | 7462 | — | DAI |
| Gastos de póliza e importación (agente aduanal) | 7452 | FC000000001 | Fletes de Carga ⚠️ |
| Cuenta ajena almacenaje | 7450 | FI0000000001 | Flete de Importación ⚠️ |
| Flete aéreo internacional | 7451 | FA00000000001 | Flete Aéreo |
| Flete marítimo | 10084 | FM00000000001 | Flete Aereo de Carga (copia) ⚠️ |
| Logística, manejo de documentos, ajuste tasa, otros | 9978 | FG00000000001 | Gastos de Poliza e Importaciòn (copia) ⚠️ |

⚠️ = nombre del producto no coincide con el uso. El campo `name` de la línea es el que manda; siempre escribirlo descriptivo. Si Diego aprueba renombrar estos productos, actualizar esta tabla.

## Reglas de negocio
1. **IVA**: nunca se capitaliza. Facturas FEL locales → costo = total / 1.12. IVA de importación de la DUCA → crédito fiscal, NO va al landed cost.
2. **DAI**: sí se capitaliza, monto en GTQ según DUCA.
3. **Tasa DUCA manda**: la OC/factura se registra a la tasa Odoo del día; la diferencia va como línea de ajuste:
   `ajuste_GTQ = Σ_facturas FOB_USD_i × (TC_DUCA − TC_Odoo_factura_i)` (puede ser negativo; cada factura puede tener tasa Odoo distinta). Producto 9978.
4. **Montos en USD** (flete internacional): convertir a tasa DUCA salvo que la factura indique otra; dejar la tasa en el `name`.
5. Una LC por DUCA/embarque con todas sus recepciones en `picking_ids` (una OC por factura de proveedor).
6. No costear recepciones de Tiendas Design Center como importación salvo instrucción expresa.

## DAI por producto (diferentes % en un mismo embarque)
Odoo prorratea cada línea de costo entre TODOS los productos de las recepciones. El DAI no puede prorratearse así porque cada producto paga 0, 5, 10 o 15 %. Solución: una sola línea DAI con el total de la DUCA y reasignación exacta por movimiento antes de validar.

1. Organización: una OC por factura de proveedor (`partner_ref` = `INV-<n>`). Ya no se separan OC por % DAI. Una LC por DUCA con todas las recepciones en `picking_ids`.
2. De la DUCA (por factura) extraer `dai_items`: `factura`, `inciso` (si la DUCA lo detalla; si no, `"*"`), `dai_pct`, `dai_gtq`. El DAI se calcula sobre valor en aduana (CIF), no FOB → tomar el MONTO de la DUCA, no recalcularlo.
3. Crear la LC con línea DAI = Σ `dai_gtq` (producto 7462) + demás líneas → `compute_landed_cost`.
4. Leer `stock.valuation.adjustment.lines` de la LC con `cost_line_id` = línea DAI: `id, move_id, product_id, former_cost, additional_landed_cost`. Mapear cada `move_id` → `purchase_line_id.order_id.partner_ref` (factura) y `product_id.hs_code` (inciso).
5. `scripts/asignar_dai.py` → asignación por movimiento (proporcional a `former_cost` dentro de cada factura/inciso; residuo al de mayor valor; valida que cuadre con la DUCA).
6. Mostrar tabla `código | factura | inciso | % DUCA | DAI asignado | % efectivo`. Con "sí": `odoo_write` de `additional_landed_cost` en cada línea de ajuste DAI.
7. Releer y verificar Σ ajustes DAI = precio de la línea DAI (±0.01). **Validar inmediatamente**: volver a presionar "Calcular" borra la reasignación.
8. Clasificación: guardar el inciso del producto en `hs_code` cuando la DUCA lo identifique por producto y difiera o esté vacío (con aprobación). Productos con DAI distinto al histórico → alerta (puede ser origen/TLC).

⚠️ Bloqueo técnico (nov-2026): no se pueden crear campos personalizados en `product.template` — el módulo `vtex_connector` tiene `vtex_brand_id` como many2one pero la columna en BD es varchar; cualquier campo nuevo dispara el error `product_template_vtex_brand_id_fkey`. Requiere corrección del desarrollador Odoo.sh. Mientras tanto el % DAI de referencia sale de `hs_code` + DUCAs previas.

## Formato del `name` de cada línea
`<Concepto> <Proveedor> <FEL/doc> (Q<total> sin IVA)` — ejemplos reales:
- `Flete Aereo de Carga Cielo Mar ($991.01 + $75 collect @7.64187) HAWB 320710793483`
- `Cuenta Ajena Almacenaje Correo Directo 220483929 (Q527.30 sin IVA)`
- `Ajuste a tasa DUCA 7.6385 vs Odoo 7.63792 sobre FOB $21,856.80`

## Procedimiento
1. Identificar recepción: `stock.picking` por `origin` = OC, `state = done`. Verificar que no exista ya una LC `done` con esas líneas (buscar `stock.landed.cost` con `picking_ids` = id) → evitar doble costeo.
2. Armar tabla de líneas y correr `scripts/preview_costeo.py` para mostrar % de costeo y costo unitario estimado por SKU.
3. Mostrar a Diego: tabla de líneas + total + % s/FOB GTQ. Esperar "sí".
4. Crear:
   ```
   odoo_create stock.landed.cost {
     "picking_ids": [[6,0,[<picking_id>]]],
     "account_journal_id": 8,
     "target_model": "picking",
     "cost_lines": [[0,0,{"product_id":<id>,"name":"...","price_unit":<GTQ>,"split_method":"by_current_cost_price","account_id":383}], ...]
   }
   ```
5. `odoo_action(model="stock.landed.cost", method="compute_landed_cost", ids=[<lc_id>])` y leer `valuation_adjustment_lines` para confirmar prorrateo. Si hay DAI con % distintos → sección "DAI por producto" antes de validar.
6. Validar con `odoo_action(model="stock.landed.cost", method="button_validate", ids=[<lc_id>])` solo con confirmación explícita.
7. Leer `standard_price` posterior de cada producto y reportar costo anterior → nuevo.

## Alertas automáticas
- % costeo s/FOB fuera de rango (umbrales provisionales hasta calibrar con históricos LC: aéreo > 25%, marítimo > 15%): avisar.
- Línea con monto que termina igual a total con IVA (no dividido entre 1.12): avisar.
- LC en `draft` con más de 3 días: listar como pendiente.
- Productos de la recepción con `standard_price` = 0 antes del costeo: avisar (OC sin precio).
