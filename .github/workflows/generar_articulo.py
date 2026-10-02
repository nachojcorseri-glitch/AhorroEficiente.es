"""
Genera artículos nuevos automáticamente, en español e inglés, a partir de las colas
temas_es.csv / temas_en.csv, usando la API gratuita de Gemini, y los deja en
_posts/ y _posts_en/ listos para revisar. Un fallo en un idioma no bloquea al otro.

Variables de entorno:
  GEMINI_API_KEY   (obligatoria) tu clave gratuita de https://aistudio.google.com/
  GEMINI_MODEL     (opcional) por defecto "gemini-3.1-flash-lite".
  SITE_NAME_ES / SITE_NICHE_ES   (opcionales) contexto para el lado español.
  SITE_NAME_EN / SITE_NICHE_EN   (opcionales) contexto para el lado inglés.

Si a un idioma se le acaban los temas "pendiente", el script le pide más ideas a la
IA automáticamente antes de rendirse con ese idioma.
"""

import csv
import datetime
import os
import re
import sys
import unicodedata

import requests


def _opcional(nombre_var: str, valor_por_defecto: str) -> str:
    """Como os.environ.get, pero trata una variable VACÍA igual que si no existiera
    (un secret de GitHub sin rellenar llega como cadena vacía, no como ausente)."""
    valor = os.environ.get(nombre_var)
    return valor if valor else valor_por_defecto


GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = _opcional("GEMINI_MODEL", "gemini-3.1-flash-lite")

IDIOMAS = {
    "es": {
        "temas_csv": "temas_es.csv",
        "posts_dir": "_posts",
        "site_name": _opcional("SITE_NAME_ES", "Ahorro Eficiente"),
        "site_niche": _opcional(
            "SITE_NICHE_ES",
            "ahorro energético y eficiencia en el hogar para hogares hispanohablantes "
            "(España y Latinoamérica): factura de la luz y el gas, electrodomésticos "
            "eficientes, domótica, autoconsumo solar y consejos prácticos de ahorro",
        ),
        "idioma_humano": "español",
    },
    "en": {
        "temas_csv": "temas_en.csv",
        "posts_dir": "_posts_en",
        "site_name": _opcional("SITE_NAME_EN", "Ahorro Eficiente"),
        "site_niche": _opcional(
            "SITE_NICHE_EN",
            "home energy costs and savings for a worldwide English-speaking audience: "
            "appliance power usage, heating and cooling costs, smart home devices, "
            "off-grid power and DIY energy efficiency",
        ),
        "idioma_humano": "English",
    },
}


CATEGORIAS = [
    ("tarifas", "gauge", [
        "tarifa", "factura", "pvpc", "potencia contratada", "discriminación horaria",
        "bono social", "bill", "rate", "meter",
    ]),
    ("electrodomesticos", "plug", [
        "electrodoméstico", "frigorífico", "lavadora", "lavavajillas", "congelador",
        "aire acondicionado", "refrigerator", "freezer", "air conditioner", "fan",
        "appliance", "gaming pc",
    ]),
    ("solar", "sun", ["solar", "autoconsumo", "placas", "off-grid", "off grid"]),
    ("domotica", "bulb", [
        "enchufe inteligente", "termostato", "domótica", "smart plug", "smart thermostat",
        "coche eléctrico", "electric car", "heat pump", "bomba de calor",
    ]),
]


def categorizar(titulo: str, palabra_clave: str):
    """Elige categoría e icono para un artículo según su título/palabra clave,
    con una categoría por defecto si no coincide con ninguna conocida."""
    texto = f"{titulo} {palabra_clave}".lower()
    for slug, icono, palabras in CATEGORIAS:
        if any(p in texto for p in palabras):
            return slug, icono
    return "ahorro", "house"


