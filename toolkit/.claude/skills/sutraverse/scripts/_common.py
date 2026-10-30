"""Shared helpers for SutraVerse scripts. Locates the OpenMontage repo, loads config."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent


def repo_root() -> Path:
    env = os.environ.get("OPENMONTAGE_ROOT")
    if env:
        return Path(env).resolve()
    for p in [SKILL_DIR, *SKILL_DIR.parents]:
        if (p / "AGENT_GUIDE.md").is_file() and (p / "tools" / "tool_registry.py").is_file():
            return p
    cwd = Path.cwd()
    if (cwd / "AGENT_GUIDE.md").is_file():
        return cwd
    sys.exit("Cannot locate the OpenMontage repo. Run from the repo root or set OPENMONTAGE_ROOT.")


ROOT = repo_root()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def cast_registry(project: Path | None = None) -> dict:
    """The shared cast (toolkit/cast/cast.json) merged with the Reel's own artifacts/cast_local.json."""
    reg = {}
    for p in [Path.home() / "sutraverse-reels/toolkit/cast/cast.json", Path("/root/sutraverse-reels/toolkit/cast/cast.json"),
              SKILL_DIR.parents[2] / "cast" / "cast.json"]:
        if p.is_file():
            reg = json.loads(p.read_text(encoding="utf-8"))["characters"]
            break
    if project is not None and (project / "artifacts" / "cast_local.json").is_file():
        reg.update(json.loads((project / "artifacts" / "cast_local.json").read_text(encoding="utf-8")).get("characters", {}))
    return reg


def load_config() -> dict:
    import yaml

    with open(SKILL_DIR / "config" / "sutraverse.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def project_dir(project_id: str) -> Path:
    cfg = load_config()
    d = ROOT / cfg["paths"]["projects_dir"] / project_id
    if not d.is_dir():
        sys.exit(f"Project workspace not found: {d}. Initialise it with scripts/new_project.py first.")
    return d


def read_json(p: Path) -> dict:
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def write_json(p: Path, data) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def ffprobe_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return float(out)


def has_devanagari(text: str) -> bool:
    return any("ऀ" <= ch <= "ॿ" for ch in text)


def fmt_ts(sec: float, sep: str = ",") -> str:
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"
