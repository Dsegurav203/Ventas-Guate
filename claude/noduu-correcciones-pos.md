# Ventas Guate · Solicitud a Noduu: correcciones de costo en Punto de Venta

**Instancia:** https://ventasguate.odoo.com (Odoo 18 Enterprise, Odoo.sh) · **Compañía:** BUYITWITHUS, S.A.
**Solicita:** Diego Segura · **Fecha:** 21-nov-2026
**Prioridad:** media. Ninguno de los dos casos afecta asientos contables ni facturas FEL; afectan el reporte de margen y la valoración de inventario.

---

## Caso 1. El costo de las devoluciones del POS se registra con signo positivo

### Síntoma
- Al hacer un reembolso en POS, la línea devuelta (`pos.order.line`, `qty < 0`) guarda `total_cost` **positivo**, copiado de la venta original.
- El margen del reembolso resta el costo otra vez, en lugar de revertirlo, así que el margen del período queda subestimado dos veces el costo del producto devuelto.

### Ejemplo
| | Venta | Reembolso (hoy) | Reembolso correcto |
|---|---|---|---|
| qty | 1 | −1 | −1 |
| price_subtotal | 1,000 | −1,000 | −1,000 |
| total_cost | 700 | **700** | **−700** |
| margin | 300 | −1,700 | −300 |

### Qué ya hicimos (temporal)
- Corregimos 839 líneas históricas el 18-nov-2026 con `total_cost = qty × costo_unitario_original` (negativo).
- Acción planificada **`ir.cron` 112 "VG: Corregir costo de devoluciones POS"** (diaria 02:00) que corrige las nuevas después de cerrar la sesión. El código está al final de este documento.

### Qué solicitamos
1. Corregir en código (módulo propio de la instancia) el cálculo de `total_cost` / `margin` de `pos.order.line` para líneas con `qty < 0`: el costo debe quedar con el mismo signo que la cantidad. Si la línea tiene `refunded_orderline_id`, usar el costo unitario de la línea original.
2. Probar en staging de Odoo.sh:
   - venta + reembolso total;
   - reembolso parcial (1 de 3 unidades);
   - reembolso de producto con costo promedio que cambió entre la venta y la devolución.

   En los tres casos se debe cumplir `margin_reembolso = −margin_venta × (qty_devuelta / qty_vendida)`.
3. Al publicar en producción, **avisarnos para archivar el `ir.cron` 112** (no lo archiven antes).

### Verificación
`pos.order.line` con `qty < 0` y `total_cost > 0` → debe dar **0** registros después de cerrar sesión, sin depender del cron.

---

## Caso 2. Producto de descuento del POS con costo e inventario

### Síntoma
- El POS **VG Design Center** (`pos.config` 2) usa como producto de descuento el producto **id 4, código `DISC`**. Está mal configurado:
  - Su nombre es "Protection Pro Ultra 2 Small Film".
  - Está en la categoría "Protección de Pantalla".
  - Su costo es **Q179,513.09**.
- Cada vez que se aplica un descuento global en caja, la línea de descuento toma ese costo. Por ejemplo, el pedido `Ventas Guate Design Center/24538` del 14-feb-2026 tiene un costo de Q179,513 en una línea de −Q107.
- Hay **23 líneas** de `pos.order.line` con `product_id = 4` y `total_cost > 1,000`, que suman **≈ Q6.0M de costo ficticio**. Son 22 líneas de oct-2022 / ene-2023 a Q264,984 cada una y 1 de feb-2026.
- Además, el producto tiene **22 capas de valoración** (`stock.valuation.layer`) que suman **−Q5,744,419** con cantidad −32. Esto distorsiona el reporte de valoración de inventario.
- **Las capas no tienen asiento contable** (`account_move_id` vacío), así que la contabilidad no está afectada.

### Qué solicitamos
1. **Crear un producto de descuento correcto:**
   - Nombre "Descuento POS", código `DESC-POS`.
   - Tipo **Servicio**: sin inventario y sin valoración.
   - Costo 0.
   - Categoría de servicios no valuada.
   - Disponible en POS y con los mismos impuestos que el actual.
2. **Asignarlo** como producto de descuento (`discount_product_id`) en el POS VG Design Center (`pos.config` 2) y en cualquier otro POS activo que use descuento.
3. **Producto 4:**
   - Poner su costo en 0.
   - Renombrarlo "Descuento POS (antiguo, no usar)".
   - Quitarlo del POS y archivarlo cuando el punto 2 esté en producción.
4. **Líneas históricas (solo reporte de margen):** poner `total_cost = 0` en las 23 líneas de `pos.order.line` con `product_id = 4` y `total_cost > 1000`. Ids: 1, 2, 27, 39, 173, 189, 213, 217, 226, 262, 276, 313, 314, 319, 326, 339, 340, 358, 417, 477, 605, 631, 70792.
5. **Valoración de inventario del producto 4:**
   - Llevar el valor acumulado de sus capas a **0 sin generar asiento contable**. Las capas originales no tienen asiento, así que la corrección tampoco debe tenerlo.
   - **No usar el asistente "Revaluar"** si la categoría es de valoración automática, porque publicaría un asiento de ~Q5.7M.
   - Sugerencia: una capa de ajuste por script (cantidad 0, valor +5,744,418.99, sin `account_move_id`), con nota de referencia a esta solicitud.
6. **Revisar también** el producto "Apple Macbook Pro M5 (2025) 14 pulgadas 16GB": su valoración es −Q13,481 con existencia −1. Confirmar si es una venta sin existencia o un error de costo, y decirnos qué recomiendan.

### Verificación
- `pos.config` 2 → `discount_product_id` = nuevo producto de tipo Servicio con costo 0.
- `pos.order.line` con `product_id = 4` y `total_cost > 1000` → **0** registros.
- Suma de `stock.valuation.layer.value` del producto 4 → **0**.
- Venta de prueba en staging con descuento global del 10%: la línea de descuento debe quedar con costo 0 y margen igual a su precio.

---

## Respaldo y entregables que pedimos
- Antes de tocar datos, hacer respaldo de los registros que cambien: exportación o adjunto en Odoo.
- Al terminar, enviarnos:
  - qué módulo o código se instaló;
  - qué registros se cambiaron;
  - los resultados de las verificaciones de arriba.

## Anexo: código del cron temporal 112 (referencia)
```python
lines = env['pos.order.line'].search([
    ('qty', '<', 0), ('total_cost', '>', 0),
    ('order_id.session_id.state', '=', 'closed'),
])
for line in lines:
    orig = line.refunded_orderline_id
    if orig and orig.qty and orig.total_cost >= 0:
        new_cost = line.qty * orig.total_cost / orig.qty
    else:
        new_cost = -abs(line.total_cost)
    line.write({'total_cost': new_cost})
```
