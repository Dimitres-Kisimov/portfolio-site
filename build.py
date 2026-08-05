#!/usr/bin/env python3
"""Static-site generator for the portfolio.

Reads ``data/projects.json`` (the single source of truth) and renders
``index.html`` from a template string. Dependency-free (Python standard
library only). Re-running regenerates the site.

The rendered page references only local assets (``styles.css`` and
``app.js``) and embeds the project data as inline JSON so the client-side
filtering and the hand-built chart work fully offline (open index.html
directly, no server, no network).
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

# Ordered role -> human label for the filter chips.
ROLE_LABELS = {
    "flagship": "Flagship",
    "Job#2 analytics": "Analytics (Job #2)",
    "Job#1 automation": "Automation (Job #1)",
    "applied-ml": "Applied ML & Ops",
    "research": "Research",
    "teaching": "Teaching",
}


def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


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
    return f'<span class="chip">{esc(text)}</span>'


def render_metric(metric: dict) -> str:
    return (
        '<div class="metric">'
        f'<span class="metric-value">{esc(metric["value"])}</span>'
        f'<span class="metric-label">{esc(metric["label"])}</span>'
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
    return f"""
          <a class="repo-link" href="{esc(live_url)}" rel="noopener">Open the live app
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
    links = [
        f'<a class="repo-link" href="{repo}" rel="noopener">View repository on GitHub'
        f"{ARROW_ICON}</a>"
    ]
    live_url = item.get("live_url")
    if live_url:
        links.append(
            f'<a class="repo-link" href="{esc(live_url)}" rel="noopener">Open the live app'
            f"{ARROW_ICON}</a>"
        )
    return "\n          ".join(links)


def render_feature(item: dict) -> str:
    media = render_featured_media(item)
    links = render_featured_links(item)
    return f"""
        <article class="feature" data-slug="{esc(item['slug'])}">
          <div class="feature-visual">{media}</div>
          <div class="feature-body">
            <p class="feature-eyebrow"><span class="feature-step">{esc(item['arc_step'])}</span>{esc(item['role_tag'])}</p>
            <h3>{esc(item['name'])}</h3>
            <p class="feature-blurb">{esc(item['blurb'])}</p>
            <div class="feature-links">
          {links}
            </div>
          </div>
        </article>"""


def render_card(project: dict) -> str:
    role = project["role"]
    role_label = ROLE_LABELS.get(role, role)
    chips = "".join(render_chip(s) for s in project["stack"])
    metrics = "".join(render_metric(m) for m in project["metrics"][:4])
    highlights = "".join(f"<li>{esc(h)}</li>" for h in project["highlights"])
    repo = esc(project["repo_url"])
    media = render_media(project)
    live_link = render_live_link(project)
    return f"""
        <article class="card" data-role="{esc(role)}" data-category="{esc(project['category'])}">
          <header class="card-head">
            <h3>{esc(project['name'])}</h3>
            <span class="badge">{esc(role_label)}</span>
          </header>
          <p class="category">{esc(project['category'])}</p>
          <p class="tagline">{esc(project['tagline'])}</p>{media}
          <div class="metrics">{metrics}</div>
          <ul class="highlights">{highlights}</ul>
          <div class="chips">{chips}</div>
          <a class="repo-link" href="{repo}" rel="noopener">View repository on GitHub
            <svg class="icon" viewBox="0 0 16 16" width="14" height="14" aria-hidden="true">
              <path d="M4.5 3.5h6a1 1 0 0 1 1 1v6" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
              <path d="M11 5 4.5 11.5" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
            </svg>
          </a>{live_link}
        </article>"""


