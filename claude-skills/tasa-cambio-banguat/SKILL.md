---
name: tasa-cambio-banguat
description: Verifica y corrige la tasa de cambio USD/GTQ en Odoo ventasguate.odoo.com contra la tasa oficial del Banguat, y calcula la diferencia contra la tasa DUCA de una póliza. USAR SIEMPRE que Diego mencione tasa de cambio, tipo de cambio, Banguat, tasa DUCA, diferencial cambiario, "verificar tasa", o antes de confirmar cualquier orden de compra o factura en USD y antes de cualquier costeo de importación.
---

# Verificación de tasa de cambio

## Fuente oficial
`scripts/banguat.py <fecha> [fecha_fin]` → JSON con tasa de referencia Banguat (webservice SOAP `TipoCambioRango`). Probado nov-2026: coincide con Odoo al 5° decimal.

## Odoo
- Modelo `res.currency.rate`, filtro `currency_id.name = USD`, `company_id = 1` (BUYITWITHUS, S.A.).
- Campo útil: `inverse_company_rate` (= GTQ por USD). `rate` = 1/tc.
- Fechas sin día hábil (fin de semana/feriado): Banguat repite la última tasa; Odoo debe tener la misma.

## Procedimiento
1. Determinar fechas: fecha de la OC (`date_approve`), fecha de factura proveedor (`invoice_date`), fecha DUCA.
2. Consultar Banguat para el rango y Odoo para las mismas fechas.
3. Tabla:
   | fecha | Banguat | Odoo | Δ | estado |
   Estado: ✅ igual (|Δ| < 0.00001) · ⚠️ distinta · ❌ falta en Odoo.
4. Si falta o difiere: proponer `odoo_create`/`odoo_write` en `res.currency.rate` con `name`=fecha, `company_id`=1, `currency_id`=2, `inverse_company_rate`=tc. Ejecutar solo con "sí".
5. Si hay DUCA: leer la tasa DUCA del documento y calcular
   `Δ_tasa = TC_DUCA − TC_Odoo_factura` y `ajuste_GTQ = FOB_USD × Δ_tasa`. Entregar el resultado al skill `costeo-destino-odoo` (línea de ajuste, producto 9978).

## Reglas
- Para costeo de importación manda la tasa DUCA; para contabilidad diaria manda Banguat.
- No modificar tasas de fechas con asientos ya publicados sin avisar: cambiar una tasa histórica no re-valúa movimientos ya contabilizados.
- Si el webservice falla: decirlo, no inventar la tasa; pedir a Diego la tasa o reintentar.
