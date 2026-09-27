"""
Genera UN artículo nuevo a partir del primer tema "pendiente" en temas.csv,
usando la API gratuita de Gemini, y lo guarda en _posts/ listo para revisar.

Variables de entorno:
  GEMINI_API_KEY     (obligatoria) tu clave gratuita de https://aistudio.google.com/
  GEMINI_MODEL       (opcional) por defecto "gemini-flash-latest".
                      Si el script falla con "modelo no encontrado", entra en
                      https://ai.google.dev/gemini-api/docs/models y pon aquí
                      el nombre exacto del modelo "Flash" actual.
  SITE_NAME          (opcional) nombre de tu web, para dar contexto al prompt.
  SITE_NICHE         (opcional) descripción de una frase de tu nicho. Se usa para que la
                      IA proponga temas nuevos ella sola cuando temas.csv se quede vacío.
  CONTENT_LANGUAGE   (opcional) "es" (por defecto) o "en".

Si no queda ningún tema "pendiente" en temas.csv, el script le pide a la IA que
proponga temas nuevos automáticamente (a partir de SITE_NICHE) antes de rendirse,
para que la cola nunca se quede seca sin que tengas que pensar tú los títulos.
"""

import csv
import datetime
import os
import re
import sys
import unicodedata

import requests

TEMAS_CSV = "temas.csv"
POSTS_DIR = "_posts"

SITE_NAME = os.environ.get("SITE_NAME", "Ahorro Eficiente")
SITE_NICHE = os.environ.get(
    "SITE_NICHE",
    "ahorro energético y eficiencia en el hogar para viviendas en España: "
    "factura de la luz y el gas, electrodomésticos eficientes, domótica, "
    "autoconsumo solar y consejos prácticos de ahorro",
)
CONTENT_LANGUAGE = os.environ.get("CONTENT_LANGUAGE", "es")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-flash-latest")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")


