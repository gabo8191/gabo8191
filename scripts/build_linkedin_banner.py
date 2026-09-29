#!/usr/bin/env python3
"""Render the LinkedIn profile banner in the README's "Hard Copy" style.

LinkedIn personal banners are 1584x396 px. The profile photo covers the
lower-left corner and mobile crops the edges, so the left block stays empty
and every piece of text sits inside the central band.

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

from build_assets import FONT_CACHE, INK, PAPER, PINK, YELLOW

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "assets" / "linkedin-banner.png"
WIDTH, HEIGHT = 1584, 396

# (title, caption, fill, text color, x, y, rotation in degrees)
STICKERS = [
    ("Systems that talk", "banks, invoicing, CRMs", INK, PAPER, 1090, 76, -4),
    ("Bugs traced to the root", "SQL → logs → code", PINK, INK, 1124, 166, 3),
    ("Busywork → internal tool", "Django, Laravel, React", PAPER, INK, 1080, 256, -2),
]

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


def sticker_html(
    title: str, caption: str, fill: str, color: str, x: int, y: int, angle: int
) -> str:
    shadow = PINK if fill == INK else INK
    return f"""
    <div class="sticker" style="left:{x}px;top:{y}px;transform:rotate({angle}deg);
         background:{fill};color:{color};box-shadow:6px 6px 0 {shadow}">
      <strong>{title}</strong><span>{caption}</span>
    </div>"""


def page() -> str:
    marquee = "<i>◆</i>".join(f"<span>{item}</span>" for item in STRIP_ITEMS)
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
          color: {PAPER}; display: flex; align-items: center; justify-content: space-between; white-space: nowrap;
          font-weight: 600; font-size: 19px; letter-spacing: 0.06em; padding: 0 28px; }}
.strip i {{ color: {YELLOW}; font-style: normal; font-size: 14px; }}
/* Dotted desk behind the profile photo: decoration only, nothing to read */
.desk {{ position: absolute; left: 0; top: 52px; width: 430px; bottom: 0;
         background-image: radial-gradient({INK} 1.6px, transparent 1.8px);
         background-size: 22px 22px; opacity: 0.22; }}
.copy {{ position: absolute; left: 470px; top: 74px; }}
.role {{ display: inline-block; background: {INK}; color: {PAPER}; font-size: 19px;
         font-weight: 500; padding: 7px 16px; }}
.name {{ font-family: Display, sans-serif; font-size: 86px; line-height: 0.9;
         color: {INK}; margin-top: 16px; letter-spacing: -0.01em; }}
.links {{ display: flex; gap: 14px; margin-top: 20px; }}
.links span {{ font-size: 18px; font-weight: 600; padding: 6px 14px; border: 3px solid {INK};
               box-shadow: 5px 5px 0 {INK}; }}
.sticker {{ position: absolute; border: 3px solid {INK}; padding: 10px 16px 11px;
            display: flex; flex-direction: column; gap: 3px; min-width: 300px; }}
.sticker strong {{ font-size: 21px; font-weight: 700; }}
.sticker span {{ font-family: Body, sans-serif; font-size: 16px; font-weight: 500; }}
.frame {{ position: absolute; inset: 0; border: 3px solid {INK}; pointer-events: none; }}
</style></head><body>
  <div class="strip">{marquee}</div>
  <div class="desk"></div>
  <div class="copy">
    <div class="role">Backend &amp; Integration Engineer</div>
    <div class="name">GABRIEL<br>CASTILLO.</div>
    <div class="links">
      <span style="background:{PINK}">gabo8191.github.io/portfolio</span>
    </div>
  </div>
  {stickers}
  <div class="frame"></div>
</body></html>"""


def main() -> None:
    """Write the banner HTML to a temp file and screenshot it with Chrome."""
    chrome = shutil.which("google-chrome") or shutil.which("chromium")
    if chrome is None:
        raise SystemExit("Google Chrome or Chromium is required to render the banner")
    if not (FONT_CACHE / "ArchivoBlack.ttf").exists():
        raise SystemExit("Fonts missing: run scripts/build_assets.py first")
    with tempfile.TemporaryDirectory() as tmp:
        html = Path(tmp) / "banner.html"
        html.write_text(page(), encoding="utf-8")
        subprocess.run(
            [
                chrome,
                "--headless=new",
                "--disable-gpu",
                "--hide-scrollbars",
                "--allow-file-access-from-files",
                f"--window-size={WIDTH},{HEIGHT}",
                f"--screenshot={OUTPUT}",
                html.as_uri(),
            ],
            check=True,
            capture_output=True,
        )
    print(OUTPUT)


if __name__ == "__main__":
    main()
