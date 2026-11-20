"""Propuesta de nombres sin MAYÚSCULAS (Odoo product.template, es_GT y en_US).
A: en_US ya limpio y mismo texto -> se copia a es_GT. A2: en_US limpio pero con otro texto -> se capitaliza es_GT (en_US no cambia). B: ambos en mayúsculas -> se capitalizan ambos por reglas, sin cambiar el texto.
Salida: seo/titulos_l/propuesta_mayusculas.csv (no escribe en Odoo)."""
import csv, json, re, os
D = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(f"{D}/mayusculas_actual.json"))

def caps(s):
    l = [c for c in s if c.isalpha()]
    return len(l) >= 6 and sum(c.isupper() for c in l) / len(l) > 0.8

FIX = {w.lower(): w for w in """LAUT JBL LOGiiX iPhone iPad MacBook AirPods AirTag iMac MagSafe USB USB-C USB-A HDMI TWS PD GaN LED RGB SSD HDD SD microSD
NFC GPS BT ANC ENC iOS PC TV UV HD 4K 8K VGA DVI AUX RCA LCD OLED AMOLED XL XXL XS IP67 IP68 MFi Qi Qi2 OhSnap Nimbus9 HiFuture Mybat
HyperGear PopSockets OtterBox ZAGG InvisibleShield UAG Spigen Belkin Anker Mophie Sudio Tucano Targus Reebok Prodigee Mello Reelcharge
Case-Mate Skullcandy Urbanista Xiaomi Huawei Samsung Galaxy Apple Watch Pixel Motorola Honor OPPO Realme Redmi POCO OnePlus Nintendo
PlayStation PS4 PS5 Xbox Alexa Echo Kindle Fire Ring Blink Garmin Fitbit Amazfit GoPro DJI Logitech HP Dell Lenovo ASUS Acer MSI
Energy Sistem SoundCore Marshall Sony LG TCL Hisense Kemik II III IV MAX PRO mAh Wh W V A Hz GB TB MB cm mm m kg g oz in""".split()}
FIX.update({"max": "Max", "pro": "Pro", "plus": "Plus", "mini": "Mini", "ultra": "Ultra", "air": "Air", "se": "SE", "fe": "FE",
            "w": "W", "v": "V", "a": "a", "m": "m", "g": "g", "in": "in"})
ACR = set("tws anc enc bt pd led rgb usb nfc gps hd tv pc uv ssd hdd ram cpu gpu eng ing vga dvi aux rca lcd xl xs xxl uag hp lg msi dji tcl jbl usa uk eu ir ac dc oem kvm ups".split())
SMALL = {"de", "del", "para", "con", "y", "e", "o", "u", "en", "a", "al", "el", "la", "los", "las", "por", "sin", "of", "and", "for", "with", "the", "to", "in", "on"}

def word(w, first):
    if not w: return w
    lw = w.lower()
    if lw in FIX and not (lw in SMALL and not first):
        return FIX[lw]
    if not first and lw in SMALL: return lw
    if any(c.isdigit() for c in w) and re.fullmatch(r"[A-Za-z]{4,}\d+", w): return lw[:1].upper() + lw[1:]
    if any(c.isdigit() for c in w): return w.upper() if not re.search(r"\d(mah|wh|gb|tb|mb|hz|mm|cm)$", lw) else re.sub(r"(mah|wh|gb|tb|mb|hz|mm|cm)$", lambda m: FIX.get(m.group(1), m.group(1)), lw)
    if w.isalpha() and w.isupper() and lw in ACR:
        return w  # siglas (TWS, ANC, BT…)
    return lw[:1].upper() + lw[1:]

def norm(s):
    import unicodedata
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "", s)

def title(s):
    s = re.sub(r"\s+", " ", s.strip())
    parts = re.split(r"([\s/()\-+,.\"]+)", s)
    out, first = [], True
    for p in parts:
        if re.fullmatch(r"[\s/()\-+,.\"]+", p or " "):
            out.append(p); continue
        prev = out[-1] if out else " "
        out.append(word(p, first or not prev.endswith(" "))); first = False
    t = "".join(out)
    t = re.sub(r"\bUsb-c\b", "USB-C", t, flags=re.I)
    return t

with open(f"{D}/propuesta_mayusculas.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "grupo", "actual_es_GT", "actual_en_US", "propuesto_es_GT", "propuesto_en_US", "marca", "stock", "en_shopify"])
    n = {"A": 0, "A2": 0, "B": 0}
    for r in rows:
        if not caps(r["en_US"]):
            same = norm(r["en_US"]) == norm(r["es_GT"])
            g, p = ("A" if same else "A2"), (r["en_US"].strip() if same else title(r["es_GT"]))
        else:
            g, p = "B", title(r["es_GT"])
        n[g] += 1
        w.writerow([r["id"], g, r["es_GT"], r["en_US"], p, (title(r["en_US"]) if g == "B" else r["en_US"].strip()), r["marca"] or "", r["stock"], r["shopify"]])
print(n)
