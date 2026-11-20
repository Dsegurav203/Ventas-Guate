"""Pruebas unitarias del control de permisos por rol (sin Odoo real: _call simulado).
Uso: python3 mcp-server/test_roles.py   (requiere las dependencias de requirements.txt)
"""
import asyncio, contextlib, io, json, os, sys, types

os.environ.setdefault("ODOO_URL", "https://odoo.invalid")
os.environ.setdefault("ODOO_DB", "test")
os.environ.setdefault("MCP_SECRET_KEY", "x" * 43 + "=")
os.environ["MCP_ALLOW_WRITE"] = "1"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import server as S  # noqa: E402

GROUPS = {
    "contabilidad@ventasguate.com": {"account.group_account_manager", "account.group_account_invoice"},
    "admin@ventasguate.com": {"base.group_system", "account.group_account_manager"},
    "vendedor@ventasguate.com": set(),
}
state = {"login": "", "calls": []}


async def fake_call(model, method, ids=None, **kw):
    if model == "res.users" and method == "has_group":
        return kw["group_ext_id"] in GROUPS[state["login"]]
    state["calls"].append((model, method, ids, kw))
    return [99] if method == "create" else True


S._call = fake_call
S._client = lambda: types.SimpleNamespace(_uid=42)
S._login = lambda: state["login"]


def as_user(login):
    state["login"], state["calls"] = login, []


def run(coro):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        res = asyncio.run(coro)
    logs = [json.loads(l) for l in buf.getvalue().splitlines() if l.startswith("{")]
    return res, logs


fails = 0


def check(cond, msg):
    global fails
    print(("PASA " if cond else "FALLA") + " · " + msg)
    fails += 0 if cond else 1


# 1. contabilidad@ concilia una línea de extracto → OK y auditado
as_user("contabilidad@ventasguate.com")
res, logs = run(S.odoo_action("account.bank.statement.line", "action_undo_reconciliation", [7]))
check(res is True and state["calls"][-1][:3] == ("account.bank.statement.line", "action_undo_reconciliation", [7]),
      "contabilidad: deshacer/conciliar línea de extracto permitido")
check(len(logs) == 1 and logs[0]["audit"] == "contabilidad" and logs[0]["login"] == "contabilidad@ventasguate.com"
      and logs[0]["ids"] == [7], "contabilidad: acción auditada en log (usuario, modelo, ids, método)")
as_user("contabilidad@ventasguate.com")
res, logs = run(S.odoo_action("account.move.line", "reconcile", [10, 11]))
check(res is True and logs and logs[0]["method"] == "reconcile", "contabilidad: reconcile de apuntes permitido y auditado")
as_user("contabilidad@ventasguate.com")
res, logs = run(S.odoo_write("account.bank.statement.line", [7], {"partner_id": 5}))
check(res is True and logs and logs[0]["values"] == {"partner_id": 5}, "contabilidad: write en línea de extracto con valores en log")

# 2. contabilidad@ intenta escribir account.journal → rechazo
for model in ("account.journal", "account.account", "account.tax", "res.company", "res.users", "ir.cron"):
    as_user("contabilidad@ventasguate.com")
    res, _ = run(S.odoo_write(model, [1], {"name": "x"}))
    check(isinstance(res, dict) and "error" in res and not state["calls"], f"contabilidad: write en {model} rechazado")
as_user("contabilidad@ventasguate.com")
res, _ = run(S.odoo_action("account.journal", "action_post", [1]))
check(isinstance(res, dict) and "error" in res and not state["calls"], "contabilidad: acción sobre account.journal rechazada")
as_user("contabilidad@ventasguate.com")
res, _ = run(S.odoo_action("account.move", "button_draft", [1]))
check(isinstance(res, dict) and "error" in res and not state["calls"], "contabilidad: método fuera de lista rechazado")

# 3. contabilidad@ intenta unlink → rechazo
as_user("contabilidad@ventasguate.com")
res, _ = run(S.odoo_unlink("account.move", [1]))
check(isinstance(res, dict) and "error" in res and not state["calls"], "contabilidad: odoo_unlink rechazado")
as_user("contabilidad@ventasguate.com")
res, _ = run(S.odoo_action("account.move", "unlink", [1]))
check(isinstance(res, dict) and "error" in res and not state["calls"], "contabilidad: unlink vía odoo_action rechazado")

# Sin cambios para los demás roles
as_user("contabilidad@ventasguate.com")
res, _ = run(S.odoo_action("stock.landed.cost", "compute_landed_cost", [3]))
check(res is True, "contabilidad: permisos de costeo (ROLE_GRANTS) intactos")
as_user("vendedor@ventasguate.com")
res, _ = run(S.odoo_write("account.move", [1], {"ref": "x"}))
check(isinstance(res, dict) and "error" in res, "usuario sin rol: account.move rechazado")
as_user("vendedor@ventasguate.com")
res, logs = run(S.odoo_write("product.template", [1], {"name": "x"}))
check(res is True and not logs, "usuario sin rol: productos permitidos, sin auditoría")
as_user("admin@ventasguate.com")
res, logs = run(S.odoo_write("account.journal", [1], {"name": "x"}))
check(res is True and not logs, "administrador: cualquier modelo (sin cambios)")
as_user("admin@ventasguate.com")
res, _ = run(S.odoo_unlink("account.move", [1]))
check(res is True, "administrador: unlink permitido (sin cambios)")

print(f"\n{'OK' if not fails else f'{fails} FALLAS'}")
sys.exit(1 if fails else 0)
