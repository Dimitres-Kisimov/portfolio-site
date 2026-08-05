#!/usr/bin/env python3
"""Static-site generator for the portfolio.

Reads ``data/projects.json`` (the single source of truth) and renders
``index.html`` from a template string. Dependency-free (Python standard
library only). Re-running regenerates the site.

The rendered page references only local assets (``styles.css`` and
``app.js``) and embeds the project data as inline JSON so the client-side
filtering and the hand-built chart work fully offline (open index.html
directly, no server, no network).

Bilingual (English + German) on the SAME URL: every visible string is
rendered in both languages via paired ``data-en`` / ``data-de`` attributes,
with the English text as the canonical default content. A small client-side
toggle (see ``app.js``) swaps the active language in place - no reload, no
URL change - and flips ``<html lang>`` accordingly. German copy lives
alongside the English in ``data/projects.json`` (``*_de`` fields) and in the
UI-string map below.
"""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path

# Windows console safety: never crash on a non-ASCII character.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # pragma: no cover - reconfigure missing on exotic stdouts
    pass

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "projects.json"
OUT = ROOT / "index.html"

# Ordered role -> human label for the filter chips (English + German).
ROLE_LABELS = {
    "flagship": "Flagship",
    "Job#2 analytics": "Analytics (Job #2)",
    "Job#1 automation": "Automation (Job #1)",
    "applied-ml": "Applied ML & Ops",
    "research": "Research",
    "teaching": "Teaching",
}

ROLE_LABELS_DE = {
    "flagship": "Vorzeigeprojekt",
    "Job#2 analytics": "Analytik (Job #2)",
    "Job#1 automation": "Automatisierung (Job #1)",
    "applied-ml": "Angewandtes ML & Betrieb",
    "research": "Forschung",
    "teaching": "Lehre",
}

# --- UI-string translation map (chrome that lives in the template, not JSON) --
# Each value is an (English, German) pair. German is faithful, professional
# copy; disclaimers are preserved in German (see the impact + footer notes).
UI = {
    "title": (
        "Dimitres Kisimov - Data & AI Portfolio",
        "Dimitres Kisimov – Daten- & KI-Portfolio",
    ),
    "skip": ("Skip to projects", "Zu den Projekten springen"),
    "eyebrow": (
        "Data & AI · Automation + Analytics",
        "Daten & KI · Automatisierung + Analytik",
    ),
    "lede": (
        "I build the seam between prediction and decision: agentic & low-code "
        "automation on one side, BI / forecasting / optimization on the other - "
        "each project shipped with a fair baseline, an honest evaluation, and a "
        "working offline artifact.",
        "Ich baue die Naht zwischen Vorhersage und Entscheidung: agentische & "
        "Low-Code-Automatisierung auf der einen Seite, BI / Prognose / "
        "Optimierung auf der anderen – jedes Projekt ausgeliefert mit einer "
        "fairen Baseline, einer ehrlichen Evaluierung und einem funktionierenden "
        "Offline-Artefakt.",
    ),
    "nav_featured": ("Featured work", "Ausgewählte Arbeiten"),
    "nav_github": ("GitHub profile", "GitHub-Profil"),
    "nav_impact": ("Impact chart", "Wirkungsdiagramm"),
    "nav_approach": ("Approach", "Vorgehen"),
    "featured_h": ("Featured work", "Ausgewählte Arbeiten"),
    "projects_h": ("Projects", "Projekte"),
    "impact_h": ("Impact at a glance", "Wirkung auf einen Blick"),
    "impact_pre": (
        "Headline annual euro figure per project that reports one - "
        "modelled/estimated on ",
        "Jährliche Euro-Kennzahl pro Projekt, sofern eines eine meldet – "
        "modelliert/geschätzt auf ",
    ),
    "impact_strong": ("synthetic data", "synthetischen Daten"),
    "impact_post": (
        ", drawn to scale (note the wide range). A bar is a claim about method on "
        "generated data, not a guaranteed business outcome.",
        ", maßstabsgetreu gezeichnet (beachten Sie die große Spanne). Ein "
        "Balken ist eine Aussage über die Methode auf generierten Daten, kein "
        "garantiertes Geschäftsergebnis.",
    ),
    "impact_figcaption": (
        "Values are annual euro impact (uplift, net saving, freed capacity, or an "
        "identified leakage lever). All synthetic/estimated. Source: each "
        "project's README.",
        "Werte sind jährliche Euro-Wirkung (Uplift, Nettoeinsparung, "
        "freigesetzte Kapazität oder ein identifizierter Leckage-Hebel). Alles "
        "synthetisch/geschätzt. Quelle: die README jedes Projekts.",
    ),
    "approach_h": ("Approach & honesty", "Vorgehen & Ehrlichkeit"),
    "repo_link": ("View repository on GitHub", "Repository auf GitHub ansehen"),
    "live_link": ("Open the live app", "Live-App öffnen"),
    "foot_datanote_label": ("Data note:", "Datenhinweis:"),
    "foot_affiliation": (
        "Any mention of Wuerth or Schwarz/Lidl/Kaufland is independent analysis "
        "of public information only - not affiliated with, endorsed by, or using "
        "internal data from those companies.",
        "Jede Erwähnung von Würth oder Schwarz/Lidl/Kaufland ist "
        "ausschließlich unabhängige Analyse öffentlicher Informationen – "
        "nicht verbunden mit, nicht unterstützt von und ohne Nutzung interner "
        "Daten dieser Unternehmen.",
    ),
    "foot_builtby": (
        "Built by Dimitres Kisimov, 2026 · © Dimitres Kisimov, all rights "
        "reserved · original hand-written HTML/CSS/JS, system fonts, no CDN, no "
        "tracking · ",
        "Erstellt von Dimitres Kisimov, 2026 · © Dimitres Kisimov, alle "
        "Rechte vorbehalten · originales, handgeschriebenes HTML/CSS/JS, "
        "Systemschriften, kein CDN, kein Tracking · ",
    ),
}

