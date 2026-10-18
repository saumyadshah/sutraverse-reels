#!/usr/bin/env python3
"""Quality gate on the ACTUAL rendered file — never on the plan.

Checks (each PASS / WARN / FAIL, written to projects/<id>/qa/qa_report.json):
  container   dimensions, fps, codec, duration vs timing, audio stream present
  loudness    integrated LUFS vs platform target, true peak <= -1 dBTP, no clipped samples
  speech      Whisper language-ID of the rendered audio == Hindi (per window)
  meaning     Whisper EN translation of each window vs the English subtitles (token overlap)
  audibility  speech-vs-bed level ratio (narration clearly above music)
  sync        cross-correlation of rendered audio vs narration track (offset ~ 0)
  subtitles   English only, inside duration, no overlaps, line length, reading speed
  on_screen   no Devanagari in rendered HTML text outside a verified .sv-sanskrit block
  branding    opening identity, watermark, end card text present; end-card frame is brand-coloured
  motion      every scene changes between its 25% and 75% frames (no static slides)
Also writes qa/contact_sheet.jpg (scene midpoints + intro + end card) for visual review.

Usage: python qa_check.py <project_id> [--whisper-dir ~/.openmontage/models/sherpa-onnx/sherpa-onnx-whisper-small]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import has_devanagari, load_config, project_dir, read_json, write_json  # noqa: E402

RES: list[dict] = []


def rec(check, status, detail):
    RES.append({"check": check, "status": status, "detail": detail})
    print(f"[{status:4}] {check:11} {detail}")


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def pcm(path, sr=16000, ss=None, t=None):
    cmd = ["ffmpeg", "-v", "error"]
    if ss is not None:
        cmd += ["-ss", f"{ss:.3f}"]
    if t is not None:
        cmd += ["-t", f"{t:.3f}"]
    cmd += ["-i", str(path), "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, dtype=np.float32)


def frame(video, t, out):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1", str(out)], check=True)
    return out


def tokens(s):
    stop = {"the", "a", "an", "of", "to", "and", "is", "in", "it", "that", "you", "your", "this", "for", "on", "with",
            "be", "are", "was", "but", "not", "at", "as", "by", "from", "or", "so", "then", "its", "have", "has", "do"}
    return {w for w in re.findall(r"[a-z']+", s.lower()) if w not in stop and len(w) > 2}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project_id")
    ap.add_argument("--whisper-dir", default=str(Path.home() / ".openmontage/models/sherpa-onnx/sherpa-onnx-whisper-small"))
    a = ap.parse_args()
    cfg = load_config()
    pdir = project_dir(a.project_id)
    T = read_json(pdir / "artifacts" / "timing.json")
    script = read_json(pdir / "artifacts" / "sv_script.json")
    fmt = cfg["formats"][T["format"]]
    video = pdir / "renders" / "final.mp4"
    qa = pdir / "qa"
    qa.mkdir(exist_ok=True)
    if not video.is_file():
        sys.exit(f"No render at {video}")

    # ---------- container ----------
    p = probe(video)
    v = next(s for s in p["streams"] if s["codec_type"] == "video")
    aud = [s for s in p["streams"] if s["codec_type"] == "audio"]
    fps = eval(v["r_frame_rate"])  # e.g. "30/1"
    dur = float(p["format"]["duration"])
    ok = v["width"] == fmt["width"] and v["height"] == fmt["height"] and abs(fps - fmt["fps"]) < 0.01
    rec("container", "PASS" if ok else "FAIL", f"{v['width']}x{v['height']} @ {fps:g}fps {v['codec_name']} (want {fmt['width']}x{fmt['height']} @ {fmt['fps']})")
    rec("duration", "PASS" if abs(dur - T["total_duration"]) < 0.25 else "FAIL", f"{dur:.2f}s rendered vs {T['total_duration']:.2f}s planned")
    if not aud:
        rec("audio", "FAIL", "no audio stream")
    else:
        rec("audio", "PASS", f"{aud[0]['codec_name']} {aud[0]['sample_rate']}Hz {aud[0]['channels']}ch lang={aud[0].get('tags', {}).get('language', '?')}")

    # ---------- loudness / peaks ----------
    eb = subprocess.run(["ffmpeg", "-nostats", "-i", str(video), "-af", "ebur128=peak=true", "-f", "null", "-"],
                        capture_output=True, text=True).stderr
    I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", eb)[-1])
    TP = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", eb)[-1])
    tgt = fmt["loudness_lufs"]
    rec("loudness", "PASS" if abs(I - tgt) <= 1.5 else "WARN", f"integrated {I:.1f} LUFS (target {tgt})")
    rec("true_peak", "PASS" if TP <= -0.9 else "FAIL", f"{TP:.1f} dBTP (limit -1.0)")
    full = pcm(video, 48000)
    clipped = int(np.sum(np.abs(full) >= 0.999))
    rec("clipping", "PASS" if clipped == 0 else "FAIL", f"{clipped} clipped samples")

    # ---------- audibility: speech windows vs bed-only windows ----------
    sr = 48000

    def rms_db(x):
        return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)

    speech = np.concatenate([full[int(l["start"] * sr):int(l["end"] * sr)] for l in T["lines"]])
    gaps = []
    for l1, l2 in zip(T["lines"], T["lines"][1:]):
        if l2["start"] - l1["end"] > 0.25:
            gaps.append(full[int((l1["end"] + 0.12) * sr):int((l2["start"] - 0.05) * sr)])
    if gaps:
        ratio = rms_db(speech) - rms_db(np.concatenate(gaps))
        rec("audibility", "PASS" if ratio >= 12 else ("WARN" if ratio >= 8 else "FAIL"),
            f"speech is {ratio:.1f} dB above the music bed in pauses (want >= 12)")

    # ---------- sync: rendered audio vs narration track ----------
    nar = pcm(pdir / "assets" / "audio" / "narration.wav", 16000, 0, 20)
    ren = pcm(video, 16000, 0, 20)
    n = min(len(nar), len(ren))
    env = lambda x: np.convolve(np.abs(x[:n]), np.ones(160) / 160, mode="same")
    e1, e2 = env(nar), env(ren)
    e1, e2 = e1 - e1.mean(), e2 - e2.mean()
    lags = range(-1600, 1601, 16)
    lag = max(lags, key=lambda L: float(np.dot(e1[max(0, L):n + min(0, L)], e2[max(0, -L):n - max(0, L)])))
    rec("sync", "PASS" if abs(lag) <= 640 else "FAIL", f"audio offset {lag / 16:.0f} ms vs narration track")

    # ---------- Hindi speech + meaning (Whisper) ----------
    wd = Path(a.whisper_dir).expanduser()
    if (wd / "small-encoder.onnx").is_file():
        import sherpa_onnx

        def recog(lang, task):
            return sherpa_onnx.OfflineRecognizer.from_whisper(
                encoder=str(wd / "small-encoder.onnx"), decoder=str(wd / "small-decoder.onnx"),
                tokens=str(wd / "small-tokens.txt"), language=lang, task=task, num_threads=2)

        lid, tr = recog("", "transcribe"), recog("hi", "translate")
        windows, cur = [], []
        for l in T["lines"]:
            if cur and l["end"] - cur[0]["start"] > 26:
                windows.append(cur)
                cur = []
            cur.append(l)
        if cur:
            windows.append(cur)
        langs, overlaps, rows = [], [], []
        for w in windows:
            s0, s1 = max(0, w[0]["start"] - 0.1), w[-1]["end"] + 0.2
            x = pcm(video, 16000, s0, s1 - s0)
            st = lid.create_stream(); st.accept_waveform(16000, x); lid.decode_stream(st)
            st2 = tr.create_stream(); st2.accept_waveform(16000, x); tr.decode_stream(st2)
            lang = getattr(st.result, "lang", "") or ""
            heard = st2.result.text.strip()
            ref = " ".join(l["en"] for l in w)
            tk_ref, tk_heard = tokens(ref), tokens(heard)
            ov = len(tk_ref & tk_heard) / max(1, len(tk_ref))
            langs.append(lang)
            overlaps.append(ov)
            rows.append({"window": f"{s0:.1f}-{s1:.1f}s", "detected_language": lang, "whisper_translation": heard,
                         "subtitle_text": ref, "keyword_overlap": round(ov, 2)})
        write_json(qa / "speech_check.json", rows)
        hi_share = sum(1 for x in langs if "hi" in x) / len(langs)
        rec("speech_lang", "PASS" if hi_share == 1 else "FAIL", f"Hindi detected in {hi_share:.0%} of {len(langs)} windows ({langs})")
        mo = float(np.mean(overlaps))
        rec("meaning", "PASS" if mo >= 0.35 else "WARN",
            f"mean keyword overlap Whisper-EN vs subtitles {mo:.2f} (see qa/speech_check.json; listen if WARN)")
    else:
        rec("speech_lang", "WARN", f"Whisper model not found at {wd}; language not machine-verified — listen manually")

    # ---------- subtitles ----------
    srt = (pdir / "renders" / "final.en.srt").read_text(encoding="utf-8")
    caps = T["captions"]
    issues = []
    if has_devanagari(srt):
        issues.append("Devanagari in .srt")
    for i, c in enumerate(caps):
        if c["start"] < 0 or c["end"] > dur + 0.05:
            issues.append(f"cue {i} outside video")
        if i and c["start"] < caps[i - 1]["end"] - 0.01:
            issues.append(f"cue {i} overlaps previous")
        for line in c["text"].split("\n"):
            if len(line) > fmt["caption_max_chars_per_line"] + 4:
                issues.append(f"cue {i} line too long ({len(line)})")
        cps = len(c["text"].replace("\n", " ")) / max(0.01, c["end"] - c["start"])
        if cps > 21:
            issues.append(f"cue {i} reading speed {cps:.0f} cps")
    hard = [x for x in issues if "Devanagari" in x or "outside" in x or "overlaps" in x]
    rec("subtitles", "FAIL" if hard else ("WARN" if issues else "PASS"), f"{len(caps)} English cues; " + ("; ".join(issues[:6]) or "clean"))

    # ---------- on-screen text ----------
    page = (pdir / "composition" / "index.html").read_text(encoding="utf-8")
    body = re.sub(r"<script.*?</script>|<style.*?</style>", "", page, flags=re.S)
    # Devanagari is allowed ONLY as the words of a verified shloka (sv_script line.shloka.deva, direct_quote + source_ref)
    allowed = set()
    for l in script.get("lines", []):
        sh = l.get("shloka")
        if sh and l.get("claim_type") == "direct_quote" and l.get("source_ref"):
            allowed.update(re.findall(r"[ऀ-ॿ]+", sh.get("deva", "")))
    text_only = re.sub(r"<[^>]+>", " ", body)
    stray = [w for w in re.findall(r"[ऀ-ॿ]+", text_only) if w not in allowed and w not in "।॥"]
    n_shl = len(re.findall(r'class="clip sv-shloka ', body))
    rec("on_screen", "FAIL" if stray else "PASS",
        f"English everywhere; Devanagari only in {n_shl} verified shloka card(s)" if not stray else f"unverified Devanagari on screen: {' '.join(stray[:6])}")

    # ---------- word sync (narration words ↔ timeline) ----------
    probs, nw = [], 0
    for l in T["lines"]:
        ws = l.get("words") or []
        nw += len(ws)
        if not ws:
            probs.append(f"{l['id']} has no word timings"); continue
        if ws[0]["start"] < l["start"] - 0.05 or ws[-1]["end"] > l["end"] + 0.05:
            probs.append(f"{l['id']} words spill outside the line")
        back = sum(1 for a, b2 in zip(ws, ws[1:]) if b2["start"] < a["start"] - 0.08)
        if back:
            probs.append(f"{l['id']} {back} non-monotonic word(s)")
        short = sum(1 for w in ws if w["end"] - w["start"] < 0.04)
        if short > max(1, len(ws) // 4):
            probs.append(f"{l['id']} {short} squeezed word(s)")
    rec("word_sync", "WARN" if probs else "PASS", f"{nw} words timed; " + ("; ".join(probs[:6]) or "monotonic, inside their lines"))

    # ---------- branding ----------
    b = cfg["brand"]
    need = {"opening": 'id="sv-intro"', "watermark": 'id="sv-wm"', "end card": 'id="sv-end"'}
    miss = [k for k, s in need.items() if s not in page]
    if b["tagline"] not in page or b["name"].upper() not in page:
        miss.append("brand text")
    ef = frame(video, T["end_card"]["start"] + 1.6, qa / "endcard.png")
    from PIL import Image

    im = np.asarray(Image.open(ef).convert("RGB")).astype(int)
    gold = np.mean((im[..., 0] > 150) & (im[..., 1] > 110) & (im[..., 2] < 140) & (im[..., 0] - im[..., 2] > 60))
    rec("branding", "PASS" if not miss and gold > 0.002 else "FAIL",
        f"missing: {miss or 'none'}; end-card gold coverage {gold:.2%}")

    # ---------- motion per scene + contact sheet ----------
    shots, static = [], []
    for sid, sc in T["scenes"].items():
        d = sc["end"] - sc["start"]
        f1 = frame(video, sc["start"] + d * 0.25, qa / f"{sid}_a.png")
        f2 = frame(video, sc["start"] + d * 0.75, qa / f"{sid}_b.png")
        x1 = np.asarray(Image.open(f1).convert("L").resize((270, 480 if T["height"] > T["width"] else 152))).astype(float)
        x2 = np.asarray(Image.open(f2).convert("L").resize(x1.shape[::-1])).astype(float)
        if np.mean(np.abs(x1 - x2)) < 1.5:
            static.append(sid)
        shots.append((sid, frame(video, sc["start"] + d * 0.5, qa / f"{sid}_mid.png")))
    rec("motion", "PASS" if not static else "WARN", f"static-looking scenes: {static or 'none'}")
    # ---------- hook & cadence (virality rules, see references/engagement.md) ----------
    def gray(t, name):
        f = frame(video, t, qa / name)
        return np.asarray(Image.open(f).convert("L").resize((216, 384) if T["height"] > T["width"] else (384, 216))).astype(float)
    g0, g05 = gray(0.0, "hook_0.0.png"), gray(0.5, "hook_0.5.png")
    first_word = T["lines"][0]["start"]
    moving = float(np.mean(np.abs(g0 - g05)))
    hook_ok = moving >= 2.0 and first_word <= 0.5
    rec("hook", "PASS" if hook_ok else "WARN",
        f"frame 0→0.5 s change {moving:.1f} (want ≥2, i.e. moving on frame 0); first word at {first_word:.2f}s (want ≤0.5)")
    still = []
    for prev, cur in zip(T["lines"], T["lines"][1:]):
        a0 = gray(max(0, prev["start"] + 0.2), "_a.png")
        b0 = gray(cur["start"] + 0.6, "_b.png")
        if np.mean(np.abs(a0 - b0)) < 2.0:
            still.append(cur["id"])
    rec("cadence", "PASS" if not still else "WARN",
        f"lines whose start brings no visible change: {still or 'none'} (every spoken line should change the picture)")
    shots = [("intro", frame(video, 1.0, qa / "intro.png"))] + shots + [("end", ef)]
    tw = 270 if T["height"] > T["width"] else 480
    th = int(tw * T["height"] / T["width"])
    cols = 6 if T["height"] > T["width"] else 4
    rows_n = -(-len(shots) // cols)
    sheet = Image.new("RGB", (cols * tw, rows_n * th), (8, 10, 20))
    for i, (_, f) in enumerate(shots):
        sheet.paste(Image.open(f).convert("RGB").resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
    sheet.save(qa / "contact_sheet.jpg", quality=88)

    fails = [r for r in RES if r["status"] == "FAIL"]
    warns = [r for r in RES if r["status"] == "WARN"]
    verdict = "FAIL" if fails else ("PASS_WITH_WARNINGS" if warns else "PASS")
    write_json(qa / "qa_report.json", {"video": str(video), "verdict": verdict, "checks": RES})
    print(f"\nVERDICT: {verdict}  ({len(fails)} fail, {len(warns)} warn) — contact sheet: {qa / 'contact_sheet.jpg'}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
