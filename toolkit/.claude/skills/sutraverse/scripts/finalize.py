#!/usr/bin/env python3
"""Render, mix and mux a SutraVerse video through OpenMontage's own tools.

1. hyperframes_compose  operation=render_existing  (lint + runtime + layout gate, then render)
2. audio_mixer          operation=full_mix         (narration + ducked bed + loudness target)
3. ffmpeg mux           video from (1) + mixed audio from (2) -> renders/final.mp4
4. writes artifacts/render_report.json and copies the English .srt next to the video

Usage: python finalize.py <project_id> [--quality draft|standard|high] [--skip-render]
Env:   HYPERFRAMES_BROWSER_PATH  optional, when Chrome Headless Shell cannot be auto-installed
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ffprobe_duration, load_config, project_dir, read_json, write_json  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project_id")
    ap.add_argument("--quality", default="high", choices=["draft", "standard", "high"])
    ap.add_argument("--skip-render", action="store_true", help="re-mix/re-mux only, reuse renders/video_raw.mp4")
    a = ap.parse_args()
    cfg = load_config()
    pdir = project_dir(a.project_id)
    T = read_json(pdir / "artifacts" / "timing.json")
    fmt = cfg["formats"][T["format"]]
    comp = pdir / "composition"
    raw = pdir / "renders" / "video_raw.mp4"
    raw.parent.mkdir(parents=True, exist_ok=True)

    if not a.skip_render:
        from tools.video.hyperframes_compose import HyperFramesCompose

        r = HyperFramesCompose().execute({
            "operation": "render_existing", "workspace_path": str(comp), "output_path": str(raw),
            "quality": a.quality, "fps": fmt["fps"], "skip_contrast": True,
        })
        if not r.success:
            print("RENDER FAILED:", r.error)
            chk = (r.data or {}).get("steps", {}).get("check")
            if chk:
                import json
                print(json.dumps(chk, indent=1, ensure_ascii=False)[:6000])
            sys.exit(1)
        print(f"rendered {raw}")

    # ---- audio: narration + ducked bed, loudness for the platform ----
    from tools.audio.audio_mixer import AudioMixer

    tracks = [{"path": str(pdir / "assets" / "audio" / "narration.wav"), "role": "speech", "start_seconds": 0}]
    bed = pdir / "assets" / "music" / "bed.wav"
    if bed.is_file():
        tracks.append({"path": str(bed), "role": "music", "volume": 1.0})
    mix = pdir / "assets" / "audio" / "final_mix.wav"
    m = AudioMixer().execute({
        "operation": "full_mix", "tracks": tracks, "output_path": str(mix),
        "ducking": {"enabled": True, "music_volume_during_speech": cfg["music"]["duck_to"], "attack_ms": 150, "release_ms": 700},
        "normalize": True, "loudnorm_target": fmt["loudness_lufs"], "target_duration": T["total_duration"],
    })
    if not m.success:
        sys.exit(f"MIX FAILED: {m.error}")

    final = pdir / "renders" / "final.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-i", str(raw), "-i", str(mix), "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-t", f"{T['total_duration']:.3f}",
        "-metadata:s:a:0", "language=hin", "-metadata", "title=" + read_json(pdir / "artifacts" / "sv_script.json")["title"],
        "-movflags", "+faststart", str(final),
    ], check=True)
    shutil.copy2(pdir / "assets" / "subtitles.en.srt", pdir / "renders" / "final.en.srt")

    report = {
        "version": "1.0",
        "outputs": [{
            "path": str(final), "format": "mp4", "codec": "h264", "audio_codec": "aac",
            "resolution": f"{T['width']}x{T['height']}", "fps": fmt["fps"],
            "duration_seconds": round(ffprobe_duration(final), 3), "file_size_bytes": final.stat().st_size,
            "platform_target": "instagram_reels+youtube_shorts" if T["format"] == "short" else "youtube",
        }],
        "verification_notes": ["Run qa_check.py for language, sync, loudness and branding verification."],
        "metadata": {
            "render_runtime": "hyperframes", "composition_mode": "atelier",
            "rendered_at": datetime.now(timezone.utc).isoformat(),
            "audio": {"language": "hi", "loudness_target_lufs": fmt["loudness_lufs"], "tts": T["tts"]},
            "subtitles": {"language": "en", "burned_in": True, "sidecar": str(pdir / "renders" / "final.en.srt")},
        },
    }
    write_json(pdir / "artifacts" / "render_report.json", report)
    print(f"FINAL: {final}  ({report["outputs"][0]["duration_seconds"]}s)")


if __name__ == "__main__":
    main()