# The four "Approach & honesty" cards: (h3_en, h3_de, p_en, p_de).
APPROACH_CARDS = [
    (
        "Baseline next to every claim",
        "Baseline neben jeder Behauptung",
        "Optimizers ship beside a fair heuristic (greedy, Clarke-Wright, "
        "nearest-neighbour, seasonal-naive) so any lift is quantified, and I say "
        "plainly when the gap is small.",
        "Optimierer werden neben einer fairen Heuristik ausgeliefert (Greedy, "
        "Clarke-Wright, Nearest-Neighbour, Seasonal-Naive), sodass jeder Zugewinn "
        "quantifiziert ist, und ich sage klar, wenn der Abstand klein ist.",
    ),
    (
        "Metrics that survive reality",
        "Metriken, die der Realität standhalten",
        "MASE, macro-F1, PR-AUC and rolling-origin CV instead of accuracy or a "
        "hero number - scores chosen because they hold up under class imbalance, "
        "short series and zeros.",
        "MASE, Macro-F1, PR-AUC und Rolling-Origin-CV statt Accuracy oder einer "
        "Heldenzahl – Kennzahlen, die gewählt wurden, weil sie unter "
        "Klassenungleichgewicht, kurzen Reihen und Nullen bestehen.",
    ),
    (
        "Offline, dependency-light",
        "Offline, abhängigkeitsarm",
        "Cores written from scratch, stdlib where possible, hand-drawn SVG/Canvas "
        "charts. Web artifacts open straight off disk with no server, CDN or API "
        "key.",
        "Kerne von Grund auf geschrieben, wo möglich Standardbibliothek, "
        "handgezeichnete SVG-/Canvas-Diagramme. Web-Artefakte öffnen direkt von "
        "der Festplatte – ohne Server, CDN oder API-Schlüssel.",
    ),
    (
        "Synthetic data, stated once and everywhere",
        "Synthetische Daten, einmal und überall genannt",
        "All figures are measured on synthetic, self-generated data. They "
        "demonstrate method, not results on any real company's business.",
        "Alle Zahlen werden auf synthetischen, selbst generierten Daten gemessen. "
        "Sie demonstrieren die Methode, nicht Ergebnisse aus dem Geschäft eines "
        "realen Unternehmens.",
    ),
]


def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


