#!/usr/bin/env python3
"""Render model sheets for cast characters (CONTENT_STANDARDS §17).

  python model_sheet.py                      # every character in toolkit/cast/cast.json
  python model_sheet.py --names kabir,gajendra --out qa/cast
  python model_sheet.py --extra projects/<id>/artifacts/cast_local.json   # characters new in this Reel

Modern characters: the same rig at ECU/CU/MCU/MS/WS, then the 8 expressions in close-up.
Mithila characters: the figure plus its action poses. One PNG per character + cast_overview.png.
Look at the sheets BEFORE animating: same face, hair, outfit and proportions in every cell.
"""
import argparse, asyncio, json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
KIT = HERE.parent / "brand-kit"


def find_registry():
    for p in [HERE.parents[3] / "cast" / "cast.json", pathlib.Path.home() / "sutraverse-reels/toolkit/cast/cast.json",
              pathlib.Path("/root/sutraverse-reels/toolkit/cast/cast.json")]:
        if p.is_file():
            return p
    sys.exit("cast.json not found; pass --registry")


PAGE = """<!doctype html><html><head><meta charset="utf-8">
<style>@font-face{font-family:Anek;src:url('%(font)s')} body{margin:0;background:#100E17;color:#F4EADB;font-family:Anek,sans-serif}
.sheet{display:flex;flex-direction:column;gap:14px;padding:24px} h1{margin:0;font-size:34px;letter-spacing:.06em;text-transform:uppercase}
.sub{opacity:.7;font-size:20px} .row{display:flex;gap:12px;flex-wrap:wrap;max-width:1460px} .cell{display:flex;flex-direction:column;gap:6px;align-items:center}
.cell svg{background:radial-gradient(circle at 50%% 40%%,#2A2F6B,#1A1D47 70%%);border-radius:10px} .cell span{font-size:18px;opacity:.8;letter-spacing:.08em;text-transform:uppercase}
.m svg{background:#D63E2A}</style>
<script src="%(gsap)s"></script><script src="%(cast)s"></script></head><body><div class="sheet" id="S"></div>
<script>
CAST.load(%(reg)s);
const name = %(name)s, spec = CAST.REG[name], S = document.getElementById("S");
S.innerHTML = `<h1>${name}</h1><div class="sub">${spec.role || ""} · rig ${spec.rig || "modern"}</div>`;
const NS = "http://www.w3.org/2000/svg";
function cell(row, label, w, h, vb, cls) {
  const c = document.createElement("div"); c.className = "cell " + (cls || ""); row.appendChild(c);
  const svg = document.createElementNS(NS, "svg"); svg.setAttribute("width", w); svg.setAttribute("height", h); svg.setAttribute("viewBox", vb); c.appendChild(svg);
  const t = document.createElement("span"); t.textContent = label; c.appendChild(t); return svg;
}
const rowA = document.createElement("div"); rowA.className = "row"; S.appendChild(rowA);
const rowB = document.createElement("div"); rowB.className = "row"; S.appendChild(rowB);
if ((spec.rig || "modern") === "modern") {
  ["ECU", "CU", "MCU", "MS", "WS"].forEach((f) => { const svg = cell(rowA, f, 270, 480, "0 0 1080 1920"); const r = CAST.build(name, svg); CAST.frame(r, f);
    const z = document.createElementNS(NS, "rect"); z.setAttribute("x", 0); z.setAttribute("y", 1500); z.setAttribute("width", 1080); z.setAttribute("height", 420); z.setAttribute("fill", "rgba(214,62,42,.18)"); svg.appendChild(z); });
  CAST.EXPRESSIONS.forEach((m) => { const svg = cell(rowB, m, 170, 200, "-170 -360 340 400"); const r = CAST.build(name, svg); const tl = gsap.timeline({ paused: true }); CAST.emote(tl, r, m, 0, 0.01); tl.progress(1); });
  [["phone at ear", "ear"], ["phone hold", "hold"], ["look left", -1], ["look right", 1]].forEach(([lab, v]) => { const svg = cell(rowB, lab, 170, 200, "-200 -360 400 470"); const r = CAST.build(name, svg); const tl = gsap.timeline({ paused: true });
    if (typeof v === "string") CAST.phone(tl, r, v, 0); else CAST.look(tl, r, v, 0, 0.01); tl.progress(1); });
} else {
  const poses = { m_elephant: [["rest", null], ["trunk raised", (tl, r) => CAST.trunk(tl, r, "raise", 0, 0.01)], ["trunk curled", (tl, r) => CAST.trunk(tl, r, "curl", 0, 0.01)], ["facing left", "flip"]],
                  m_crocodile: [["rest", null], ["jaw open", (tl, r) => CAST.jaw(tl, r, true, 0, 0.01)], ["facing left", "flip"]] }[spec.rig] || [["rest", null], ["facing left", "flip"]];
  poses.forEach(([lab, fn]) => { const svg = cell(rowA, lab, 380, 380, "-560 -1000 1120 1120", "m"); const r = CAST.build(name, svg, fn === "flip" ? { flip: !spec.flip } : {});
    if (typeof fn === "function") { const tl = gsap.timeline({ paused: true }); fn(tl, r); tl.progress(1); } });
}
document.body.dataset.ready = 1;
</script></body></html>"""


async def render(names, reg, out):
    from playwright.async_api import async_playwright
    out.mkdir(parents=True, exist_ok=True)
    files = []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1510, "height": 1200})
        msgs = []
        pg.on("pageerror", lambda e: msgs.append(str(e)))
        for n in names:
            html = PAGE % {"font": (KIT / "fonts").as_uri() + "/anek-latin-var.ttf", "gsap": (KIT / "vendor/gsap.min.js").as_uri(),
                           "cast": (KIT / "cast.js").as_uri(), "reg": json.dumps(reg), "name": json.dumps(n)}
            tmp = out / f"_{n}.html"; tmp.write_text(html)
            msgs.clear()
            await pg.goto(tmp.as_uri()); await pg.wait_for_timeout(300)
            if msgs:
                print(f"ERROR {n}: {msgs[0]}"); continue
            f = out / f"{n}.png"
            await pg.locator("#S").screenshot(path=str(f)); tmp.unlink(); files.append(f)
            print("sheet:", f)
        await b.close()
    return files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry"); ap.add_argument("--extra", help="extra JSON {characters:{...}} merged over the registry")
    ap.add_argument("--names"); ap.add_argument("--out", default="cast_sheets")
    a = ap.parse_args()
    reg = json.loads(pathlib.Path(a.registry or find_registry()).read_text())["characters"]
    if a.extra:
        reg.update(json.loads(pathlib.Path(a.extra).read_text()).get("characters", {}))
    names = a.names.split(",") if a.names else list(reg)
    missing = [n for n in names if n not in reg]
    if missing:
        sys.exit(f"not in registry: {missing}")
    files = asyncio.run(render(names, {"characters": reg}, pathlib.Path(a.out).resolve()))
    if len(files) > 1:
        from PIL import Image
        ims = [Image.open(f) for f in files]
        W = max(i.width for i in ims); H = sum(i.height for i in ims)
        sheet = Image.new("RGB", (W, H), (16, 14, 23)); y = 0
        for i in ims:
            sheet.paste(i, (0, y)); y += i.height
        sheet.save(pathlib.Path(a.out) / "cast_overview.png"); print("overview:", pathlib.Path(a.out) / "cast_overview.png")


if __name__ == "__main__":
    main()
