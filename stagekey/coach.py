"""Stage Coach — professional workflow: Adversal understand, then StageKey finish."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional

from .adversal import pipeline_card, pull, status, submit
from .farm import DEFAULT_LOOKS, farm

FRAMES = {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".mp4", ".mov", ".webm"}


def _first_plates(folder: Path, limit: int = 3) -> list[Path]:
    found: list[Path] = []
    if not folder.exists():
        return found
    for path in sorted(folder.rglob("*")):
        if path.is_file() and path.suffix.lower() in FRAMES:
            found.append(path)
            if len(found) >= limit:
                break
    return found


def run_coach(
    source: str,
    jobs: Optional[Iterable[str]] = None,
    name: str = "slate",
    dest: str = "adversal_out",
    wait: bool = True,
    plates: Optional[Iterable[str]] = None,
    notes: str = "",
) -> dict:
    jobs = list(jobs or DEFAULT_LOOKS)
    board: dict = {
        "product": "Stage Coach",
        "name": name,
        "source": source,
        "jobs": jobs,
        "notes": notes,
        "workflow": ["understand", "select", "finish", "reel"],
        "probe": pipeline_card().get("probe"),
    }
    queued = submit(source, artifact="report", wait=wait)
    board["ingest"] = queued
    request_id = queued.get("request_id")
    if request_id and wait:
        board["status"] = status(request_id, wait=True)
        board["pull"] = pull(request_id, dest=dest)
    dest_path = Path(dest)
    selected = [Path(p) for p in plates] if plates else _first_plates(dest_path)
    if not selected:
        src_path = Path(source)
        if src_path.exists() and src_path.suffix.lower() in FRAMES:
            selected = [src_path]
    board["plates"] = [str(p) for p in selected]
    farms = []
    for i, plate in enumerate(selected, start=1):
        farms.append(
            farm(
                plate,
                jobs=jobs,
                name=f"{name}_{i:02d}",
                planner="coach",
                notes=notes,
            )
        )
    board["farms"] = farms
    return board
