#!/usr/bin/env python3
"""Layout + readability check on the composition itself, at real timeline positions (CONTENT_STANDARDS §17).

  python layout_check.py <project_id> [--step 0.5]
  python layout_check.py path/to/composition/index.html

Seeks window.__timelines.main every --step seconds and, for every VISIBLE text element, checks:
  size      effective font size >= 30 px at 1080 wide (subtitles and labels included)
  frame     fully inside the frame with >= 40 px side margin
  ui_zone   story text stays out of the bottom 420 px (Instagram/Shorts UI) and the top 120 px
            (subtitles .sv-cap and the end card are exempt; they are placed by the pipeline)
  overlap   no two text boxes overlap (> 6 % of the smaller one)
  contrast  WCAG contrast of the text colour against the pixels around it >= 4.5 (>= 3 for >= 60 px text)
  crowding  more than 3 separate text groups on screen at once (subtitle + 2) -> WARN
Writes qa/layout_report.json and qa/layout_<t>.png with red boxes on every failure.
"""
import argparse, asyncio, json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent

JS = r"""
() => {
  const W = 1080, H = 1920, out = [];
  const vis = (e) => { for (let n = e; n && n.nodeType === 1; n = n.parentElement) { const cs = getComputedStyle(n);
      if (cs.display === "none" || cs.visibility === "hidden" || parseFloat(cs.opacity) < 0.2) return false;
      const cp = cs.clipPath || ""; const m = cp.match(/inset\(([^)]*)\)/);
      if (m && m[1].split(/\s+/).some((v) => v.endsWith("%") && parseFloat(v) >= 99)) return false; } return true; };
  const solidBg = (e, r) => { for (let n = e, d = 0; n && d < 4; n = n.parentElement, d++) { const c = getComputedStyle(n).backgroundColor;
      const a = c.match(/rgba?\(([^)]*)\)/); if (!a) continue; const v = a[1].split(",").map(parseFloat); if (v.length === 4 && v[3] < 0.6) continue;
      const nr = n.getBoundingClientRect(); if (nr.width * nr.height > 6 * r.width * r.height) return null; return c; } return null; };
  const root = document.getElementById("root") || document.body; const rr = root.getBoundingClientRect(); const k = W / rr.width;
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  const seen = new Set();
  while (walker.nextNode()) {
    const t = walker.currentNode; if (!t.textContent.trim()) continue;
    const e = t.parentElement; if (!e) continue;
    const inSvg = !!e.closest("svg");
    // group by the nearest block-level ancestor so a line of spans is one box
    let blk = e; if (!inSvg) while (blk && blk !== root && getComputedStyle(blk).display.startsWith("inline")) blk = blk.parentElement;
    if (!blk || blk === root || seen.has(blk)) continue; seen.add(blk);
    if (!vis(blk)) continue;
    const rg = document.createRange(); rg.selectNodeContents(blk); const r = inSvg ? blk.getBoundingClientRect() : rg.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) continue;
    if (r.right < rr.left || r.left > rr.right || r.bottom < rr.top || r.top > rr.bottom) continue;
    const cs = getComputedStyle(e);
    let fs;
    if (inSvg) fs = r.height * k * 0.72;
    else { const lines = Math.max(1, Math.round(blk.offsetHeight / (parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.2)));
           const br = blk.getBoundingClientRect(); const scale = blk.offsetHeight ? br.height / blk.offsetHeight : 1; fs = parseFloat(cs.fontSize) * (isFinite(scale) && scale > 0 ? scale : 1) * k; }
    const cap = !!blk.closest(".sv-cap, .sv-end, #sv-end, .sv-intro, #sv-intro, .sv-wm, #sv-wm, .sv-shloka");
    const label = (blk.className && blk.className.baseVal === undefined ? blk.className : "") + "";
    out.push({ text: blk.innerText.trim().slice(0, 60), x: (r.left - rr.left) * k, y: (r.top - rr.top) * k, w: r.width * k, h: r.height * k,
      fs, color: cs.color, bg: inSvg ? null : solidBg(blk, r), exempt: cap, ex: !!blk.closest(".ex-stage"), cls: label.slice(0, 40) });
  }
  // faces (CAST rigs mark heads with data-face) must not sit under subtitles
  const caps = [...root.querySelectorAll(".sv-cap")].filter(vis).map((c) => (c.querySelector("p") || c).getBoundingClientRect());
  root.querySelectorAll("[data-face]").forEach((f) => { if (!vis(f)) return; const r = f.getBoundingClientRect(); if (r.width < 20) return;
    caps.forEach((c) => { const ix = Math.max(0, Math.min(r.right, c.right) - Math.max(r.left, c.left)), iy = Math.max(0, Math.min(r.bottom, c.bottom) - Math.max(r.top, c.top));
      if (ix * iy > 0.04 * r.width * r.height) out.push({ face: true, text: "face", x: (r.left - rr.left) * k, y: (r.top - rr.top) * k, w: r.width * k, h: r.height * k, fs: 99, color: "rgb(0,0,0)", exempt: true }); }); });
  return out;
}
"""


