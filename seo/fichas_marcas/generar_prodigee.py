#!/usr/bin/env python3
"""Genera la propuesta de descripciones Prodigee (SOLO PROPUESTA, no escribe en Shopify).

Entrada: JSON con los productos Prodigee activos leídos de Shopify (lista de nodos con
id, title, totalInventory, onlineStoreUrl, descriptionHtml, seo).
Salida: prodigee_propuesta.json, prodigee_respaldo.json y prodigee_sin_fuente.json en esta carpeta.

Fuente: fichas hermanas Prodigee ya publicadas en ventasguate.gt (prodigee.com bloqueado, HTTP 441).
Cada línea reutiliza solo afirmaciones de sus hermanas (ids en FUENTES).
Uso: python3 generar_prodigee.py <productos.json>
"""
import json, re, sys, html, os

AQUI = os.path.dirname(os.path.abspath(__file__))
CIERRE = ("Producto original con 1 año de garantía. Envío a toda Guatemala con pago contra entrega, "
          "o cómpralo en nuestra tienda en zona 13, Ciudad de Guatemala.")
G = "gid://shopify/Product/"

# ---------------- Líneas: intro (1-2 frases) + viñetas, solo afirmaciones de fichas hermanas -------------
L = {
 "kickit17": dict(nombre="KickIt", tipo="funda",
   intro="La funda Prodigee KickIt para {dev} en color {color} tiene soporte integrado para ver videos y hacer videollamadas manos libres. Protege tu {corto} sin descuidar su diseño.",
   li=["Soporte integrado (kickstand) de aluminio para usar tu teléfono en horizontal.",
       "Compatible con MagSafe y accesorios magnéticos.",
       "Doble material: TPU flexible y policarbonato.",
       "Protección contra caídas de hasta 6 ft (1.8 m).",
       "Acabado soft-touch.",
       "Cortes precisos para botones, puertos y cámaras."],
   meta="soporte integrado, MagSafe y caídas de 1.8 m",
   fuentes=["9141945204949 Prodigee Kickit iPhone 17 Air Negro", "9141945270485 Prodigee Kickit iPhone 17 Pro Clear", "9149960487125 descripción actual (stand, MagSafe, doble material)"]),
 "kickit14plus": dict(nombre="KickIt", tipo="funda",
   intro="La funda Prodigee KickIt para {dev} en color {color} tiene soporte integrado para ver videos y hacer videollamadas manos libres. Su material dual suave al tacto protege tu {corto} de golpes y caídas.",
   li=["Soporte integrado (kickstand) para usar tu teléfono en horizontal.",
       "Material dual con acabado suave al tacto.",
       "Imanes integrados compatibles con los accesorios de carga Prodigee con función MagSafe.",
       "Compatible con carga inalámbrica.",
       "Cortes precisos para botones, puertos y cámaras."],
   meta="soporte integrado, material dual e imanes para carga inalámbrica",
   fuentes=["9400707449045 Prodigee Kickit iPhone 14 Plus Negro", "9149918871765 Prodigee Kickit iPhone 16 Rosado"]),
 "kickit_old": dict(nombre="KickIt", tipo="funda",
   intro="La funda Prodigee KickIt para {dev} en color {color} tiene soporte integrado para ver videos y hacer videollamadas manos libres. Protege tu iPhone en el uso diario sin perder estilo.",
   li=["Soporte integrado (kickstand) para usar tu teléfono en horizontal.",
       "Protección contra impactos del uso diario.",
       "Compatible con carga inalámbrica.",
       "Cortes precisos para botones, puertos y cámaras."],
   meta="soporte integrado para ver videos manos libres y carga inalámbrica",
   fuentes=["9149918871765 Prodigee Kickit iPhone 16 Rosado", "9149918675157 Prodigee Kickit iPhone 15 Pro Rosado"]),
 "superglass_cam": dict(nombre="Super Glass Camera", tipo="protector de cámara",
   intro="El Prodigee Super Glass Camera protege los lentes de la cámara trasera de tu {dev} contra rayones, golpes y desgaste diario. Su cristal templado de alta resistencia cuida uno de los componentes más importantes de tu teléfono.",
   li=["Cristal templado de alta resistencia.",
       "Cubre los lentes de la cámara trasera.",
       "Diseño delgado que no afecta la calidad de tus fotos y videos.",
       "Fácil instalación con ajuste preciso al módulo de cámara.",
       "Protección contra rayones, golpes y suciedad."],
   meta="cristal templado contra rayones y golpes, fácil instalación",
   fuentes=["9400708104405 Prodigee Super Glass Camera iPhone 17 Pro / Pro Max Orange", "9271505879253 Prodigee Super Glass Camera Galaxy S26 / S26 Plus", "9170874106069 descripción actual (protector de cámara, vidrio templado, fácil instalación)"]),
 "superstar_new": dict(nombre="Superstar", tipo="funda",
   intro="La funda Prodigee Superstar para {dev} en color {color} tiene un brillo sutil que resalta tu iPhone y lo protege en el día a día. Es delgada, ligera y compatible con MagSafe.",
   li=["Compatible con MagSafe y accesorios magnéticos.",
       "Material TPU resistente.",
       "Bordes elevados en pantalla y cámara.",
       "Grip para un agarre firme.",
       "Protección contra caídas de hasta 6 ft (1.8 m).",
       "Cortes precisos para botones, puertos y cámaras."],
   meta="brillo sutil, MagSafe y caídas de hasta 1.8 m",
   fuentes=["9141946810581 Prodigee Superstar iPhone 17 Air Clear", "9391674261717 Prodigee Superstar iPhone 18 Pro Max/17 Pro Max Space"]),
 "superstar_old": dict(nombre="Superstar", tipo="funda",
   intro="La funda Prodigee Superstar para {dev} en color {color} tiene un brillo sutil que resalta tu iPhone mientras lo protege en el día a día. Su grip evita que se te resbale de la mano.",
   li=["Material TPU resistente.",
       "Grip para un agarre firme sin que se resbale.",
       "Destellos en la parte interna para un acabado brillante.",
       "Bordes elevados en pantalla y cámara para mayor protección.",
       "Cortes precisos para botones, puertos y cámaras."],
   meta="TPU resistente, grip firme y acabado brillante",
   fuentes=["9149925949653 Prodigee Superstar iPhone 15/14/13 Clear", "9141946810581 Prodigee Superstar iPhone 17 Air Clear (cortes precisos)"]),
 "flow17": dict(nombre="Flow", tipo="funda",
   intro="La funda Prodigee Flow para {dev} en color {color} es translúcida, con acabado degradado que combina estilo y protección. Es compatible con MagSafe para cargar y usar accesorios sin quitarla.",
   li=["Compatible con MagSafe y accesorios magnéticos.",
       "Construcción co-moldeada de 3 materiales.",
       "Protección contra impactos.",
       "Bordes elevados en pantalla y cámara.",
       "Cortes precisos para botones, puertos y cámaras."],
   meta="translúcida con degradado, 3 materiales y MagSafe",
   fuentes=["9141943566549 Prodigee Flow iPhone 17 Blush Frost (hermana)", "9141943501013 Prodigee Flow iPhone 17 Air Blush Frost", "9141943632085 Prodigee Flow iPhone 17 Desert"]),
 "safeteeflow": dict(nombre="Safetee Flow", tipo="funda",
   intro="La funda Prodigee Safetee Flow para {dev} en color {color} es translúcida, con acabado degradado que combina estilo y protección. Su construcción de tres materiales ayuda a absorber los golpes del día a día.",
   li=["Construcción co-moldeada de 3 materiales.",
       "Protección contra impactos.",
       "Bordes elevados en pantalla y cámara.",
       "Cortes precisos para botones, puertos y cámaras."],
   meta="translúcida con degradado, 3 materiales y bordes elevados",
   fuentes=["9149922050261 Prodigee Safetee Flow iPhone 16 Night Frost", "9149921493205 Prodigee Safetee Flow iPhone 12 Pro Max Night", "9149921263829 Prodigee Safetee Flow Galaxy S25 Desert"]),
 "neo": dict(nombre="Safetee Neo", tipo="funda",
   intro="La funda Prodigee Safetee Neo para {dev} en color {color} es una funda resistente con esquinas reforzadas que protegen tu teléfono de las caídas del día a día. Sus cortes precisos te dan acceso completo a botones, puertos y cámara, así que no tienes que quitarla para cargar o tomar fotos.",
   li=["Esquinas reforzadas contra caídas.",
       "Acceso completo a puertos y cámara.",
       "Cortes precisos para botones, puertos y cámaras."],
   meta="funda resistente con esquinas reforzadas contra caídas",
   fuentes=["9142004941013 Prodigee Safetee Neo iPhone 14 Plus Ruby", "9149922345173 Prodigee Safetee Neo iPhone 14 Plus Limón"]),
 "smooth": dict(nombre="Safetee Smooth", tipo="funda",
   intro="La funda Prodigee Safetee Smooth para {dev} en color {color} es una funda resistente con esquinas reforzadas que protegen tu teléfono de las caídas del día a día. Sus cortes precisos te dan acceso completo a botones, puertos y cámara, así que no tienes que quitarla para cargar o tomar fotos.",
   li=["Esquinas reforzadas contra caídas.",
       "Acceso completo a puertos y cámara.",
       "Cortes precisos para botones, puertos y cámaras."],
   meta="funda resistente con esquinas reforzadas contra caídas",
   fuentes=["9142022570197 Prodigee Safetee Smooth iPhone 12 Pro Max Smoke"]),
 "rockee": dict(nombre="Rockee", tipo="funda",
   intro="La funda Prodigee Rockee para {dev} en color {color} es una funda resistente con esquinas reforzadas que protegen tu teléfono de las caídas del día a día. Sus bordes elevados ayudan a cuidar la pantalla y la cámara, y sus cortes precisos te dan acceso completo a botones y puertos sin quitarla.",
   li=["Esquinas reforzadas contra caídas.",
       "Bordes elevados para pantalla y cámara.",
       "Acceso completo a puertos y cámara.",
       "Cortes precisos para botones, puertos y cámaras."],
   meta="esquinas reforzadas y bordes elevados para pantalla y cámara",
   fuentes=["9142022471893 Prodigee Rockee iPhone 13 Pro Rosado"]),
 "magneteek": dict(nombre="Magneteek", tipo="funda",
   intro="La funda Prodigee Magneteek para {dev} en color {color} es delgada, de doble material y compatible con MagSafe. Protege tu {corto} contra golpes y caídas sin agregar volumen.",
   li=["Compatible con MagSafe y accesorios magnéticos.",
       "Doble material: flexibilidad y absorción de impactos.",
       "Diseño slim.",
       "Compatible con carga inalámbrica.",
       "Cortes precisos para botones, puertos y cámaras."],
   meta="slim, doble material y compatible con MagSafe",
   fuentes=["9149920116949 Prodigee Magneteek iPhone 16 Pro Max Blanco", "9149920215253 Prodigee Magneteek iPhone 16E/15/14/13 Blanco"]),
 "pampas": dict(nombre="Pampas", tipo="funda",
   intro="La funda Prodigee Pampas para {dev} en color {color} es ultradelgada, con acabado metálico y textura sutil. Es compatible con MagSafe y protege contra caídas de hasta 1.8 m.",
   li=["Compatible con MagSafe y accesorios magnéticos.",
       "Diseño ultradelgado con acabado metálico.",
       "Botones metálicos.",
       "Protección contra caídas de hasta 6 ft (1.8 m).",
       "Cortes precisos para botones, puertos y cámaras."],
   meta="ultradelgada con acabado metálico y MagSafe",
   fuentes=["9149920739541 Prodigee Pampas iPhone 16 Pro Max Breeze", "9149920706773 Prodigee Pampas iPhone 16 Pro Ice"]),
 "balance16": dict(nombre="Balance", tipo="funda",
   intro="La funda Prodigee Balance para {dev} en color {color} tiene acabado suave, agarre cómodo y kickstand integrado. Protege tu {corto} en el día a día y es compatible con MagSafe.",
   li=["Compatible con MagSafe y accesorios magnéticos.",
       "Acabado suave y agarre cómodo.",
       "Kickstand de aleación de aluminio.",
       "Bumpers que absorben impactos.",
       "Bordes elevados para la cámara.",
       "Cortes precisos para botones, puertos y cámaras."],
   meta="kickstand de aluminio, agarre cómodo y MagSafe",
   fuentes=["9142431482069 Prodigee Balance iPhone 16 Negro", "9142431613141 Prodigee Balance iPhone 16 Pro Negro"]),
 "balance_old": dict(nombre="Balance", tipo="funda",
   intro="La funda Prodigee Balance para {dev} en color {color} tiene acabado suave y agarre cómodo para el día a día. Protege tu iPhone con protección anticaídas de grado militar.",
   li=["Acabado suave y agarre cómodo.",
       "Protección anticaídas de grado militar.",
       "Compatible con carga inalámbrica.",
       "Cortes precisos para botones, puertos y cámaras."],
   meta="acabado suave, protección de grado militar y carga inalámbrica",
   fuentes=["9142431187157 Prodigee Balance iPhone 15 Pro Lavender", "9309628924117 descripción actual (grado militar, carga inalámbrica, pantalla 6.1)"]),
 "jogger18": dict(nombre="Jogger", tipo="funda",
   intro="La funda Prodigee Jogger para {dev} en color {color} es deportiva y resistente, con agarre táctico y acabado soft-touch. Ideal si buscas protección de alto rendimiento para el uso diario.",
   li=["Material TPU flexible y policarbonato resistente.",
       "Compatible con MagSafe gracias a sus imanes integrados.",
       "Protección contra caídas de hasta 10 ft (3 m).",
       "Acabado soft-touch.",
       "Agarre táctico antideslizante.",
       "Cortes precisos para botones, puertos y cámaras."],
   meta="agarre táctico, MagSafe y caídas de hasta 3 m",
   fuentes=["9391673966805 Prodigee Jogger iPhone 18 Pro Max/17 Pro Max Army", "9141944942805 Prodigee Jogger iPhone 17 Pro Midnight"]),
 "jogger_s26": dict(nombre="Jogger", tipo="funda",
   intro="La funda Prodigee Jogger para {dev} en color {color} combina diseño funcional, agarre mejorado y protección reforzada. Ideal si buscas seguridad adicional y comodidad diaria.",
   li=["Protección certificada contra caídas de hasta 10 ft (3 m).",
       "Diseño de doble material.",
       "Acabado soft-touch.",
       "Laterales resistentes a impactos.",
       "Tactical Grip integrado para un agarre firme.",
       "Compatible con carga inalámbrica MagSafe."],
   meta="agarre táctico, doble material y caídas de hasta 3 m",
   fuentes=["9271505617109 descripción actual Jogger Galaxy S26 Ultra Midnight", "9271505518805 descripción actual Jogger Galaxy S26 Ultra Army", "9141944942805 Prodigee Jogger iPhone 17 Pro Midnight (línea)"]),
 "revolve": dict(nombre="Revolve", tipo="funda",
   intro="La funda Prodigee Revolve para {dev} en color {color} gira 360° para que alternes entre vertical y horizontal. Ideal para ver videos o hacer videollamadas con más comodidad.",
   li=["Rotación de 360° para usar el iPad en vertical u horizontal.",
       "Ángulo de visión elevado que acerca la pantalla al nivel de los ojos.",
       "Cubierta frontal magnética desmontable.",
       "Carcasa trasera rígida.",
       "Encendido y apagado automático al abrir y cerrar la tapa.",
       "Ranura integrada para Apple Pencil."],
   meta="giro de 360°, cubierta magnética desmontable y ranura para Apple Pencil",
   fuentes=["9170873909461 Prodigee Revolve iPad 10TH Gen 10.9 Negro"]),
 "slim_galaxy": dict(nombre="Safetee Slim", tipo="funda",
   intro="La funda Prodigee Safetee Slim para {dev} en color {color} es delgada y protege tu teléfono en el uso diario. Sus bordes elevados ayudan a cuidar la pantalla y la cámara.",
   li=["Protección contra golpes, caídas leves y rayones del uso diario.",
       "Bordes elevados que ayudan a proteger la pantalla y la cámara.",
       "Cortes precisos para botones, puertos y cámaras."],
   meta="protección contra golpes y rayones con bordes elevados",
   fuentes=["9150255136981 Prodigee Safetee Slim Galaxy S20 Ultra Blanco"]),
 "glow_galaxy": dict(nombre="Glow", tipo="funda",
   intro="La funda Prodigee Glow para {dev} en color {color} es transparente y deja ver el diseño original de tu Galaxy. Protege tu teléfono de golpes, caídas leves y rayones.",
   li=["Diseño transparente que deja ver el color original de tu Galaxy.",
       "Protección contra golpes, caídas leves y rayones del uso diario.",
       "Bordes elevados que ayudan a proteger la pantalla y la cámara.",
       "Cortes precisos para botones, puertos y cámaras."],
   meta="deja ver tu Galaxy, bordes elevados y protección diaria",
   fuentes=["9149916184789 Prodigee Glow Galaxy S23 Clear", "9149916250325 Prodigee Glow Galaxy S23 Plus Clear"]),
 "formula_galaxy": dict(nombre="Formula", tipo="funda",
   intro="La funda Prodigee Formula para {dev} en color {color} tiene un diseño moderno y protección confiable contra los impactos del uso diario. Su ajuste preciso y sus cortes exactos te dan acceso a botones, puertos y cámaras sin tener que quitarla, para que la uses todo el día sin estorbos.",
   li=["Protección contra impactos.",
       "Ajuste preciso.",
       "Cortes precisos para botones, puertos y cámaras."],
   meta="diseño moderno, ajuste preciso y protección contra impactos",
   fuentes=["9149915693269 Prodigee Formula iPhone 16 Pro Max Gris", "9149915594965 Prodigee Formula iPhone 16 Gris"]),
 "hero_iphone": dict(nombre="Hero", tipo="funda",
   intro="La funda Prodigee Hero para {dev} en color {color} es transparente y delgada, así que deja ver el diseño original de tu iPhone mientras lo protege de los impactos del uso diario. Sus cortes precisos te dan acceso a botones, puertos y cámaras sin tener que quitarla.",
   li=["Diseño transparente que deja ver el color original del teléfono.",
       "Protección contra impactos del uso diario.",
       "Cortes precisos para botones, puertos y cámaras."],
   meta="delgada, deja ver tu iPhone y lo protege a diario",
   fuentes=["9149916971221 Prodigee Hero iPhone 15 Pro Clear", "9149917429973 Prodigee iPhone 16 Pro Hero Clear"]),
 "hero_galaxy": dict(nombre="Hero", tipo="funda",
   intro="La funda Prodigee Hero para {dev} en color {color} es transparente y deja ver el diseño original de tu Galaxy. Su construcción reforzada lo protege de las caídas del día a día.",
   li=["Diseño transparente que deja ver el color original de tu Galaxy.",
       "Construcción reforzada pensada para proteger contra caídas del día a día.",
       "Bordes elevados que ayudan a proteger la pantalla y la cámara.",
       "Cortes precisos para botones, puertos y cámaras."],
   meta="construcción reforzada, deja ver tu Galaxy y tiene bordes elevados",
   fuentes=["9149916840149 Prodigee Hero Galaxy S24 Clear", "9149916905685 Prodigee Hero Galaxy S24 Plus Clear"]),
 "superhero": dict(nombre="Super Hero", tipo="funda",
   intro="La funda Prodigee Super Hero para {dev} en color {color} combina una estructura de doble material con un diseño elegante y delgado. Protege tu iPhone de golpes y caídas sin ocultar su apariencia original.",
   li=["Construcción de doble material.",
       "Bumper que absorbe impactos.",
       "Bordes elevados de protección para pantalla y cámara.",
       "Laterales resistentes a impactos.",
       "Diseño ligero y resistente."],
   meta="doble material, bumper que absorbe impactos y bordes elevados",
   fuentes=["9141946745045 Prodigee Super Hero iPhone 17 Smoke", "9141946319061 Prodigee Super Hero iPhone 17 Pro Clear"]),
}

