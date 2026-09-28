#!/usr/bin/env python3
"""Génère le site Sans Gluten Festival : accueil, une page par ville, 404, sitemap.

Usage : python3 tools/build_pages.py   (depuis le dossier du site)
Tout le contenu (villes, textes, titres) se modifie ici, puis on relance le script.
"""
import json
import os
from datetime import date
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://sansglutenfestival.fr"
TODAY = date.today().isoformat()
INSTAGRAM = "https://www.instagram.com/sansglutenfestival/"
EMAIL = "contact@sansglutenfestival.fr"

# slug, nom, région, couleur de fond, couleur d'encre, texte de la ville
CITIES = [
    ("montpellier", "Montpellier", "Occitanie", "tomate", "creme",
     "Le soleil presque toute l’année, les ruelles de l’Écusson, les terrasses de la Comédie et la mer à deux pas. Imaginez un Sans Gluten Festival ici : des food trucks, un verre au soleil, et tout ce que vous voulez manger, sans rien demander."),
    ("paris", "Paris", "Île-de-France", "basilic", "creme",
     "Les quais de Seine, le canal Saint-Martin, les marchés du dimanche et les terrasses à chaque coin de rue. Imaginez un Sans Gluten Festival ici : un petit coin de Paris où tout se mange, sans lire les étiquettes."),
    ("lyon", "Lyon", "Auvergne-Rhône-Alpes", "moutarde", "cacao",
     "Deux fleuves, les traboules du Vieux-Lyon, la vue depuis Fourvière et une vraie passion pour la bonne table. Imaginez un Sans Gluten Festival dans la capitale de la gastronomie : on relève le défi."),
    ("marseille", "Marseille", "Provence", "citron", "basilic",
     "Le Vieux-Port, les calanques, la Bonne Mère qui veille sur la ville et le soleil qui ne lâche rien. Imaginez un Sans Gluten Festival ici : food trucks, apéro, et la mer pas loin."),
    ("toulouse", "Toulouse", "Occitanie", "guimauve", "framboise",
     "La ville rose, la place du Capitole, les bords de Garonne et les couchers de soleil sur les quais de la Daurade. Imaginez un Sans Gluten Festival ici : ça tombe bien, on a déjà la couleur."),
    ("bordeaux", "Bordeaux", "Nouvelle-Aquitaine", "framboise", "guimauve",
     "Le miroir d’eau, la pierre blonde, les quais au soleil et l’art de bien vivre à table. Imaginez un Sans Gluten Festival ici : des food trucks, un verre sur les quais, et tout le monde à la même table."),
    ("lille", "Lille", "Hauts-de-France", "lavande", "prune",
     "La Grand-Place, les pavés du Vieux-Lille, les estaminets et un sens de l’accueil que tout le monde envie au Nord. Imaginez un Sans Gluten Festival ici : la convivialité, on n’aura pas à vous l’expliquer."),
    ("nantes", "Nantes", "Loire-Atlantique", "abricot", "cacao",
     "Le grand éléphant des Machines de l’île, la Loire, le château des ducs de Bretagne et une ville qui ne s’ennuie jamais. Imaginez un Sans Gluten Festival dans la ville du petit-beurre : on relève le défi."),
    ("strasbourg", "Strasbourg", "Alsace", "prune", "abricot",
     "La Petite France, les maisons à colombages, la cathédrale et l’odeur des bretzels à chaque coin de rue. Imaginez un Sans Gluten Festival ici : des bretzels ? On ne promet rien, mais on cherche."),
    ("geneve", "Genève", "Suisse", "creme", "tomate",
     "Le jet d’eau, le lac Léman, les ruelles de la vieille ville et, par temps clair, le Mont-Blanc en toile de fond. Imaginez un Sans Gluten Festival au bord du lac : food trucks, soleil et chocolat."),
]
TICKER = ["Le rendez-vous sans gluten de votre ville", "Food trucks et bar", "Petit, familial, convivial",
          "Sans chichi", "Sans file d’attente", "Sans lire les étiquettes"]
