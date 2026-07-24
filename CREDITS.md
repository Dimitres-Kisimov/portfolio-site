# Credits

All assets in this repository are **original work by Dimitres Kisimov**, created from scratch for
this site.

- **Code** — hand-written HTML template (`build.py`), CSS (`styles.css`) and JavaScript
  (`app.js`). No framework, no build tooling beyond Python's standard library.
- **Typography** — the **system font stack only**
  (`-apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`). No web fonts, no
  `@font-face`, nothing loaded from a font CDN.
- **Icons** — the only icon is an inline SVG (an "external link" arrow) written by hand in
  `build.py`. No icon library.
- **Charts** — the "impact at a glance" chart is built by hand from `<div>` bars in `app.js`
  driven by inline data. No Chart.js, D3, or any charting dependency.
- **No third-party assets** — no CDN scripts or stylesheets, no remote images, no company logos
  (no Würth or Schwarz logos or branding), no tracking, no external network requests of any kind.
  The page renders identically offline (open `index.html` directly) and on GitHub Pages.

## Data

All project figures are **synthetic and self-generated** in the source repositories they come
from (the single exception, FlyHash in `bio-efficient-ai`, uses public **MNIST**). They
demonstrate method, not results on any real company's business. The headline numbers here are
transcribed from each source repository's own README.

## Company mentions

Any reference to **Würth** or **Schwarz / Lidl / Kaufland** is **independent analysis of publicly
available information only**. This project is not affiliated with, endorsed by, or reviewed by
those companies, and uses no internal or proprietary data from them.

## Third-party sources (documentation only)

`docs/MARKET_REQUESTS.md` cites public reports and product documentation (Dresner Advisory,
Gartner, MHI, Anthropic, Microsoft, Google OR-Tools, n8n) as plain-text references for research
purposes. No third-party text, images, or trademarks are embedded in the site itself.