# ---------------- Asignación producto -> (línea, dispositivos, color, corto, dudas) ---------------------
A = {
 "9149960487125": ("kickit17", ["iPhone 17"], "Negro", "iPhone 17", []),
 "9149960388821": ("kickit17", ["iPhone 17 Air"], "Transparente", "iPhone 17 Air", []),
 "9309629055189": ("kickit_old", ["iPhone 15", "iPhone 14", "iPhone 13"], "Rosado", "iPhone", ["Sin hermana publicada 15/14/13; se usaron solo afirmaciones comunes de la línea KickIt (16 Rosado, 15 Pro Rosado)."]),
 "9400707383509": ("kickit14plus", ["iPhone 14 Plus"], "Rosado", "iPhone 14 Plus", []),
 "9170874237141": ("superglass_cam", ["iPhone 17"], "Negro", "iPhone 17", ["Color se refiere al aro del protector; verificar en foto."]),
 "9170873974997": ("superglass_cam", ["iPhone 17 Air"], "Negro", "iPhone 17 Air", ["Título dice 'Black'; se usó 'Negro'. Verificar color del aro en foto."]),
 "9170874466517": ("superglass_cam", ["iPhone 17"], "Plateado", "iPhone 17", ["Título dice 'Silver'."]),
 "9170874040533": ("superglass_cam", ["iPhone 17 Air"], "Plateado con brillo (Glitter Silver)", "iPhone 17 Air", []),
 "9170874106069": ("superglass_cam", ["iPhone 17 Air"], "Plateado", "iPhone 17 Air", ["Título dice 'Silver'."]),
 "9170874171605": ("superglass_cam", ["iPhone 17"], "Plateado con brillo (Glitter Silver)", "iPhone 17", []),
 "9170874335445": ("superglass_cam", ["iPhone 17 Pro", "iPhone 17 Pro Max"], "Negro", "iPhone 17 Pro", []),
 "9149933486293": ("superstar_old", ["iPhone 16"], "Rosado", "iPhone 16", ["No se afirma MagSafe ni prueba de caídas: la única hermana iPhone 16 con ese dato (16 Pro Max Rosado) no está publicada."]),
 "9149933387989": ("superstar_old", ["iPhone 16 Pro"], "Rosado", "iPhone 16 Pro", ["Igual que Superstar iPhone 16: sin MagSafe/caídas por falta de hermana publicada."]),
 "9149926080725": ("superstar_old", ["iPhone 16"], "Transparente", "iPhone 16", ["Sin MagSafe/caídas por falta de hermana publicada iPhone 16."]),
 "9149933125845": ("superstar_old", ["iPhone 16 Pro"], "Transparente", "iPhone 16 Pro", ["Sin MagSafe/caídas por falta de hermana publicada iPhone 16."]),
 "9149933060309": ("superstar_old", ["iPhone 16 Plus"], "Rosado", "iPhone 16 Plus", ["Sin MagSafe/caídas por falta de hermana publicada iPhone 16."]),
 "9149933027541": ("superstar_old", ["iPhone 16 Plus"], "Transparente", "iPhone 16 Plus", ["Sin MagSafe/caídas por falta de hermana publicada iPhone 16."]),
 "9149925884117": ("superstar_old", ["iPhone 15 Pro"], "Rosado", "iPhone 15 Pro", []),
 "9149925982421": ("superstar_old", ["iPhone 15", "iPhone 14", "iPhone 13"], "Rosado", "iPhone", []),
 "9150256578773": ("superstar_old", ["iPhone 12 Pro Max"], "Rosado", "iPhone 12 Pro Max", []),
 "9339362148565": ("superstar_new", ["iPhone 17 Air"], "Space", "iPhone 17 Air", ["Color 'Space' tal como en el título; verificar en foto si es negro/gris translúcido."]),
 "9584081109205": ("superstar_new", ["iPhone 18 Pro", "iPhone 17 Pro"], "Rain", "iPhone", ["Hermana publicada es la versión Pro Max (Space); mismas afirmaciones de línea."]),
 "9170873516245": ("flow17", ["iPhone 17"], "Blush Frost", "iPhone 17", []),
 "9170873450709": ("flow17", ["iPhone 17 Air"], "Night Frost", "iPhone 17 Air", []),
 "9400707940565": ("safeteeflow", ["iPhone 16 Pro Max"], "Night Frost", "iPhone 16 Pro Max", []),
 "9150029889749": ("safeteeflow", ["iPhone 11 Pro"], "Passion", "iPhone 11 Pro", []),
 "9150016946389": ("safeteeflow", ["iPhone 11 Pro"], "Night", "iPhone 11 Pro", ["Título 'Prodigee Safetee Flow Night 11 Pro' no dice 'iPhone'; no se cambia el título."]),
 "9150029660373": ("safeteeflow", ["iPhone 12 Pro Max"], "Passion", "iPhone 12 Pro Max", ["Título con errata 'Safete'; no se cambia en esta fase."]),
 "9149965762773": ("safeteeflow", ["Samsung Galaxy S25 Ultra"], "Night Frost", "Galaxy S25 Ultra", ["Afirmación de 3 materiales viene de hermanas iPhone de la línea; la hermana Galaxy solo dice protección y bordes elevados."]),
 "9310361419989": ("safeteeflow", ["Samsung Galaxy S25 Ultra"], "Desert", "Galaxy S25 Ultra", ["Afirmación de 3 materiales viene de hermanas iPhone de la línea."]),
 "9321272803541": ("neo", ["iPhone 13"], "Menta", "iPhone 13", ["Título dice 'Neo Mag': no se afirma MagSafe/imanes porque ninguna hermana Neo publicada lo indica. Confirmar con producto físico."]),
 "9321273852117": ("neo", ["iPhone 13"], "Limón", "iPhone 13", []),
 "9291022106837": ("neo", ["iPhone 15", "iPhone 14", "iPhone 13"], "Lemon", "iPhone", []),
 "9291022139605": ("neo", ["iPhone 15", "iPhone 14", "iPhone 13"], "Ruby", "iPhone", []),
 "9321273426133": ("neo", ["iPhone 13 Pro"], "Peach", "iPhone 13 Pro", ["'Neo Mag': no se afirma MagSafe sin fuente."]),
 "9321275162837": ("neo", ["iPhone 13"], "Peach", "iPhone 13", ["'Neo Mag': no se afirma MagSafe sin fuente."]),
 "9321273163989": ("neo", ["iPhone 13 Pro"], "Menta", "iPhone 13 Pro", ["'Neo Mag': no se afirma MagSafe sin fuente."]),
 "9321274245333": ("neo", ["iPhone 14 Pro"], "Ruby", "iPhone 14 Pro", []),
 "9321275490517": ("neo", ["iPhone 14 Pro"], "Limón", "iPhone 14 Pro", []),
 "9150254416085": ("neo", ["iPhone 14 Pro Max"], "Lila", "iPhone 14 Pro Max", []),
 "9319023640789": ("neo", ["iPhone 14 Pro Max"], "Ruby", "iPhone 14 Pro Max", ["Título no dice 'iPhone' ('Safetee Neo 14 Pro Max Ruby'); no se cambia."]),
 "9150015930581": ("smooth", ["iPhone 12 Pro Max"], "Gris", "iPhone 12 Pro Max", []),
 "9335556538581": ("smooth", ["iPhone 14 Pro"], "Negro", "iPhone 14 Pro", []),
 "9150028939477": ("rockee", ["iPhone 12", "iPhone 12 Pro"], "Menta", "iPhone", []),
 "9400707809493": ("rockee", ["iPhone 12", "iPhone 12 Pro"], "Rosado", "iPhone", []),
 "9400707875029": ("rockee", ["iPhone 13"], "Rosado", "iPhone 13", []),
 "9150026481877": ("magneteek", ["iPhone 16 Pro Max"], "Negro", "iPhone 16 Pro Max", []),
 "9319024001237": ("magneteek", ["iPhone 14 Pro Max"], "Negro", "iPhone 14 Pro Max", []),
 "9400707612885": ("magneteek", ["iPhone 13 Pro Max"], "Negro", "iPhone 13 Pro Max", []),
 "9400707743957": ("pampas", ["iPhone 16 Pro Max"], "Ice", "iPhone 16 Pro Max", []),
 "9400706760917": ("balance16", ["iPhone 16"], "Transparente", "iPhone 16", []),
 "9400706859221": ("balance16", ["iPhone 16 Pro Max"], "Negro", "iPhone 16 Pro Max", []),
 "9309628924117": ("balance_old", ["iPhone 15", "iPhone 14", "iPhone 13"], "Lavanda", "iPhone", ["Meta actual menciona precio de liquidación; la nueva no lleva precio."]),
 "9584075866325": ("jogger18", ["iPhone 18 Pro", "iPhone 17 Pro"], "Burgundy", "iPhone", []),
 "9584078815445": ("jogger18", ["iPhone 18 Pro Max", "iPhone 17 Pro Max"], "Midnight", "iPhone", ["Título termina en 'New'; no se cambia en esta fase."]),
 "9271505617109": ("jogger_s26", ["Samsung Galaxy S26 Ultra"], "Midnight", "Galaxy S26 Ultra", ["'Carga inalámbrica MagSafe' viene del texto actual del producto; Galaxy no usa MagSafe nativo, confirmar si trae imanes."]),
 "9271505518805": ("jogger_s26", ["Samsung Galaxy S26 Ultra"], "Army", "Galaxy S26 Ultra", ["'Carga inalámbrica MagSafe' viene del texto actual; confirmar si trae imanes."]),
 "9150028153045": ("revolve", ["iPad 11 Pro"], "Negro", "iPad", ["Hermana es Revolve iPad 10.ª gen; mismas funciones de línea. Confirmar generación exacta del 'iPad 11 Pro' (y que tenga ranura para Apple Pencil) antes de publicar."]),
 "9150255202517": ("slim_galaxy", ["Samsung Galaxy S22 Plus"], "Negro", "Galaxy S22 Plus", []),
 "9299472646357": ("glow_galaxy", ["Samsung Galaxy S23 Ultra"], "Transparente", "Galaxy S23 Ultra", []),
 "9310361354453": ("formula_galaxy", ["Samsung Galaxy S25 Ultra"], "Gris", "Galaxy S25 Ultra", ["Hermanas Formula son iPhone 16 con MagSafe; en Galaxy no se afirma MagSafe."]),
 "9335556440277": ("hero_iphone", ["iPhone 14 Pro"], "Transparente", "iPhone 14 Pro", []),
 "9400707252437": ("hero_galaxy", ["Samsung Galaxy S24 Ultra"], "Transparente", "Galaxy S24 Ultra", ["Título dice 'Hero S24 Ultra' sin 'Galaxy'; no se cambia."]),
 "9149924507861": ("superhero", ["iPhone 16 Pro"], "Transparente", "iPhone 16 Pro", ["Hermanas Super Hero son iPhone 17; no se afirma MagSafe ni prueba de 10 ft para iPhone 16 Pro."]),
}

