---
name: "importaciones-poliza"
description: Orquesta el ingreso completo de una importación (póliza/DUCA) de Ventas Guate en Odoo ventasguate.odoo.com — desde la factura del proveedor extranjero hasta el costeo en destino validado. USAR SIEMPRE que Diego mencione póliza, DUCA, importación, ingreso de mercadería importada, "ingresar póliza", "costear póliza", embarque, HAWB/BL, agente aduanal (Correo Directo, Cielomar, etc.), DAI, o suba facturas de proveedor extranjero + DUCA + facturas locales de servicios. Coordina los skills tasa-cambio-banguat, ordenes-compra-odoo, creacion-productos-odoo, imagenes-productos-odoo y costeo-destino-odoo en el orden correcto.
---

# Importaciones / Póliza — flujo maestro

Instancia: `ventasguate.odoo.com` (conector Odoo Ventas Guate). NUNCA usar nadu-tech.odoo.com.
Empresa: BUYITWITHUS, S.A. — moneda compañía GTQ.

## Fuente de documentos: carpeta de Dropbox de la póliza (estándar)
- Diego sube TODOS los soportes (DUCA, facturas proveedor, guía, facturas locales FEL/cuenta ajena/flete) a la carpeta de Dropbox de la póliza, nombrada por número de póliza (ej. `Polizas/261-2026-00005402`). No se suben al chat.
- Claude: (1) lista la carpeta con el conector Dropbox, (2) lee cada PDF desde ahí para extraer datos, (3) genera link de descarga temporal (Dropbox `download_link`) y adjunta cada PDF en Odoo con `odoo_attach_from_url(model, record_id, url, filename)` a su OC (`purchase.order`), factura de proveedor (`account.move`) y al landed cost (`stock.landed.cost`: DUCA + gastos locales).
- Si el conector Dropbox no está activo en el chat, pedir activarlo antes de empezar; solo como último recurso aceptar PDFs en el chat.
- Si un documento falta en la carpeta, pedirlo indicando el nombre esperado.

## Documentos de entrada (pedir los que falten, uno solo por vez)
| Documento | Para qué |
|---|---|
| Factura comercial proveedor (USD) | Líneas OC: código, descripción, qty, precio FOB |
| DUCA | Tasa de cambio DUCA, valor FOB/CIF declarado, DAI, IVA importación |
| Guía aérea / BL (HAWB) | Referencia del embarque |
| Facturas FEL locales (agente, almacenadora, flete local) | Costos en destino (netos de IVA) |
| Factura flete internacional (USD) | Flete aéreo/marítimo |

Leer PDFs con el skill `leer-pdf-economico` (texto primero, rasterizar solo si es escaneo).

## Secuencia (no saltar pasos)
1. **Tasa** → skill `tasa-cambio-banguat`: confirmar tasa Banguat del día de la factura/OC en Odoo y extraer tasa DUCA. Registrar ambas.
2. **Productos** → skill `creacion-productos-odoo`: cruzar cada código de la factura contra Odoo (`default_code`, `barcode`, `seller_ids.product_code`). Crear solo los inexistentes, con aprobación.
3. **Imágenes** → skill `imagenes-productos-odoo` para productos nuevos o sin `image_1920`.
4. **Orden de compra** → skill `ordenes-compra-odoo`: una OC por factura de proveedor, en USD, sin impuestos, `partner_ref` = `INV-<n>`. No dividir por % DAI.
5. **Recepción**: la valida bodega (Astrid/Mayra). Claude solo verifica cantidades recibidas vs factura y reporta diferencias. No validar pickings sin orden explícita de Diego.
6. **Costeo** → skill `costeo-destino-odoo`: un `stock.landed.cost` por DUCA con todas las recepciones, gastos prorrateados por valor, DAI reasignado por producto según DUCA (factura/inciso) y ajuste de tasa DUCA.
6b. **Clasificación arancelaria**: con la DUCA por factura, actualizar `hs_code` de los productos (con aprobación) y reportar productos cuyo DAI cambió vs DUCAs anteriores.
7. **Control de precio**: ningún producto de la póliza puede quedar con `list_price` ≤ 1 (se publica en la web). Corregir con el precio Tarifa Pública sugerido del costeo final antes de cerrar.
8. **Cierre**: tabla resumen de costo unitario final por SKU vs costo anterior y margen sobre `list_price`.

## Reglas de control
- Antes de cualquier escritura en Odoo: mostrar tabla de lo que se va a crear/modificar y esperar "sí".
- Cada escritura se registra en la tabla "Bitácora" del resumen final (modelo, id, campo, antes → después) para poder revertir.
- Notas en chatter: solo internas (`mail.mt_note`), nunca mensajes a seguidores externos.
- Si una cifra no cuadra (FOB factura ≠ FOB DUCA, qty recibida ≠ facturada) detenerse y reportar.

## Formato de salida final
```
PÓLIZA <DUCA> | OC <P0xxxx> | Recepción <BD3/IN/xxxxx> | LC <LC/2026/xxxx>
Tasa OC/factura: x.xxxxx | Tasa DUCA: x.xxxxx | Δ: ±Qx.xx
FOB USD | FOB GTQ | Costos destino GTQ | % costeo s/FOB
Tabla SKU: código | descripción | qty | costo unit anterior | costo unit nuevo | precio venta | margen %
Bitácora de cambios
Pendientes / alertas
```
