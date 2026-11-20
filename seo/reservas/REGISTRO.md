# Colección Reservas iPhone (smart, etiqueta "Reserva")

## 2026-11-20 · Apple Watch Series 11 46mm sin inventario
- Odoo: 0 unidades (product.product 12202 SDL9TC63GR7 y 12203 SM322191JT6).
- Shopify 9433695092949 "Apple Watch Series 11 46mm Jet Black" (sin SKU, inventario manual): quitada la etiqueta "Reserva" e inventario 2 → 0 en Tienda Ventas Guate. Queda activo y agotado: la URL se conserva para SEO.
- Shopify 15480769183957 "…SDL9TC63GR7" (no publicado en la tienda): inventario 1 → 0.
- Respaldo: `respaldo_applewatch_s11_2026-11-20.json`.

## Regla (Diego, 2026-11-20)
- Las fichas "Reserva iPhone …" llevan a propósito un inventario manual (sin SKU, sin ligar a Odoo) para que el cliente pueda reservar. **No** ponerlas en 0 ni reportarlas como descuadre.
- Solo productos que no son reserva (ej. Apple Watch) deben salir de la colección cuando no hay existencia en Odoo.