SIN_FUENTE = {
 "9149923721429": "Sparkle Leemonchelo: no hay hermana publicada con descripción.",
 "9149923688661": "Sparkle Leemonchelo: no hay hermana publicada con descripción.",
 "9319024066773": "Sparkle Leemonchelo: no hay hermana publicada con descripción.",
 "9149915562197": "Folio Mag Wallet: solo existe su propio texto corto (folio con tarjetas); sin hermana.",
 "9142022242517": "Billetera Universal: solo texto propio genérico (tamaño/color); sin especificaciones.",
 "9142431711445": "Billetera Universal: solo texto propio genérico (tamaño/color); sin especificaciones.",
 "9150256021717": "Sidekick: sin hermana con descripción.",
 "9149923754197": "Strap & Go: sin hermana con descripción.",
 "9149923786965": "Strap & Go: sin hermana con descripción.",
 "9150018453717": "Cross-It Strap: sin hermana con descripción.",
 "9150018519253": "Cross-It Strap: sin hermana con descripción.",
 "9400706924757": "Cross-It Strap: sin hermana con descripción.",
 "9150016127189": "Safetee Transforme: solo 2 afirmaciones en su texto actual; sin hermana.",
 "9150027759829": "Magwallet Ease: la hermana Magwallet Pop es otro modelo.",
 "9149933617365": "Tesla Soporte Universal Mag: la única hermana (Tesla Soporte Universal para Carro) no está publicada y es otra versión.",
 "9150018879701": "Energee to Go Powerbank Wireless 10000mAh: sin hermana; no se inventan potencias.",
 "9150026809557": "MagPower 2 Go 10000 mAh: hermanas MagPower to-Go 10K se contradicen (USB-C 20 W vs 30 W); no se puede asegurar cuál es.",
 "9150027006165": "MagPower to Go 5mAh: capacidad del título ambigua (¿5,000 mAh / Slim 5K?); sin fuente segura.",
 "9150255595733": "Safetee Steel: sin hermana con descripción.",
 "9335556604117": "Safetee Steel: sin hermana con descripción.",
 "9335556636885": "Safetee Steel: sin hermana con descripción.",
 "9339362312405": "Cubo de Carga Dual 20W: la hermana Ultra Slim 20W es de un puerto; no aplica.",
 "9400707023061": "Handsfree Vent: la hermana Handsfree Magnet Pro es otro modelo y no está publicada.",
 "9149978804437": "Hands Free Soporte Universal (escritorio): sin hermana.",
 "9301031551189": "Energee Magstand: sin hermana (Mag Station 2 en 1 es otro producto).",
 "9150256808149": "The Sleeve funda MacBook: sin hermana; tamaño de MacBook no indicado.",
 "15398000394453": "Tile iPhone 18/17 Pro Max: sin hermana Tile con descripción.",
 "9611528372437": "PowerStrap 1FT: sin hermana con descripción; no se inventan potencia ni conectores.",
 "9611528798421": "PowerStrap 1FT: sin hermana con descripción.",
 "9611529257173": "PowerStrap 4FT: sin hermana con descripción.",
}

