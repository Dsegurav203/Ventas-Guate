# Acción planificada Odoo: "VG: Corregir costo de devoluciones POS"
# Modelo: pos.order.line (Línea de pedido de punto de venta) · Acción: Ejecutar código Python
# Frecuencia: 1 día, 02:00 hora Guatemala
#
# Odoo copia el costo de la venta original con signo positivo en los reembolsos POS,
# lo que duplica la resta en el margen. Solo afecta el reporte de margen; no toca contabilidad.
lines = env['pos.order.line'].search([
    ('qty', '<', 0), ('total_cost', '>', 0),
    ('order_id.session_id.state', '=', 'closed'),
])
fixed = 0
for line in lines:
    orig = line.refunded_orderline_id
    if orig and orig.qty and orig.total_cost >= 0:
        new_cost = line.qty * orig.total_cost / orig.qty
    else:
        new_cost = -abs(line.total_cost)
    line.write({'total_cost': new_cost})
    fixed += 1
if fixed:
    log('Devoluciones POS corregidas: %s' % fixed, level='info')
