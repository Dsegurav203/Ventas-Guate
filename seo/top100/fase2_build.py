"""Fase 2: normaliza 53 descripciones (60-150 palabras) sin agregar datos técnicos nuevos."""
import json, re
B = json.load(open("fase2_base.json"))
CIERRE = "<p>Producto original con 1 año de garantía. Envío a toda Guatemala con pago contra entrega, o cómpralo en nuestra tienda en zona 13, Ciudad de Guatemala.</p>"
def compat(t):
    tl = t.lower()
    if "galaxy s25 ultra" in tl: return ["Samsung Galaxy S25 Ultra"]
    if "targus safeport max" in tl: return ["iPad A16 (11.ª gen.) de 11\"", "iPad (10.ª gen.) de 10.9\""]
    if any(k in tl for k in ["dime", "smokin", "vibe beam", "vibe buds", "colorbuds", "cassette"]):
        return ["Teléfonos, tablets y computadoras con Bluetooth (iPhone y Android)"]
    return None
out = []
for r in B:
    h = r["html"]
    # limpiar atributos pegados de otras herramientas
    h = re.sub(r'\s(data-[\w-]+|dir|class)=("[^"]*"|\'[^\']*\')', "", h)
    h = re.sub(r'<span style=(\"[^\"]*\"|\'[^\']*\')>', "<span>", h)
    h = re.sub(r"<span>([^<]*)</span>", r"\1", h)
    h = re.sub(r"<span>([^<]*)</span>", r"\1", h)
    h = re.sub(r"<p>\s*</p>", "", h)
    # encabezados a H2
    h = re.sub(r"<h[13]>\s*Características técnicas\s*</h[13]>", "<h2>Características</h2>", h)
    h = re.sub(r"<h3>(.*?)</h3>", r"<h2>\1</h2>", h)
    h = re.sub(r"<h1>(.*?)</h1>", r"<h2>\1</h2>", h)
    # envío viejo (Q35 / 1 día) -> se reemplaza por el cierre estándar
    h = re.sub(r"<p>Envío a toda Guatemala por Q35[^<]*</p>", "", h)
    cambios = []
    c = compat(r["title"])
    if c and "ompatib" not in h:
        h += "\n<h2>Compatibilidad</h2>\n<ul>\n" + "".join(f"<li>{x}</li>\n" for x in c) + "</ul>"
        cambios.append("compatibilidad")
    if "contra entrega" not in h:
        h = h.rstrip() + "\n" + CIERRE
        cambios.append("cierre garantía/envío")
    if h != r["html"]:
        out.append({"id": r["id"], "title": r["title"], "html": h, "cambios": cambios, "galaxy_week": "GALAXY WEEK" in h})
json.dump(out, open("fase2_propuesta.json", "w"), ensure_ascii=False, indent=1)
print(len(out), "cambian;", sum(o["galaxy_week"] for o in out), "con banner Galaxy Week")
