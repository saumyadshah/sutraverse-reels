#!/usr/bin/env python3
"""SutraVerse v4 cover / thumbnail generator (CONTENT_STANDARDS.md §8).

python3 cover.py --series office --line1 "Boss took" --line2 "your credit?" \
  --sub "Karna knew this feeling." --art frame.png [--inset ancient.png] --out cover.png

--art   a 1080x1920 still from the Reel (the modern character's face, rim-lit), used full-bleed.
--inset optional ancient-parallel still, shown small inside a Mithila double-outline panel.
Series: office (haldi), family (palash), friends (mor), social (kumkum), explains (chandan).
Writes a 1080x1920 PNG and a 270x480 preview (*_small.png) to check readability at grid size.
"""
import argparse, asyncio, html, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from motifs import C, mithila_frame  # noqa: E402

SERIES = {
    "office": ("Office ka Mahabharat", C["haldi"]),
    "family": ("Ghar ki Ramayan", C["palash"]),
    "friends": ("Dosti &amp; Dharma", "#2FB3A8"),
    "social": ("Log Kya Kahenge", "#E85A7F"),
    "explains": ("SutraVerse Explains", C["chandan"]),
}


def build(a):
    name, accent = SERIES[a.series]
    art = f'<img src="{pathlib.Path(a.art).resolve().as_uri()}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">' if a.art else ""
    inset = ""
    if a.inset:
        inset = (f'<svg width="1080" height="1920" style="position:absolute;inset:0;z-index:3">{mithila_frame(720,470,290,410,accent,band=18,gap=10)}</svg>'
                 f'<img src="{pathlib.Path(a.inset).resolve().as_uri()}" style="position:absolute;left:738px;top:488px;width:254px;height:374px;object-fit:cover;z-index:2">')
    return f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{(HERE/'brand.css').as_uri()}"></head><body>
<div class="frame grain vignette" style="background:{C['kajal']}">{art}{inset}
<div style="position:absolute;left:0;right:0;top:960px;bottom:0;z-index:4;background:linear-gradient(rgba(16,14,23,0),rgba(16,14,23,.92) 45%,{C['kajal']})"></div>
<div style="position:absolute;left:0;right:0;top:300px;text-align:center;z-index:6;color:{accent}"><span class="chip"><i></i>{name}<i></i></span></div>
<div style="position:absolute;left:70px;right:70px;top:1160px;z-index:6;text-align:center">
 <div class="headline" style="font-size:{a.size}px;color:{C['chandan']};text-shadow:0 8px 30px rgba(0,0,0,.6)">{html.escape(a.line1)}<br><em style="color:{accent}">{html.escape(a.line2)}</em></div>
 <div class="voice" style="margin-top:34px;font-size:58px;color:{C['chandan2']}">{html.escape(a.sub)}</div></div>
<div style="position:absolute;left:0;right:0;bottom:250px;text-align:center;z-index:6"><span class="wordmark">sutraverse</span></div>
</div></body></html>'''


async def shoot(page_html, out):
    from playwright.async_api import async_playwright
    tmp = pathlib.Path(out).with_suffix(".html"); tmp.write_text(page_html)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.goto(tmp.as_uri()); await pg.wait_for_timeout(800); await pg.screenshot(path=out); await b.close()
    tmp.unlink()
    from PIL import Image
    Image.open(out).resize((270, 480)).save(str(pathlib.Path(out).with_name(pathlib.Path(out).stem + "_small.png")))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--series", choices=SERIES, required=True)
    ap.add_argument("--line1", required=True); ap.add_argument("--line2", required=True); ap.add_argument("--sub", default="")
    ap.add_argument("--art"); ap.add_argument("--inset"); ap.add_argument("--size", type=int, default=170)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    words = len((a.line1 + " " + a.line2).split())
    if words > 6:
        sys.exit(f"headline has {words} words; keep it to 2-5 (CONTENT_STANDARDS §8)")
    asyncio.run(shoot(build(a), a.out)); print("cover written:", a.out)


if __name__ == "__main__":
    main()
