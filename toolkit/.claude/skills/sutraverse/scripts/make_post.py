#!/usr/bin/env python3
"""Render a SutraVerse Instagram post (single image or carousel, 1080x1350, 4:5) from a JSON spec.

Usage: python make_post.py spec.json out_dir
Spec (v4: optional "series": office|family|friends|social|explains puts the series chip on the cover and CTA slides):
{
  "series": "office",
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
@font-face{{font-family:Anek;font-weight:100 800;font-stretch:75% 125%;src:url({FONTS.as_uri()}/anek-latin-var.ttf)}}
@font-face{{font-family:Fraunces;font-weight:100 900;src:url({FONTS.as_uri()}/fraunces-var.ttf)}}
@font-face{{font-family:Fraunces;font-style:italic;font-weight:100 900;src:url({FONTS.as_uri()}/fraunces-italic-var.ttf)}}
@font-face{{font-family:Tiro;src:url({FONTS.as_uri()}/tiro-devanagari-sanskrit-devanagari-400-normal.woff2)}}
/* v4 "Mithila Night" (CONTENT_STANDARDS.md v4 §6-7, §9): kajal/neel night, chandan paper, haldi accent, Mithila double outline */
html,body{{margin:0;background:#000}}
.s{{--acc:#F2B33D;width:1080px;height:1350px;position:relative;overflow:hidden;box-sizing:border-box;padding:120px 104px;color:#F4EADB;
  background:radial-gradient(120% 80% at 50% 25%,#2A2F6B 0%,#1A1D47 48%,#100E17 100%);font-family:Anek,sans-serif;display:flex;flex-direction:column;justify-content:center;gap:34px}}
.s::before{{content:"";position:absolute;inset:34px;border:5px solid var(--acc);outline:2px solid var(--acc);outline-offset:-16px;pointer-events:none;opacity:.9}}
.s::after{{content:"";position:absolute;inset:0;pointer-events:none;opacity:.07;
  background:repeating-linear-gradient(135deg,#F4EADB 0 2px,transparent 2px 9px)}}
.s.light{{background:#F4EADB;color:#100E17}} .s.light::after{{background:repeating-linear-gradient(135deg,#100E17 0 2px,transparent 2px 11px);opacity:.05}}
.chip{{align-self:flex-start;display:inline-flex;gap:14px;align-items:center;font:700 26px/1 Anek;font-stretch:85%;letter-spacing:.16em;text-transform:uppercase;
  color:var(--acc);border:2px solid var(--acc);outline:3px solid var(--acc);outline-offset:5px;padding:12px 20px 10px}}
.chip i{{width:12px;height:12px;background:currentColor;transform:rotate(45deg);display:inline-block}}
.kick{{font:700 28px/1 Anek;font-stretch:85%;letter-spacing:.2em;color:var(--acc);text-transform:uppercase}}
.title{{font:800 112px/.95 Anek;font-stretch:75%;text-transform:uppercase;letter-spacing:-.005em;text-wrap:balance}}
.title em{{font-style:normal;color:var(--acc)}}
.sub{{font:italic 500 48px/1.25 Fraunces;color:#D9CBB4;text-wrap:balance}}
.light .sub{{color:#2A2F6B}}
.ref{{align-self:flex-start;font:700 24px/1 Anek;font-stretch:85%;letter-spacing:.14em;text-transform:uppercase;background:#100E17;color:#F2B33D;padding:14px 20px 12px}}
.deva{{font:400 62px/1.4 Tiro;color:#100E17;text-wrap:balance}}
.iast{{font:italic 500 34px/1.32 Fraunces;color:#2A2F6B}}
.mean{{font:600 40px/1.34 Anek;color:#100E17;padding-top:22px;border-top:3px double #F2B33D}}
.card{{background:#F4EADB;padding:54px 56px;display:flex;flex-direction:column;gap:20px;box-shadow:inset 0 0 0 5px #F2B33D,inset 0 0 0 12px #F4EADB,inset 0 0 0 15px #100E17,0 30px 80px rgba(0,0,0,.5)}}
.n{{font:800 160px/1 Anek;font-stretch:75%;color:var(--acc)}}
.pt{{font:800 76px/1 Anek;font-stretch:75%;text-transform:uppercase;text-wrap:balance}}
.pt em{{font-style:normal;color:var(--acc)}}
.body{{font:500 44px/1.4 Anek;color:#F4EADB;text-wrap:pretty}}
.foot{{position:absolute;left:104px;right:104px;bottom:66px;display:flex;justify-content:space-between;align-items:center;font:700 24px/1 Anek;font-stretch:85%;letter-spacing:.16em;color:rgba(244,234,219,.8)}}
.light .foot{{color:#2A2F6B}}
.wm{{font:700 30px/1 Anek;font-stretch:85%;letter-spacing:.02em;text-transform:lowercase;color:#F4EADB;padding-bottom:9px;border-bottom:6px double #F2B33D}}
.light .wm{{color:#100E17}}
.swipe{{color:var(--acc)}}
"""
SERIES = {"office": ("Office ka Mahabharat", "#F2B33D"), "family": ("Ghar ki Ramayan", "#EE7A2E"),
          "friends": ("Dosti &amp; Dharma", "#2FB3A8"), "social": ("Log Kya Kahenge", "#E85A7F"),
          "explains": ("SutraVerse Explains", "#F2B33D")}


