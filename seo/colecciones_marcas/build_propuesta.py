"""Genera propuesta.json, respaldo.json y PROPUESTA.md de colecciones de marca.
Datos leídos de Shopify el 2026-11-21 (solo lectura). No escribe en Shopify."""
import json, re, html
from pathlib import Path

D = Path(__file__).parent
CIERRE_ENVIO = ("Sí, a toda Guatemala con pago contra entrega: Ciudad de Guatemala el mismo día "
                "e interior al día siguiente. También puedes comprar en nuestra tienda en zona 13, Ciudad de Guatemala.")

def faq(marca):
    return (
        "<h2>Preguntas frecuentes</h2>\n"
        f"<p><strong>¿Los productos {marca} son originales?</strong><br>Sí. {marca} es una de las marcas oficiales que distribuimos en Guatemala.</p>\n"
        f"<p><strong>¿Tienen garantía?</strong><br>Sí, 1 año por defectos de fabricación.</p>\n"
        f"<p><strong>¿Hacen envíos?</strong><br>{CIERRE_ENVIO}</p>"
    )

def cond(marca, vendors):
    return {
        "matchType": "ANY",
        "conditions": [
            {"productVendor": {"matchType": "ANY", "relation": "EQUALS", "values": vendors}},
            {"productTitle": {"matchType": "ANY", "relation": "STARTS_WITH", "values": [marca]}},
        ],
    }

