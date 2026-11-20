"""Correcciones de ortografía y tildes para nombres de producto (palabra completa, sin distinguir mayúsculas)."""
import re
TYPOS = {"aple": "Apple", "audifno": "Audífono", "balancce": "Balance", "blac": "Black", "bluethooth": "Bluetooth",
         "bluetootah": "Bluetooth", "bluetoth": "Bluetooth", "burgendy": "Burgundy", "corflower": "Cornflower",
         "fuction": "Function", "garga": "Carga", "glecier": "Glacier", "gliter": "Glitter", "griip": "Grip", "hgmi": "HDMI",
         "luat": "LAUT", "mafsafe": "MagSafe", "magsafee": "MagSafe", "magnntico": "Magnético", "maybat": "Mybat",
         "oranage": "Orange", "pnrpura": "Púrpura", "pourple": "Purple", "prodigeee": "Prodigee", "pulcera": "Pulsera",
         "siicone": "Silicone", "slevee": "Sleeve", "traslucent": "Translucent", "walley": "Wallet",
         "whaterproof": "Waterproof", "wirelees": "Wireless", "safete": "Safetee", "nexerea": "Nexera", "ohsnap": "OhSnap",
         "lte": "LTE", "usbc": "USB-C", "aplewatch": "Apple Watch", "applewatch": "Apple Watch"}
TILDES = {"audifono": "Audífono", "audifonos": "Audífonos", "camara": "Cámara", "camaras": "Cámaras", "bateria": "Batería",
          "baterias": "Baterías", "rapida": "Rápida", "rapido": "Rápido", "maquina": "Máquina", "polimeros": "Polímeros",
          "polimero": "Polímero", "magnetico": "Magnético", "magnetica": "Magnética", "magneticos": "Magnéticos",
          "lamina": "Lámina", "laminas": "Láminas", "marron": "Marrón", "pequena": "Pequeña", "diseno": "Diseño",
          "proteccion": "Protección", "purpura": "Púrpura", "metalico": "Metálico", "metalica": "Metálica",
          "inalambrico": "Inalámbrico", "inalambrica": "Inalámbrica", "inalambricos": "Inalámbricos",
          "inalambricas": "Inalámbricas", "electrico": "Eléctrico", "electrica": "Eléctrica", "tactil": "Táctil",
          "plastico": "Plástico", "telefono": "Teléfono", "cafe": "Café", "limon": "Limón", "cancelacion": "Cancelación",
          "edicion": "Edición", "coleccion": "Colección", "generacion": "Generación", "boton": "Botón",
          "vehiculo": "Vehículo", "portatil": "Portátil", "automatico": "Automático", "automatica": "Automática",
          "energia": "Energía", "lapiz": "Lápiz", "numero": "Número", "ergonomico": "Ergonómico", "optico": "Óptico",
          "termico": "Térmico", "camion": "Camión", "conexion": "Conexión", "transmision": "Transmisión",
          "silicon": None, "mas": None}
FIXES = {k: v for k, v in {**TYPOS, **TILDES}.items() if v}

def corregir(s: str) -> str:
    s = re.sub(r"\bInfinity Infitiny\b", "Infinity", s, flags=re.I)
    s = re.sub(r"\bInfitiny\b", "Infinity", s, flags=re.I)
    def rep(m):
        w = m.group(0); v = FIXES.get(w.lower())
        if not v: return w
        if w.islower() and v[0].isupper() and v.lower() == v.lower() and not any(c.isupper() for c in v[1:]):
            return v.lower()  # palabra en minúscula dentro del título (ej. "de")
        return v
    return re.sub(r"[A-Za-zÁÉÍÓÚÑáéíóúñü]+", rep, s)
