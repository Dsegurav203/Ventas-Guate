#!/usr/bin/env python3
"""MCP propio de Ventas Guate: conector remoto de Odoo para el chat de claude.ai.

- Cada persona inicia sesión con SU usuario y API key de Odoo: Odoo aplica sus permisos.
- OAuth 2.1 con registro dinámico (lo que exige claude.ai) y sin base de datos: clientes,
  códigos y tokens van cifrados (Fernet) con MCP_SECRET_KEY. Cambiar la clave cierra todas
  las sesiones. Revocar la API key en Odoo corta el acceso de esa persona de inmediato.
- Escritura (crear/editar/ejecutar) solo si MCP_ALLOW_WRITE=1; aun así Odoo valida permisos.

Variables: ODOO_URL, ODOO_DB, MCP_PUBLIC_URL (https://…), MCP_SECRET_KEY (Fernet),
           MCP_ALLOW_WRITE (0/1), MCP_ALLOW_LOCAL_REDIRECTS (0/1, solo pruebas), PORT.
"""
from __future__ import annotations

import base64, hashlib, hmac, html, json, os, sys, time, urllib.parse, xmlrpc.client
from typing import Any

import anyio
from cryptography.fernet import Fernet, InvalidToken
from pydantic import AnyUrl
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse, Response

from mcp.server.auth.middleware.auth_context import get_access_token
from mcp.server.auth.provider import (AccessToken, AuthorizationCode, AuthorizationParams,
                                      OAuthAuthorizationServerProvider, RefreshToken, RegistrationError,
                                      TokenError, construct_redirect_uri)
from mcp.server.auth.settings import AuthSettings, ClientRegistrationOptions, RevocationOptions
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from mcp.shared.auth import OAuthClientInformationFull, OAuthToken

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "odoo-cli"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "odoo-cli"))
import odoo_cli as oc  # noqa: E402

ODOO_URL = os.environ["ODOO_URL"].rstrip("/")
ODOO_DB = os.environ["ODOO_DB"]
PUBLIC_URL = os.environ.get("MCP_PUBLIC_URL", "http://localhost:8000").rstrip("/")
SECRET = os.environ["MCP_SECRET_KEY"].encode()
ALLOW_WRITE = os.environ.get("MCP_ALLOW_WRITE", "0") == "1"
ALLOW_LOCAL = os.environ.get("MCP_ALLOW_LOCAL_REDIRECTS", "0") == "1"
F = Fernet(SECRET)

ACCESS_TTL = 8 * 3600
REFRESH_TTL = 90 * 24 * 3600
CODE_TTL = 300
LOGIN_TTL = 900
CALLBACK_HOSTS = {"claude.ai", "claude.com"}


# --------------------------------------------------------------------------- helpers
def seal(kind: str, data: dict, ttl: int) -> str:
    return F.encrypt(json.dumps({"k": kind, "exp": int(time.time()) + ttl, **data}).encode()).decode()


def unseal(kind: str, token: str) -> dict | None:
    try:
        d = json.loads(F.decrypt(token.encode()))
    except (InvalidToken, ValueError):
        return None
    if d.get("k") != kind or d.get("exp", 0) < time.time():
        return None
    return d


def sign(s: str) -> str:
    return hmac.new(SECRET, s.encode(), hashlib.sha256).hexdigest()


def redirect_ok(uri: str) -> bool:
    u = urllib.parse.urlparse(uri)
    if u.scheme == "https" and u.hostname in CALLBACK_HOSTS:
        return True
    return ALLOW_LOCAL and u.hostname in ("localhost", "127.0.0.1")


def odoo_authenticate(login: str, key: str) -> int | None:
    try:
        uid = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common").authenticate(ODOO_DB, login, key, {})
        return uid or None
    except Exception:
        return None


