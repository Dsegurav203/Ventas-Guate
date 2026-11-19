#!/usr/bin/env python3
"""Tareas semanales de cobranza en Odoo (actividades "Cobranza semanal" sobre el cliente).

Uso (desde la raíz del repo):
  python3 odoo-cli/reports/cobranza_tareas.py preview  CORTE HOY    # lista de tareas propuestas (no escribe)
  python3 odoo-cli/reports/cobranza_tareas.py create   CORTE HOY    # crea las tareas (pide --yes)
  python3 odoo-cli/reports/cobranza_tareas.py review   DESDE HOY    # respuestas y cumplimiento desde DESDE

CORTE = último día de vencimiento incluido (normalmente ayer). Fechas YYYY-MM-DD.
Criterio: cliente con saldo vencido >= Q1,000 o con alguna factura > 30 días. Excluye internas.
Responsable: vendedor de la factura; si no es vendedor (bodega, logística, sin asignar) -> Glenda (contabilidad).
Formato de respuesta del vendedor al marcar hecha:
  COMPROMISO: AAAA-MM-DD Q<monto> | DISPUTA: <motivo> | SIN CONTACTO | PAGADO
"""
import collections, datetime as dt, json, os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import odoo_cli as oc  # noqa: E402

TYPE_NAME = "Cobranza semanal"
MIN_SALDO, MIN_DIAS = 1000, 30
SELLERS = {7: "Henry Galindo", 34: "Luis Guevara", 359: "Estuardo Pineda", 338: "Fernando Aguilar", 35: "Luis Alfredo Cantoral"}
FALLBACK_USER = 27  # Glenda Ixcayau (contabilidad)
INTERNAL = ("SEGURA VILLAGRAN", "BUYITWITHUS", "CONSUMIDOR FINAL")


def client():
    oc.load_env()
    e = os.environ
    return oc.Odoo(e["ODOO_URL"], e.get("ODOO_DB"), e.get("ODOO_USER"), e["ODOO_API_KEY"], e.get("ODOO_PROTOCOL", "auto"))


def q(n):
    return f"Q{n:,.2f}"


def build(o, corte, hoy):
    dom = [["move_type", "=", "out_invoice"], ["state", "=", "posted"],
           ["payment_state", "in", ["not_paid", "partial"]], ["invoice_date_due", "<=", corte]]
    rows = o.call("account.move", "search_read", domain=dom, limit=5000, order="invoice_date_due asc",
                  fields=["name", "partner_id", "invoice_date_due", "amount_total", "amount_residual_signed",
                          "amount_residual", "payment_state", "invoice_user_id", "commercial_partner_id"])
    by = collections.defaultdict(list)
    for r in rows:
        if any(x in r["partner_id"][1].upper() for x in INTERNAL):
            continue
        r["dias"] = (hoy - dt.date.fromisoformat(r["invoice_date_due"])).days
        by[r["commercial_partner_id"][0]].append(r)
    tasks = []
    for pid, rs in by.items():
        saldo = sum(r["amount_residual_signed"] for r in rs)
        dias = max(r["dias"] for r in rs)
        if saldo < MIN_SALDO and dias <= MIN_DIAS:
            continue
        top = max(rs, key=lambda r: r["amount_residual_signed"])
        uid = top["invoice_user_id"][0] if top["invoice_user_id"] else None
        user = uid if uid in SELLERS else FALLBACK_USER
        solo_ret = [r for r in rs if r["payment_state"] == "partial" and 1.5 <= 100 * (1 - r["amount_residual"] / r["amount_total"]) <= 1.7]
        if dias > 60:
            accion = "Más de 60 días: acordar plan de pago por escrito o escalar a gerencia. No despachar a crédito."
        elif solo_ret:
            accion = "Solo tiene aplicada la retención de IVA (sin pago real). Confirmar fecha y monto de pago."
        elif dias > 30:
            accion = "Más de 30 días: pedir compromiso de pago con fecha antes de cruzar 60 días."
        else:
            accion = "Vencida reciente: llamar y confirmar fecha de pago."
        lines = "".join(f"<li>{r['name']} · vence {r['invoice_date_due']} · {r['dias']} d · saldo {q(r['amount_residual_signed'])}</li>"
                        for r in sorted(rs, key=lambda r: -r["dias"]))
        note = (f"<p><b>Saldo vencido: {q(saldo)}</b> · {len(rs)} factura(s) · máx. {dias} días (corte {corte}).</p>"
                f"<ul>{lines}</ul><p><b>Acción:</b> {accion}</p>"
                "<p>Al marcar como hecha, responder con: <code>COMPROMISO: AAAA-MM-DD Q monto</code> · "
                "<code>DISPUTA: motivo</code> · <code>SIN CONTACTO</code> · <code>PAGADO</code></p>")
        tasks.append({"partner_id": pid, "partner": top["commercial_partner_id"][1], "user_id": user,
                      "user": SELLERS.get(user, "Glenda Ixcayau (contabilidad)"), "saldo": saldo, "dias": dias,
                      "facturas": len(rs), "accion": accion, "note": note,
                      "prioridad": saldo * (1 + dias / 30)})
    return sorted(tasks, key=lambda t: -t["prioridad"])


