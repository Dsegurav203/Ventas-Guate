#!/usr/bin/env python3
"""Valida prodigee_propuesta.json: HTML bien formado, plantilla, longitudes, sin precios (Q+dígitos), 90–180 palabras."""
import json, re, html, sys
from html.parser import HTMLParser

VOID = {"br", "img", "hr"}
class Chk(HTMLParser):
    def __init__(s): super().__init__(); s.st=[]; s.err=[]
    def handle_starttag(s,t,a):
        if t not in VOID: s.st.append(t)
    def handle_endtag(s,t):
        if not s.st or s.st[-1]!=t: s.err.append(f"cierre {t} inesperado (pila {s.st})")
        else: s.st.pop()

prop = json.load(open("prodigee_propuesta.json"))
bad = 0; wc = []
for p in prop:
    e = []; h = p["html"]
    c = Chk(); c.feed(h); c.close()
    if c.err or c.st: e.append(f"HTML: {c.err} abiertos={c.st}")
    texto = html.unescape(re.sub(r"<[^>]+>", " ", h)); n = len(texto.split()); wc.append(n)
    if not 90 <= n <= 180: e.append(f"palabras={n}")
    if len(p["seo_title"]) > 60: e.append(f"seo_title {len(p['seo_title'])}")
    if len(p["seo_description"]) > 155: e.append(f"meta {len(p['seo_description'])}")
    for campo in (h, p["seo_title"], p["seo_description"]):
        if re.search(r"Q\s?\d", campo): e.append("precio Q+dígito")
    if h.count("<h2>Características</h2>") != 1 or h.count("<h2>Compatibilidad</h2>") != 1: e.append("faltan H2")
    nli = len(re.findall(r"<li>", h.split("<h2>Compatibilidad</h2>")[0]))
    if not 4 <= nli <= 7: e.append(f"viñetas={nli}")
    if not h.startswith("<p>") or "Producto original con 1 año de garantía. Envío a toda Guatemala con pago contra entrega, o cómpralo en nuestra tienda en zona 13, Ciudad de Guatemala." not in h: e.append("intro/cierre")
    intro = re.match(r"<p>(.*?)</p>", h).group(1)
    if not 1 <= len(re.findall(r"[.!?](\s|$)", intro)) <= 2: e.append("intro no es 1-2 frases")
    if e: bad += 1; print(p["title"], e)
print(f"{len(prop)} fichas, {bad} con errores; palabras min {min(wc)} max {max(wc)} prom {sum(wc)/len(wc):.0f}")
sys.exit(1 if bad else 0)
