"""Coach floor on the optical printer."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from .engine import FFMPEG, _run, list_modes, stage
from .gomotion import apply_rig, go_motion
from .jobs import list_jobs, spec_for
from .optical import print_shot


def _media_path(media: Any) -> Path:
    if media is None:
        raise FileNotFoundError("No media")
    if isinstance(media, (str, Path)):
        path = Path(media)
    else:
        name = getattr(media, "name", None) or getattr(media, "path", None)
        if not name:
            raise FileNotFoundError("Upload had no path")
        path = Path(name)
    if not path.exists():
        raise FileNotFoundError(path)
    return path


def studio_bible() -> dict:
    return {
        "product": "Stage Coach",
        "jobs": list_jobs(),
        "modes": list_modes(),
        "workflow": [
            "Adversal MCP understands the source (Markdown + frames).",
            "Coach selects plates.",
            "StageKey finishes: key, look, go-motion, farm.",
            "Reel the approved takes.",
        ],
        "commands": {
            "coach": "python -m stagekey coach SOURCE --jobs hologram-cyan,cel --name slate_01",
            "finish": "python -m stagekey stage plate.mp4 --screen green --look hologram-cyan",
            "ingest": "python -m stagekey ingest clip.mp4",
        },
    }


def make_shot(
    src: str | Path,
    job: str = "puppet-walk",
    name: str = "shot",
    rig: Optional[str] = None,
) -> dict:
    spec = spec_for(job)
    job = spec.get("id", job)
    src = Path(src)
    work = src.parent / "stagekey_out"
    work.mkdir(parents=True, exist_ok=True)
    current = src
    if spec["kind"] in {"puppet", "rig"}:
        if rig and spec["kind"] == "rig":
            current = Path(apply_rig(current, rig, output=str(work / f"{name}_rig.mp4")))
        else:
            current = Path(
                go_motion(
                    current,
                    move=spec["move"],
                    shutter=int(spec.get("shutter", 3)),
                    duration=float(spec.get("duration", 3.0)),
                    output=str(work / f"{name}_go.mp4"),
                )
            )
    if spec.get("look") != "raw" or spec.get("screen") in {"green", "blue"}:
        current = Path(
            print_shot(
                current,
                output=str(work / f"{name}_print.mp4"),
                screen=spec.get("screen", "none"),
                look=spec.get("look", "raw"),
                background=spec.get("background", "black"),
            )
        )
    elif spec["kind"] == "optical":
        current = Path(
            stage(
                current,
                screen=spec.get("screen", "none"),
                look=spec.get("look", "raw"),
                background=spec.get("background", "black"),
                output=str(work / f"{name}_stage.mp4"),
            )
        )
    card = {
        "name": name,
        "job": job,
        "title": spec["title"],
        "desk": spec["desk"],
        "shot": str(current),
        "spec": spec,
    }
    (work / f"{name}.card.json").write_text(json.dumps(card, indent=2))
    return card


def make_movie(media: Any, job: str = "puppet-walk", name: str = "shot") -> dict:
    return make_shot(_media_path(media), job=job, name=name)


def assemble_reel(clips: list[str | Path], name: str = "reel", output: Optional[str] = None) -> str:
    clips = [Path(c) for c in clips]
    if not clips:
        raise ValueError("No clips")
    out = Path(output) if output else clips[0].with_name(f"{name}.mp4")
    lst = out.with_suffix(".txt")
    lines = []
    for c in clips:
        if not c.exists():
            raise FileNotFoundError(c)
        lines.append(f"file '{c.resolve().as_posix()}'")
    lst.write_text("\n".join(lines) + "\n")
    _run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(out)])
    return str(out)
