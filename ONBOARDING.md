# Guía de inicio · Luis Hernández (ecommerce Ventas Guate)

Bienvenido. Este repositorio concentra todo el trabajo de SEO y catálogo de **ventasguate.gt** hecho con Claude: qué se cambió, por qué, los respaldos para revertir y las herramientas para seguir. Claude lee `CLAUDE.md` al iniciar, así que trabaja con las mismas reglas que Diego.

## 1. Configuración (una sola vez)

1. **Claude Code**: abre este repositorio (`dsegurav203/Ventas-Guate`, rama de trabajo indicada por Diego) en claude.ai/code o en la app de escritorio.
2. **Conectores** en claude.ai → Configuración → Conectores:
   - **Shopify** (tienda ventas-guate-1) con tu usuario de staff.
   - **Odoo Ventas Guate** con tu usuario.
3. **Tus credenciales de Odoo** (para los scripts): en Odoo → Mi perfil → Seguridad de la cuenta → Nueva clave API. Configúralas como variables de entorno del entorno de Claude (no en archivos):
   `ODOO_URL=https://ventasguate.odoo.com`, `ODOO_DB=…`, `ODOO_USER=lhernandez@ventasguate.com`, `ODOO_API_KEY=<tu clave>`.
   Así cada cambio queda registrado a tu nombre.

## 2. Reglas de oro (resumen de `CLAUDE.md`)

- Nada se escribe en Shopify u Odoo sin propuesta y "aprobado".
- Siempre respaldo antes de cambiar; todo reversible.
- No inventar especificaciones; sin precios en descripciones ni metas.
- Títulos con marca + modelo + compatibilidad + color, sin MAYÚSCULAS ni "L-". Si cambias un título en Shopify, también en Odoo.
- Conector: **nunca** "Set Basic Detail".
- Tema: solo el publicado. Si vas a editar en el editor de Shopify, avisa a Diego (choca con los cambios guardados por API).

## 3. Qué se hizo (18–19 nov 2026)

Reporte completo: [`seo/reporte/Reporte_SEO_VentasGuate_2026-11-19.pdf`](seo/reporte/Reporte_SEO_VentasGuate_2026-11-19.pdf) (también en tu tarea #15 de Odoo).

| Tema | Resultado | Carpeta |
|---|---|---|
| Catálogo | 2,458 marcas, 2,621 títulos, 6,589 alt text, duplicados con 301 | `seo/handoff/` |
| Marcas prioritarias | HiFuture, Skullcandy, OhSnap | `seo/hifuture/`, `seo/skullcandy/`, `seo/ohsnap/` |
| Colecciones | 30 textos con FAQ; 18 páginas inútiles fuera de Google | `seo/colecciones/` |
| Top 100 vendidos | 32 fichas nuevas + 53 completadas; títulos y marcas | `seo/top100/` |
| Páginas | Envíos, Garantía, Contacto, Preguntas frecuentes + footer | `seo/VISIBILIDAD_IA_2026-11-19.md` |
| Odoo | Nombres sincronizados, liquidación por etiqueta, OFI BODEGA 13 exporta stock | `seo/handoff/`, `seo/top100/CATALOGO_FALTANTE.md` |
| Imágenes | 15 LAUT en Odoo, 8 en Shopify | `seo/imagenes/` |
| Velocidad | Diagnóstico y correcciones de popup y filtros | `seo/tema/` |

## 4. Tus pendientes inmediatos

1. **Tarea #15 en Odoo (pasos 1–7)**: ficha de tienda (`seo/tema/store-schema.liquid`), JSON-LD del blog, filtros en móvil y popup. Instrucciones con código en la tarea y en `seo/tema/INSTRUCCIONES_PUBLICAR.md`.
2. **Políticas** (Admin → Configuración → Políticas): garantía de seminuevos 30 días (texto en `seo/politicas/garantia_nueva.html`), punto 9 de Términos, y crear política de envíos.
3. **Conector**: exportar a Shopify los productos nuevos con stock (LAUT Crystal Matter X iPhone 18, Zuro Folio iPad Pro 11, Sympl) — lista en `seo/top100/no_existen_shopify.json`.

## 5. Cómo pedirle trabajo a Claude

Habilidades del proyecto (escribe `/` y el nombre, o pídelo en palabras):

| Habilidad | Para qué | Ejemplo de pedido |
|---|---|---|
| `/seo-ficha-producto` | Descripciones y SEO de productos con datos del fabricante | "Haz las fichas de los 20 productos LAUT más vendidos sin descripción" |
| `/seo-coleccion` | Textos y FAQ de colecciones; ocultar campañas de Google | "Escribe el texto de la colección Fundas iPhone 18" |
| `/imagenes-catalogo` | Fotos oficiales a Odoo y Shopify | "Busca fotos para los productos ocultos sin imagen" |
| `/catalogo-faltante` | Productos vendidos que no están en línea | "¿Qué productos con stock no se ven en la tienda?" |
| `/velocidad-tema` | Medir y corregir velocidad | "Mide la velocidad del inicio y de colecciones" |

Plugin SEO general (ya configurado): `/seo audit https://ventasguate.gt`, `/seo page <url>`, `/seo schema <url>`.

Consejos: pide siempre la propuesta primero ("muéstrame antes de publicar"); revisa el `.md` de propuesta; responde "aprobado" para aplicar.

## 6. Pendientes del proyecto (compartidos con Diego)

- Fichas del fabricante para Prodigee Orbit 360, Geo y Torte (iPhone 18/17 Pro Max).
- Fotos para 11 productos con stock que siguen ocultos (`seo/top100/reactivacion.json` → `sin_foto`).
- Revisar 192 productos de Odoo sin coincidencia en Shopify (`seo/handoff/odoo_sync_resultado_final.csv`).
- Quitar el aviso de Galaxy Week en 5 fundas cuando termine la campaña.
- Velocidad fase 2: JavaScript, CSS y píxel de Facebook.
- Visibilidad en IA (22/100): reseñas en Google Business, guías comparativas en el blog.
- Medir en Search Console a las 4 y 8 semanas (impresiones, clics, posición por colección).

Dudas: Diego Segura.
