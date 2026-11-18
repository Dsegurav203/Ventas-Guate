# odoo-cli

CLI directo a Odoo vía su API externa oficial. Sin MCP de terceros, sin dependencias (Python 3.9+ stdlib).

| Protocolo | Versión Odoo | Endpoint |
|---|---|---|
| `json2` | 19+ | `POST /json/2/<modelo>/<método>` + `Authorization: Bearer <API key>` |
| `xmlrpc` | ≤18 | `/xmlrpc/2/object` `execute_kw` |
| `auto` (default) | — | intenta `json2`, cae a `xmlrpc` |

## Setup

1. Odoo → Preferencias de usuario → Seguridad de la cuenta → **Nueva API Key**.
2. `cp odoo-cli/.env.example .env` y completar (también lee `~/.config/odoo-cli/.env`).
3. Desde la raíz del repo: `./odoo <comando>`
4. `odoo ping`

> Usar un usuario con permisos mínimos necesarios. Nunca commitear `.env`.

## Modo solo lectura

`./odoo-ro …` o `ODOO_READONLY=1` / `--readonly`: solo permite métodos de lectura (search, read, read_group, fields_get, name_search…); cualquier otro método falla, también en scripts que importen el CLI. Si existen `ODOO_RO_USER` y `ODOO_RO_API_KEY`, el modo solo lectura usa ese usuario.

## Comandos

```bash
odoo ping
odoo models sale                                   # buscar modelos
odoo fields product.template precio                # campos que contengan "precio"
odoo search sale.order -d '[["state","=","sale"]]' -f name,partner_id,amount_total -o "date_order desc" -l 20
odoo search res.partner -d '[["customer_rank",">",0]]' -F csv > clientes.csv
odoo count account.move -d '[["move_type","=","out_invoice"],["payment_state","!=","paid"]]'
odoo get product.product 12,15 -f name,default_code,qty_available,standard_price
odoo group sale.order -g partner_id -a amount_total:sum -d '[["date_order",">=","2026-01-01"]]'
odoo group account.move -g invoice_date:month -a amount_total:sum -d '[["move_type","=","out_invoice"],["state","=","posted"]]'

# Escritura (pide confirmación; --yes para scripts)
odoo create res.partner '{"name":"Cliente Nuevo","vat":"1234567-8"}'
odoo write product.template 45 '{"list_price":1299}' --yes
odoo unlink crm.lead 88
odoo call sale.order action_confirm --ids 120 --yes
odoo call res.partner name_search -k '{"name":"walmart","limit":5}'
```

Formatos: `-F table` (default) | `json` | `csv`. Dominios/valores aceptan `@archivo.json`.
