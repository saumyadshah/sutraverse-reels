#!/usr/bin/env python3
"""Shlokwise carousel renderer (2.0 kit) ("Lamp & Ink"), 1080x1350 slides.

  python3 toolkit/brand2/carousel2.py spec.json out_dir

spec.json: {"series": "Ghar Ki Baat", "format": "Field Guide", "cover_cast": {"name": "riya", "mood": "worried"} (optional),
            "slides": [{type: cover|point|shloka|cta, kicker, title (*word* = amber), sub, body, n, ref, deva, iast, meaning}]}
Same slide types as the v4 make_post.py spec, so verified v4 specs can be re-rendered in 2.0 by adding "series"/"format".
"""
import html, json, os, re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

KIT = Path(__file__).resolve().parent
BRAND = json.loads((KIT.parent / "BRAND.json").read_text())
IG = BRAND["instagram"]["handle"]
WORD = html.escape(BRAND["wordmark"])
SIG = html.escape(BRAND["tagline"])


def md(s):
    s = html.escape(s or "")
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)


CSS = """
@import url('brand2.css');
* { box-sizing: border-box; }
html, body { margin: 0; width: 1080px; height: 1350px; background: var(--ink); }
.s { position: relative; width: 1080px; height: 1350px; overflow: hidden; color: var(--paper);
  background: radial-gradient(90% 70% at 70% 18%, rgba(242,169,59,.10), transparent 60%), var(--ink); }
.s::after { content: ""; position: absolute; inset: 0; pointer-events: none;
  background: radial-gradient(130% 100% at 50% 40%, transparent 60%, rgba(0,0,0,.5) 100%); }
.top { position: absolute; top: 64px; left: 72px; right: 72px; display: flex; justify-content: space-between; align-items: center; z-index: 5; }
.top .word span { font: 700 30px/1 var(--display); letter-spacing: .2em; }
.top .chip { color: var(--amber); font-size: 22px; padding: 8px 14px 6px; }
.pg { position: absolute; bottom: 60px; right: 72px; font: 600 24px/1 var(--mono); letter-spacing: .1em; color: var(--dust); z-index: 5; }
.sw { position: absolute; bottom: 60px; left: 72px; font: 600 24px/1 var(--mono); letter-spacing: .14em; color: var(--amber); z-index: 5; }
.box { position: absolute; left: 72px; right: 72px; top: 190px; bottom: 140px; display: flex; flex-direction: column; z-index: 3; }
.k { font: 600 26px/1.2 var(--mono); letter-spacing: .14em; text-transform: uppercase; color: var(--amber); }
h1, h2 { margin: 0; font-family: var(--display); font-weight: 700; font-variation-settings: "opsz" 144, "SOFT" 30; letter-spacing: -.01em; }
h1 { font-size: 104px; line-height: 1.0; }
h2 { font-size: 78px; line-height: 1.04; }
h1 em, h2 em { font-style: italic; font-weight: 600; color: var(--amber); }
.sub { font: 500 40px/1.32 var(--ui); color: var(--bone); }
.body { font: 500 42px/1.36 var(--ui); color: var(--paper); }
.ref { font: 500 24px/1.3 var(--mono); color: var(--dust); letter-spacing: .04em; }
.num { font: 600 130px/1 var(--mono); color: var(--amber); letter-spacing: -.02em; }
.rule { height: 3px; width: 120px; background: var(--amber); }
.panel { background: var(--coal); border-left: 8px solid var(--amber); padding: 34px 38px; border-radius: 4px; }
.deva { font: 400 56px/1.55 var(--sanskrit); color: var(--paper); }
.iast { font: italic 400 32px/1.4 var(--display); color: var(--bone); }
.cta-foot { font: 600 28px/1.35 var(--mono); color: var(--teal); letter-spacing: .04em; }
canvas.cast { position: absolute; right: -40px; bottom: 0; z-index: 2; }
.cover .box { bottom: auto; top: 200px; }
.cover .lowsub { position: absolute; left: 72px; width: 520px; bottom: 150px; z-index: 4; }
"""


