#!/usr/bin/env python3
"""Derive OpenMontage canonical artifacts from SutraVerse working files.

Reads  artifacts/sv_script.json, artifacts/timing.json, artifacts/storyboard.json (authored scene plan),
       assets on disk, composition/src.
Writes artifacts/script.json, scene_plan.json, asset_manifest.json, edit_decisions.json, and the
       human deliverables renders/script.hi.md (Hindi + English) and renders/storyboard.md.
Then validates each against schemas/artifacts/*.schema.json.

storyboard.json shape: {"scenes": {"S1": {"type": "...", "description": "...", "visual": "...",
  "motion": "...", "on_screen_text": "...", "sfx_music": "...", "transition": "dissolve"}}}

Usage: python derive_artifacts.py <project_id>
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ROOT, fmt_ts, project_dir, read_json, write_json  # noqa: E402


def validate(name: str, data: dict) -> str:
    import jsonschema

    schema = read_json(ROOT / "schemas" / "artifacts" / f"{name}.schema.json")
    errs = sorted(jsonschema.Draft202012Validator(schema).iter_errors(data), key=lambda e: e.path)
    return "valid" if not errs else "INVALID: " + "; ".join(f"{list(e.path)}: {e.message[:120]}" for e in errs[:4])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project_id")
    a = ap.parse_args()
    pdir = project_dir(a.project_id)
    A = pdir / "artifacts"
    S = read_json(A / "sv_script.json")
    T = read_json(A / "timing.json")
    sb = read_json(A / "storyboard.json")["scenes"] if (A / "storyboard.json").is_file() else {}

    lines_by_scene: dict[str, list] = {}
    for ln, tm in zip(S["lines"], T["lines"]):
        lines_by_scene.setdefault(ln["scene"], []).append({**ln, **tm})

    script = {
        "version": "1.0", "title": S["title"], "total_duration_seconds": T["total_duration"],
        "voice_performance": {"performance_intent": "warm, conversational Hindi storyteller", "pacing_profile": "conversational",
                              "pause_policy": "0.32 s between lines, 0.5 s at scene changes"},
        "sections": [{
            "id": sid, "label": lines_by_scene[sid][0].get("role", ""),
            "text": " ".join(l["hi"] for l in lines_by_scene[sid]),
            "start_seconds": sc["start"], "end_seconds": sc["end"],
            "speaker_directions": "warm, conversational Hindi storyteller",
        } for sid, sc in T["scenes"].items()],
        "metadata": {"narration_language": "hi", "subtitle_language": "en", "bilingual_lines": S["lines"]},
    }

    allowed = {"talking_head", "broll", "animation", "character_scene", "diagram", "text_card", "transition", "generated", "screen_recording"}
    scene_plan = {"version": "1.0", "style_playbook": "sutraverse", "scenes": [], "metadata": {"storyboard": {}}}
    for sid, sc in T["scenes"].items():
        d = sb.get(sid, {})
        scene_plan["scenes"].append({
            "id": sid, "type": d.get("type") if d.get("type") in allowed else "animation",
            "description": " ".join(x for x in (d.get("description", ""), d.get("visual", "")) if x),
            "start_seconds": sc["start"], "end_seconds": sc["end"], "script_section_id": sid,
            "movement": d.get("motion", ""), "transition_in": d.get("transition", "dissolve"),
            "overlay_notes": f"On-screen English: {d.get('on_screen_text', '')}. Sound: {d.get('sfx_music', '')}",
        })
        scene_plan["metadata"]["storyboard"][sid] = {**d, "narration_lines": [l["id"] for l in lines_by_scene[sid]]}

    assets = []
    for ln in T["lines"]:
        assets.append({"id": f"vo-{ln['id']}", "type": "narration", "path": str(pdir / "assets/audio/lines" / f"{ln['id']}.wav"),
                       "source_tool": T["tts"]["tool"], "scene_id": ln["scene"],
                       "provider": T["tts"]["provider"], "model": T["tts"]["voice"], "format": "wav",
                       "duration_seconds": round(ln["end"] - ln["start"], 3), "generation_summary": "Hindi narration line"})
    assets.append({"id": "vo-full", "type": "narration", "path": str(pdir / "assets/audio/narration.wav"),
                   "source_tool": T["tts"]["tool"], "scene_id": "all", "provider": T["tts"]["provider"], "format": "wav"})
    if (pdir / "assets/music/bed.wav").is_file():
        assets.append({"id": "music-bed", "type": "music", "path": str(pdir / "assets/music/bed.wav"),
                       "source_tool": "sutraverse.music_bed", "scene_id": "all",
                       "license": "original synthesis, royalty-free", "generation_summary": "tanpura drone + pad, additive synthesis"})
    assets.append({"id": "subs-en", "type": "subtitle", "path": str(pdir / "assets/subtitles.en.srt"),
                   "source_tool": "sutraverse.narrate", "scene_id": "all", "format": "srt", "generation_summary": "English subtitles timed to measured Hindi narration"})
    for sid in T["scenes"]:
        assets.append({"id": f"scene-{sid}", "type": "animation", "path": str(pdir / "composition/src/scenes.html") + f"#{sid}",
                       "source_tool": "hyperframes (atelier, hand-authored SVG/GSAP)", "scene_id": sid})
    asset_manifest = {"version": "1.0", "assets": assets, "total_cost_usd": 0.0}

    edit = {
        "version": "1.0", "render_runtime": "hyperframes", "composition_mode": "atelier",
        "cuts": [{"id": f"cut-{sid}", "source": f"scene-{sid}", "in_seconds": sc["start"], "out_seconds": sc["end"],
                  "transition_in": "dissolve"} for sid, sc in T["scenes"].items()],
        "subtitles": {"enabled": True, "style": "sentence", "source": str(pdir / "assets/subtitles.en.srt"), "position": "bottom-center"},
        "music": {"asset_id": "music-bed", "ducking": True},
        "metadata": {"loudnorm_target": -14, "subtitle_language": "en", "narration_language": "hi"},
    }

    for name, data in (("script", script), ("scene_plan", scene_plan), ("asset_manifest", asset_manifest), ("edit_decisions", edit)):
        write_json(A / f"{name}.json", data)
        print(f"{name:15} {validate(name, data)}")

    # human-readable deliverables
    r = pdir / "renders"
    r.mkdir(exist_ok=True)
    md = [f"# {S['title']}", "", "Hindi narration (as voiced) with the English subtitle for each line.", ""]
    for ln, tm in zip(S["lines"], T["lines"]):
        ref = f" · *{ln['source_ref']}* ({ln['claim_type'].replace('_', ' ')})" if ln.get("source_ref") else f" · ({ln['claim_type'].replace('_', ' ')})"
        md += [f"**{fmt_ts(tm['start'], '.')[3:11]}** · {ln['scene']}{ref}", "", ln["hi"], "", f"> {ln['en']}", ""]
    (r / "script.hi.md").write_text("\n".join(md), encoding="utf-8")
    sbm = [f"# Storyboard — {S['title']}", "", "| Scene | Time | Lines | Visual | Motion / camera | On-screen English | Sound |", "|---|---|---|---|---|---|---|"]
    for sc in scene_plan["scenes"]:
        m = scene_plan["metadata"]["storyboard"].get(sc["id"], {"narration_lines": []})
        sbm.append(f"| {sc['id']} | {sc['start_seconds']:.1f}–{sc['end_seconds']:.1f}s | {', '.join(m['narration_lines'])} | "
                   f"{sc['description']} | {m.get('motion', '')} | {m.get('on_screen_text', '')} | {m.get('sfx_music', '')} |")
    (r / "storyboard.md").write_text("\n".join(sbm), encoding="utf-8")
    print("wrote renders/script.hi.md, renders/storyboard.md")


if __name__ == "__main__":
    main()
