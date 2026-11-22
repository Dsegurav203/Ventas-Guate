# Google Merchant Center: carga de GTIN en variantes de Shopify (PROPUESTA)

Fecha: 2026-11-22 · Estado: **solo propuesta, nada aplicado** · Tienda: ventasguate.gt

## Fuente

- `productVariants(first:100, query:"product_status:active")` paginado: **2005 variantes** de 2,004 productos activos (`productVariantsCount` ignora el filtro y devuelve 3,067; `productsCount(status:active)` = 2,004).
- Datos crudos: `variantes_barcodes.json`. Propuesta: `barcodes_propuesta.json`.
- Candidato = SKU sin `L`/`l` inicial, solo dígitos, longitud 8/12/13/14 y dígito verificador GS1 válido (pesos 3/1 desde la derecha).

## Conteos por caso

| Caso | Descripción | Variantes | Aplicables | Bloqueadas por alerta |
|---|---|---|---|---|
| a | Barcode vacío y SKU es GTIN válido → cargar | 417 | 366 | 51 |
| b | Barcode no GTIN (código interno) y SKU GTIN válido → reemplazar | 1332 | 1314 | 18 |
| c | Barcode ya es GTIN válido → nada | 59 | — | — |
| d | Sin GTIN válido → nada, anotado | 197 | — | — |
| | **Total** | **2005** | **1680** (1,679 productos) | **69** |

Caso (b): 1,263 barcodes actuales alfanuméricos (`L_APP3_HPT_BK`, `PO07HS541SW16BK0106`, `iPh17P-6 9-…`, `JBLGO4BLKAM`, `CL-LAT-…`, `LGX-…`) y 69 numéricos cortos/no GTIN (`53568`, `15693`, `581456`).

Caso (c): 10 con barcode = SKU; 49 con GTIN válido **distinto** del SKU (p. ej. CLCKR `4251993301582` vs SKU `850052633905`, JBL `1200130006685`). No se tocan, pero conviene revisar cuál es el correcto.

Caso (d) desglose:

- seminuevo ITR: 106
- numérico 5 díg. checksum/longitud no válida: 28
- sin SKU: 24
- SKU interno no numérico: 16
- numérico 11 díg. checksum/longitud no válida: 12
- numérico 13 díg. checksum/longitud no válida: 5
- numérico 4 díg. checksum/longitud no válida: 2
- numérico 12 díg. checksum/longitud no válida: 1
- numérico 14 díg. checksum/longitud no válida: 1
- numérico 7 díg. checksum/longitud no válida: 1
- numérico 8 díg. checksum/longitud no válida: 1
- 9 de ellos son recuperables a mano (UPC de 11 dígitos sin el 0 inicial, p. ej. Solo `30918012673` → `030918012673`; `VG8809848204685` → `8809848204685`). Marcados en `nota` con "revisar manualmente"; no se proponen automáticamente.

## Alertas (excluidas de la carga automática, `aplicar=false`)

| Alerta (bloqueante) | Variantes |
|---|---|
| GTIN duplicado en otro producto activo | 64 |
| GTIN ya es barcode de otra variante | 5 |
| combo | 2 |
| combo: GTIN de un componente | 2 |

- **GTIN duplicado**: el mismo SKU-GTIN está en 2 productos activos (fichas duplicadas Master Case, MyBat, Urbanista, Nimbus9, Prodigee Glow S26 Ultra, Baseus, Mageasy, etc.). Merchant Center marcaría conflicto; resolver primero (archivar el duplicado).
- **Combos** (`Combo Echo Dot … + 3 Bombillos`): llevan el GTIN del Echo Dot solo; un combo no debe usar el GTIN de un componente (en Google: `identifier_exists=no` o `is_bundle`).
- 49 variantes con SKU `L…` (liquidación) sí se proponen (alerta informativa): el GTIN real es el SKU sin `L`.

## 10 ejemplos

| Caso | Producto | SKU | Barcode actual | GTIN propuesto | Tipo | Aplicar |
|---|---|---|---|---|---|---|
| b | LAUT Huex Protect AirPods Pro3 Black | `4895206947350` | `L_APP3_HPT_BK` | `4895206947350` | EAN | sí |
| b | Smartwatch HiFuture Edge – Negro | `6972576182456` | `PO07HS541SW16BK0106` | `6972576182456` | EAN | sí |
| b | JBL Authentics-300 Bluetooth 5.1 y WiFi Alexa incorporado | `050036396271` | `JBLAUTH300BLKAM` | `050036396271` | UPC | sí |
| b | Prodigee Blackout iPhone 18 Pro Max/17 Pro Max Negro | `810192100804` | `iPh17P-6 9-BLOT-BLK` | `810192100804` | UPC | sí |
| a | Smartwatch HiFuture Active Adventure – Silver | `6972576182012` | (vacío) | `6972576182012` | EAN | sí |
| a | MyBat Pro Vidrio Templado para Apple Watch 7 41mm | `L885126697538` | (vacío) | `885126697538` | UPC | no (GTIN duplicado en otro producto activo; SKU con prefijo L) |
| a | Master Case Protect Xiaomi 14T Pro Clear | `6978421710058` | (vacío) | `6978421710058` | EAN | no (GTIN duplicado en otro producto activo) |
| c | CLCKR Diamante iPhone 15 Negro | `850052633905` | `4251993301582` | — | — | no — SKU distinto: 850052633905 |
| d | iPhone 8 Plus 64GB Gris Espacial Seminuevo | `ITR-IP8PLUS-64GB-GRISESPACIAL` | (vacío) | — | — | no — seminuevo ITR |
| d | Solo Bedfor Universal Tablet 5.5 a 8.5 Pulgadas Negro | `30918012673` | `UNS2101-10` | — | — | no — numérico 11 díg. checksum/longitud no válida; posible UPC con 0 inicial: 030918012673 (revisar manualmente) |