TIPO_SEO = {"funda": "Funda", "protector de cámara": "Protector de cámara"}


def dev_txt(devs):
    if len(devs) == 1:
        return devs[0]
    if all(d.startswith("iPhone ") for d in devs):
        partes = [devs[0]] + [d.replace("iPhone ", "") for d in devs[1:]]
        return ", ".join(partes[:-1]) + " y " + partes[-1]
    return ", ".join(devs[:-1]) + " y " + devs[-1]


def dev_corto(devs):
    if len(devs) == 1:
        return devs[0].replace("Samsung ", "")
    if all(d.startswith("iPhone ") for d in devs):
        return devs[0] + "/" + "/".join(d.replace("iPhone ", "") for d in devs[1:])
    return " / ".join(d.replace("Samsung ", "") for d in devs)


def construir(pid, nodo):
    linea, devs, color, corto, dudas = A[pid]
    d = L[linea]
    dev = dev_txt(devs)
    intro = d["intro"].format(dev=dev, color=color, corto=corto)
    lis = list(d["li"]) + [f"Color: {color}."]
    htmlp = (f"<p>{intro}</p>\n<h2>Características</h2>\n<ul>\n"
             + "".join(f"<li>{x}</li>\n" for x in lis)
             + "</ul>\n<h2>Compatibilidad</h2>\n<ul>\n"
             + "".join(f"<li>{x}</li>\n" for x in devs)
             + f"</ul>\n<p>{CIERRE}</p>")
    tipo = TIPO_SEO[d["tipo"]]
    dc = dev_corto(devs)
    col_corto = color.split(" (")[0]
    cands = [f"{tipo} Prodigee {d['nombre']} {dc} {col_corto} | Ventas Guate",
             f"{tipo} Prodigee {d['nombre']} {dc} {col_corto}",
             f"{tipo} Prodigee {d['nombre']} {dc} | Ventas Guate",
             f"Prodigee {d['nombre']} {dc} {col_corto}",
             f"Prodigee {d['nombre']} {dc}"]
    seo_title = next(c for c in cands if len(c) <= 60)
    metas = [f"{tipo} Prodigee {d['nombre']} para {dc} color {col_corto}: {d['meta']}. Envío a toda Guatemala.",
             f"{tipo} Prodigee {d['nombre']} para {dc}: {d['meta']}. Envío a toda Guatemala.",
             f"Prodigee {d['nombre']} para {dc}: {d['meta']}. Envío en Guatemala."]
    seo_desc = next(m for m in metas if len(m) <= 155)
    return {"id": G + pid, "title": nodo["title"], "totalInventory": nodo.get("totalInventory"),
            "linea": linea, "html": htmlp, "seo_title": seo_title, "seo_description": seo_desc,
            "fuentes": ["Fichas hermanas publicadas en ventasguate.gt (ids Shopify): " + "; ".join(d["fuentes"]),
                        "prodigee.com/products.json bloqueado (HTTP 441) el 2026-11-21"],
            "dudas": dudas}


