"""Prueba de punta a punta del MCP propio contra Odoo real (solo lectura).
Uso: con el servidor corriendo (MCP_ALLOW_LOCAL_REDIRECTS=1), TEST_LOGIN y TEST_KEY definidos:
    python3 mcp-server/test_flow.py http://localhost:8765
"""
import asyncio, base64, hashlib, json, os, secrets, sys, urllib.parse
import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

BASE = sys.argv[1].rstrip("/")
CB = "http://localhost:9999/cb"
ok = lambda c, m: print(("PASA " if c else "FALLA") + " · " + m) or c


async def main():
    async with httpx.AsyncClient(follow_redirects=False, timeout=60) as h:
        meta = (await h.get(f"{BASE}/.well-known/oauth-authorization-server")).json()
        ok("registration_endpoint" in meta, "metadatos OAuth publicados")
        bad = await h.post(meta["registration_endpoint"], json={"redirect_uris": ["https://evil.example/cb"], "token_endpoint_auth_method": "none"})
        ok(bad.status_code == 400, "rechaza redirect_uri ajeno a claude.ai")
        reg = (await h.post(meta["registration_endpoint"], json={"redirect_uris": [CB], "client_name": "prueba",
               "token_endpoint_auth_method": "client_secret_post", "grant_types": ["authorization_code", "refresh_token"]})).json()
        cid, csec = reg["client_id"], reg.get("client_secret")
        ok(bool(cid and csec), "registro dinámico de cliente")
        ver = secrets.token_urlsafe(48)
        ch = base64.urlsafe_b64encode(hashlib.sha256(ver.encode()).digest()).decode().rstrip("=")
        r = await h.get(meta["authorization_endpoint"], params={"response_type": "code", "client_id": cid, "redirect_uri": CB,
                        "code_challenge": ch, "code_challenge_method": "S256", "state": "xyz"})
        login_url = r.headers.get("location", "")
        ok(r.status_code == 302 and "/login?txn=" in login_url, "authorize redirige a la página de inicio de sesión")
        txn = urllib.parse.parse_qs(urllib.parse.urlparse(login_url).query)["txn"][0]
        page = await h.get(login_url)
        ok(page.status_code == 200 and "API key" in page.text, "página de inicio de sesión")
        wrong = await h.post(f"{BASE}/login", data={"txn": txn, "login": os.environ["TEST_LOGIN"], "key": "x" * 40})
        ok(wrong.status_code == 401, "rechaza API key incorrecta")
        good = await h.post(f"{BASE}/login", data={"txn": txn, "login": os.environ["TEST_LOGIN"], "key": os.environ["TEST_KEY"]})
        q = urllib.parse.parse_qs(urllib.parse.urlparse(good.headers.get("location", "")).query)
        ok(good.status_code == 302 and q.get("state") == ["xyz"] and "code" in q, "login correcto devuelve código a Claude")
        tok = (await h.post(meta["token_endpoint"], data={"grant_type": "authorization_code", "code": q["code"][0], "redirect_uri": CB,
               "client_id": cid, "client_secret": csec, "code_verifier": ver})).json()
        ok("access_token" in tok and "refresh_token" in tok, "intercambio de código por token (PKCE)")
        badpk = await h.post(meta["token_endpoint"], data={"grant_type": "authorization_code", "code": q["code"][0], "redirect_uri": CB,
               "client_id": cid, "client_secret": csec, "code_verifier": "otro" * 12})
        ok(badpk.status_code == 400, "rechaza code_verifier incorrecto")
        ref = (await h.post(meta["token_endpoint"], data={"grant_type": "refresh_token", "refresh_token": tok["refresh_token"],
               "client_id": cid, "client_secret": csec})).json()
        ok("access_token" in ref, "renovación con refresh token (revalida la key en Odoo)")
        noauth = await h.post(f"{BASE}/mcp", json={})
        ok(noauth.status_code == 401, "MCP sin token responde 401")

    async with streamablehttp_client(f"{BASE}/mcp", headers={"Authorization": f"Bearer {ref['access_token']}"}) as (r, w, _):
        async with ClientSession(r, w) as s:
            await s.initialize()
            tools = [t.name for t in (await s.list_tools()).tools]
            ok("odoo_group" in tools and "odoo_create" not in tools, f"herramientas: {', '.join(tools)}")
            who = await s.call_tool("odoo_whoami", {})
            ok("login" in who.content[0].text, "odoo_whoami: " + json.loads(who.content[0].text)["name"] if who.content else "")
            g = await s.call_tool("odoo_group", {"model": "crm.team", "groupby": ["name"], "limit": 5})
            ok(not g.isError and "__count" in g.content[0].text, "odoo_group devuelve totales")
            c = await s.call_tool("odoo_count", {"model": "res.partner", "domain": [["customer_rank", ">", 0]]})
            ok(not c.isError, "odoo_count: " + c.content[0].text)
            w_ = await s.call_tool("odoo_search", {"model": "res.partner", "domain": [["id", "=", 1]], "fields": ["name"]})
            ok(not w_.isError, "odoo_search")


asyncio.run(main())