def slugify(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    texto = re.sub(r"[^a-zA-Z0-9\s-]", "", texto).strip().lower()
    return re.sub(r"\s+", "-", texto)[:60].strip("-")


def leer_temas():
    with open(TEMAS_CSV, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def guardar_temas(temas):
    with open(TEMAS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["titulo", "palabra_clave", "estado"])
        writer.writeheader()
        writer.writerows(temas)


def construir_prompt(titulo: str, palabra_clave: str) -> str:
    idioma = "español" if CONTENT_LANGUAGE == "es" else "English"
    return f"""Actúa como redactor experto y honesto para {SITE_NAME}.

Escribe un artículo completo en {idioma} sobre: "{titulo}"
Palabra clave objetivo: "{palabra_clave}"

Requisitos:
- Entre 900 y 1300 palabras.
- Tono claro y cercano, sin relleno genérico ni frases vacías tipo "en el mundo actual".
- Aporta ejemplos o cifras concretas SOLO si son razonables y generales; si no estás
  seguro de un dato, exprésalo en términos generales en vez de inventarlo.
- Estructura en Markdown: un H1 al principio, varios H2/H3, listas cuando ayuden,
  y una conclusión práctica.
- Si el tema toca dinero, salud o decisiones legales, incluye un aviso breve de que
  es información general y no asesoramiento profesional individualizado.
- No repitas el título tal cual dentro del cuerpo como si fuera un H2.

Devuelve SOLO el Markdown del artículo, sin explicaciones antes ni después."""


def llamar_gemini(prompt: str) -> str:
    if not GEMINI_API_KEY:
        sys.exit(
            "Falta la variable de entorno GEMINI_API_KEY. "
            "Añádela como 'secret' en GitHub (ver README.md)."
        )

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
    headers = {"Content-Type": "application/json", "x-goog-api-key": GEMINI_API_KEY}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    r = requests.post(url, headers=headers, json=payload, timeout=120)
    if r.status_code != 200:
        sys.exit(
            f"Error {r.status_code} llamando a Gemini (modelo '{GEMINI_MODEL}'):\n"
            f"{r.text[:800]}\n\n"
            "Si el error menciona el modelo, comprueba el nombre actual en "
            "https://ai.google.dev/gemini-api/docs/models y actualiza el secret "
            "GEMINI_MODEL en GitHub."
        )

    data = r.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        sys.exit(f"Respuesta inesperada de Gemini: {data}")


def generar_mas_temas(temas_existentes, cuantos: int = 8):
    """Pide a la IA nuevos títulos de artículo cuando temas.csv se queda sin pendientes,
    para que la cola de contenido nunca se agote sin intervención humana."""
    titulos_existentes = "\n".join(f"- {t['titulo']}" for t in temas_existentes) or "(ninguno todavía)"

    prompt = f"""Eres un estratega de contenidos SEO para una web sobre: {SITE_NICHE}.

Ya existen estos artículos (no los repitas ni propongas variaciones casi idénticas):
{titulos_existentes}

Propón {cuantos} títulos de artículo NUEVOS, evergreen, en español, con intención de
búsqueda real. Evita títulos que dependan de precios o cifras que cambian a menudo
(por ejemplo, evita "mejor tarifa en [mes/año]"); prioriza guías, comparativas de
conceptos y consejos prácticos que sigan siendo válidos con el tiempo.

Devuelve SOLO {cuantos} líneas, una por artículo, exactamente en este formato:
titulo|palabra_clave

Sin numeración, sin explicaciones antes ni después, sin nada más."""

    respuesta = llamar_gemini(prompt)
    nuevos = []
    for linea in respuesta.strip().splitlines():
        linea = linea.strip().lstrip("-").strip()
        if "|" not in linea:
            continue
        titulo, _, palabra_clave = linea.partition("|")
        titulo = titulo.strip().strip('"')
        palabra_clave = palabra_clave.strip().strip('"')
        if titulo:
            nuevos.append({"titulo": titulo, "palabra_clave": palabra_clave, "estado": "pendiente"})
    return nuevos


def escribir_salida_github(nombre: str, valor: str):
    ruta_salida = os.environ.get("GITHUB_OUTPUT")
    if not ruta_salida:
        return
    with open(ruta_salida, "a", encoding="utf-8") as f:
        valor_limpio = valor.replace("\n", " ").replace('"', "'")
        f.write(f"{nombre}={valor_limpio}\n")


def main():
    temas = leer_temas()
    pendiente = next(
        (t for t in temas if t.get("estado", "").strip().lower() == "pendiente"), None
    )

    if not pendiente:
        print("No quedan temas pendientes: pidiendo ideas nuevas a la IA...")
        nuevos = generar_mas_temas(temas)
        if not nuevos:
            print("No se pudieron generar temas nuevos. Revisa temas.csv manualmente.")
            return
        temas.extend(nuevos)
        guardar_temas(temas)
        pendiente = nuevos[0]
        print(f"Se han añadido {len(nuevos)} temas nuevos a temas.csv.")

    titulo = pendiente["titulo"].strip()
    palabra_clave = pendiente.get("palabra_clave", "").strip()

    print(f"Generando artículo para: {titulo}")
    contenido = llamar_gemini(construir_prompt(titulo, palabra_clave))

    hoy = datetime.date.today().isoformat()
    slug = slugify(titulo) or "articulo"
    ruta = os.path.join(POSTS_DIR, f"{hoy}-{slug}.md")

    titulo_yaml = titulo.replace('"', "'")
    front_matter = (
        "---\n"
        "layout: post\n"
        f'title: "{titulo_yaml}"\n'
        f"date: {hoy} 09:00:00 +0200\n"
        "categories: [articulos]\n"
        "---\n\n"
    )

    os.makedirs(POSTS_DIR, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(front_matter + contenido.strip() + "\n")

    pendiente["estado"] = "borrador-generado"
    guardar_temas(temas)

    print(f"Artículo generado en: {ruta}")
    escribir_salida_github("ruta", ruta)
    escribir_salida_github("titulo", titulo)


if __name__ == "__main__":
    main()