def bi(en: str, de: str, tag: str = "span", cls: str | None = None, extra: str = "") -> str:
    """Render one element carrying paired EN/DE text.

    The visible/default content is the English string (so the page reads
    correctly with JS disabled and the existing English-only tests still pass);
    ``data-en`` / ``data-de`` hold both, and the client toggle swaps the active
    one in place via ``textContent``. Used only for text-only elements (no child
    markup), so a textContent swap is lossless.
    """
    attrs = ""
    if cls:
        attrs += f' class="{cls}"'
    if extra:
        attrs += f" {extra}"
    return f'<{tag}{attrs} data-en="{esc(en)}" data-de="{esc(de)}">{esc(en)}</{tag}>'


# Small external-link glyph reused by every repo/live anchor.
ARROW_ICON = (
    '\n            <svg class="icon" viewBox="0 0 16 16" width="14" height="14" aria-hidden="true">'
    '\n              <path d="M4.5 3.5h6a1 1 0 0 1 1 1v6" fill="none" stroke="currentColor"'
    ' stroke-width="1.4" stroke-linecap="round"/>'
    '\n              <path d="M11 5 4.5 11.5" fill="none" stroke="currentColor"'
    ' stroke-width="1.4" stroke-linecap="round"/>'
    "\n            </svg>"
)


def render_chip(text: str) -> str:
    # Tech/stack names are proper nouns - not translated.
    return f'<span class="chip">{esc(text)}</span>'


def render_metric(metric: dict) -> str:
    # The VALUE (numbers, proper nouns) is language-neutral; only the label is
    # translated.
    label_de = metric.get("label_de") or metric["label"]
    return (
        '<div class="metric">'
        f'<span class="metric-value">{esc(metric["value"])}</span>'
        f'{bi(metric["label"], label_de, "span", cls="metric-label")}'
        "</div>"
    )


def render_media(project: dict) -> str:
    """Optional screenshot preview for projects that ship one.

    The image is a local, relative asset (no external host) so the offline
    guarantee holds; alt text is required and rendered escaped.
    """
    image = project.get("image")
    if not image:
        return ""
    alt = esc(project.get("image_alt", ""))
    return (
        f'\n          <img class="card-media" src="{esc(image)}" alt="{alt}"'
        ' loading="lazy">'
    )


def render_live_link(project: dict) -> str:
    """Optional second anchor for projects that ship a live, hosted app."""
    live_url = project.get("live_url")
    if not live_url:
        return ""
    link_text = bi(UI["live_link"][0], UI["live_link"][1], "span")
    return f"""
          <a class="repo-link" href="{esc(live_url)}" rel="noopener">{link_text}
            <svg class="icon" viewBox="0 0 16 16" width="14" height="14" aria-hidden="true">
              <path d="M4.5 3.5h6a1 1 0 0 1 1 1v6" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
              <path d="M11 5 4.5 11.5" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
            </svg>
          </a>"""


def chain_diagram_svg() -> str:
    """Hand-built, theme-aware inline SVG for the decision-chain feature card.

    decision-chain ships no screenshot (it is a clickable Flask dashboard), so
    its visual is a small stage-pipeline diagram drawn from CSS design tokens -
    fully local, no external asset, honest (no invented numbers beyond the
    13/13 reconciliation identity count the repo actually machine-checks).
    """
    stages = ["Clean", "Forecast", "Inventory", "Slotting", "Fulfilment", "Routing"]
    final_label = "Reconciled ledger"
    final_sub = "13/13 identities PASS"
    box_x, box_w, box_h, step, top = 30, 240, 32, 46, 8
    cx = box_x + box_w / 2  # horizontal centre (150)
    n = len(stages)
    parts = [
        # No xmlns: this SVG is inlined in an HTML5 document, so the HTML parser
        # assigns the SVG namespace. Emitting the xmlns URL would also trip the
        # site's own external-URL guard for no benefit.
        '<svg class="chain-svg" viewBox="0 0 300 340" role="img"'
        ' aria-labelledby="chain-title">',
        '<title id="chain-title">decision-chain: one real dataset flows through six stages'
        " into a single reconciled ledger where every identity check passes</title>",
    ]
    # Connectors + arrowheads (each box down into the next, ending in the ledger).
    for i in range(n):
        y_from = top + i * step + box_h
        y_to = top + (i + 1) * step
        parts.append(
            f'<line class="chain-arrow" x1="{cx:g}" y1="{y_from}" x2="{cx:g}"'
            f' y2="{y_to}" stroke-width="2"/>'
        )
        parts.append(
            f'<path class="chain-arrow-head" d="M{cx - 4:g} {y_to - 6} L{cx + 4:g}'
            f' {y_to - 6} L{cx:g} {y_to} Z"/>'
        )
    # Regular stage boxes.
    for i, label in enumerate(stages):
        y = top + i * step
        parts.append(
            f'<rect class="chain-box" x="{box_x}" y="{y}" width="{box_w}"'
            f' height="{box_h}" rx="8"/>'
        )
        parts.append(
            f'<text class="chain-text" x="{cx:g}" y="{y + box_h / 2 + 4:g}"'
            f' text-anchor="middle" font-size="13">{esc(label)}</text>'
        )
    # Final, highlighted ledger box (taller, two lines).
    fy = top + n * step
    parts.append(
        f'<rect class="chain-box-final" x="{box_x}" y="{fy}" width="{box_w}"'
        ' height="44" rx="8"/>'
    )
    parts.append(
        f'<text class="chain-text-final" x="{cx:g}" y="{fy + 19:g}" text-anchor="middle"'
        f' font-size="13" font-weight="700">{esc(final_label)}</text>'
    )
    parts.append(
        f'<text class="chain-sub-final" x="{cx:g}" y="{fy + 35:g}" text-anchor="middle"'
        f' font-size="11">{esc(final_sub)}</text>'
    )
    parts.append("</svg>")
    return "".join(parts)


