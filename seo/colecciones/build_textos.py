"""Genera textos SEO para las 30 colecciones principales (por sesiones de 90 días).

Salida: textos_colecciones.json (id, handle, title, seo_title, seo_description, html).
Hechos usados: 1 año de garantía (política de devoluciones), tienda en zona 13,
envío a toda Guatemala. Sin precios, sin plazos ni costos de envío.
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
TIENDA = "9a Calle 15-45 zona 13, Edificio Trafalgar, Oficina 102, Ciudad de Guatemala"


def faq(*pares):
    out = ["<h2>Preguntas frecuentes</h2>"]
    for q, r in pares:
        out.append(f"<p><strong>{q}</strong><br>{r}</p>")
    return "\n".join(out)


ORIG = ("¿Son productos originales?", "Sí. Son productos originales y nuevos, con 1 año de garantía por defectos de fabricación.")
ENVIO = ("¿Cómo funciona el envío?", "Enviamos a toda Guatemala con pago contra entrega y entrega garantizada y respaldada por nosotros. También puedes comprar en nuestra tienda en zona 13.")
TIENDA_Q = ("¿Dónde puedo verlos en persona?", f"En nuestra tienda: {TIENDA}.")


def L(handle, texto):
    return f'<a href="/collections/{handle}">{texto}</a>'


C = []


def add(id_, handle, title, seo_title, seo_desc, html):
    assert len(seo_title) <= 70, (handle, len(seo_title))
    assert len(seo_desc) <= 160, (handle, len(seo_desc))
    C.append(dict(id=f"gid://shopify/Collection/{id_}", handle=handle, title=title,
                  seo_title=seo_title, seo_description=seo_desc, html=html.strip()))


# 1. Seminuevos (394 sesiones)
add(None, "seminuevos", "iPhone Seminuevos",
    "iPhone Seminuevos en Guatemala | Revisados | Ventas Guate",
    "iPhone seminuevos en Guatemala: iPhone 13, 14, 15, 16 y 17 revisados por nuestro equipo técnico. Varias capacidades y colores. Envío a todo el país.",
    f"""
<p>Compra tu <strong>iPhone seminuevo en Guatemala</strong> con la tranquilidad de una tienda establecida. Cada equipo es revisado y verificado por nuestro equipo técnico antes de publicarse, para que recibas un teléfono que funciona como debe.</p>
<h2>Modelos disponibles</h2>
<p>Tenemos iPhone 13 Pro Max, iPhone 14, 14 Plus y 14 Pro, iPhone 15, 15 Plus y 15 Pro Max, iPhone 16, 16E, 16 Plus, 16 Pro y 16 Pro Max, y los más recientes iPhone 17, 17 Pro y 17 Pro Max, en capacidades de 128 GB hasta 1 TB. La disponibilidad cambia rápido: cada equipo es una unidad única.</p>
<h2>Protégelo desde el primer día</h2>
<p>¿Buscas un iPhone nuevo de lanzamiento? Visita {L('reservas','Reservas')}. Encuentra la funda para tu modelo en {L('cases-iphone','fundas para iPhone')} y carga rápida en {L('cubos','cargadores de pared')}.</p>
{faq(("¿Los equipos están revisados?", "Sí, cada iPhone seminuevo pasa por revisión de nuestro equipo técnico antes de publicarse."), ("¿Tienen garantía?", "Sí, los equipos seminuevos tienen 30 días de garantía."), ENVIO, TIENDA_Q)}
""")

# 2. Alexa (948)
add(None, "alexa", "Alexa y Amazon Echo",
    "Alexa en Guatemala: Echo Dot, Echo Spot y Combos | Ventas Guate",
    "Amazon Echo con Alexa en Guatemala: Echo Dot 5ta generación, Echo Dot Max, Echo Spot y combos con bombillos smart. Originales y con envío a todo el país.",
    f"""
<p>Encuentra <strong>Alexa en Guatemala</strong>: parlantes Amazon Echo originales para escuchar música, preguntar el clima, poner alarmas y controlar tu casa con la voz.</p>
<h2>¿Qué Echo elegir?</h2>
<ul>
<li><strong>Echo Dot 5ta generación:</strong> el más popular, compacto y fácil de configurar. En negro, azul y blanco.</li>
<li><strong>Echo Dot Max:</strong> la opción con más sonido dentro de la familia Dot, en negro y blanco glaciar.</li>
<li><strong>Echo Spot (2024):</strong> con pantalla para ver la hora, el clima y lo que está sonando. Ideal para la mesa de noche.</li>
</ul>
<h2>Combos y casa inteligente</h2>
<p>Los combos Echo Dot + bombillos smart traen lo necesario para empezar a controlar las luces por voz. También hay bombillas inteligentes Amazon Basics y VTA+ compatibles con Alexa. Para más ideas, visita {L('smart-home','Smart Home')} y {L('govee','luces Govee')}.</p>
{faq(("¿Alexa funciona en Guatemala?", "Sí. Se configura con la app Amazon Alexa en tu celular y una red Wi-Fi."), ("¿Los bombillos funcionan con Alexa?", "Sí, los bombillos de esta colección son compatibles con Alexa."), ORIG, ENVIO)}
""")

# 3. Mondo (317)
add(525533053141, "mondo", "Mondo",
    "Mondo Guatemala: Bocinas y Audífonos Bluetooth | Ventas Guate",
    "Bocinas y audífonos Mondo en Guatemala: Speaker Small y Medium, audífonos Freestyle y Mondo ANC con cancelación de ruido. Originales, 1 año de garantía.",
    f"""
