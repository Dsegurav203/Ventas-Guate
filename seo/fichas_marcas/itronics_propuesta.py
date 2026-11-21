"""Genera la propuesta de descripciones iTronics (iPhone seminuevos).

Entradas:
  itronics_actual.tsv  id|title|primer párrafo actual (leído de Shopify 2026-11-21)
  apple_tab.json       columnas extraídas de https://www.apple.com/la/iphone/compare/
Salidas: itronics_specs_modelos.json, itronics_respaldo.json, itronics_propuesta.json
Uso: python3 seo/fichas_marcas/itronics_propuesta.py <apple_tab.json>
"""
import json, re, sys, html
from pathlib import Path

D = Path(__file__).parent
FUENTE = "https://www.apple.com/la/iphone/compare/"
WA = "https://wa.me/50240273277?text=Hola%2C%20quiero%20ver%20fotos%20reales"
SUFIJO = ('</p><p><strong>Cuenta con 30 días de garantía.</strong></p><p>Imagen de referencia. '
          'Si deseas ver fotos reales del equipo, escríbenos a nuestro '
          f'<a href="{WA}">WhatsApp 4027-3277</a>.</p>')

# Nombre en la descripción -> nombre oficial Apple (columna del comparador)
MODELOS = {
    "iPhone 8 Plus": "iPhone 8 Plus", "iPhone X": "iPhone X", "iPhone XS": "iPhone XS",
    "iPhone XS Max": "iPhone XS Max", "iPhone XR": "iPhone XR",
    "iPhone SE 2020": "iPhone SE (2.ª generación)",
    "iPhone 11": "iPhone 11", "iPhone 11 Pro": "iPhone 11 Pro", "iPhone 11 Pro Max": "iPhone 11 Pro Max",
    "iPhone 12 mini": "iPhone 12 mini", "iPhone 12": "iPhone 12", "iPhone 12 Pro": "iPhone 12 Pro",
    "iPhone 12 Pro Max": "iPhone 12 Pro Max", "iPhone 13 mini": "iPhone 13 mini", "iPhone 13": "iPhone 13",
    "iPhone 13 Pro": "iPhone 13 Pro", "iPhone 13 Pro Max": "iPhone 13 Pro Max", "iPhone 14": "iPhone 14",
    "iPhone 14 Plus": "iPhone 14 Plus", "iPhone 14 Pro": "iPhone 14 Pro", "iPhone 15": "iPhone 15",
    "iPhone 15 Plus": "iPhone 15 Plus", "iPhone 15 Pro": "iPhone 15 Pro", "iPhone 15 Pro Max": "iPhone 15 Pro Max",
    "iPhone 16e": "iPhone 16e", "iPhone 16": "iPhone 16", "iPhone 16 Plus": "iPhone 16 Plus",
    "iPhone 16 Pro": "iPhone 16 Pro", "iPhone 16 Pro Max": "iPhone 16 Pro Max", "iPhone 17e": "iPhone 17e",
    "iPhone 17 Air": "iPhone Air", "iPhone 17 Pro": "iPhone 17 Pro", "iPhone 17 Pro Max": "iPhone 17 Pro Max",
}

