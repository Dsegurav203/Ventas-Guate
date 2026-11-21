"""Genera las mutaciones aprobadas (A, B) a partir del respaldo de Shopify.
Entrada: seo/seminuevos_seo/respaldo_2026-11-21.json  (lista de {id,title,handle,seo:{title,description}})
Salida:  seo/seminuevos_seo/lote_<n>.json  (variables {"p":[ProductUpdateInput…]} de hasta 25 productos)
         seo/seminuevos_seo/aplicar_resumen.json
"""
import json, os, re

AQUI = os.path.dirname(os.path.abspath(__file__))
prods = json.load(open(f"{AQUI}/respaldo_2026-11-21.json"))

TITULOS_A = {
    "IPHONE 15 PRO 256GB TITANIO NATURAL SEMINUEVO": "iPhone 15 Pro 256GB Titanio Natural Seminuevo",
    "IPHONE 15 PRO MAX 256GB TITANIO NATURAL SEMINUEVO": "iPhone 15 Pro Max 256GB Titanio Natural Seminuevo",
    "IPHONE 15 PRO MAX 1TB TITANIO NEGRO SEMINUEVO": "iPhone 15 Pro Max 1TB Titanio Negro Seminuevo",
    "iPhone Se 2020 64GB Rojo Seminuevo": "iPhone SE 2020 64GB Rojo Seminuevo",
    "iPhone 16E 128GB Blanco Seminuevo": "iPhone 16e 128GB Blanco Seminuevo",
    "iPhone 17E 256GB Rosa Seminuevo": "iPhone 17e 256GB Rosa Seminuevo",
}
PAT = re.compile(r"^(?P<modelo>.+?)\s+(?P<cap>\d+\s?(?:GB|TB))\s+(?P<color>.+?)\s+Seminuevo$")

entradas, resumen, sin_patron = [], [], []
for p in prods:
    titulo = TITULOS_A.get(p["title"], p["title"])
    cambio = {"id": p["id"]}
    if titulo != p["title"]:
        cambio["title"] = titulo
    seo = p.get("seo") or {}
    if not seo.get("title") and not seo.get("description"):
        m = PAT.match(titulo)
        if not m:
            sin_patron.append(titulo)
        else:
            mod, cap, col = m["modelo"], m["cap"].replace(" ", ""), m["color"]
            t = f"{titulo} | Ventas Guate"
            if len(t) > 60:
                t = titulo
            d = (f"{mod} de {cap} en {col.lower()}, seminuevo revisado por nuestro equipo técnico. "
                 "30 días de garantía y envío a toda Guatemala con pago contra entrega.")
            if len(d) > 155:
                d = (f"{mod} de {cap} en {col.lower()}, seminuevo revisado. "
                     "30 días de garantía y envío a toda Guatemala con pago contra entrega.")
            cambio["seo"] = {"title": t, "description": d}
    if len(cambio) > 1:
        entradas.append(cambio)
        resumen.append({"id": p["id"], "antes": p["title"], **{k: v for k, v in cambio.items() if k != "id"}})

for i in range(0, len(entradas), 25):
    json.dump({"p": entradas[i:i + 25]}, open(f"{AQUI}/lote_{i // 25 + 1}.json", "w"), ensure_ascii=False)
json.dump(resumen, open(f"{AQUI}/aplicar_resumen.json", "w"), ensure_ascii=False, indent=1)
print(f"{len(entradas)} productos en {(len(entradas) + 24) // 25} lotes; títulos A: "
      f"{sum(1 for e in entradas if 'title' in e)}; SEO B: {sum(1 for e in entradas if 'seo' in e)}; sin patrón: {sin_patron}")
print("meta más larga:", max((len(e['seo']['description']) for e in entradas if 'seo' in e), default=0))