<p><strong>Mondo</strong> combina sonido y diseño: bocinas y audífonos Bluetooth con acabados que se ven bien en cualquier espacio.</p>
<h2>Bocinas Mondo Speaker</h2>
<p>Disponibles en tamaño Small (Grey, Greige y Brass) y Medium (Metal Gray), pensadas para la sala, el escritorio o el cuarto.</p>
<h2>Audífonos Mondo</h2>
<p>Los <strong>Mondo Freestyle</strong> en Black y Pink, y los <strong>Mondo ANC Over-Ear</strong> con cancelación de ruido en Orange y Graphite.</p>
<p>Compara con otras marcas en {L('bocinas','bocinas Bluetooth')} y {L('over-ear','audífonos over-ear')}.</p>
{faq(ORIG, ENVIO, TIENDA_Q)}
""")

# 4. iPhone 18 (233)
add(528474570965, "iphone-18", "Fundas y Accesorios iPhone 18",
    "Fundas iPhone 18 Pro y 18 Pro Max en Guatemala | Ventas Guate",
    "Fundas para iPhone 18 Pro y 18 Pro Max en Guatemala: Prodigee Jogger, Kickit, Blackout, Orbit 360, Superstar y más. Compatibles también con iPhone 17 Pro.",
    f"""
<p>Protege tu <strong>iPhone 18</strong> desde el primer día. Reunimos fundas para iPhone 18 Pro y 18 Pro Max, y para iPhone Duo.</p>
<h2>Fundas compatibles con iPhone 17 Pro</h2>
<p>Muchos modelos Prodigee están marcados como <strong>iPhone 18 Pro Max/17 Pro Max</strong> o <strong>18 Pro/17 Pro</strong>: la misma funda sirve para ambos. Revisa el nombre de cada producto antes de comprar.</p>
<h2>Estilos disponibles</h2>
<ul>
<li><strong>Uso rudo:</strong> Prodigee Blackout, Jogger y Kevo.</li>
<li><strong>Con soporte:</strong> Prodigee Kickit y Orbit 360.</li>
<li><strong>Transparentes y de diseño:</strong> Superstar, Tile, Torte y Geo.</li>
<li><strong>Silicón:</strong> LOGiiX Vibrance.</li>
</ul>
<p>Complementa con {L('accesorios-iphone-18-pro-max','accesorios para iPhone 18 Pro Max')} y {L('magsafe','accesorios MagSafe')}.</p>
{faq(("¿Una funda de iPhone 17 Pro Max le queda al 18 Pro Max?", "Solo si el producto indica ambos modelos (por ejemplo, \"iPhone 18 Pro Max/17 Pro Max\")."), ORIG, ENVIO)}
""")

# 5. cases-iphone (207)
add(None, "cases-iphone", "Fundas para iPhone",
    "Fundas para iPhone en Guatemala | Todos los Modelos | Ventas Guate",
    "Fundas y protectores para iPhone 13 al 18 en Guatemala: Prodigee, ZAGG, Spigen, Nimbus9, MyBat, Click y más. Originales, 1 año de garantía.",
    f"""
<p>Encuentra la <strong>funda para tu iPhone</strong> en un solo lugar: modelos para iPhone 13, 14, 15, 16, 17 y 18, además de vidrios templados y protectores de cámara.</p>
<h2>Busca por modelo</h2>
<ul>
<li>{L('iphone-18','Fundas iPhone 18')}</li>
<li>{L('cases-iphone-17','Fundas iPhone 17')} · {L('iphone-17-pro','iPhone 17 Pro')}</li>
<li>{L('cases-iphone-16','Fundas iPhone 16')} · {L('iphone-16-pro-max','iPhone 16 Pro Max')}</li>
<li>{L('cases-iphone-15','Fundas iPhone 15')}</li>
</ul>
<h2>Marcas</h2>
<p>{L('prodigee','Prodigee')}, ZAGG, Spigen, {L('nimbus9','Nimbus9')}, MyBat, Click, CLCKR, ITSkins, SwitchEasy y {L('logiix','LOGiiX')}: desde fundas transparentes y delgadas hasta protección de uso rudo con MagSafe.</p>
<h2>Vidrios y protectores de cámara</h2>
<p>Vidrios templados Gadget Guard y MyBat, y protectores de cámara CaseCo Screen Patrol y Prodigee Super Glass.</p>
{faq(("¿Cómo sé si la funda es para mi modelo?", "Cada producto indica el modelo exacto en el nombre. Si dice varios modelos (por ejemplo, 15/14/13), sirve para todos ellos."), ORIG, ENVIO)}
""")

# 6. Promociones (114)
add(None, "promociones", "Promociones",
    "Promociones y Ofertas en Tecnología | Ventas Guate",
    "Promociones en fundas, audífonos, bocinas, smart home y accesorios originales en Guatemala. Skullcandy, Prodigee, ZAGG, Govee, Alexa y más.",
    f"""