P = [
 {
  "marca": "LAUT", "accion": "crear", "handle": "laut", "title": "LAUT",
  "seo_title": "LAUT Guatemala: fundas, iPad y AirPods | Ventas Guate",
  "seo_description": "Accesorios LAUT originales en Guatemala: fundas iPhone 17 Pro y Pro Max, teclados y folios para iPad, estuches AirPods. Envío a todo el país.",
  "descriptionHtml": (
   "<p>Encuentra accesorios <strong>LAUT Guatemala</strong> originales: fundas para iPhone 17 Pro y 17 Pro Max, teclados y folios para iPad, estuches para AirPods y protectores para MacBook Air.</p>\n"
   "<h2>Fundas para iPhone</h2>\n"
   "<p>Crystal Matter X y Luxedge para iPhone 17 Pro Max, y Luxedge para iPhone 17 Pro. Mira más opciones en <a href=\"/collections/17-pro-max\">fundas iPhone 17 Pro Max</a> y <a href=\"/collections/iphone-17-pro\">fundas iPhone 17 Pro</a>.</p>\n"
   "<h2>iPad y MacBook</h2>\n"
   "<p>Teclados Typefolio 2.0 para iPad 10.9\", iPad 11\" e iPad Pro 11\" (M4), Typefolio y Prestige Folio universales de 9 a 11 pulgadas, Prestige Folio Mg para iPad Air 13\", Little Buddy para iPad 10.9\" y Huex para MacBook Air 13.6\". Ver <a href=\"/collections/ipads\">accesorios para iPad</a>.</p>\n"
   "<h2>AirPods</h2>\n"
   "<p>Estuches Huex Protect y Zentry para AirPods Pro 3 y AirPods 4.</p>\n" + faq("LAUT")),
  "condicion": cond("LAUT", ["LAUT"]),
  "productos_publicados": 19, "productos_con_stock": 19,
  "enlaces": ["/collections/17-pro-max", "/collections/iphone-17-pro", "/collections/ipads"],
  "notas": "11 productos con vendor LAUT + 8 con vendor 'Ventas Guate' (Huex MacBook Air 13.6 Negro, Huex Protect AirPods Pro3 Light Pink, Luxedge 17 Pro x2, Huex Protect AirPods 4, Zentry AirPods 4, Typefolio 2.0 iPad 11 y Pro 11). Por eso la condición agrega 'título empieza con LAUT'. Activos con stock pero sin publicar en tienda en línea: Huex MacBook Neo 13 Pink/Yellow, Links 2.0 Apple Watch Silver, Huex Protect MacBook Air 13 Black.",
 },
 {
  "marca": "Sudio", "accion": "no_crear", "handle": "sudio", "title": "Sudio",
  "seo_title": None, "seo_description": None, "descriptionHtml": None, "condicion": None,
  "productos_publicados": 0, "productos_con_stock": 0, "enlaces": [],
  "notas": "No hay ningún producto Sudio en Shopify (ni por vendor ni por título) ni en Odoo (product.template por nombre o brand_id). Crear la colección cuando haya al menos 4 productos publicados.",
 },
 {
  "marca": "OhSnap", "accion": "actualizar", "collection_id": "gid://shopify/Collection/522582950101",
  "handle": "ohsnap", "title": "OhSnap",
  "seo_title": "OhSnap Guatemala: grips MagSafe y soportes | Ventas Guate",
  "seo_description": "Grips, billeteras y soportes MagSafe OhSnap originales en Guatemala: Snap Grip, Grip Stand, Grip Wallet y Snap Car Mount. Envío a todo el país.",
  "descriptionHtml": (
   "<p>Accesorios magnéticos <strong>OhSnap Guatemala</strong> originales para tu teléfono: grips, billeteras con grip y soporte, y soporte para carro, todos compatibles con MagSafe.</p>\n"
   "<h2>Snap Grip y Grip Stand</h2>\n"
   "<p>El Snap Grip MagSafe viene en varios colores y diseños, como Black, Rose, Insomnia Blue, Retro Wave y Silver Fox. El Grip Stand agrega soporte vertical, en Black y Overexposed.</p>\n"
   "<h2>Grip Wallet y Snap Car Mount</h2>\n"
   "<p>Grip Wallet es billetera con grip y soporte (Black, Cranberry Smash y Orchid Slap). Snap Car Mount es el soporte magnético para carro. Mira más en <a href=\"/collections/magsafe\">accesorios MagSafe</a> y <a href=\"/collections/auto\">accesorios para carro</a>.</p>\n" + faq("OhSnap")),
  "condicion": {"actual": "Etiqueta = OhSnap (TAGGED_WITH) + 15 selecciones manuales; se mantiene. Opcional: agregar 'título empieza con OhSnap' para incluir Snap Grip Wine Noir y MCON cuando se publiquen."},
  "productos_publicados": 15, "productos_con_stock": 11,
  "enlaces": ["/collections/magsafe", "/collections/auto"],
  "notas": "La colección existe pero responde 404 en ventasguate.gt/collections/ohsnap: no está publicada en la tienda en línea (publicar con publishablePublish). El texto actual menciona el control MCON, que no está publicado (activo con 48 unidades, sin canal tienda en línea, vendor 'Ventas Guate'); igual 'Ohsnap Snap Grip Wine Noir' (21 u.). Sin stock: Snap Grip Blazed Sunset, Gator Fade, Orchid Slap y Pick Me Pink.",
 },
 {
  "marca": "Mello", "accion": "crear", "handle": "mello", "title": "Mello",
  "seo_title": "Mello Guatemala: fundas iPhone Duo y vidrios | Ventas Guate",
  "seo_description": "Accesorios Mello originales en Guatemala: fundas iPhone Duo, vidrio templado, protectores de cámara y cables USB-C. Envío a todo el país.",
  "descriptionHtml": (
   "<p>Accesorios <strong>Mello Guatemala</strong> originales para proteger y cargar tu iPhone: fundas y vidrios para iPhone Duo, protectores de cámara y cables USB-C.</p>\n"
   "<h2>Fundas iPhone Duo</h2>\n"
   "<p>Fundas Mello para iPhone Duo en Clear, Negro, Azul, Púrpura y Rosado, además del modelo Ch64 en negro. Ver <a href=\"/collections/iphone-duo\">accesorios iPhone Duo</a>.</p>\n"
   "<h2>Vidrios y protectores de cámara</h2>\n"
   "<p>Vidrio templado clear y de privacidad, y protectores de cámara 2 en 1 y completo en plata y azul.</p>\n"
   "<h2>Cables</h2>\n"
   "<p>Cables USB-C a Lightning y USB-C a USB-C en blanco. Más opciones en <a href=\"/collections/cables\">cables USB-C y Lightning</a>.</p>\n" + faq("Mello")),
  "condicion": cond("Mello", ["Mello", "MELLO DISTRIBUTION"]),
  "productos_publicados": 14, "productos_con_stock": 14,
  "enlaces": ["/collections/iphone-duo", "/collections/cables"],
  "notas": "Los 14 publicados tienen vendor 'MELLO DISTRIBUTION' (no 'Mello'). Hay 15 duplicados en borrador con vendor 'Ventas Guate' (no afectan: la colección solo muestra activos publicados). Stock bajo: iPhone Duo Púrpura (2) y Rosado (4).",
 },
 {
  "marca": "Reelcharge", "accion": "crear", "handle": "reelcharge", "title": "Reelcharge",
  "seo_title": "Reelcharge Guatemala: powerbanks y cargadores | Ventas Guate",
  "seo_description": "Power banks y cargadores Reelcharge originales en Guatemala: Reelsafe, Reelsafe Glass magnético, Fusion y cargador 45W tipo C. Envío a todo el país.",
  "descriptionHtml": (
   "<p>Carga tu teléfono donde estés con <strong>Reelcharge Guatemala</strong>: power banks, cargador de pared tipo C y holder inalámbrico para carro.</p>\n"
   "<h2>Power banks</h2>\n"
   "<p>Reelsafe de 5000 y 10000 mAh semi sólido, Reelsafe Glass magnético de 5000 mAh en gris y plata, y Fusion, que une power bank de 5000 mAh y cargador de 65 W, en negro y blanco. Ver <a href=\"/collections/powerbanks\">power banks</a>.</p>\n"
   "<h2>Cargadores</h2>\n"
   "<p>Cargador de pared Smart de 45 W tipo C y holder inalámbrico de 15 W para la rejilla del carro, con cable retráctil. Más en <a href=\"/collections/cubos\">cargadores de pared</a> y <a href=\"/collections/auto\">accesorios para carro</a>.</p>\n" + faq("Reelcharge")),
  "condicion": cond("Reelcharge", ["Reelcharge"]),
  "productos_publicados": 8, "productos_con_stock": 8,
  "enlaces": ["/collections/powerbanks", "/collections/cubos", "/collections/auto"],
  "notas": "Los 8 publicados tienen vendor 'Ventas Guate': sin la regla por título la colección quedaría vacía.",
 },
]

