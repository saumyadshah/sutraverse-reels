#!/usr/bin/env python3
"""Original, royalty-free background bed: a synthesized tanpura-style drone + soft pad.

Used only when no better music source exists (OpenMontage order: music_library/ ->
royalty-free search -> music generation API -> this local fallback). It is generated
from scratch (additive synthesis), so there are no licensing questions.

Usage: python music_bed.py <project_id> [--key C#] [--seconds N] [--seed 7]
Writes projects/<id>/assets/music/bed.wav (48 kHz stereo) and prints its provenance.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import load_config, project_dir, read_json  # noqa: E402

SR = 48000
NOTES = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}


def hz(key: str, octave: int) -> float:
    n = NOTES[key] + 12 * (octave + 1)  # MIDI
    return 440.0 * 2 ** ((n - 69) / 12)


def pluck(f0: float, dur: float, rng: np.random.Generator) -> np.ndarray:
    """Tanpura-like string: rich harmonics whose emphasis drifts upward (jawari buzz)."""
    t = np.arange(int(dur * SR)) / SR
    out = np.zeros_like(t)
    sweep = 1.0 + 6.0 * (1 - np.exp(-t / 1.6))           # harmonic centre drifts upward
    for h in range(1, 28):
        amp = (1.0 / h ** 0.9) * np.exp(-((h - sweep) ** 2) / 18.0) + 0.25 / h ** 1.6
        detune = 1 + rng.normal(0, 0.0007)
        out += amp * np.sin(2 * np.pi * f0 * h * detune * t + rng.uniform(0, 6.28))
    env = (1 - np.exp(-t / 0.012)) * np.exp(-t / 3.8)
    return out * env


def reverb(x: np.ndarray, seconds: float, rng: np.random.Generator) -> np.ndarray:
    n = int(seconds * SR)
    ir = rng.normal(0, 1, n) * np.exp(-np.arange(n) / (SR * seconds / 5))
    ir[0] = 0
    ir /= np.sqrt(np.sum(ir ** 2))
    size = 1 << int(np.ceil(np.log2(len(x) + n)))
    y = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[: len(x)]
    return y


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project_id")
    ap.add_argument("--key")
    ap.add_argument("--seconds", type=float)
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()
    cfg = load_config()
    pdir = project_dir(a.project_id)
    total = a.seconds or read_json(pdir / "artifacts" / "timing.json")["total_duration"]
    key = a.key or cfg["music"]["drone_key"]
    rng = np.random.default_rng(a.seed)

    n = int((total + 4) * SR)
    L = np.zeros(n)
    R = np.zeros(n)
    # classic Pa-Sa'-Sa'-Sa cycle, ~1.05 s per pluck, slightly humanised
    cycle = [(hz(key, 3) * 1.5, -0.35), (hz(key, 4), 0.25), (hz(key, 4), 0.3), (hz(key, 3), -0.1)]
    t = 0.0
    k = 0
    while t < total + 1:
        f, pan = cycle[k % 4]
        s = pluck(f, 6.0, rng) * (0.9 if k % 4 else 1.0)
        i = int(t * SR)
        j = min(n, i + len(s))
        L[i:j] += s[: j - i] * (1 - pan) * 0.5
        R[i:j] += s[: j - i] * (1 + pan) * 0.5
        t += 1.05 + rng.normal(0, 0.02)
        k += 1
    # pad: low Sa + Pa sines with slow swell, plus air (filtered noise)
    tt = np.arange(n) / SR
    swell = 0.55 + 0.45 * np.sin(2 * np.pi * tt / 19.0 - 1.2) ** 2
    pad = (np.sin(2 * np.pi * hz(key, 2) * tt) * 0.5 + np.sin(2 * np.pi * hz(key, 2) * 1.5 * tt) * 0.22) * swell
    air = np.convolve(rng.normal(0, 1, n), np.ones(220) / 220, mode="same") * 0.6
    L += pad * 0.35 + air * 0.08
    R += pad * 0.35 + air * 0.08
    L = 0.75 * L + 0.5 * reverb(L, 2.8, rng)
    R = 0.75 * R + 0.5 * reverb(R, 2.9, rng)
    st = np.stack([L, R], 1)[: int(total * SR)]
    fade_in, fade_out = int(1.5 * SR), int(2.5 * SR)
    st[:fade_in] *= np.linspace(0, 1, fade_in)[:, None]
    st[-fade_out:] *= np.linspace(1, 0, fade_out)[:, None]
    st *= 10 ** (cfg["music"]["bed_volume_db"] / 20) / (np.max(np.abs(st)) + 1e-9) * 3.0
    st = np.clip(st, -0.98, 0.98)

    import soundfile as sf

    out = pdir / "assets" / "music" / "bed.wav"
    out.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(out), st.astype(np.float32), SR, subtype="PCM_16")
    print(f"music bed: {out} ({total:.1f}s, tanpura drone in {key}, seed {a.seed}) — original synthesis, royalty-free")


if __name__ == "__main__":
    main()