<p>Aquí reunimos las <strong>promociones vigentes</strong> de Ventas Guate: fundas, audífonos, bocinas, smartwatches, casa inteligente y accesorios de carga de marcas originales.</p>
<h2>Qué encontrarás</h2>
<ul>
<li>Audífonos y bocinas {L('skullcandy','Skullcandy')}, {L('hifuture','HiFuture')} y Urbanista.</li>
<li>Fundas ZAGG, Prodigee, Nimbus9 y CLCKR para iPhone y Galaxy.</li>
<li>Combos {L('alexa','Alexa')} y luces {L('govee','Govee')}.</li>
</ul>
<p>Las promociones cambian según inventario. Para precios de remate, revisa también {L('liquidacion','Liquidación')}.</p>
{faq(("¿Los productos en promoción tienen garantía?", "Sí, tienen 1 año de garantía por defectos de fabricación. Los productos en oferta no tienen cambio ni devolución."), ENVIO)}
""")

# 7. S26 cases (103)
add(519159087317, "s26-cases", "Fundas Galaxy S26",
    "Fundas Samsung Galaxy S26, S26 Plus y S26 Ultra | Ventas Guate",
    "Fundas para Samsung Galaxy S26, S26 Plus y S26 Ultra en Guatemala: Prodigee Kickit, Jogger, Formula K1, Hero + Mag y protectores de cámara.",
    f"""
<p>Fundas originales para la línea <strong>Samsung Galaxy S26</strong>: S26, S26 Plus y S26 Ultra.</p>
<h2>Galaxy S26 Ultra</h2>
<p>Prodigee Kickit, Jogger, Blackout, Formula K1, Superstar y Hero + Mag, además de Click Latch. Ver solo Ultra en {L('s26-ultra','fundas Galaxy S26 Ultra')}.</p>
<h2>Galaxy S26 y S26 Plus</h2>
<p>Prodigee Super Hero, Superstar Clear y Hero + Mag Clear.</p>
<h2>Protección extra</h2>
<p>Prodigee Super Glass Camera para S26 / S26 Plus y Super Glass Privacy para S26 Ultra.</p>
<p>Más modelos en {L('cases-samsung','fundas Samsung')}.</p>
{faq(ORIG, ENVIO)}
""")

# 8. Accesorios iPhone 18 Pro Max (90)
add(531095453909, "accesorios-iphone-18-pro-max", "Accesorios iPhone 18 Pro Max",
    "Accesorios iPhone 18 Pro Max en Guatemala | MagSafe | Ventas Guate",
    "Accesorios MagSafe para iPhone 18 Pro Max: grips y billeteras OhSnap, soporte para carro, power bank MagPower y base de carga Qi2 Prodigee.",
    f"""
<p>Accesorios magnéticos para sacarle más provecho a tu <strong>iPhone 18 Pro Max</strong>.</p>
<h2>Grips y billeteras OhSnap</h2>
<p>Snap Grip, Grip Stand con soporte vertical y Grip Wallet con espacio para tarjetas, en varios colores. Ver toda la marca en {L('ohsnap','OhSnap')}.</p>
<h2>Carro y carga</h2>
<p>OhSnap Snap Car Mount, power bank Prodigee MagPower to-Go + Watch 5K y base de carga Prodigee Mag Chill Station Qi2.</p>
<p>¿Buscas funda? Visita {L('iphone-18','fundas iPhone 18')}.</p>
{faq(("¿Funcionan con funda?", "Funcionan con fundas compatibles con MagSafe."), ORIG, ENVIO)}
""")

# 9. S25 cases (72)
add(519159742677, "s25-cases", "Fundas Galaxy S25",
    "Fundas Samsung Galaxy S25, S25 Plus y S25 Ultra | Ventas Guate",
    "Fundas para Samsung Galaxy S25, S25 Plus y S25 Ultra en Guatemala: Prodigee Kickit, Superstar, Safetee Flow, Balance, Glow y Super Hero.",
    f"""
<p>Fundas originales para <strong>Samsung Galaxy S25</strong>, S25 Plus y S25 Ultra.</p>
<h2>Modelos Prodigee</h2>
<ul>
<li><strong>Kickit:</strong> con soporte integrado, en negro y rosado.</li>
<li><strong>Superstar y Super Hero:</strong> transparentes.</li>
<li><strong>Safetee Flow y Balance:</strong> acabados de color (Night Frost, Desert, Lavanda).</li>
<li><strong>Glow y Pampas:</strong> diseños con estilo.</li>
</ul>
<p>Para otros Galaxy visita {L('cases-samsung','fundas Samsung')} o {L('s26-cases','fundas Galaxy S26')}.</p>
{faq(ORIG, ENVIO)}
""")

# 10. cases iPhone 17 (63)
add(None, "cases-iphone-17", "Fundas iPhone 17",
    "Fundas iPhone 17, 17 Pro, 17 Pro Max y Air | Ventas Guate",
    "Fundas para iPhone 17, 17 Pro, 17 Pro Max y iPhone Air en Guatemala: Prodigee Jogger, Super Hero, Flow, Magneteek y protectores CaseCo.",
    f"""
