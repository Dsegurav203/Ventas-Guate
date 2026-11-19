#!/usr/bin/env python3
"""Calcula el sugerido semanal a partir de las respuestas del conector Odoo Ventas Guate (sin credenciales).
Uso: python calcular.py <carpeta_entrada> [--semana 2026-W46]
Lee de la carpeta (ver SKILL.md, Paso 1): ventas_90.json, ventas_28.json, stock.json, transito.json,
borradores.json, proveedores.csv, productos.csv y opcionales consignacion.json, clientes.json.
Escribe en <carpeta>/salida: sugerido.json, po_payload.json, correo.html, Sugerido_Compras_<semana>.xlsx
"""
import csv, io, json, math, sys
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CFG = json.loads((BASE / "config" / "parametros.json").read_text(encoding="utf-8"))
IN = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
OUT = IN / "salida"; OUT.mkdir(exist_ok=True)
HOY = date.today(); iso = HOY.isocalendar()
SEMANA = sys.argv[sys.argv.index("--semana") + 1] if "--semana" in sys.argv else f"{iso[0]}-W{iso[1]:02d}"
TAG = f"SUGERIDO SEMANAL {SEMANA}"


def grupos(nombre):
    f = IN / nombre
    if not f.exists():
        return []
    d = json.loads(f.read_text(encoding="utf-8"))
    return d.get("groups", d) if isinstance(d, dict) else d


def val(g, campo):
    for k in (f"{campo}:sum", campo):
        if k in g and g[k] is not None:
            return float(g[k])
    return 0.0


def pid(g, campo="product_id"):
    v = g.get(campo)
    return v[0] if isinstance(v, list) and v else None


def leer_csv(nombre):
    f = IN / nombre
    if not f.exists():
        return []
    txt = f.read_text(encoding="utf-8")
    try:
        d = json.loads(txt)
    except json.JSONDecodeError:
        d = None
    if isinstance(d, list):  # odoo_export del conector propio: lista de filas {campo: valor}
        return [{k: ("" if v in (False, None) else str(v)) for k, v in r.items()} for r in d]
    if isinstance(d, dict) and "csv" in d:  # formato del conector anterior
        txt = d["csv"]
    return list(csv.DictReader(io.StringIO(txt)))


def col(row, *nombres):
    for n in nombres:
        if n in row and row[n] not in (None, ""):
            return row[n]
    return ""


def num(x):
    try:
        return float(str(x).replace(",", ""))
    except ValueError:
        return 0.0


def marca_de(p):
    for k in ("brand_id", "Marca", "x_studio_marca", "Marca."):
        if col(p, k):
            return col(p, k).strip().upper()
    n = col(p, "name", "Nombre").upper().replace("L-", "", 1).split()
    return "PROTECTION PRO" if n[:2] == ["PROTECTION", "PRO"] else (n[0] if n else "SIN MARCA")


def prm_marca(marca, nombre):
    p = dict(CFG["default"]); p.update(CFG["marcas"].get(marca, {}))
    for palabra, m in p.get("multiplo_por_palabra", {}).items():
        if palabra in nombre.upper():
            p["multiplo"] = m; break
    p["en_config"] = marca in CFG["marcas"]
    return p


# ---------------- carga
v90 = {pid(g): val(g, "product_uom_qty") for g in grupos("ventas_90.json")}
mov90 = {pid(g): int(g.get("__count", 99)) for g in grupos("ventas_90.json")}
v28 = {pid(g): val(g, "product_uom_qty") for g in grupos("ventas_28.json")}
stock = {pid(g): val(g, "quantity") for g in grupos("stock.json")}
reserv = {pid(g): val(g, "reserved_quantity") for g in grupos("stock.json")}
consig = {pid(g): val(g, "quantity") for g in grupos("consignacion.json")}
transito = {pid(g): max(0, val(g, "product_qty") - val(g, "qty_received")) for g in grupos("transito.json")}
borr = {pid(g): val(g, "product_qty") for g in grupos("borradores.json")}
_pf = IN / "pendientes_cliente.json"
pend = {int(k): float(v) for k, v in json.loads(_pf.read_text(encoding="utf-8")).items()} if _pf.exists() else {}
top_cli = {}
for g in grupos("clientes.json"):
    p, q = pid(g), val(g, "product_uom_qty")
    if q > top_cli.get(p, (0, ""))[0]:
        top_cli[p] = (q, (g.get("order_partner_id") or [0, ""])[1])

