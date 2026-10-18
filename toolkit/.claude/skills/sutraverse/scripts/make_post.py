#!/usr/bin/env python3
"""Render a SutraVerse Instagram post (single image or carousel, 1080x1350, 4:5) from a JSON spec.

Usage: python make_post.py spec.json out_dir
Spec:
{
  "slides": [
    {"type": "cover", "kicker": "UPANISHAD WISDOM", "title": "Arise. Awake.", "sub": "The 3-word line that...", "ref": "Katha Upanishad 1.3.14"},
    {"type": "shloka", "deva": "उत्तिष्ठत जाग्रत ...", "iast": "uttiṣṭhata jāgrata ...", "meaning": "Arise, awake ...", "ref": "Katha Upanishad 1.3.14"},
    {"type": "point", "n": 1, "title": "...", "body": "..."},
    {"type": "cta", "title": "Save this for the day you need it", "sub": "Follow @sutraverselife for daily wisdom"}
  ]
}
Rules (same as the Reels):
  - On-screen text is English.
  - Devanagari appears only in a "shloka" slide, and only for a verified quote with its reference.
Writes slide-01.png ... into out_dir.
Browser: uses $HYPERFRAMES_BROWSER_PATH when set; otherwise Playwright's default Chromium.
"""
import html
import json
import os
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent / "brand-kit"
FONTS = KIT / "fonts"
LOGO = (KIT / "logo.svg").read_text(encoding="utf-8")

CSS = f"""
@font-face{{font-family:Cinzel;font-weight:700;src:url({FONTS.as_uri()}/cinzel-latin-700-normal.woff2)}}
@font-face{{font-family:Corm;font-weight:600;src:url({FONTS.as_uri()}/cormorant-garamond-latin-600-normal.woff2)}}
@font-face{{font-family:Corm;font-weight:600;font-style:italic;src:url({FONTS.as_uri()}/cormorant-garamond-latin-600-italic.woff2)}}
@font-face{{font-family:Inter;font-weight:600;src:url({FONTS.as_uri()}/inter-latin-600-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:700;src:url({FONTS.as_uri()}/inter-latin-700-normal.woff2)}}
@font-face{{font-family:Tiro;src:url({FONTS.as_uri()}/tiro-devanagari-sanskrit-devanagari-400-normal.woff2)}}
html,body{{margin:0;background:#000}}
.s{{width:1080px;height:1350px;position:relative;overflow:hidden;box-sizing:border-box;padding:110px 96px;color:#FFF6E6;
  background:radial-gradient(circle at 50% 38%,#3A5BE0 0%,#2340B8 46%,#16247A 100%);font-family:Inter,sans-serif;display:flex;flex-direction:column;justify-content:center;gap:34px}}
.s::before{{content:"";position:absolute;inset:0;background:radial-gradient(circle at 50% 30%,rgba(255,178,46,.22),rgba(255,122,26,0) 48%);pointer-events:none}}
.s.light{{background:#FFF6E6;color:#1A1240}} .s.light::before{{background:radial-gradient(circle at 50% 20%,rgba(255,178,46,.35),rgba(255,178,46,0) 55%)}}
.kick{{font:700 30px/1 Inter;letter-spacing:.22em;color:#FFB22E;text-transform:uppercase}}
.title{{font:700 104px/1.04 Cinzel;letter-spacing:.01em;text-wrap:balance}}
.title em{{font-style:normal;color:#FFB22E}}
.sub{{font:600 46px/1.3 Corm;font-style:italic;color:#FFE6A6;text-wrap:balance}}
.light .sub{{color:#3B2E8E}}
.ref{{align-self:flex-start;font:700 26px/1 Inter;letter-spacing:.08em;text-transform:uppercase;background:#FF7A1A;color:#fff;padding:14px 22px;border-radius:999px}}
.deva{{font:400 76px/1.45 Tiro;color:#1A1240;text-wrap:balance}}
.iast{{font:600 40px/1.35 Corm;font-style:italic;color:#3B2E8E}}
.mean{{font:600 40px/1.4 Inter;color:#1A1240}}
.card{{background:#FFF6E6;border-radius:36px;padding:70px 64px;display:flex;flex-direction:column;gap:30px;box-shadow:0 30px 80px rgba(10,16,70,.45);border-top:12px solid #FF7A1A}}
.n{{font:700 150px/1 Cinzel;color:#FFB22E}}
.pt{{font:700 70px/1.12 Cinzel;text-wrap:balance}}
.body{{font:600 44px/1.42 Inter;color:#E8E3FF;text-wrap:pretty}}
.foot{{position:absolute;left:96px;right:96px;bottom:56px;display:flex;justify-content:space-between;align-items:center;font:700 24px/1 Inter;letter-spacing:.18em;color:rgba(255,246,230,.8)}}
.light .foot{{color:#3B2E8E}}
.foot svg{{width:56px;height:56px}}
.swipe{{color:#FFB22E}}
"""


