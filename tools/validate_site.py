#!/usr/bin/env python3
"""Site quality gate: validate the committed, generated site as a DOCUMENT.

The pytest suite guards the generator's inputs (schema, German source fields,
determinism). This tool inspects the rendered output the way a browser and a
screen reader consume it, and fails the build on:

1.  Well-formedness - index.html parses, tags balance, ids are unique.
2.  Structure       - exactly one <h1>, heading levels never skip.
3.  Links           - every #fragment href and aria-labelledby resolves to an
                      existing id; every relative asset (CSS, JS, images)
                      exists on disk; absolute URLs stay on the allowlist
                      (github.com + declared live apps); no external asset
                      references (offline guarantee).
4.  Accessibility   - every <img> has non-empty alt text; every inline <svg>
                      is aria-hidden or a titled role="img"; buttons carry an
                      explicit type; the skip link and <html lang> exist.
5.  Bilingual DOM   - every data-en element has a non-empty data-de twin (and
                      vice versa) and its default text IS the English string;
                      every visible text node is either bilingual or on the
                      explicit proper-noun allowlist (project names, tech
                      chips, metric values, ...); aria-labels and image alts
                      carry paired translations too.
6.  Honest claims   - no marketing superlatives, in either language, in the
                      rendered page or in data/projects.json.
7.  WCAG AA color   - every text/background token pair styles.css actually
                      uses meets a >= 4.5:1 contrast ratio in BOTH the light
                      and the dark scheme (computed, not eyeballed).

Standard library only, like everything else in this repo. Exit code 0 = all
checks pass; 1 = findings (each printed on its own line). Run directly:

    python tools/validate_site.py
"""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# HTML void elements (never pushed on the open-tag stack).
VOID = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}

# Absolute URLs allowed in anchors: the GitHub profile/repos plus any live_url
# declared in data/projects.json (added at runtime).
ALLOWED_URL_PREFIXES = ("https://github.com/",)

# aria-labels that are already language-neutral (carry both languages inline).
NEUTRAL_ARIA_LABELS = {"Language / Sprache"}

# Marketing superlatives banned in BOTH languages (honest framing, enforced).
BANNED_CLAIMS = (
    "state-of-the-art", "state of the art", "world-class", "world class",
    "best-in-class", "best in class", "industry-leading", "industry leading",
    "cutting-edge", "cutting edge", "revolutionary", "game-changing",
    "game changing", "market-leading", "market leading", "blazingly fast",
    "unrivaled", "unrivalled",
    "weltklasse", "branchenführend", "marktführend", "bahnbrechend",
    "revolutionär", "konkurrenzlos",
)

# Foreground/background CSS-token pairs the design actually uses; each must
# meet WCAG AA for normal text (>= 4.5:1) in both color schemes.
CONTRAST_PAIRS = (
    ("text", "bg"), ("text", "surface"), ("text", "surface-2"),
    ("text", "chip-bg"),
    ("muted", "bg"), ("muted", "surface"), ("muted", "surface-2"),
    ("accent", "bg"), ("accent", "surface"), ("accent", "accent-soft"),
    ("on-accent", "accent"),
)
AA_NORMAL_TEXT = 4.5


class Node:
    """One element in the parsed tree; text children are plain strings."""

    __slots__ = ("tag", "attrs", "children")

    def __init__(self, tag: str, attrs: dict[str, str]):
        self.tag = tag
        self.attrs = attrs
        self.children: list[Node | str] = []

    def text(self) -> str:
        """Concatenated text of this subtree."""
        parts = []
        for child in self.children:
            parts.append(child if isinstance(child, str) else child.text())
        return "".join(parts)


