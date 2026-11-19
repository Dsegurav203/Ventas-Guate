# Runbook: actualización diaria del Centro de Control Ventas Guate

Tablero: https://claude.ai/artifact/Y5C4JYfL9TuGZp7NwXeJ5y (tipo Dashboard). Solo Ventas Guate; nunca mezclar con Tech Stop (Costa Rica).
Horario: diario 7:39 hora de Guatemala, corte = ayer. Odoo **solo lectura** (`ODOO_READONLY=1`, usuario Claude Lectura).

## Pasos
1. `cd /home/user/Ventas-Guate && ODOO_READONLY=1 python3 odoo-cli/reports/ventasguate_refresh.py --cutoff <AYER> --out /tmp/vg-centro`
   - Código 2 = falló una validación obligatoria → **no publicar**. Avisar a Diego con el detalle de `validaciones` y terminar.
   - Avisos (`aviso: true`) no bloquean; se muestran en la pestaña Auditoría y notas.
2. Subir el archivo: Artifact `publish` con `url` del tablero, `asset: true`, `file_path: /tmp/vg-centro/centro.json`. Anotar el `/_blob/<id>` que devuelve.
3. `python3 odoo-cli/reports/ventasguate_refresh.py writes /_blob/<id> <AYER> /tmp/vg-centro/writes.json` (19 documentos `datasets/*`).
4. Leer versiones actuales: ArtifactData `list` de `datasets` (limit 100). Hacer ArtifactData `batch` con cada escritura de `writes.json` y su `if_version` (los datasets del archivo diario apuntan todos al mismo blob). No tocar `metas`, `fact_mes`, `apple_retail`, `vencidas`, `auditoria` ni `files/index.html`.
5. Borrar el blob anterior (el `url` que tenían los datasets antes del paso 4) con Artifact `delete` + `path` = su id, solo si ya ningún dataset lo usa.
6. Resumen al celular (≤5 líneas): corte, venta del mes vs mes anterior, avance Distribución, días de inventario, avisos nuevos.

## Datasets
- Archivo diario `centro.json` → `{meta, sets}`; cada dataset toma `sets.<id>` con su loader en la página.
- En vivo (consulta a Odoo al abrir): `metas`, `fact_mes`, `apple_retail`, `vencidas`. Archivo de auditoría: `auditoria` (lo actualiza la tarea de auditoría).

## Parámetros (en el script)
| Parámetro | Valor |
|---|---|
| Compañía | BUYITWITHUS, S.A. (id 1), GTQ, IVA 12% |
| Zona horaria | America/Guatemala (UTC−6; medianoche = 06:00 UTC) |
| Canales | mapeo `CANAL` de equipos (ver CLAUDE.md) |
| Apple | `brand_id` 126, familia aparte |
| Consignación | bodegas TOPC, LGUEV, Jorge, Heinz, JenCo, TECH, VAPES, ITRON, Con, TRAV, DISTE |
| Umbrales | sin rotación 90 d; liquidar >180 d; cobertura 15/75 d; meta inventario 60–75 d |

## Validaciones obligatorias
1. Venta neta 90 d por vendedor de tienda = Σ `pos.order.line.price_subtotal`.
2. Costo de venta 90 d de tienda = Σ `pos.order.line.total_cost`.
3. Existencias × costo ≈ `stock.valuation.layer` (±10%), excluyendo valoraciones negativas anómalas (se listan como aviso).
4. Un producto "Sin rotación" sin ventas en 90 d.
Avisos: existencias negativas; líneas de descuento POS con costo > Q1,000.

## Problemas conocidos (2026-11-19)
- Producto de descuento POS `[DISC]` (product.product 4) con costo Q179,513 y valoración −Q5.74M; 23 líneas POS con Q6.0M de costo ficticio (2022–2026). Pendiente decisión de Diego/Glenda; no corregir desde el tablero.
- 3,094 líneas de banco sin conciliar (−Q2.96M) inflan CxP vencida.