GRAINS = ["tomate", "abricot", "moutarde", "citron", "basilic", "lavande", "prune", "framboise", "guimauve"]
SANS = [
    ("Sans chichi", "Pas de grande scène, pas de décor XXL. Des stands, des tables, des gens."),
    ("Sans file d’attente", "Un rendez-vous à taille humaine : on vient, on mange, on discute avec ceux qui cuisinent."),
    ("Sans lire les étiquettes", "Tout est sans gluten. Pour une fois, vous n’avez rien à demander."),
]


def fr(s):
    """Espaces insécables avant : ; ! ? (typographie française)."""
    for p in (":", ";", "!", "?"):
        s = s.replace(" " + p, "\u00a0" + p)
    return s


def grain(color, cls="", empty=False):
    fill = "none" if empty else f"var(--{color})"
    stroke = f' stroke="var(--{color})" stroke-width="2"' if empty else ""
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 20 12" aria-hidden="true"><ellipse cx="10" cy="6" rx="8.5" ry="4.6" transform="rotate(-24 10 6)" fill="{fill}"{stroke}/></svg>'


def city_grain(slug, cls=""):
    c = next(c for c in CITIES if c[0] == slug)
    if slug == "geneve":
        return grain("tomate", cls, empty=True)
    return grain(c[3], cls)


def head(title, desc, path, jsonld, og="/img/og-image.png", og_alt="Logo du Sans Gluten Festival"):
    url = SITE + path
    return f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(desc)}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta property="og:site_name" content="Sans Gluten Festival">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:url" content="{url}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="fr_FR">
  <meta property="og:image" content="{SITE}{og}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{escape(og_alt)}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#2B1810">
  <link rel="icon" href="/favicon.png" type="image/png" sizes="64x64">
  <link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="preload" href="/fonts/ZingRust-Base.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/site.css">
  <script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
</head>
<body>
"""


def ticker():
    def group(offset):
        out = ""
        for i, t in enumerate(TICKER + TICKER):
            out += f'<span class="tk-item">{t}</span>' + grain(GRAINS[(i + offset) % len(GRAINS)], "tk-grain")
        return f'<div class="tk-group">{out}</div>'
    return f"""  <div class="ticker" role="region" aria-label="Au programme">
    <p class="sr">{'. '.join(TICKER)}.</p>
    <div class="tk-track" aria-hidden="true">
      {group(0)}
      {group(0)}
    </div>
  </div>
"""


def header(is_home):
    img = """<picture>
          <source srcset="/img/logo-sgf.webp" type="image/webp">
          <img src="/img/logo-sgf.png" width="1400" height="495" alt="Sans Gluten Festival">
        </picture>"""
    if is_home:
        inner = f'<h1 class="logo">{img}</h1>'
    else:
        inner = f'<p class="logo"><a href="/" aria-label="Sans Gluten Festival, accueil">{img}</a></p>'
    return f"""  <header class="site-header">
    <div class="wrap">
      {inner}
    </div>
  </header>
