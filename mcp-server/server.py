#!/usr/bin/env python3
"""MCP propio de Ventas Guate: conector remoto de Odoo para el chat de claude.ai.

- Cada persona inicia sesión con SU usuario y API key de Odoo: Odoo aplica sus permisos.
- OAuth 2.1 con registro dinámico (lo que exige claude.ai) y sin base de datos: clientes,
  códigos y tokens van cifrados (Fernet) con MCP_SECRET_KEY. Cambiar la clave cierra todas
  las sesiones. Revocar la API key en Odoo corta el acceso de esa persona de inmediato.
- Escritura solo si MCP_ALLOW_WRITE=1 y únicamente en los modelos de MCP_WRITE_MODELS (por defecto productos);
  aun así Odoo valida los permisos de cada usuario. Imágenes: el servidor descarga la URL y la normaliza.

Variables: ODOO_URL, ODOO_DB, MCP_PUBLIC_URL (https://…), MCP_SECRET_KEY (Fernet),
           MCP_ALLOW_WRITE (0/1), MCP_ALLOW_LOCAL_REDIRECTS (0/1, solo pruebas), PORT.
"""
from __future__ import annotations

import base64, hashlib, hmac, html, json, os, sys, time, urllib.parse, urllib.request, xmlrpc.client
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
WRITE_MODELS = {m.strip() for m in os.environ.get(
    "MCP_WRITE_MODELS", "product.template,product.product,product.category,product.brand").replace(";", ",").split(",") if m.strip()}
IMAGE_MODELS = {"product.template", "product.product"} & WRITE_MODELS
# Modelos de configuración: solo usuarios con Ajustes (base.group_system) en Odoo.
ADMIN_WRITE_MODELS = {m.strip() for m in os.environ.get(
    "MCP_ADMIN_WRITE_MODELS", "stock.warehouse,stock.location,stock.picking,res.users").replace(";", ",").split(",") if m.strip()}
NO_CREATE_MODELS = {"res.users", "stock.picking"}             # se editan, no se crean desde el chat
FIELD_LIMITS = {"res.users": {"property_warehouse_id"}}      # en usuarios solo el almacén predeterminado
NEVER_WRITE = {"ir.rule", "ir.model.access", "res.groups", "ir.config_parameter", "res.users.apikeys"}
# Permisos adicionales por persona (login de Odoo) para quienes no son administradores. Odoo igual valida sus permisos.
# MCP_ROLE_GRANTS (JSON) reemplaza este valor por defecto.
ROLE_GRANTS = json.loads(os.environ.get("MCP_ROLE_GRANTS") or json.dumps({
    "logistica@ventasguate.com": {   # Mayra González: compras (pedido semanal en borrador)
        "models": ["purchase.order", "purchase.order.line"], "actions": []},
    "contabilidad@ventasguate.com": {  # Wilber (Auxiliar Contable): costeo de pólizas y tasa de cambio
        "models": ["stock.landed.cost", "stock.landed.cost.lines", "stock.valuation.adjustment.lines", "res.currency.rate"],
        "actions": ["stock.landed.cost.compute_landed_cost", "stock.landed.cost.button_validate"]},
}))
# Administradores de Odoo (Ajustes): acceso completo desde el chat (cualquier modelo, campo, acción y borrado).
ADMIN_FULL = os.environ.get("MCP_ADMIN_FULL", "1") == "1"
ACTIONS = {tuple(a.strip().rsplit(".", 1)) for a in os.environ.get(
    "MCP_ACTIONS", "stock.picking.action_cancel").replace(";", ",").split(",") if a.strip()}
# Rol contabilidad (account.group_account_manager, sin Ajustes): escritura y acciones solo en conciliación y pagos.
ACCOUNTING_GROUP = "account.group_account_manager"
ACCOUNTING_MODELS = {m.strip() for m in os.environ.get("MCP_ACCOUNTING_MODELS",
    "account.bank.statement,account.bank.statement.line,account.move,account.move.line,account.payment,"
    "account.partial.reconcile,account.full.reconcile,account.reconcile.model").replace(";", ",").split(",") if m.strip()}
# Métodos públicos de conciliación (Odoo 18): reconcile, remove_move_reconcile, action_unreconcile_match_entries y
# action_register_payment (account.move.line); action_undo_reconciliation (account.bank.statement.line).
ACCOUNTING_METHODS = {m.strip() for m in os.environ.get("MCP_ACCOUNTING_METHODS",
    "reconcile,remove_move_reconcile,action_unreconcile_match_entries,action_post,action_register_payment,"
    "action_payment_items_register_payment,action_undo_reconciliation,button_validate_or_action").replace(";", ",").split(",") if m.strip()}