def render_featured_media(item: dict) -> str:
    """Visual for a featured card: a local screenshot, or the inline diagram.

    Screenshots are local, relative assets (offline guarantee); the only card
    without one (decision-chain) gets the hand-built inline SVG pipeline.
    """
    image = item.get("image")
    if image:
        alt = esc(item.get("image_alt", ""))
        return f'<img class="feature-media" src="{esc(image)}" alt="{alt}" loading="lazy">'
    if item.get("diagram") == "chain":
        return f'<div class="feature-diagram">{chain_diagram_svg()}</div>'
    return ""


def render_featured_links(item: dict) -> str:
    repo = esc(item["repo_url"])
    repo_text = bi(UI["repo_link"][0], UI["repo_link"][1], "span")
    links = [
        f'<a class="repo-link" href="{repo}" rel="noopener">{repo_text}{ARROW_ICON}</a>'
    ]
    live_url = item.get("live_url")
    if live_url:
        live_text = bi(UI["live_link"][0], UI["live_link"][1], "span")
        links.append(
            f'<a class="repo-link" href="{esc(live_url)}" rel="noopener">'
            f"{live_text}{ARROW_ICON}</a>"
        )
    return "\n          ".join(links)


def render_feature(item: dict) -> str:
    media = render_featured_media(item)
    links = render_featured_links(item)
    role_tag_de = item.get("role_tag_de") or item["role_tag"]
    blurb_de = item.get("blurb_de") or item["blurb"]
    role_tag = bi(item["role_tag"], role_tag_de, "span")
    blurb = bi(item["blurb"], blurb_de, "p", cls="feature-blurb")
    return f"""
        <article class="feature" data-slug="{esc(item['slug'])}">
          <div class="feature-visual">{media}</div>
          <div class="feature-body">
            <p class="feature-eyebrow"><span class="feature-step">{esc(item['arc_step'])}</span>{role_tag}</p>
            <h3>{esc(item['name'])}</h3>
            {blurb}
            <div class="feature-links">
          {links}
            </div>
          </div>
        </article>"""


def render_card(project: dict) -> str:
    role = project["role"]
    role_label = ROLE_LABELS.get(role, role)
    role_label_de = ROLE_LABELS_DE.get(role, role_label)
    chips = "".join(render_chip(s) for s in project["stack"])
    metrics = "".join(render_metric(m) for m in project["metrics"][:4])
    h_en = project["highlights"]
    h_de = project.get("highlights_de") or []
    highlights = "".join(
        bi(h, h_de[i] if i < len(h_de) else h, "li") for i, h in enumerate(h_en)
    )
    repo = esc(project["repo_url"])
    media = render_media(project)
    live_link = render_live_link(project)
    category = project["category"]
    category_de = project.get("category_de") or category
    tagline = project["tagline"]
    tagline_de = project.get("tagline_de") or tagline
    badge = bi(role_label, role_label_de, "span", cls="badge")
    category_el = bi(category, category_de, "p", cls="category")
    tagline_el = bi(tagline, tagline_de, "p", cls="tagline")
    repo_text = bi(UI["repo_link"][0], UI["repo_link"][1], "span")
    return f"""
        <article class="card" data-role="{esc(role)}" data-category="{esc(category)}">
          <header class="card-head">
            <h3>{esc(project['name'])}</h3>
            {badge}
          </header>
          {category_el}
          {tagline_el}{media}
          <div class="metrics">{metrics}</div>
          <ul class="highlights">{highlights}</ul>
          <div class="chips">{chips}</div>
          <a class="repo-link" href="{repo}" rel="noopener">{repo_text}
            <svg class="icon" viewBox="0 0 16 16" width="14" height="14" aria-hidden="true">
              <path d="M4.5 3.5h6a1 1 0 0 1 1 1v6" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
              <path d="M11 5 4.5 11.5" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
            </svg>
          </a>{live_link}
        </article>"""