"""


def form(city_slug, city_name, suffix=""):
    fid = f"email-{city_slug}{suffix}"
    return f"""<form class="notify" data-city="{city_name}">
            <label class="sr" for="{fid}">Votre email pour être prévenu de la date à {city_name}</label>
            <input type="email" id="{fid}" name="email" placeholder="Votre email" autocomplete="email" required>
            <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
            <button type="submit">OK</button>
          </form>"""


SHARE_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12v7a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-7M12 3v12M7.5 7.5 12 3l4.5 4.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def share(slug, name):
    url = f"{SITE}/{slug}/"
    text = f"Le Sans Gluten Festival arrive à {name} 🌾 Le rendez-vous sans gluten de votre ville : {url}"
    from urllib.parse import quote
    return (f'<a class="share" href="https://wa.me/?text={quote(text)}" target="_blank" rel="noopener" '
            f'data-url="{url}" data-text="{escape(text)}">{SHARE_ICON}Prévenir un ami</a>')


def footer():
    cities = "".join(f'<li><a href="/{c[0]}/">{city_grain(c[0])}{c[1]}</a></li>' for c in CITIES)
    grains = "".join(grain(g) for g in GRAINS)
    insta = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M7.0301.084c-1.2768.0602-2.1487.264-2.911.5634-.7888.3075-1.4575.72-2.1228 1.3877-.6652.6677-1.075 1.3368-1.3802 2.127-.2954.7638-.4956 1.6365-.552 2.914-.0564 1.2775-.0689 1.6882-.0626 4.947.0062 3.2586.0206 3.6671.0825 4.9473.061 1.2765.264 2.1482.5635 2.9107.308.7889.72 1.4573 1.388 2.1228.6679.6655 1.3365 1.0743 2.1285 1.38.7632.295 1.6361.4961 2.9134.552 1.2773.056 1.6884.069 4.9462.0627 3.2578-.0062 3.668-.0207 4.9478-.0814 1.28-.0607 2.147-.2652 2.9098-.5633.7889-.3086 1.4578-.72 2.1228-1.3881.665-.6682 1.0745-1.3378 1.3795-2.1284.2957-.7632.4966-1.636.552-2.9124.056-1.2809.0692-1.6898.063-4.948-.0063-3.2583-.021-3.6668-.0817-4.9465-.0607-1.2797-.264-2.1487-.5633-2.9117-.3084-.7889-.72-1.4568-1.3876-2.1228C21.2982 1.33 20.628.9208 19.8378.6165 19.074.321 18.2017.1197 16.9244.0645 15.6471.0093 15.236-.005 11.977.0014 8.718.0076 8.31.0215 7.0301.0839m.1402 21.6932c-1.17-.0509-1.8053-.2453-2.2287-.408-.5606-.216-.96-.4771-1.3819-.895-.422-.4178-.6811-.8186-.9-1.378-.1644-.4234-.3624-1.058-.4171-2.228-.0595-1.2645-.072-1.6442-.079-4.848-.007-3.2037.0053-3.583.0607-4.848.05-1.169.2456-1.805.408-2.2282.216-.5613.4762-.96.895-1.3816.4188-.4217.8184-.6814 1.3783-.9003.423-.1651 1.0575-.3614 2.227-.4171 1.2655-.06 1.6447-.072 4.848-.079 3.2033-.007 3.5835.005 4.8495.0608 1.169.0508 1.8053.2445 2.228.408.5608.216.96.4754 1.3816.895.4217.4194.6816.8176.9005 1.3787.1653.4217.3617 1.056.4169 2.2263.0602 1.2655.0739 1.645.0796 4.848.0058 3.203-.0055 3.5834-.061 4.848-.051 1.17-.245 1.8055-.408 2.2294-.216.5604-.4763.96-.8954 1.3814-.419.4215-.8181.6811-1.3783.9-.4224.1649-1.0577.3617-2.2262.4174-1.2656.0595-1.6448.072-4.8493.079-3.2045.007-3.5825-.006-4.848-.0608M16.953 5.5864A1.44 1.44 0 1 0 18.39 4.144a1.44 1.44 0 0 0-1.437 1.4424M5.8385 12.012c.0067 3.4032 2.7706 6.1557 6.173 6.1493 3.4026-.0065 6.157-2.7701 6.1506-6.1733-.0065-3.4032-2.771-6.1565-6.174-6.1498-3.403.0067-6.156 2.771-6.1496 6.1738M8 12.0077a4 4 0 1 1 4.008 3.9921A3.9996 3.9996 0 0 1 8 12.0077"/></svg>'
    mail = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="3" fill="none" stroke="currentColor" stroke-width="2"/><path d="M4 7l8 6 8-6" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>'
    truck = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 7h12v9H2zM14 10h4l4 3v3h-8z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><circle cx="6.5" cy="17.5" r="2" fill="currentColor"/><circle cx="17.5" cy="17.5" r="2" fill="currentColor"/></svg>'
    return f"""  <footer class="site-footer">
    <div class="wrap wide">
      <div class="foot-top">
        <div class="foot-brand">
          <img src="/img/logo-sgf.png" width="1400" height="495" alt="Sans Gluten Festival" loading="lazy">
          <p>Le rendez-vous sans gluten de votre ville. Food trucks, bar, et tout le monde à la même table.</p>
        </div>
        <nav class="foot-col" aria-label="Les villes">
          <h2>La tournée</h2>
          <ul class="foot-cities">{cities}</ul>
        </nav>
        <div class="foot-col">
          <h2>Nous suivre</h2>
          <ul class="foot-links">
            <li><a href="{INSTAGRAM}" rel="noopener" target="_blank">{insta}@sansglutenfestival</a></li>
            <li><a href="mailto:{EMAIL}">{mail}{EMAIL}</a></li>
            <li><a href="mailto:{EMAIL}?subject=Devenir%20exposant%20%E2%80%94%20Sans%20Gluten%20Festival">{truck}Devenir exposant</a></li>
          </ul>
        </div>
      </div>
      <div class="foot-bottom">
        <p>© {date.today().year} Sans Gluten Festival · Votre email sert uniquement à vous prévenir de la date dans votre ville.</p>
        <div class="foot-grains" aria-hidden="true">{grains}</div>
      </div>
    </div>
  </footer>
  <script src="/assets/site.js" defer></script>
