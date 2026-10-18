"""Word-level alignment of narration audio to its (known) script text.

Why: subtitles, kinetic type, character lip-flap and story beats must land on the
spoken WORD, not on an estimate. The script text is known, so this is forced
alignment, not recognition.

How (no GPU, no model download):
1. Speech segments: a 10 ms energy envelope splits the audio into voiced runs. Word
   and syllable boundaries in fluent Hindi show up as short dips (>= 30 ms).
2. A prior for every word start:
   - Gemini (audio understanding, when GEMINI_API_KEY/GOOGLE_API_KEY is set): the audio
     plus the exact token list goes in, a start time per token comes back.
   - otherwise: character-proportional positions laid over the VOICED time only.
3. Snap: a monotonic dynamic-programming match of every prior to a voiced-run onset
   (cost = |onset - prior|, an unmatched word costs a fixed penalty and keeps its
   clamped prior). Result: word starts sit on real acoustic onsets, in order.

Typical accuracy on clean TTS: +-40-80 ms at word starts (vs +-200-400 ms for raw
Gemini timestamps or proportional guesses).
"""
from __future__ import annotations

import base64
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

import numpy as np

TOKEN_RE = re.compile(r"[^\s…।॥,?!—.\"“”'‘’:;()\[\]|]+")


def tokens(text: str) -> list[str]:
    return TOKEN_RE.findall(text)


def speech_segments(pcm: np.ndarray, sr: int, rel_db: float = 26, min_gap_s: float = 0.03,
                    min_run_s: float = 0.03) -> list[tuple[float, float]]:
    hop = int(0.01 * sr)
    n = len(pcm) // hop
    if n < 2:
        return [(0.0, len(pcm) / sr)]
    env = np.sqrt(np.mean(pcm[: n * hop].reshape(n, hop) ** 2, axis=1) + 1e-12)
    db = 20 * np.log10(env)
    # smooth lightly so a single quiet frame inside a vowel does not split it
    db = np.convolve(db, np.ones(3) / 3, mode="same")
    voiced = db > (np.percentile(db, 92) - rel_db)
    segs, i = [], 0
    while i < n:
        if voiced[i]:
            j = i
            while j < n and voiced[j]:
                j += 1
            segs.append([i, j])
            i = j
        else:
            i += 1
    # merge across gaps shorter than min_gap, drop specks
    merged = []
    for s in segs:
        if merged and s[0] - merged[-1][1] < int(min_gap_s * 100):
            merged[-1][1] = s[1]
        else:
            merged.append(s)
    return [(a / 100, b / 100) for a, b in merged if (b - a) >= int(min_run_s * 100)] or [(0.0, n / 100)]


def proportional_prior(words: list[str], segs: list[tuple[float, float]]) -> list[float]:
    """Character-weighted word starts laid over voiced time only."""
    w = np.array([max(1, len(x)) for x in words], dtype=float)
    cum = np.concatenate([[0], np.cumsum(w)[:-1]]) / w.sum()
    voiced = np.array([b - a for a, b in segs])
    total = voiced.sum()
    edges = np.concatenate([[0], np.cumsum(voiced)])
    out = []
    for c in cum:
        tv = c * total
        k = min(len(segs) - 1, int(np.searchsorted(edges, tv, side="right") - 1))
        out.append(segs[k][0] + (tv - edges[k]))
    return out


ALIGN_MODELS = ["gemini-3.8-flash", "gemini-3.6-flash", "gemini-3.5-flash", "gemini-3-flash-preview", "gemini-3.1-flash-lite"]