def words(h):
    return len(re.sub(r"<[^>]+>", " ", html.unescape(h)).split())

errs = []
for p in P:
    if p["accion"] == "no_crear":
        continue
    st, sd, h = p["seo_title"], p["seo_description"], p["descriptionHtml"]
    p["validacion"] = {"seo_title_len": len(st), "seo_description_len": len(sd), "palabras": words(h)}
    if len(st) > 60: errs.append(f"{p['marca']}: seo_title {len(st)}")
    if len(sd) > 155: errs.append(f"{p['marca']}: meta {len(sd)}")
    if not 90 <= words(h) <= 200: errs.append(f"{p['marca']}: palabras {words(h)}")
    for t in (st, sd, h):
        if re.search(r"Q\s?\d", t): errs.append(f"{p['marca']}: precio")
    if f"{p['marca']} Guatemala" not in h: errs.append(f"{p['marca']}: falta keyword")
    for e in p["enlaces"]:
        if e not in h: errs.append(f"{p['marca']}: enlace {e}")

(D / "propuesta.json").write_text(json.dumps(P, ensure_ascii=False, indent=1))

respaldo = [{
 "marca": "OhSnap", "collection_id": "gid://shopify/Collection/522582950101", "handle": "ohsnap",
 "title": "OhSnap", "fecha_lectura": "2026-11-21",
 "seo": {"title": "OhSnap Guatemala | Grips Magnéticos y Accesorios MagSafe",
         "description": "Compra accesorios OhSnap originales en Guatemala: Snap Grip, Grip Stand, Grip Wallet y control gaming MCON. Envío a todo el país, paga al recibir."},
 "descriptionHtml": "<p>Accesorios magnéticos <strong>OhSnap</strong> originales en Guatemala: grips magnéticos, soportes, billeteras MagSafe y el control gaming MCON. Envíos a todo el país con pago contra entrega y tienda física en zona 13, Ciudad de Guatemala.</p>",
 "sortOrder": "MOST_RELEVANT",
 "sources": [{"id": "gid://shopify/CollectionConditionsSource/27019608277", "matchType": "ALL",
              "conditions": [{"productTag": {"relation": "TAGGED_WITH", "values": ["OhSnap"]}}],
              "selecciones_manuales": 15}],
 "publicada_tienda_en_linea": False,
}]
(D / "respaldo.json").write_text(json.dumps(respaldo, ensure_ascii=False, indent=1))