ACCOUNTING_FORBIDDEN = {"account.account", "account.journal", "account.tax", "res.company", "res.users", "res.groups"}
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
    o.readonly = not ALLOW_WRITE  # además, cada herramienta de escritura valida WRITE_MODELS
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
async def odoo_export(model: str, fields: list[str], domain: list | None = None, order: str | None = None,
                      limit: int = 500) -> Any:
    """Exporta registros como en "Exportar" de Odoo: admite campos relacionados con "/", ej. "partner_id/id",
    "seller_ids/partner_id", "seller_ids/price". Útil para líneas uno-a-muchos. Máx. 2000 registros por llamada."""
    ids = await _call(model, "search", domain=domain or [], limit=min(limit, 2000), **({"order": order} if order else {}))
    if not isinstance(ids, list):
        return ids
    if not ids:
        return []
    res = await _call(model, "export_data", ids=ids, fields_to_export=fields)
    if isinstance(res, dict) and "datas" in res:
        return [dict(zip(fields, row)) for row in res["datas"]]
    return res


@mcp.tool()
async def odoo_name_search(model: str, text: str, limit: int = 10) -> Any:
    """Busca registros por nombre (clientes, productos, proveedores…). Devuelve [id, nombre]."""
    return await _call(model, "name_search", name=text, limit=limit)


def _login() -> str:
    tok = get_access_token()
    d = unseal("access", tok.token) if tok else None
    return (d or {}).get("login", "").lower()


def _grant() -> dict:
    g = ROLE_GRANTS.get(_login(), {})
    return {"models": set(g.get("models", [])),
            "actions": {tuple(a.rsplit(".", 1)) for a in g.get("actions", [])}}


async def _has_group(xml_id: str) -> bool:
    o = _client()
    r = await _call("res.users", "has_group", ids=[o._uid], group_ext_id=xml_id)
    return r is True


async def _is_admin() -> bool:
    return await _has_group("base.group_system")


async def _is_accounting() -> bool:
    """Rol contabilidad: Contabilidad / Administrador en Odoo y sin Ajustes."""
    return not await _is_admin() and await _has_group(ACCOUNTING_GROUP)


def _accounting_forbidden(model: str) -> bool:
    return model in ACCOUNTING_FORBIDDEN or model.startswith("ir.")


def _short(v: Any) -> Any:
    if isinstance(v, str) and len(v) > 300:
        return v[:300] + f"…({len(v)} car.)"
    if isinstance(v, dict):
        return {k: _short(x) for k, x in v.items()}
    if isinstance(v, list):
        return [_short(x) for x in v[:200]]
    return v


def _audit(model: str, method: str, ids: list[int] | None = None, values: Any = None, result: Any = None) -> None:
    """Auditoría del rol contabilidad: una línea JSON por escritura en stdout (Cloud Logging la indexa)."""
    o = _client()
    ok = not (isinstance(result, dict) and "error" in result)
    print(json.dumps({"severity": "NOTICE", "message": f"auditoria contabilidad {model}.{method}",
                      "audit": "contabilidad", "login": _login(), "uid": o._uid, "model": model, "method": method,
                      "ids": ids, "values": _short(values), "ok": ok,
                      "error": None if ok else str(result.get("error"))[:500]}, default=str, ensure_ascii=False), flush=True)


async def _check_write(model: str, values: dict | None = None, create: bool = False) -> dict | None:
    if ADMIN_FULL and await _is_admin():
        return None
    if model in NEVER_WRITE:
        return {"error": f"'{model}' es configuración de seguridad: no se modifica desde el chat. Hazlo en Claude Code con revisión."}
    if model in WRITE_MODELS or model in _grant()["models"]:
        return None
    if model in ACCOUNTING_MODELS or _accounting_forbidden(model):
        if await _is_accounting():
            if _accounting_forbidden(model) or model not in ACCOUNTING_MODELS:
                return {"error": f"Rol contabilidad: '{model}' es configuración contable o del sistema; no se modifica desde el chat"}
            return None
    if model in ADMIN_WRITE_MODELS:
        if not await _is_admin():
            return {"error": f"Solo administradores de Odoo (Ajustes) pueden modificar '{model}' desde el chat"}
        if create and model in NO_CREATE_MODELS:
            return {"error": f"No se crean registros de '{model}' desde el chat"}
        allowed = FIELD_LIMITS.get(model)
        if allowed and values and set(values) - allowed:
            return {"error": f"En '{model}' solo se pueden editar: {', '.join(sorted(allowed))}"}
        return None
    return {"error": f"Escritura no permitida en '{model}'. Modelos permitidos: "
                     f"{', '.join(sorted(WRITE_MODELS))}; solo administradores: {', '.join(sorted(ADMIN_WRITE_MODELS))}"}


