#!/usr/bin/env python3
"""Asigna el DAI de la DUCA a cada movimiento de inventario (stock.move) del landed cost.

Uso: python3 asignar_dai.py input.json  > salida.json

input.json:
{
  "dai_items": [                       # de la DUCA (por factura y/o inciso)
    {"factura": "INV-123", "inciso": "8518.30.00", "dai_pct": 15, "dai_gtq": 2603.94}
  ],
  "moves": [                           # de stock.valuation.adjustment.lines (cost_line DAI)
    {"adj_id": 1, "move_id": 10, "codigo": "8501...", "factura": "INV-123",
     "inciso": "8518.30.00", "former_cost": 12345.67}
  ]
}
Reglas:
- Agrupa por (factura, inciso). Si la DUCA no trae inciso por ítem, usar inciso = "*"
  en dai_items y en moves de esa factura (todo el DAI de la factura se reparte por valor).
- Reparte cada grupo proporcional a former_cost; el residuo de redondeo va al move de mayor valor.
- Moves sin grupo en dai_items => DAI 0 (se reporta como alerta si su factura sí tiene DAI).
Salida: JSON con asignaciones, totales y alertas.
"""
import json
import sys
from collections import defaultdict


def main(path):
    d = json.load(open(path))
    grupos = defaultdict(list)
    for m in d["moves"]:
        grupos[(m["factura"], m.get("inciso") or "*")].append(m)

    asign, alertas = {}, []
    facturas_con_dai = {i["factura"] for i in d["dai_items"] if i["dai_gtq"]}
    usados = set()
    for it in d["dai_items"]:
        key = (it["factura"], it.get("inciso") or "*")
        ms = grupos.get(key)
        if not ms:
            alertas.append(f"DAI sin productos: {key} Q{it['dai_gtq']:.2f}")
            continue
        usados.add(key)
        base = sum(m["former_cost"] for m in ms)
        tot = round(it["dai_gtq"], 2)
        parc = {m["adj_id"]: round(tot * m["former_cost"] / base, 2) for m in ms}
        resto = round(tot - sum(parc.values()), 2)
        mayor = max(ms, key=lambda m: m["former_cost"])["adj_id"]
        parc[mayor] = round(parc[mayor] + resto, 2)
        asign.update(parc)
        pct_real = tot / base * 100 if base else 0
        if it.get("dai_pct") is not None and abs(pct_real - it["dai_pct"]) > 1.5:
            alertas.append(f"{key}: DAI efectivo {pct_real:.2f}% vs {it['dai_pct']}% DUCA (base CIF vs FOB?)")

    for key, ms in grupos.items():
        if key not in usados:
            for m in ms:
                asign.setdefault(m["adj_id"], 0.0)
            if key[0] in facturas_con_dai:
                alertas.append(f"Productos sin DAI asignado en factura con DAI: {key}")

    total_duca = round(sum(i["dai_gtq"] for i in d["dai_items"]), 2)
    total_asig = round(sum(asign.values()), 2)
    if abs(total_duca - total_asig) > 0.01:
        alertas.append(f"DESCUADRE: DUCA Q{total_duca} vs asignado Q{total_asig}")
    print(json.dumps({"asignaciones": asign, "total_duca": total_duca,
                      "total_asignado": total_asig, "alertas": alertas}, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