def render_filters(roles: list[str]) -> str:
    buttons = [
        '<button class="filter is-active" data-filter="all" type="button"'
        ' data-en="All" data-de="Alle">All</button>'
    ]
    for role in roles:
        label = ROLE_LABELS.get(role, role)
        label_de = ROLE_LABELS_DE.get(role, label)
        buttons.append(
            f'<button class="filter" data-filter="{esc(role)}" type="button"'
            f' data-en="{esc(label)}" data-de="{esc(label_de)}">{esc(label)}</button>'
        )
    return "".join(buttons)


def render_approach_cards() -> str:
    cards = []
    for h3_en, h3_de, p_en, p_de in APPROACH_CARDS:
        cards.append(
            '<div class="approach-card">'
            f'{bi(h3_en, h3_de, "h3")}'
            f'{bi(p_en, p_de, "p")}'
            "</div>"
        )
    return "\n        ".join(cards)


LANG_TOGGLE = """<div class="lang-toggle" role="group" aria-label="Language / Sprache">
        <button class="lang-btn is-active" data-lang="en" type="button" aria-pressed="true">EN</button>
        <button class="lang-btn" data-lang="de" type="button" aria-pressed="false">DE</button>
      </div>"""


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  {title}
  <meta name="description" content="Data &amp; AI portfolio: automation, agents, analytics/BI and applied ML. Hand-built, offline-capable, generated from projects.json.">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  {skip}
  <header class="hero">
    <div class="wrap">
      <div class="lang-bar">
        {lang_toggle}
      </div>
      {eyebrow}
      <h1>Dimitres Kisimov</h1>
      {lede}
      <nav class="hero-links">
        {nav_featured}
        {nav_github}
        {nav_browse}
        {nav_impact}
        {nav_approach}
      </nav>
    </div>
  </header>

  <main class="wrap">
    <section id="featured" aria-labelledby="featured-h">
      <div class="section-head">
        {featured_h}
        {featured_note}
      </div>
      <div class="featured-stack">
        {featured}
      </div>
    </section>

    <section id="projects" aria-labelledby="projects-h">
      <div class="section-head">
        {projects_h}
        {projects_note}
      </div>
      <div class="filters" role="group" aria-label="Filter projects by focus area">
        {filters}
      </div>
      <div class="grid" id="grid">
        {cards}
      </div>
    </section>

    <section id="impact" aria-labelledby="impact-h">
      <div class="section-head">
        {impact_h}
        <p class="muted">{impact_note}</p>
      </div>
      <figure class="chart-wrap">
        <div id="chart" class="chart" role="img" aria-label="Bar chart of modelled annual euro impact per project"></div>
        {impact_figcaption}
      </figure>
    </section>

    <section id="approach" aria-labelledby="approach-h">
      <div class="section-head">
        {approach_h}
      </div>
      <div class="approach-grid">
        {approach_cards}
      </div>
    </section>
  </main>

  <footer class="site-foot">
    <div class="wrap">
      <p class="note">{foot_datanote_label} {foot_generated_note}</p>
      {foot_affiliation}
      <p class="muted">{foot_builtby}<a href="https://github.com/Dimitres-Kisimov" rel="noopener">github.com/Dimitres-Kisimov</a></p>
    </div>
  </footer>

  <script id="projects-data" type="application/json">{data_json}</script>
  <script src="app.js"></script>