def slide_html(s, i, n, spec):
    t = s.get("type", "point")
    top = (f'<div class="top"><div class="sv2-word word"><span>{html.escape(BRAND["wordmark"])}</span></div>'
           f'<div class="sv2-chip chip">{html.escape(spec.get("series", ""))}</div></div>')
    foot = f'<div class="pg">{i:02d}/{n:02d}</div>' + ('<div class="sw">SWIPE &rarr;</div>' if i < n else "")
    if t == "cover":
        fmt = spec.get("format", "")
        inner = (f'<div class="box" style="gap:34px;justify-content:flex-start">'
                 f'<div class="k">{html.escape(s.get("kicker", ""))}{" · " + html.escape(fmt) if fmt else ""}</div>'
                 f'<h1>{md(s.get("title"))}</h1><div class="rule"></div></div>'
                 f'<div class="lowsub" style="display:flex;flex-direction:column;gap:22px;{"" if spec.get("cover_cast") else "width:820px"}">'
                 f'<div class="sub">{md(s.get("sub"))}</div><div class="ref">{html.escape(s.get("ref", ""))}</div></div>')
        cast = '<canvas class="cast" id="cast" width="500" height="700"></canvas>' if spec.get("cover_cast") else ""
        return f'<div class="s cover">{top}{inner}{cast}{foot}</div>'
    if t == "shloka":
        inner = (f'<div class="box" style="gap:30px;justify-content:center">'
                 f'<div class="k">{html.escape(s.get("kicker", ""))}</div>'
                 f'<div class="deva">{html.escape(s.get("deva", ""))}</div>'
                 f'<div class="iast">{html.escape(s.get("iast", ""))}</div>'
                 f'<div class="panel"><div class="body" style="font-size:40px">{md(s.get("meaning"))}</div></div>'
                 f'<div class="ref">{html.escape(s.get("ref", ""))}</div></div>')
        return f'<div class="s">{top}{inner}{foot}</div>'
    if t == "cta":
        inner = (f'<div class="box" style="gap:40px;justify-content:center">'
                 f'<div class="k">{html.escape(s.get("kicker", ""))}</div><h2 style="font-size:92px">{md(s.get("title"))}</h2>'
                 f'<div class="rule" style="background:var(--teal)"></div><div class="sub">{md(s.get("sub"))}</div>'
                 f'<div class="cta-foot">@{html.escape(IG)} · {SIG}</div></div>')
        return f'<div class="s">{top}{inner}{foot}</div>'
    num = f'<div class="num">{html.escape(s["n"]).zfill(2)}</div>' if s.get("n") else ""
    ref = f'<div class="ref">{html.escape(s["ref"])}</div>' if s.get("ref") else ""
    inner = (f'<div class="box" style="gap:38px;justify-content:center">{num}<h2>{md(s.get("title"))}</h2>'
             f'<div class="rule"></div><div class="body">{md(s.get("body"))}</div>{ref}</div>')
    return f'<div class="s">{top}{inner}{foot}</div>'


def render(spec_path, out):
    spec = json.loads(Path(spec_path).read_text())
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    slides = spec["slides"]; n = len(slides)
    cc = spec.get("cover_cast")
    cast_js = ""
    if cc:
        cast_js = (f"<script src='cast2.js'></script><script>(j=>{{CAST2.load(j);"
                   f"const c=document.getElementById('cast');if(c){{const g=c.getContext('2d');"
                   f"CAST2.draw(g,{json.dumps(cc['name'])},{{x:250,y:330,s:200,yaw:-0.25,mood:{json.dumps(cc.get('mood','neutral'))},"
                   f"body:'bust',style:'cel',lookX:-0.4}});}}window.READY=true;}})({(KIT/'cast2.json').read_text()});</script>")
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        for i, s in enumerate(slides, 1):
            doc = (f"<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body>"
                   f"{slide_html(s, i, n, spec)}{cast_js if (s.get('type') == 'cover' and cast_js) else '<script>window.READY=true</script>'}</body></html>")
            tmp = KIT / f".c2_{i}.html"; tmp.write_text(doc)
            pg.goto(tmp.as_uri()); pg.wait_for_function("window.READY===true", timeout=20000)
            pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(150)
            pg.screenshot(path=str(out / f"slide-{i:02d}.png")); tmp.unlink()
        b.close()
    print("rendered", n, "slides to", out)


if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2])