# --------------------------------------------------------------------------- OAuth provider (stateless)
class OdooOAuth(OAuthAuthorizationServerProvider[AuthorizationCode, RefreshToken, AccessToken]):

    async def register_client(self, client_info: OAuthClientInformationFull) -> None:
        uris = [str(u) for u in (client_info.redirect_uris or [])]
        if not uris or not all(redirect_ok(u) for u in uris):
            raise RegistrationError(error="invalid_redirect_uri", error_description="redirect_uri no permitido")
        meta = {"r": uris, "m": client_info.token_endpoint_auth_method or "none", "n": client_info.client_name or ""}
        body = base64.urlsafe_b64encode(json.dumps(meta, separators=(",", ":")).encode()).decode().rstrip("=")
        client_info.client_id = f"{body}.{sign(body)[:32]}"
        client_info.client_secret = sign("secret:" + client_info.client_id) if meta["m"] != "none" else None
        client_info.client_secret_expires_at = None

    async def get_client(self, client_id: str) -> OAuthClientInformationFull | None:
        try:
            body, mac = client_id.rsplit(".", 1)
            if not hmac.compare_digest(mac, sign(body)[:32]):
                return None
            meta = json.loads(base64.urlsafe_b64decode(body + "=" * (-len(body) % 4)))
        except Exception:
            return None
        return OAuthClientInformationFull(
            client_id=client_id, redirect_uris=[AnyUrl(u) for u in meta["r"]], token_endpoint_auth_method=meta["m"],
            client_secret=sign("secret:" + client_id) if meta["m"] != "none" else None,
            grant_types=["authorization_code", "refresh_token"], response_types=["code"], client_name=meta.get("n"))

    async def authorize(self, client: OAuthClientInformationFull, params: AuthorizationParams) -> str:
        txn = seal("login", {"c": client.client_id, "ru": str(params.redirect_uri),
                             "rx": params.redirect_uri_provided_explicitly, "ch": params.code_challenge,
                             "st": params.state, "sc": params.scopes or [], "rs": params.resource}, LOGIN_TTL)
        return f"{PUBLIC_URL}/login?txn={txn}"

    async def load_authorization_code(self, client, authorization_code: str) -> AuthorizationCode | None:
        d = unseal("code", authorization_code)
        if not d or d["c"] != client.client_id:
            return None
        return AuthorizationCode(code=authorization_code, scopes=d["sc"], expires_at=d["exp"], client_id=d["c"],
                                 code_challenge=d["ch"], redirect_uri=AnyUrl(d["ru"]),
                                 redirect_uri_provided_explicitly=d["rx"], resource=d.get("rs"), subject=d["login"])

    def _tokens(self, client_id: str, d: dict) -> OAuthToken:
        user = {"c": client_id, "login": d["login"], "key": d["key"], "uid": d["uid"], "sc": d.get("sc", []), "rs": d.get("rs")}
        return OAuthToken(access_token=seal("access", user, ACCESS_TTL), token_type="Bearer", expires_in=ACCESS_TTL,
                          refresh_token=seal("refresh", user, REFRESH_TTL), scope=" ".join(user["sc"]) or None)

    async def exchange_authorization_code(self, client, authorization_code: AuthorizationCode) -> OAuthToken:
        d = unseal("code", authorization_code.code)
        if not d:
            raise TokenError(error="invalid_grant", error_description="código vencido")
        return self._tokens(client.client_id, d)

    async def load_refresh_token(self, client, refresh_token: str) -> RefreshToken | None:
        d = unseal("refresh", refresh_token)
        if not d or d["c"] != client.client_id:
            return None
        return RefreshToken(token=refresh_token, client_id=d["c"], scopes=d["sc"], expires_at=d["exp"])

    async def exchange_refresh_token(self, client, refresh_token: RefreshToken, scopes: list[str]) -> OAuthToken:
        d = unseal("refresh", refresh_token.token)
        if not d:
            raise TokenError(error="invalid_grant", error_description="sesión vencida")
        uid = await anyio.to_thread.run_sync(odoo_authenticate, d["login"], d["key"])
        if not uid:  # API key revocada en Odoo
            raise TokenError(error="invalid_grant", error_description="la API key de Odoo ya no es válida")
        return self._tokens(client.client_id, {**d, "uid": uid})

    async def load_access_token(self, token: str) -> AccessToken | None:
        d = unseal("access", token)
        if not d:
            return None
        return AccessToken(token=token, client_id=d["c"], scopes=d["sc"], expires_at=d["exp"],
                           resource=d.get("rs"), subject=d["login"])

    async def revoke_token(self, token) -> None:  # sin estado: la sesión vence sola; revocar la API key en Odoo
        return None


# --------------------------------------------------------------------------- server
INSTRUCTIONS = """Conector de Odoo 18 de Ventas Guate (Buyitwithus, S.A.). Moneda GTQ. Responde en español.
Consultas con los permisos de Odoo de la persona conectada.
- Totales y reportes: usa odoo_group (agrupa en el servidor), no bajes miles de registros.
- Ventas confirmadas: modelo sale.report con dominio [["state","not in",["draft","sent","cancel"]]] (incluye POS).
- Marca del producto: campo brand_id. Canal de venta: team_id (Retail, E-commerce, Distribución – Mayoreo, Distribución – Dropship).
- Facturas de cliente: account.move con move_type out_invoice; vencidas: payment_state in [not_paid, partial] e invoice_date_due < hoy.
- Montos en GTQ: usa campos *_signed. Fechas siempre como AAAA-MM-DD.
Si un campo no existe, consulta odoo_fields antes de reintentar."""