def _safe_url(url: str) -> str | None:
    """Solo http(s) a IPs públicas (evita que el servidor lea su red interna o el metadata server)."""
    import ipaddress, socket
    u = urllib.parse.urlparse(url)
    if u.scheme not in ("http", "https") or not u.hostname:
        return "La URL debe empezar con http:// o https://"
    try:
        infos = socket.getaddrinfo(u.hostname, u.port or (443 if u.scheme == "https" else 80))
    except socket.gaierror:
        return "No se pudo resolver el dominio de la imagen"
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if not ip.is_global:
            return "URL no permitida"
    return None


def _download(url: str, max_bytes: int, require_image: bool = False) -> tuple[bytes, str, str]:
    """Descarga una URL pública (re-valida redirecciones). Devuelve (datos, content-type, nombre sugerido)."""
    class _SafeRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            if _safe_url(newurl):
                raise ValueError("redirección a una URL no permitida")
            return super().redirect_request(req, fp, code, msg, headers, newurl)
    if err := _safe_url(url):
        raise ValueError(err)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (VentasGuate MCP)"})
    with urllib.request.build_opener(_SafeRedirect).open(req, timeout=30) as r:
        ctype = (r.headers.get("Content-Type") or "application/octet-stream").split(";")[0].strip()
        if require_image and not ctype.startswith("image/"):
            raise ValueError(f"La URL no es una imagen ({ctype})")
        data = r.read(max_bytes + 1)
        if len(data) > max_bytes:
            raise ValueError(f"Archivo mayor a {max_bytes // 1_000_000} MB")
        name = ""
        cd = r.headers.get("Content-Disposition") or ""
        if "filename=" in cd:
            name = cd.split("filename=")[-1].strip().strip('"').split(";")[0]
        if not name:
            name = urllib.parse.unquote(urllib.parse.urlparse(r.geturl()).path.rsplit("/", 1)[-1]) or "archivo"
        return data, ctype, name


