#!/usr/bin/env python3
"""Assemble the HyperFrames workspace for a SutraVerse video.

Hand-authored (atelier) scene art lives in projects/<id>/composition/src/:
    scenes.html   <section class="clip sv-scene" data-scene="S1"> … </section> per scene
    scenes.css    scene styling (use brand tokens from brand.css)
    scenes.js     window.SV_BUILD_SCENES = function (tl, T) { … }   // tweens at GLOBAL time
This script wraps them with the brand system — opening identity, watermark, English
captions from timing.json, end card, narration audio — and writes a lint-clean
standalone composition to projects/<id>/composition/index.html.

Re-run it whenever timing.json or src/* change; never hand-edit index.html.
Usage: python build_composition.py <project_id>
"""
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import SKILL_DIR, has_devanagari, load_config, project_dir, read_json  # noqa: E402

KIT = SKILL_DIR / "brand-kit"
OVERLAP = 0.45  # scene crossfade overlap (seconds) on each side


def logo(suffix: str) -> str:
    svg = (KIT / "logo.svg").read_text(encoding="utf-8")
    return svg.replace('id="svGold"', f'id="svGold-{suffix}"').replace("url(#svGold)", f"url(#svGold-{suffix})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project_id")
    a = ap.parse_args()
    cfg = load_config()
    brand = cfg["brand"]
    pdir = project_dir(a.project_id)
    T = read_json(pdir / "artifacts" / "timing.json")
    fmt_key = T["format"]
    fmt = cfg["formats"][fmt_key]
    W, H = T["width"], T["height"]
    u = min(W, H) / 1080.0
    total = T["total_duration"]
    comp = pdir / "composition"
    src = comp / "src"
    for f in ("scenes.html", "scenes.css", "scenes.js"):
        if not (src / f).is_file():
            sys.exit(f"Missing {src / f}. Author the scenes first (see references/visual-direction.md).")

    # --- copy brand kit + media into the workspace ---
    for name in ("brand.css", "sv-lib.js", "characters.js"):
        shutil.copy2(KIT / name, comp / name)
    shutil.copy2(KIT / "vendor" / "gsap.min.js", comp / "gsap.min.js")
    shutil.copytree(KIT / "fonts", comp / "fonts", dirs_exist_ok=True)
    (comp / "assets").mkdir(exist_ok=True)
    shutil.copy2(pdir / "assets" / "audio" / "narration.wav", comp / "assets" / "narration.wav")
    if (src / "assets").is_dir():
        shutil.copytree(src / "assets", comp / "assets", dirs_exist_ok=True)

    # --- scenes: inject timing attributes ---
    scenes_html = (src / "scenes.html").read_text(encoding="utf-8")
    missing = [s for s in T["scenes"] if f'data-scene="{s}"' not in scenes_html]
    if missing:
        sys.exit(f"scenes.html has no section for scene(s): {missing}")

    def attrs(m):
        sid = m.group(1)
        sc = T["scenes"][sid]
        start = max(0.0, sc["start"] - OVERLAP)
        end = min(T["end_card"]["start"] + OVERLAP, sc["end"] + OVERLAP)
        return f'data-scene="{sid}" id="scene-{sid}" data-start="{start:.3f}" data-duration="{end - start:.3f}" data-track-index="2" data-layout-allow-occlusion'

    scenes_html = re.sub(r'data-scene="([A-Za-z0-9_-]+)"', attrs, scenes_html)
    # optional root-level media (generated video clips must be direct children of the root)
    media_html = (src / "media.html").read_text(encoding="utf-8") if (src / "media.html").is_file() else ""

    # --- on-screen language guard: no Devanagari outside an explicit verified verse block ---
    if has_devanagari(scenes_html):
        sys.exit("On-screen language rule: Devanagari found in scenes.html. Sanskrit verses go in sv_script.json "
                 "line['shloka'] (verified, with a source) and are rendered by this builder; scene text is English only.")

    intro_mode = brand["intro"]["short_form" if fmt_key == "short" else "long_form"]
    intro_end = {"badge": 1.8, "overlay": 1.9}.get(intro_mode, 3.0)
    ec0, ec1 = T["end_card"]["start"], T["end_card"]["end"]

    script = read_json(pdir / "artifacts" / "sv_script.json")
    sources_txt = (pdir / "artifacts" / "sources.json").read_text(encoding="utf-8") if (pdir / "artifacts" / "sources.json").is_file() else ""
    lines_by_id = {l["id"]: l for l in T["lines"]}

    def word_time(line_id: str, token: str):
        ws = lines_by_id[line_id].get("words", [])
        n = 1
        if "#" in token:
            token, n = token.split("#")[0], int(token.split("#")[1])
        hits = [w for w in ws if w["w"] == token] or [w for w in ws if w["w"].startswith(token) or token.startswith(w["w"])]
        return hits[n - 1]["start"] if len(hits) >= n else None

    caps = []
    hl_count = 0
    for i, c in enumerate(T["captions"]):
        if has_devanagari(c["text"]):
            sys.exit(f"Caption {i} contains Devanagari — subtitles must be English.")
        body = html.escape(c["text"])
        # word-synced emphasis: the English word lights up exactly when its Hindi counterpart is spoken
        for sy in lines_by_id[c["line"]].get("sync", []):
            t_hl = word_time(c["line"], sy["hi"])
            en = html.escape(sy["en"])
            if t_hl is None or not (c["start"] - 0.05 <= t_hl <= c["end"]):
                continue
            pat = re.compile(r"(?<![\w>])(" + re.escape(en) + r")(?![\w<])", re.I)
            if pat.search(body):
                body = pat.sub(lambda m: f'<span class="sv-hl" data-t="{t_hl:.3f}">{m.group(1)}</span>', body, count=1)
                hl_count += 1
        caps.append(
            f'<div class="clip sv-cap{" sv-long" if fmt_key == "long" else ""}" id="cap-{i}" data-start="{c["start"]:.3f}" '
            f'data-duration="{c["end"] - c["start"]:.3f}" data-track-index="8"><p>{body}</p></div>'
        )

    # verified shloka cards: Devanagari + IAST, each word lit as it is recited; reference chip
    shlokas = []
    for sl in script["lines"]:
        sh = sl.get("shloka")
        if not sh:
            continue
        if sl.get("claim_type") != "direct_quote" or not sl.get("source_ref") or sl["source_ref"].split(",")[0] not in sources_txt:
            sys.exit(f"{sl['id']}: a shloka needs claim_type=direct_quote and a source_ref listed in artifacts/sources.json")
        tl_line = lines_by_id[sl["id"]]
        deva, iast = sh["deva"].split(), sh["iast"].split()
        ws = tl_line.get("words", [])
        def times(n):
            if len(ws) == n:
                return [w["start"] for w in ws]
            s0, e0 = tl_line["start"], tl_line["end"]
            return [s0 + (e0 - s0) * k / n for k in range(n)]
        td, ti = times(len(deva)), times(len(iast))
        start = tl_line["start"] - 0.35
        nxt = [l for l in T["lines"] if l["start"] > tl_line["start"]]
        end = (nxt[0]["start"] - 0.05) if nxt else tl_line["end"] + 0.8
        end = max(end, tl_line["end"] + 0.5)
        pos = sh.get("pos", "top")
        dv = " ".join(f'<span class="sv-sw" data-t="{t:.3f}">{html.escape(w)}</span>' for w, t in zip(deva, td))
        iv = " ".join(f'<span class="sv-sw" data-t="{t:.3f}">{html.escape(w)}</span>' for w, t in zip(iast, ti))
        who = f'<div class="sv-shloka-who">{html.escape(sh["speaker"])} says</div>' if sh.get("speaker") else ""
        shlokas.append(
            f'<div class="clip sv-shloka sv-shloka-{pos}" id="shl-{sl["id"]}" data-start="{start:.3f}" data-duration="{end - start:.3f}" data-track-index="5">'
            f'{who}<div class="sv-sanskrit">{dv}</div><div class="sv-iast">{iv}</div>'
            f'<div class="sv-shloka-ref">{html.escape(sh["ref"])}</div></div>'
        )

    sting_cls = {"sting": " sv-sting", "badge": " sv-badge"}.get(intro_mode, "")
    intro = (f'<div class="clip sv-intro{sting_cls}" id="sv-intro" data-start="0" data-duration="{intro_end + 0.2:.2f}" data-track-index="7">'
             f'{logo("intro")}<div class="sv-word" id="sv-intro-word">{html.escape(brand["name"].upper())}</div>'
             f'<div class="sv-tag" id="sv-intro-tag">{html.escape(brand["tagline"])}</div></div>')
    wm = (f'<div class="clip sv-watermark" id="sv-wm" data-start="{intro_end - 0.3:.2f}" data-duration="{ec0 - intro_end + 0.3:.2f}" data-track-index="9">'
          f'{logo("wm")}<span>{html.escape(brand["name"].upper())}</span></div>') if brand["watermark"]["enabled"] else ""
    handle = f'<div class="sv-handle" id="sv-end-handle">{html.escape(brand["handle"])}</div>' if brand.get("handle") else ""
    cta = T.get("cta") or read_json(pdir / "artifacts" / "sv_script.json").get("cta") or brand["cta_default"]
    end = (f'<div class="clip sv-end" id="sv-end" data-start="{ec0 - 0.5:.3f}" data-duration="{ec1 - ec0 + 0.5:.3f}" data-track-index="6">'
           f'{logo("end")}<div class="sv-word" id="sv-end-word">{html.escape(brand["name"].upper())}</div><div class="sv-rule" id="sv-end-rule"></div>'
           f'<div class="sv-tag" id="sv-end-tag">{html.escape(brand["tagline"])}</div><div class="sv-cta" id="sv-end-cta">{html.escape(cta)}</div>{handle}</div>')

    music = ""
    bed = pdir / "assets" / "music" / "bed.wav"
    if bed.is_file():
        shutil.copy2(bed, comp / "assets" / "bed.wav")
        music = (f'<audio id="sv-bed" src="assets/bed.wav" data-start="0" data-duration="{total:.3f}" '
                 f'data-track-index="11" data-volume="0.35"></audio>')

    tjs = {
        "W": W, "H": H, "u": u, "total": total, "introEnd": intro_end,
        "scenes": T["scenes"],
        "lines": {l["id"]: {"start": l["start"], "end": l["end"], "phrases": l.get("phrases", []), "words": l.get("words", [])} for l in T["lines"]},
        "endCard": T["end_card"], "safe": fmt["safe_area"],
    }
    wm_op = brand["watermark"]["opacity"]
    sa = fmt["safe_area"]
    grain = ("<svg class='sv-grain' width='100%' height='100%'><filter id='svNoise'><feTurbulence type='fractalNoise' "
             "baseFrequency='.9' numOctaves='2' seed='7'/><feColorMatrix values='0 0 0 0 .9  0 0 0 0 .8  0 0 0 0 .6  0 0 0 .9 0'/></filter>"
             "<rect width='100%' height='100%' filter='url(#svNoise)'/></svg>")

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={W}, height={H}" />
<title>{html.escape(T.get('project_id', 'SutraVerse'))}</title>
<script src="gsap.min.js"></script>
<script src="sv-lib.js"></script>
<script src="characters.js"></script>
<link rel="stylesheet" href="brand.css" />
<style>
:root {{ --sv-w: {W}px; --sv-h: {H}px; --sv-u: {u:.4f}px; --sv-safe-top: {sa['top']}px; --sv-safe-bottom: {sa['bottom']}px; --sv-safe-side: {sa['side']}px; }}
.sv-scene {{ position: absolute; inset: 0; overflow: hidden; }}
</style>
<link rel="stylesheet" href="scenes.css" />
</head>
<body>
<div id="root" data-composition-id="main" data-width="{W}" data-height="{H}" data-duration="{total:.3f}">
<div class="sv-fill" id="sv-base"><div class="sv-sky"></div>{grain}</div>
{media_html}
{scenes_html}
{intro}
{wm}
{chr(10).join(shlokas)}
{chr(10).join(caps)}
{end}
<audio id="sv-narration" src="assets/narration.wav" data-start="0" data-duration="{total:.3f}" data-track-index="10" data-volume="1"></audio>
{music}
</div>
<script>window.SV_T = {json.dumps(tjs)};</script>
<script src="scenes.js"></script>
<script>
(function () {{
  const T = window.SV_T;
  window.__timelines = window.__timelines || {{}};
  const tl = gsap.timeline({{ paused: true }});
  // ---- opening identity ----
  const intro = document.getElementById("sv-intro");
  const badge = intro.classList.contains("sv-badge");
  // badge (short-form default): already on screen at frame 0, small, never competes with the hook
  const k = badge ? 0.5 : 1;
  SV.drawOn(tl, intro.querySelectorAll(".sv-thread"), 0.0, {{ dur: 0.9 * k }});
  SV.drawOn(tl, intro.querySelectorAll(".sv-petal, .sv-base"), 0.25 * k, {{ dur: 0.7 * k, stagger: 0.06 }});
  tl.fromTo(intro.querySelector(".sv-bindu"), {{ opacity: 0, scale: 0.2, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }}, 0.7 * k);
  tl.fromTo("#sv-intro-word", {{ opacity: badge ? 0.35 : 0, y: badge ? 0 : 18 * T.u, scale: badge ? 1 : 1.12 }}, {{ opacity: 1, y: 0, scale: 1, duration: badge ? 0.4 : 0.8, ease: "power3.out" }}, badge ? 0 : 0.25);
  tl.fromTo("#sv-intro-tag", {{ opacity: badge ? 0.3 : 0 }}, {{ opacity: 0.9, duration: 0.5 }}, badge ? 0.1 : 0.6);
  tl.to(intro, {{ opacity: 0, y: -20 * T.u, duration: 0.45, ease: "power2.in" }}, T.introEnd - 0.4);
  // ---- watermark ----
  const wm = document.getElementById("sv-wm");
  if (wm) {{
    tl.fromTo(wm, {{ opacity: 0 }}, {{ opacity: {wm_op}, duration: 0.6 }}, T.introEnd - 0.3);
    tl.to(wm, {{ opacity: 0, duration: 0.4 }}, T.endCard.start - 0.5);
  }}
  // ---- captions ----
  document.querySelectorAll(".sv-cap").forEach((el) => {{
    const s = parseFloat(el.dataset.start), d = parseFloat(el.dataset.duration);
    tl.fromTo(el.firstElementChild, {{ opacity: 0, y: 10 * T.u }}, {{ opacity: 1, y: 0, duration: 0.14, ease: "power2.out" }}, s);
    tl.to(el.firstElementChild, {{ opacity: 0, duration: 0.1 }}, s + d - 0.1);
  }});
  // ---- word-synced caption emphasis ----
  document.querySelectorAll(".sv-hl").forEach((sp) => {{
    const t = parseFloat(sp.dataset.t);
    tl.fromTo(sp, {{ color: "#F4EADB", backgroundColor: "rgba(242,179,61,0)" }}, {{ color: "#100E17", backgroundColor: "rgba(242,179,61,1)", duration: 0.08 }}, t);
    tl.fromTo(sp, {{ scale: 1 }}, {{ scale: 1.12, duration: 0.1, yoyo: true, repeat: 1, ease: "power2.out" }}, t);
  }});
  // ---- shloka cards: slide in, light each word as it is recited ----
  document.querySelectorAll(".sv-shloka").forEach((card) => {{
    const s = parseFloat(card.dataset.start), d = parseFloat(card.dataset.duration);
    tl.fromTo(card, {{ opacity: 0, y: -30 * T.u, scale: 0.94 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.35, ease: "back.out(1.8)" }}, s);
    tl.to(card, {{ opacity: 0, y: -16 * T.u, duration: 0.25 }}, s + d - 0.25);
    card.querySelectorAll(".sv-sw").forEach((w) => {{
      const t = parseFloat(w.dataset.t);
      tl.fromTo(w, {{ color: "rgba(16,14,23,.38)" }}, {{ color: "#D63E2A", duration: 0.12 }}, t);
      tl.to(w, {{ color: "#100E17", duration: 0.35 }}, t + 0.45);
      tl.fromTo(w, {{ y: 0 }}, {{ y: -6 * T.u, duration: 0.12, yoyo: true, repeat: 1 }}, t);
    }});
  }});
  // ---- scenes (hand-authored) ----
  if (typeof window.SV_BUILD_SCENES === "function") window.SV_BUILD_SCENES(tl, T);
  // ---- end card ----
  const e0 = T.endCard.start;
  tl.fromTo("#sv-end", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5, ease: "sine.out" }}, e0 - 0.5);
  const end = document.getElementById("sv-end");
  SV.drawOn(tl, end.querySelectorAll(".sv-thread"), e0 - 0.2, {{ dur: 1.0 }});
  SV.drawOn(tl, end.querySelectorAll(".sv-petal, .sv-base"), e0, {{ dur: 0.8, stagger: 0.06 }});
  tl.fromTo(end.querySelector(".sv-bindu"), {{ opacity: 0, scale: 0.2, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }}, e0 + 0.6);
  tl.fromTo("#sv-end-word", {{ opacity: 0, y: 24 * T.u }}, {{ opacity: 1, y: 0, duration: 0.7, ease: "power3.out" }}, e0 + 0.15);
  tl.fromTo("#sv-end-rule", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.7, ease: "power2.out" }}, e0 + 0.45);
  tl.fromTo("#sv-end-tag", {{ opacity: 0, y: 12 * T.u }}, {{ opacity: 1, y: 0, duration: 0.6 }}, e0 + 0.6);
  tl.fromTo("#sv-end-cta", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6 }}, e0 + 0.95);
  if (document.getElementById("sv-end-handle")) tl.fromTo("#sv-end-handle", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, e0 + 1.1);
  // keep timeline length == composition length
  tl.set({{}}, {{}}, T.total);
  window.__timelines["main"] = tl;
}})();
</script>
</body>
</html>
"""
    (comp / "index.html").write_text(page, encoding="utf-8")
    shutil.copy2(src / "scenes.css", comp / "scenes.css")
    shutil.copy2(src / "scenes.js", comp / "scenes.js")
    print(f"Composition written: {comp / 'index.html'}  ({W}x{H}, {total:.2f}s, {len(caps)} captions, "
          f"{hl_count} word-synced highlights, {len(shlokas)} shloka cards, intro={intro_mode})")


if __name__ == "__main__":
    main()