<p>Todas las <strong>fundas para iPhone 17</strong> en un solo lugar: iPhone 17, 17 Pro, 17 Pro Max y iPhone Air.</p>
<h2>Fundas Prodigee</h2>
<p>Jogger, Super Hero, Flow, Magneteek, Kickit, Edge, Blackout, Glow, Hero+M y Superstar en varios colores. Ver por modelo: {L('iphone-17-pro','iPhone 17 Pro')}.</p>
<h2>Protector de cámara</h2>
<p>CaseCo Screen Patrol para iPhone 17 Pro y 17 Pro Max, y Prodigee Super Glass Camera para iPhone Air.</p>
<p>Si tu funda dice "18 Pro Max/17 Pro Max", también sirve para tu iPhone 17 Pro Max: mira {L('iphone-18','fundas iPhone 18')}.</p>
{faq(ORIG, ENVIO)}
""")

# 11. PopSockets (51)
add(None, "popsockets", "PopSockets",
    "PopSockets Guatemala: Grips y Billeteras MagSafe | Ventas Guate",
    "PopSockets originales en Guatemala: grips MagSafe y billeteras Wallet y Wallet+ MagSafe en varios colores. Envío a todo el país.",
    f"""
<p><strong>PopSockets originales en Guatemala</strong>: agarre seguro, soporte para ver videos y, en las versiones Wallet, espacio para tus tarjetas.</p>
<h2>Modelos</h2>
<ul>
<li><strong>PopSockets MagSafe:</strong> grip magnético en rojo, verde y azul.</li>
<li><strong>Wallet y Wallet+ MagSafe:</strong> billetera magnética en negro, azul, cognac, clear y blanco.</li>
</ul>
<p>Alternativas magnéticas en {L('ohsnap','OhSnap')} y {L('magsafe','MagSafe')}.</p>
{faq(("¿Funcionan con cualquier iPhone?", "Las versiones MagSafe se pegan a iPhone con MagSafe o a fundas compatibles con MagSafe."), ORIG, ENVIO)}
""")

# 12. Powerbanks (45)
add(None, "powerbanks", "Power Banks",
    "Power Banks en Guatemala: Baterías Portátiles | Ventas Guate",
    "Power banks y baterías portátiles en Guatemala: Prodigee MagPower, LOGiiX Piston Power, Belkin, MyBat y Battarix. MagSafe y de 5,000 a 10,000 mAh.",
    f"""
<p>Una <strong>power bank</strong> es la forma más simple de no quedarte sin batería. Tenemos opciones magnéticas, con cable integrado y con soporte.</p>
<h2>MagSafe</h2>
<p>Prodigee MagPower to-Go (Slim 5K, 10,000 mAh, Halo y versión con cargador para Apple Watch) y LOGiiX Piston Power 5000mAh Slim Mag.</p>
<h2>Con cable o soporte</h2>
<p>Belkin Powerbank Stand 10,000 mAh, LOGiiX Piston Power 10000mAh Classic, MyBat Pro 10000 mAh, Prodigee Energee to Go Wireless y la tarjeta de emergencia Battarix Charge Card.</p>
<p>Completa con {L('cables','cables')} y {L('cubos','cargadores de pared')}.</p>
{faq(("¿Qué capacidad necesito?", "5,000 mAh es para un refuerzo durante el día; 10,000 mAh da más cargas completas para viajes."), ORIG, ENVIO)}
""")

# 13. Govee (38)
add(None, "govee", "Govee",
    "Govee Guatemala: Tiras LED, Paneles y Lámparas RGBIC | Ventas Guate",
    "Luces inteligentes Govee en Guatemala: tiras LED RGBIC de 3 y 5 m, TV Backlight, paneles Glide Hexagon, lámpara Lyra y barras LED. Control por app y voz.",
    f"""
<p>Transforma tu cuarto, sala o setup gaming con <strong>luces inteligentes Govee</strong>: millones de colores, efectos y control desde el celular.</p>
<h2>Productos Govee</h2>
<ul>
<li><strong>Tiras LED RGBIC:</strong> 3 y 5 metros para interior, y Phantasy de 10 metros para exterior.</li>
<li><strong>TV Backlight 3 Lite:</strong> luz ambiental para TV de 55" a 65".</li>
<li><strong>Paneles:</strong> Glide Hexagon y Glide Wall Light.</li>
<li><strong>Lámpara de pie Lyra</strong> y <strong>barras LED</strong>.</li>
</ul>
<p>Suma control por voz con {L('alexa','Alexa')} o mira más en {L('smart-home','Smart Home')}.</p>
{faq(("¿Qué significa RGBIC?", "Que la tira puede mostrar varios colores al mismo tiempo en distintos segmentos."), ORIG, ENVIO)}
""")

# 14. cases iPhone 15 (27)
add(None, "cases-iphone-15", "Fundas iPhone 15",
    "Fundas iPhone 15, 15 Plus, 15 Pro y 15 Pro Max | Ventas Guate",
    "Fundas para iPhone 15, 15 Plus, 15 Pro y 15 Pro Max en Guatemala: Prodigee, Spigen, Nimbus9, CLCKR, ITSkins, SwitchEasy y vidrios templados.",
    f"""