ult = {}
for r in leer_csv("proveedores.csv"):  # ordenado id desc → el primero es el último comprado
    p = int(num(col(r, "product_id/id", "product_id/.id", "Producto/ID")))
    if p and p not in ult:
        ult[p] = {"partner_id": int(num(col(r, "partner_id/id", "partner_id/.id"))), "proveedor": col(r, "partner_id", "Proveedor"),
                  "currency_id": int(num(col(r, "currency_id/id", "currency_id/.id"))), "moneda": col(r, "currency_id", "Moneda"),
                  "precio": num(col(r, "price_unit", "Precio unitario"))}
nombres = {}
for f in ("ventas_90.json", "stock.json", "ventas_28.json"):
    for g in grupos(f):
        lab = (g.get("product_id") or [0, ""])[1] or ""
        if lab and pid(g) not in nombres:
            nombres[pid(g)] = lab.split("] ", 1)[1] if lab.startswith("[") and "] " in lab else lab
prods, ficha = {}, {}
ultimo = None
for r in leer_csv("productos.csv"):
    p = int(num(col(r, "id", ".id", "ID"))) or ultimo
    if not p:
        continue
    if p != ultimo:
        prods[p] = r
    ultimo = p
    sp = int(num(col(r, "seller_ids/partner_id/id")))
    if sp and sp not in CFG.get("proveedores_excluidos", []) and p not in ficha:
        ficha[p] = {"partner_id": sp, "proveedor": col(r, "seller_ids/partner_id"),
                    "currency_id": int(num(col(r, "seller_ids/currency_id/id"))), "moneda": col(r, "seller_ids/currency_id"),
                    "precio": num(col(r, "seller_ids/price"))}

# ---------------- cálculo
pedir, lento, alertas = [], [], []
for p_id in set(v90) | set(stock) | set(pend):
    if not p_id or p_id not in prods:
        continue
    p = prods[p_id]; nombre = col(p, "name", "display_name", "Nombre") or nombres.get(p_id, "")
    p.setdefault("name", nombre)
    marca = marca_de(p)
    if marca in CFG["marcas_excluidas"] or col(p, "purchase_ok", "Puede ser comprado").lower() in ("false", "0", "no"):
        continue
    prm = prm_marca(marca, nombre)
    st, disp = stock.get(p_id, 0), stock.get(p_id, 0) - reserv.get(p_id, 0)
    q90, q28 = v90.get(p_id, 0), v28.get(p_id, 0)
    r90, r28 = q90 / CFG["dias_ventana_larga"], q28 / CFG["dias_ventana_corta"]
    costo = num(col(p, "standard_price", "Costo"))
    tr, bo = transito.get(p_id, 0), max(0, borr.get(p_id, 0))
    f = {"product_id": p_id, "codigo": col(p, "default_code", "Referencia interna"), "producto": nombre, "marca": marca,
         "stock": round(st), "disponible": round(disp), "consignacion": round(consig.get(p_id, 0)), "transito": round(tr),
         "borradores": round(bo), "venta_28d": round(q28), "venta_90d": round(q90), "costo_gtq": round(costo, 2),
         "lead_time": prm["lead_time_dias"], "multiplo": prm["multiplo"]}
    pc = pend.get(p_id, 0)
    f["pendiente_cliente"] = round(pc)
    if q90 <= 0 and pc <= 0:
        if st > 0:
            f.update(tipo="MUERTO (0 venta 90d)", capital_gtq=round(st * costo, 2)); lento.append(f)
        continue
    if q90 <= 0:
        r90 = r28 = 0.0
    quiebre = disp <= 0 and q28 == 0 and q90 > 0
    v_cuando = max(r28, r90); v_cuanto = r90 if quiebre else 0.6 * r28 + 0.4 * r90
    cub = disp + tr + bo
    cobertura = (cub - pc) / v_cuando if v_cuando else (-1 if cub < pc else 9999)
    f.update(v_dia=round(v_cuanto, 2), cobertura_dias=round(cobertura))
    if cobertura > CFG["sobrestock_dias"]:
        f.update(tipo="SOBRESTOCK", capital_gtq=round(max(0, disp - v_cuanto * CFG["sobrestock_dias"]) * costo, 2)); lento.append(f)
    if cobertura >= prm["lead_time_dias"] + CFG["seguridad_dias"] + CFG["horizonte_revision_dias"] and cub >= pc:
        continue
    falta = pc + v_cuanto * CFG["cobertura_objetivo_dias"] - cub
    if falta <= 0:
        continue
    mult = max(1, prm["multiplo"])
    f["sugerido"] = max(math.ceil(falta / mult) * mult, prm["moq_unidades"])
    f["estado"] = "QUIEBRE" if disp <= 0 else ("PEDIR YA" if cobertura < prm["lead_time_dias"] + CFG["seguridad_dias"] else "PEDIR ESTA SEMANA")
    mot = []
    if quiebre: mot.append("Posible quiebre: sin stock ni venta 28d, se usa v90")
    if not prm["en_config"] or not prm["confirmado"]: mot.append("Lead time por confirmar")
    tq, tc = top_cli.get(p_id, (0, ""))
    if q90 > 20 and tq > 0.5 * q90: mot.append(f"Venta atípica: {tc} = {tq:.0f} de {q90:.0f} u")
    if pc > 0: mot.append(f"Incluye {pc:.0f} u de PO de cliente pendientes")
    if pc <= 0 and mov90.get(p_id, 99) < CFG.get("min_movimientos_90d", 0):
        mot.append(f"Venta concentrada: {mov90[p_id]} movimiento(s) en 90d — pedir solo contra pedido de cliente")
        f["motivos"] = mot; alertas.append(f); continue
    sup = ult.get(p_id)
    if sup and sup["partner_id"] in CFG.get("proveedores_excluidos", []):
        sup = None
    if not sup and p_id in ficha:
        sup = ficha[p_id]; mot.append("Proveedor tomado de la ficha del producto (sin OC reciente válida)")
    f["motivos"] = mot
    if not sup:
        mot.append("SIN PROVEEDOR — no entra a OC"); alertas.append(f); continue
    f.update(sup); f["subtotal"] = round(f["sugerido"] * sup["precio"], 2); pedir.append(f)
    if any(m.startswith(("Posible", "Venta")) for m in mot):
        alertas.append(f)