def esc(t):
    return html.escape(str(t or ""))


def rich(t):
    """*word* -> highlighted"""
    out, parts = [], esc(t).split("*")
    for i, p in enumerate(parts):
        out.append(f"<em>{p}</em>" if i % 2 else p)
    return "".join(out)


def slide(s, i, n, series=None):
    t = s.get("type", "point")
    last = i == n
    name, acc = SERIES.get(series or "", (None, "#F2B33D"))
    chip = f'<div class="chip"><i></i>{name}<i></i></div>' if name else ""
    foot = (f'<div class="foot"><span class="wm">sutraverse</span>'
            f'<span class="swipe">{"" if last else "SWIPE →"}</span><span>{i}/{n}</span></div>')
    if t == "cover":
        inner = (chip + (f'<div class="kick">{esc(s["kicker"])}</div>' if s.get("kicker") else "") + f'<div class="title">{rich(s.get("title"))}</div>'
                 f'<div class="sub">{esc(s.get("sub"))}</div>' + (f'<div class="ref">{esc(s["ref"])}</div>' if s.get("ref") else ""))
        cls = "s"
    elif t == "shloka":
        inner = (f'<div class="kick">{esc(s.get("kicker", "THE ORIGINAL VERSE"))}</div><div class="card">'
                 f'<div class="deva">{esc(s.get("deva"))}</div><div class="iast">{esc(s.get("iast"))}</div>'
                 f'<div class="mean">{esc(s.get("meaning"))}</div><div class="ref">{esc(s.get("ref"))}</div></div>')
        cls = "s"
    elif t == "cta":
        inner = (chip + f'<div class="kick">{esc(s.get("kicker", "ANCIENT WISDOM. MODERN LIFE."))}</div>'
                 f'<div class="title">{rich(s.get("title"))}</div><div class="sub">{esc(s.get("sub"))}</div>')
        cls = "s light"
    else:
        inner = (f'<div class="n">{esc(s.get("n", ""))}</div><div class="pt">{rich(s.get("title"))}</div>'
                 f'<div class="body">{esc(s.get("body"))}</div>' + (f'<div class="ref">{esc(s["ref"])}</div>' if s.get("ref") else ""))
        cls = "s"
    return f'<div class="{cls}" id="sl{i}" style="--acc:{acc if cls == "s" else "#9E2348"}">{inner}{foot}</div>'


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
                    "".join(slide(s, i + 1, len(slides), spec.get("series")) for i, s in enumerate(slides)), encoding="utf-8")
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