provider = OdooOAuth()
mcp = FastMCP(
    name="Odoo Ventas Guate", instructions=INSTRUCTIONS, auth_server_provider=provider,
    auth=AuthSettings(issuer_url=AnyUrl(PUBLIC_URL), resource_server_url=AnyUrl(f"{PUBLIC_URL}/mcp"),
                      client_registration_options=ClientRegistrationOptions(enabled=True),
                      revocation_options=RevocationOptions(enabled=True)),
    host="0.0.0.0", port=int(os.environ.get("PORT", "8000")), stateless_http=True,
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
)


def _client() -> oc.Odoo:
    tok = get_access_token()
    d = unseal("access", tok.token) if tok else None
    if not d:
        raise oc.OdooError("Sesión no válida: vuelve a conectar el conector de Odoo")
    o = oc.Odoo(ODOO_URL, ODOO_DB, d["login"], d["key"], "xmlrpc")
    o._uid = d["uid"]
    o.readonly = not ALLOW_WRITE
    return o


async def _call(model: str, method: str, ids: list[int] | None = None, **kw) -> Any:
    o = _client()
    try:
        return await anyio.to_thread.run_sync(lambda: o.call(model, method, ids=ids, **kw))
    except oc.OdooError as e:
        return {"error": str(e)}


@mcp.tool()
async def odoo_whoami() -> Any:
    """Usuario de Odoo conectado, idioma, zona horaria y compañía."""
    o = _client()
    return await _call("res.users", "read", ids=[o._uid], fields=["name", "login", "company_id", "tz", "lang"])


@mcp.tool()
async def odoo_search(model: str, domain: list | None = None, fields: list[str] | None = None,
                      limit: int = 80, offset: int = 0, order: str | None = None) -> Any:
    """Busca y lee registros (search_read). domain en formato Odoo, ej. [["state","=","sale"]]. Máx. 500 por llamada."""
    kw: dict = {"domain": domain or [], "limit": min(limit, 500), "offset": offset}
    if fields:
        kw["fields"] = fields
    if order:
        kw["order"] = order
    return await _call(model, "search_read", **kw)


@mcp.tool()
async def odoo_count(model: str, domain: list | None = None) -> Any:
    """Cuenta registros que cumplen el dominio."""
    return await _call(model, "search_count", domain=domain or [])


@mcp.tool()
async def odoo_read(model: str, ids: list[int], fields: list[str] | None = None) -> Any:
    """Lee registros por ID."""
    return await _call(model, "read", ids=ids, **({"fields": fields} if fields else {}))


@mcp.tool()
async def odoo_group(model: str, groupby: list[str], aggregates: list[str] | None = None,
                     domain: list | None = None, order: str | None = None, limit: int | None = None) -> Any:
    """Totales agrupados en el servidor (read_group). groupby ej. ["partner_id"] o ["date:month"];
    aggregates ej. ["amount_total:sum","price_subtotal:sum"]. Devuelve __count por grupo."""
    res = await _call(model, "read_group", domain=domain or [], fields=aggregates or [], groupby=groupby,
                      orderby=order or False, limit=limit, lazy=False)
    if isinstance(res, list):
        for r in res:
            r.pop("__domain", None)
    return res


@mcp.tool()
async def odoo_fields(model: str, filter: str | None = None) -> Any:
    """Campos de un modelo (nombre, etiqueta, tipo, relación). filter busca por nombre o etiqueta."""
    res = await _call(model, "fields_get", attributes=["string", "type", "relation", "selection"])
    if isinstance(res, dict) and filter:
        f = filter.lower()
        res = {k: v for k, v in res.items() if f in k.lower() or f in str(v.get("string", "")).lower()}
    return res


@mcp.tool()
async def odoo_models(filter: str | None = None) -> Any:
    """Lista modelos de Odoo (ej. filter="sale")."""
    dom = ["|", ["model", "ilike", filter], ["name", "ilike", filter]] if filter else []
    return await _call("ir.model", "search_read", domain=dom, fields=["model", "name"], limit=200, order="model")


@mcp.tool()
async def odoo_name_search(model: str, text: str, limit: int = 10) -> Any:
    """Busca registros por nombre (clientes, productos, proveedores…). Devuelve [id, nombre]."""
    return await _call(model, "name_search", name=text, limit=limit)