</body>
</html>
"""


def build() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    projects = data["projects"]
    count = len(projects)

    roles = [r for r in ROLE_LABELS if any(p["role"] == r for p in projects)]

    cards = "\n".join(render_card(p) for p in projects)
    filters = render_filters(roles)
    featured = "\n".join(render_feature(f) for f in data.get("featured", []))

    # Only expose what the client needs (name + impact) to the chart script.
    chart_data = [
        {"name": p["name"], "impact_eur": p.get("impact_eur"), "role": p["role"]}
        for p in projects
    ]
    # Escape every "<" to its JSON unicode-escape form (backslash-u003c) so a
    # value can never close the inline script block; JSON.parse restores "<",
    # so the client sees identical data.
    data_json = json.dumps(chart_data, ensure_ascii=True).replace("<", "\\u003c")

    featured_note = bi(
        data.get("featured_note", ""), data.get("featured_note_de", ""), "p", cls="muted"
    )
    generated_note = bi(
        data.get("generated_note", ""), data.get("generated_note_de", ""), "span"
    )
    impact_note = (
        bi(UI["impact_pre"][0], UI["impact_pre"][1], "span")
        + bi(UI["impact_strong"][0], UI["impact_strong"][1], "strong")
        + bi(UI["impact_post"][0], UI["impact_post"][1], "span")
    )

    page = TEMPLATE.format(
        title=bi(UI["title"][0], UI["title"][1], "title"),
        skip=bi(UI["skip"][0], UI["skip"][1], "a", cls="skip", extra='href="#projects"'),
        lang_toggle=LANG_TOGGLE,
        eyebrow=bi(UI["eyebrow"][0], UI["eyebrow"][1], "p", cls="eyebrow"),
        lede=bi(UI["lede"][0], UI["lede"][1], "p", cls="lede"),
        nav_featured=bi(
            UI["nav_featured"][0], UI["nav_featured"][1], "a",
            cls="btn primary", extra='href="#featured"',
        ),
        nav_github=bi(
            UI["nav_github"][0], UI["nav_github"][1], "a",
            cls="btn", extra='href="https://github.com/Dimitres-Kisimov" rel="noopener"',
        ),
        nav_browse=bi(
            f"Browse {count} projects", f"{count} Projekte ansehen", "a",
            cls="btn", extra='href="#projects"',
        ),
        nav_impact=bi(
            UI["nav_impact"][0], UI["nav_impact"][1], "a", cls="btn", extra='href="#impact"'
        ),
        nav_approach=bi(
            UI["nav_approach"][0], UI["nav_approach"][1], "a",
            cls="btn", extra='href="#approach"',
        ),
        featured_h=bi(
            UI["featured_h"][0], UI["featured_h"][1], "h2", extra='id="featured-h"'
        ),
        featured_note=featured_note,
        featured=featured,
        projects_h=bi(
            UI["projects_h"][0], UI["projects_h"][1], "h2", extra='id="projects-h"'
        ),
        projects_note=bi(
            f"Filter by focus area. {count} projects across analytics, automation, "
            "logistics, applied ML and research.",
            f"Nach Schwerpunkt filtern. {count} Projekte aus Analytik, "
            "Automatisierung, Logistik, angewandtem ML und Forschung.",
            "p", cls="muted",
        ),
        filters=filters,
        cards=cards,
        impact_h=bi(UI["impact_h"][0], UI["impact_h"][1], "h2", extra='id="impact-h"'),
        impact_note=impact_note,
        impact_figcaption=bi(
            UI["impact_figcaption"][0], UI["impact_figcaption"][1],
            "figcaption", cls="muted",
        ),
        approach_h=bi(
            UI["approach_h"][0], UI["approach_h"][1], "h2", extra='id="approach-h"'
        ),
        approach_cards=render_approach_cards(),
        foot_datanote_label=bi(
            UI["foot_datanote_label"][0], UI["foot_datanote_label"][1], "strong"
        ),
        foot_generated_note=generated_note,
        foot_affiliation=bi(
            UI["foot_affiliation"][0], UI["foot_affiliation"][1], "p", cls="note"
        ),
        foot_builtby=bi(UI["foot_builtby"][0], UI["foot_builtby"][1], "span"),
        data_json=data_json,
    )
    OUT.write_text(page, encoding="utf-8")
    print(f"Rendered {OUT.name}: {len(projects)} projects, {len(page)} bytes.")
    return len(projects)


if __name__ == "__main__":
    build()