pedir.sort(key=lambda r: (r["proveedor"], r["marca"], r["cobertura_dias"]))
lento.sort(key=lambda r: -r.get("capital_gtq", 0))

# ---------------- payload OC
grp = defaultdict(list)
for r in pedir:
    grp[(r["partner_id"], r["currency_id"])].append(r)
payload = []
for (partner, curr), ls in grp.items():
    tax = [] if ls[0]["moneda"] == "USD" else [CFG["impuesto_compras_gtq_id"]]
    lt = max(l["lead_time"] for l in ls)
    nota = "".join(f"<li>{l['codigo']} {l['producto'][:60]}: <b>{l['sugerido']}</b> u — disp {l['disponible']}, tránsito {l['transito']}, "
                   f"{l['v_dia']} u/día, cobertura {l['cobertura_dias']} d{(' — ' + '; '.join(l['motivos'])) if l['motivos'] else ''}</li>" for l in ls)
    payload.append({
        "proveedor": ls[0]["proveedor"], "moneda": ls[0]["moneda"], "lineas": len(ls),
        "total": round(sum(l["subtotal"] for l in ls), 2), "marcas": sorted({l["marca"] for l in ls}),
        "vals": {"partner_id": partner, "currency_id": curr, "origin": TAG, "user_id": CFG["comprador_user_id"],
                 "picking_type_id": CFG["picking_type_id"],
                 "order_line": [[0, 0, {"product_id": l["product_id"], "name": f"[{l['codigo']}] {l['producto']}",
                                        "product_qty": l["sugerido"], "price_unit": l["precio"], "taxes_id": [[6, 0, tax]],
                                        "date_planned": f"{(HOY + timedelta(days=lt)).isoformat()} 12:00:00"}] for l in ls]},
        "nota_html": f"<p>Sugerido automático {SEMANA}. OC en borrador: revisar cantidades, MOQ y precio antes de confirmar.</p><ul>{nota}</ul>"})

retenidas = []
_min = CFG.get("minimo_usd_por_proveedor", {})
for o in list(payload):
    m = _min.get(str(o["vals"]["partner_id"]))
    if m and o["total"] < m:
        payload.remove(o); retenidas.append({"proveedor": o["proveedor"], "total": o["total"], "minimo": m, "lineas": o["lineas"]})
tot = defaultdict(float)
for o in payload: tot[o["moneda"]] += o["total"]
capital = sum(r.get("capital_gtq", 0) for r in lento)
filas = "".join(f"<tr><td>{{OC_{i}}}</td><td>{o['proveedor']}</td><td>{', '.join(o['marcas'])}</td><td align='right'>{o['lineas']}</td>"
                f"<td>{o['moneda']}</td><td align='right'>{o['total']:,.2f}</td></tr>" for i, o in enumerate(payload))