## Esquema verificado (graphql_schema, Admin 2026-10)

- `ProductVariant.barcodes: ProductVariantBarcodeConnection!` → nodos `ProductVariantBarcode { type: BarcodeType, value: String! }`. Ya no existe el campo `barcode` (singular) en `ProductVariant`.
- `BarcodeInput { type: BarcodeType, value: String! }`. `type` es opcional: `null` = sin tipo, el valor se guarda tal cual (así están hoy todos). Con tipo, Shopify **valida el formato**.
- `BarcodeType`: `ASIN, EAN, GTIN, ISBN, NS_PID, UPC`. `GTIN` acepta 8, 12, 13 y 14 dígitos.
- `ProductVariantsBulkInput.barcodes: [BarcodeInput!]` — **"Replaces the entire barcode set"**; máx. 20 por variante; no se puede mandar `barcode` y `barcodes` a la vez.
- `productVariantsBulkUpdate(productId: ID!, variants: [ProductVariantsBulkInput!]!, allowPartialUpdates: Boolean)` — una llamada por producto.

## Mutación propuesta

```graphql
mutation SetGtin($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
  productVariantsBulkUpdate(productId: $productId, variants: $variants) {
    productVariants { id sku barcodes(first: 5) { nodes { type value } } }
    userErrors { field message code }
  }
}
```
Variables (ejemplo LAUT, caso b):
```json
{
  "productId": "gid://shopify/Product/15480769675477",
  "variants": [
    { "id": "gid://shopify/ProductVariant/68045036060885",
      "barcodes": [ { "type": "EAN", "value": "4895206947398" } ] }
  ]
}
```
- Tipo: `UPC` para 12 dígitos, `EAN` para 13, `GTIN` para 8/14 (campo `tipo_propuesto`). Alternativa equivalente: `GTIN` para todos.
- Como `barcodes` reemplaza la lista, el código interno actual se pierde en Shopify (queda respaldado en `barcode_actual`). Si se quiere conservarlo: `[{type:EAN, value:GTIN}, {type:null, value:"L_APP3_HPT_P"}]` (el GTIN primero). Recomendación: solo el GTIN, para que Google no tome el código interno.
- Volumen: 1,680 variantes en ~1,680 productos → ~1,680 llamadas (lotes con pausa por rate limit) o una `bulkOperationRunMutation` con JSONL.
- Orden sugerido: 1) prueba con 3 variantes (1 UPC, 1 EAN, 1 con `L`) y verificar en Merchant Center; 2) resto en lotes de 100 con respaldo `barcodes_respaldo_<fecha>.json` y registro en `APLICADO.md`.

## Riesgos

1. **Sincronización Odoo → Shopify**: los códigos internos actuales probablemente vienen del campo `barcode` de Odoo vía el conector. Si una exportación del conector actualiza barcode, podría revertir el GTIN. Verificar antes (no se pudo consultar Odoo desde esta sesión: sin resolución DNS a ventasguate.odoo.com) y, si aplica, cargar también el GTIN en `product.product.barcode` de Odoo o desactivar esa sincronización.
2. **POS / lectores**: si en tienda se escanea el código interno en Shopify POS, dejará de encontrarse. (El POS principal es Odoo, pero confirmar.)
3. **SKU = GTIN no garantiza que sea del producto**: el checksum solo valida formato. Hay 49 casos (c) donde barcode y SKU son GTIN distintos, señal de que algunos SKU pueden ser de otra variante/color. Muestrear marcas grandes (Prodigee, Click, Nimbus9, HiFuture, LAUT) contra fuente oficial (LAUT: EAN coincide con itslaut.com).
4. **Duplicados** (64 variantes) y **combos** (2): excluidos; resolver primero o Merchant Center los rechaza/fusiona.
5. Validación por tipo: con `type` definido Shopify valida; si algún valor falla, `userErrors`. Usar `allowPartialUpdates: false` (por producto es 1 variante, sin impacto).
6. Seminuevos `ITR-` (106) y SKUs internos: sin GTIN → en Google usar `identifier_exists = no` (o marca + MPN) para que no queden limitados.
