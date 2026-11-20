# Títulos de productos en Odoo: "L-" y MAYÚSCULAS

## 2026-11-20 · Corrección "L-" en español (aplicado)
- Causa: el 2026-11-19 los títulos limpios se escribieron en `product.template.name` sin contexto de idioma, así que quedaron solo en **en_US**. Odoo se usa en **es_GT**, y esa traducción conservaba "L-".
- Aplicado: 810 productos; `name` (es_GT) = título limpio de en_US. 0 errores. Quedan 0 nombres es_GT que empiecen con "L-".
- Respaldo: `respaldo_es_GT_2026-11-20.json` (813 registros: es_GT anterior, en_US, capa Shopify).
- Excluidos: 3 coincidencias falsas ("AZUL-VERDE", "CRYSTAL-X", "ERROR - …").
- Regla nueva: todo cambio de `name` en Odoo se escribe en **es_GT y en_US** (`context={"lang": …}`).

## 2026-11-20 · MAYÚSCULAS (propuesta, pendiente de aprobación)
- `propuesta_mayusculas.py` → `propuesta_mayusculas.csv` (estado actual en `mayusculas_actual.json`).
- 2,373 productos activos con nombre en MAYÚSCULAS:
  - A (1,140): en_US ya está bien escrito y tiene el mismo texto → copiar a es_GT.
  - A2 (102): en_US tiene otro texto → solo capitalizar es_GT; en_US no cambia.
  - B (1,131): ambos idiomas en mayúsculas → capitalizar los dos por reglas (marcas, siglas, iPhone, MagSafe, mAh…).
- Solo cambian mayúsculas y espacios: 0 cambios de texto en A2 y B.
