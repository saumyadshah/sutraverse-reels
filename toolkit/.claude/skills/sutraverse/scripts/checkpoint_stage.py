#!/usr/bin/env python3
"""Write an OpenMontage checkpoint for a stage from the canonical artifacts on disk.

Reads projects/<id>/artifacts/<artifact>.json for the stage, validates through
lib.checkpoint.write_checkpoint (schema + gate enforcement). A gated stage is
marked human-approved only when decision_log.json holds an `approval_policy`
full-run pre-authorization (set by new_project.py --full-run-approved) or when
--approved is passed after the user approved in chat.

Usage: python checkpoint_stage.py <project_id> <stage> [--status completed|awaiting_human] [--approved]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ROOT, load_config, read_json  # noqa: E402

STAGE_ARTIFACTS = {
    "research": ["research_brief"],
    "proposal": ["proposal_packet", "decision_log"],
    "script": ["script"],
    "scene_plan": ["scene_plan"],
    "assets": ["asset_manifest"],
    "edit": ["edit_decisions"],
    "compose": ["render_report"],
    "publish": ["publish_log"],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project_id")
    ap.add_argument("stage", choices=list(STAGE_ARTIFACTS))
    ap.add_argument("--status", default="completed", choices=["completed", "awaiting_human", "in_progress"])
    ap.add_argument("--approved", action="store_true")
    a = ap.parse_args()
    cfg = load_config()
    pipe = ROOT / cfg["paths"]["projects_dir"]
    adir = pipe / a.project_id / "artifacts"
    arts = {}
    for name in STAGE_ARTIFACTS[a.stage]:
        f = adir / f"{name}.json"
        if not f.is_file():
            sys.exit(f"missing artifact {f}")
        arts[name] = read_json(f)
    dl = adir / "decision_log.json"
    policy = dl.is_file() and any(d.get("category") == "approval_policy" for d in read_json(dl).get("decisions", []))

    from lib.checkpoint import _stage_requires_approval, write_checkpoint

    marker = read_json(pipe / a.project_id / "project.json")
    gated = bool(_stage_requires_approval(marker.get("pipeline_type"), a.stage))
    approved = a.approved or policy
    if gated and a.status == "completed" and not approved:
        sys.exit(f"Stage '{a.stage}' is gated. Present it to the user, or record a full-run approval policy.")
    p = write_checkpoint(pipe, a.project_id, a.stage, a.status, arts,
                         human_approval_required=gated, human_approved=approved if gated else False,
                         metadata={"approval_basis": "decision_log approval_policy" if policy and not a.approved else ("user approved in chat" if a.approved else "not gated")})
    print(f"checkpoint written: {p}")


if __name__ == "__main__":
    main()
