#!/usr/bin/env python3
"""Tipo de cambio oficial Banguat (USD→GTQ) vía webservice SOAP.

Uso:
  python3 banguat.py 2026-11-11                 # una fecha
  python3 banguat.py 2026-11-01 2026-11-11      # rango
Salida: JSON [{"fecha":"YYYY-MM-DD","tc":7.63792}, ...]
"""
import json
import re
import sys
import urllib.request
from datetime import datetime

URL = "https://www.banguat.gob.gt/variables/ws/TipoCambio.asmx"
NS = "http://www.banguat.gob.gt/variables/ws/"


def _soap(fi, ff):
    body = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body>'
        f'<TipoCambioRango xmlns="{NS}"><fechainit>{fi}</fechainit><fechafin>{ff}</fechafin>'
        "</TipoCambioRango></soap:Body></soap:Envelope>"
    )
    req = urllib.request.Request(
        URL,
        data=body.encode(),
        headers={"Content-Type": "text/xml; charset=utf-8", "SOAPAction": f'"{NS}TipoCambioRango"'},
    )
    return urllib.request.urlopen(req, timeout=30).read().decode()


def rango(ini, fin):
    f = lambda s: datetime.strptime(s, "%Y-%m-%d").strftime("%d/%m/%Y")
    xml = _soap(f(ini), f(fin))
    out = []
    for fecha, venta in re.findall(r"<fecha>([\d/]+)</fecha><venta>([\d.]+)</venta>", xml):
        out.append({"fecha": datetime.strptime(fecha, "%d/%m/%Y").strftime("%Y-%m-%d"), "tc": float(venta)})
    return out


if __name__ == "__main__":
    a = sys.argv[1]
    b = sys.argv[2] if len(sys.argv) > 2 else a
    print(json.dumps(rango(a, b)))
