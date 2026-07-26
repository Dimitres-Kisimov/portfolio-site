# Business case: one portfolio page instead of twenty repositories

## The situation

The work behind this portfolio lives in 20+ separate GitHub repositories — analytics,
automation/agents, logistics, applied ML, research and one flagship BIM project. A recruiter or
hiring manager gives an unfamiliar candidate roughly three minutes. In three minutes nobody
clones repositories, reads READMEs across twenty tabs, or reconstructs which numbers matter.
Scattered work is, for review purposes, invisible work.

## The solution

A single static page — [dimitres-kisimov.github.io/portfolio-site](https://dimitres-kisimov.github.io/portfolio-site/) —
generated from one source of truth, `data/projects.json`, by a standard-library-only Python
script (`build.py`). One screen answers the three-minute questions: what was built, what it
measured, where the code is. Filter chips group the projects by focus area; every card links to
its repository; two projects link to live, hosted apps.

Design constraints, chosen deliberately:

- **Offline and copyright-free.** No CDN, no web fonts, no icon library, no framework, no
  tracking. Every icon is hand-written inline SVG; the impact chart is built from the DOM by
  hand. `index.html` opens straight off disk, and works identically on GitHub Pages.
- **One source of truth.** All names, metrics, links and highlight text come from
  `data/projects.json`. The page, the embedded chart data and the PDF one-pager in
  [`deliverables/`](../deliverables/) are all generated from it — nothing is hand-copied, so
  nothing can drift.
- **Deterministic build.** `python build.py` produces byte-identical output for identical
  input. The committed `index.html` is asserted in CI to match a fresh build.

## Evidence of quality

- **Tested.** A pytest suite (`tests/test_build.py`) checks: the build runs and is
  byte-deterministic; every project appears with its repo link; the offline guard (no external
  `src=`, `<link href="http...">`, `@import`, or `url(http...)` references; external anchors are
  limited to github.com and the declared live apps); hostile JSON values cannot inject markup
  (all fields are HTML-escaped, and `<` is escaped inside the inline JSON block); and every
  `projects.json` entry carries the required keys.
- **Guarded in CI.** The GitHub Actions workflow lints (ruff), runs the tests, regenerates the
  site, re-runs the offline/copyright-free grep guard on the artifact, and builds the PDF
  one-pager with a size check.
- **Honest numbers.** Every figure on the page is copied verbatim from each project's own
  measured results and is labelled for what it is: measured on **synthetic, self-generated
  data** (the one exception, FlyHash, uses public MNIST and is labelled). Euro figures are
  modelled estimates, not audited business outcomes, and the page says so next to the chart.
  Projects that report a small or negative lift say so on the card.

## Stakeholders

- **Recruiters and hiring managers** — the primary audience: a three-minute, filterable
  overview with direct links to the underlying code.
- **Interviewers** — a shared index during technical conversations: pick a card, open the
  repo, go deep.
- **The owner (Dimitres Kisimov)** — one place to maintain; adding a project is one JSON entry
  plus `python build.py`.

## The deliverable

- The live site: <https://dimitres-kisimov.github.io/portfolio-site/>
- This repository: the generator, the data, the tests, the CI guard, and
  [`deliverables/portfolio_onepager.pdf`](../deliverables/portfolio_onepager.pdf) — a one-page
  printable summary generated from the same `projects.json`.

No revenue, traffic or conversion claims are made for the site itself; its value is review
efficiency, and the honest-numbers policy above applies to this document too.
