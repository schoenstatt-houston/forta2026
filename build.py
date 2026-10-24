#!/usr/bin/env python3
"""Genera una página por pareja para Forta 2026.

Uso:  python3 build.py
- Lee la lista PAREJAS de abajo.
- Si existe fotos/<slug>.jpg la usa como fondo del encabezado.
- El video debe estar en videos/<slug>.mp4.
"""
import html
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

EVENTO = "Fortalecimiento Matrimonial Houston 2026"

# (número, nombre para mostrar, slug)
PAREJAS = [
    ("01", "Antonio y Verónica", "01-antonio-y-veronica"),
    ("02", "Nelson y Jessica", "02-nelson-y-jessica"),
    ("03", "Álvaro y Deyna", "03-alvaro-y-deyna"),
    ("04", "Luis y Lourdes", "04-luis-y-lourdes"),
    ("05", "Ricky y Lorena", "05-ricky-y-lorena"),
    ("06", "Samuel y Judith", "06-samuel-y-judith"),
    ("07", "Gilbert y Bertha", "07-gilbert-y-bertha"),
    ("09", "Rodrigo y Andrea", "09-rodrigo-y-andrea"),
    ("10", "Carlos y María Elisa", "10-carlos-y-maria-elisa"),
    ("11", "José y Adriana", "11-jose-y-adriana"),
    ("12", "Andrés y Erika", "12-andres-y-erika"),
    ("13", "Lalo y Mayra", "13-lalo-y-mayra"),
    ("14", "Mario y Nora", "14-mario-y-nora"),
    ("15", "Miguel y Lucy", "15-miguel-y-lucy"),
    ("16", "Ricardo y Marre", "16-ricardo-y-marre"),
    ("17", "Gerardo y Mónica", "17-gerardo-y-monica"),
    ("18", "Andrés y Lina", "18-andres-y-lina"),
    ("19", "Hermilio y Mónica", "19-hermilio-y-monica"),
    ("20", "Carlos y Adriana", "20-carlos-y-adriana"),
    ("21", "Jonathan y Perla", "21-jonathan-y-perla"),
    ("22", "Héctor y Sandra", "22-hector-y-sandra"),
]

HEAD = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{title}</title>
<link rel="icon" href="{prefix}assets/logo.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600&family=Lato:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}assets/style.css">
</head>
"""

PAGE = HEAD + """<body>
<header class="hero{hero_class}"{hero_style}>
  <div class="brand"><img src="../assets/logo.jpg" alt="Logo Forta"><span>Forta 2026</span></div>
  <p class="eyebrow">{evento}</p>
  <h1>{nombre}</h1>
</header>

<main>
  <div class="video-card">
    <video controls playsinline preload="metadata">
      <source src="../videos/{slug}.mp4" type="video/mp4">
      Tu navegador no puede reproducir este video.
    </video>
  </div>
  <p class="note">Toca el video para reproducirlo.</p>
</main>

<footer>
  <img src="../assets/logo.jpg" alt="">
  Schoenstatt Houston &middot; {evento}
</footer>
</body>
</html>
"""

LANDING = HEAD + """<body>
<div class="landing">
  <div>
    <img src="assets/logo.jpg" alt="Logo Forta">
    <h1>{evento}</h1>
    <p>Abre el enlace personal que recibiste para ver tu video.</p>
  </div>
</div>
</body>
</html>
"""


def build():
    missing_video = []
    for num, nombre, slug in PAREJAS:
        foto = os.path.join(ROOT, "fotos", f"{slug}.jpg")
        has_photo = os.path.exists(foto)
        if not os.path.exists(os.path.join(ROOT, "videos", f"{slug}.mp4")):
            missing_video.append(slug)

        out_dir = os.path.join(ROOT, slug)
        os.makedirs(out_dir, exist_ok=True)
        page = PAGE.format(
            title=html.escape(f"{nombre} · Forta 2026"),
            prefix="../",
            evento=html.escape(EVENTO),
            nombre=html.escape(nombre),
            slug=slug,
            hero_class="" if has_photo else " no-photo",
            hero_style=f' style="background-image:url(\'../fotos/{slug}.jpg\')"' if has_photo else "",
        )
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(page)

    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(LANDING.format(title="Forta 2026", prefix="", evento=html.escape(EVENTO)))

    with open(os.path.join(ROOT, "robots.txt"), "w") as f:
        f.write("User-agent: *\nDisallow: /\n")
    open(os.path.join(ROOT, ".nojekyll"), "w").close()

    print(f"{len(PAREJAS)} páginas generadas.")
    if missing_video:
        print("Falta el video de:", ", ".join(missing_video))


if __name__ == "__main__":
    build()