def render_filters(roles: list[str]) -> str:
    buttons = ['<button class="filter is-active" data-filter="all" type="button">All</button>']
    for role in roles:
        label = ROLE_LABELS.get(role, role)
        buttons.append(
            f'<button class="filter" data-filter="{esc(role)}" type="button">{esc(label)}</button>'
        )
    return "".join(buttons)


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Dimitres Kisimov - Data &amp; AI Portfolio</title>
  <meta name="description" content="Data &amp; AI portfolio: automation, agents, analytics/BI and applied ML. Hand-built, offline-capable, generated from projects.json.">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <a class="skip" href="#projects">Skip to projects</a>
  <header class="hero">
    <div class="wrap">
      <p class="eyebrow">Data &amp; AI &middot; Automation + Analytics</p>
      <h1>Dimitres Kisimov</h1>
      <p class="lede">I build the seam between prediction and decision: agentic &amp; low-code
      automation on one side, BI / forecasting / optimization on the other - each project shipped
      with a fair baseline, an honest evaluation, and a working offline artifact.</p>
      <nav class="hero-links">
        <a class="btn primary" href="#featured">Featured work</a>
        <a class="btn" href="https://github.com/Dimitres-Kisimov" rel="noopener">GitHub profile</a>
        <a class="btn" href="#projects">Browse {count} projects</a>
        <a class="btn" href="#impact">Impact chart</a>
        <a class="btn" href="#approach">Approach</a>
      </nav>
    </div>
  </header>

  <main class="wrap">
    <section id="featured" aria-labelledby="featured-h">
      <div class="section-head">
        <h2 id="featured-h">Featured work</h2>
        <p class="muted">{featured_note}</p>
      </div>
      <div class="featured-stack">
        {featured}
      </div>
    </section>

    <section id="projects" aria-labelledby="projects-h">
      <div class="section-head">
        <h2 id="projects-h">Projects</h2>
        <p class="muted">Filter by focus area. {count} projects across analytics, automation, logistics, applied ML and research.</p>
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
        <h2 id="impact-h">Impact at a glance</h2>
        <p class="muted">Headline annual euro figure per project that reports one - modelled/estimated
        on <strong>synthetic data</strong>, drawn to scale (note the wide range). A bar is a claim about
        method on generated data, not a guaranteed business outcome.</p>
      </div>
      <figure class="chart-wrap">
        <div id="chart" class="chart" role="img" aria-label="Bar chart of modelled annual euro impact per project"></div>
        <figcaption class="muted">Values are annual euro impact (uplift, net saving, freed capacity, or an
        identified leakage lever). All synthetic/estimated. Source: each project's README.</figcaption>
      </figure>
    </section>

    <section id="approach" aria-labelledby="approach-h">
      <div class="section-head">
        <h2 id="approach-h">Approach &amp; honesty</h2>
      </div>
      <div class="approach-grid">
        <div class="approach-card">
          <h3>Baseline next to every claim</h3>
          <p>Optimizers ship beside a fair heuristic (greedy, Clarke-Wright, nearest-neighbour,
          seasonal-naive) so any lift is quantified, and I say plainly when the gap is small.</p>
        </div>
        <div class="approach-card">
          <h3>Metrics that survive reality</h3>
          <p>MASE, macro-F1, PR-AUC and rolling-origin CV instead of accuracy or a hero number -
          scores chosen because they hold up under class imbalance, short series and zeros.</p>
        </div>
        <div class="approach-card">
          <h3>Offline, dependency-light</h3>
          <p>Cores written from scratch, stdlib where possible, hand-drawn SVG/Canvas charts. Web
          artifacts open straight off disk with no server, CDN or API key.</p>
        </div>
        <div class="approach-card">
          <h3>Synthetic data, stated once and everywhere</h3>
          <p>All figures are measured on synthetic, self-generated data. They demonstrate method,
          not results on any real company's business.</p>
        </div>
      </div>
    </section>
  </main>

  <footer class="site-foot">
    <div class="wrap">
      <p class="note"><strong>Data note:</strong> {generated_note}</p>
      <p class="note">Any mention of Wuerth or Schwarz/Lidl/Kaufland is independent analysis of
      public information only - not affiliated with, endorsed by, or using internal data from those
      companies.</p>
      <p class="muted">Built by Dimitres Kisimov, 2026 &middot; &copy; Dimitres Kisimov, all rights reserved &middot; original
      hand-written HTML/CSS/JS, system fonts, no CDN, no tracking &middot;
      <a href="https://github.com/Dimitres-Kisimov" rel="noopener">github.com/Dimitres-Kisimov</a></p>
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

    page = TEMPLATE.format(
        count=len(projects),
        filters=filters,
        featured=featured,
        featured_note=esc(data.get("featured_note", "")),
        cards=cards,
        generated_note=esc(data.get("generated_note", "")),
        data_json=data_json,
    )
    OUT.write_text(page, encoding="utf-8")
    print(f"Rendered {OUT.name}: {len(projects)} projects, {len(page)} bytes.")
    return len(projects)


if __name__ == "__main__":
    build()
