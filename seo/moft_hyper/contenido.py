"""Contenido aplicado 2026-11-23 a 4 MOFT Carry Sleeve + Hyper HD Flex 9 (fuentes: moft.com, hypershop.com)."""
import json

CIERRE = ('<p>Producto original con 1 año de garantía. Envío a toda Guatemala con pago contra entrega, '
          'o cómpralo en nuestra tienda en zona 13, Ciudad de Guatemala.</p>')

MOFT_CARAC = """<h2>Características</h2>
<ul>
<li>Diseño 3 en 1: funda protectora, soporte para laptop y bolsillo de almacenamiento.</li>
<li>Se dobla en soporte en segundos con dos ángulos: 15° (eleva la pantalla 50 mm) y 25° (la eleva 80 mm).</li>
<li>Cuero vegano PU resistente a rayones y al agua, con estructura de fibra de vidrio reciclada.</li>
<li>Bolsillo de neopreno expandible para cargador, mouse u otros accesorios; vuelve a su forma delgada al vaciarlo.</li>
<li>Limpieza sencilla con un paño húmedo (no usar alcohol).</li>
</ul>"""

COMP_14 = """<h2>Compatibilidad</h2>
<p>Talla 14": MacBook Pro 14" (incluye modelos 2026), MacBook Pro 13", MacBook Air 13.6" (M2 y M5) y MacBook Air 13.3", además de la mayoría de laptops de 14" con medidas máximas de 32.5 × 23 × 1.7 cm.</p>"""

COMP_16 = """<h2>Compatibilidad</h2>
<p>Talla 16": la mayoría de laptops de 15" a 16", como MacBook Pro 15" y 16", Surface Laptop 3 15", Dell XPS 15 y Razer Blade 15 Advanced, con medidas máximas de 36 × 25 × 1.7 cm.</p>"""


def moft_intro(talla, color, uso):
    return (f'<p>La MOFT Carry Sleeve {talla} en color {color} protege tu laptop y se transforma en soporte '
            f'para trabajar con mejor postura. {uso}</p>')