def main(src):
    nodos = {n["id"].split("/")[-1]: n for n in json.load(open(src))}
    faltan = [k for k in list(A) + list(SIN_FUENTE) if k not in nodos]
    assert not faltan, faltan
    prop = [construir(pid, nodos[pid]) for pid in A]
    prop.sort(key=lambda p: -(p["totalInventory"] or 0))
    sinf = sorted(({"id": G + k, "title": nodos[k]["title"], "totalInventory": nodos[k].get("totalInventory"),
                    "dudas": ["SIN FUENTE: " + v]} for k, v in SIN_FUENTE.items()), key=lambda x: -(x["totalInventory"] or 0))
    resp = [{"id": G + k, "title": nodos[k]["title"], "descriptionHtml": nodos[k]["descriptionHtml"],
             "seo": nodos[k]["seo"]} for k in list(A) + list(SIN_FUENTE)]
    json.dump(prop, open(os.path.join(AQUI, "prodigee_propuesta.json"), "w"), ensure_ascii=False, indent=1)
    json.dump(sinf, open(os.path.join(AQUI, "prodigee_sin_fuente.json"), "w"), ensure_ascii=False, indent=1)
    json.dump(resp, open(os.path.join(AQUI, "prodigee_respaldo.json"), "w"), ensure_ascii=False, indent=1)
    print(len(prop), "propuestas;", len(sinf), "SIN FUENTE;", len(resp), "en respaldo")


if __name__ == "__main__":
    main(sys.argv[1])
