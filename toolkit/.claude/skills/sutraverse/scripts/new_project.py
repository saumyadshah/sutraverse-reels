#!/usr/bin/env python3
"""Create a SutraVerse project workspace using OpenMontage's own initialiser.

- lib.checkpoint.init_project  -> projects/<id>/ layout + project.json (Backlot board marker)
- composition/src/ skeleton    -> scenes.html / scenes.css / scenes.js to author
- artifacts/sv_script.json     -> bilingual script stub (Hindi narration + English subtitle per line)
- artifacts/decision_log.json  -> records the approval policy for this run

Usage:
  python new_project.py <project-id> --title "…" [--format short|long] [--pipeline animated-explainer]
                        [--full-run-approved]   # user asked for the finished video in one go
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ROOT, SKILL_DIR, load_config, read_json, write_json  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project_id")
    ap.add_argument("--title", required=True)
    ap.add_argument("--format", default="short", choices=["short", "long"])
    ap.add_argument("--pipeline", default="animated-explainer")
    ap.add_argument("--full-run-approved", action="store_true")
    a = ap.parse_args()
    cfg = load_config()

    from lib.checkpoint import init_project

    pdir = init_project(a.project_id, title=a.title, pipeline_type=a.pipeline,
                        pipeline_dir=ROOT / cfg["paths"]["projects_dir"], style_playbook="sutraverse")
    src = pdir / "composition" / "src"
    src.mkdir(parents=True, exist_ok=True)
    for name in ("scenes.html", "scenes.css", "scenes.js"):
        if not (src / name).exists():
            shutil.copy2(SKILL_DIR / "templates" / f"{name}.template", src / name)
    stub = pdir / "artifacts" / "sv_script.json"
    if not stub.exists():
        s = read_json(SKILL_DIR / "templates" / "sv_script.example.json")
        s.update({"title": a.title, "format": a.format})
        write_json(stub, s)
    dl = pdir / "artifacts" / "decision_log.json"
    if not dl.exists():
        decisions = [{
            "decision_id": "d-lang-001", "stage": "proposal", "category": "playbook_selection",
            "subject": "Narration and on-screen language policy",
            "options_considered": [{"option_id": "hi-en", "label": "Hindi voice-over + English on-screen text", "score": 1.0,
                                    "reason": "SutraVerse channel standard"}],
            "selected": "hi-en",
            "reason": "SutraVerse channel standard (non-negotiable unless the user explicitly changes it)", "user_visible": True,
        }]
        if a.full_run_approved:
            decisions.append({
                "decision_id": "d-approval-001", "stage": "proposal", "category": "approval_policy",
                "subject": "Run approval mode",
                "options_considered": [
                    {"option_id": "per-stage", "label": "Per-stage approval gates", "score": 0.4, "reason": "Slower; user asked for the finished video", "rejected_because": "user requested a complete video in one request"},
                    {"option_id": "full-run", "label": "Full-run pre-authorization", "score": 0.9, "reason": "Matches the request; paid calls above the budget threshold still need a yes"}],
                "selected": "full-run",
                "reason": "User requested the complete finished video in one request (SutraVerse skill default)", "user_visible": True, "user_approved": True,
            })
        write_json(dl, {"version": "1.0", "project_id": a.project_id, "decisions": decisions})
    print(f"Project ready: {pdir}")
    print("Next: research -> fill artifacts/sv_script.json -> narrate.py -> author composition/src -> build_composition.py -> finalize.py -> qa_check.py")


if __name__ == "__main__":
    main()
