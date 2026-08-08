"""Tests for the site quality gate (tools/validate_site.py).

Two halves:
- the gate must PASS on the committed site (zero findings), and
- the gate must be able to FAIL: for every check, a small hostile fixture
  proves the defect is actually detected (a gate that cannot go red guards
  nothing). Three of those fixtures reproduce the real accessibility bugs
  the gate caught when it was introduced (see the contrast regression test).
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

_spec = importlib.util.spec_from_file_location(
    "validate_site", ROOT / "tools" / "validate_site.py"
)
vs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vs)


def _page(body: str, head: str = "") -> str:
    return (
        "<!doctype html>\n"
        f'<html lang="en"><head><title data-en="t" data-de="t">t</title>{head}</head>'
        f"<body>{body}</body></html>"
    )


# --- the committed site passes the whole gate --------------------------------

def test_committed_site_has_zero_findings():
    findings = vs.validate()
    assert findings == [], "site quality gate found:\n" + "\n".join(findings)


# --- well-formedness ---------------------------------------------------------

def test_parser_accepts_wellformed_page():
    _, errors = vs.parse_html(_page("<div><p>ok</p></div>"))
    assert errors == []

def test_parser_catches_mismatched_close_tag():
    _, errors = vs.parse_html(_page("<div><span>x</div>"))
    assert any("</div>" in e for e in errors)

def test_parser_catches_unclosed_tag_at_eof():
    _, errors = vs.parse_html("<!doctype html><html><body><div>")
    assert any("unclosed" in e for e in errors)

def test_parser_catches_missing_doctype():
    _, errors = vs.parse_html("<html><body></body></html>")
    assert any("doctype" in e for e in errors)


# --- structure ---------------------------------------------------------------

def test_structure_requires_exactly_one_h1():
    root, _ = vs.parse_html(_page("<h1>a</h1><h1>b</h1>"))
    assert any("exactly one <h1>" in f for f in vs.check_structure(root))

def test_structure_catches_heading_level_skip():
    root, _ = vs.parse_html(_page("<h1>a</h1><h3>b</h3>"))
    assert any("skips" in f for f in vs.check_structure(root))

def test_structure_catches_duplicate_id():
    root, _ = vs.parse_html(_page('<div id="x"></div><div id="x"></div>'))
    assert any('duplicate id "x"' in f for f in vs.check_structure(root))

def test_structure_requires_html_lang():
    root, _ = vs.parse_html("<!doctype html><html><body><h1>a</h1></body></html>")
    assert any("lang" in f for f in vs.check_structure(root))


# --- links, assets, offline --------------------------------------------------

def test_links_catch_broken_fragment(tmp_path):
    root, _ = vs.parse_html(_page('<a href="#nope">x</a>'))
    assert any('"#nope"' in f for f in vs.check_links(root, tmp_path, set()))

def test_links_catch_missing_asset_on_disk(tmp_path):
    root, _ = vs.parse_html(_page('<img src="missing.png" alt="x">'))
    assert any("not found on disk" in f for f in vs.check_links(root, tmp_path, set()))

def test_links_catch_external_asset_src(tmp_path):
    root, _ = vs.parse_html(_page('<img src="https://cdn.example.com/x.png" alt="x">'))
    assert any("external" in f for f in vs.check_links(root, tmp_path, set()))

def test_links_catch_unresolved_aria_labelledby(tmp_path):
    root, _ = vs.parse_html(_page('<svg role="img" aria-labelledby="ghost"></svg>'))
    assert any('"ghost"' in f for f in vs.check_links(root, tmp_path, set()))

def test_links_allow_github_and_declared_live_urls(tmp_path):
    live = "https://example.github.io/app/"
    root, _ = vs.parse_html(
        _page(f'<a href="https://github.com/x/y">r</a><a href="{live}">l</a>')
    )
    assert vs.check_links(root, tmp_path, {live}) == []

def test_offline_css_catches_import_and_remote_url():
    bad = '@import "x.css"; .a { background: url(https://cdn.example.com/i.png); }'
    findings = vs.check_offline_css(bad)
    assert any("@import" in f for f in findings)
    assert any("url()" in f for f in findings)


# --- accessibility -----------------------------------------------------------

def test_a11y_catches_empty_img_alt():
    root, _ = vs.parse_html(_page('<img src="x.png" alt="">'))
    assert any("empty alt" in f for f in vs.check_accessibility(root))

def test_a11y_catches_untitled_visible_svg():
    root, _ = vs.parse_html(_page("<svg></svg>"))
    assert any("svg" in f for f in vs.check_accessibility(root))

def test_a11y_accepts_hidden_and_titled_svgs():
    body = (
        '<a class="skip" href="#m">skip</a>'
        '<svg aria-hidden="true"></svg>'
        '<svg role="img"><title>ok</title></svg>'
    )
    assert vs.check_accessibility(vs.parse_html(_page(body))[0]) == []

def test_a11y_catches_button_without_type():
    root, _ = vs.parse_html(_page("<button>x</button>"))
    assert any("button" in f for f in vs.check_accessibility(root))

def test_a11y_catches_missing_skip_link():
    root, _ = vs.parse_html(_page("<p>x</p>"))
    assert any("skip" in f for f in vs.check_accessibility(root))


# --- bilingual DOM -----------------------------------------------------------

def test_i18n_catches_missing_german_half():
    root, _ = vs.parse_html(_page('<p data-en="Hello">Hello</p>'))
    assert any("data-en/data-de" in f for f in vs.check_bilingual(root))

def test_i18n_catches_default_text_drift():
    root, _ = vs.parse_html(_page('<p data-en="Hello" data-de="Hallo">Bye</p>'))
    assert any("differs from its data-en" in f for f in vs.check_bilingual(root))

def test_i18n_catches_untranslated_visible_text():
    root, _ = vs.parse_html(_page("<p>An English-only sentence.</p>"))
    assert any("without a translation pair" in f for f in vs.check_bilingual(root))

def test_i18n_allows_proper_nouns_and_neutral_text():
    body = (
        "<h1>Dimitres Kisimov</h1><h3>project-name</h3>"
        '<span class="chip">Python</span><span class="metric-value">4.2</span>'
        '<a href="https://github.com/x">github.com/x</a>'
    )
    root, _ = vs.parse_html(_page(body))
    findings = [f for f in vs.check_bilingual(root) if "without a translation" in f]
    assert findings == []

def test_i18n_catches_monolingual_aria_label():
    root, _ = vs.parse_html(_page('<div role="img" aria-label="Chart"></div>'))
    assert any("aria-label" in f for f in vs.check_bilingual(root))

def test_i18n_catches_monolingual_img_alt():
    root, _ = vs.parse_html(_page('<img src="x.png" alt="A chart">'))
    assert any("data-alt-en/data-alt-de" in f for f in vs.check_bilingual(root))


# --- honest-claims lint ------------------------------------------------------

def test_claims_catch_english_superlative():
    findings = vs.check_honest_claims({"x": "a world-class, cutting-edge tool"})
    assert any("world-class" in f for f in findings)
    assert any("cutting-edge" in f for f in findings)

def test_claims_catch_german_superlative():
    findings = vs.check_honest_claims({"x": "eine branchenführende Lösung"})
    assert any("branchenführend" in f for f in findings)

def test_claims_pass_honest_copy():
    honest = "measured on synthetic data; a fair baseline ships beside every claim"
    assert vs.check_honest_claims({"x": honest}) == []


# --- WCAG AA contrast --------------------------------------------------------

def test_contrast_math_matches_known_values():
    assert vs.contrast_ratio("#000000", "#ffffff") == 21.0
    assert abs(vs.contrast_ratio("#777777", "#ffffff") - 4.48) < 0.01

def test_contrast_catches_the_old_pre_gate_palette():
    """Regression: the palette shipped before this gate existed failed AA on
    three real pairs (accent on bg 4.20, accent on accent-soft 3.83, and
    white-on-accent 2.58 in dark mode). The gate must catch all three."""
    old_css = (
        ":root { --bg: #f6f7f9; --surface: #ffffff; --surface-2: #eef1f5;"
        " --text: #14181f; --muted: #5a6473; --accent: #2f6bff;"
        " --accent-soft: #e5edff; --on-accent: #ffffff; --chip-bg: #eef1f5; }"
        " @media (prefers-color-scheme: dark) { :root {"
        " --bg: #0d1017; --surface: #161a22; --surface-2: #1e232d;"
        " --text: #e8ecf2; --muted: #98a2b3; --accent: #6ea0ff;"
        " --accent-soft: #1a2438; --on-accent: #ffffff; --chip-bg: #212734; } }"
    )
    findings = vs.check_contrast(old_css)
    assert any("light --accent on --bg" in f for f in findings)
    assert any("light --accent on --accent-soft" in f for f in findings)
    assert any("dark --on-accent on --accent" in f for f in findings)

def test_contrast_catches_missing_token():
    findings = vs.check_contrast(":root { --bg: #ffffff; }")
    assert any("missing" in f for f in findings)

def test_contrast_passes_current_palette():
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    assert vs.check_contrast(css) == []


# --- the gate's own honesty: it inspects the real committed artifacts --------

def test_gate_reads_the_committed_index_html():
    committed = (ROOT / "index.html").read_text(encoding="utf-8")
    root, errors = vs.parse_html(committed)
    assert errors == []
    pairs = sum(1 for el, _ in vs.elements(root) if "data-en" in el.attrs)
    assert pairs > 200, "expected hundreds of EN/DE pairs in the committed site"
