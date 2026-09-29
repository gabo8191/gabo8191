#!/usr/bin/env python3
"""Generate the animated SVG assets of the profile README.

Same "Hard Copy" neo-brutalist system as the portfolio (paper, ink, yellow,
pink, blue; 3px ink strokes; zero-blur offset shadows). GitHub serves README
images as <img>, so SVGs may only use CSS animation: no JavaScript and no
external fonts. Each SVG embeds its own font subset as a data URI, and text
widths are measured from the real glyph metrics so every tag fits.

Usage:
    python3 scripts/build_assets.py

Fonts are downloaded once into .fonts/ (git-ignored). Requires fontTools.
"""

from __future__ import annotations

import base64
import io
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
FONT_CACHE = ROOT / ".fonts"

PAPER = "#fffdf5"
INK = "#0d0d0d"
YELLOW = "#ffd93d"
PINK = "#ff6fb5"
BLUE = "#2f5bff"

GOOGLE_FONTS = "https://github.com/google/fonts/raw/main/ofl"
FONT_SOURCES = {
    "display": (
        "ArchivoBlack.ttf",
        f"{GOOGLE_FONTS}/archivoblack/ArchivoBlack-Regular.ttf",
        None,
    ),
    "mono": (
        "JetBrainsMono.ttf",
        f"{GOOGLE_FONTS}/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf",
        500,
    ),
    "body": (
        "SpaceGrotesk.ttf",
        f"{GOOGLE_FONTS}/spacegrotesk/SpaceGrotesk%5Bwght%5D.ttf",
        500,
    ),
}

MARQUEE_ITEMS = [
    "BACKEND",
    "INTEGRATIONS",
    "SQL",
    "PRODUCTION SUPPORT",
    "INTERNAL TOOLS",
    "PYTHON / DJANGO",
    "NESTJS",
    "LARAVEL",
    "JAVA / APACHE CAMEL",
    "REMOTE FROM TUNJA, CO",
]


# ── Fonts ─────────────────────────────────────────────────────────────


class Face:
    """A font instance that can measure text and emit a subset data URI."""

    def __init__(self, family: str, font: TTFont):
        self.family = family
        # Never rewrite the head timestamp, so reruns produce identical SVGs
        font.recalcTimestamp = False
        self.font = font
        self.cmap = font.getBestCmap()
        self.upem = font["head"].unitsPerEm
        self.used: set[str] = set()

    def width(self, text: str, size: float, tracking: float = 0.0) -> float:
        hmtx = self.font["hmtx"]
        missing = [char for char in text if ord(char) not in self.cmap]
        if missing:
            raise ValueError(f"{self.family} has no glyph for {missing!r}")
        units = sum(hmtx[self.cmap[ord(char)]][0] for char in text)
        return units * size / self.upem + tracking * max(len(text) - 1, 0)

    def use(self, text: str) -> str:
        self.used.update(text)
        return text

    def font_face(self) -> str:
        options = subset.Options()
        options.hinting = False
        options.layout_features = ["kern", "liga"]
        subsetter = subset.Subsetter(options)
        subsetter.populate(text="".join(sorted(self.used)))
        font = TTFont(io.BytesIO(self._raw()), recalcTimestamp=False)
        subsetter.subset(font)
        buffer = io.BytesIO()
        font.save(buffer)
        data = base64.b64encode(buffer.getvalue()).decode("ascii")
        return (
            f"@font-face{{font-family:'{self.family}';"
            f"src:url(data:font/ttf;base64,{data}) format('truetype');}}"
        )

    def _raw(self) -> bytes:
        buffer = io.BytesIO()
        self.font.save(buffer)
        return buffer.getvalue()


def load_faces() -> dict[str, Face]:
    FONT_CACHE.mkdir(exist_ok=True)
    faces: dict[str, Face] = {}
    for role, (filename, url, weight) in FONT_SOURCES.items():
        path = FONT_CACHE / filename
        if not path.exists():
            print(f"Downloading {filename}…")
            urllib.request.urlretrieve(url, path)
        font = TTFont(path)
        if weight is not None and "fvar" in font:
            font = instancer.instantiateVariableFont(font, {"wght": weight})
        faces[role] = Face(f"hc-{role}", font)
    return faces