# Redacción de cámaras a partir de la fila "cámaras" del comparador (texto Apple entre comillas en el JSON)
CAMARAS = {
    "Dos cámaras Principal de 12 MP Teleobjetivo": "Sistema de dos cámaras de 12 MP: principal y teleobjetivo",
    "Una cámara Principal de 12 MP": "Cámara principal de 12 MP",
    "Dos cámaras Principal de 12 MP Ultra gran angular": "Sistema de dos cámaras de 12 MP: principal y ultra gran angular",
    "Sistema de dos cámaras Principal de 12 MP Ultra gran angular": "Sistema de dos cámaras de 12 MP: principal y ultra gran angular",
    "Sistema de tres cámaras Principal de 12 MP Ultra gran angular Teleobjetivo": "Sistema de tres cámaras de 12 MP: principal, ultra gran angular y teleobjetivo",
    "Sistema de cámaras Pro Principal de 12 MP Ultra gran angular Teleobjetivo": "Sistema de cámaras Pro de 12 MP: principal, ultra gran angular y teleobjetivo",
    "Sistema de cámaras Pro Principal de 48 MP Ultra gran angular Teleobjetivo": "Sistema de cámaras Pro: principal de 48 MP, ultra gran angular y teleobjetivo",
    "Sistema de dos cámaras Principal de 48 MP Ultra gran angular": "Sistema de dos cámaras: principal de 48 MP y ultra gran angular",
    "Sistema de cámara dos en uno Fusion principal de 48 MP": "Sistema de cámara dos en uno con cámara Fusion principal de 48 MP",
    "Sistema avanzado de dos cámaras Fusion principal de 48 MP Ultra gran angular de 12 MP": "Sistema avanzado de dos cámaras: Fusion principal de 48 MP y ultra gran angular de 12 MP",
    "Sistema de cámaras Pro Fusion principal de 48 MP Ultra gran angular de 48 MP Teleobjetivo": "Sistema de cámaras Pro: Fusion principal de 48 MP, ultra gran angular de 48 MP y teleobjetivo",
    "Sistema de cámara Fusion de 48 MP Fusion principal de 48 MP": "Cámara Fusion principal de 48 MP",
    "Sistema de cámaras Pro Fusion de 48 MP Fusion principal de 48 MP Fusion ultra gran angular de 48 MP Fusion teleobjetivo de 48 MP": "Sistema de cámaras Pro Fusion de 48 MP: principal, ultra gran angular y teleobjetivo",
}

def limpio(s):
    return re.sub(r"\s+\d+$", "", s.replace("‑", "-")).strip()

def specs_modelo(col):
    nombre_pant = col[60]
    m = re.search(r"Pantalla (?:widescreen )?(OLED|LCD) de ([\d.]+) pulgadas", col[61])
    tipo, pulg = m.group(1), m.group(2)
    agua = re.search(r"(IP6\d) \(hasta 30 minutos a una profundidad máxima de (\d+) metros?\)", col[82])
    conector = "USB-C" if "USB" in col[182] and "Lightning" not in col[182] else "Lightning"
    return {
        "chip": col[83],
        "pantalla": f"{nombre_pant} {tipo} de {pulg} pulgadas",
        "camaras": CAMARAS[col[34]],
        "biometria": col[173],
        "conector": conector,
        "magsafe": bool(col[59].strip()),
        "agua": f"{agua.group(1)}, hasta {agua.group(2)} metro{'s' if agua.group(2) != '1' else ''} por 30 minutos",
        "apple_textual": {"camaras": col[34], "pantalla": col[61], "agua": col[82],
                          "biometria": col[173] + " — " + col[174], "conector": limpio(col[182]),
                          "magsafe": col[59] or "(sin MagSafe)"},
    }

def html_ficha(modelo, cap, color, estado, bat, s):
    color_l = color[0].lower() + color[1:]
    if estado == "seminuevo":
        intro = (f"<p>{modelo} de {cap} en color {color_l}, seminuevo revisado por nuestro equipo técnico. "
                 f"Combina el {s['chip'].replace('Chip', 'chip')} con una {s['pantalla'][0].lower() + s['pantalla'][1:]}.</p>")
        li_bat = f"<li>Batería del equipo: {bat}.</li>"
        cierre_est = "Seminuevo con 30 días de garantía."
    else:  # caja sellada
        intro = (f"<p>{modelo} de {cap} en color {color_l}, en caja sellada. "
                 f"Combina el {s['chip'].replace('Chip', 'chip')} con una {s['pantalla'][0].lower() + s['pantalla'][1:]}.</p>")
        li_bat = "<li>Equipo en caja sellada.</li>"
        cierre_est = "Equipo en caja sellada con 30 días de garantía."
    bio = ("Face ID: desbloqueo con reconocimiento facial" if s["biometria"] == "Face ID"
           else "Touch ID: sensor de huellas en el botón de inicio")
    con = f"Conector {s['conector']}" + (" y compatibilidad con accesorios MagSafe" if s["magsafe"] else "")
    lis = [li_bat,
           f"<li>Almacenamiento de {cap}.</li>",
           f"<li>{s['camaras']}.</li>",
           f"<li>{bio}.</li>",
           f"<li>{con}.</li>",
           f"<li>Resistencia al agua {s['agua']} (especificación de fábrica de Apple).</li>"]
    garantia = (f"<h2>Garantía y entrega</h2><p>{cierre_est} Imagen de referencia: si quieres ver fotos reales del equipo, "
                f'escríbenos por <a href="{WA}">WhatsApp al 4027-3277</a>. '
                "Envío a toda Guatemala con pago contra entrega, o cómpralo en nuestra tienda en zona 13, Ciudad de Guatemala.</p>")
    return intro + "<h2>Características</h2><ul>" + "".join(lis) + "</ul>" + garantia