def activity_type(o):
    ids = o.call("mail.activity.type", "search", domain=[["name", "=", TYPE_NAME]])
    if ids:
        return ids[0]
    return o.call("mail.activity.type", "create", vals_list=[{
        "name": TYPE_NAME, "res_model": "res.partner", "category": "default", "icon": "fa-money",
        "delay_count": 2, "delay_unit": "days", "delay_from": "current_date", "keep_done": True,
        "summary": "Gestión de cobranza semanal"}])[0]


def preview(tasks):
    print(f"{'Responsable':32} {'Cliente':42} {'Saldo':>14} {'Días':>5} Fac")
    for t in tasks:
        print(f"{t['user'][:32]:32} {t['partner'][:42]:42} {q(t['saldo']):>14} {t['dias']:>5} {t['facturas']:>3}")
    tot = collections.Counter()
    for t in tasks:
        tot[t["user"]] += 1
    print(f"\n{len(tasks)} tareas ·", " · ".join(f"{u}: {n}" for u, n in tot.most_common()))


def create(o, tasks, hoy):
    tid = activity_type(o)
    model_id = o.call("ir.model", "search", domain=[["model", "=", "res.partner"]])[0]
    deadline = str(hoy + dt.timedelta(days=2))
    open_ids = o.call("mail.activity", "search_read", domain=[["activity_type_id", "=", tid], ["res_model", "=", "res.partner"]],
                      fields=["res_id"])
    abiertas = {a["res_id"] for a in open_ids}
    vals = [{"res_model_id": model_id, "res_id": t["partner_id"], "activity_type_id": tid, "user_id": t["user_id"],
             "summary": f"Cobranza: {t['partner'][:40]} · {q(t['saldo'])}", "note": t["note"], "date_deadline": deadline}
            for t in tasks if t["partner_id"] not in abiertas]
    ids = o.call("mail.activity", "create", vals_list=vals) if vals else []
    print(f"creadas {len(ids)} tareas (vencen {deadline}); omitidas {len(tasks) - len(vals)} con tarea abierta previa")
    return ids


PAT = re.compile(r"COMPROMISO:\s*(\d{4}-\d{2}-\d{2})\s*Q?\s*([\d,\.]+)|DISPUTA|SIN CONTACTO|PAGADO", re.I)


def review(o, desde, hoy):
    tid = activity_type(o)
    msgs = o.call("mail.message", "search_read", limit=1000,
                  domain=[["mail_activity_type_id", "=", tid], ["model", "=", "res.partner"], ["date", ">=", desde]],
                  fields=["res_id", "record_name", "author_id", "body", "date"])
    pend = o.call("mail.activity", "search_read", domain=[["activity_type_id", "=", tid]],
                  fields=["res_id", "user_id", "date_deadline", "summary"])
    out = {"cerradas": [], "pendientes": [], "vencidas": []}
    for m in msgs:
        txt = re.sub("<[^>]+>", " ", m["body"] or "")
        mm = PAT.search(txt)
        kind = (mm.group(0).split(":")[0].upper() if mm else "SIN FORMATO")
        rec = {"cliente": m["record_name"], "por": m["author_id"] and m["author_id"][1], "fecha": m["date"][:10], "respuesta": kind}
        if mm and mm.group(1):
            rec.update(compromiso_fecha=mm.group(1), compromiso_monto=float(mm.group(2).replace(",", "")))
            pagos = o.call("account.payment", "search_read", fields=["amount_company_currency_signed", "date"],
                           domain=[["partner_id", "child_of", m["res_id"]], ["payment_type", "=", "inbound"],
                                   ["date", ">=", rec["fecha"]], ["state", "not in", ["draft", "canceled", "cancel"]]])
            rec["pagado_desde"] = sum(p["amount_company_currency_signed"] for p in pagos)
            vencido = dt.date.fromisoformat(mm.group(1)) < hoy
            rec["cumplido"] = rec["pagado_desde"] >= rec["compromiso_monto"] * 0.95 if vencido else None
        out["cerradas"].append(rec)
    for a in pend:
        r = {"cliente": a["summary"], "responsable": a["user_id"][1], "vence": a["date_deadline"]}
        (out["vencidas"] if a["date_deadline"] < str(hoy) else out["pendientes"]).append(r)
    print(json.dumps(out, ensure_ascii=False, indent=2, default=str))


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        return 1
    mode, a, b = sys.argv[1], sys.argv[2], dt.date.fromisoformat(sys.argv[3])
    o = client()
    if mode == "review":
        review(o, a, b)
        return 0
    tasks = build(o, a, b)
    if mode == "preview":
        preview(tasks)
    elif mode == "create":
        if "--yes" not in sys.argv:
            preview(tasks)
            print("\nNo se creó nada. Repetir con --yes para crear.")
            return 1
        create(o, tasks, b)
    return 0


if __name__ == "__main__":
    sys.exit(main())
