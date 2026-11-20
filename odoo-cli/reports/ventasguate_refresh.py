#!/usr/bin/env python3
"""Actualización diaria del Centro de Control Ventas Guate (solo lectura en Odoo).

Uso:  ODOO_READONLY=1 python3 odoo-cli/reports/ventasguate_refresh.py --cutoff AAAA-MM-DD --out DIR
Genera un JSON por dataset ({rows, meta}) en DIR y validaciones.json. Sale con código 2 si una
validación obligatoria falla: en ese caso NO se publica (regla del runbook).
Adaptado del modelo Tech Stop (Costa Rica) a la operación unificada de Guatemala.
"""
import argparse, collections, datetime as dt, json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import odoo_cli as oc  # noqa: E402

TZ = "America/Guatemala"
CANAL = {3: "Retail", 13: "Retail", 6: "Retail", 7: "Retail", 8: "Retail", 20: "Retail", 14: "E-commerce", 2: "E-commerce",
         5: "Mayoreo", 9: "Mayoreo", 10: "Mayoreo", 11: "Mayoreo", 12: "Mayoreo", 17: "Mayoreo", 18: "Mayoreo", 21: "Mayoreo",
         1: "Dropship"}
APPLE_BRAND = 126
CONSIG = {"TOPC", "LGUEV", "Jorge", "Heinz", "JenCo", "TECH", "VAPES", "ITRON", "Con", "TRAV", "DISTE"}
UMBRAL = {"sin_rotacion_dias": 90, "liquidar_dias": 180, "cobertura_baja": 15, "cobertura_alta": 75}
SALE_OK = ["state", "not in", ["draft", "sent", "cancel"]]


def client():
    e = os.environ
    ro = bool(e.get("ODOO_RO_API_KEY"))
    o = oc.Odoo(e["ODOO_URL"], e["ODOO_DB"], e["ODOO_RO_USER"] if ro else e["ODOO_USER"],
                e["ODOO_RO_API_KEY"] if ro else e["ODOO_API_KEY"], "xmlrpc")
    o.readonly = True
    return o


def rel(v, i=0):
    return v[i] if isinstance(v, list) and v else (None if i == 0 else "")


def family(complete_name):
    parts = [p.strip() for p in (complete_name or "").split("/") if p.strip()]
    if parts and parts[0].lower() in ("all", "todos", "todo"):
        parts = parts[1:]
    if not parts:
        return "Sin categoría"
    f = parts[0].replace("√°", "á").replace("√©", "é").replace("√≠", "í").replace("√≥", "ó").replace("√∫", "ú")
    return f[:1].upper() + f[1:]


