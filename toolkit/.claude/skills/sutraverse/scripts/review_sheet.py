#!/usr/bin/env python3
"""Build the sheets for the final review of a rendered Reel (CONTENT_STANDARDS §17).

  python review_sheet.py <project_id>        # needs renders/final.mp4 and artifacts/shotlist.json

qa/review_shots.jpg   one row per shot: frames at start / middle / end + id, time, purpose, cast
qa/review_cast.jpg    one row per character: the middle frame of every shot they appear in, next to
                      their model sheet cell, so face / hair / outfit / proportions can be compared
qa/review_strip.jpg   1 frame per second with time stamps (pacing, transitions, black frames)
"""
import json, pathlib, subprocess, sys, tempfile, textwrap

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _common import project_dir  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

FONT = HERE.parent / "brand-kit" / "fonts" / "anek-latin-var.ttf"
TW, TH = 216, 384


def font(n):
    try:
        return ImageFont.truetype(str(FONT), n)
    except Exception:
        return ImageFont.load_default()


def grab(video, t, tmp):
    out = pathlib.Path(tmp) / f"f_{t:08.3f}.png"
    if not out.exists():
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{max(0, t):.3f}", "-i", str(video), "-frames:v", "1",
                        "-vf", f"scale={TW}:{TH}", str(out)], check=True)
    return Image.open(out).convert("RGB")


def main():
    pid = sys.argv[1]
    pd = project_dir(pid); qa = pd / "qa"; qa.mkdir(exist_ok=True)
    video = pd / "renders" / "final.mp4"
    SL = json.loads((pd / "artifacts" / "shotlist.json").read_text())
    shots = SL["shots"]
    f1, f2 = font(22), font(18)
    with tempfile.TemporaryDirectory() as tmp:
        # shots sheet
        rows = []
        for s in shots:
            a, b = s["start"], s["end"]
            ims = [grab(video, t, tmp) for t in (a + 0.25, (a + b) / 2, b - 0.25)]
            row = Image.new("RGB", (3 * TW + 560, TH + 16), (16, 14, 23))
            for i, im in enumerate(ims):
                row.paste(im, (8 + i * (TW + 6), 8))
            d = ImageDraw.Draw(row); x = 3 * (TW + 6) + 20
            d.text((x, 12), f"{s['id']}  {a:.1f}-{b:.1f}s  {s.get('world', '')} · {s.get('size', '')} · in: {s.get('transition_in', 'cut')}", font=f1, fill=(242, 179, 61))
            y = 46
            for para in [s.get("purpose", ""), "SEE: " + s.get("key_visual", ""),
                         "CAST: " + ", ".join(f"{c['name']} ({c.get('expression', '-')}, {c.get('side', '-')})" for c in s.get("characters", [])),
                         "TEXT: " + " | ".join(s.get("text", []))]:
                for ln in textwrap.wrap(para, 52)[:4]:
                    d.text((x, y), ln, font=f2, fill=(244, 234, 219)); y += 24
                y += 8
            rows.append(row)
        sheet = Image.new("RGB", (rows[0].width, sum(r.height for r in rows)), (16, 14, 23)); y = 0
        for r in rows:
            sheet.paste(r, (0, y)); y += r.height
        sheet.save(qa / "review_shots.jpg", quality=86)

        # cast continuity sheet
        names = []
        for s in shots:
            for c in s.get("characters", []):
                if c["name"] not in names: names.append(c["name"])
        crow = []
        for n in names:
            appear = [s for s in shots if n in [c["name"] for c in s.get("characters", [])]]
            if not appear: continue
            row = Image.new("RGB", (8 + (len(appear) + 1) * (TW + 6), TH + 44), (16, 14, 23)); d = ImageDraw.Draw(row)
            d.text((8, 8), n.upper() + f"  ({len(appear)} shots)", font=f1, fill=(242, 179, 61))
            ms = qa / "cast" / f"{n}.png"
            if ms.exists():
                m = Image.open(ms).convert("RGB"); m.thumbnail((TW, TH)); row.paste(m, (8, 40))
            for i, s in enumerate(appear):
                row.paste(grab(video, (s["start"] + s["end"]) / 2, tmp), (8 + (i + 1) * (TW + 6), 40))
                d.text((10 + (i + 1) * (TW + 6), 44), s["id"], font=f2, fill=(242, 179, 61))
            crow.append(row)
        if crow:
            W = max(r.width for r in crow); sheet = Image.new("RGB", (W, sum(r.height for r in crow)), (16, 14, 23)); y = 0
            for r in crow:
                sheet.paste(r, (0, y)); y += r.height
            sheet.save(qa / "review_cast.jpg", quality=86)

        # 1 fps strip
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)], capture_output=True, text=True).stdout or 0)
        n = int(dur); cols = 10; sw, sh = 162, 288
        strip = Image.new("RGB", (cols * (sw + 4) + 4, ((n // cols) + 1) * (sh + 26) + 4), (16, 14, 23)); d = ImageDraw.Draw(strip)
        for k in range(n + 1):
            im = grab(video, min(k + 0.5, dur - 0.05), tmp).resize((sw, sh))
            x, y = 4 + (k % cols) * (sw + 4), 4 + (k // cols) * (sh + 26)
            strip.paste(im, (x, y)); d.text((x + 4, y + sh + 2), f"{k + 0.5:.1f}s", font=f2, fill=(244, 234, 219))
        strip.save(qa / "review_strip.jpg", quality=84)
    print("review sheets:", qa / "review_shots.jpg", qa / "review_cast.jpg", qa / "review_strip.jpg")


if __name__ == "__main__":
    main()