def fresh_faces(template: dict[str, Face]) -> dict[str, Face]:
    """Each SVG embeds only the glyphs it uses."""
    return {role: Face(face.family, face.font) for role, face in template.items()}


# ── SVG helpers ───────────────────────────────────────────────────────


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


@dataclass
class Sticker:
    label: str
    note: str
    fill: str
    ink: str
    x: float
    y: float
    rotate: float


def sticker_svg(face: Face, sticker: Sticker, index: int) -> str:
    label_size, note_size, pad = 21, 14, 16
    width = (
        max(face.width(sticker.label, label_size), face.width(sticker.note, note_size))
        + pad * 2
    )
    height = 70 if sticker.note else 50
    shadow = PINK if sticker.fill == INK else INK
    note = (
        f'<text x="{pad}" y="56" font-size="{note_size}">{esc(face.use(sticker.note))}</text>'
        if sticker.note
        else ""
    )
    return f"""
  <g transform="translate({sticker.x} {sticker.y}) rotate({sticker.rotate})">
    <g class="drop" style="animation-delay:{0.35 + index * 0.14:.2f}s">
      <rect x="6" y="6" width="{width:.1f}" height="{height}" fill="{shadow}"/>
      <rect width="{width:.1f}" height="{height}" fill="{sticker.fill}" stroke="{INK}" stroke-width="3"/>
      <g font-family="{face.family}" fill="{sticker.ink}">
        <text x="{pad}" y="{31 if sticker.note else 32}" font-size="{label_size}">{esc(face.use(sticker.label))}</text>
        {note}
      </g>
    </g>
  </g>"""


def marquee_svg(
    face: Face, y: float, height: float, reverse: bool, fill: str, color: str
) -> str:
    size, gap = 17, 34
    x = 0.0
    parts: list[str] = []
    copy_width = 0.0
    for _ in range(2):
        for item in MARQUEE_ITEMS:
            parts.append(
                f'<text x="{x:.1f}" y="{y + height / 2 + 6:.1f}">{esc(face.use(item))}</text>'
            )
            x += face.width(item, size, 1.2) + gap / 2
            parts.append(
                f'<text x="{x:.1f}" y="{y + height / 2 + 6:.1f}" fill="{YELLOW}">{face.use("◆")}</text>'
            )
            x += face.width("◆", size) + gap / 2
        if copy_width == 0.0:
            copy_width = x
    direction = "reverse" if reverse else "normal"
    return f"""
  <rect y="{y}" width="1200" height="{height}" fill="{fill}"/>
  <g font-family="{face.family}" font-size="{size}" letter-spacing="1.2" fill="{color}">
    <g class="marquee" style="--shift:-{copy_width:.1f}px;animation-direction:{direction}">
      {"".join(parts)}
    </g>
  </g>"""


def document(
    width: int, height: int, faces: dict[str, Face], css: str, body: str, label: str
) -> str:
    font_faces = "".join(face.font_face() for face in faces.values() if face.used)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(label)}">
  <title>{esc(label)}</title>
  <style>
    {font_faces}
    {css}
    @media (prefers-reduced-motion: reduce) {{
      * {{ animation: none !important; }}
    }}
  </style>
{body}
</svg>
"""


BASE_CSS = """
    .marquee { animation: marquee 32s linear infinite; }
    @keyframes marquee { to { transform: translateX(var(--shift)); } }
    .drop { animation: drop 0.9s cubic-bezier(.2,.9,.3,1.3) both; }
    @keyframes drop {
      0% { transform: translateY(-560px) rotate(-14deg); }
      100% { transform: none; }
    }
    .rise { animation: rise 0.8s cubic-bezier(.2,.9,.3,1.25) both; }
    @keyframes rise { from { transform: translateY(110px); } to { transform: none; } }
    .pop { animation: pop 0.45s cubic-bezier(.2,.9,.3,1.4) both; transform-box: fill-box; transform-origin: center; }
    @keyframes pop { from { transform: scale(0.4) rotate(-8deg); opacity: 0; } to { transform: none; opacity: 1; } }