if ALLOW_WRITE:
    @mcp.tool()
    async def odoo_create(model: str, values: dict) -> Any:
        """Crea un registro. Confirma con el usuario los valores antes de llamar."""
        return await _call(model, "create", vals_list=[values])

    @mcp.tool()
    async def odoo_write(model: str, ids: list[int], values: dict) -> Any:
        """Edita registros. Confirma con el usuario los cambios antes de llamar."""
        return await _call(model, "write", ids=ids, vals=values)

    @mcp.tool()
    async def odoo_execute(model: str, method: str, ids: list[int] | None = None, kwargs: dict | None = None) -> Any:
        """Ejecuta un método (ej. action_confirm). Confirma con el usuario antes de llamar."""
        return await _call(model, method, ids=ids, **(kwargs or {}))


# --------------------------------------------------------------------------- login page
PAGE = """<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Conectar Odoo · Ventas Guate</title><style>
:root{{--bg:#F5F3F7;--card:#fff;--ink:#1F1A24;--muted:#6B6372;--line:#DDD7E2;--acc:#714B67;--err:#9B2C2C}}
@media (prefers-color-scheme:dark){{:root{{--bg:#16131A;--card:#211C26;--ink:#EEE9F2;--muted:#A79FB0;--line:#3A3341;--acc:#C79BBE;--err:#F08A8A}}}}
*{{box-sizing:border-box}}body{{margin:0;min-height:100vh;display:grid;place-items:center;background:var(--bg);color:var(--ink);
font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;padding:16px}}
main{{width:100%;max-width:380px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:28px}}
h1{{font-size:20px;margin:0 0 4px}}p{{color:var(--muted);margin:0 0 20px;font-size:13.5px}}
label{{display:block;font-size:13px;font-weight:600;margin:14px 0 6px}}
input{{width:100%;padding:10px 12px;border:1px solid var(--line);border-radius:6px;background:transparent;color:var(--ink);font:inherit}}
input:focus{{outline:2px solid var(--acc);outline-offset:1px}}
button{{margin-top:22px;width:100%;padding:11px;border:0;border-radius:6px;background:var(--acc);color:#fff;font:600 15px system-ui;cursor:pointer}}
.err{{color:var(--err);font-size:13.5px;margin-top:14px}}small{{display:block;color:var(--muted);margin-top:16px;font-size:12px}}
</style></head><body><main><h1>Conectar Odoo</h1><p>Ventas Guate · entra con tu usuario de Odoo. Claude verá solo lo que tus permisos permiten.</p>
<form method="post"><input type="hidden" name="txn" value="{txn}">
<label for="login">Usuario (correo de Odoo)</label><input id="login" name="login" type="email" required autocomplete="username" value="{login}">
<label for="key">API key de Odoo</label><input id="key" name="key" type="password" required autocomplete="off">
<button type="submit">Conectar</button>{error}</form>
<small>La API key se crea en Odoo: tu nombre → Preferencias → Seguridad de la cuenta → Nueva API Key.</small></main></body></html>"""


@mcp.custom_route("/login", methods=["GET", "POST"])
async def login(request: Request) -> Response:
    if request.method == "GET":
        txn = request.query_params.get("txn", "")
        if not unseal("login", txn):
            return HTMLResponse("<p>El enlace venció. Vuelve a conectar desde Claude.</p>", status_code=400)
        return HTMLResponse(PAGE.format(txn=html.escape(txn), login="", error=""))
    form = await request.form()
    txn, login_, key = str(form.get("txn", "")), str(form.get("login", "")).strip(), str(form.get("key", "")).strip()
    t = unseal("login", txn)
    if not t:
        return HTMLResponse("<p>El enlace venció. Vuelve a conectar desde Claude.</p>", status_code=400)
    uid = await anyio.to_thread.run_sync(odoo_authenticate, login_, key)
    if not uid:
        return HTMLResponse(PAGE.format(txn=html.escape(txn), login=html.escape(login_),
                                        error='<div class="err">Usuario o API key incorrectos.</div>'), status_code=401)
    code = seal("code", {**{k: t[k] for k in ("c", "ru", "rx", "ch", "sc", "rs")},
                         "login": login_, "key": key, "uid": uid}, CODE_TTL)
    return RedirectResponse(construct_redirect_uri(t["ru"], code=code, state=t.get("st")), status_code=302)


@mcp.custom_route("/health", methods=["GET"])
async def health(request: Request) -> Response:
    return Response("ok")


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
