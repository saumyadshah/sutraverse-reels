#!/usr/bin/env python3
"""Verify single-take line cuts: Whisper-translate every line clip and compare it with the line's English.

Usage: python linecheck.py <project_id>
A clip whose translation carries its neighbour's words means the cuts are wrong — fix
assets/audio/lines/_line_starts.json (or delete it and re-run narrate.py) before composing.
Sanskrit shloka lines translate poorly; judge those by position, not by words.
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import project_dir  # noqa: E402

W = Path.home() / ".openmontage/models/sherpa-onnx/sherpa-onnx-whisper-small"


def main():
    import sherpa_onnx

    pdir = project_dir(sys.argv[1])
    r = sherpa_onnx.OfflineRecognizer.from_whisper(
        encoder=str(W / "small-encoder.onnx"), decoder=str(W / "small-decoder.onnx"), tokens=str(W / "small-tokens.txt"),
        language="hi", task="translate", num_threads=2)
    T = json.loads((pdir / "artifacts/timing.json").read_text(encoding="utf-8"))
    for l in T["lines"]:
        wav = pdir / f"assets/audio/lines/{l['id']}.wav"
        a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(wav), "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                                         capture_output=True).stdout, dtype=np.float32)
        s = r.create_stream()
        s.accept_waveform(16000, a)
        r.decode_stream(s)
        print(f"{l['id']} {l['end'] - l['start']:5.2f}s | heard: {s.result.text[:90]}\n{'':10}| script: {l['en'][:90]}")


if __name__ == "__main__":
    main()
