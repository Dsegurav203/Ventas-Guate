# Productos agotados en la Tienda online · 2026-11-21
Solicitado por Diego (2026-11-21): quitar de ventasguate.gt todo lo agotado y sin inventario, sin archivar ni borrar.

## Estado

**NO APLICADO.** La mutación `publishableUnpublish` fue rechazada por la política de seguridad del conector MCP de Shopify ("Unpublishing is blocked to prevent accidental storefront catalog removal"). No se cambió ningún producto: ni canales, ni estado, ni precios, ni inventario. No se intentaron vías alternativas (p. ej. pasar a borrador) porque cambiarían el estado en todos los canales.

## Criterio de candidatos

- `status:active AND inventory_total:<=0`, publicado en Tienda online (`gid://shopify/Publication/164168564949`).
- `tracksInventory = true` y ninguna variante con `inventoryPolicy = CONTINUE` (venta sin stock permitida).
- Excluidos: etiqueta/título "Reserva" (ninguno apareció en la consulta; las reservas tienen stock manual) y gift cards (ninguna).

## Resultado

- Candidatos a ocultar: **234** (respaldo completo en `agotados_ocultados_2026-11-21.json`).
- Excluidos por `CONTINUE` (se pueden vender sin stock, quedan visibles): 6
  - `govee-tv-backlight-3-lite-h60991-55-a-65` (gid://shopify/Product/9254595592405)
  - `iphone-pocket-negro` (gid://shopify/Product/9258219110613)
  - `spidercase-funda-magnetica-para-samsung-galaxy-s25-fe` (gid://shopify/Product/9377151025365)
  - `spidercase-funda-magnetica-para-samsung-galaxy-s25-fe-negro` (gid://shopify/Product/9378100183253)
  - `funda-galaxy-s21-ultra` (gid://shopify/Product/15420254322901)
  - `amazon-alexa-echo-studio-modelo-mas-reciente` (gid://shopify/Product/15439858991317)

### Top 10 marcas (vendor) entre los candidatos

| Vendor | Productos |
|---|---|
| Prodigee | 38 |
| Tucano | 31 |
| ITRONICS GT, SOCIEDAD ANÓNIMA | 17 |
| Nimbus9 | 16 |
| MyBat | 13 |
| LOGiiX | 10 |
| HiFuture | 9 |
| LAUT | 9 |
| Click | 7 |
| JBL | 7 |

De los candidatos, 20 además no tienen imagen (6 de Tucano).

## Con stock y publicados pero SIN imagen (solo reporte, no se cambió)

Total: **37**. Ninguno es Tucano (los Tucano sin imagen están todos agotados y ya están en la lista de candidatos).

| ID | Handle | Título | Vendor | Stock |
|---|---|---|---|---|
| 9613273563349 | hifuture-evo3-smart-band-black | Smartwatch HiFuture Evo3 – Negro | HiFuture | 50 |
| 15439859318997 | combo-8-bombillos-amazon | Combo 8 Bombillos Amazon | Ventas Guate | 47 |
| 9613271236821 | hifuture-sonicore-anc-true-wireless-azul | Audífonos HiFuture SoniCore ANC – Azul | HiFuture | 40 |
| 9613274218709 | hifuture-passion-s-lifestyle-wireless-bocina-latte | Bocina HiFuture Passion S – Latte | HiFuture | 35 |
| 9613273727189 | hifuture-lino-s-compact-wireless-speaker-black | Bocina HiFuture Lino S – Negro | HiFuture | 34 |
| 9613274153173 | hifuture-passion-s-lifestyle-wireless-bocina-black | Bocina HiFuture Passion S – Negro | HiFuture | 33 |
| 9613274284245 | hifuture-sonify2-anc-true-wireless-black | Audífonos HiFuture Sonify2 Open Ear – Negro | HiFuture | 29 |
| 9613274349781 | hifuture-sonify2-anc-true-wireless-navy-blue | Audífonos HiFuture Sonify2 Open Ear – Navy Blue | HiFuture | 24 |
| 15480763711701 | l-itskins-hybrid-spark-galaxy-s23-plus-smoke | ITSkins Hybrid Spark Galaxy S23 Plus Smoke | Ventas Guate | 20 |
| 9613273694421 | hifuture-evo3-smart-band-silver | Smartwatch HiFuture Evo3 – Silver | HiFuture | 18 |
| 9613273858261 | hifuture-lino-s-compact-wireless-speaker-green | Bocina HiFuture Lino S – Verde | HiFuture | 17 |
| 9613273792725 | hifuture-lino-s-compact-wireless-speaker-blue | Bocina HiFuture Lino S – Azul | HiFuture | 16 |
| 9142026797269 | master-case-anpro-redmi-14c-negro | Master Case Anpro Redmi 14C Negro | Master Case | 7 |
| 9142027550933 | master-case-protect-redmi-14c-clear | Master Case Protect Redmi 14C Clear | Master Case | 7 |
| 9142028501205 | master-case-pure-redmi-note-14c-humo | Master Case Pure Redmi Note 14C Humo | Master Case | 7 |
| 9262570668245 | master-case-pure-redmi-note-14c-humo-1 | Master Case Pure Redmi Note 14C Humo (duplicado) | Master Case | 7 |
| 15480762597589 | l-mybat-vidrio-templado-para-camara-galaxy-s20-fan-edition-clear | MyBat Vidrio Templado para Cámara Galaxy S20 Fan Edition Clear | Ventas Guate | 4 |
| 9150018355413 | prodigee-clear-fit-galaxy-a72-negro | Prodigee Clear Fit Galaxy A72 Negro | Prodigee | 2 |
| 15480759124181 | l-uag-lucent-samsung-galaxy-s22-ultra-rosado | UAG Lucent Samsung Galaxy S22 Ultra Rosado | Ventas Guate | 1 |
| 15480759288021 | l-mybat-maverick-antimicrobial-con-holster-galaxy-s22-negro | MyBat Maverick Antimicrobial con Holster Galaxy S22 Negro | Ventas Guate | 1 |
| 15480762794197 | silicon-case-galaxy-a72-turquesa | Silicón Case Galaxy A72 Turquesa | Ventas Guate | 1 |
| 15480763318485 | ballistic-soft-jacket-galaxy-s20-ultra-negro | Ballistic Soft Jacket Galaxy S20 Ultra Negro | Ventas Guate | 1 |
| 15480767578325 | l-torras-upro-magnetic-magsafe-galaxy-s24-negro | Torras Upro Magnetic MagSafe Galaxy S24 Negro | Ventas Guate | 1 |
| 9142034038997 | mybat-pro-stealth-series-galaxy-s22-plus-negro | Mybat pro stealth series galaxy s22 plus negro | MyBat | 1 |
| 9150016127189 | l-prodigee-safetee-transforme-iphone-13-negro | Prodigee Safetee Transforme iPhone 13 Negro | Prodigee | 1 |
| 9150016946389 | l-prodigee-safetee-flow-nigt-11-pro | Prodigee Safetee Flow Night 11 Pro | Prodigee | 1 |
| 9150018322645 | prodigee-clear-fit-galaxy-a53-clear | Prodigee Clear Fit Galaxy A53 Clear | Prodigee | 1 |
| 9150019076309 | prodigee-galaxy-a14-5g-clear-fit-black | Prodigee Galaxy A14 5G Clear Fit Black | Prodigee | 1 |
| 9265496785109 | ipad-air-6-2024-azul | Ipad Air 6 2024 azul | Apple | 1 |
| 9265497571541 | ipad-air-6-m2-128gb-spacegray | Ipad Air 6 M2 128GB Spacegray | Apple | 1 |
| 9265499111637 | ipad-5ta-generacion-32gb-spacegray | Ipad 5ta Generacion 32GB Spacegray | Apple | 1 |
| 9265500913877 | ipad-7ma-generacion-32gb-spacegray | iPad 7ma Generación 32GB Gris Espacial — Seminuevo | Apple | 1 |
| 9265502552277 | ipad-air-2-64gb-spacegray | iPad Air 2 64GB Gris Espacial — Seminuevo | Apple | 1 |
| 9265502748885 | ipad-air-5-64gb-spacegray | Ipad Air 5 64GB Spacegray | Apple | 1 |
| 9474285043925 | zizo-ion-iphone-15-plus-verde-menta | ZIZO Ion iPhone 15 Plus Verde Menta | Zizo | 1 |
| 9474285076693 | zizo-nebula-iphone-15-plus | ZIZO Nebula iPhone 15 Plus | Zizo | 1 |
| 9533698539733 | spigen-essential-cable-usb-a-lightning-2-metros-blanco | Spigen Essential Cable USB a Lightning 2 Metros Blanco | Spigen | 1 |

## Cómo aplicarlo (pendiente)

Opción A — Admin de Shopify (manual, inmediato): Productos → filtro *Inventario: agotado* + *Canal: Tienda online* → seleccionar → Más acciones → **Excluir de canales de venta** → Tienda online. Revisar antes que no se incluyan los 6 productos con `CONTINUE` ni las reservas.

Opción B — API con permiso explícito: por cada `id` del JSON,
```graphql
mutation { publishableUnpublish(id: "<gid>", input: [{publicationId: "gid://shopify/Publication/164168564949"}]) { userErrors { message } } }
```

## Cómo volver a publicar (cuando haya stock)

```graphql
mutation { publishablePublish(id: "<gid>", input: [{publicationId: "gid://shopify/Publication/164168564949"}]) { userErrors { message } } }
```
Hasta ~40 alias por documento. La lista de `id` está en `agotados_ocultados_2026-11-21.json`.