</body>
</html>
"""


ORG = {
    "@type": "Organization", "@id": SITE + "/#org", "name": "Sans Gluten Festival", "url": SITE + "/",
    "logo": SITE + "/img/logo-sgf.png", "email": EMAIL, "sameAs": [INSTAGRAM],
    "description": "Des petits rendez-vous sans gluten dans les grandes villes : food trucks, bar et ambiance conviviale.",
}


def home():
    title = "Sans Gluten Festival · Le rendez-vous sans gluten de votre ville"
    desc = ("Food trucks, bar, ambiance conviviale : des petits rendez-vous sans gluten à Paris, Lyon, "
            "Montpellier, Marseille, Toulouse… Inscrivez-vous pour votre ville.")
    ld = {"@context": "https://schema.org", "@graph": [ORG, {
        "@type": "WebSite", "@id": SITE + "/#site", "url": SITE + "/", "name": "Sans Gluten Festival",
        "inLanguage": "fr-FR", "publisher": {"@id": SITE + "/#org"}}]}
    bands = ""
    for slug, name, region, bg, ink, _ in CITIES:
        bands += f"""      <div class="city v-{slug}">
        <div class="wrap">
          <h2 class="city-name"><a href="/{slug}/">{name}<span class="city-region">{region} · <span class="city-more">Voir la page</span></span></a></h2>
          <span class="pill">À venir</span>
          {form(slug, name)}
          {share(slug, name)}
        </div>
      </div>
"""
    bands += """      <div class="city v-propose">
        <div class="wrap">
          <h2 class="city-name">Votre ville\u00a0?<span class="city-region">Elle n’est pas dans la liste\u00a0? Proposez-la, on regarde où aller ensuite.</span></h2>
          <span class="pill">À proposer</span>
          <form class="notify propose">
            <label class="sr" for="propose-ville">Votre ville</label>
            <input type="text" id="propose-ville" name="ville" placeholder="Votre ville" autocomplete="address-level2" required>
            <label class="sr" for="propose-email">Votre email</label>
            <input type="email" id="propose-email" name="email" placeholder="Votre email" autocomplete="email" required>
            <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
            <button type="submit">OK</button>
          </form>
        </div>
      </div>
"""
    sans = "".join(f'<li><b>{grain(GRAINS[i * 3])}{t}</b><span>{fr(d)}</span></li>' for i, (t, d) in enumerate(SANS))
    body = head(title, desc, "/", ld) + ticker() + header(True) + f"""  <main>
    <section class="cities" aria-label="Les villes du Sans Gluten Festival">
{bands}    </section>
    <section class="wrap about" aria-labelledby="concept">
      <h2 id="concept">Ni salon, ni gros festival</h2>
      <p class="lede">Le Sans Gluten Festival, ce sont des petits rendez-vous sans gluten dans les grandes villes de France et à Genève. Quelques food trucks, un bar, des tables\u00a0: tout ce qui est servi est sans gluten. On vient en famille ou entre amis, cœliaque ou pas, pour manger une pizza, un burger ou un croissant sans poser de questions.</p>
      <ul class="sans">{sans}</ul>
    </section>
  </main>
