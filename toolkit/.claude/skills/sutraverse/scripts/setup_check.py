#!/usr/bin/env python3
"""SutraVerse preflight: what can this machine produce right now?

Runs OpenMontage's registry preflight and adds the channel-specific checks:
Hindi TTS, Whisper verifier, render runtime + browser, fonts/GSAP vendored, image/video
providers. With --install it fetches the free local pieces (sherpa-onnx, Hindi voices, Whisper).

Usage: python setup_check.py [--install]
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tarfile
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ROOT, SKILL_DIR, load_config  # noqa: E402

WHISPER = "https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-small.tar.bz2"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--install", action="store_true", help="install free local voice + verifier models")
    a = ap.parse_args()
    cfg = load_config()

    if a.install:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "sherpa-onnx", "soundfile"], check=False)
        subprocess.run([sys.executable, "-m", "tools.audio.sherpa_onnx_tts", "--download", "hi_rohan", "hi_kokoro_psi"],
                       cwd=ROOT, check=False)
        from tools.audio.sherpa_onnx_tts import models_dir

        wd = models_dir() / "sherpa-onnx-whisper-small"
        if not (wd / "small-encoder.onnx").is_file():
            tmp = models_dir() / "whisper.tar.bz2"
            print("downloading Whisper small (~600 MB compressed)…")
            urllib.request.urlretrieve(WHISPER, tmp)
            with tarfile.open(tmp, "r:bz2") as tf:
                tf.extractall(models_dir(), filter="data")
            tmp.unlink(missing_ok=True)

    from tools.base_tool import ToolStatus
    from tools.tool_registry import registry

    registry.discover()
    s = registry.provider_menu_summary()
    caps = {c["capability"]: c for c in s["capabilities"]}
    print("OPENMONTAGE CAPABILITIES")
    for k in ("tts", "image_generation", "video_generation", "music_generation", "music_search", "music_library", "subtitle", "video_post"):
        c = caps.get(k)
        if c:
            print(f"  {k:18} {c['configured']}/{c['total']} configured  {', '.join(c['available_providers']) or '-'}")
    print("  runtimes          ", s["composition_runtimes"])

    print("\nSUTRAVERSE CHECKS")
    hindi = []
    for p in cfg["voice"]["preference"]:
        t = registry._tools.get(p["tool"])
        ok = bool(t) and t.get_status() == ToolStatus.AVAILABLE
        if ok and p["tool"] == "sherpa_onnx_tts":
            ok = p["voice"] in t.available_voices()
        if ok and p["tool"] == "elevenlabs_tts" and not p.get("voice"):
            ok = False
        hindi.append((p["tool"], p.get("voice"), ok))
        print(f"  Hindi voice  {'READY ' if ok else 'no    '} {p['tool']}:{p.get('voice') or '-'}  ({p['note']})")
    first = next((h for h in hindi if h[2]), None)
    print(f"  -> narration will use: {first[0]}:{first[1]}" if first else
          "  -> BLOCKER: no Hindi voice. Run: python .claude/skills/sutraverse/scripts/setup_check.py --install")

    wd = Path.home() / ".openmontage/models/sherpa-onnx/sherpa-onnx-whisper-small"
    print(f"  Whisper verifier {'READY' if (wd / 'small-encoder.onnx').is_file() else 'missing (QA cannot machine-verify Hindi; --install)'}")
    kit = SKILL_DIR / "brand-kit"
    print(f"  brand kit        {'READY' if (kit / 'vendor/gsap.min.js').is_file() and any((kit / 'fonts').glob('*.woff2')) else 'INCOMPLETE'} (GSAP + fonts vendored, offline-safe)")
    hf_ok = s["composition_runtimes"].get("hyperframes")
    bp = os.environ.get(cfg["paths"]["browser_env"])
    if hf_ok:
        try:
            out = subprocess.run(["npx", "--yes", "hyperframes", "doctor", "--json"], capture_output=True, text=True, timeout=240, cwd=ROOT).stdout
            j = json.loads(out[out.find("{"):]) if "{" in out else {}
            chrome = next((c for c in j.get("checks", []) if "chrome" in str(c.get("name", "")).lower()), None)
            chrome_ok = bool(chrome and chrome.get("ok")) or bool(bp)
        except Exception:
            chrome_ok = bool(bp)
        print(f"  HyperFrames      READY; headless Chrome {'READY' if chrome_ok else 'MISSING → run: npx hyperframes browser ensure (or set ' + cfg['paths']['browser_env'] + ')'}")
    else:
        print("  HyperFrames      NOT AVAILABLE (needs Node >= 22 + FFmpeg) — see skills/core/hyperframes.md")
    print(f"  ffmpeg           {'READY' if shutil.which('ffmpeg') else 'MISSING'}")
    img = caps.get("image_generation", {}).get("configured", 0)
    vid = caps.get("video_generation", {}).get("configured", 0)
    route = "C (generated motion + plates)" if vid else ("B (generated plates, animated)" if img else "A (hand-authored SVG/GSAP animation)")
    print(f"  visual route     {route}")
    if s.get("setup_offers"):
        envs = sorted({e for o in s["setup_offers"] if o["capability"] in ("image_generation", "video_generation", "tts") for e in o.get("env_vars", [])})
        print(f"  upgrades (1-min env var): {', '.join(envs[:12])}")


if __name__ == "__main__":
    main()