def _gemini_json(pcm: np.ndarray, sr: int, prompt: str, timeout: int = 240):
    """Send audio + prompt; walk the model chain on quota/availability errors. Returns parsed JSON or None."""
    key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not key:
        return None
    import requests
    import soundfile as sf

    with tempfile.TemporaryDirectory() as td:
        sf.write(f"{td}/a.wav", pcm, sr)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{td}/a.wav", "-ar", "16000", "-ac", "1", "-c:a", "flac", f"{td}/a.flac"], check=True)
        data = base64.b64encode(Path(f"{td}/a.flac").read_bytes()).decode()
    body = {"contents": [{"parts": [{"inlineData": {"mimeType": "audio/flac", "data": data}}, {"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 0}}
    for model in ALIGN_MODELS:
        try:
            r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                              headers={"x-goog-api-key": key}, json=body, timeout=timeout)
            j = r.json()
        except Exception as exc:
            print(f"  aligner: {model} {exc.__class__.__name__}")
            continue
        if "error" in j:
            code = j["error"].get("code")
            if code in (429, 503, 404, 500):
                continue
            print(f"  aligner: {model}: {j['error'].get('message', '')[:100]}")
            return None
        try:
            return json.loads(j["candidates"][0]["content"]["parts"][0]["text"])
        except Exception:
            continue
    print("  aligner: no Gemini model available (quota); using local alignment")
    return None


def gemini_prior(pcm: np.ndarray, sr: int, words: list[str], transcript: str,
                 model: str = "gemini-3.8-flash", timeout: int = 180) -> list[float] | None:
    if not words:
        return None
    prompt = (
        "You are a precise forced aligner. The audio contains exactly this narration (Hindi, possibly with short "
        "Sanskrit lines):\n" + transcript + "\n\nFor EACH of the following tokens, in this exact order, give the time "
        "in seconds (2 decimals, from the start of the audio) at which the token begins to be spoken. Return ONLY a "
        "JSON array of numbers with exactly " + str(len(words)) + " entries.\nTokens: " + json.dumps(words, ensure_ascii=False)
    )
    arr = _gemini_json(pcm, sr, prompt, timeout)
    if arr is None:
        return None
    try:
        if isinstance(arr, dict):
            arr = next((v for v in arr.values() if isinstance(v, list)), [])
        arr = [float(x["s"] if isinstance(x, dict) else x) for x in arr]
    except Exception:
        return None
    if len(arr) != len(words):
        return None
    return arr


def snap(prior: list[float], onsets: list[float], penalty: float = 0.22, max_dev: float = 0.6) -> list[float]:
    """Monotonic DP: match each prior word start to a distinct, increasing onset (or leave it unmatched)."""
    N, M = len(prior), len(onsets)
    INF = 1e9
    dp = np.full((N + 1, M + 1), INF)
    back = np.zeros((N + 1, M + 1), dtype=np.int32)  # 0 = unmatched, 1 = matched to onset j-1, 2 = carry (skip onset)
    dp[0, :] = 0.0
    for k in range(N):
        best_prev, best_j = INF, 0
        for j in range(M + 1):
            # carry: dp[k+1][j] can come from dp[k+1][j-1] (skip onset j-1 without using it)
            if j > 0 and dp[k + 1, j - 1] < dp[k + 1, j]:
                dp[k + 1, j] = dp[k + 1, j - 1]
                back[k + 1, j] = 2
            # unmatched word k
            c = dp[k, j] + penalty
            if c < dp[k + 1, j]:
                dp[k + 1, j] = c
                back[k + 1, j] = 0
            # matched to onset j (uses onset index j, needs dp[k][j] i.e. onsets < j used)
            if j < M:
                d = abs(onsets[j] - prior[k])
                if d <= max_dev:
                    c = dp[k, j] + d
                    if c < dp[k + 1, j + 1]:
                        dp[k + 1, j + 1] = c
                        back[k + 1, j + 1] = 1
    # backtrack
    k, j = N, int(np.argmin(dp[N]))
    out = [None] * N
    while k > 0:
        b = back[k, j]
        if b == 2:
            j -= 1
        elif b == 1:
            out[k - 1] = onsets[j - 1]
            k, j = k - 1, j - 1
        else:
            k -= 1
    # unmatched: clamp prior between matched neighbours
    for i in range(N):
        if out[i] is None:
            lo = max([out[x] for x in range(i) if out[x] is not None] or [-1e9]) + 0.05
            hi = min([out[x] for x in range(i + 1, N) if out[x] is not None] or [1e9]) - 0.05
            out[i] = float(min(max(prior[i], lo), hi))
    return out


def onsets_from(segs: list[tuple[float, float]], pcm: np.ndarray, sr: int) -> list[float]:
    """Voiced-run starts plus strong energy rises inside long runs (word boundaries without a full dip)."""
    ons = [a for a, _ in segs]
    hop = int(0.01 * sr)
    n = len(pcm) // hop
    env = np.sqrt(np.mean(pcm[: n * hop].reshape(n, hop) ** 2, axis=1) + 1e-12)
    db = 20 * np.log10(env)
    for a, b in segs:
        if b - a < 0.45:
            continue
        i0, i1 = int(a * 100), int(b * 100)
        seg = db[i0:i1]
        for i in range(6, len(seg) - 3):
            dip = seg[i - 4:i].min()
            if seg[i - 1] - dip < 2 and seg[i + 2] - dip > 7 and seg[i - 4:i].argmin() >= 2:
                t = (i0 + i - 1) / 100
                if all(abs(t - o) > 0.09 for o in ons):
                    ons.append(t)
    return sorted(ons)


BREAK_CHARS = "…।॥,?!—.;:"


def token_breaks(text: str) -> tuple[list[str], list[int]]:
    """Tokens plus a break strength after each: 2 = sentence/ellipsis, 1 = comma-ish, 0 = none."""
    toks, brk = [], []
    ms = list(TOKEN_RE.finditer(text))
    for i, m in enumerate(ms):
        toks.append(m.group(0))
        between = text[m.end(): ms[i + 1].start()] if i + 1 < len(ms) else text[m.end():]
        if "\n" in between:
            brk.append(3)   # line break (between script lines)
        elif any(c in between for c in "…।॥?!.—"):
            brk.append(2)
        elif any(c in between for c in ",;:"):
            brk.append(1)
        else:
            brk.append(0)
    return toks, brk


def gaps_from(segs: list[tuple[float, float]], min_gap: float = 0.16) -> list[tuple[float, float]]:
    return [(a[1], b[0]) for a, b in zip(segs, segs[1:]) if b[0] - a[1] >= min_gap]


def assign_breaks(brk: list[int], words: list[str], segs, gaps) -> dict[int, tuple[float, float]]:
    """Monotonic DP: map text breaks (token index after which a pause is expected) to audio gaps."""
    idx = [k for k, b in enumerate(brk[:-1]) if b > 0]
    if not idx or not gaps:
        return {}
    prior = proportional_prior(words, segs)
    total = segs[-1][1]
    exp = [(prior[k + 1] if k + 1 < len(prior) else total) for k in idx]
    B, G = len(idx), len(gaps)
    INF = 1e9
    dp = np.full((B + 1, G + 1), INF)
    bk = np.zeros((B + 1, G + 1), dtype=np.int8)
    dp[0, :] = 0
    for i in range(B):
        strength = brk[idx[i]]
        miss = {3: 3.0, 2: 0.5}.get(strength, 0.25)
        bonus = {3: 1.8, 2: 0.8}.get(strength, 0.4)
        for j in range(G + 1):
            if j > 0 and dp[i + 1, j - 1] < dp[i + 1, j]:
                dp[i + 1, j], bk[i + 1, j] = dp[i + 1, j - 1], 2
            if dp[i, j] + miss < dp[i + 1, j]:
                dp[i + 1, j], bk[i + 1, j] = dp[i, j] + miss, 0
            if j < G:
                g0, g1 = gaps[j]
                c = dp[i, j] + abs((g0 + g1) / 2 - exp[i]) * 0.6 - min(1.0, (g1 - g0)) * bonus
                if c < dp[i + 1, j + 1]:
                    dp[i + 1, j + 1], bk[i + 1, j + 1] = c, 1
    i, j = B, int(np.argmin(dp[B]))
    out = {}
    while i > 0:
        b = bk[i, j]
        if b == 2:
            j -= 1
        elif b == 1:
            out[idx[i - 1]] = gaps[j - 1]
            i, j = i - 1, j - 1
        else:
            i -= 1
    return out


def align(pcm: np.ndarray, sr: int, words_or_text, prior: list[float] | None = None) -> list[dict]:
    """Align with an optional external prior; the prior is rejected if it squeezes or drifts the words."""
    local = _align(pcm, sr, words_or_text, None)
    if prior is None:
        return local
    try:
        withp = _align(pcm, sr, words_or_text, prior)
    except Exception:
        return local
    segs = speech_segments(pcm, sr)
    span = max(1e-3, segs[-1][0] - segs[0][0])
    cover = (withp[-1]["start"] - withp[0]["start"]) / span
    drift = float(np.mean([abs(a["start"] - b["start"]) for a, b in zip(local, withp)]))
    gaps = [b["start"] - a["start"] for a, b in zip(withp, withp[1:])]
    squeezed = sum(1 for g in gaps if g < 0.06)
    if cover < 0.8 or drift > 0.45 or squeezed > max(1, len(gaps) // 5):
        return local
    return withp


def _align(pcm: np.ndarray, sr: int, words_or_text, prior: list[float] | None = None) -> list[dict]:
    """Return [{"w", "start", "end"}] (seconds, relative to pcm start).
    Pass the TEXT (with punctuation) for best results: pauses at "…", "।", "," anchor the alignment."""
    if isinstance(words_or_text, str):
        words, brk = token_breaks(words_or_text)
    else:
        words, brk = list(words_or_text), [0] * len(words_or_text)
    if not words:
        return []
    segs = speech_segments(pcm, sr)
    ons = onsets_from(segs, pcm, sr)
    gaps = gaps_from(segs)
    anchors = assign_breaks(brk, words, segs, gaps)
    # chunk the token list at anchored breaks, align each chunk inside its audio span
    cuts = sorted(anchors)
    bounds_t, bounds_k = [segs[0][0]], [0]
    for k in cuts:
        g0, g1 = anchors[k]
        bounds_t += [g0, g1]
        bounds_k.append(k + 1)
    bounds_t.append(segs[-1][1])
    bounds_k.append(len(words))
    starts = []
    for c in range(len(bounds_k) - 1):
        k0, k1 = bounds_k[c], bounds_k[c + 1]
        t0, t1 = bounds_t[2 * c], bounds_t[2 * c + 1]
        cw = words[k0:k1]
        csegs = [(max(a, t0), min(b, t1)) for a, b in segs if b > t0 and a < t1] or [(t0, t1)]
        cprior = proportional_prior(cw, csegs)
        if prior is not None:  # external prior (e.g. Gemini), re-based to this chunk
            p = prior[k0:k1]
            off = csegs[0][0] - p[0]
            cprior = [0.3 * x + 0.7 * (y + off) for x, y in zip(cprior, p)]
        cons = [o for o in ons if t0 - 0.01 <= o < t1]
        seg_starts = [a for a, _ in csegs]
        if len(seg_starts) == len(cw) and prior is None:  # one voiced run per word: the runs ARE the words
            cs = list(seg_starts)
        else:
            cs = snap(cprior, cons, penalty=0.3, max_dev=0.45) if cons else cprior
        cs[0] = csegs[0][0]  # a chunk always starts on its first voiced frame
        starts += cs
    out = []
    for i, w in enumerate(words):
        s0 = starts[i]
        nxt = starts[i + 1] if i + 1 < len(words) else segs[-1][1]
        run_end = next((b for a, b in segs if a - 0.02 <= s0 < b), s0 + 0.25)
        e = min(nxt - 0.01, max(run_end, s0 + 0.08))
        out.append({"w": w, "start": round(s0, 3), "end": round(max(e, s0 + 0.05), 3), "brk": brk[i]})
    return out


def gemini_line_starts(pcm: np.ndarray, sr: int, texts: list[str], timeout: int = 240) -> list[float] | None:
    """Ask Gemini (audio understanding) where each script line starts. Coarse (+-0.5 s) but
    reliable in ORDER, which is exactly what is needed to pick the right silence to cut at."""
    numbered = "\n".join(f"{i + 1}. {t}" for i, t in enumerate(texts))
    prompt = ("This audio is a narrator reading these " + str(len(texts)) + " numbered lines, in order (Hindi, with a few "
              "Sanskrit lines):\n" + numbered + "\n\nFor each line give the time in seconds (2 decimals, from the start of "
              "the audio) at which the narrator starts speaking that line. Return ONLY a JSON array of " + str(len(texts)) + " numbers.")
    arr = _gemini_json(pcm, sr, prompt, timeout)
    try:
        arr = [float(x) for x in (arr or [])]
    except Exception:
        return None
    if len(arr) != len(texts) or any(b <= a for a, b in zip(arr, arr[1:])):
        if arr:
            print("  aligner: Gemini line starts not usable (count/order); using local cut")
        return None
    return arr


def cut_points(pcm: np.ndarray, sr: int, prior_starts: list[float], window: float = 1.3) -> list[float] | None:
    """Pick, for every line boundary, the silence that best matches the prior (longer silences preferred)."""
    segs = speech_segments(pcm, sr)
    gaps = gaps_from(segs, min_gap=0.12)
    cuts, last = [0.0], 0.0
    for p in prior_starts[1:]:
        cands = [(g0, g1) for g0, g1 in gaps if abs((g0 + g1) / 2 - p) <= window and (g0 + g1) / 2 > last + 0.3]
        if not cands:
            return None
        g0, g1 = max(cands, key=lambda g: min(0.8, g[1] - g[0]) - 0.45 * abs((g[0] + g[1]) / 2 - p))
        last = (g0 + g1) / 2
        cuts.append(last)
    cuts.append(len(pcm) / sr)
    return cuts