DATASETS = {
    "corte": ("Corte de datos", "Fecha de corte, hora de generación y tipo de cambio del archivo diario."),
    "ventas_dia": ("Venta diaria por canal (90 días)", "Venta sin IVA, margen y tickets por día y canal (pedidos y POS)."),
    "mensual": ("Venta mensual por canal", "Venta sin IVA y margen por mes y canal desde enero del año anterior."),
    "comparativos": ("Comparativos al mismo corte", "Mes en curso contra mes anterior y mismo mes del año anterior al mismo día; YTD contra año anterior."),
    "familias": ("Margen por familia (90 días)", "Venta, margen y unidades por familia de categoría; Apple separado."),
    "marcas": ("Margen por marca (90 días)", "Las 40 marcas con más venta en 90 días."),
    "inventario": ("Inventario y rotación por producto", "Existencia (propia y consignación), costo, valor, ventas 90 días, cobertura, días sin venta, ABC y estado."),
    "inventario_bodegas": ("Valor de inventario por bodega", "Valor al costo por bodega propia o de consignación."),
    "vendedores": ("Vendedores por área (90 días)", "Tienda por empleado del POS; Distribución y E-commerce por vendedor del pedido."),
    "dias_horas": ("Venta de tienda por día y hora", "Venta sin IVA del POS por día de la semana y hora de Guatemala (90 días)."),
    "ecommerce_top": ("Top productos e-commerce (90 días)", "Los 15 productos con más venta en ventasguate.gt y sitio web."),
    "logistica": ("Operaciones de bodega pendientes", "Despachos, recepciones y traslados abiertos y cuántos están atrasados."),
    "compras_transito": ("Compras en tránsito", "Órdenes de compra confirmadas con mercadería pendiente de recibir."),
    "ajustes_30d": ("Ajustes de inventario (30 días)", "Movimientos de ajuste de inventario validados por usuario."),
    "cxc_cxp": ("Cuentas por cobrar y por pagar por tramo", "Saldos abiertos de clientes y proveedores por tramo de vencimiento (GTQ)."),
    "flujo": ("Flujo proyectado 30/60/90", "Caja actual más cobros menos pagos por vencer en cada horizonte."),
    "contabilidad_pendientes": ("Pendientes contables", "Asientos en borrador por tipo y líneas de banco sin conciliar."),
    "finanzas_bancos": ("Saldos de bancos y caja", "Saldo contable por diario de banco o caja (GTQ)."),
    "validaciones": ("Validaciones del archivo", "Cuadres obligatorios antes de publicar y avisos de calidad de datos."),
}


