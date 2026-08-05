"""Tests for the static-site generator (build.py).

What is covered:
- the build runs and produces a non-empty index.html;
- the build is deterministic (two runs are byte-identical);
- every project in data/projects.json appears in the output (name + repo link);
- the offline guard: no external src=, <link href="http...">, @import or
  url(http...) asset references (anchor links to github.com / the live-app
  URLs are allowed);
- HTML escaping: hostile strings in JSON fields cannot inject raw <script>;
- projects.json schema sanity (required keys on every entry);
- data-integrity / quality guard (anti-drift for the single source of truth):
  required fields present AND non-empty, role is one the builder maps,
  repo_url is a well-formed github.com URL, any live_url is well-formed, and
  metrics carry a non-empty value + label;
- license guard: neither the template nor the rendered/committed index.html
  makes a stale MIT-license self-claim (the site is proprietary / all rights
  reserved), and the footer keeps that notice.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse

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


@pytest.fixture(scope="module")
def featured() -> list[dict]:
    data = json.loads((ROOT / "data" / "projects.json").read_text(encoding="utf-8"))
    return data.get("featured", [])


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


def test_external_anchors_limited_to_allowlist(site_html, projects, featured):
    """Every absolute http(s) URL in the page is a github.com repo/profile
    anchor or one of the declared live-app URLs (grid or featured) - nothing else."""
    allowed_prefixes = ["https://github.com/"]
    allowed_exact = {p["live_url"] for p in projects if p.get("live_url")}
    allowed_exact |= {f["live_url"] for f in featured if f.get("live_url")}
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


# --- Data-integrity & quality guard (anti-drift for the single source of truth)

# Fields the builder relies on for every card (see render_card in build.py):
# each must be present AND non-empty. (test_projects_json_schema above checks
# presence + type; this adds the non-empty guarantee.)
REQUIRED_NONEMPTY = (
    "name",
    "role",
    "category",
    "tagline",
    "stack",
    "metrics",
    "highlights",
    "repo_url",
)


def _is_nonempty(value: object) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return len(value) > 0
    return value is not None


def test_required_fields_present_and_nonempty(projects):
    for project in projects:
        name = project.get("name", "?")
        for field in REQUIRED_NONEMPTY:
            assert field in project, f"{name}: missing required field {field!r}"
            assert _is_nonempty(project[field]), f"{name}: required field {field!r} is empty"


def test_role_is_a_known_builder_role(projects):
    """Every role must be one the builder maps to a label (build.ROLE_LABELS);
    an unknown role would silently fall back to the raw string on the card and
    would produce no filter chip."""
    for project in projects:
        role = project["role"]
        assert role in build.ROLE_LABELS, (
            f"{project['name']}: role {role!r} is not a known builder role "
            f"{sorted(build.ROLE_LABELS)}"
        )


def _is_well_formed_url(url: str, *, require_host: str | None = None) -> bool:
    if not isinstance(url, str) or any(ch.isspace() for ch in url):
        return False
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        return False
    if require_host is not None and parsed.netloc != require_host:
        return False
    return True


def test_repo_urls_are_wellformed_github(projects):
    for project in projects:
        url = project["repo_url"]
        assert _is_well_formed_url(url, require_host="github.com"), (
            f"{project['name']}: repo_url must be a well-formed https github.com URL: {url!r}"
        )
        # Must address an owner/repo path, not just the bare host.
        path = urlparse(url).path.strip("/")
        assert len(path.split("/")) >= 2, f"{project['name']}: repo_url has no owner/repo path: {url!r}"


def test_live_urls_are_wellformed(projects):
    for project in projects:
        url = project.get("live_url")
        if url is None:
            continue
        assert _is_well_formed_url(url), (
            f"{project['name']}: live_url must be a well-formed https URL: {url!r}"
        )


def test_metrics_have_nonempty_value_and_label(projects):
    for project in projects:
        assert project["metrics"], f"{project['name']}: metrics must be non-empty"
        for metric in project["metrics"]:
            assert set(metric) == {"label", "value"}, (
                f"{project['name']}: metric keys must be exactly label+value: {metric!r}"
            )
            for key in ("label", "value"):
                assert isinstance(metric[key], str) and metric[key].strip(), (
                    f"{project['name']}: metric {key!r} must be a non-empty string: {metric!r}"
                )


# --- License guard: proprietary / all rights reserved, never a stale MIT claim

# Matches an MIT-license SELF-CLAIM ("MIT License", "MIT-licensed",
# "licensed under MIT") while the \bMIT\b word-boundary keeps innocent
# substrings like "committed", "limits" or "permit" from tripping it.
MIT_LICENSE_CLAIM = re.compile(
    r"\bMIT\b[\s-]{0,3}licen[sc]e|licen[sc]ed?\s+under\s+(?:the\s+)?\bMIT\b",
    re.IGNORECASE,
)


def test_template_has_no_mit_license_claim():
    assert not MIT_LICENSE_CLAIM.search(build.TEMPLATE), (
        "build.py TEMPLATE contains a stale MIT-license claim - the site is "
        "proprietary / all rights reserved"
    )


def test_rendered_and_committed_html_have_no_mit_license_claim(site_html):
    committed = (ROOT / "index.html").read_text(encoding="utf-8")
    for label, blob in (("fresh build", site_html), ("committed index.html", committed)):
        assert not MIT_LICENSE_CLAIM.search(blob), (
            f"{label} contains a stale MIT-license claim - the footer must remain "
            "'(c) Dimitres Kisimov, all rights reserved'"
        )


def test_footer_keeps_all_rights_reserved(site_html):
    assert "all rights reserved" in site_html, (
        "the footer must keep the proprietary '(c) Dimitres Kisimov, all rights reserved' notice"
    )


# --- Featured-work guard (the four crown jewels, in the narrative arc) --------

# Spine order (see PORTFOLIO_STORY.md): showpiece -> engine -> integration proof
# -> command center. This is the exact set and order the featured section shows.
EXPECTED_FEATURED_ORDER = [
    "logistics-flow-studio",
    "logistics-digital-twin",
    "decision-chain",
    "distributor-intelligence-platform",
]
FEATURED_REQUIRED_KEYS = ("slug", "arc_step", "role_tag", "name", "blurb", "repo_url")


def _featured_segment(site_html: str) -> str:
    """The rendered HTML between the featured section start and the grid."""
    start = site_html.index('id="featured"')
    end = site_html.index('id="projects"')
    assert start < end, "the featured section must render ABOVE the projects grid"
    return site_html[start:end]


def test_featured_section_present(site_html):
    assert 'id="featured"' in site_html
    assert "Featured work" in site_html


def test_featured_is_the_four_jewels_in_arc_order(featured, site_html):
    slugs = [f["slug"] for f in featured]
    assert slugs == EXPECTED_FEATURED_ORDER, (
        f"featured must be the four crown jewels in spine order, got {slugs}"
    )
    # ...and they render in that same order in the HTML.
    rendered = re.findall(r'class="feature" data-slug="([^"]+)"', site_html)
    assert rendered == EXPECTED_FEATURED_ORDER, f"featured cards render out of order: {rendered}"


def test_featured_entries_schema(featured):
    assert len(featured) == 4, "expected exactly four featured entries"
    seen: set[str] = set()
    for item in featured:
        for key in FEATURED_REQUIRED_KEYS:
            assert key in item and str(item[key]).strip(), f"featured missing {key!r}: {item}"
        assert item["slug"] not in seen, f"duplicate featured slug: {item['slug']}"
        seen.add(item["slug"])
        # Every card must carry a LOCAL visual: a screenshot image OR the diagram.
        assert item.get("image") or item.get("diagram"), (
            f"featured entry {item['slug']} has no visual (image or diagram)"
        )


def test_featured_names_role_tags_and_arc_steps_render(featured, site_html):
    seg = _featured_segment(site_html)
    for item in featured:
        assert build.esc(item["name"]) in seg, f"featured name missing: {item['name']}"
        assert build.esc(item["role_tag"]) in seg, f"featured role tag missing: {item['role_tag']}"
        assert f'feature-step">{build.esc(item["arc_step"])}</span>' in seg, (
            f"featured arc step missing: {item['arc_step']}"
        )


def test_featured_images_are_local_relative_and_exist_on_disk(featured):
    for item in featured:
        image = item.get("image")
        if not image:
            continue
        # GitHub Pages only serves THIS repo, so the asset must be a relative,
        # in-repo path - never a scheme, protocol-relative or root-absolute URL.
        assert "://" not in image and not image.startswith(("/", "http", "data:")), (
            f"featured image must be a local relative path: {image!r}"
        )
        assert (ROOT / image).is_file(), f"featured image missing on disk: {image!r}"


def test_featured_media_has_no_external_reference(site_html):
    seg = _featured_segment(site_html)
    assert not re.search(r'src=["\']https?://', seg), "external image src in featured section"
    assert not re.search(r'src=["\']//', seg), "protocol-relative image src in featured section"


def test_featured_repo_urls_are_wellformed_github(featured):
    for item in featured:
        assert _is_well_formed_url(item["repo_url"], require_host="github.com"), (
            f"{item['slug']}: featured repo_url must be a well-formed github.com URL"
        )


def test_featured_live_urls_are_wellformed(featured):
    for item in featured:
        url = item.get("live_url")
        if url:
            assert _is_well_formed_url(url), f"{item['slug']}: featured live_url malformed"


def test_featured_section_has_no_mit_license_claim(site_html):
    assert not MIT_LICENSE_CLAIM.search(_featured_segment(site_html)), (
        "featured section must not carry a stale MIT-license self-claim"
    )