<p><strong>Fundas para iPhone 15</strong> en todas sus versiones: 15, 15 Plus, 15 Pro y 15 Pro Max.</p>
<h2>Marcas</h2>
<p>Prodigee (Safetee Neo, Safetee Flow, Balance, Sidekick), Spigen Core Armor, Nimbus9 Alto2 y Stratus MagSafe, CLCKR Onyx MagSafe, ITSkins Spectrum Armor, SwitchEasy Artist y MyBat Maverick con holster.</p>
<h2>Vidrios y cámara</h2>
<p>Vidrios templados Gadget Guard (packs) y MyBat Privacy, y protectores de cámara para 15/15 Plus y 15 Pro/15 Pro Max.</p>
<p>Algunas fundas dicen "15/14/13": sirven para los tres modelos. Ver todos los modelos en {L('cases-iphone','fundas para iPhone')}.</p>
{faq(ORIG, ENVIO)}
""")

# 15. S26 Ultra (27)
add(None, "s26-ultra", "Fundas Galaxy S26 Ultra",
    "Fundas Samsung Galaxy S26 Ultra en Guatemala | Ventas Guate",
    "Fundas para Galaxy S26 Ultra: Prodigee Kickit, Jogger, Blackout, Formula K1, Superstar, Hero + Mag y Click Latch. Vidrio Super Glass Privacy.",
    f"""
<p>Fundas originales para el <strong>Samsung Galaxy S26 Ultra</strong>.</p>
<ul>
<li><strong>Con soporte:</strong> Prodigee Kickit.</li>
<li><strong>Uso rudo:</strong> Prodigee Jogger (Midnight, Army) y Blackout Navy.</li>
<li><strong>Deportiva:</strong> Prodigee Formula K1 en Smoke y Gris.</li>
<li><strong>Transparentes:</strong> Prodigee Superstar y Hero + Mag.</li>
<li><strong>Click Latch</strong> en Purple.</li>
</ul>
<p>Protege la pantalla con Prodigee Super Glass Privacy. Ver S26 y S26 Plus en {L('s26-cases','fundas Galaxy S26')}.</p>
{faq(ORIG, ENVIO)}
""")

# 16. cases iPhone 16 (26)
add(None, "cases-iphone-16", "Fundas iPhone 16",
    "Fundas iPhone 16, 16 Plus, 16 Pro y 16 Pro Max | Ventas Guate",
    "Fundas para iPhone 16, 16 Plus, 16 Pro y 16 Pro Max en Guatemala: ZAGG Santa Cruz y Luxe Snap, Prodigee, MyBat Maverick y Click MagSafe.",
    f"""
<p><strong>Fundas para iPhone 16</strong>: 16, 16 Plus, 16 Pro y 16 Pro Max.</p>
<h2>Marcas</h2>
<ul>
<li><strong>ZAGG:</strong> Santa Cruz Snap, Luxe Snap y London Snap.</li>
<li><strong>Prodigee:</strong> Solid, Safetee Flow, Popstar, Hero y más.</li>
<li><strong>MyBat Maverick:</strong> antimicrobial con holster y MagSafe.</li>
<li><strong>Click:</strong> Latch, Radient y Ultra Slim MagSafe.</li>
</ul>
<p>Ver solo Pro Max en {L('iphone-16-pro-max','fundas iPhone 16 Pro Max')} o todos los modelos en {L('cases-iphone','fundas para iPhone')}.</p>
{faq(ORIG, ENVIO)}
""")

# 17. Conectividad (25)
add(None, "conectividad-1", "Conectividad y Carga",
    "Cables, Cargadores y Organizadores Tech | Ventas Guate",
    "Cables USB-C, cargadores de pared, power banks, adaptadores de viaje y organizadores Function101 en Guatemala. Prodigee, LOGiiX, Tekya y más.",
    f"""
<p>Todo para <strong>cargar y conectar</strong> tus dispositivos, y mantener tu escritorio ordenado.</p>
<h2>Carga</h2>
<p>{L('cubos','Cargadores de pared')} Prodigee Energee y LOGiiX, {L('powerbanks','power banks')} MagPower y la base Tekya Qitek Magdock 3 en 1.</p>
<h2>Cables</h2>
<p>Function Smart Cable con pantalla digital de potencia (60W y 100W), Neat Cable magnético, cables retráctiles 2 en 1 y cables Prodigee Energee. Más en {L('cables','cables')}.</p>
<h2>Escritorio y viaje</h2>
<p>Function Workpad Pro y Desk Mat Pro, organizadores Bentopack y adaptadores universales LOGiiX World Traveler.</p>
{faq(ORIG, ENVIO)}
""")

# 18. Cases Samsung (24)
add(520149369045, "cases-samsung", "Fundas Samsung Galaxy",
    "Fundas Samsung Galaxy en Guatemala: S22 a S26 | Ventas Guate",
    "Fundas para Samsung Galaxy S22, S23, S24, S25 y S26 en Guatemala: Prodigee, Nimbus9, ITSkins, CLCKR, MyBat, Avana, Click y Spigen.",
    f"""
