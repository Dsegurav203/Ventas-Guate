# Cambios del tema pendientes de publicar (tema en vivo "Fix Buscador + Error Popup")

Shopify no dejó publicarlos desde aquí porque 15 archivos del tema (configuración, plantillas, header y footer) se editaron en el editor de Shopify después de guardar nuestra versión. Publicar habría sobrescrito esas ediciones con versiones viejas.

Se aplican a mano desde Admin → Tienda online → Temas → "..." → Editar código (edita el tema en vivo directamente, sin conflicto):

1. **Snippets → Agregar snippet** `store-schema` y pegar el contenido de `store-schema.liquid` (este directorio).
2. **layout/theme.liquid**: justo antes de `</head>` agregar:
   `{%- if template.name == 'index' -%}{%- render 'store-schema' -%}{%- endif -%}`
3. **sections/article-template.liquid** (líneas ~351-358), reemplazar:
   - `"articleBody": "{{ article.content | strip_html | escape }}",` → `"articleBody": {{ article.content | strip_html | strip_newlines | json }},`
   - `"headline": "{{ article.title }}",` → `"headline": {{ article.title | json }},`
   - `"description": "{{ article.excerpt | strip_html | escape }}",` → `"description": {{ article.excerpt | strip_html | strip_newlines | json }},`
4. Guardar. Verificar en https://search.google.com/test/rich-results con https://ventasguate.gt
