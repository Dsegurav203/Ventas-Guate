#!/usr/bin/env python3
"""odoo-cli: direct command-line access to Odoo (no third-party MCP).

Protocols:
  json2   Odoo 19+  -> POST {url}/json/2/{model}/{method}, Bearer API key
  xmlrpc  Odoo <=18 -> {url}/xmlrpc/2/common + /xmlrpc/2/object (execute_kw)
  auto    try json2, fall back to xmlrpc

Config (env vars or .env in cwd / ~/.config/odoo-cli/.env):
  ODOO_URL, ODOO_DB, ODOO_USER, ODOO_API_KEY, ODOO_PROTOCOL (auto|json2|xmlrpc)
Python stdlib only.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.request
import xmlrpc.client
from pathlib import Path

__version__ = "0.1.0"

READ_METHODS = {"search", "search_read", "read", "search_count", "read_group", "formatted_read_group",
                "fields_get", "name_search", "name_get", "display_name", "context_get", "default_get",
                "check_access_rights", "has_group", "get_views", "authenticate", "version"}

WRITE_METHODS = {"create", "write", "unlink", "copy", "action_confirm", "action_post",
                 "button_confirm", "button_validate", "action_cancel"}


# --------------------------------------------------------------------------- config
def load_env() -> None:
    for p in (Path.cwd() / ".env", Path.home() / ".config" / "odoo-cli" / ".env"):
        if not p.is_file():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


class OdooError(Exception):
    pass


# --------------------------------------------------------------------------- client
class Odoo:
    def __init__(self, url: str, db: str | None, user: str | None, key: str,
                 protocol: str = "auto", timeout: int = 60):
        if not url or not key:
            raise OdooError("Faltan ODOO_URL y/o ODOO_API_KEY")
        self.url = url.rstrip("/")
        self.db, self.user, self.key = db, user, key
        self.timeout = timeout
        self.readonly = os.environ.get("ODOO_READONLY", "") not in ("", "0", "false")
        self.protocol = protocol
        self._uid: int | None = None
        if protocol == "auto":
            self.protocol = self._detect()

    # -- detection
    def _detect(self) -> str:
        try:
            self._json2("res.users", "context_get", {})
            return "json2"
        except OdooError as e:
            if getattr(e, "status", None) in (404, 405):
                return "xmlrpc"
            raise

    # -- JSON-2 (Odoo 19+)
    def _json2(self, model: str, method: str, body: dict):
        req = urllib.request.Request(
            f"{self.url}/json/2/{model}/{method}",
            data=json.dumps(body, default=str).encode(),
            method="POST",
            headers={
                "Authorization": f"Bearer {self.key}",
                "Content-Type": "application/json; charset=utf-8",
                "User-Agent": f"odoo-cli/{__version__}",
                **({"X-Odoo-Database": self.db} if self.db else {}),
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                raw = r.read()
                if raw and "json" not in (r.headers.get("Content-Type") or ""):
                    # route missing (Odoo <=18 redirects to /web/login)
                    err = OdooError(f"Respuesta no JSON desde {r.geturl()} (¿Odoo <=18? use xmlrpc)")
                    err.status = 404
                    raise err
                return json.loads(raw) if raw else None
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")
            try:
                msg = json.loads(msg).get("message", msg)
            except Exception:
                pass
            err = OdooError(f"HTTP {e.code}: {msg[:500]}")
            err.status = e.code
            raise err from None
        except urllib.error.URLError as e:
            raise OdooError(f"No se pudo conectar a {self.url}: {e.reason}") from None

    # -- XML-RPC (Odoo <= 18)
    @property
    def uid(self) -> int:
        if self._uid is None:
            if not (self.db and self.user):
                raise OdooError("XML-RPC requiere ODOO_DB y ODOO_USER")
            common = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/common", allow_none=True)
            uid = common.authenticate(self.db, self.user, self.key, {})
            if not uid:
                raise OdooError("Autenticación fallida (usuario/API key/DB)")
            self._uid = uid
        return self._uid

    def _xmlrpc(self, model: str, method: str, args: list, kwargs: dict):
        obj = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/object", allow_none=True)
        try:
            return obj.execute_kw(self.db, self.uid, self.key, model, method, args, kwargs)
        except xmlrpc.client.Fault as f:
            last = [l for l in str(f.faultString).strip().splitlines() if l.strip()]
            raise OdooError(last[-1] if last else str(f)) from None
        except OSError as e:
            raise OdooError(f"No se pudo conectar a {self.url}: {e}") from None

    # -- unified call: ids (optional) + keyword args
    def call(self, model: str, method: str, ids: list[int] | None = None, **kwargs):
        if self.readonly and method not in READ_METHODS:
            raise OdooError(f"Modo solo lectura: '{model}.{method}' bloqueado (ODOO_READONLY=1)")
        if self.protocol == "json2":
            body = dict(kwargs)
            if ids is not None:
                body["ids"] = ids
            return self._json2(model, method, body)
        args = [ids] if ids is not None else []
        # pass the main argument positionally: @api.model_create_multi requires it and
        # many models override write(self, values) with a different parameter name
        for m, k in (("create", "vals_list"), ("write", "vals")):
            if method == m and k in kwargs:
                args.append(kwargs.pop(k))
        return self._xmlrpc(model, method, args, kwargs)

    def version(self) -> dict:
        if self.protocol == "xmlrpc":
            return xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/common").version()
        req = urllib.request.Request(f"{self.url}/web/version", data=b"{}", method="POST",
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                return json.loads(r.read())
        except Exception:
            return {}


def client_from_env(args) -> Odoo:
    ro = bool(getattr(args, "readonly", False)) or os.environ.get("ODOO_READONLY", "") not in ("", "0", "false")
    # with a read-only key configured, read-only mode uses it (defense in depth: an Odoo user without write rights)
    key = os.environ.get("ODOO_RO_API_KEY") if ro and os.environ.get("ODOO_RO_API_KEY") else os.environ.get("ODOO_API_KEY", "")
    user = os.environ.get("ODOO_RO_USER") if ro and os.environ.get("ODOO_RO_USER") else os.environ.get("ODOO_USER")
    o = Odoo(
        url=os.environ.get("ODOO_URL", ""),
        db=os.environ.get("ODOO_DB"),
        user=user,
        key=key,
        protocol=args.protocol or os.environ.get("ODOO_PROTOCOL", "auto"),
    )
    o.readonly = ro
    return o


# --------------------------------------------------------------------------- helpers
def jarg(s: str | None, default):
    if s is None:
        return default
    if s.startswith("@"):
        s = Path(s[1:]).read_text(encoding="utf-8")
    try:
        return json.loads(s)
    except json.JSONDecodeError as e:
        raise OdooError(f"JSON inválido: {s!r} ({e})") from None


def ids_arg(s: str) -> list[int]:
    return [int(x) for x in s.replace(" ", "").split(",") if x]


def flat(v):
    # many2one -> "Name" ; x2many -> "1,2,3"
    if isinstance(v, list) and len(v) == 2 and isinstance(v[0], int) and isinstance(v[1], str):
        return v[1]
    if isinstance(v, list):
        return ",".join(map(str, v))
    if v is False:
        return ""
    return v


def emit(data, fmt: str, out=None):
    out = out or sys.stdout
    if fmt == "json" or not isinstance(data, list) or (data and not isinstance(data[0], dict)):
        json.dump(data, out, ensure_ascii=False, indent=2, default=str)
        out.write("\n")
        return
    if not data:
        print("(sin resultados)", file=sys.stderr)
        return
    cols = list(dict.fromkeys(k for r in data for k in r))
    rows = [[flat(r.get(c, "")) for c in cols] for r in data]
    if fmt == "csv":
        w = csv.writer(out)
        w.writerow(cols)
        w.writerows(rows)
        return
    srows = [[f"{x:,.2f}" if isinstance(x, float) else ("" if x is None else str(x)) for x in r] for r in rows]
    widths = [min(max(len(c), *(len(r[i]) for r in srows)), 40) for i, c in enumerate(cols)]
    num = [all(isinstance(r[i], (int, float)) and not isinstance(r[i], bool) for r in rows) for i in range(len(cols))]
    line = lambda vals: "  ".join((v[:w].rjust(w) if n else v[:w].ljust(w)) for v, w, n in zip(vals, widths, num))
    print(line(cols), file=out)
    print("  ".join("-" * w for w in widths), file=out)
    for r in srows:
        print(line(r), file=out)


def confirm(action: str, yes: bool):
    if yes:
        return
    if not sys.stdin.isatty():
        raise OdooError(f"'{action}' modifica datos: agrega --yes para confirmar")
    if input(f"{action} — ¿confirmar? [y/N] ").strip().lower() not in ("y", "s", "si", "sí", "yes"):
        raise OdooError("Cancelado")


# --------------------------------------------------------------------------- commands
def cmd_ping(o: Odoo, a):
    v = o.version()
    who = o.call("res.users", "context_get")
    emit({"url": o.url, "db": o.db, "protocol": o.protocol,
          "server_version": v.get("server_version"), "user": who}, "json")


def cmd_models(o: Odoo, a):
    dom = [["model", "ilike", a.filter]] if a.filter else []
    emit(o.call("ir.model", "search_read", domain=dom, fields=["model", "name"], order="model",
                limit=a.limit), a.format)


def cmd_fields(o: Odoo, a):
    res = o.call(a.model, "fields_get", attributes=["string", "type", "relation", "required", "readonly"])
    rows = [{"field": k, **v} for k, v in sorted(res.items())]
    if a.filter:
        f = a.filter.lower()
        rows = [r for r in rows if f in r["field"].lower() or f in str(r.get("string", "")).lower()]
    emit(rows, a.format)


def cmd_search(o: Odoo, a):
    kw = {"domain": jarg(a.domain, []), "limit": a.limit, "offset": a.offset}
    if a.fields:
        kw["fields"] = a.fields.split(",")
    if a.order:
        kw["order"] = a.order
    emit(o.call(a.model, "search_read", **kw), a.format)


def cmd_count(o: Odoo, a):
    print(o.call(a.model, "search_count", domain=jarg(a.domain, [])))


def cmd_get(o: Odoo, a):
    kw = {"fields": a.fields.split(",")} if a.fields else {}
    emit(o.call(a.model, "read", ids=ids_arg(a.ids), **kw), a.format)


def cmd_group(o: Odoo, a):
    domain = jarg(a.domain, [])
    groupby = a.groupby.split(",")
    aggs = a.aggregates.split(",") if a.aggregates else []
    try:  # Odoo 19+
        res = o.call(a.model, "formatted_read_group", domain=domain, groupby=groupby,
                     aggregates=aggs + ["__count"], order=a.order or None, limit=a.limit)
    except OdooError:
        # <= 18: fields like "amount_total:sum"
        res = o.call(a.model, "read_group", domain=domain, groupby=groupby,
                     fields=aggs, orderby=a.order or False,
                     limit=a.limit, lazy=False)
        for r in res:
            r.pop("__domain", None)
    for r in res:
        r.pop("__extra_domain", None)
    emit(res, a.format)


def cmd_create(o: Odoo, a):
    vals = jarg(a.values, {})
    vals_list = vals if isinstance(vals, list) else [vals]
    confirm(f"create {a.model} x{len(vals_list)}", a.yes)
    emit(o.call(a.model, "create", vals_list=vals_list), "json")


def cmd_write(o: Odoo, a):
    ids = ids_arg(a.ids)
    confirm(f"write {a.model} {ids}", a.yes)
    emit(o.call(a.model, "write", ids=ids, vals=jarg(a.values, {})), "json")


def cmd_unlink(o: Odoo, a):
    ids = ids_arg(a.ids)
    confirm(f"DELETE {a.model} {ids}", a.yes)
    emit(o.call(a.model, "unlink", ids=ids), "json")


def cmd_call(o: Odoo, a):
    ids = ids_arg(a.ids) if a.ids else None
    if a.method in WRITE_METHODS or a.method.startswith(("action_", "button_")):
        confirm(f"{a.model}.{a.method} {ids or ''}", a.yes)
    emit(o.call(a.model, a.method, ids=ids, **jarg(a.kwargs, {})), "json")


# --------------------------------------------------------------------------- argparse
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="odoo", description="CLI directo a Odoo (JSON-2 / XML-RPC)")
    p.add_argument("--protocol", choices=["auto", "json2", "xmlrpc"], help="default: $ODOO_PROTOCOL o auto")
    p.add_argument("--version", action="version", version=__version__)
    p.add_argument("--readonly", action="store_true", help="bloquea cualquier escritura (igual que ODOO_READONLY=1)")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add(name, fn, help_, fmt=True):
        sp = sub.add_parser(name, help=help_)
        sp.set_defaults(fn=fn)
        if fmt:
            sp.add_argument("-F", "--format", choices=["table", "json", "csv"], default="table")
        return sp

    add("ping", cmd_ping, "probar conexión y mostrar versión/usuario", fmt=False)

    sp = add("models", cmd_models, "listar modelos")
    sp.add_argument("filter", nargs="?")
    sp.add_argument("-l", "--limit", type=int, default=200)

    sp = add("fields", cmd_fields, "campos de un modelo")
    sp.add_argument("model")
    sp.add_argument("filter", nargs="?")

    sp = add("search", cmd_search, "search_read")
    sp.add_argument("model")
    sp.add_argument("-d", "--domain", help='JSON, ej: \'[["state","=","sale"]]\' o @archivo.json')
    sp.add_argument("-f", "--fields", help="campo1,campo2")
    sp.add_argument("-l", "--limit", type=int, default=80)
    sp.add_argument("--offset", type=int, default=0)
    sp.add_argument("-o", "--order", help='ej: "date_order desc"')

    sp = add("count", cmd_count, "search_count", fmt=False)
    sp.add_argument("model")
    sp.add_argument("-d", "--domain")

    sp = add("get", cmd_get, "read por IDs")
    sp.add_argument("model")
    sp.add_argument("ids", help="1,2,3")
    sp.add_argument("-f", "--fields")

    sp = add("group", cmd_group, "agrupar/sumar (reportes)")
    sp.add_argument("model")
    sp.add_argument("-g", "--groupby", required=True, help="ej: partner_id o date_order:month")
    sp.add_argument("-a", "--aggregates", help="ej: amount_total:sum,amount_untaxed:sum")
    sp.add_argument("-d", "--domain")
    sp.add_argument("-o", "--order")
    sp.add_argument("-l", "--limit", type=int)

    for name, fn, h in (("create", cmd_create, "crear registro(s)"),
                        ("write", cmd_write, "actualizar registros"),
                        ("unlink", cmd_unlink, "eliminar registros")):
        sp = add(name, fn, h, fmt=False)
        sp.add_argument("model")
        if name != "create":
            sp.add_argument("ids")
        if name != "unlink":
            sp.add_argument("values", help="JSON o @archivo.json")
        sp.add_argument("-y", "--yes", action="store_true")

    sp = add("call", cmd_call, "llamar cualquier método", fmt=False)
    sp.add_argument("model")
    sp.add_argument("method")
    sp.add_argument("--ids")
    sp.add_argument("-k", "--kwargs", help="JSON de argumentos con nombre")
    sp.add_argument("-y", "--yes", action="store_true")
    return p


def main(argv=None) -> int:
    load_env()
    a = build_parser().parse_args(argv)
    try:
        a.fn(client_from_env(a), a)
        return 0
    except OdooError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
