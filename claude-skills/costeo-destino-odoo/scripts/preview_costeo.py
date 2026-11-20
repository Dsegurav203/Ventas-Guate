#!/usr/bin/env python3
"""Previsualiza prorrateo by_current_cost_price de un landed cost.

Uso:
  python3 preview_costeo.py input.json

input.json:
{
  "tc_odoo": 7.63792,          # tasa con que se registró la factura/OC
  "tc_duca": 7.6385,           # tasa DUCA (manda)
  "lineas_producto": [          # de la OC / recepción
    {"codigo": "850070394239", "desc": "...", "qty": 700, "fob_usd": 2.88}
  ],
  "costos": [                   # montos tal como vienen en el documento
    {"concepto": "DAI", "monto": 2603.94, "moneda": "GTQ", "con_iva": false},
    {"concepto": "Almacenaje Correo Directo", "monto": 527.30, "moneda": "GTQ", "con_iva": true},
    {"concepto": "Flete aereo", "monto": 1066.01, "moneda": "USD", "con_iva": false}
  ],
  "incluir_ajuste_tasa": true
}
"""
import json
import sys

IVA = 1.12


def main(path):
    d = json.load(open(path))
    tc_o, tc_d = d["tc_odoo"], d["tc_duca"]
    lineas = d["lineas_producto"]
    fob_usd = sum(l["qty"] * l["fob_usd"] for l in lineas)
    base_gtq = fob_usd * tc_o  # valor con que entró a inventario

    costos = []
    for c in d["costos"]:
        m = c["monto"]
        if c.get("moneda", "GTQ") == "USD":
            m = m * tc_d
        if c.get("con_iva"):
            m = m / IVA
        costos.append((c["concepto"], round(m, 2)))
    if d.get("incluir_ajuste_tasa", True):
        aj = round(fob_usd * (tc_d - tc_o), 2)
        costos.append((f"Ajuste a tasa DUCA {tc_d} vs Odoo {tc_o} sobre FOB ${fob_usd:,.2f}", aj))

    total = round(sum(m for _, m in costos), 2)
    print("LINEAS DE COSTO (GTQ, netas de IVA)")
    for n, m in costos:
        print(f"  {m:>12,.2f}  {n}")
    print(f"  {total:>12,.2f}  TOTAL")
    print(f"\nFOB USD {fob_usd:,.2f} | FOB GTQ {base_gtq:,.2f} | % costeo s/FOB {total / base_gtq * 100:.2f}%\n")

    print(f"{'codigo':<16}{'qty':>8}{'unit GTQ':>12}{'+costeo':>10}{'unit final':>12}")
    for l in lineas:
        val = l["qty"] * l["fob_usd"] * tc_o
        asig = total * val / base_gtq
        u0 = l["fob_usd"] * tc_o
        u1 = (val + asig) / l["qty"]
        print(f"{l['codigo']:<16}{l['qty']:>8}{u0:>12.4f}{u1 - u0:>10.4f}{u1:>12.4f}")


if __name__ == "__main__":
    main(sys.argv[1])