def slugify(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    texto = re.sub(r"[^a-zA-Z0-9\s-]", "", texto).strip().lower()
    return re.sub(r"\s+", "-", texto)[:60].strip("-")


def leer_temas(ruta_csv: str):
    with open(ruta_csv, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def guardar_temas(ruta_csv: str, temas):
    with open(ruta_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["titulo", "palabra_clave", "estado"])
        writer.writeheader()
        writer.writerows(temas)


def llamar_gemini(prompt: str) -> str:
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "Falta la variable de entorno GEMINI_API_KEY. Añádela como 'secret' en GitHub."
        )

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
    headers = {"Content-Type": "application/json", "x-goog-api-key": GEMINI_API_KEY}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    r = requests.post(url, headers=headers, json=payload, timeout=120)
    if r.status_code != 200:
        raise RuntimeError(
            f"Error {r.status_code} llamando a Gemini (modelo '{GEMINI_MODEL}'): "
            f"{r.text[:500]} — comprueba el nombre del modelo en "
            "https://ai.google.dev/gemini-api/docs/models si el error lo menciona."
        )

    data = r.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise RuntimeError(f"Respuesta inesperada de Gemini: {data}")


def construir_prompt_articulo(cfg, titulo: str, palabra_clave: str) -> str:
    return f"""Actúa como redactor experto y honesto para {cfg['site_name']}.

Escribe un artículo completo en {cfg['idioma_humano']} sobre: "{titulo}"
Palabra clave objetivo: "{palabra_clave}"

Requisitos:
- Entre 900 y 1300 palabras.
- Tono claro y cercano, sin relleno genérico ni frases vacías.
- Aporta ejemplos o cifras concretas SOLO si son razonables y generales; si no estás
  seguro de un dato, exprésalo en términos generales en vez de inventarlo.
- Estructura en Markdown: un H1 al principio, varios H2/H3, listas cuando ayuden,
  y una conclusión práctica.
- Si el tema toca dinero, salud o decisiones legales, incluye un aviso breve de que
  es información general y no asesoramiento profesional individualizado.
- Si el tema incluye algo específico de un país o región (mecanismos regulatorios,
  programas concretos de ayuda, etc.), acláralo explícitamente en vez de darlo por
  universal para cualquier lector.
- No repitas el título tal cual dentro del cuerpo como si fuera un H2.
- Escribe TODO el artículo (título, cuerpo, avisos) en {cfg['idioma_humano']}; no
  mezcles idiomas.

Devuelve SOLO el Markdown del artículo, sin explicaciones antes ni después."""


def construir_prompt_temas(cfg, temas_existentes, cuantos: int = 8) -> str:
    titulos_existentes = "\n".join(f"- {t['titulo']}" for t in temas_existentes) or "(ninguno todavía)"
    return f"""Eres un estratega de contenidos SEO para una web sobre: {cfg['site_niche']}.

Ya existen estos artículos (no los repitas ni propongas variaciones casi idénticas):
{titulos_existentes}

Propón {cuantos} títulos de artículo NUEVOS, evergreen, en {cfg['idioma_humano']}, con
intención de búsqueda real. Evita títulos que dependan de precios o cifras que cambian
a menudo; prioriza guías, comparativas de conceptos y consejos prácticos que sigan
siendo válidos con el tiempo. Prefiere ángulos concretos y específicos (un aparato, una
comparación puntual) antes que titulares genéricos y muy competidos.

Devuelve SOLO {cuantos} líneas, una por artículo, exactamente en este formato:
titulo|palabra_clave

Sin numeración, sin explicaciones antes ni después, sin nada más."""


def generar_mas_temas(cfg, temas_existentes, cuantos: int = 8):
    respuesta = llamar_gemini(construir_prompt_temas(cfg, temas_existentes, cuantos))
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


def procesar_idioma(codigo: str, cfg: dict):
    """Genera un artículo para un idioma. Devuelve (ruta, titulo)."""
    temas = leer_temas(cfg["temas_csv"])
    pendiente = next(
        (t for t in temas if t.get("estado", "").strip().lower() == "pendiente"), None
    )

    if not pendiente:
        print(f"[{codigo}] No quedan temas pendientes: pidiendo ideas nuevas a la IA...")
        nuevos = generar_mas_temas(cfg, temas)
        if not nuevos:
            raise RuntimeError("no se pudieron generar temas nuevos")
        temas.extend(nuevos)
        guardar_temas(cfg["temas_csv"], temas)
        pendiente = nuevos[0]
        print(f"[{codigo}] Se han añadido {len(nuevos)} temas nuevos.")

    titulo = pendiente["titulo"].strip()
    palabra_clave = pendiente.get("palabra_clave", "").strip()

    print(f"[{codigo}] Generando artículo para: {titulo}")
    contenido = llamar_gemini(construir_prompt_articulo(cfg, titulo, palabra_clave))

    hoy = datetime.date.today().isoformat()
    slug = slugify(titulo) or "articulo"
    ruta = os.path.join(cfg["posts_dir"], f"{hoy}-{slug}.md")

    categoria_slug, categoria_icono = categorizar(titulo, palabra_clave)
    titulo_yaml = titulo.replace('"', "'")
    front_matter = (
        "---\n"
        "layout: post\n"
        f'title: "{titulo_yaml}"\n'
        f"date: {hoy} 09:00:00 +0200\n"
        f"categories: [{categoria_slug}]\n"
        f"icon: {categoria_icono}\n"
        "---\n\n"
    )

    os.makedirs(cfg["posts_dir"], exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(front_matter + contenido.strip() + "\n")

    pendiente["estado"] = "borrador-generado"
    guardar_temas(cfg["temas_csv"], temas)

    print(f"[{codigo}] Artículo generado en: {ruta}")
    return ruta, titulo


def escribir_salida_github(nombre: str, valor: str):
    ruta_salida = os.environ.get("GITHUB_OUTPUT")
    if not ruta_salida:
        return
    with open(ruta_salida, "a", encoding="utf-8") as f:
        valor_limpio = valor.replace("\n", " ").replace('"', "'")
        f.write(f"{nombre}={valor_limpio}\n")


def main():
    resultados = []
    errores = []

    for codigo, cfg in IDIOMAS.items():
        try:
            ruta, titulo = procesar_idioma(codigo, cfg)
            resultados.append((codigo, ruta, titulo))
        except Exception as e:
            print(f"[{codigo}] ERROR: {e}")
            errores.append((codigo, str(e)))

    if not resultados:
        print("No se ha generado ningún artículo en ningún idioma.")
        sys.exit(1)

    resumen = " | ".join(f"{c.upper()}: {t}" for c, _, t in resultados)
    if errores:
        resumen += " | Fallos: " + ", ".join(f"{c.upper()} ({m})" for c, m in errores)

    escribir_salida_github("resumen", resumen)
    escribir_salida_github("hubo_contenido", "si")
    print("Resumen:", resumen)


if __name__ == "__main__":
    main()
