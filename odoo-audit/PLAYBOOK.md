# Auditoría de Odoo — Ventas Guate

Instancia: https://ventasguate.odoo.com (Odoo 18 Enterprise, Odoo.sh). Acceso: **CLI en solo lectura `./odoo-ro`** (no MCP).
Moneda: GTQ. Zona horaria: America/Guatemala.
Responsable: Diego Segura (CEO). Aprobaciones contables: Glenda Ixcayau.

## Reglas para todos los agentes

1. **Solo lectura, sin correcciones.** Ningún agente (ni el supervisor) crea, modifica, cancela, valida ni borra registros en Odoo. Usar únicamente `./odoo-ro`, que bloquea cualquier escritura.
   El objetivo es **detalle de errores, alertas y temas por área**. Cada hallazgo dice qué revisar o decidir y quién; la corrección la decide y ejecuta un humano.
   Tipos: **error** (dato o registro incorrecto), **alerta** (riesgo de dinero o control violado), **tema** (proceso o tendencia a revisar).
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

1. Lanzar los agentes **en paralelo** con la herramienta Agent (`subagent_type` = nombre del agente; si el tipo no existe, `general-purpose` con el contenido del archivo del agente como instrucciones).
   Pasar a cada uno la fecha de hoy, el modo (**alertas diarias** o **completa semanal**, ver abajo) y "revisa desde el último corte y el estado actual".
2. **Verificar** cada hallazgo ALTA y MEDIA con una consulta propia con `./odoo-ro`.
   Descartar lo que no se reproduzca y anotarlo como "descartado en verificación".
3. Comparar contra el reporte anterior (si existe): marcar cada hallazgo como **NUEVO**, **SIGUE** (con días abierto) o **RESUELTO**.
4. Publicar el reporte (ver abajo) y terminar con un resumen de 3 líneas.
5. Si un agente falla o no responde, el reporte lo dice explícitamente. Nunca inventar resultados.

## Frecuencia

| Modo | Cuándo | Agentes | Qué revisa |
|---|---|---|---|
| **Alertas diarias** | Martes a sábado, 6:10 | seguridad, inventario, ventas-facturacion, credito-cartera | Solo lo ocurrido desde el día anterior (ajustes de inventario, cambios de permisos, ventas bajo costo o con descuento alto, notas de crédito, pedidos de clientes sobre límite). Reportar solo ALTA y MEDIA nuevas. Si no hay nada, el reporte dice "sin alertas" en una línea. |
| **Completa semanal** | Lunes, 6:10 | los 6 | Todo el checklist de cada agente, estado actual completo, tendencias contra la semana anterior y estado NUEVO / SIGUE / RESUELTO de cada hallazgo. |

La cobranza semanal (proceso aparte, ver `CLAUDE.md`) corre el lunes 7:00 y usa los hallazgos de crédito y cartera de esta auditoría como contexto.

## Reporte

Publicar como Artifact con título **"Auditoría Odoo"** (un solo artifact; arriba el último corte, indicando si es diario o semanal):
- Buscar con `Artifact action=list` un artifact con ese título. Si existe, `read` y republicar en la misma URL; si no, crear uno nuevo.
- Mantener el reporte de hoy arriba y un historial resumido (fecha, # ALTA/MEDIA/BAJA) de los últimos 30 días.

Estructura:
1. **Resumen ejecutivo**: 3–5 viñetas, lo más importante primero, con montos.
2. **Decisiones pendientes**: tabla (qué revisar o decidir, quién, registros, monto, severidad). Son propuestas: nadie las ejecuta automáticamente.
3. **Hallazgos por área**: tabla por agente (severidad, tipo error/alerta/tema, estado NUEVO/SIGUE/RESUELTO, detalle, evidencia).
4. **Métricas del día**: cartera total, vencido, crédito comprometido sin facturar, ventas facturadas ayer, ajustes de inventario ayer.
5. **Control del equipo**: qué agentes corrieron, cuántas consultas, qué se descartó en verificación, qué no se pudo revisar.

Idioma: español. Sin saludos ni cierres.

## Datos de referencia

- Usuarios autorizados como **Inventario / Administrador** (únicos que pueden aplicar ajustes): Diego Segura (id 2), Glenda Ixcayau (id 27), SOPORTE NODUU (id 229) y Mayra González (id 30, desde 2026-11-18). Sus ajustes se reportan como métrica, no como alerta, salvo montos > Q25,000 en un día (MEDIA, para que Glenda valide contra el físico).
- Grupo Inventario / Administrador: `res.groups` id 47. Shopify / Manager (id 148) implica id 47.
- Grupo "Consulta de costos de inventario" (`res.groups` id 154): solo lectura de valoración, sin ajustes. Autorizado: Henry Galindo (id 7). Reportar cualquier otro miembro.
- Grupo "Bloqueo de creación de productos" (`res.groups` id 156, reglas `ir.rule` 639 y 640): miembros no pueden crear productos. Deben estar Bodega Central (17) y Auxiliar de bodega (28). ALTA si faltan, si las reglas se desactivan o si cualquiera de los dos crea un `product.template`.
- Grupo "Costeo de importaciones (pólizas)" (`res.groups` id 157): crea/valida costos en destino y ve valoración, sin ajustes. Autorizados: Luis Hernández (id 8) y Auxiliar Contable / Wilber (id 14). Reportar cualquier otro miembro.
- Usuarios autorizados a crear productos (grupo 140): Diego, Henry Galindo, Luis Hernández, Auxiliar Contable, Mayra González. Bodega (17, 28) bloqueada con grupo 156.
- Menú Inventario / Reportes (`ir.ui.menu` 289) abierto a Inventario / Usuario (46); Valoración (317) solo grupos 47 y 154. Si se revierte tras una actualización, reportarlo como ALTA.
- Obitech (res.partner 49): 14 pedidos entregados sin facturar (~Q226,418) pendientes de validación contra FEL por Glenda. Reportar como SIGUE hasta que se resuelva.
- Canales de venta, metas mensuales, margen POS y cartera de Chicas → Estuardo: ver "Datos de esta instancia" en `CLAUDE.md`.
- Devoluciones POS con `total_cost` positivo (`./odoo-ro count pos.order.line -d '[["qty","<",0],["total_cost",">",0]]'`): debe ser 0 si la tarea nocturna de corrección existe en Odoo. Desde 2026-11-19 la acción planificada `ir.cron` 112 los corrige cada noche: solo reportar si quedan líneas de sesiones cerradas hace más de 1 día (MEDIA), o si el cron 112 está inactivo o falló (ALTA).
- **Administradores autorizados** (Ajustes / Derechos de acceso, `base.group_system` / `base.group_erp_manager`): Diego (2), Glenda (27), SOPORTE NODUU (229) y **María Fernanda Paredes (15, esposa y dueña: cuenta de emergencia; no reportar como inactiva ni proponer desactivarla)** y **Mayra González (30), autorizada por Diego el 2026-11-18** (recomendaciones de bodegas: grupo 160 y reglas 643/644 aprobados). Cualquier otro usuario con esos grupos: ALTA. Fase 1 aplicada el 2026-11-18 (respaldo `ir.attachment` 356233).
- **Plantilla de usuario por defecto** (`base.default_user`, res.users 3): debe tener solo "Usuario interno" y grupos técnicos, ningún grupo de administrador de módulo. Si aparece alguno: ALTA (todo usuario nuevo nacería como administrador).
- **Alta de usuarios:** solo Diego o Glenda crean usuarios y asignan un rol definido. Usuario nuevo creado por otra persona, o con grupos de administrador de módulo sin aprobación: ALTA.