def _normalize_image(raw: bytes) -> tuple[bytes, bytes, tuple[int, int]]:
    """Estándar Ventas Guate: 1200x1200, fondo blanco, producto al 90 %, JPEG < 350 KB. Devuelve (jpeg, miniatura, tamaño original)."""
    import io
    from PIL import Image, ImageOps
    im = Image.open(io.BytesIO(raw))
    im = ImageOps.exif_transpose(im)
    orig = im.size
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        bg.alpha_composite(im)
        im = bg
    im = im.convert("RGB")
    k = min(1080 / im.width, 1080 / im.height)  # producto al 90 % del lienzo (agranda o reduce)
    im = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
    canvas = Image.new("RGB", (1200, 1200), (255, 255, 255))
    canvas.paste(im, ((1200 - im.width) // 2, (1200 - im.height) // 2))
    for q in (88, 82, 76, 70, 62, 55):
        buf = io.BytesIO()
        canvas.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
        if buf.tell() < 350_000:
            break
    thumb = canvas.copy()
    thumb.thumbnail((320, 320))
    tb = io.BytesIO()
    thumb.save(tb, "JPEG", quality=80)
    return buf.getvalue(), tb.getvalue(), orig


if ALLOW_WRITE:
    @mcp.tool()
    async def odoo_create(model: str, values: dict | list[dict]) -> Any:
        """Crea uno o varios registros (values = dict o lista de dicts, máx. 200). Administradores de Odoo: cualquier modelo.
        Contabilidad / Administrador: solo extractos, líneas de extracto, asientos, apuntes, pagos, conciliaciones y modelos
        de conciliación (nunca plan de cuentas, diarios, impuestos, compañía, usuarios ni ir.*). Demás usuarios: solo productos.
        Antes de llamar, muestra al usuario los valores y espera su confirmación. Para imágenes usa odoo_set_image_from_url."""
        vals_list = values if isinstance(values, list) else [values]
        if len(vals_list) > 200:
            return {"error": "Máximo 200 registros por llamada; divide en bloques"}
        admin = ADMIN_FULL and await _is_admin()
        for v in vals_list:
            if err := await _check_write(model, v, create=True):
                return err
            if not admin and any(k.startswith("image_") for k in v):
                return {"error": "Para imágenes usa odoo_set_image_from_url"}
        res = await _call(model, "create", vals_list=vals_list)
        if model in ACCOUNTING_MODELS and not admin and await _is_accounting():
            _audit(model, "create", res if isinstance(res, list) else None, vals_list, res)
        return res

    @mcp.tool()
    async def odoo_write(model: str, ids: list[int], values: dict) -> Any:
        """Edita registros (varios ids a la vez). Administradores de Odoo: cualquier modelo y campo, incluido image_1920 en
        base64 para fotos subidas al chat. Contabilidad / Administrador: solo account.bank.statement(.line), account.move(.line),
        account.payment, account.partial/full.reconcile y account.reconcile.model (queda auditado). Demás usuarios: solo
        productos. Archivar = {"active": false}.
        Antes de llamar, muestra al usuario los cambios y espera su confirmación."""
        if err := await _check_write(model, values):
            return err
        if any(k.startswith("image_") for k in values) and not (ADMIN_FULL and await _is_admin()):
            return {"error": "Para imágenes usa odoo_set_image_from_url"}
        res = await _call(model, "write", ids=ids, vals=values)
        if model in ACCOUNTING_MODELS and await _is_accounting():
            _audit(model, "write", ids, values, res)
        return res

    @mcp.tool()
    async def odoo_action(model: str, method: str, ids: list[int], kwargs: dict | None = None) -> Any:
        """Ejecuta un método de Odoo sobre registros (ej. action_cancel, action_confirm, button_validate, action_post).
        Administradores de Odoo: cualquier acción. Contabilidad / Administrador: en los modelos de conciliación y pagos
        (account.bank.statement(.line), account.move(.line), account.payment, account.*reconcile*) solo reconcile,
        remove_move_reconcile, action_unreconcile_match_entries, action_post, action_register_payment,
        action_undo_reconciliation y button_validate_or_action (queda auditado; nunca unlink). Otros usuarios: solo las de su
        función (ej. costeo: compute_landed_cost, button_validate en stock.landed.cost).
        Antes de llamar, muestra al usuario los registros y la acción y espera su confirmación."""
        if (model, method) in _grant()["actions"]:
            return await _call(model, method, ids=ids, **(kwargs or {}))
        if await _is_accounting():
            if method == "unlink" or method.startswith("_"):
                return {"error": "Rol contabilidad: no se eliminan registros ni se llaman métodos privados desde el chat"}
            if model not in ACCOUNTING_MODELS or _accounting_forbidden(model):
                return {"error": f"Rol contabilidad: acciones solo en {', '.join(sorted(ACCOUNTING_MODELS))}"}
            if method not in ACCOUNTING_METHODS:
                return {"error": f"Rol contabilidad: método no permitido. Permitidos: {', '.join(sorted(ACCOUNTING_METHODS))}"}
            res = await _call(model, method, ids=ids, **(kwargs or {}))
            _audit(model, method, ids, kwargs, res)
            return res
        if not await _is_admin():
            return {"error": "Solo administradores de Odoo (Ajustes) pueden ejecutar esta acción desde el chat"}
        if not ADMIN_FULL and (model, method) not in ACTIONS:
            return {"error": f"Acción no permitida. Permitidas: {', '.join(f'{m}.{a}' for m, a in sorted(ACTIONS))}"}
        return await _call(model, method, ids=ids, **(kwargs or {}))

    @mcp.tool()
    async def odoo_unlink(model: str, ids: list[int]) -> Any:
        """Elimina registros (solo administradores de Odoo; el rol contabilidad nunca elimina). Prefiere archivar ({"active": false}) cuando el modelo lo permita.
        Antes de llamar, muestra al usuario exactamente qué se va a borrar y espera su confirmación explícita."""
        if not (ADMIN_FULL and await _is_admin()):
            return {"error": "Solo administradores de Odoo (Ajustes) pueden eliminar registros desde el chat"}
        return await _call(model, "unlink", ids=ids)

    @mcp.tool()
    async def odoo_post_note(model: str, record_id: int, body: str, internal: bool = True,
                             partner_ids: list[int] | None = None, html: bool = False) -> Any:
        """Publica en el historial (chatter) de un registro. internal=True: nota interna (no se envía a nadie, salvo los
        partner_ids que menciones, que reciben notificación). internal=False: mensaje que se ENVÍA por correo a los
        seguidores del registro (clientes/proveedores incluidos): confirma con el usuario antes. html=True si body es HTML."""
        kw: dict = {"body": body, "message_type": "comment",
                    "subtype_xmlid": "mail.mt_note" if internal else "mail.mt_comment", "body_is_html": html}
        if partner_ids:
            kw["partner_ids"] = partner_ids
        res = await _call(model, "message_post", ids=[record_id], **kw)
        if model in ACCOUNTING_MODELS and await _is_accounting():
            _audit(model, "message_post", [record_id], {"internal": internal, "partner_ids": partner_ids, "body": body}, res)
        return {"ok": True, "message_id": res} if isinstance(res, int) else res

    @mcp.tool()
    async def odoo_register_payment(invoice_ids: list[int], amount: float | None = None, payment_date: str | None = None,
                                    journal_id: int | None = None, memo: str | None = None) -> Any:
        """Registra el pago de facturas de cliente o proveedor (asistente "Registrar pago" de Odoo). Sin amount paga el
        saldo completo. journal_id = diario de banco/caja (búscalo en account.journal type in bank,cash). Fecha AAAA-MM-DD.
        Requiere permisos de facturación en Odoo (el rol contabilidad queda auditado). Antes de llamar, muestra facturas, monto, fecha y banco y espera confirmación."""
        o = _client()
        ok = await _call("res.users", "has_group", ids=[o._uid], group_ext_id="account.group_account_invoice")
        if ok is not True:
            return {"error": "Tu usuario de Odoo no tiene permisos de facturación para registrar pagos"}
        ctx = {"active_model": "account.move", "active_ids": invoice_ids}
        vals: dict = {}
        if amount is not None:
            vals["amount"] = amount
        if payment_date:
            vals["payment_date"] = payment_date
        if journal_id:
            vals["journal_id"] = journal_id
        if memo:
            vals["communication"] = memo
        wiz = await _call("account.payment.register", "create", vals_list=[vals], context=ctx)
        if isinstance(wiz, dict):
            return wiz
        res = await _call("account.payment.register", "action_create_payments", ids=wiz, context=ctx)
        if await _is_accounting():
            _audit("account.move", "register_payment", invoice_ids, vals, res)
        if isinstance(res, dict) and "error" in res:
            return res
        return await _call("account.move", "read", ids=invoice_ids,
                           fields=["name", "partner_id", "amount_total", "amount_residual", "payment_state"])

    @mcp.tool()
    async def odoo_attach_from_url(model: str, record_id: int, url: str, filename: str | None = None) -> Any:
        """Descarga un archivo desde una URL pública o un link temporal (ej. link de descarga de Dropbox) y lo adjunta al
        registro (PDF de factura, póliza, cotización, Excel…). Máx. 20 MB. Para imágenes de producto usa odoo_set_image_from_url."""
        try:
            data, ctype, name = await anyio.to_thread.run_sync(lambda: _download(url, 20_000_000))
        except Exception as e:
            return {"error": f"No se pudo descargar: {e}"}
        att = await _call("ir.attachment", "create", vals_list=[{
            "name": filename or name, "datas": base64.b64encode(data).decode(), "mimetype": ctype,
            "res_model": model, "res_id": record_id}])
        if isinstance(att, dict):
            return att
        return {"ok": True, "attachment_id": att[0], "nombre": filename or name, "kb": round(len(data) / 1024), "tipo": ctype}

    if IMAGE_MODELS:
        from mcp.server.fastmcp import Image as McpImage

        @mcp.tool()
        async def odoo_set_image_from_url(record_id: int, url: str, model: str = "product.template") -> Any:
            """Descarga una imagen desde una URL pública, la normaliza al estándar de Ventas Guate (1200x1200, fondo blanco,
            JPEG < 350 KB) y la carga como imagen principal del producto. Devuelve una miniatura: revísala y confirma que es
            el mismo modelo y color antes de dar por buena la carga. Usa preferentemente el sitio oficial de la marca."""
            if model not in IMAGE_MODELS:
                return {"error": f"Solo se cargan imágenes en {', '.join(sorted(IMAGE_MODELS))}"}
            try:
                raw, _, _ = await anyio.to_thread.run_sync(lambda: _download(url, 15_000_000, require_image=True))
                jpeg, thumb, orig = await anyio.to_thread.run_sync(_normalize_image, raw)
            except Exception as e:
                return {"error": f"No se pudo usar la imagen: {e}"}
            res = await _call(model, "write", ids=[record_id], vals={"image_1920": base64.b64encode(jpeg).decode()})
            if isinstance(res, dict) and "error" in res:
                return res
            name = await _call(model, "read", ids=[record_id], fields=["display_name"])
            info = {"ok": True, "producto": name[0]["display_name"] if isinstance(name, list) and name else record_id,
                    "original_px": f"{orig[0]}x{orig[1]}", "final": "1200x1200", "kb": round(len(jpeg) / 1024)}
            if max(orig) < 600:
                info["aviso"] = "Imagen original de baja resolución (<600 px): buscar una mejor si existe"
            return [json.dumps(info, ensure_ascii=False), McpImage(data=thumb, format="jpeg")]


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