def writes(blob, corte, out):
    w = [{"op": "set", "collection": "datasets", "doc_id": k, "data": {"title": t, "description": d,
          "source": {"kind": "file", "url": blob, "name": "centro.json", "format": "json"},
          "updated": {"at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "by": f"Actualización diaria (corte {corte})"},
          "schedule": "Diario 7:39 hora de Guatemala, con corte al día anterior", "staleAfterHours": 50}} for k, (t, d) in DATASETS.items()]
    json.dump(w, open(out, "w"), ensure_ascii=False)
    print(f"{len(w)} escrituras en {out}")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "writes":  # writes <blob_url> <corte> <archivo>
        return writes(*sys.argv[2:5]) or 0
    ap = argparse.ArgumentParser()
    ap.add_argument("--cutoff", required=True, help="último día incluido (normalmente ayer)")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    o = client()
    ctx = {"tz": TZ}
    cut = dt.date.fromisoformat(a.cutoff)
    nxt = cut + dt.timedelta(days=1)
    d90 = cut - dt.timedelta(days=89)
    d365 = cut - dt.timedelta(days=364)
    mes0 = cut.replace(day=1)
    ytd0 = cut.replace(month=1, day=1)
    prev_y0 = ytd0.replace(year=ytd0.year - 1)
    utc = lambda d: f"{d.isoformat()} 06:00:00"  # medianoche Guatemala = 06:00 UTC (sin horario de verano)
    os.makedirs(a.out, exist_ok=True)
    out = {}

    def G(model, groupby, aggs, domain, **kw):
        return o.call(model, "read_group", domain=domain, fields=aggs, groupby=groupby, lazy=False, context=ctx, **kw)

    # ---------- catálogo
    cats = {c["id"]: family(c["complete_name"]) for c in o.call("product.category", "search_read", domain=[], fields=["complete_name"], limit=2000)}
    teams = {t["id"]: t for t in o.call("crm.team", "search_read", domain=[["active", "in", [True, False]]], fields=["name", "invoiced_target", "active"])}
    fx = o.call("res.currency.rate", "search_read", domain=[["currency_id.name", "=", "USD"]], fields=["name", "inverse_company_rate"], order="name desc", limit=1)

    # ---------- ventas diarias y mensuales por canal (sale.report incluye POS; sin IVA)
    rango = [SALE_OK, ["date", ">=", utc(min(d90, mes0.replace(year=mes0.year - 1)))], ["date", "<", utc(nxt)]]
    dia = G("sale.report", ["date:day", "team_id"], ["price_subtotal:sum", "margin:sum"], [SALE_OK, ["date", ">=", utc(d90)], ["date", "<", utc(nxt)]])
    ventas_dia = collections.defaultdict(lambda: {"venta": 0.0, "margen": 0.0})
    for r in dia:
        day = r["__range"]["date:day"]["from"][:10]
        k = (day, CANAL.get(rel(r["team_id"]), "Otros"))
        ventas_dia[k]["venta"] += r["price_subtotal"] or 0
        ventas_dia[k]["margen"] += r["margin"] or 0
    out["ventas_dia"] = [{"fecha": d, "canal": c, "venta": round(v["venta"], 2), "margen": round(v["margen"], 2)} for (d, c), v in sorted(ventas_dia.items())]

    tick = collections.Counter()
    for r in G("sale.order", ["date_order:day", "team_id"], ["amount_untaxed:sum"], [["state", "in", ["sale", "done"]], ["date_order", ">=", utc(d90)], ["date_order", "<", utc(nxt)]]):
        tick[(r["__range"]["date_order:day"]["from"][:10], CANAL.get(rel(r["team_id"]), "Otros"))] += r["__count"]
    for r in G("pos.order", ["date_order:day"], ["amount_total:sum"], [["state", "not in", ["draft", "cancel"]], ["amount_total", ">", 0], ["date_order", ">=", utc(d90)], ["date_order", "<", utc(nxt)]]):
        tick[(r["__range"]["date_order:day"]["from"][:10], "Retail")] += r["__count"]
    for row in out["ventas_dia"]:
        row["tickets"] = tick.get((row["fecha"], row["canal"]), 0)

    mens = collections.defaultdict(lambda: {"venta": 0.0, "margen": 0.0})
    for r in G("sale.report", ["date:month", "team_id"], ["price_subtotal:sum", "margin:sum"], [SALE_OK, ["date", ">=", utc(prev_y0)], ["date", "<", utc(nxt)]]):
        m = r["__range"]["date:month"]["from"][:7]
        k = (m, CANAL.get(rel(r["team_id"]), "Otros"))
        mens[k]["venta"] += r["price_subtotal"] or 0
        mens[k]["margen"] += r["margin"] or 0
    out["mensual"] = [{"mes": m, "canal": c, "venta": round(v["venta"], 2), "margen": round(v["margen"], 2)} for (m, c), v in sorted(mens.items())]
    # mismo corte de días del mes anterior y del año anterior (comparativo MTD justo)
    def mtd(d0, d1):
        s = collections.defaultdict(float)
        for r in G("sale.report", ["team_id"], ["price_subtotal:sum"], [SALE_OK, ["date", ">=", utc(d0)], ["date", "<", utc(d1)]]):
            s[CANAL.get(rel(r["team_id"]), "Otros")] += r["price_subtotal"] or 0
        return s
    pm0 = (mes0 - dt.timedelta(days=1)).replace(day=1)
    py0 = mes0.replace(year=mes0.year - 1)
    import calendar
    def same_day(d0, day):
        return d0.replace(day=min(day, calendar.monthrange(d0.year, d0.month)[1])) + dt.timedelta(days=1)
    cmp_ = {"mtd": mtd(mes0, nxt), "mes_anterior_mismo_corte": mtd(pm0, same_day(pm0, cut.day)),
            "anio_anterior_mismo_corte": mtd(py0, same_day(py0, cut.day)), "ytd": mtd(ytd0, nxt),
            "ytd_anio_anterior": mtd(prev_y0, cut.replace(year=cut.year - 1) + dt.timedelta(days=1))}
    canales = ["Mayoreo", "Dropship", "Retail", "E-commerce", "Otros"]
    out["comparativos"] = [{"canal": c, **{k: round(v.get(c, 0.0), 2) for k, v in cmp_.items()}} for c in canales]

    # ---------- productos 90 días (ABC, marcas, familias, Apple)
    prod90 = G("sale.report", ["product_id"], ["price_subtotal:sum", "margin:sum", "product_uom_qty:sum"], [SALE_OK, ["date", ">=", utc(d90)], ["date", "<", utc(nxt)]], limit=20000)
    pids = [rel(r["product_id"]) for r in prod90 if r["product_id"]]
    lastsale = {rel(r["product_id"]): r["date"] for r in G("sale.report", ["product_id"], ["date:max"], [SALE_OK, ["date", ">=", utc(d365)], ["date", "<", utc(nxt)]], limit=20000) if r["product_id"]}
    stock = {}
    for r in G("stock.quant", ["product_id", "location_id"], ["quantity:sum"], [["location_id.usage", "=", "internal"], ["quantity", "!=", 0]], limit=50000):
        p, loc = rel(r["product_id"]), rel(r["location_id"], 1) or ""
        wh = loc.split("/")[0]
        s = stock.setdefault(p, {"propio": 0.0, "consignacion": 0.0, "por_bodega": collections.Counter()})
        s["consignacion" if wh in CONSIG else "propio"] += r["quantity"] or 0
        s["por_bodega"][wh] += r["quantity"] or 0
    allp = sorted(set(pids) | set(stock))
    pinfo = {}
    for i in range(0, len(allp), 1000):
        for p in o.call("product.product", "search_read", domain=[["id", "in", allp[i:i + 1000]], ["active", "in", [True, False]]],
                        fields=["default_code", "name", "brand_id", "categ_id", "standard_price", "is_storable", "type"], limit=1000):
            pinfo[p["id"]] = p
    p90 = {rel(r["product_id"]): r for r in prod90 if r["product_id"]}

    tot90 = sum(r["price_subtotal"] or 0 for r in prod90) or 1
    acc, abc = 0.0, {}
    for r in sorted(prod90, key=lambda r: -(r["price_subtotal"] or 0)):
        acc += r["price_subtotal"] or 0
        abc[rel(r["product_id"])] = "A" if acc / tot90 <= 0.8 else ("B" if acc / tot90 <= 0.95 else "C")

    fam, marca = collections.defaultdict(lambda: [0.0, 0.0, 0.0]), collections.defaultdict(lambda: [0.0, 0.0, 0.0])
    for pid, r in p90.items():
        pi = pinfo.get(pid, {})
        is_apple = rel(pi.get("brand_id")) == APPLE_BRAND
        f = "Apple" if is_apple else cats.get(rel(pi.get("categ_id")), "Sin categoría")
        for bucket, k in ((fam, f), (marca, rel(pi.get("brand_id"), 1) or "Sin marca")):
            bucket[k][0] += r["price_subtotal"] or 0; bucket[k][1] += r["margin"] or 0; bucket[k][2] += r["product_uom_qty"] or 0
    out["familias"] = [{"familia": k, "venta": round(v[0], 2), "margen": round(v[1], 2), "margen_pct": round(v[1] / v[0], 4) if v[0] else None, "unidades": round(v[2])}
                       for k, v in sorted(fam.items(), key=lambda x: -x[1][0])]
    out["marcas"] = [{"marca": k, "venta": round(v[0], 2), "margen": round(v[1], 2), "margen_pct": round(v[1] / v[0], 4) if v[0] else None, "unidades": round(v[2])}
                     for k, v in sorted(marca.items(), key=lambda x: -x[1][0])[:40]]

    # ---------- inventario y rotación
    inv = []
    for pid in allp:
        pi = pinfo.get(pid)
        if not pi or not (pi.get("is_storable") or pi.get("type") == "product"):
            continue
        s = stock.get(pid, {"propio": 0.0, "consignacion": 0.0})
        q = s["propio"] + s["consignacion"]
        u90 = (p90.get(pid) or {}).get("product_uom_qty") or 0
        ls = lastsale.get(pid)
        dias_sin = (cut - dt.date.fromisoformat(ls[:10])).days if ls else None
        cob = round(q / (u90 / 90), 1) if u90 > 0 else None
        if q <= 0 and u90 <= 0:
            continue
        estado = ("Liquidar" if q > 0 and (dias_sin is None or dias_sin > UMBRAL["liquidar_dias"]) else
                  "Sin rotación" if q > 0 and u90 == 0 else
                  "Quiebre" if q <= 0 < u90 else
                  "Alta rotación" if cob is not None and cob < UMBRAL["cobertura_baja"] else
                  "Sobre-stock" if cob is not None and cob > UMBRAL["cobertura_alta"] else "Normal")
        inv.append({"producto_id": pid, "codigo": pi.get("default_code") or "", "producto": pi["name"], "marca": rel(pi.get("brand_id"), 1) or "Sin marca",
                    "familia": cats.get(rel(pi.get("categ_id")), "Sin categoría"), "abc": abc.get(pid, "Sin venta"),
                    "existencia": round(q, 2), "consignacion": round(s["consignacion"], 2), "costo_unit": round(pi.get("standard_price") or 0, 2),
                    "valor": round(max(q, 0) * (pi.get("standard_price") or 0), 2), "unidades_90d": round(u90, 2),
                    "cobertura_dias": cob, "dias_sin_venta": dias_sin, "estado": estado})
    out["inventario"] = sorted(inv, key=lambda r: -r["valor"])
    porb = collections.defaultdict(float)
    for pid, s in stock.items():
        c = (pinfo.get(pid) or {}).get("standard_price") or 0
        for wh, q in s["por_bodega"].items():
            porb[wh] += max(q, 0) * c
    out["inventario_bodegas"] = [{"bodega": k, "tipo": "Consignación" if k in CONSIG else "Propia", "valor": round(v, 2)} for k, v in sorted(porb.items(), key=lambda x: -x[1]) if v > 0]

    # ---------- vendedores por área
    vend = []
    for r in G("report.pos.order", ["employee_id"], ["price_subtotal_excl:sum", "margin:sum"], [["date", ">=", utc(d90)], ["date", "<", utc(nxt)], ["state", "not in", ["draft", "cancel"]]]):
        vend.append({"area": "Retail", "vendedor": rel(r["employee_id"], 1) or "Sin vendedor", "venta_90d": round(r["price_subtotal_excl"] or 0, 2), "margen_90d": round(r["margin"] or 0, 2), "lineas": r["__count"]})
    dvend = collections.defaultdict(lambda: [0.0, 0.0, 0])
    for r in G("sale.report", ["user_id", "team_id"], ["price_subtotal:sum", "margin:sum"], [SALE_OK, ["date", ">=", utc(d90)], ["date", "<", utc(nxt)], ["team_id", "in", [k for k, v in CANAL.items() if v in ("Mayoreo", "Dropship", "E-commerce")]]]):
        k = (CANAL.get(rel(r["team_id"])), rel(r["user_id"], 1) or "Sin vendedor")
        dvend[k][0] += r["price_subtotal"] or 0; dvend[k][1] += r["margin"] or 0; dvend[k][2] += r["__count"]
    for (area, v), x in dvend.items():
        vend.append({"area": "Distribución" if area in ("Mayoreo", "Dropship") else area, "subarea": area, "vendedor": v, "venta_90d": round(x[0], 2), "margen_90d": round(x[1], 2), "lineas": x[2]})
    for r in vend:
        r["margen_pct"] = round(r["margen_90d"] / r["venta_90d"], 4) if r["venta_90d"] else None
    out["vendedores"] = sorted(vend, key=lambda r: (r["area"], -r["venta_90d"]))

    # ---------- días y horas (tienda), hora de Guatemala
    dh = G("report.pos.order", ["date:day_of_week", "date:hour_number"], ["price_subtotal_excl:sum"], [["date", ">=", utc(d90)], ["date", "<", utc(nxt)], ["state", "not in", ["draft", "cancel"]]])
    out["dias_horas"] = [{"dia_semana": int(r["date:day_of_week"]), "hora": int(r["date:hour_number"]), "venta": round(r["price_subtotal_excl"] or 0, 2), "lineas": r["__count"]} for r in dh]

    # ---------- e-commerce (equipos 14 y 2): top productos 90d
    eco = G("sale.report", ["product_id"], ["price_subtotal:sum", "product_uom_qty:sum"], [SALE_OK, ["date", ">=", utc(d90)], ["date", "<", utc(nxt)], ["team_id", "in", [14, 2]]], orderby="price_subtotal desc", limit=15)
    out["ecommerce_top"] = [{"producto": rel(r["product_id"], 1), "venta": round(r["price_subtotal"] or 0, 2), "unidades": round(r["product_uom_qty"] or 0)} for r in eco]

    # ---------- logística y bodega
    now = f"{nxt.isoformat()} 06:00:00"
    log = []
    for code, label in (("outgoing", "Despachos"), ("incoming", "Recepciones"), ("internal", "Traslados")):
        for r in G("stock.picking", ["picking_type_id"], ["id:count"], [["picking_type_code", "=", code], ["state", "in", ["confirmed", "waiting", "assigned"]]]):
            late = o.call("stock.picking", "search_count", domain=[["picking_type_id", "=", rel(r["picking_type_id"])], ["state", "in", ["confirmed", "waiting", "assigned"]], ["scheduled_date", "<", now]])
            log.append({"tipo": label, "operacion": rel(r["picking_type_id"], 1), "pendientes": r["__count"], "atrasados": late})
    out["logistica"] = sorted(log, key=lambda r: -r["atrasados"])
    out["compras_transito"] = [{"oc": p["name"], "proveedor": rel(p["partner_id"], 1), "fecha_esperada": (p["date_planned"] or "")[:10], "monto": p["amount_untaxed"], "moneda": rel(p["currency_id"], 1)}
                               for p in o.call("purchase.order", "search_read", domain=[["state", "=", "purchase"], ["receipt_status", "!=", "full"]],
                                               fields=["name", "partner_id", "date_planned", "amount_untaxed", "currency_id"], order="date_planned asc", limit=50)]
    adj = G("stock.move", ["create_uid"], ["product_uom_qty:sum"], [["is_inventory", "=", True], ["state", "=", "done"], ["date", ">=", utc(cut - dt.timedelta(days=29))]])
    out["ajustes_30d"] = [{"usuario": rel(r["create_uid"], 1), "movimientos": r["__count"], "unidades": round(r["product_uom_qty"] or 0)} for r in adj]

    # ---------- contabilidad y finanzas
    banks = G("account.move.line", ["journal_id"], ["balance:sum"], [["account_id.account_type", "=", "asset_cash"], ["parent_state", "=", "posted"]])
    fin = [{"concepto": rel(r["journal_id"], 1), "grupo": "Bancos y caja", "monto": round(r["balance"] or 0, 2)} for r in banks]
    def buckets(move_types, sign=1):
        rows = o.call("account.move", "search_read", domain=[["move_type", "in", move_types], ["state", "=", "posted"], ["payment_state", "in", ["not_paid", "partial"]]],
                      fields=["invoice_date_due", "amount_residual_signed"], limit=20000)
        b = collections.OrderedDict((k, 0.0) for k in ["Vencido +90", "Vencido 61-90", "Vencido 31-60", "Vencido 1-30", "Vence 0-30", "Vence 31-60", "Vence 61-90", "Vence +90"])
        for r in rows:
            dd = (dt.date.fromisoformat(r["invoice_date_due"]) - nxt).days if r["invoice_date_due"] else 0
            k = ("Vence 0-30" if dd <= 30 else "Vence 31-60" if dd <= 60 else "Vence 61-90" if dd <= 90 else "Vence +90") if dd >= 0 else \
                ("Vencido 1-30" if dd >= -30 else "Vencido 31-60" if dd >= -60 else "Vencido 61-90" if dd >= -90 else "Vencido +90")
            b[k] += sign * (r["amount_residual_signed"] or 0)
        return b
    cxc, cxp = buckets(["out_invoice", "out_refund"]), buckets(["in_invoice", "in_refund"], -1)
    out["cxc_cxp"] = [{"tramo": k, "por_cobrar": round(cxc[k], 2), "por_pagar": round(cxp[k], 2)} for k in cxc]
    venc = [k for k in cxc if k.startswith("Vencido")]
    caja = sum(r["monto"] for r in fin)
    flujo = [{"horizonte": "Caja hoy", "entradas": None, "salidas": None, "caja_proyectada": round(caja, 2)},
             {"horizonte": "Ya vencido", "entradas": round(sum(cxc[k] for k in venc), 2), "salidas": round(sum(cxp[k] for k in venc), 2)}]
    for h, keys in ((30, ["Vence 0-30"]), (60, ["Vence 31-60"]), (90, ["Vence 61-90"])):
        flujo.append({"horizonte": f"Por vencer {h - 29 if h > 30 else 0}-{h} días", "entradas": round(sum(cxc[k] for k in keys), 2), "salidas": round(sum(cxp[k] for k in keys), 2)})
    for f in flujo[1:]:
        caja += f["entradas"] - f["salidas"]
        f["caja_proyectada"] = round(caja, 2)
    out["flujo"] = flujo
    drafts = G("account.move", ["move_type"], ["amount_total_signed:sum"], [["state", "=", "draft"]])
    unrec = o.call("account.bank.statement.line", "search_read", domain=[["is_reconciled", "=", False]], fields=["amount"], limit=20000)
    out["contabilidad_pendientes"] = [{"pendiente": f"Borradores: {r['move_type']}", "cantidad": r["__count"], "monto": round(r["amount_total_signed"] or 0, 2)} for r in drafts] + \
        [{"pendiente": "Banco sin conciliar", "cantidad": len(unrec), "monto": round(sum(x["amount"] for x in unrec), 2)}]
    out["finanzas_bancos"] = fin

    # ---------- validaciones obligatorias
    val = []
    pos_lines = o.call("pos.order.line", "read_group", domain=[["order_id.date_order", ">=", utc(d90)], ["order_id.date_order", "<", utc(nxt)], ["order_id.state", "not in", ["draft", "cancel"]]],
                       fields=["price_subtotal:sum", "total_cost:sum"], groupby=[], lazy=False)
    pl = pos_lines[0] if pos_lines else {"price_subtotal": 0, "total_cost": 0}
    ret = sum(r["venta_90d"] for r in out["vendedores"] if r["area"] == "Retail")
    val.append({"validacion": "Venta neta 90d por vendedor (tienda) = suma de líneas POS", "esperado": round(pl["price_subtotal"] or 0, 2), "obtenido": round(ret, 2),
                "ok": abs(ret - (pl["price_subtotal"] or 0)) <= max(1.0, 0.005 * abs(pl["price_subtotal"] or 1))})
    rpm = G("report.pos.order", [], ["margin:sum"], [["date", ">=", utc(d90)], ["date", "<", utc(nxt)], ["state", "not in", ["draft", "cancel"]]])
    cost_from_report = ret - (rpm[0]["margin"] if rpm else 0)
    val.append({"validacion": "Costo de venta 90d (tienda) = suma de total_cost POS", "esperado": round(pl["total_cost"] or 0, 2), "obtenido": round(cost_from_report, 2),
                "ok": abs(cost_from_report - (pl["total_cost"] or 0)) <= max(1.0, 0.01 * abs(pl["total_cost"] or 1))})
    svl = o.call("stock.valuation.layer", "read_group", domain=[], fields=["value:sum", "quantity:sum"], groupby=["product_id"], lazy=False, limit=50000)
    anom = [r for r in svl if r["product_id"] and (r["value"] or 0) < -1000]
    vs = sum((r["value"] or 0) for r in svl if r not in anom)
    vq = sum(r["valor"] for r in out["inventario"])
    val.append({"validacion": "Valor inventario (existencias × costo) ≈ valoración contable (sin valoraciones negativas anómalas)", "esperado": round(vs, 2), "obtenido": round(vq, 2),
                "ok": vs == 0 or abs(vq - vs) / abs(vs) <= 0.10})
    if anom:
        val.append({"validacion": "Valoraciones negativas anómalas: " + "; ".join(f"{rel(r['product_id'], 1)[:45]} Q{r['value']:,.0f}" for r in anom),
                    "esperado": 0, "obtenido": round(sum(r["value"] for r in anom), 2), "ok": True, "aviso": True})
    disc = o.call("pos.order.line", "read_group", domain=[["product_id", "in", [c["discount_product_id"][0] for c in o.call("pos.config", "search_read", domain=[["active", "in", [True, False]], ["discount_product_id", "!=", False]], fields=["discount_product_id"])]], ["total_cost", ">", 1000]],
                  fields=["total_cost:sum"], groupby=[], lazy=False)
    if disc and disc[0]["__count"]:
        val.append({"validacion": "Líneas de descuento POS con costo > Q1,000 (margen subestimado)", "esperado": 0, "obtenido": disc[0]["__count"], "ok": True, "aviso": True, "monto": disc[0]["total_cost"]})
    neg = o.call("stock.quant", "search_count", domain=[["location_id.usage", "=", "internal"], ["quantity", "<", 0]])
    val.append({"validacion": "Existencias negativas en ubicaciones internas", "esperado": 0, "obtenido": neg, "ok": True, "aviso": neg > 0})
    sr = next((r for r in out["inventario"] if r["estado"] == "Sin rotación"), None)
    if sr:
        n = o.call("sale.report", "search_count", domain=[SALE_OK, ["product_id", "=", sr["producto_id"]], ["date", ">=", utc(d90)]])
        val.append({"validacion": f"Producto sin rotación revisado ({sr['codigo'] or sr['producto'][:30]}) no tuvo ventas en 90d", "esperado": 0, "obtenido": n, "ok": n == 0})
    out["validaciones"] = val

    meta = [{"label": "Corte", "value": f"{cut.isoformat()} (incluido), hora de Guatemala"}, {"label": "Fuente", "value": "Odoo ventasguate.odoo.com, usuario Claude Lectura (solo lectura)"},
            {"label": "Script", "value": "odoo-cli/reports/ventasguate_refresh.py"}]
    out["corte"] = [{"corte": cut.isoformat(), "generado": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                     "tipo_cambio": (fx[0]["inverse_company_rate"] if fx else None), "inicio_90d": d90.isoformat(), "inicio_mes": mes0.isoformat()}]
    for k, rows in out.items():
        json.dump({"rows": rows, "meta": meta}, open(os.path.join(a.out, f"{k}.json"), "w"), ensure_ascii=False, default=str)
    meta.append({"label": "Validaciones", "value": "; ".join(f"{'OK' if v['ok'] else 'FALLA'}{' (aviso)' if v.get('aviso') else ''}: {v['validacion']}" for v in val)})
    json.dump({"meta": meta, "sets": out}, open(os.path.join(a.out, "centro.json"), "w"), ensure_ascii=False, default=str, separators=(",", ":"))
    bad = [v for v in val if not v["ok"]]
    print(json.dumps({"datasets": {k: len(v) for k, v in out.items()}, "validaciones": val}, ensure_ascii=False, indent=1, default=str))
    return 2 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
