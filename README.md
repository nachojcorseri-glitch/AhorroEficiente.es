# Web que se escribe sola 


Este proyecto es una web de contenido (Jekyll) que se aloja gratis en GitHub Pages y que,
cada pocos días, genera un artículo nuevo con IA (API gratuita de Gemini) y te lo deja
como Pull Request para que le eches un vistazo de un par de minutos antes de publicarlo.

No es "cero esfuerzo para siempre": es "esfuerzo mínimo y concentrado en lo que importa
(darle un vistazo rápido a cada borrador)". Más abajo explico por qué merece la pena esa
pequeña revisión.

---

## 0. El nicho ya viene elegido: ahorro energético en el hogar

Te la dejo montada sobre "ahorro y eficiencia energética en el hogar" (factura de la
luz y el gas, electrodomésticos eficientes, domótica, autoconsumo solar). Lo elegí así
y no con el nicho más obvio y "de mayor CPC teórico" (tarjetas/seguros/préstamos) porque:

- Tiene intención de búsqueda comercial real (gente decidiendo qué contratar o comprar).
- No está monopolizado por 3-4 sitios imposibles de superar, como sí pasa en finanzas puras.
- Es mayoritariamente evergreen: la mayoría de los 18 títulos de `temas.csv` no dependen
  de precios que cambian cada mes, así que el contenido no caduca ni obliga a estar
  verificando cifras constantemente.
- Combina bien con AdSense y, más adelante, con afiliación (Amazon y similares) en los
  artículos de electrodomésticos.

`temas.csv` ya trae 18 artículos listos para generar. Cuando se agoten, el propio script
le pide más ideas a la IA automáticamente (ver `generar_mas_temas` en
`generar_articulo.py`) — no hace falta que pienses tú los siguientes títulos.

Si prefieres otro tema, es tan fácil como reescribir `temas.csv` y el título de
`_config.yml` — puedes usar `PROMPT-MAESTRO-NICHO.md` con Claude para planificar uno
distinto cuando quieras.

## 1. Crea la cuenta y el repositorio en GitHub (gratis)

1. Crea una cuenta en https://github.com si no tienes una.
2. Pulsa "New repository". Ponle un nombre (por ejemplo, el de tu web) y márcalo como
   **público** (los repos públicos tienen minutos ilimitados de Actions gratis; con uno
   privado también funciona, pero con un límite mensual de minutos).
3. Sube todos los archivos de esta carpeta a ese repositorio (arrastrándolos desde la web
   de GitHub con "Add file → Upload files", o con `git` si ya lo usas).

## 2. Activa GitHub Pages

1. En tu repositorio, ve a **Settings → Pages**.
2. En "Build and deployment", elige **Source: Deploy from a branch**, rama `main`, carpeta `/root`.
3. Guarda. En un par de minutos tu web estará en `https://tu-usuario.github.io/tu-repo`.

## 3. Consigue tu clave gratuita de Gemini

1. Entra en https://aistudio.google.com/ con una cuenta de Google.
2. Genera una **API key** gratuita (no pide tarjeta para este paso).
3. En tu repositorio de GitHub, ve a **Settings → Secrets and variables → Actions**.
4. Añade estos "Repository secrets":
   - `GEMINI_API_KEY`: la clave que acabas de generar. Esta es la única obligatoria.
   - `SITE_NAME`: el nombre de tu web (opcional; por defecto "Ahorro Eficiente").
   - `SITE_NICHE`: una frase describiendo tu nicho (opcional; ya trae por defecto el de
     ahorro energético). Solo hace falta si cambias de tema y quieres que la IA proponga
     temas nuevos acertados cuando `temas.csv` se quede vacío.
   - `CONTENT_LANGUAGE`: `es` o `en` (opcional, por defecto `es`).
   - `GEMINI_MODEL`: déjalo vacío al principio. Solo lo necesitas si el modelo por
     defecto (`gemini-flash-latest`) da error — los nombres de modelo de Google cambian
     con frecuencia. Si eso pasa, entra en
     https://ai.google.dev/gemini-api/docs/models, copia el nombre del modelo "Flash"
     actual y ponlo aquí.

## 4. Activa la publicación automática

1. Ve a la pestaña **Actions** de tu repositorio y actívalas si te lo pide.
2. En **Settings → Actions → General → Workflow permissions**, marca
   "Read and write permissions" y también "Allow GitHub Actions to create and approve
   pull requests". Sin esto, el flujo no podrá abrir los Pull Requests con los borradores.