def main():
    tab = json.load(open(sys.argv[1], encoding="utf8"))["tab"]
    specs = {}
    for nuestro, apple in MODELOS.items():
        s = specs_modelo(tab[apple])
        s.update({"nombre_apple": apple, "fuente": FUENTE, "consultado": "2026-11-21"})
        specs[nuestro] = s
    (D / "itronics_specs_modelos.json").write_text(json.dumps(
        {"fuente": FUENTE, "consultado": "2026-11-21",
         "nota": "Extraído del comparador oficial de Apple (Latinoamérica). Sin MagSafe = celda vacía en el comparador.",
         "modelos": specs}, ensure_ascii=False, indent=1), encoding="utf8")

    respaldo, propuesta = [], []
    for line in (D / "itronics_actual.tsv").read_text(encoding="utf8").splitlines():
        pid, title, p1 = line.split("|")
        gid = f"gid://shopify/Product/{pid}"
        respaldo.append({"id": gid, "title": title, "descriptionHtml": f"<p>{p1}{SUFIJO}"})
        m = re.match(r"^(.*?) (\d+(?:GB|TB)), (.*?)\. (?:Seminuevo, batería (.*?)|(Caja sellada))\.$", p1)
        if not m or m.group(1) not in MODELOS:
            propuesta.append({"id": gid, "title": title, "html": None, "fuentes": [],
                              "dudas": ["SIN FUENTE: no es iPhone/iPad (fuera del alcance con fuente Apple); requiere ficha oficial del fabricante (samsung.com)."]})
            continue
        modelo, cap, color, bat, sellado = m.groups()
        s = specs[modelo]
        dudas = []
        nombre = modelo
        if modelo == "iPhone 17 Air":
            nombre = "iPhone Air"
            dudas.append("Apple lo llama 'iPhone Air' (no '17 Air'); el título no se tocó. Confirmar si se corrige el título.")
        if modelo == "iPhone SE 2020":
            nombre = "iPhone SE 2020 (2.ª generación)"
        if sellado:
            dudas.append("Equipo en caja sellada (no seminuevo): se conserva '30 días de garantía' de la ficha actual; confirmar garantía.")
        h = html_ficha(nombre, cap, color, "sellado" if sellado else "seminuevo", bat, s)
        propuesta.append({"id": gid, "title": title, "html": h, "fuentes": [FUENTE + f" ({s['nombre_apple']})"],
                          "dudas": dudas, "_bateria": bat, "_modelo": modelo})
    (D / "itronics_respaldo.json").write_text(json.dumps(respaldo, ensure_ascii=False, indent=1), encoding="utf8")
    (D / "itronics_propuesta.json").write_text(json.dumps(
        [{k: v for k, v in p.items() if not k.startswith("_")} for p in propuesta], ensure_ascii=False, indent=1), encoding="utf8")
    json.dump(propuesta, open(sys.argv[2], "w", encoding="utf8"), ensure_ascii=False)  # con campos internos para validar

if __name__ == "__main__":
    main()