alert = "".join(f"<li>{a['codigo']} {a['producto'][:60]}: {'; '.join(a['motivos'])}</li>" for a in alertas[:15])
correo = (f"<p>Sugerido de compras semana {SEMANA}. OC en <b>borrador</b> asignadas a Mayra. Revisar cantidades, MOQ y precios antes de confirmar.</p>"
          f"<p><b>Total:</b> {' · '.join(f'{m} {v:,.2f}' for m, v in tot.items())} | <b>Quiebres:</b> {sum(r['estado']=='QUIEBRE' for r in pedir)} | "
          f"<b>Capital lento/muerto:</b> GTQ {capital:,.2f}</p><table border='1' cellpadding='4' style='border-collapse:collapse'>"
          f"<tr><th>OC</th><th>Proveedor</th><th>Marcas</th><th>Líneas</th><th>Moneda</th><th>Subtotal</th></tr>{filas}</table>"
          f"<p><b>Alertas</b></p><ul>{alert or '<li>Ninguna</li>'}</ul>"
          + ("<p><b>Retenidas por mínimo de proveedor</b></p><ul>" + "".join(f"<li>{r['proveedor']}: USD {r['total']:,.2f} de USD {r['minimo']:,.2f} mínimo ({r['lineas']} líneas)</li>" for r in retenidas) + "</ul>" if retenidas else ""))

json.dump({"semana": SEMANA, "tag": TAG, "pedir": pedir, "lento": lento, "alertas": alertas, "retenidas": retenidas},
          open(OUT / "sugerido.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(payload, open(OUT / "po_payload.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
(OUT / "correo.html").write_text(correo, encoding="utf-8")

# ---------------- Excel
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
wb = Workbook(); H = Font(name="Arial", bold=True, color="FFFFFF"); F = Font(name="Arial", size=10)
fill = PatternFill("solid", fgColor="1F3A5F")
def hoja(ws, cols, rows, keys, anchos=None):
    ws.append(cols)
    for c in ws[1]: c.font, c.fill = H, fill
    for r in rows:
        ws.append([("; ".join(r.get(k, [])) if k == "motivos" else r.get(k, "")) for k in keys])
    for row in ws.iter_rows(min_row=2):
        for c in row: c.font = F
    for i in range(1, len(cols) + 1):
        ws.column_dimensions[ws.cell(1, i).column_letter].width = (anchos or {}).get(i, 13)
    ws.freeze_panes = "A2"
ws = wb.active; ws.title = "Resumen"
hoja(ws, ["Proveedor", "Moneda", "Marcas", "Líneas", "Total"],
     [{"p": o["proveedor"], "m": o["moneda"], "b": ", ".join(o["marcas"]), "l": o["lineas"], "t": o["total"]} for o in payload],
     ["p", "m", "b", "l", "t"], {1: 38, 3: 30})
ws = wb.create_sheet("Pedir")
hoja(ws, ["Proveedor", "Marca", "Código", "Producto", "Estado", "Disponible", "Tránsito", "Borradores", "Consignación", "Venta 28d",
          "Venta 90d", "u/día", "Días cobertura", "Lead time", "Múltiplo", "Sugerido", "Moneda", "Precio", "Subtotal", "Motivos"],
     pedir, ["proveedor", "marca", "codigo", "producto", "estado", "disponible", "transito", "borradores", "consignacion", "venta_28d",
             "venta_90d", "v_dia", "cobertura_dias", "lead_time", "multiplo", "sugerido", "moneda", "precio", "subtotal", "motivos"],
     {1: 30, 4: 50, 20: 50})
for i in range(2, ws.max_row + 1): ws[f"S{i}"] = f"=P{i}*R{i}"
ws = wb.create_sheet("Lento-Muerto")
hoja(ws, ["Tipo", "Marca", "Código", "Producto", "Stock", "Venta 90d", "Días cobertura", "Costo GTQ", "Capital GTQ"], lento,
     ["tipo", "marca", "codigo", "producto", "stock", "venta_90d", "cobertura_dias", "costo_gtq", "capital_gtq"], {1: 20, 4: 50})
ws = wb.create_sheet("Alertas")
hoja(ws, ["Marca", "Código", "Producto", "Disponible", "Venta 90d", "Sugerido", "Motivos"], alertas,
     ["marca", "codigo", "producto", "disponible", "venta_90d", "sugerido", "motivos"], {3: 50, 7: 60})
xlsx = OUT / f"Sugerido_Compras_{SEMANA}.xlsx"; wb.save(xlsx)

print(f"Semana {SEMANA} | OC: {len(payload)} | líneas: {len(pedir)} | alertas: {len(alertas)} | lento/muerto: {len(lento)} | "
      + " · ".join(f"{m} {v:,.2f}" for m, v in tot.items()))
for o in payload:
    print(f"  {o['proveedor'][:38]:<38} {o['moneda']} {o['total']:>12,.2f}  ({o['lineas']} líneas)")
print(f"Archivos: {OUT}")