class TreeBuilder(HTMLParser):
    """Parse HTML into a Node tree, recording well-formedness violations."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = Node("#document", {})
        self.stack: list[Node] = [self.root]
        self.errors: list[str] = []
        self.saw_doctype = False

    def _append(self, tag: str, attrs: list[tuple[str, str | None]]) -> Node:
        node = Node(tag, {k: (v if v is not None else "") for k, v in attrs})
        self.stack[-1].children.append(node)
        return node

    def handle_decl(self, decl: str) -> None:
        if decl.lower().startswith("doctype"):
            self.saw_doctype = True

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        node = self._append(tag, attrs)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._append(tag, attrs)  # self-closing (SVG shapes): never pushed

    def handle_endtag(self, tag: str) -> None:
        if tag in VOID:
            return
        line, _ = self.getpos()
        if self.stack[-1].tag == tag:
            self.stack.pop()
            return
        open_tags = [n.tag for n in self.stack[1:]]
        if tag in open_tags:  # recover, but record the mismatch
            self.errors.append(
                f"line {line}: </{tag}> closes over unclosed "
                f"<{self.stack[-1].tag}>"
            )
            while self.stack[-1].tag != tag:
                self.stack.pop()
            self.stack.pop()
        else:
            self.errors.append(f"line {line}: stray </{tag}> with no open <{tag}>")

    def handle_data(self, data: str) -> None:
        if data:
            self.stack[-1].children.append(data)

    def finish(self) -> None:
        self.close()
        if not self.saw_doctype:
            self.errors.append("missing <!doctype html>")
        unclosed = [n.tag for n in self.stack[1:]]
        if unclosed:
            self.errors.append(f"unclosed tags at EOF: {', '.join(unclosed)}")


def parse_html(text: str) -> tuple[Node, list[str]]:
    builder = TreeBuilder()
    builder.feed(text)
    builder.finish()
    return builder.root, builder.errors


def walk(node: Node, ancestors: tuple[Node, ...] = ()):
    """Yield (child, ancestors-including-parent) for every node and text."""
    for child in node.children:
        yield child, ancestors + (node,)
        if isinstance(child, Node):
            yield from walk(child, ancestors + (node,))


def elements(root: Node):
    for item, ancestors in walk(root):
        if isinstance(item, Node):
            yield item, ancestors


def norm(text: str) -> str:
    return " ".join(text.split())


# --- 1 + 2: structure --------------------------------------------------------

def check_structure(root: Node) -> list[str]:
    findings = []
    ids: dict[str, int] = {}
    headings: list[str] = []
    html_el = None
    for el, _ in elements(root):
        if el.tag == "html":
            html_el = el
        el_id = el.attrs.get("id")
        if el_id:
            ids[el_id] = ids.get(el_id, 0) + 1
        if re.fullmatch(r"h[1-6]", el.tag):
            headings.append(el.tag)
    for el_id, count in ids.items():
        if count > 1:
            findings.append(f"structure: duplicate id \"{el_id}\" ({count}x)")
    if html_el is None or not html_el.attrs.get("lang"):
        findings.append("structure: <html> must carry a lang attribute")
    if headings.count("h1") != 1:
        findings.append(f"structure: expected exactly one <h1>, found {headings.count('h1')}")
    previous = 0
    for h in headings:
        level = int(h[1])
        if previous == 0 and level != 1:
            findings.append(f"structure: first heading is <{h}>, must be <h1>")
        elif level > previous + 1:
            findings.append(f"structure: heading level skips <h{previous}> -> <{h}>")
        previous = level
    return findings


# --- 3: links + assets + offline guarantee ----------------------------------

def check_links(root: Node, base_dir: Path, allowed_urls: set[str]) -> list[str]:
    findings = []
    ids = {el.attrs["id"] for el, _ in elements(root) if el.attrs.get("id")}
    for el, _ in elements(root):
        for ref_attr in ("aria-labelledby", "aria-describedby"):
            ref = el.attrs.get(ref_attr)
            if ref:
                for ref_id in ref.split():
                    if ref_id not in ids:
                        findings.append(f"links: {ref_attr}=\"{ref_id}\" resolves to no id")
        for attr in ("href", "src"):
            url = el.attrs.get(attr)
            if url is None:
                continue
            if url.startswith("#"):
                if url[1:] not in ids:
                    findings.append(f"links: {attr}=\"{url}\" resolves to no id")
            elif url.startswith(("http://", "https://", "//")):
                ok = url in allowed_urls or url.startswith(ALLOWED_URL_PREFIXES)
                if el.tag != "a" or not ok:
                    findings.append(
                        f"links: external {attr}=\"{url}\" on <{el.tag}> "
                        "(assets must be local; anchors must stay on the allowlist)"
                    )
            elif url.startswith(("data:", "mailto:", "javascript:")):
                findings.append(f"links: unexpected scheme in {attr}=\"{url}\"")
            else:  # relative asset -> must exist in the repo
                target = base_dir / url.split("#")[0].split("?")[0]
                if not target.is_file():
                    findings.append(f"links: {attr}=\"{url}\" not found on disk")
    return findings


def check_offline_css(css_text: str) -> list[str]:
    findings = []
    if "@import" in css_text:
        findings.append("offline: @import found in styles.css")
    if re.search(r"url\(\s*[\"']?https?://", css_text):
        findings.append("offline: external url() reference found in styles.css")
    if "@font-face" in css_text:
        findings.append("offline: @font-face found in styles.css (system fonts only)")
    return findings


# --- 4: accessibility --------------------------------------------------------

def check_accessibility(root: Node) -> list[str]:
    findings = []
    saw_skip_link = False
    for el, _ in elements(root):
        if el.tag == "a" and "skip" in el.attrs.get("class", "").split():
            saw_skip_link = True
        if el.tag == "img" and not el.attrs.get("alt", "").strip():
            findings.append(f"a11y: <img src=\"{el.attrs.get('src', '?')}\"> has empty alt")
        if el.tag == "button" and el.attrs.get("type") != "button":
            findings.append("a11y: <button> without explicit type=\"button\"")
        if el.tag == "svg":
            hidden = el.attrs.get("aria-hidden") == "true"
            titled = el.attrs.get("role") == "img" and any(
                isinstance(c, Node) and c.tag == "title" for c in el.children
            )
            if not hidden and not titled:
                findings.append("a11y: <svg> is neither aria-hidden nor a titled role=\"img\"")
    if not saw_skip_link:
        findings.append("a11y: skip-to-content link missing")
    return findings


# --- 5: bilingual DOM completeness ------------------------------------------

def _untranslated_ok(parent: Node, text: str) -> bool:
    """Visible text allowed to stay single-language: proper nouns + neutrals."""
    classes = parent.attrs.get("class", "").split()
    if parent.tag == "h1":  # the author's name
        return True
    if parent.tag == "h3":  # project names (approach h3s carry data-en instead)
        return True
    if "chip" in classes or "metric-value" in classes:  # tech + figures
        return True
    if "feature-step" in classes:  # arc step number
        return True
    if "lang-btn" in classes:  # the EN / DE labels themselves
        return True
    if parent.tag == "a" and norm(text).startswith("github.com/"):
        return True
    return False


def check_bilingual(root: Node) -> list[str]:
    findings = []
    pair_count = 0
    for el, _ancestors in elements(root):
        en, de = el.attrs.get("data-en"), el.attrs.get("data-de")
        if en is not None or de is not None:
            pair_count += 1
            if not (en or "").strip() or not (de or "").strip():
                findings.append(
                    f"i18n: <{el.tag}> has an empty/missing half of the "
                    f"data-en/data-de pair (en={en!r}, de={de!r})"
                )
            elif norm(el.text()) != norm(en):
                findings.append(
                    f"i18n: <{el.tag}> default text differs from its data-en "
                    f"({norm(el.text())!r} != {norm(en)!r})"
                )
        aria = el.attrs.get("aria-label")
        if aria is not None and aria not in NEUTRAL_ARIA_LABELS:
            aria_en = el.attrs.get("data-aria-en", "")
            aria_de = el.attrs.get("data-aria-de", "")
            if not aria_en.strip() or not aria_de.strip():
                findings.append(
                    f"i18n: aria-label \"{aria}\" has no data-aria-en/data-aria-de pair"
                )
            elif aria != aria_en:
                findings.append(
                    f"i18n: aria-label \"{aria}\" differs from its data-aria-en"
                )
        if el.tag == "img":
            alt_en = el.attrs.get("data-alt-en", "")
            alt_de = el.attrs.get("data-alt-de", "")
            if not alt_en.strip() or not alt_de.strip():
                findings.append(
                    f"i18n: <img src=\"{el.attrs.get('src', '?')}\"> has no "
                    "data-alt-en/data-alt-de pair"
                )
            elif el.attrs.get("alt") != alt_en:
                findings.append(
                    f"i18n: <img src=\"{el.attrs.get('src', '?')}\"> alt differs "
                    "from its data-alt-en"
                )
    if pair_count < 50:
        findings.append(f"i18n: only {pair_count} bilingual pairs found - expected many")
    # Every remaining visible text node must be covered or explicitly allowed.
    for item, ancestors in walk(root):
        if not isinstance(item, str) or not item.strip():
            continue
        tags = [a.tag for a in ancestors]
        if "script" in tags or "style" in tags:
            continue
        if any("data-en" in a.attrs for a in ancestors):
            continue
        if _untranslated_ok(ancestors[-1], item):
            continue
        findings.append(
            f"i18n: visible text without a translation pair in <{ancestors[-1].tag}>: "
            f"{norm(item)[:60]!r}"
        )
    return findings


# --- 6: honest-claims lint ---------------------------------------------------

def check_honest_claims(blobs: dict[str, str]) -> list[str]:
    findings = []
    for source, blob in blobs.items():
        low = blob.lower()
        for term in BANNED_CLAIMS:
            if term in low:
                findings.append(f"claims: banned superlative {term!r} in {source}")
    return findings


# --- 7: WCAG AA contrast -----------------------------------------------------

def _luminance(hex_color: str) -> float:
    raw = hex_color.lstrip("#")
    r, g, b = (int(raw[i : i + 2], 16) / 255 for i in (0, 2, 4))

    def channel(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast_ratio(fg: str, bg: str) -> float:
    lighter, darker = sorted((_luminance(fg), _luminance(bg)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def parse_palettes(css_text: str) -> tuple[dict[str, str], dict[str, str]]:
    """The light palette and the dark palette (light merged with overrides)."""
    blocks = re.findall(r":root\s*\{([^}]*)\}", css_text)
    palettes = [
        dict(re.findall(r"--([a-z0-9-]+)\s*:\s*(#[0-9a-fA-F]{6})\b", block))
        for block in blocks
    ]
    light = palettes[0] if palettes else {}
    dark = {**light, **(palettes[1] if len(palettes) > 1 else {})}
    return light, dark


def check_contrast(css_text: str) -> list[str]:
    findings = []
    light, dark = parse_palettes(css_text)
    for scheme_name, palette in (("light", light), ("dark", dark)):
        for fg, bg in CONTRAST_PAIRS:
            if fg not in palette or bg not in palette:
                findings.append(f"contrast: token --{fg} or --{bg} missing in {scheme_name}")
                continue
            ratio = contrast_ratio(palette[fg], palette[bg])
            if ratio < AA_NORMAL_TEXT:
                findings.append(
                    f"contrast: {scheme_name} --{fg} on --{bg} is {ratio:.2f}:1 "
                    f"(< {AA_NORMAL_TEXT}:1 AA)"
                )
    return findings


# --- runner ------------------------------------------------------------------

def validate(root_dir: Path | None = None) -> list[str]:
    base = root_dir or ROOT
    html_text = (base / "index.html").read_text(encoding="utf-8")
    css_text = (base / "styles.css").read_text(encoding="utf-8")
    data_text = (base / "data" / "projects.json").read_text(encoding="utf-8")

    data = json.loads(data_text)
    allowed_urls = {
        p["live_url"]
        for p in data.get("projects", []) + data.get("featured", [])
        if p.get("live_url")
    }

    root, findings = parse_html(html_text)
    findings = [f"parse: {e}" for e in findings]
    findings += check_structure(root)
    findings += check_links(root, base, allowed_urls)
    findings += check_offline_css(css_text)
    findings += check_accessibility(root)
    findings += check_bilingual(root)
    findings += check_honest_claims({"index.html": html_text, "data/projects.json": data_text})
    findings += check_contrast(css_text)
    return findings


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # pragma: no cover
        pass
    findings = validate()
    if findings:
        print(f"Site quality gate: {len(findings)} finding(s)")
        for finding in findings:
            print(f"  FAIL  {finding}")
        return 1
    html_text = (ROOT / "index.html").read_text(encoding="utf-8")
    root, _ = parse_html(html_text)
    pairs = sum(1 for el, _ in elements(root) if "data-en" in el.attrs)
    imgs = sum(1 for el, _ in elements(root) if el.tag == "img")
    anchors = sum(
        1 for el, _ in elements(root) if el.attrs.get("href", "").startswith("#")
    )
    checks = 2 * len(CONTRAST_PAIRS)
    print(
        "Site quality gate: PASS "
        f"(well-formed HTML; {anchors} fragment links resolve; {imgs} images "
        f"with bilingual alt; {pairs} EN/DE pairs; no banned claims; "
        f"{checks} contrast pairs >= {AA_NORMAL_TEXT}:1)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