def esc(t):
    return html.escape(str(t or ""))


def rich(t):
    """*word* -> highlighted"""
    out, parts = [], esc(t).split("*")
    for i, p in enumerate(parts):
        out.append(f"<em>{p}</em>" if i % 2 else p)
    return "".join(out)


def slide(s, i, n):
    t = s.get("type", "point")
    last = i == n
    foot = (f'<div class="foot"><span style="display:flex;gap:14px;align-items:center">{LOGO}SUTRAVERSE</span>'
            f'<span class="swipe">{"" if last else "SWIPE →"}</span><span>{i}/{n}</span></div>')
    if t == "cover":
        inner = (f'<div class="kick">{esc(s.get("kicker"))}</div><div class="title">{rich(s.get("title"))}</div>'
                 f'<div class="sub">{esc(s.get("sub"))}</div>' + (f'<div class="ref">{esc(s["ref"])}</div>' if s.get("ref") else ""))
        cls = "s"
    elif t == "shloka":
        inner = (f'<div class="kick">{esc(s.get("kicker", "THE ORIGINAL VERSE"))}</div><div class="card">'
                 f'<div class="deva">{esc(s.get("deva"))}</div><div class="iast">{esc(s.get("iast"))}</div>'
                 f'<div class="mean">{esc(s.get("meaning"))}</div><div class="ref">{esc(s.get("ref"))}</div></div>')
        cls = "s"
    elif t == "cta":
        inner = (f'<div class="kick">{esc(s.get("kicker", "ANCIENT WISDOM. MODERN LIFE."))}</div>'
                 f'<div class="title">{rich(s.get("title"))}</div><div class="sub">{esc(s.get("sub"))}</div>')
        cls = "s light"
    else:
        inner = (f'<div class="n">{esc(s.get("n", ""))}</div><div class="pt">{rich(s.get("title"))}</div>'
                 f'<div class="body">{esc(s.get("body"))}</div>' + (f'<div class="ref">{esc(s["ref"])}</div>' if s.get("ref") else ""))
        cls = "s"
    return f'<div class="{cls}" id="sl{i}">{inner}{foot}</div>'


def main():
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = Path(sys.argv[2]).resolve()
    out.mkdir(parents=True, exist_ok=True)
    slides = spec["slides"]
    import re
    for s in slides:
        if s.get("type") != "shloka":
            for k, v in s.items():
                if isinstance(v, str) and re.search(r"[ऀ-ॿ]", v):
                    sys.exit(f"Devanagari outside a shloka slide ({k}): on-screen text must be English")
        elif not s.get("ref"):
            sys.exit("shloka slide needs a ref")
    page = out / "_post.html"
    page.write_text(f"<!doctype html><meta charset=utf-8><style>{CSS}</style>" +
                    "".join(slide(s, i + 1, len(slides)) for i, s in enumerate(slides)), encoding="utf-8")
    from playwright.sync_api import sync_playwright
    exe = os.environ.get("HYPERFRAMES_BROWSER_PATH")
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=exe or None, args=["--no-sandbox", "--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        pg.goto(page.as_uri())
        pg.wait_for_timeout(600)
        for i in range(1, len(slides) + 1):
            pg.locator(f"#sl{i}").screenshot(path=str(out / f"slide-{i:02d}.png"))
        b.close()
    page.unlink()
    print(f"wrote {len(slides)} slide(s) to {out}")


if __name__ == "__main__":
    main()
