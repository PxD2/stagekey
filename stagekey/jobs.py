"""Named finishes for the coach floor."""

from __future__ import annotations

JOBS = {
    "puppet-walk": {
        "title": "Puppet walk",
        "desk": "Go-motion walk, heavy shutter",
        "kind": "puppet",
        "move": "heavy-steps",
        "screen": "none",
        "look": "raw",
        "background": "black",
        "duration": 3.0,
        "shutter": 5,
    },
    "flyby": {
        "title": "Locked flyby",
        "desk": "Motion-control pass on a fixed path",
        "kind": "puppet",
        "move": "flyby",
        "screen": "none",
        "look": "raw",
        "background": "black",
        "duration": 3.0,
        "shutter": 4,
    },
    "push-in": {
        "title": "Push-in",
        "desk": "Repeatable camera move in",
        "kind": "rig",
        "move": "push-in",
        "screen": "none",
        "look": "raw",
        "background": "keep",
        "duration": 3.0,
        "shutter": 3,
    },
    "hover": {
        "title": "Hover",
        "desk": "Go-motion hover, soft shutter",
        "kind": "puppet",
        "move": "hover",
        "screen": "none",
        "look": "raw",
        "background": "black",
        "duration": 3.0,
        "shutter": 6,
    },
    "hologram-cyan": {
        "title": "Cyan hologram",
        "desk": "Key + cyan hologram on black",
        "kind": "optical",
        "move": "hold",
        "screen": "green",
        "look": "hologram-cyan",
        "background": "black",
        "duration": 3.0,
        "shutter": 1,
    },
    "hologram-red": {
        "title": "Red hologram",
        "desk": "Key + red hologram on black",
        "kind": "optical",
        "move": "hold",
        "screen": "green",
        "look": "hologram-red",
        "background": "black",
        "duration": 3.0,
        "shutter": 1,
    },
    "cel": {
        "title": "Cel",
        "desk": "Cel optical, optional key",
        "kind": "optical",
        "move": "hold",
        "screen": "none",
        "look": "cartoon-cel",
        "background": "keep",
        "duration": 3.0,
        "shutter": 1,
    },
    "cel-hologram": {
        "title": "Cel hologram",
        "desk": "Cel into hologram printer",
        "kind": "optical",
        "move": "hold",
        "screen": "green",
        "look": "toon-hologram",
        "background": "black",
        "duration": 3.0,
        "shutter": 1,
    },
    "rerun": {
        "title": "Rerun rig",
        "desk": "Replay a saved camera path on a new plate",
        "kind": "rig",
        "move": "flyby",
        "screen": "none",
        "look": "raw",
        "background": "keep",
        "duration": 3.0,
        "shutter": 3,
    },
}

ALIASES = {
    "toy-walk": "puppet-walk",
    "fly-across": "flyby",
    "come-closer": "push-in",
    "float": "hover",
    "ghost-message": "hologram-cyan",
    "alert-ghost": "hologram-red",
    "cartoon-show": "cel",
    "toon-ghost": "cel-hologram",
    "same-move": "rerun",
}

MOVES = {
    "hold": {"dx": 0, "dy": 0, "dz": 0.0, "bob": 0, "steps": 0},
    "flyby": {"dx": 520, "dy": -20, "dz": 0.06, "bob": 8, "steps": 1},
    "push-in": {"dx": 0, "dy": 0, "dz": 0.28, "bob": 0, "steps": 0},
    "hover": {"dx": 30, "dy": 0, "dz": 0.02, "bob": 28, "steps": 2},
    "heavy-steps": {"dx": 280, "dy": 0, "dz": 0.0, "bob": 18, "steps": 4},
    "creature-run": {"dx": 420, "dy": 0, "dz": 0.0, "bob": 26, "steps": 6},
    "peek": {"dx": 80, "dy": -10, "dz": 0.1, "bob": 6, "steps": 1},
}


def resolve_job(name: str) -> str:
    name = (name or "").strip()
    if name in JOBS:
        return name
    if name in ALIASES:
        return ALIASES[name]
    raise KeyError(f"Unknown finish {name!r}. Known: {sorted(JOBS)}")


def spec_for(name: str) -> dict:
    return JOBS[resolve_job(name)]


def list_jobs() -> list[dict]:
    return [{"id": job_id, **spec} for job_id, spec in JOBS.items()]