def lum(rgb):
    def ch(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb[:3]
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def parse_rgb(s):
    import re
    n = [float(x) for x in re.findall(r"[\d.]+", s)[:3]]
    return tuple(int(v) for v in n) if len(n) == 3 else (255, 255, 255)


async def run(index, step, outdir):
    from playwright.async_api import async_playwright
    from PIL import Image, ImageDraw
    import io, statistics
    report, bad_frames = [], {}
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.goto(index.as_uri()); await pg.wait_for_function("() => !!(window.__timelines && window.__timelines.main)", timeout=20000, polling=200)
        await pg.evaluate("document.fonts.ready.then(() => 1)"); await pg.wait_for_timeout(300)
        dur = await pg.evaluate("window.__timelines.main.duration()")
        t = 0.05
        while t < dur:
            await pg.evaluate(f"void window.__timelines.main.seek({t}, false)"); await pg.wait_for_timeout(40)
            boxes = await pg.evaluate(JS)
            png = await pg.screenshot(); img = Image.open(io.BytesIO(png)).convert("RGB")
            issues = []
            faces = [bx for bx in boxes if bx.get("face")]
            boxes = [bx for bx in boxes if not bx.get("face")]
            for bx in faces:
                issues.append(("FAIL", "face_cap", bx, "a subtitle covers a character's face: reframe (CAST.frame) or move the character up"))
            for bx in boxes:
                x, y, w, h = bx["x"], bx["y"], bx["w"], bx["h"]
                if bx["fs"] < 29.5:
                    issues.append(("FAIL", "size", bx, f"{bx['fs']:.0f}px text"))
                if x < 40 or y < 0 or x + w > 1040 or y + h > 1920:
                    issues.append(("FAIL", "frame", bx, "outside the frame / side margin"))
                if not bx["exempt"] and (y + h > 1500 or y < 120) and bx["fs"] < 200:
                    issues.append(("WARN" if y + h <= 1560 else "FAIL", "ui_zone", bx, f"text at y {y:.0f}-{y + h:.0f} (platform UI / subtitle zone)"))
                # contrast against a ring of pixels just outside the box
                ring = []
                for xx in range(int(max(0, x - 6)), int(min(1079, x + w + 6)), 6):
                    for yy in (int(max(0, y - 6)), int(min(1919, y + h + 6))):
                        ring.append(img.getpixel((xx, yy)))
                for yy in range(int(max(0, y)), int(min(1919, y + h)), 6):
                    for xx in (int(max(0, x - 6)), int(min(1079, x + w + 6))):
                        ring.append(img.getpixel((xx, yy)))
                if (ring or bx.get("bg")) and not bx["exempt"]:
                    bg = parse_rgb(bx["bg"]) if bx.get("bg") else tuple(int(statistics.median(c[i] for c in ring)) for i in range(3))
                    cr = contrast(parse_rgb(bx["color"]), bg)
                    need = 3.0 if bx["fs"] >= 60 else 4.5
                    if cr < need:
                        issues.append(("FAIL" if cr < need * 0.75 else "WARN", "contrast", bx, f"contrast {cr:.1f} (needs {need})"))
            for i in range(len(boxes)):
                for j in range(i + 1, len(boxes)):
                    a, c = boxes[i], boxes[j]
                    ix = max(0, min(a["x"] + a["w"], c["x"] + c["w"]) - max(a["x"], c["x"]))
                    iy = max(0, min(a["y"] + a["h"], c["y"] + c["h"]) - max(a["y"], c["y"]))
                    small = min(a["w"] * a["h"], c["w"] * c["h"])
                    contained = (ix * iy) >= 0.98 * small
                    if small and ix * iy > 0.06 * small and not contained:
                        issues.append(("FAIL", "overlap", a, f"overlaps '{c['text'][:24]}'"))
            groups = [bx for bx in boxes if not bx["exempt"] and not bx.get("ex")]
            if len(groups) > 3:
                issues.append(("WARN", "crowding", groups[0], f"{len(groups)} text groups on screen"))
            for lvl, kind, bx, msg in issues:
                report.append({"t": round(t, 2), "level": lvl, "check": kind, "text": bx["text"], "detail": msg})
            if any(i[0] == "FAIL" for i in issues):
                d = ImageDraw.Draw(img)
                for lvl, kind, bx, msg in issues:
                    d.rectangle([bx["x"], bx["y"], bx["x"] + bx["w"], bx["y"] + bx["h"]], outline=(255, 0, 0) if lvl == "FAIL" else (255, 170, 0), width=5)
                bad_frames[round(t, 2)] = img
            t += step
        await b.close()
    outdir.mkdir(parents=True, exist_ok=True)
    for tt, im in list(bad_frames.items())[:12]:
        im.resize((540, 960)).save(outdir / f"layout_{tt:06.2f}.png")
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target"); ap.add_argument("--step", type=float, default=0.5); ap.add_argument("--out")
    a = ap.parse_args()
    tp = pathlib.Path(a.target)
    if tp.suffix == ".html":
        index, qa = tp, pathlib.Path(a.out or tp.parent / "qa")
    else:
        sys.path.insert(0, str(HERE)); from _common import project_dir  # noqa
        pd = project_dir(a.target); index, qa = pd / "composition" / "index.html", pd / "qa"
    rep = asyncio.run(run(index.resolve(), a.step, qa))
    # collapse repeats of the same issue on the same text
    seen, rows = set(), []
    for r in rep:
        key = (r["check"], r["text"], r["level"])
        if key in seen: continue
        seen.add(key); rows.append(r)
    fails = [r for r in rows if r["level"] == "FAIL"]
    for r in rows:
        print(f"{r['level']:4} {r['t']:6.2f}s {r['check']:8} '{r['text'][:40]}'  {r['detail']}")
    (qa / "layout_report.json").write_text(json.dumps({"verdict": "FAIL" if fails else "PASS", "issues": rows}, indent=1))
    print(f"\nlayout: {len(fails)} FAIL, {len(rows) - len(fails)} WARN -> {'FAIL' if fails else 'PASS'}  (frames with failures: {qa}/layout_*.png)")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