<p><strong>Fundas para Samsung Galaxy</strong> de la serie S, desde S22 hasta S26, incluyendo Plus y Ultra.</p>
<h2>Busca por modelo</h2>
<ul>
<li>{L('s26-cases','Galaxy S26')} · {L('s26-ultra','S26 Ultra')}</li>
<li>{L('s25-cases','Galaxy S25')}</li>
<li>Galaxy S24, S23 y S22</li>
</ul>
<h2>Marcas</h2>
<p>{L('prodigee','Prodigee')}, {L('nimbus9','Nimbus9')}, ITSkins, CLCKR, MyBat, Avana Velvet MagSafe, Click y Spigen. También protectores de cámara.</p>
{faq(ORIG, ENVIO)}
""")

# 19. iPhone 17 Pro (17)
add(None, "iphone-17-pro", "Fundas iPhone 17 Pro",
    "Fundas iPhone 17 Pro en Guatemala | Prodigee y Nimbus9 | Ventas Guate",
    "Fundas para iPhone 17 Pro: Prodigee Jogger, Flow, Super Hero, Edge, Kickit, Magneteek y Blackout, Nimbus9 Stratus2 y protector de cámara CaseCo.",
    f"""
<p>Fundas originales para el <strong>iPhone 17 Pro</strong>.</p>
<ul>
<li><strong>Uso rudo:</strong> Prodigee Jogger, Blackout y Super Hero.</li>
<li><strong>Color y estilo:</strong> Prodigee Flow (Desert, Night Frost, Blush Frost), Edge y Glow.</li>
<li><strong>Con soporte o magnética:</strong> Prodigee Kickit y Magneteek.</li>
<li><strong>Nimbus9 Stratus2</strong> en Frost y Confetti.</li>
</ul>
<p>Protege la cámara con CaseCo Screen Patrol. Ver todos los iPhone 17 en {L('cases-iphone-17','fundas iPhone 17')}.</p>
{faq(ORIG, ENVIO)}
""")

# 20. Audio gaming (17)
add(None, "audio-gaming", "Audífonos Gaming",
    "Audífonos Gaming en Guatemala: PS5, JBL Quantum | Ventas Guate",
    "Audífonos gaming en Guatemala: Sony PlayStation Pulse Explore para PS5 y JBL Quantum 360P y 100 M2 con micrófono. Originales, 1 año de garantía.",
    f"""
<p><strong>Audífonos gaming</strong> para jugar con mejor sonido y comunicarte con tu equipo.</p>
<ul>
<li><strong>Sony PlayStation Pulse Explore:</strong> inalámbricos para PS5 con drivers planar magnéticos, en Blanco y Midnight.</li>
<li><strong>JBL Quantum 360P:</strong> audífono gaming en blanco.</li>
<li><strong>JBL Quantum 100 M2:</strong> con micrófono, en blanco.</li>
</ul>
<p>Más audio en {L('audio','Audio')} y {L('jbl','JBL')}.</p>
{faq(ORIG, ENVIO)}
""")

# 21. LOGiiX
add(None, "logiix", "LOGiiX",
    "LOGiiX Guatemala: Power Banks, Cargadores y Cables | Ventas Guate",
    "Accesorios LOGiiX en Guatemala: power banks Piston Power, cargadores Power Plus, adaptadores World Traveler, cables y pulseras para Apple Watch.",
    f"""
<p><strong>LOGiiX</strong> diseña accesorios de carga y protección con buen acabado y colores.</p>
<h2>Carga</h2>
<p>Power banks Piston Power (Slim Mag, Classic), cargadores de pared Power Plus Duo y Slim Duo, y kits Vibrance Charging Kit.</p>
<h2>Viaje y cables</h2>
<p>Adaptadores universales World Traveler Lite, cables Vibrance Braid y Wrist Connect.</p>
<h2>Más</h2>
<p>Lápiz Precision para iPad y pulseras Milanese Link para Apple Watch.</p>
<p>Ver también {L('powerbanks','power banks')} y {L('cubos','cargadores de pared')}.</p>
{faq(ORIG, ENVIO)}
""")

# 22. Smartwatch HiFuture
add(None, "smartwatch-hifuture", "Smartwatch HiFuture",
    "Smartwatch HiFuture en Guatemala | Relojes Inteligentes | Ventas Guate",
    "Smartwatches HiFuture en Guatemala: Lume, Aura2, Aurora2, Zone3, Flex2, MIX3 Sport, Ultra3, GO PRO2 y AIX. Originales con 1 año de garantía.",
    f"""
<p>Los <strong>smartwatches HiFuture</strong> ofrecen pantallas grandes, monitoreo de salud y modos deportivos en diseños para cada estilo.</p>
<h2>Modelos</h2>
<ul>
<li><strong>Estilo y uso diario:</strong> Lume, Lume Pro, Aura2, Aurora2 y Edge.</li>
<li><strong>Deportivos:</strong> MIX3 Sport, Vortex Sport, Aurora Sport, Ultra3 Sport, Flex2 y Zone3.</li>
<li><strong>Acero inoxidable:</strong> GO PRO2, Ultra3 Pro y AIX.</li>
<li><strong>Aventura:</strong> Vela Adventure.</li>
</ul>
<p>Compara con otras marcas en {L('smartwatch','Smartwatch')} o mira todo {L('hifuture','HiFuture')}.</p>
{faq(("¿Funcionan con iPhone y Android?", "Sí, se sincronizan con la app del fabricante en ambos sistemas."), ORIG, ENVIO)}
""")

# 23. Over-ear
add(None, "over-ear", "Audífonos Over-Ear",
    "Audífonos Over-Ear y de Diadema en Guatemala | Ventas Guate",
    "Audífonos over-ear y de diadema en Guatemala: Skullcandy Crusher y Hesh, JBL Tour One M2 y T520, HiFuture Tour MKII, Mondo y Urbanista.",
    f"""
