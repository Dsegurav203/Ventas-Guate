# Tablero de Distribución para Henry: instrucciones

Henry lo crea desde **su** cuenta de claude.ai. Todas las cifras se consultan en vivo en Odoo con **su** usuario y API key, así que solo ve lo que sus permisos de Odoo le dejan ver. Al abrir el tablero los números se actualizan; no hace falta una tarea programada.

## 1. Requisitos (una sola vez)
1. Tener cuenta en la organización de Claude de Ventas Guate, con su correo `distribucion@ventasguate.com`.
2. Tener el conector **Odoo Ventas Guate** agregado y conectado (Configuración → Conectores) con su login de Odoo y su API key. Para probarlo, escribir en un chat: *"usa odoo_whoami"*. Debe responder "Henry Galindo".
   - Su API key se genera en Odoo: Mi perfil → Seguridad de la cuenta → Nueva clave API. **No la pegue en el chat**; solo va en el conector.

## 2. Crear el tablero
Abrir un chat nuevo en claude.ai y pegar completo el texto de abajo. Claude va a pedir permiso para usar el conector de Odoo: responder **"Permitir siempre"**.

```
Crea un tablero (artifact de tipo Dashboard) llamado "Distribución Ventas Guate" con datos EN VIVO del conector "Odoo Ventas Guate" (solo lectura: no crees ni modifiques nada en Odoo). Moneda GTQ, montos sin IVA, en español. Usa fechas concretas AAAA-MM-DD a partir de hoy en hora de Guatemala (filtros "inicio" = primer día del mes, "hoy", "inicio_ant" = primer día del mes anterior, "hace90", "hace365").

Definiciones fijas:
- Equipos Mayoreo (crm.team id): 5, 9, 10, 11, 12, 17, 21. Dropship: 1. Distribución = Mayoreo + Dropship.
- Metas mensuales de facturación: Mayoreo Q1,000,000 (mínimo), Dropship Q200,000 (campo invoiced_target de los equipos 5 y 1).
- Venta confirmada = modelo sale.report con dominio ["state","not in",["draft","sent","cancel"]] y team_id en los equipos de Distribución.
- Facturación = account.move con move_type in [out_invoice, out_refund], state = posted, campo amount_untaxed_signed.
- La cartera de Luis Antonio Chicas pasó a Estuardo Pineda; sus ventas históricas siguen a nombre de Chicas.
- Margen mínimo de alerta: 15%.

Pestañas y contenido:
1. Metas: facturación del mes de Mayoreo, Dropship y Distribución contra su meta, % de avance, ritmo del mes (días transcurridos / días del mes) y proyección al cierre. Gráfica de barras con la línea de ritmo.
2. Vendedores: por user_id, venta y margen % del mes, del mes anterior y de los últimos 90 días; # pedidos y ticket promedio (sale.order state sale). Tabla ordenada por venta del mes.
3. Clientes: top 20 por venta de 12 meses (sale.report por partner_id) con última fecha de compra; lista de clientes que compraron en los últimos 12 meses y no tienen pedido en 60 días (alerta) o 90 días (crítico), con su vendedor; alerta si un cliente pasa del 30% de la venta de 90 días.
4. Pipeline: cotizaciones abiertas (sale.order state draft/sent de esos equipos) por vendedor con monto y días de antigüedad; oportunidades CRM activas (crm.lead type opportunity) por etapa y vendedor con expected_revenue y ponderado (× probability); pedidos confirmados pendientes de facturar (invoice_status = to invoice).
5. Margen: margen % por categoría (sale.report categ_id) y por vendedor en 90 días; pedidos confirmados del mes con margin_percent < 0.15 (sale.order: name, partner_id, user_id, amount_untaxed, margin_percent). Separar Apple (marca brand_id "Apple") porque su margen esperado es 6–10%.
6. Cobranza: facturas de cliente publicadas con payment_state not_paid/partial vencidas (invoice_date_due < hoy) cuyo team_id es de Distribución: total por vendedor (invoice_user_id) y antigüedad 1–30, 31–60, 61–90, +90; los 10 clientes a cobrar primero (saldo × (1 + días/30)). Actividades abiertas de tipo "Cobranza semanal" (mail.activity sobre res.partner) por responsable: vencidas y por vencer.
7. Inventario para vender: existencias disponibles (stock.quant en ubicaciones internas que yo pueda ver, quantity − reserved_quantity) de los 50 productos más vendidos por Distribución en 90 días; marcar quiebres (disponible ≤ 0); inventario en consignación por cliente; compras en tránsito (purchase.order state purchase con receipt_status pending/partial).
8. Despachos: entregas pendientes (stock.picking outgoing en estado confirmed/waiting/assigned) de pedidos de Distribución, y cuántas están atrasadas (scheduled_date < hoy).

Reglas:
- Agrega en Odoo con odoo_group; no bajes miles de registros. Usa límites razonables.
- Gerencia primero: arriba de todo, tarjetas con avance de Distribución, venta del mes vs mes anterior, margen % del mes, cartera vencida del equipo y cotizaciones abiertas.
- Si una consulta da "Access Denied", muéstralo en la sección como "Sin permiso en Odoo" y sigue con el resto.
- Al terminar, dime qué consultas corrieron y cuánto tardó cada pestaña.
```

## 3. Uso diario
- Abrir el tablero desde claude.ai (menú Artifacts). Se actualiza solo al abrirlo.
- Para cambios: abrir el chat del tablero y pedirlos en palabras ("agrega la meta por vendedor", "quita Dropship de la gráfica").
- Para compartirlo con un vendedor: menú Compartir → permiso "Ver". Cada persona ve los datos según **sus** permisos de Odoo, con su propio conector.

## 4. Notas para Diego
- El tablero no ve caja, bancos ni cuentas por pagar si Henry no los pide; tus datos financieros siguen solo en el Centro de Control.
- Las actividades "Cobranza semanal" existen desde la primera corrida del lunes 23-nov; antes de esa fecha esa sección sale vacía.
- Si se definen metas por vendedor, se agregan como un dato fijo en el prompt o en Odoo, y Henry pide: "agrega meta por vendedor: Henry Q…, Luis Guevara Q…".