""" + footer()
    return body


def city_page(c):
    slug, name, region, bg, ink, text = c
    title = f"Sans Gluten Festival {name} · Le rendez-vous sans gluten"
    desc = (f"Le Sans Gluten Festival arrive à {name} : food trucks, bar et ambiance conviviale, "
            f"tout sans gluten. Inscrivez-vous pour connaître la date en premier.")
    path = f"/{slug}/"
    ld = {"@context": "https://schema.org", "@graph": [ORG, {
        "@type": "WebPage", "@id": SITE + path, "url": SITE + path, "name": title, "inLanguage": "fr-FR",
        "about": {"@type": "City", "name": name}, "isPartOf": {"@id": SITE + "/#site"},
        "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": name, "item": SITE + path}]}}]}
    others = "".join(f'<li><a href="/{o[0]}/">{city_grain(o[0])}{o[1]}</a></li>' for o in CITIES if o[0] != slug)
    sans = "".join(f'<li><b>{grain(GRAINS[i * 3])}{t}</b><span>{fr(d)}</span></li>' for i, (t, d) in enumerate(SANS))
    body = head(title, desc, path, ld, og=f"/img/og/{slug}.png", og_alt=f"Sans Gluten Festival {name}") + ticker() + header(False) + f"""  <main>
    <section class="hero-city v-{slug}">
      <div class="wrap">
        <p class="crumb"><a href="/">Accueil</a> › {name}</p>
        <h1><small>Sans Gluten Festival</small><span class="name">{name}</span></h1>
        <p class="intro">{fr(text)}</p>
        <span class="pill">À venir · {region}</span>
        <div class="signup">
          <p>Soyez prévenu de la date en premier\u00a0:</p>
          {form(slug, name, "-page")}
          {share(slug, name)}
        </div>
      </div>
    </section>
    <section class="wrap expect" aria-labelledby="attendre">
      <h2 id="attendre">Ce qui vous attend à {name}</h2>
      <p class="lede" style="margin-top:14px;max-width:62ch">Quelques food trucks, un bar, des tables et une ambiance conviviale. Petit, familial, et tout ce qui est servi est sans gluten.</p>
      <ul class="sans">{sans}</ul>
    </section>
    <section class="wrap others" aria-labelledby="autres">
      <h2 id="autres">Les autres villes de la tournée</h2>
      <ul class="chips">{others}</ul>
    </section>
  </main>
""" + footer()
    return body


def page_404():
    ld = {"@context": "https://schema.org", "@graph": [ORG]}
    chips = "".join(f'<li><a href="/{o[0]}/">{city_grain(o[0])}{o[1]}</a></li>' for o in CITIES)
    return head("Page introuvable · Sans Gluten Festival", "Cette page n’existe pas. Retrouvez les villes du Sans Gluten Festival.", "/404.html", ld).replace(
        '<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">') + ticker() + header(False) + f"""  <main>
    <section class="wrap about">
      <h1 style="font-family:var(--display);font-weight:400;font-size:clamp(44px,9vw,90px);line-height:.95;margin:0 0 14px;text-transform:uppercase">Cette page s’est fait la malle</h1>
      <p class="lede">Elle n’existe pas, ou plus. Pas de panique\u00a0: les villes de la tournée sont juste là.</p>
      <ul class="chips">{chips}</ul>
    </section>
  </main>
""" + footer()


def sitemap():
    urls = ["/"] + [f"/{c[0]}/" for c in CITIES]
    items = "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}</urlset>\n'


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    write("index.html", home())
    for c in CITIES:
        write(f"{c[0]}/index.html", city_page(c))
    write("404.html", page_404())
    write("sitemap.xml", sitemap())
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    print("ok :", 1 + len(CITIES), "pages + 404 + sitemap + robots")
