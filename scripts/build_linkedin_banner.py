#!/usr/bin/env python3
"""Render the LinkedIn profile banner in the README's "Hard Copy" style.

Layout rules taken from reviews of well-performing LinkedIn banners:
- 1584x396 px. The profile photo covers about 568x264 px of the lower-left
  corner on desktop, so that area only carries decoration.
- Mobile shows roughly the central 60% of the width: the value proposition and
  the call to action live in the centre; the right column is decoration.
- LinkedIn prints the name right below the banner, so the banner spends its
  space on one outcome statement readable in two seconds, not on the name.

Usage:
    python3 scripts/build_assets.py          # downloads the fonts into .fonts/
    python3 scripts/build_linkedin_banner.py

Requires Google Chrome for the headless screenshot.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

from build_assets import BLUE, FONT_CACHE, INK, PAPER, PINK, YELLOW

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "assets" / "linkedin-banner.png"
WIDTH, HEIGHT = 1584, 396

# A static banner cannot scroll, so the strip only carries what fits whole
STRIP_ITEMS = [
    "BACKEND",
    "INTEGRATIONS",
    "SQL",
    "PRODUCTION SUPPORT",
    "INTERNAL TOOLS",
    "PYTHON / DJANGO",
    "NESTJS",
    "LARAVEL",
]

# (title, caption, background, text color, top in px, rotation in degrees)
STICKERS = [
    ("Bugs traced to the root", "SQL → logs → code", INK, PAPER, 78, -4),
    ("Busywork → internal tool", "Django, Laravel, React", PINK, INK, 168, 3),
    ("Bank messages, translated", "SWIFT to ISO 20022", BLUE, PAPER, 262, -2),
]


def sticker_html(
    title: str, caption: str, fill: str, color: str, top: int, angle: int
) -> str:
    shadow = PINK if fill == INK else INK
    return f"""
    <div class="sticker" style="top:{top}px;transform:rotate({angle}deg);
         background:{fill};color:{color};box-shadow:6px 6px 0 {shadow}">
      <strong>{title}</strong><span>{caption}</span>
    </div>"""


def page() -> str:
    strip = "<i>◆</i>".join(f"<span>{item}</span>" for item in STRIP_ITEMS)
    stickers = "".join(sticker_html(*sticker) for sticker in STICKERS)
    fonts = FONT_CACHE.resolve()
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><style>
@font-face {{ font-family: Display; src: url("file://{fonts}/ArchivoBlack.ttf"); }}
@font-face {{ font-family: Mono; src: url("file://{fonts}/JetBrainsMono.ttf"); font-weight: 100 900; }}
@font-face {{ font-family: Body; src: url("file://{fonts}/SpaceGrotesk.ttf"); font-weight: 300 700; }}
* {{ margin: 0; box-sizing: border-box; }}
body {{ width: {WIDTH}px; height: {HEIGHT}px; overflow: hidden; background: {YELLOW};
        font-family: Mono, monospace; position: relative; }}
.strip {{ position: absolute; inset: 0 0 auto 0; height: 52px; background: {INK};
          color: {PAPER}; display: flex; align-items: center; justify-content: space-between;
          white-space: nowrap; font-weight: 600; font-size: 19px; letter-spacing: 0.06em;
          padding: 0 28px; }}
.strip i {{ color: {YELLOW}; font-style: normal; font-size: 14px; }}
/* Dotted desk under the profile photo: decoration only */
.desk {{ position: absolute; left: 0; top: 52px; width: 580px; bottom: 0;
         background-image: radial-gradient({INK} 1.6px, transparent 1.8px);
         background-size: 22px 22px; opacity: 0.2; }}
.copy {{ position: absolute; left: 610px; top: 74px; }}
.role {{ display: inline-block; background: {INK}; color: {PAPER}; font-size: 18px;
         font-weight: 500; padding: 6px 14px; }}
.headline {{ font-family: Display, sans-serif; font-size: 84px; line-height: 0.88;
             color: {INK}; margin-top: 16px; letter-spacing: -0.01em; }}
.sub {{ font-family: Body, sans-serif; font-size: 21px; font-weight: 500; color: {INK};
        margin-top: 16px; }}
.cta {{ display: inline-block; margin-top: 16px; font-size: 18px; font-weight: 700;
        padding: 7px 16px; border: 3px solid {INK}; background: {PINK};
        box-shadow: 5px 5px 0 {INK}; }}
.sticker {{ position: absolute; right: 40px; border: 3px solid {INK}; padding: 9px 15px 10px;
            display: flex; flex-direction: column; gap: 3px; white-space: nowrap; }}
.sticker strong {{ font-size: 18px; font-weight: 700; }}
.sticker span {{ font-family: Body, sans-serif; font-size: 15px; font-weight: 500; }}
.frame {{ position: absolute; inset: 0; border: 3px solid {INK}; pointer-events: none; }}
</style></head><body>
  <div class="strip">{strip}</div>
  <div class="desk"></div>
  <div class="copy">
    <div class="role">Backend &amp; Integration Engineer</div>
    <div class="headline">SYSTEMS<br>THAT TALK.</div>
    <div class="sub">APIs, integrations and internal tools that keep running.</div>
    <div class="cta">See my work → gabo8191.github.io/portfolio</div>
  </div>
  {stickers}
  <div class="frame"></div>
</body></html>"""


def render(html: str, output: Path) -> None:
    """Screenshot an HTML page at banner size with headless Chrome."""
    chrome = shutil.which("google-chrome") or shutil.which("chromium")
    if chrome is None:
        raise SystemExit("Google Chrome or Chromium is required to render the banner")
    with tempfile.TemporaryDirectory() as tmp:
        page_path = Path(tmp) / "banner.html"
        page_path.write_text(html, encoding="utf-8")
        subprocess.run(
            [
                chrome,
                "--headless=new",
                "--disable-gpu",
                "--hide-scrollbars",
                "--allow-file-access-from-files",
                f"--window-size={WIDTH},{HEIGHT}",
                f"--screenshot={output}",
                page_path.as_uri(),
            ],
            check=True,
            capture_output=True,
        )


def main() -> None:
    if not (FONT_CACHE / "ArchivoBlack.ttf").exists():
        raise SystemExit("Fonts missing: run scripts/build_assets.py first")
    render(page(), OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    main()
