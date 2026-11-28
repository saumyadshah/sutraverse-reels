"""OTLO score v1 (28 Nov 2026): an original, fully synthesised background score for OTLO features (no licensing).
Raag Bhoopali (S R G P D) on D. Layers: tanpura (Karplus-Strong + jawari buzz), santoor motifs (paired detuned
strings), warm string pad, and a dhol/tabla groove that enters at the story's turn and builds to the climax.
Call: score(T, SR, climax_at=None) -> mono numpy array. T = timing dict (starts/ends of scenes).
Arc: scenes 1-3 intimate (drone + santoor + pad); scene 4 onward the groove enters; it builds to `climax_at`
(default: 55% into the second-to-last scene) with a cymbal swell; the last scene resolves (groove stops, cadence)."""
import numpy as np
from scipy.signal import lfilter

SA = 146.83  # D3
RATIO = {'S': 1, 'R': 9/8, 'G': 5/4, 'P': 3/2, 'D': 5/3}

def _note(n):
    o = 1.0
    if n.endswith("'"): o, n = 2.0, n[:-1]
    if n.endswith(','): o, n = 0.5, n[:-1]
    return SA * RATIO[n] * o

def ks(f, dur, sr, bright=0.6, decay=0.996, seed=0):
    """Karplus-Strong plucked string via lfilter (fast)."""
    rng = np.random.default_rng(seed); L = max(2, int(round(sr / f))); n = int(dur * sr)
    exc = rng.uniform(-1, 1, L)
    for _ in range(int((1 - bright) * 6)): exc = np.convolve(exc, [0.5, 0.5], 'same')   # darker attack
    x = np.zeros(n); x[:L] = exc
    a = np.zeros(L + 2); a[0] = 1; a[L] = -decay / 2; a[L + 1] = -decay / 2
    y = lfilter([1.0], a, x)
    return y / (np.max(np.abs(y)) + 1e-9)

def score(T, sr, climax_at=None):
    DUR = T['ends'][-1] + 0.2; N = int(DUR * sr); t = np.arange(N) / sr
    out = np.zeros(N); st = T['starts']; en = T['ends']; ns = len(st)
    turn = st[3] if ns > 4 else st[-2]; last = st[-1]
    climax = climax_at or (st[-2] + 0.55 * (en[-2] - st[-2]))
    def add(y, at, amp):
        i = int(at * sr); n = min(len(y), N - i)
        if n > 0 and i >= 0: out[i:i + n] += amp * y[:n]
    # 1. tanpura: P, S', S', S cycle; jawari = soft saturation of a bright string
    cyc = 3.4; k = 0; x0 = 0.0
    while x0 < DUR:
        for nm in ["P,", "S", "S", "S,"]:
            f = _note(nm); y = ks(f, 5.5, sr, bright=0.9, decay=0.9985, seed=k)
            y = np.tanh(2.2 * y) * 0.7 + 0.3 * y
            add(y, x0, 0.16); k += 1; x0 += cyc / 4
    # 2. pad: detuned additive saws on S, P, S' with slow swells; louder from the turn to the climax
    padenv = 0.35 + 0.65 * np.clip((t - turn) / max(0.5, climax - turn), 0, 1)
    padenv *= np.where(t > climax, np.exp(-(t - climax) / 4.0) * 0.6 + 0.4, 1.0)
    padenv *= np.minimum(t / 2.0, 1)
    pad = np.zeros(N)
    for f in [_note('S,'), _note('P,'), _note('S')]:
        for det in (-0.003, 0.003):
            ff = f * (1 + det)
            for h in range(1, 7): pad += np.sin(2 * np.pi * ff * h * t + h) / h ** 1.6
    pad = np.convolve(pad, np.ones(24) / 24, 'same')
    out += 0.018 * pad * padenv
    # 3. santoor motifs at chapter starts (hammered: two detuned strings, bright, short)
    motifs = [["S", "R", "G", "P"], ["G", "P", "D", "S'"], ["D", "P", "G", "R", "S"], ["P", "D", "S'", "R'"],
              ["S'", "D", "P", "G"], ["G", "P", "D", "S'", "R'", "S'"], ["P", "G", "R", "S"]]
    for i, s0 in enumerate(st):
        mot = motifs[i % len(motifs)]; base = s0 + (0.15 if i else 0.9)
        for j, nm in enumerate(mot):
            f = _note(nm) * 2
            y = 0.5 * ks(f * 1.0012, 1.6, sr, 0.95, 0.993, 100 + i * 10 + j) + 0.5 * ks(f * 0.9988, 1.6, sr, 0.95, 0.993, 200 + i * 10 + j)
            add(y, base + j * 0.19, 0.07 if i < ns - 1 else 0.10)
    # final cadence over the end slate
    for j, nm in enumerate(["P", "D", "S'", "R'", "S'"]):
        f = _note(nm) * 2; y = 0.5 * ks(f * 1.001, 2.5, sr, 0.95, 0.995, 900 + j) + 0.5 * ks(f * 0.999, 2.5, sr, 0.95, 0.995, 950 + j)
        add(y, last + 1.2 + j * 0.32, 0.09)
    # 4. groove: dhol (low) + tabla ticks; enters at the turn, builds to the climax, stops for the last scene
    bpm = 88; beat = 60 / bpm; x0 = turn; k = 0; rng = np.random.default_rng(3)
    while x0 < last - 0.1:
        prog = np.clip((x0 - turn) / max(0.5, climax - turn), 0, 1)
        n = int(0.4 * sr); xx = np.arange(n) / sr
        if k % 4 in (0, 3):        # dhol "dha": pitch-falling low drum + skin noise
            f = 95 * np.exp(-xx * 9) + 52
            y = np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-xx * 9) + 0.15 * rng.standard_normal(n) * np.exp(-xx * 60)
            add(y, x0, 0.22 + 0.18 * prog)
        if prog > 0.25 and k % 2 == 1:   # tabla "na": ringing high tone
            y = (np.sin(2 * np.pi * 520 * xx) + 0.5 * np.sin(2 * np.pi * 1310 * xx)) * np.exp(-xx * 22)
            add(y, x0, 0.07 + 0.08 * prog)
        if prog > 0.6:                  # 16th ghost ticks near the climax
            y = rng.standard_normal(int(0.05 * sr)) * np.exp(-np.arange(int(0.05 * sr)) / sr * 90)
            add(y, x0 + beat / 2, 0.05 * prog)
        x0 += beat; k += 1
    # 5. cymbal swell into the climax, and a soft low "boom" on it
    n = int(1.4 * sr); xx = np.arange(n) / sr; nz = np.random.default_rng(9).standard_normal(n)
    nz = nz - np.convolve(nz, np.ones(8) / 8, 'same')
    add(nz * (xx / 1.4) ** 2.5, climax - 1.4, 0.10)
    nb = int(1.8 * sr); xb = np.arange(nb) / sr
    add(np.sin(2 * np.pi * (60 * np.exp(-xb * 2) + 38) * xb) * np.exp(-xb * 2.2), climax, 0.30)
    # master envelope: quick fade-in, gentle fade-out
    out *= np.minimum(1, np.minimum(t / 0.25, (DUR - t) / 1.6).clip(0, 1))
    return out / (np.max(np.abs(out)) + 1e-9)