"""


# ── Header ────────────────────────────────────────────────────────────


def build_header(template: dict[str, Face]) -> str:
    faces = fresh_faces(template)
    display, mono = faces["display"], faces["mono"]
    width, height = 1200, 450

    name_size = 118
    # Keep the longest line clear of the sticker column
    while display.width("CASTILLO.", name_size) > 700:
        name_size -= 2

    role = "Backend & Integration Engineer"
    role_width = mono.width(role, 18) + 32
    lines = [("GABRIEL", 244), ("CASTILLO.", 244 + name_size * 0.9)]
    name_svg = "".join(
        f"""
  <g clip-path="url(#line{i})">
    <text class="rise" style="animation-delay:{0.1 + i * 0.12:.2f}s" x="44" y="{y:.1f}"
          font-family="{display.family}" font-size="{name_size}" fill="{INK}">{display.use(text)}</text>
  </g>"""
        for i, (text, y) in enumerate(lines)
    )
    clips = "".join(
        f'<clipPath id="line{i}"><rect x="0" y="{y - name_size * 0.9:.1f}" width="820" height="{name_size * 0.98:.1f}"/></clipPath>'
        for i, (_, y) in enumerate(lines)
    )

    stickers = [
        Sticker("MT103 → pacs.008", "SWIFT · ISO 20022", INK, PAPER, 800, 88, -5),
        Sticker(
            "Siigo · Alegra · SATCOM", "e-invoicing connectors", PINK, INK, 836, 174, 4
        ),
        Sticker(
            "L2/L3 incidents", "SQL · Sentry · war rooms", PAPER, INK, 790, 260, -3
        ),
        Sticker(
            "Django + Celery", "PBIX → Tableau estimates", BLUE, PAPER, 866, 342, 5
        ),
    ]
    # Stickers fall in below the marquee strip, never over it
    stickers_svg = (
        '<g clip-path="url(#desk)">'
        + "".join(sticker_svg(mono, sticker, i) for i, sticker in enumerate(stickers))
        + "</g>"
    )

    footer_line = (
        "Python/Django · NestJS · Laravel · Java · SQL — Tunja, Colombia · Remote"
    )
    body = f"""
  <defs>{clips}<clipPath id="desk"><rect x="0" y="52" width="{width}" height="{height - 52}"/></clipPath></defs>
  <rect width="{width}" height="{height}" fill="{YELLOW}"/>
  {marquee_svg(mono, 0, 52, False, INK, PAPER)}
  <rect x="50" y="86" width="{role_width:.1f}" height="36" fill="{INK}"/>
  <text x="66" y="110" font-family="{mono.family}" font-size="18" fill="{PAPER}">{esc(mono.use(role))}</text>
  {name_svg}
  <text x="46" y="{lines[1][1] + 58:.1f}" font-family="{mono.family}" font-size="17" fill="{INK}">{esc(mono.use(footer_line))}</text>
  {stickers_svg}
  <rect x="1.5" y="1.5" width="{width - 3}" height="{height - 3}" fill="none" stroke="{INK}" stroke-width="3"/>"""
    return document(
        width,
        height,
        faces,
        BASE_CSS,
        body,
        "Gabriel Castillo — Backend and Integration Engineer",
    )


# ── Section banners ───────────────────────────────────────────────────


def build_section(
    template: dict[str, Face], index: str, title: str, accent: str
) -> str:
    faces = fresh_faces(template)
    display, mono = faces["display"], faces["mono"]
    width, height = 1200, 112
    index_width = mono.width(index, 17) + 26
    title_size = 58
    while display.width(title, title_size) > 900:
        title_size -= 2
    body = f"""
  <rect width="{width}" height="{height}" fill="{INK}"/>
  <rect x="32" y="{height / 2 - 17}" width="{index_width:.1f}" height="34" fill="{accent}"/>
  <text x="45" y="{height / 2 + 6}" font-family="{mono.family}" font-size="17" fill="{INK}">{esc(mono.use(index))}</text>
  <g clip-path="url(#title)">
    <text class="rise" x="{56 + index_width:.1f}" y="{height / 2 + title_size * 0.36:.1f}"
          font-family="{display.family}" font-size="{title_size}" fill="{PAPER}">{esc(display.use(title))}</text>
  </g>
  <defs><clipPath id="title"><rect x="0" y="10" width="{width}" height="{height - 20}"/></clipPath></defs>
  <rect x="1130" y="{height / 2 - 18}" width="36" height="36" fill="{accent}" stroke="{PAPER}" stroke-width="3"/>"""
    return document(width, height, faces, BASE_CSS, body, f"{index} {title.title()}")


# ── Stack sheet ───────────────────────────────────────────────────────

STACK = [
    ("Languages", YELLOW, ["Python", "TypeScript", "PHP", "Java", "SQL"]),
    (
        "Backend",
        PINK,
        [
            "Django",
            "DRF",
            "Celery",
            "NestJS",
            "Laravel",
            "Filament",
            "Apache Camel",
            "REST",
            "OpenAPI",
        ],
    ),
    (
        "Data",
        PAPER,
        [
            "PostgreSQL",
            "MySQL",
            "Oracle PL/SQL",
            "Redis",
            "pandas",
            "Excel",
            "Power BI",
            "Tableau",
        ],
    ),
    (
        "Operations",
        BLUE,
        ["L2/L3 diagnosis", "Sentry", "Docker", "Portainer", "GitHub Actions", "Linux"],
    ),
]


def build_stack(template: dict[str, Face]) -> str:
    faces = fresh_faces(template)
    display, mono = faces["display"], faces["mono"]
    width = 1200
    column_width, gap, margin = 264, 24, 36
    tag_size, tag_height, tag_pad = 15, 32, 11
    blocks: list[tuple[int, str, str, str, str]] = []
    tallest = 0.0
    tag_index = 0
    for column, (title, fill, items) in enumerate(STACK):
        x0 = margin + column * (column_width + gap)
        ink = PAPER if fill == BLUE else INK
        cursor_x, cursor_y = x0 + 18, 96.0
        tags: list[str] = []
        for item in items:
            tag_width = mono.width(item, tag_size) + tag_pad * 2
            if cursor_x + tag_width > x0 + column_width - 16:
                cursor_x, cursor_y = x0 + 18, cursor_y + tag_height + 12
            tags.append(
                f"""
      <g class="pop" style="animation-delay:{0.2 + tag_index * 0.05:.2f}s">
        <rect x="{cursor_x + 3:.1f}" y="{cursor_y + 3:.1f}" width="{tag_width:.1f}" height="{tag_height}" fill="{INK}"/>
        <rect x="{cursor_x:.1f}" y="{cursor_y:.1f}" width="{tag_width:.1f}" height="{tag_height}" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>
        <text x="{cursor_x + tag_pad:.1f}" y="{cursor_y + 21:.1f}" font-family="{mono.family}" font-size="{tag_size}" fill="{INK}">{esc(mono.use(item))}</text>
      </g>"""
            )
            cursor_x += tag_width + 10
            tag_index += 1
        block_height = cursor_y + tag_height + 22 - 36
        tallest = max(tallest, block_height)
        blocks.append((x0, fill, ink, title, "".join(tags)))

    height = int(36 + tallest + 44)
    body_parts = [
        f'<rect width="{width}" height="{height}" fill="{PAPER}"/>',
        f'<pattern id="dots" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1.3" fill="{INK}" fill-opacity="0.18"/></pattern>',
        f'<rect width="{width}" height="{height}" fill="url(#dots)"/>',
    ]
    for x0, fill, ink, title, tags in blocks:
        body_parts.append(
            f"""
  <rect x="{x0 + 8}" y="44" width="{column_width}" height="{tallest:.1f}" fill="{INK}"/>
  <rect x="{x0}" y="36" width="{column_width}" height="{tallest:.1f}" fill="{fill}" stroke="{INK}" stroke-width="3"/>
  <text x="{x0 + 18}" y="78" font-family="{display.family}" font-size="26" fill="{ink}">{esc(display.use(title.upper()))}</text>
  {tags}"""
        )
    body_parts.append(
        f'<rect x="1.5" y="1.5" width="{width - 3}" height="{height - 3}" fill="none" stroke="{INK}" stroke-width="3"/>'
    )
    label = "Stack: " + "; ".join(
        f"{title}: {', '.join(items)}" for title, _, items in STACK
    )
    return document(width, height, faces, BASE_CSS, "\n".join(body_parts), label)


# ── Footer ────────────────────────────────────────────────────────────


def build_footer(template: dict[str, Face]) -> str:
    faces = fresh_faces(template)
    display, mono = faces["display"], faces["mono"]
    width, height = 1200, 250
    size = 92
    lets = display.width("LET'S TALK", size)
    systems = "SYSTEMS."
    systems_width = display.width(systems, size) + 30
    x_systems = 44 + lets + 30
    if x_systems + systems_width > width - 40:
        size = 76
        lets = display.width("LET'S TALK", size)
        systems_width = display.width(systems, size) + 30
        x_systems = 44 + lets + 26
    body = f"""
  <rect width="{width}" height="{height}" fill="{PINK}"/>
  <g clip-path="url(#talk)">
    <text class="rise" x="44" y="138" font-family="{display.family}" font-size="{size}" fill="{INK}">{display.use("LET'S TALK")}</text>
  </g>
  <defs><clipPath id="talk"><rect x="0" y="40" width="{width}" height="118"/></clipPath></defs>
  <g transform="rotate(-3 {x_systems + systems_width / 2:.1f} 105)">
    <g class="drop" style="animation-delay:0.5s">
      <rect x="{x_systems + 7:.1f}" y="{146 - size * 0.86 + 7:.1f}" width="{systems_width:.1f}" height="{size * 0.98:.1f}" fill="{INK}"/>
      <rect x="{x_systems:.1f}" y="{146 - size * 0.86:.1f}" width="{systems_width:.1f}" height="{size * 0.98:.1f}" fill="{YELLOW}" stroke="{INK}" stroke-width="4"/>
      <text x="{x_systems + 15:.1f}" y="138" font-family="{display.family}" font-size="{size}" fill="{INK}">{display.use(systems)}</text>
    </g>
  </g>
  {marquee_svg(mono, 196, 54, True, INK, PAPER)}
  <rect x="1.5" y="1.5" width="{width - 3}" height="{height - 3}" fill="none" stroke="{INK}" stroke-width="3"/>"""
    return document(width, height, faces, BASE_CSS, body, "Let's talk systems.")


# ── Main ──────────────────────────────────────────────────────────────

SECTIONS = [
    ("01 / ABOUT", "WHAT I DO", YELLOW),
    ("02 / STACK", "TOOLS I USE", PINK),
    ("03 / OPEN SOURCE", "BUILT IN THE OPEN", BLUE),
    ("04 / LIVE", "LIVE PROJECTS", YELLOW),
    ("05 / EXPERIENCE", "WHERE I WORKED", PINK),
    ("06 / EDUCATION", "STUDIES & LANGUAGES", BLUE),
]


def main() -> None:
    template = load_faces()
    ASSETS.mkdir(exist_ok=True)
    outputs = {
        "header.svg": build_header(template),
        "stack.svg": build_stack(template),
        "footer.svg": build_footer(template),
    }
    for index, title, accent in SECTIONS:
        slug = index.split("/")[1].strip().lower().replace(" ", "-")
        outputs[f"section-{slug}.svg"] = build_section(template, index, title, accent)
    for name, content in outputs.items():
        (ASSETS / name).write_text(content, encoding="utf-8")
        print(f"assets/{name}  {len(content.encode()) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
