"""Tests for the static-site generator (build.py).

What is covered:
- the build runs and produces a non-empty index.html;
- the build is deterministic (two runs are byte-identical);
- every project in data/projects.json appears in the output (name + repo link);
- the offline guard: no external src=, <link href="http...">, @import or
  url(http...) asset references (anchor links to github.com / the live-app
  URLs are allowed);
- HTML escaping: hostile strings in JSON fields cannot inject raw <script>;
- projects.json schema sanity (required keys on every entry).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

import build

ROOT = Path(build.__file__).resolve().parent


@pytest.fixture(scope="module")
def site_html(tmp_path_factory: pytest.TempPathFactory) -> str:
    """Build the site once into a temp file and return the rendered HTML."""
    out = tmp_path_factory.mktemp("site") / "index.html"
    original = build.OUT
    build.OUT = out
    try:
        build.build()
    finally:
        build.OUT = original
    return out.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def projects() -> list[dict]:
    data = json.loads((ROOT / "data" / "projects.json").read_text(encoding="utf-8"))
    return data["projects"]


def test_build_runs_and_produces_nonempty_html(tmp_path, monkeypatch):
    out = tmp_path / "index.html"
    monkeypatch.setattr(build, "OUT", out)
    count = build.build()
    assert out.is_file()
    html_text = out.read_text(encoding="utf-8")
    assert len(html_text) > 1000
    assert html_text.startswith("<!doctype html>")
    assert count == len(json.loads(build.DATA.read_text(encoding="utf-8"))["projects"])


def test_build_is_deterministic(tmp_path, monkeypatch):
    """Two consecutive builds must be byte-identical (no timestamps, no randomness)."""
    out_a = tmp_path / "a.html"
    out_b = tmp_path / "b.html"
    monkeypatch.setattr(build, "OUT", out_a)
    build.build()
    monkeypatch.setattr(build, "OUT", out_b)
    build.build()
    assert out_a.read_bytes() == out_b.read_bytes()


def test_committed_index_html_is_up_to_date(site_html):
    """The committed index.html must match a fresh build of data/projects.json."""
    committed = (ROOT / "index.html").read_text(encoding="utf-8")
    assert committed == site_html, (
        "index.html is stale - run `python build.py` and commit the result"
    )


def test_every_project_name_appears(site_html, projects):
    for project in projects:
        assert build.esc(project["name"]) in site_html, f"missing project: {project['name']}"


def test_every_repo_link_appears(site_html, projects):
    for project in projects:
        needle = f'href="{build.esc(project["repo_url"])}"'
        assert needle in site_html, f"missing repo link: {project['repo_url']}"


def test_live_app_links_appear(site_html, projects):
    live = [p["live_url"] for p in projects if p.get("live_url")]
    assert live, "expected at least one project with a live_url"
    for url in live:
        assert f'href="{build.esc(url)}"' in site_html, f"missing live-app link: {url}"


# --- Offline guard -----------------------------------------------------------

def test_offline_no_external_src(site_html):
    """No <script src=http...>, <img src=http...> etc."""
    assert not re.search(r'src=["\']https?://', site_html)


def test_offline_no_external_stylesheet_or_font_link(site_html):
    assert not re.search(r'<link[^>]+href=["\']https?://', site_html)


def test_offline_no_css_import_or_remote_url(site_html):
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    for blob in (site_html, css):
        assert "@import" not in blob
        assert not re.search(r'url\(\s*["\']?https?://', blob)


def test_external_anchors_limited_to_allowlist(site_html, projects):
    """Every absolute http(s) URL in the page is a github.com repo/profile
    anchor or one of the declared live-app URLs - nothing else."""
    allowed_prefixes = ["https://github.com/"]
    allowed_exact = {p["live_url"] for p in projects if p.get("live_url")}
    for url in re.findall(r'https?://[^"\'<>\s]+', site_html):
        ok = url in allowed_exact or any(url.startswith(p) for p in allowed_prefixes)
        assert ok, f"unexpected external URL in output: {url}"


# --- Escaping ----------------------------------------------------------------

def test_hostile_json_fields_cannot_inject_script(tmp_path, monkeypatch):
    """A <script> payload placed in every user-facing JSON field must come out
    HTML-escaped, never as live markup."""
    payload = '<script>alert(1)</script>'
    hostile = {
        "generated_note": payload,
        "projects": [
            {
                "name": payload,
                "slug": "hostile",
                "tagline": payload,
                "role": payload,
                "category": payload,
                "stack": [payload],
                "metrics": [{"label": payload, "value": payload}],
                "impact_eur": None,
                "highlights": [payload],
                "repo_url": f"https://github.com/x/{payload}",
            }
        ],
    }
    data_file = tmp_path / "projects.json"
    data_file.write_text(json.dumps(hostile), encoding="utf-8")
    out = tmp_path / "index.html"
    monkeypatch.setattr(build, "DATA", data_file)
    monkeypatch.setattr(build, "OUT", out)
    build.build()
    rendered = out.read_text(encoding="utf-8")
    # The only raw <script> open/close tags allowed are the two the template
    # itself emits (inline JSON data + app.js).
    assert len(re.findall(r"<script", rendered)) == 2, "hostile input injected a <script> tag"
    assert len(re.findall(r"</script", rendered)) == 2, "hostile input injected a </script> tag"
    # Card fields come out HTML-escaped; the inline JSON uses < escaping.
    assert "&lt;script&gt;" in rendered
    assert "\\u003cscript>" in rendered


# --- Schema sanity -----------------------------------------------------------

REQUIRED_KEYS = {
    "name": str,
    "slug": str,
    "tagline": str,
    "role": str,
    "category": str,
    "stack": list,
    "metrics": list,
    "highlights": list,
    "repo_url": str,
}


def test_projects_json_schema(projects):
    assert projects, "projects.json must contain at least one project"
    for project in projects:
        for key, typ in REQUIRED_KEYS.items():
            assert key in project, f"{project.get('name', '?')}: missing key {key!r}"
            assert isinstance(project[key], typ), f"{project['name']}: {key} must be {typ.__name__}"
        assert "impact_eur" in project, f"{project['name']}: missing impact_eur (may be null)"
        assert project["repo_url"].startswith("https://github.com/")
        for metric in project["metrics"]:
            assert set(metric) == {"label", "value"}, f"{project['name']}: malformed metric"


def test_project_names_and_slugs_unique(projects):
    names = [p["name"] for p in projects]
    slugs = [p["slug"] for p in projects]
    assert len(names) == len(set(names))
    assert len(slugs) == len(set(slugs))
