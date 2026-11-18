# Extrae cartera vencida (corte YYYY-MM-DD, fecha de hoy) y valida contra read_group.
# Uso: python3 odoo-cli/reports/cobranza_extract.py 2026-11-17 2026-11-18  -> cob_<corte>.json
import json, sys, os, time, datetime as dt
sys.path.insert(0, "odoo-cli"); import odoo_cli as oc; oc.load_env()
t0=time.time()
o = oc.Odoo(os.environ["ODOO_URL"], os.environ["ODOO_DB"], os.environ["ODOO_USER"], os.environ["ODOO_API_KEY"], "xmlrpc")
cut = sys.argv[1]; hoy = dt.date.fromisoformat(sys.argv[2])
dom=[["move_type","=","out_invoice"],["state","=","posted"],["payment_state","in",["not_paid","partial"]],["invoice_date_due","<=",cut]]
F=["name","partner_id","invoice_date","invoice_date_due","amount_total","amount_total_signed","amount_residual","amount_residual_signed","payment_state","invoice_user_id","currency_id"]
rows=o.call("account.move","search_read",domain=dom,fields=F,order="invoice_date_due asc",limit=5000)
grp=o.call("account.move","read_group",domain=dom,fields=["amount_residual_signed:sum"],groupby=["invoice_user_id"],lazy=False)
for r in rows:
    r["dias"]=(hoy-dt.date.fromisoformat(r["invoice_date_due"])).days
    r["pagado_pct"]=round(100*(1-r["amount_residual"]/r["amount_total"]),2) if r["amount_total"] else 0
tot=sum(r["amount_residual_signed"] for r in rows)
gtot=sum(g["amount_residual_signed"] for g in grp)
out={"cut":cut,"hoy":str(hoy),"rows":rows,"group":grp,"total":tot,"group_total":gtot,"secs":round(time.time()-t0,2)}
json.dump(out,open(f"{os.environ.get("OUT_DIR",".")}/cob_{cut}.json","w"),default=str)
print(f"corte {cut}: {len(rows)} facturas, {len({r['partner_id'][0] for r in rows})} clientes, Q{tot:,.2f} | read_group Q{gtot:,.2f} | dif {tot-gtot:.2f} | {out['secs']}s")