<p><strong>Audífonos over-ear</strong> y de diadema para escuchar música por horas con comodidad y, en varios modelos, con cancelación de ruido (ANC).</p>
<h2>Con cancelación de ruido</h2>
<p>Skullcandy Crusher ANC 2 y Hesh 540 ANC, JBL Tour One M2, HiFuture Tour MKII y FutureTour X, y Mondo ANC.</p>
<h2>Bluetooth y con cable</h2>
<p>Skullcandy Hesh 360, Hesh Evo e Icon ANC, Urbanista Miami y Los Angeles (carga solar), y JBL T520 con conexión USB-C.</p>
<p>Para niños: Skullcandy Grom. Más en {L('skullcandy','Skullcandy')} y {L('audifonos','Audífonos')}.</p>
{faq(("¿Qué es ANC?", "Cancelación activa de ruido: reduce el ruido de fondo, útil en viajes, oficina o transporte."), ORIG, ENVIO)}
""")

# 24. Nimbus9
add(None, "nimbus9", "Nimbus9",
    "Nimbus9 Guatemala: Fundas iPhone y Galaxy | Ventas Guate",
    "Fundas Nimbus9 en Guatemala: Cirrus3, Stratus2, Vantage y Alto2 para iPhone y Galaxy, base de carga Qi2 3 en 1 y pulseras para Apple Watch.",
    f"""
<p><strong>Nimbus9</strong> fabrica fundas delgadas con buena protección y compatibilidad magnética.</p>
<h2>Fundas</h2>
<ul>
<li><strong>Cirrus3:</strong> iPhone 17, 17 Pro y iPhone Air.</li>
<li><strong>Stratus2:</strong> iPhone 16, 16 Pro Max, 17 y 17 Pro en Frost y Confetti.</li>
<li><strong>Vantage:</strong> transparente, para iPhone Duo y iPhone Air.</li>
<li><strong>Alto2 y Cirrus2:</strong> para Galaxy.</li>
</ul>
<h2>Carga y Apple Watch</h2>
<p>Base de carga inalámbrica Qi2 3 en 1 y pulseras Nylon Sport Band.</p>
<p>Ver también {L('cases-iphone','fundas para iPhone')} y {L('cases-samsung','fundas Samsung')}.</p>
{faq(ORIG, ENVIO)}
""")

# 25. Cubos
add(None, "cubos", "Cargadores de Pared",
    "Cargadores de Pared USB-C en Guatemala: 20W a 100W | Ventas Guate",
    "Cargadores de pared USB-C en Guatemala: Prodigee Energee 20W, 40W y 65W, Wemiss 40W, adaptadores de viaje Tucano GaN 100W y LOGiiX World Traveler.",
    f"""
<p><strong>Cargadores de pared</strong> (cubos) para celular, tablet y laptop.</p>
<h2>Por potencia</h2>
<ul>
<li><strong>20W:</strong> carga rápida para iPhone. Prodigee Energee Ultra Slim 20W.</li>
<li><strong>40W:</strong> dos dispositivos o carga más rápida. Prodigee Energee 40W y Wemiss 40W.</li>
<li><strong>65W y 100W:</strong> para laptops USB-C. Prodigee Ultra Slim 65W y Tucano Travel Adapter GaN 100W.</li>
</ul>
<h2>Viaje</h2>
<p>Adaptadores universales LOGiiX World Traveler Lite y Prodigee Energee World Traveler.</p>
<p>Combínalo con un {L('cables','cable USB-C')}.</p>
{faq(("¿Qué potencia necesito para mi iPhone?", "Un cargador USB-C de 20W o más permite la carga rápida en iPhone."), ORIG, ENVIO)}
""")

# 26. Cables
add(None, "cables", "Cables USB-C y Lightning",
    "Cables USB-C y Lightning en Guatemala | Function101 | Ventas Guate",
    "Cables USB-C y Lightning en Guatemala: Function Smart Cable con pantalla de potencia, Neat Cable magnético, cables retráctiles y Prodigee Energee.",
    f"""