md = ["# Colecciones de marca: LAUT, Sudio, OhSnap, Mello, Reelcharge", "",
      "Propuesta del 2026-11-21. **Solo propuesta: no se ha escrito nada en Shopify.** Datos leídos de Shopify ese día.", "",
      "| Marca | Acción | Handle | Publicados (activos en tienda en línea) | Con stock | SEO title | Meta | Palabras |",
      "|---|---|---|---|---|---|---|---|"]
for p in P:
    v = p.get("validacion", {})
    md.append(f"| {p['marca']} | {p['accion']} | {p['handle']} | {p['productos_publicados']} | {p['productos_con_stock']} | {v.get('seo_title_len','–')} | {v.get('seo_description_len','–')} | {v.get('palabras','–')} |")
md += ["", "## Hallazgos", "",
 "- **Vendor inconsistente**: solo LAUT (11 de 19) y OhSnap usan el vendor de la marca. Mello está como `MELLO DISTRIBUTION`; Reelcharge y 8 LAUT como `Ventas Guate`. Una condición solo `vendor = <Marca>` dejaría Reelcharge vacía y LAUT incompleta. Por eso cada colección nueva usa **ANY**: vendor EQUALS la marca (y variantes) **o** título STARTS_WITH la marca. Alternativa más limpia: normalizar el vendor de esos productos (ver `seo/vendor_a_marca.csv`) y dejar solo la regla de vendor.",
 "- **OhSnap** existe pero `ventasguate.gt/collections/ohsnap` da 404: no está publicada en la tienda en línea. Hay que publicarla (`publishablePublish`) además de actualizar el texto. El texto actual menciona el control MCON, que no está publicado.",
 "- `collectionCreate` crea las colecciones **sin publicar**: después de crearlas, `publishablePublish` en la tienda en línea.",
 "- **Sudio**: 0 productos en Shopify y en Odoo → no crear.",
 "", "## Mutación propuesta (no ejecutada)", "",
 "```graphql",
 "mutation($c: CollectionCreateInput!){ collectionCreate(collection:$c){ collection{ id handle } userErrors{ field message } } }",
 "# variables c = {title, handle, descriptionHtml, seo:{title, description}, sortOrder: BEST_SELLING,",
 "#   sources:[{source:{title:\"Marca\", targetType: PRODUCTS, inclusion: <condicion de propuesta.json>}}]}",
 "# OhSnap: collectionUpdate(collection:{id, descriptionHtml, seo}) + publishablePublish",
 "```", ""]
for p in P:
    md += [f"## {p['marca']} ({p['accion']})", ""]
    if p["accion"] == "no_crear":
        md += [p["notas"], ""]; continue
    md += [f"- **Handle**: `{p['handle']}` · **Título visible**: {p['title']}",
           f"- **SEO title** ({len(p['seo_title'])}): {p['seo_title']}",
           f"- **Meta** ({len(p['seo_description'])}): {p['seo_description']}",
           f"- **Condición**: `{json.dumps(p['condicion'], ensure_ascii=False)}`",
           f"- **Enlaces** (verificados, responden 200): {', '.join(p['enlaces'])}",
           f"- **Notas**: {p['notas']}", "", "```html", p["descriptionHtml"], "```", ""]
(D / "PROPUESTA.md").write_text("\n".join(md))
print("ERRORES:" if errs else "OK", errs)
for p in P: print(p["marca"], p.get("validacion"))