3. Ya está. El flujo (`.github/workflows/generar-articulo.yml`) se ejecuta solo los
   lunes y jueves, y también puedes lanzarlo a mano desde "Actions →
   Generar artículo automático → Run workflow" para probarlo ahora mismo.

Cada vez que se ejecute, si hay un tema "pendiente" en `temas.csv`, te aparecerá una
Pull Request nueva con el artículo dentro de `_posts/`.

## 5. Revisa cada borrador antes de fusionar (esto es importante)

Cuando llegue una Pull Request:

1. Ábrela y lee el artículo (5-10 minutos).
2. Corrige cualquier frase que suene genérica, cualquier dato que parezca inventado, o
   añade algo que tú sepas de primera mano.
3. Pulsa **Merge pull request**. En cuanto la rama `main` se actualiza, GitHub Pages
   despliega la web con el artículo ya publicado.

**Por qué este paso no es opcional si quieres que esto funcione a medio plazo:** desde
2026 Google persigue activamente lo que llama "abuso de contenido a escala" — publicar
muchas páginas generadas por IA sin revisión humana ni valor añadido puede hacer que un
sitio pierda toda su visibilidad en buscadores de golpe. Un repaso corto por artículo es
justo la diferencia entre "contenido asistido por IA" (que puede posicionar bien) y
"spam generado en serie" (que Google penaliza). Google AdSense tampoco acepta sitios de
contenido exclusivamente generado por IA sin revisión.

## 6. Prepárate para Google y AdSense

- Rellena `privacidad.md` y `sobre.md` con tus datos reales (son plantillas de partida).
- Da de alta tu web en **Google Search Console** (gratis) para que Google la indexe antes.
- Cuando tengas 15-20 artículos publicados y revisados, solicita
  **Google AdSense** (gratis, sin coste por apuntarte). Ten en cuenta:
  - Necesitas ser mayor de 18 años.
  - Google aprueba mejor sitios con **dominio propio** (ver punto 7) que con subdominios
    gratuitos tipo `.github.io`.
  - Si tienes visitantes en la UE, necesitas un aviso/banner de cookies con consentimiento
    (busca "Google AdSense Privacy & messaging" o "Funding Choices" para configurarlo
    gratis desde tu cuenta de AdSense).

## 7. El único gasto real: un dominio propio (opcional pero recomendable)

Todo lo anterior es gratis. Lo único que de verdad conviene pagar, si quieres tomártelo
en serio, es un dominio propio (un .com o .es suele rondar 10-15 €/año en registradores
como Namecheap o Cloudflare). Un dominio de verdad multiplica tus probabilidades de que
AdSense apruebe el sitio frente a un subdominio gratuito. Puedes seguir usando GitHub
Pages gratis y solo apuntar tu dominio nuevo hacia él (GitHub explica cómo en
"Settings → Pages → Custom domain").

## 8. Cuando esto empiece a generar ingresos

Si el sitio empieza a dar dinero de forma recurrente, en España lo normal es darte de
alta como autónomo para poder facturarlo/declararlo. No hace falta el primer día que
actives AdSense, pero no lo dejes de lado cuando la cosa funcione — esto no es
asesoramiento legal ni fiscal, así que para tu caso concreto conviene confirmarlo con un
gestor o con la Agencia Tributaria.

---

## Estructura del proyecto

```
_config.yml            → configuración de Jekyll
index.md               → portada (lista los artículos automáticamente)
privacidad.md          → plantilla de política de privacidad
sobre.md               → plantilla de página "sobre"
temas.csv              → cola de temas a escribir (título, palabra clave, estado)
generar_articulo.py    → script que llama a Gemini y crea el artículo
requirements.txt       → dependencias de Python
_posts/                → aquí caen los artículos (uno de ejemplo incluido)
.github/workflows/     → el flujo que automatiza todo
PROMPT-MAESTRO-NICHO.md → prompt para planificar el nicho con IA
```

## Ideas para más adelante (no imprescindibles para empezar)

- Añadir Google Analytics.
- Cambiar el tema visual de Jekyll (hay temas gratuitos compatibles con GitHub Pages).
- Añadir enlaces de afiliación donde tenga sentido (siempre con su aviso correspondiente),
  sobre todo en los artículos de electrodomésticos.