P = {
 "gid://shopify/Product/15480774623445": dict(  # MB002-1-16-PEWH
    title="MOFT Carry Sleeve para Laptop 15 y 16 Pulgadas Beach White",
    vendor="MOFT", productType="Sleeves",
    html=moft_intro('de 16"', "Beach White", "Ideal para MacBook Pro de 15\" y 16\" y laptops de ese tamaño.") + "\n" + MOFT_CARAC + "\n" + COMP_16 + "\n" + CIERRE,
    seo_title="MOFT Carry Sleeve 15-16\" Beach White | Ventas Guate",
    seo_desc="Funda MOFT Carry Sleeve para laptop de 15 y 16\" Beach White: se convierte en soporte de 15° y 25° y tiene bolsillo expandible. Envío a toda Guatemala.",
    alt="MOFT Carry Sleeve para laptop 15 y 16 pulgadas Beach White con soporte plegable",
    media="beach"),
 "gid://shopify/Product/15480774656213": dict(  # MB002-1-13B-BK
    title="MOFT Carry Sleeve para Laptop 14 Pulgadas Negro",
    vendor="MOFT", productType="Sleeves",
    html=moft_intro('de 14"', "negro (Night Black)", "Ideal para MacBook Pro 14\", MacBook Air 13\" y laptops de 14\".") + "\n" + MOFT_CARAC + "\n" + COMP_14 + "\n" + CIERRE,
    seo_title="MOFT Carry Sleeve 14\" Negro para laptop | Ventas Guate",
    seo_desc="Funda MOFT Carry Sleeve para laptop de 14\" color negro: se convierte en soporte de 15° y 25° y tiene bolsillo expandible. Envío a toda Guatemala.",
    alt="MOFT Carry Sleeve para laptop 14 pulgadas negro con soporte plegable",
    media="black"),
 "gid://shopify/Product/15480774688981": dict(  # MB002-1-16-BK
    title="MOFT Carry Sleeve para Laptop 15 y 16 Pulgadas Negro",
    vendor="MOFT", productType="Sleeves",
    html=moft_intro('de 16"', "negro (Night Black)", "Ideal para MacBook Pro de 15\" y 16\" y laptops de ese tamaño.") + "\n" + MOFT_CARAC + "\n" + COMP_16 + "\n" + CIERRE,
    seo_title="MOFT Carry Sleeve 15-16\" Negro para laptop | Ventas Guate",
    seo_desc="Funda MOFT Carry Sleeve para laptop de 15 y 16\" color negro: se convierte en soporte de 15° y 25° y tiene bolsillo expandible. Envío a toda Guatemala.",
    alt="MOFT Carry Sleeve para laptop 15 y 16 pulgadas negro con soporte plegable",
    media="black"),
 "gid://shopify/Product/15480775409877": dict(  # MB002-1-13B-PEWH (talla 14" según MOFT)
    title="MOFT Carry Sleeve para MacBook Air 13 y Laptop 14 Pulgadas Beach White",
    vendor="MOFT", productType="Sleeves",
    html=moft_intro('de 14"', "Beach White", "Le queda a MacBook Air 13.3\" y 13.6\" y a laptops de 14\".") + "\n" + MOFT_CARAC + "\n" + COMP_14 + "\n" + CIERRE,
    seo_title="MOFT Carry Sleeve MacBook Air 13 / 14\" Beach White",
    seo_desc="Funda MOFT Carry Sleeve talla 14\" color Beach White para MacBook Air 13\" y laptops de 14\": se convierte en soporte de 15° y 25°. Envío a toda Guatemala.",
    alt="MOFT Carry Sleeve para MacBook Air 13 y laptop 14 pulgadas Beach White con soporte plegable",
    media="beach"),
 "gid://shopify/Product/15480780521685": dict(  # HD4103BUGL
    title="Hyper HyperDrive Flex Dock USB-C 9 Puertos Dual 4K HDMI Blanco y Azul",
    vendor="Hyper", productType="Periféricos",
    html=("<p>El HyperDrive Flex de 9 puertos convierte un solo puerto USB-C en una estación completa: "
          "dos monitores 4K, carga de 100 W, puertos USB, lectores de tarjetas y audio.</p>\n"
          "<h2>Características</h2>\n<ul>\n"
          "<li>2 puertos HDMI 4K a 60 Hz para monitores extendidos.</li>\n"
          "<li>Puerto USB-C Power Delivery de hasta 100 W para cargar tu laptop.</li>\n"
          "<li>2 puertos USB-C y 1 USB-A de 5 Gbps para discos, teclados y otros accesorios.</li>\n"
          "<li>Lectores de tarjetas SD y microSD de 104 MB/s.</li>\n"
          "<li>Conector de audio de 3.5 mm.</li>\n"
          "<li>Fabricado con 75 % de plástico reciclado; mide 136 × 42 × 14.9 mm y pesa 99 g.</li>\n"
          "</ul>\n"
          "<h2>Compatibilidad</h2>\n"
          "<p>Funciona con Windows, ChromeOS, macOS e iPadOS. El video requiere un puerto USB-C con DP Alt Mode en tu equipo "
          "y los dos monitores extendidos requieren un equipo compatible con MST.</p>\n" + CIERRE),
    seo_title="HyperDrive Flex Dock USB-C 9 en 1 Dual 4K | Ventas Guate",
    seo_desc="Dock USB-C HyperDrive Flex de 9 puertos: 2 HDMI 4K60, carga PD 100 W, USB-C y USB-A 5 Gbps, lector SD y microSD y audio 3.5 mm. Envío a toda Guatemala.",
    alt="Hyper HyperDrive Flex dock USB-C de 9 puertos con doble HDMI 4K blanco y azul",
    media="hyper"),
}

if __name__ == "__main__":
    import re
    for k, v in P.items():
        words = len(re.sub(r"<[^>]+>", " ", v["html"]).split())
        print(k[-14:], len(v["title"]), "seoT", len(v["seo_title"]), "meta", len(v["seo_desc"]), "palabras", words)
    json.dump(P, open("/tmp/claude-0/-home-user-Ventas-Guate/f1b76b12-5905-59a6-b3d5-7357ecfdb229/scratchpad/contenido.json", "w"), ensure_ascii=False, indent=1)
