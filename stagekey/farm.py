"""Multi-render farm. Planners pick jobs. StageKey prints them. Adversal is never replaced."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Optional

from .jobs import JOBS
from .studio import assemble_reel, make_shot

DEFAULT_LOOKS = ["ghost-message", "alert-ghost", "cartoon-show", "toon-ghost", "toy-walk"]


def farm(
    src: str | Path,
    jobs: Optional[Iterable[str]] = None,
    name: str = "farm",
    planner: str = "grok",
    reel: bool = True,
    notes: str = "",
) -> dict:
    jobs = list(jobs or DEFAULT_LOOKS)
    unknown = [j for j in jobs if j not in JOBS]
    if unknown:
        raise ValueError(f"Unknown jobs {unknown}. Known: {sorted(JOBS)}")
    src = Path(src)
    work = src.parent / "stagekey_out" / name
    work.mkdir(parents=True, exist_ok=True)
    shots = []
    for job in jobs:
        card = make_shot(src, job=job, name=f"{name}_{job}")
        shots.append(card)
    reel_path = None
    if reel and shots:
        reel_path = assemble_reel([c["shot"] for c in shots], name=name, output=str(work / f"{name}_reel.mp4"))
    board = {
        "name": name,
        "src": str(src),
        "planner": planner,
        "notes": notes,
        "jobs": jobs,
        "shots": shots,
        "reel": reel_path,
        "desks": {
            "understand": "adversal",
            "plan_online": "grok",
            "plan_offline": "mistral-ollama",
            "finish": "stagekey",
        },
    }
    (work / f"{name}.farm.json").write_text(json.dumps(board, indent=2))
    return board
