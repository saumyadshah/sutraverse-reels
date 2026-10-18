#!/usr/bin/env python3
"""Hindi narration + synchronized English subtitles from a SutraVerse bilingual script.

Input : projects/<id>/artifacts/sv_script.json   (see templates/sv_script.example.json)
Output: assets/audio/lines/<line>.wav           one clip per line (provenance kept)
        assets/audio/narration.wav              full narration, 48 kHz mono, placed on the video timeline
        artifacts/timing.json                   exact start/end per line, per scene, per caption cue
        assets/subtitles.en.srt / .vtt          English subtitles timed to the ACTUAL audio

Timing is measured from the synthesized audio, never estimated: each line is generated
separately, its real duration is measured, and lines are laid end-to-end with the configured
pauses. Subtitle cues are cut from those measured spans, so sync is exact at line level.

Voice routing follows config.voice.preference: the first AVAILABLE tool in the
OpenMontage registry wins (cloud neural voices when keys exist, local sherpa-onnx otherwise).
Usage:
  python narrate.py <project_id> [--voice-tool sherpa_onnx_tts --voice hi_rohan] [--speed 0.95]
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ROOT, fmt_ts, has_devanagari, load_config, project_dir, read_json, write_json  # noqa: E402

SR = 48000
STYLE_PROMPT = ""
TTS_MODEL = ""
TTS_FALLBACKS: list = []
RETAKE = False


def pick_voice(cfg: dict, tool_override: str | None, voice_override: str | None):
    from tools.base_tool import ToolStatus
    from tools.tool_registry import registry

    registry.discover()
    prefs = cfg["voice"]["preference"]
    if tool_override:
        prefs = [{"tool": tool_override, "voice": voice_override or ""}]
    tried = []
    for p in prefs:
        tool = registry._tools.get(p["tool"])
        if tool is None:
            tried.append(f"{p['tool']}: not installed")
            continue
        if tool.get_status() != ToolStatus.AVAILABLE:
            tried.append(f"{p['tool']}: unavailable (needs setup)")
            continue
        if p["tool"] == "sherpa_onnx_tts" and p.get("voice") and p["voice"] not in tool.available_voices():
            tried.append(f"{p['tool']}:{p['voice']}: model bundle missing")
            continue
        if p["tool"] == "elevenlabs_tts" and not p.get("voice"):
            tried.append("elevenlabs_tts: no Hindi voice_id configured")
            continue
        global TTS_MODEL, TTS_FALLBACKS
        TTS_MODEL = p.get("model", "")
        TTS_FALLBACKS = list(p.get("fallback_models", []))
        return tool, p.get("voice", ""), tried
    sys.exit("No Hindi-capable TTS available.\n  " + "\n  ".join(tried) +
             "\nFix: python -m tools.audio.sherpa_onnx_tts --download hi_rohan  (free, offline)")


def tts_inputs(tool_name: str, voice: str, text: str, out: Path, speed: float) -> dict:
    if tool_name == "sherpa_onnx_tts":
        return {"text": text, "voice": voice, "speed": speed, "output_path": str(out)}
    if tool_name == "azure_tts":
        rate = f"{int(round((speed - 1) * 100)):+d}%"
        return {"text": text, "voice": voice, "locale": "hi-IN", "rate": rate, "output_path": str(out)}
    if tool_name == "google_tts":
        return {"text": text, "voice": voice, "language_code": "hi-IN", "speaking_rate": speed, "output_path": str(out)}
    if tool_name == "gemini_tts":
        style = STYLE_PROMPT + (" Speak a little faster." if speed > 1.02 else " Speak a little slower." if speed < 0.97 else "")
        d = {"text": text, "voice_id": voice or "Charon", "style": style, "output_path": str(out)}
        if TTS_MODEL:
            d["model_id"] = TTS_MODEL
        return d
    if tool_name == "elevenlabs_tts":
        return {"text": text, "voice_id": voice, "language_code": "hi", "model_id": "eleven_multilingual_v2",
                "speed": speed, "output_path": str(out)}
    return {"text": text, "voice_id": voice, "output_path": str(out)}


def load_pcm(path: Path) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    a = np.frombuffer(raw, dtype=np.float32).copy()
    # trim leading/trailing digital silence so measured spans hug the speech
    thr = 10 ** (-50 / 20)
    idx = np.where(np.abs(a) > thr)[0]
    if len(idx):
        a = a[max(0, idx[0] - int(0.02 * SR)): min(len(a), idx[-1] + int(0.06 * SR))]
    return a


def load_pcm_raw(path: Path) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def split_phrases(text: str, marks: list[str]) -> list[tuple[str, str | None]]:
    """Split at dramatic beats ("…", "—"). Returns [(phrase, mark_that_followed_or_None)]."""
    pat = "(" + "|".join(re.escape(m) for m in marks) + ")"
    parts = re.split(pat, text)
    out, cur = [], ""
    for p in parts:
        if p in marks:
            if cur.strip():
                out.append((cur.strip(), p))
            cur = ""
        else:
            cur += p
    if cur.strip():
        out.append((cur.strip(), None))
    return out or [(text, None)]


def process_take(pcm: np.ndarray, script: dict, vcfg: dict, natural_voice: bool) -> np.ndarray:
    """Pause capping + optional pitch-preserving tempo, applied once to a take."""
    delivery = vcfg.get("delivery", {})
    if natural_voice and delivery.get("max_internal_pause_s"):
        pcm = cap_pauses(pcm, float(delivery["max_internal_pause_s"]))
    tempo = float(script.get("tempo", vcfg.get("tempo", 1.0)))
    if abs(tempo - 1.0) > 0.005:
        import soundfile as _sf
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            _sf.write(f"{td}/i.wav", pcm, SR)
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{td}/i.wav", "-af", f"atempo={tempo}", f"{td}/o.wav"], check=True)
            pcm = load_pcm(Path(f"{td}/o.wav"))
    return pcm


def single_take(tool, voice, lines, lines_dir, speed, script, vcfg) -> dict:
    """Perform the whole script in ONE take (consistent voice + natural flow, one API call), align every
    word to the audio, then cut it into per-line clips in the silences between lines.
    Returns {line_id: (pcm, words_relative_to_clip)}."""
    import soundfile as sf
    import align as AL

    full = lines_dir / "_single_take.wav"
    text = "\n\n".join(l.get("hi_tts", l["hi"]) for l in lines)
    stamp = lines_dir / "_single_take.txt"
    if full.exists() and stamp.exists() and stamp.read_text(encoding="utf-8") == text + "|" + STYLE_PROMPT and not RETAKE:
        print("  single take: reusing the existing take (same text + direction); pass --retake to record again")
    else:
        r = run_tts(tool, tts_inputs(tool.name, voice, text, full, speed), timeout_s=300, attempts=2)
        if not r.success:
            print(f"  single take failed ({r.error}); falling back to line-by-line")
            return {}
        stamp.write_text(text + "|" + STYLE_PROMPT, encoding="utf-8")
    raw = load_pcm(full)
    texts = [l.get("hi_tts", l["hi"]) for l in lines]
    # 1) coarse: find where each line starts in the RAW take (natural pauses), then cut in the silences.
    #    Gemini audio understanding gives the line order/positions; local pause-anchored alignment is the fallback.
    cache = lines_dir / "_line_starts.json"
    key = text + "|" + STYLE_PROMPT
    starts = None
    if cache.exists() and not RETAKE:
        c = read_json(cache)
        if c.get("key") == key:
            starts = c["starts"]
    if starts is None:
        starts = AL.gemini_line_starts(raw, SR, texts)
        if starts:
            write_json(cache, {"key": key, "starts": starts})
    cuts = AL.cut_points(raw, SR, starts) if starts else None
    if cuts is None:
        words = AL.align(raw, SR, "\n".join(texts))
        counts = [len(AL.tokens(t)) for t in texts]
        offs = np.concatenate([[0], np.cumsum(counts)]).astype(int)
        cuts = [0.0]
        for k in range(1, len(lines)):
            last_end, nxt = words[offs[k] - 1]["end"], words[offs[k]]["start"]
            if nxt - last_end < 0.12:
                print(f"  single take: no pause found between {lines[k - 1]['id']} and {lines[k]['id']}; falling back")
                return {}
            cuts.append((last_end + nxt) / 2)
        cuts.append(len(raw) / SR)
        print("  single take: cut with local alignment")
    else:
        print("  single take: cut at Gemini-located line starts, snapped to silences")
    words = [None] * sum(len(AL.tokens(t)) for t in texts)
    # 2) fine: process each line clip (pause cap, tempo) and align it on its own text
    out = {}
    total = 0.0
    for k, l in enumerate(lines):
        seg = raw[int(cuts[k] * SR): int(cuts[k + 1] * SR)]
        seg = process_take(seg, script, vcfg, True)
        thr = 10 ** (-50 / 20)
        idx = np.where(np.abs(seg) > thr)[0]
        if len(idx):
            seg = seg[max(0, idx[0] - int(0.03 * SR)): min(len(seg), idx[-1] + int(0.08 * SR))]
        gp = None
        wcache = lines_dir / f"_{l['id']}_prior.json"
        sig = f"{len(seg)}|{texts[k]}"
        if wcache.exists() and read_json(wcache).get("sig") == sig:
            gp = read_json(wcache)["prior"]
        elif vcfg.get("delivery", {}).get("gemini_word_prior", True):
            gp = AL.gemini_prior(seg, SR, AL.tokens(texts[k]), texts[k])
            if gp:
                write_json(wcache, {"sig": sig, "prior": gp})
        lw = AL.align(seg, SR, texts[k], prior=gp)
        sf.write(str(lines_dir / f"{l['id']}.wav"), seg, SR, subtype="PCM_16")
        out[l["id"]] = (seg, lw)
        total += len(seg) / SR
    pcm = np.zeros(int(total * SR), dtype=np.float32)
    print(f"  single take: {len(raw) / SR:.1f}s raw -> {total:.1f}s speech, {len(words)} words aligned, cut into {len(lines)} lines")
    return out


def run_tts(tool, inp, timeout_s: float = 90, attempts: int = 3):
    """Cloud calls can stall; give each attempt a hard timeout and retry."""
    import concurrent.futures as cf
    global TTS_MODEL
    if inp.get("model_id") and TTS_FALLBACKS:  # quota on one model -> try the next (same voice)
        chain = [inp["model_id"]] + [m for m in TTS_FALLBACKS if m != inp["model_id"]]
        r = None
        for m in chain:
            r = run_tts.__wrapped__(tool, {**inp, "model_id": m}, timeout_s, attempts)
            if r.success:
                if m != TTS_MODEL:
                    print(f"  TTS model {TTS_MODEL} unavailable; using {m}")
                    TTS_MODEL = m
                return r
            if not ("429" in (r.error or "") or "quota" in (r.error or "").lower()):
                return r
        return r
    return run_tts.__wrapped__(tool, inp, timeout_s, attempts)


def _run_tts_once(tool, inp, timeout_s: float = 90, attempts: int = 3):
    import concurrent.futures as cf
    last = None
    for k in range(attempts):
        ex = cf.ThreadPoolExecutor(max_workers=1)
        fut = ex.submit(tool.execute, dict(inp))
        try:
            r = fut.result(timeout=timeout_s)
            ex.shutdown(wait=False)
            if r.success:
                return r
            last = r
            if "429" in (r.error or "") or "quota" in (r.error or "").lower():
                break  # quota: retrying won't help
        except cf.TimeoutError:
            ex.shutdown(wait=False, cancel_futures=True)
            print(f"  TTS attempt {k + 1} timed out after {timeout_s:.0f}s, retrying", flush=True)
    if last is not None:
        return last
    from tools.base_tool import ToolResult
    return ToolResult(success=False, error=f"TTS timed out {attempts}x")


run_tts.__wrapped__ = _run_tts_once


def cap_pauses(pcm: np.ndarray, max_pause_s: float) -> np.ndarray:
    """Shorten any internal silence longer than max_pause_s (keeps rhythm, trims dead air)."""
    hop = int(0.01 * SR)
    n = len(pcm) // hop
    if n < 3:
        return pcm
    env = np.sqrt(np.mean(pcm[: n * hop].reshape(n, hop) ** 2, axis=1) + 1e-12)
    db = 20 * np.log10(env)
    quiet = db < (np.percentile(db, 90) - 30)
    keep = np.ones(n, dtype=bool)
    i, lim = 0, int(max_pause_s * 100)
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]:
                j += 1
            if j - i > lim:
                mid = (i + j) // 2
                drop = (j - i) - lim
                keep[mid - drop // 2: mid - drop // 2 + drop] = False
            i = j
        else:
            i += 1
    out = pcm[: n * hop].reshape(n, hop)[keep].reshape(-1)
    return np.concatenate([out, pcm[n * hop:]])


def find_beats(pcm: np.ndarray, n: int, weights: list[int], min_gap_s: float = 0.09) -> list[tuple[float, float]]:
    """Locate n spoken phrases in one line of audio: pick the n-1 silences that best match the
    character-proportional expected break points. Returns [(start_s, end_s)] relative to the line."""
    hop = int(0.01 * SR)
    env = np.array([np.sqrt(np.mean(pcm[i:i + hop] ** 2) + 1e-12) for i in range(0, len(pcm) - hop, hop)])
    db = 20 * np.log10(env + 1e-9)
    quiet = db < (np.percentile(db, 90) - 28)
    runs, i = [], 0
    while i < len(quiet):
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]:
                j += 1
            if j - i >= int(min_gap_s * 100) and i > 5 and j < len(quiet) - 5:  # long enough, not at the edges
                runs.append((i, j))
            i = j
        else:
            i += 1
    total = len(pcm) / SR
    cum = np.cumsum(weights)[:-1] / sum(weights) * total
    chosen = []
    for target in cum:
        cands = [r for r in runs if r not in chosen]
        if not cands:
            break
        best = min(cands, key=lambda r: abs((r[0] + r[1]) / 2 * 0.01 - target) - 0.004 * (r[1] - r[0]))
        chosen.append(best)
    if len(chosen) != n - 1:
        bounds = [0.0] + list(cum) + [total]
        return [(bounds[k], bounds[k + 1]) for k in range(n)]
    chosen.sort()
    spans, s0 = [], 0.0
    for a0, b0 in chosen:
        spans.append((s0, a0 * 0.01))
        s0 = b0 * 0.01
    spans.append((s0, total))
    return spans


def phrase_speed(ph: str, base: float, delivery: dict) -> float:
    """Gentle per-phrase rate variation: questions and short punch lines slower, connective phrases a touch faster."""
    words = len(ph.split())
    if ph.rstrip().endswith("?"):
        return round(base * delivery.get("question_rate", 0.95), 3)
    if words <= 3:
        return round(base * delivery.get("punch_rate", 0.93), 3)
    if words >= 9:
        return round(base * delivery.get("long_rate", 1.03), 3)
    return base


def split_caption(text: str, max_chars: int, max_lines: int) -> list[str]:
    """Split one English subtitle line into cue texts that fit max_lines x max_chars."""
    limit = max_chars * max_lines
    if len(text) <= limit:
        return [text]
    # prefer clause boundaries, then word boundaries
    parts = [p.strip() for p in re.split(r"(?<=[,.;:?!—…])\s+", text) if p.strip()]
    cues, cur = [], ""
    for p in parts:
        cand = (cur + " " + p).strip()
        if len(cand) <= limit:
            cur = cand
        else:
            if cur:
                cues.append(cur)
            while len(p) > limit:
                cut = p.rfind(" ", 0, limit)
                cut = cut if cut > 0 else limit
                cues.append(p[:cut].strip())
                p = p[cut:].strip()
            cur = p
    if cur:
        cues.append(cur)
    return cues


def wrap_lines(text: str, max_chars: int) -> str:
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len((cur + " " + w).strip()) <= max_chars:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    if len(lines) == 2 and len(lines[1]) < len(lines[0]) * 0.45:  # balance the two lines
        allw = text.split()
        best = min(range(1, len(allw)), key=lambda i: abs(len(" ".join(allw[:i])) - len(" ".join(allw[i:]))))
        lines = [" ".join(allw[:best]), " ".join(allw[best:])]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project_id")
    ap.add_argument("--voice-tool")
    ap.add_argument("--voice")
    ap.add_argument("--speed", type=float)
    ap.add_argument("--only", nargs="*", help="regenerate only these line ids (others reuse cached clips)")
    ap.add_argument("--retake", action="store_true", help="record a new single take even if one exists")
    a = ap.parse_args()
    global RETAKE
    RETAKE = a.retake

    cfg = load_config()
    pdir = project_dir(a.project_id)
    script = read_json(pdir / "artifacts" / "sv_script.json")
    fmt = cfg["formats"][script.get("format", "short")]
    speed = a.speed or cfg["voice"]["speed"]

    # ---- language guards (mandatory rules) ----
    problems = []
    for ln in script["lines"]:
        if not has_devanagari(ln["hi"]):
            problems.append(f"{ln['id']}: narration is not Hindi/Devanagari")
        if has_devanagari(ln["en"]):
            problems.append(f"{ln['id']}: English subtitle contains Devanagari")
    if problems:
        sys.exit("Language rule violations:\n  " + "\n  ".join(problems))

    global STYLE_PROMPT
    STYLE_PROMPT = script.get("voice_style") or cfg["voice"].get("style_prompt", "")
    tool, voice, tried = pick_voice(cfg, a.voice_tool, a.voice)
    print(f"TTS: {tool.name} voice={voice or '(provider default)'} speed={speed}")
    for t in tried:
        print(f"  skipped {t}")

    lines_dir = pdir / "assets" / "audio" / "lines"
    lines_dir.mkdir(parents=True, exist_ok=True)

    intro_mode = cfg["brand"]["intro"]["short_form" if script.get("format", "short") == "short" else "long_form"]
    lead_in = float(script.get("lead_in_seconds", 0.2 if intro_mode in ("overlay", "badge") else 3.3))  # first word within 0.5 s

    pieces = [np.zeros(int(lead_in * SR), dtype=np.float32)]
    t = lead_in
    timing_lines, cues, scenes = [], [], {}
    vcfg = cfg["voice"]
    delivery = vcfg.get("delivery", {})
    beat_marks = delivery.get("phrase_breaks", ["…", "—"])
    beat_pause = delivery.get("beat_pause_s", {"…": 0.38, "—": 0.26})
    tuning = vcfg.get("local_tuning", {}) if tool.name == "sherpa_onnx_tts" else {}
    import align as AL
    pregen = {}
    take_cache = lines_dir / "_take_words.json"
    if tool.name != "sherpa_onnx_tts" and delivery.get("single_take", True):
        if a.only is None:
            pregen = single_take(tool, voice, script["lines"], lines_dir, speed, script, vcfg)
            if pregen:
                write_json(take_cache, {k: v[1] for k, v in pregen.items()})
        elif take_cache.exists():  # re-time from the cached take (e.g. --only NONE)
            cached = read_json(take_cache)
            for lid, ws in cached.items():
                f = lines_dir / f"{lid}.wav"
                if f.exists() and lid not in (a.only or []):
                    pregen[lid] = (load_pcm_raw(f), ws)
    for i, ln in enumerate(script["lines"]):
        text = ln.get("hi_tts", ln["hi"])  # optional pronunciation-tuned variant
        pl = delivery.get("phrase_level", "auto")
        per_phrase = (tool.name == "sherpa_onnx_tts") if pl == "auto" else bool(pl)
        all_phrases = split_phrases(text, beat_marks)
        # natural cloud voices perform the whole line (better intonation); beats are found afterwards in the audio
        phrases = all_phrases if per_phrase else [(text, None)]
        en_parts = split_phrases(ln["en"], beat_marks)
        line_pcm, phrase_spans, lt = [], [], 0.0
        if ln["id"] in pregen:
            pcm, words_rel = pregen[ln["id"]]
            phrases = all_phrases
        else:
            for k, (ph, mark) in enumerate(phrases):
                out = lines_dir / (f"{ln['id']}.wav" if len(phrases) == 1 else f"{ln['id']}_{k + 1}.wav")
                if a.only is None or ln["id"] in a.only or not out.exists():
                    inp = tts_inputs(tool.name, voice, ph, out, phrase_speed(ph, speed, delivery))
                    inp.update(tuning)
                    r = run_tts(tool, inp)
                    if not r.success:
                        sys.exit(f"TTS failed on {ln['id']} phrase {k + 1}: {r.error}")
                pcm = process_take(load_pcm(out), script, vcfg, tool.name != "sherpa_onnx_tts")
                line_pcm.append(pcm)
                if k < len(phrases) - 1:
                    gap = float(beat_pause.get(mark, 0.3))
                    line_pcm.append(np.zeros(int(gap * SR), dtype=np.float32))
            pcm = np.concatenate(line_pcm)
            phrases = all_phrases
            if len(all_phrases) > 1:  # keep a single-file copy of the whole line for provenance / review
                import soundfile as _sf
                _sf.write(str(lines_dir / f"{ln['id']}.wav"), pcm, SR, subtype="PCM_16")
            words_rel = AL.align(pcm, SR, text)
        # the aligner may push the last word(s) past the trimmed clip end — pull them back inside the clip
        clip_dur = len(pcm) / SR
        if words_rel and words_rel[-1]["end"] > clip_dur - 0.02:
            lim = clip_dur - 0.03
            tail = [w for w in words_rel if w["start"] > lim - 0.25]
            if words_rel[-1]["start"] >= lim - 0.06:
                # squeezed at the very end: share the last stretch of speech among the tail words
                k = max(1, len(tail))
                t0 = min(tail[0]["start"], lim - 0.18 * k) if tail else lim - 0.18
                step = (lim - t0) / k
                for i, w in enumerate(words_rel[-k:]):
                    w["start"], w["end"] = t0 + i * step, t0 + (i + 1) * step - 0.01
            for w in words_rel:
                w["end"] = min(w["end"], lim)
                w["start"] = min(w["start"], w["end"] - 0.02)
        # phrase spans come from the aligned words (a phrase = the tokens between "…"/"—" beats)
        k0 = 0
        for ph, _m in phrases:
            n = len(AL.tokens(ph))
            ws = words_rel[k0:k0 + n] or words_rel[-1:]
            phrase_spans.append((ws[0]["start"], ws[-1]["end"]))
            k0 += n
        dur = len(pcm) / SR
        start, end = t, t + dur
        pieces.append(pcm)
        timing_lines.append({"id": ln["id"], "scene": ln["scene"], "start": round(start, 3), "end": round(end, 3),
                             "hi": ln["hi"], "en": ln["en"],
                             "phrases": [{"start": round(start + a0, 3), "end": round(start + b0, 3)} for a0, b0 in phrase_spans],
                             "words": [{"w": w["w"], "start": round(start + w["start"], 3), "end": round(start + w["end"], 3)} for w in words_rel],
                             "sync": ln.get("sync", [])})
        # subtitle cues: when the English has the same beats as the Hindi, cut cues exactly on the spoken phrases
        if len(en_parts) == len(phrases) and len(phrases) > 1 and all(len(e[0]) <= fmt["caption_max_chars_per_line"] * fmt["caption_max_lines"] for e in en_parts):
            groups = [(start + a0, start + b0, (e[0] + (e[1] or "")).strip()) for (a0, b0), e in zip(phrase_spans, en_parts)]
            for j, (cs, ce, txt) in enumerate(groups):
                ce = groups[j + 1][0] if j + 1 < len(groups) else end
                cues.append({"line": ln["id"], "start": round(cs, 3), "end": round(ce, 3),
                             "text": wrap_lines(txt, fmt["caption_max_chars_per_line"])})
        else:
            chunks = split_caption(ln["en"], fmt["caption_max_chars_per_line"], fmt["caption_max_lines"])
            total_chars = sum(len(c) for c in chunks)
            cs = start
            for j, c in enumerate(chunks):
                ce = end if j == len(chunks) - 1 else cs + dur * len(c) / total_chars
                cues.append({"line": ln["id"], "start": round(cs, 3), "end": round(ce, 3),
                             "text": wrap_lines(c, fmt["caption_max_chars_per_line"])})
                cs = ce
        sc = scenes.setdefault(ln["scene"], {"start": round(start, 3), "end": round(end, 3)})
        sc["end"] = round(end, 3)
        nxt = script["lines"][i + 1]["scene"] if i + 1 < len(script["lines"]) else None
        default_pause = vcfg["pause_after_section_s"] if nxt != ln["scene"] else vcfg["pause_after_line_s"]
        pause = float(ln.get("pause_after", default_pause))
        pieces.append(np.zeros(int(pause * SR), dtype=np.float32))
        t = end + pause

    narration_end = t
    tail = cfg["brand"]["end_card_seconds"]["short_form" if script.get("format", "short") == "short" else "long_form"]
    total = round(narration_end + tail, 2)
    audio = np.concatenate(pieces)
    audio = np.concatenate([audio, np.zeros(int(total * SR) - len(audio), dtype=np.float32)]) if len(audio) < total * SR else audio
    peak = float(np.max(np.abs(audio))) or 1.0
    audio = audio * min(1.0, 0.89 / peak)  # headroom; loudness is set at the final mix

    wav = pdir / "assets" / "audio" / "narration.wav"
    import soundfile as sf

    sf.write(str(wav), audio, SR, subtype="PCM_16")
    polish = vcfg.get("polish")
    if polish:  # broadcast-style voice chain: warmth, presence, gentle compression, small room
        tmp = wav.with_name("narration_dry.wav")
        wav.replace(tmp)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(tmp), "-af", polish, "-ar", str(SR), "-ac", "1",
                        "-t", f"{total:.3f}", str(wav)], check=True)
    # consistent narration level whatever the voice (voices differ by 10 dB+); the final mix sets platform loudness
    tmp2 = wav.with_name("narration_prenorm.wav")
    wav.replace(tmp2)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(tmp2), "-af", "loudnorm=I=-18:TP=-2:LRA=9", "-ar", str(SR), "-ac", "1",
                    "-t", f"{total:.3f}", str(wav)], check=True)

    # extend the last scene to the end card start and add the end card span
    scene_order = list(dict.fromkeys(ln["scene"] for ln in script["lines"]))
    for k, sid in enumerate(scene_order):
        if k + 1 < len(scene_order):
            scenes[sid]["end"] = scenes[scene_order[k + 1]]["start"]
    scenes[scene_order[0]]["start"] = 0.0
    scenes[scene_order[-1]]["end"] = round(narration_end, 3)

    # readability: merge cues that would flash by too fast (< ~17 chars/s or < 0.8 s) into a neighbour from the same line
    merged = []
    for c in cues:
        txt = c["text"].replace("\n", " ")
        if merged and merged[-1]["line"] == c["line"]:
            prev = merged[-1]
            p_txt = prev["text"].replace("\n", " ")
            too_fast = lambda t, d: d < 0.8 or len(t) / max(d, 0.01) > 17
            if too_fast(p_txt, prev["end"] - prev["start"]) or too_fast(txt, c["end"] - c["start"]):
                joined = (p_txt + " " + txt).strip()
                if len(joined) <= fmt["caption_max_chars_per_line"] * fmt["caption_max_lines"]:
                    prev["end"] = c["end"]
                    prev["text"] = wrap_lines(joined, fmt["caption_max_chars_per_line"])
                    continue
        merged.append(dict(c))
    cues = merged
    # let each cue breathe: lead the voice by 80 ms and hold through the following pause (max +0.45 s)
    for k, c in enumerate(cues):
        prev_end = cues[k - 1]["end"] if k else 0.0
        c["start"] = round(max(prev_end, c["start"] - 0.08), 3)
        nxt = cues[k + 1]["start"] - 0.08 if k + 1 < len(cues) else c["end"] + 0.45
        c["end"] = round(max(c["end"], min(nxt, c["end"] + 0.45)), 3)

    timing = {
        "project_id": a.project_id, "format": script.get("format", "short"),
        "width": fmt["width"], "height": fmt["height"], "fps": fmt["fps"],
        "lead_in": lead_in, "narration_end": round(narration_end, 3),
        "end_card": {"start": round(narration_end, 3), "end": total},
        "total_duration": total,
        "tts": {"tool": tool.name, "provider": tool.provider, "voice": voice, "speed": speed},
        "scenes": scenes, "lines": timing_lines, "captions": cues,
    }
    write_json(pdir / "artifacts" / "timing.json", timing)

    srt, vtt = [], ["WEBVTT", ""]
    for n, c in enumerate(cues, 1):
        srt += [str(n), f"{fmt_ts(c['start'])} --> {fmt_ts(c['end'])}", c["text"], ""]
        vtt += [f"{fmt_ts(c['start'], '.')} --> {fmt_ts(c['end'], '.')}", c["text"], ""]
    (pdir / "assets" / "subtitles.en.srt").write_text("\n".join(srt), encoding="utf-8")
    (pdir / "assets" / "subtitles.en.vtt").write_text("\n".join(vtt), encoding="utf-8")

    words_hi = sum(len(ln["hi"].split()) for ln in script["lines"])
    print(f"Narration {narration_end - lead_in:.1f}s spoken ({words_hi} Hindi words, "
          f"{words_hi / max(1e-6, narration_end - lead_in):.2f} w/s); video total {total:.1f}s; {len(cues)} caption cues")
    lo, hi = fmt["target_seconds"]
    if not (lo <= total <= hi + 5):
        print(f"WARNING: total {total:.1f}s is outside the {lo}-{hi}s target — tighten or extend the script, don't pad.")


if __name__ == "__main__":
    main()
