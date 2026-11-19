# Visibilidad en IA: Ventas Guate (19/11/2026)

Puntaje: **22/100**. Antes: 27/10/2026, sin puntaje formal; 0 de 6 consultas con presencia.

## Pruebas (buscador web, índice EE.UU.; aproximación a lo que leen ChatGPT, Gemini y Perplexity)

| Consulta | ¿Aparece Ventas Guate? | Quién aparece |
|---|---|---|
| Ventas Guate tienda accesorios celulares | No | Pacifiko (Gadget TechStore), Samsung, Unicomer |
| Dónde comprar fundas Prodigee en Guatemala | No | Pacifiko (1 funda de tablet), eBay, Cyberpuerta MX |
| HiFuture Guatemala distribuidor | No | Pacifiko (7 smartwatches HiFuture) |
| Skullcandy Guatemala tienda original | No | Pacifiko (20 fichas) |
| Mejor tienda Alexa Echo Dot Guatemala | No | Pacifiko (único resultado) |
| iPhone seminuevo Guatemala con garantía | No | Pacifiko (vendedores del marketplace, 30 días) |

**Lectura:** Pacifiko ocupa todas las respuestas. Ventas Guate no existe como entidad para las IA, aunque tiene más catálogo en Prodigee, HiFuture, Skullcandy y Alexa.

## Puntaje

| Dimensión | 0-10 | Nota |
|---|---|---|
| Presencia | 0 | 0 de 6 consultas |
| Precisión | 3 | Organization schema sin dirección, teléfono ni horario |
| Sentimiento | 5 | Neutral (sin menciones) |
| Posición | 0 | — |
| Completitud | 2 | Faltan páginas Envíos, Garantía y Contacto con datos |
| Consistencia | 3 | Correo .com vs .gt; dos teléfonos |

## Estado técnico

| Señal | Estado |
|---|---|
| Robots.txt | ✅ No bloquea bots de IA |
| llms.txt | ⚠️ Existe, pero es el genérico de Shopify (instrucciones de compra); no dice quién es Ventas Guate |
| Schema Organization | ⚠️ Solo nombre, logo, Facebook e Instagram |
| Schema ElectronicsStore (dirección, NIT, horario, pagos) | ❌ |
| /pages/contact | ❌ Vacía |
| /pages/envios, /pages/garantia | ❌ 404 |
| Política de envíos | ❌ No existe |
| Colecciones con texto y FAQ | ✅ 30 nuevas (19/11) |
| Google Business Profile | ❓ Sin verificar |

## Plan (orden de impacto)

1. **Google Business Profile verificado** (Alto). Es la fuente principal de Google y Gemini para negocios locales.
2. **Schema ElectronicsStore en el tema** (Alto). Dirección, teléfono, NIT, horario, pago contra entrega y redes. Necesita horario y teléfono confirmados.
3. **Páginas Envíos, Garantía y Contacto** (Alto). Pago contra entrega, entrega garantizada, 1 año para nuevos y 30 días para seminuevos.
4. **Publicar en Pacifiko como vendedor** (Alto). Las IA ya citan Pacifiko; estar ahí con la marca "Ventas Guate" da menciones inmediatas.
5. **Guías comparativas en el blog** (Medio): "HiFuture vs Xiaomi vs Amazfit", "Dónde comprar Prodigee en Guatemala", "Echo Dot vs Echo Spot vs Echo Dot Max".
6. **Menciones de terceros** (Medio): reseñas en Google, Facebook, Reddit r/guatemala, Encuentra24 y prensa local de tecnología.
7. **Unificar datos** (Medio): correo .gt en todas las políticas y un solo teléfono o WhatsApp público.

## Datos que faltan confirmar

- Horario de la tienda en zona 13.
- Teléfono público: 4149-9168 o WhatsApp 4027-3277.
- Marcas de las que Ventas Guate es distribuidor oficial por contrato.
- Costo y tiempo de envío (capital e interior).
- ¿Hay perfil de Google Business y cuenta de vendedor en Pacifiko?

## Aplicado 19/11/2026
- Páginas creadas: /pages/envios (Q25 capital mismo día, Q35 interior próximo día, pago contra entrega) y /pages/garantia (1 año nuevos, 30 días seminuevos, devoluciones 15 días).
- /pages/contact con dirección, horario, WhatsApp 4027-3277, marcas oficiales y canales (Pacifiko, Kemik, Max, Walmart, Guatemala Digital).
- Tema en vivo "Fix Buscador + Error Popup" (187700674773): snippet `store-schema` (ElectronicsStore) en inicio + JSON-LD del blog corregido. Guardado; pendiente de publicar (theme_publish).
- Nota: el JSON-LD del blog del 18/11 se había guardado en el tema no publicado "Fix Galería + Popups"; ahora está en el tema en vivo.
- JBL y Reebok confirmados como marcas oficiales (14 en total); agregados a schema, contacto y garantía. Textos de colecciones JBL y Reebok se mantienen.
- Footer "Información importante": agregados Contacto y horario, Envíos y formas de pago, Garantía y devoluciones.
