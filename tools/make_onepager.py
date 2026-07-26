#!/usr/bin/env python3
"""Generate deliverables/portfolio_onepager.pdf - the portfolio at a glance.

Reads data/projects.json (the same single source of truth build.py uses) and
typesets one printable A4 page with matplotlib: every project name with its
first (headline) metric, grouped by focus area, plus the live site URL and
the honesty note. Nothing is hand-copied; edit projects.json and re-run.

Usage:  python tools/make_onepager.py
"""

from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "projects.json"
OUT = ROOT / "deliverables" / "portfolio_onepager.pdf"

SITE_URL = "https://dimitres-kisimov.github.io/portfolio-site/"

# Same group order the site uses (build.py ROLE_LABELS).
ROLE_LABELS = {
    "flagship": "Flagship",
    "Job#2 analytics": "Analytics (Job #2)",
    "Job#1 automation": "Automation (Job #1)",
    "applied-ml": "Applied ML & Ops",
    "research": "Research",
    "teaching": "Teaching",
}

# Ink tokens only - this page is a typeset list, not a chart.
INK = "#1a1a1a"
MUTED = "#555555"
FAINT = "#c8c8c8"

PAGE_W, PAGE_H = 8.27, 11.69  # A4 portrait, inches
MARGIN_X = 0.75 / PAGE_W  # 0.75 in side margins, as figure fraction


def say(text: str) -> None:
    """ASCII-only stdout, safe on any Windows console codepage."""
    print(text.encode("ascii", "replace").decode("ascii"))


def build_pdf() -> Path:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    projects = data["projects"]
    note = data.get("generated_note", "")

    fig = plt.figure(figsize=(PAGE_W, PAGE_H))
    fig.patch.set_facecolor("white")
    left, right = MARGIN_X, 1 - MARGIN_X

    def rule(y: float, color: str = FAINT, lw: float = 0.8) -> None:
        fig.add_artist(plt.Line2D([left, right], [y, y], color=color, lw=lw,
                                  transform=fig.transFigure))

    # --- Header ---------------------------------------------------------
    y = 1 - 0.75 / PAGE_H
    fig.text(left, y, "Dimitres Kisimov", fontsize=19, fontweight="bold", color=INK)
    fig.text(right, y, "Data & AI portfolio - at a glance", fontsize=10.5,
             color=MUTED, ha="right")
    y -= 0.26 / PAGE_H
    fig.text(left, y, f"Live site: {SITE_URL}", fontsize=9.5, color=MUTED)
    fig.text(right, y, f"{len(projects)} projects - one headline metric each",
             fontsize=9.5, color=MUTED, ha="right")
    y -= 0.16 / PAGE_H
    rule(y, color=INK, lw=1.2)
    y -= 0.14 / PAGE_H

    # --- Grouped project rows ------------------------------------------
    group_h = 0.34 / PAGE_H
    row_h = 0.315 / PAGE_H
    for role, label in ROLE_LABELS.items():
        group = [p for p in projects if p["role"] == role]
        if not group:
            continue
        y -= group_h
        fig.text(left, y, label.upper(), fontsize=8.5, fontweight="bold",
                 color=MUTED)
        y -= 0.10 / PAGE_H
        rule(y)
        for project in group:
            y -= row_h
            metric = project["metrics"][0]
            fig.text(left, y, project["name"], fontsize=10,
                     fontweight="bold", color=INK)
            fig.text(right, y, f"{metric['label']}:  {metric['value']}",
                     fontsize=9.5, color=INK, ha="right")

    # --- Footer ---------------------------------------------------------
    y_foot = 0.74 / PAGE_H
    rule(y_foot + 0.28 / PAGE_H, color=INK, lw=1.2)
    note_lines = textwrap.wrap(f"Honesty note: {note}", width=108)
    for line in note_lines:
        fig.text(left, y_foot, line, fontsize=8, color=MUTED)
        y_foot -= 0.15 / PAGE_H
    fig.text(left, y_foot - 0.05 / PAGE_H,
             "Generated from data/projects.json by tools/make_onepager.py - "
             "nothing on this page is hand-copied.",
             fontsize=8, color=MUTED)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, format="pdf")
    plt.close(fig)
    return OUT


def main() -> int:
    out = build_pdf()
    size = out.stat().st_size
    say(f"Wrote {out.relative_to(ROOT)} ({size} bytes).")
    if size <= 10_000:
        say("ERROR: PDF is suspiciously small (<= 10 KB).")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