<p><strong>Cables de carga</strong> USB-C a USB-C, USB-C a Lightning y USB-A a Lightning.</p>
<h2>Function101</h2>
<ul>
<li><strong>Smart Cable:</strong> con pantalla digital que muestra la potencia, de 60W y 100W.</li>
<li><strong>Neat Cable:</strong> magnético, se enrolla sin enredos.</li>
<li><strong>2 in 1 Retractable:</strong> cable retráctil con cargador inalámbrico.</li>
</ul>
<h2>Prodigee Energee</h2>
<p>Cables tipo C, Lightning de 6 pies, magnético C a C, 4 en 1 y cable dual para Apple Watch.</p>
<p>Agrega un {L('cubos','cargador de pared')}.</p>
{faq(ORIG, ENVIO)}
""")

# 27. Carga
add(528059891925, "carga", "Accesorios de Carga",
    "Accesorios de Carga: Cargadores y Power Banks | Ventas Guate",
    "Cargadores de pared, cables, power banks, cargadores para carro y bases inalámbricas en Guatemala. Prodigee, Function101, LOGiiX, Belkin y más.",
    f"""
<p>Todo lo que necesitas para <strong>cargar tus dispositivos</strong> en casa, en la oficina, en el carro o de viaje.</p>
<ul>
<li>{L('cubos','Cargadores de pared')} de 20W a 100W.</li>
<li>{L('cables','Cables')} USB-C y Lightning.</li>
<li>{L('powerbanks','Power banks')} MagSafe y de 10,000 mAh.</li>
<li>Cargadores y soportes para {L('auto','carro')}.</li>
<li>Bases de carga inalámbrica Tekya y Prodigee.</li>
</ul>
<p>También: arrancador de batería Veratek V6 1000A para el carro.</p>
{faq(ORIG, ENVIO)}
""")

# 28. iPhone 16 Pro Max
add(None, "iphone-16-pro-max", "Fundas iPhone 16 Pro Max",
    "Fundas iPhone 16 Pro Max en Guatemala | Ventas Guate",
    "Fundas para iPhone 16 Pro Max: Prodigee Kickit, Formula, Superstar, Pampas, Magneteek y Glow, ZAGG Luxe Snap, Click y Nimbus9 Stratus2.",
    f"""
<p>Fundas originales para el <strong>iPhone 16 Pro Max</strong>.</p>
<ul>
<li><strong>Prodigee:</strong> Kickit, Formula, Superstar, Pampas, Magneteek, Glow y Solid.</li>
<li><strong>ZAGG Luxe Snap</strong> con MagSafe.</li>
<li><strong>Click:</strong> Clear Ombre MagSafe, Ultra Slim y Latch.</li>
<li><strong>Nimbus9 Stratus2</strong> Confetti.</li>
</ul>
<p>Ver todo iPhone 16 en {L('cases-iphone-16','fundas iPhone 16')}.</p>
{faq(ORIG, ENVIO)}
""")

# 29. Auto
add(None, "auto", "Accesorios para Carro",
    "Accesorios para Carro: Cargadores y Soportes | Ventas Guate",
    "Accesorios para carro en Guatemala: cargadores USB-C 30W y 60W, soportes magnéticos con carga inalámbrica Prodigee y arrancador de batería Veratek.",
    f"""
<p><strong>Accesorios para carro</strong> para cargar y sostener tu celular mientras manejas.</p>
<ul>
<li><strong>Cargadores:</strong> Prodigee Energee con Power Delivery 30W, Retract-It 60W con cable retráctil y kit HyperGear 25W.</li>
<li><strong>Soportes con carga inalámbrica:</strong> Prodigee Magneteek Car Mount y Vol. 2.</li>
<li><strong>Soporte universal</strong> Prodigee para Tesla.</li>
<li><strong>Arrancador de batería</strong> Veratek V6 1000A.</li>
</ul>
<p>Ver más en {L('carga','accesorios de carga')}.</p>
{faq(ORIG, ENVIO)}
""")

# 30. Reservas (11,705 sesiones)
add(528406511829, "reservas", "Reservas iPhone",
    "Reserva tu iPhone Nuevo de Lanzamiento en Guatemala | Ventas Guate",
    "Reserva tu iPhone nuevo de lanzamiento en Guatemala con Ventas Guate. Aparta modelo, capacidad y color. Equipos nuevos con 1 año de garantía.",
    f"""
<p>¿Quieres el <strong>iPhone nuevo apenas salga</strong>? En esta sección puedes reservar los modelos de lanzamiento para asegurar tu equipo con Ventas Guate.</p>
<h2>Aparta tu modelo</h2>
<p>Elige el modelo, la capacidad y el color que quieres y aparta tu iPhone de lanzamiento.</p>
<h2>Prepárate para tu nuevo iPhone</h2>
<p>Ten lista la protección desde el primer día: {L('iphone-18','fundas iPhone 18')}, {L('accesorios-iphone-18-pro-max','accesorios para iPhone 18 Pro Max')} y {L('cubos','cargadores de pared')}.</p>
<p>¿Prefieres un equipo disponible hoy? Mira nuestros {L('seminuevos','iPhone seminuevos')}.</p>
{faq(("¿Los iPhone son nuevos?", "Sí, los equipos de esta sección son nuevos y tienen 1 año de garantía."), ("¿Hacen envíos?", "Sí, enviamos a toda Guatemala con entrega garantizada. También puedes comprar en nuestra tienda en zona 13."), TIENDA_Q)}
""")

if __name__ == "__main__":
    json.dump(C, open(os.path.join(AQUI, "textos_colecciones.json"), "w"), ensure_ascii=False, indent=1)
    print(len(C))
