# Auditoría diaria de Odoo — Ventas Guate

Instancia: https://ventasguate.odoo.com (conector **Odoo MCP**).
Moneda: GTQ. Zona horaria: America/Guatemala.
Responsable: Diego Segura (CEO). Aprobaciones contables: Glenda Ixcayau.

## Reglas para todos los agentes

1. **Solo lectura.** Ningún agente crea, modifica, cancela, valida ni borra registros en Odoo.
   Toda corrección se propone en el reporte y la ejecuta un humano o Claude con aprobación explícita de Diego.
2. Cada hallazgo lleva evidencia verificable: modelo, IDs/nombres de registro, montos y el dominio de búsqueda usado.
3. No reportar sospechas sin datos. Si una consulta falla, se reporta como "no revisado" con el error.
4. Montos en quetzales con separador de miles (Q12,345.67).
5. Severidad:
   - **ALTA**: dinero en riesgo > Q25,000, control violado (permisos, ajustes no autorizados), cliente sobre crédito con vencido.
   - **MEDIA**: dinero en riesgo Q5,000–Q25,000, procesos atrasados > 30 días.
   - **BAJA**: limpieza de datos, registros viejos sin impacto en dinero.

## Equipo

| Agente | Archivo | Área |
|---|---|---|
| Credito y cartera | `.claude/agents/odoo-credito-cartera.md` | Límites de crédito, vencidos, pedidos sin facturar que inflan crédito |
| Ventas y facturación | `.claude/agents/odoo-ventas-facturacion.md` | Entregado sin facturar, cotizaciones viejas, márgenes, descuentos |
| Inventario | `.claude/agents/odoo-inventario.md` | Ajustes de inventario, stock negativo, costos en cero, entregas atrasadas |
| Contabilidad y tesorería | `.claude/agents/odoo-contabilidad.md` | Banco sin conciliar, asientos en borrador, cuentas por pagar, duplicados |
| Compras | `.claude/agents/odoo-compras.md` | Órdenes sin recibir, recepciones sin factura de proveedor |
| Seguridad y permisos | `.claude/agents/odoo-seguridad.md` | Grupos de administrador, usuarios nuevos, cambios de permisos |

## Procedimiento del supervisor (sesión principal)

1. Lanzar los 6 agentes **en paralelo** con la herramienta Agent (`subagent_type` = nombre del agente).
   Pasar a cada uno la fecha de hoy y "revisa ayer y el estado actual".
2. **Verificar** cada hallazgo ALTA y MEDIA con una consulta propia en Odoo (record_search/record_get).
   Descartar lo que no se reproduzca y anotarlo como "descartado en verificación".
3. Comparar contra el reporte anterior (si existe): marcar cada hallazgo como **NUEVO**, **SIGUE** (con días abierto) o **RESUELTO**.
4. Publicar el reporte (ver abajo) y terminar con un resumen de 3 líneas.
5. Si un agente falla o no responde, el reporte lo dice explícitamente. Nunca inventar resultados.

## Reporte diario

Publicar como Artifact con título **"Auditoría Odoo Diaria"**:
- Buscar con `Artifact action=list` un artifact con ese título. Si existe, `read` y republicar en la misma URL; si no, crear uno nuevo.
- Mantener el reporte de hoy arriba y un historial resumido (fecha, # ALTA/MEDIA/BAJA) de los últimos 30 días.

Estructura:
1. **Resumen ejecutivo**: 3–5 viñetas, lo más importante primero, con montos.
2. **Acciones que requieren aprobación de Diego**: tabla (acción propuesta, registros, monto, severidad).
3. **Hallazgos por área**: tabla por agente (severidad, estado NUEVO/SIGUE/RESUELTO, detalle, evidencia).
4. **Métricas del día**: cartera total, vencido, crédito comprometido sin facturar, ventas facturadas ayer, ajustes de inventario ayer.
5. **Control del equipo**: qué agentes corrieron, cuántas consultas, qué se descartó en verificación, qué no se pudo revisar.

Idioma: español. Sin saludos ni cierres.

## Datos de referencia

- Usuarios autorizados como **Inventario / Administrador** (únicos que pueden aplicar ajustes): Diego Segura (id 2), Glenda Ixcayau (id 27), SOPORTE NODUU (id 229).
- Grupo Inventario / Administrador: `res.groups` id 47. Shopify / Manager (id 148) implica id 47.
- Obitech (res.partner 49): 14 pedidos entregados sin facturar (~Q226,418) pendientes de validación contra FEL por Glenda. Reportar como SIGUE hasta que se resuelva.
