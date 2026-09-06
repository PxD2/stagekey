"""Kid names on the front. Studio technique on the back."""

from __future__ import annotations

JOBS = {
    "toy-walk": {"kid": "Make the toy walk", "desk": "Go-motion puppet walk with heavy shutter blur", "kind": "puppet", "move": "heavy-steps", "screen": "none", "look": "raw", "background": "black", "duration": 3.0, "shutter": 5},
    "fly-across": {"kid": "Fly it across the sky", "desk": "Motion-control flyby, locked path", "kind": "puppet", "move": "flyby", "screen": "none", "look": "raw", "background": "black", "duration": 3.0, "shutter": 4},
    "come-closer": {"kid": "Walk the camera in", "desk": "Dykstra-style push-in, repeatable rig", "kind": "rig", "move": "push-in", "screen": "none", "look": "raw", "background": "keep", "duration": 3.0, "shutter": 3},
    "float": {"kid": "Make it float", "desk": "Hover go-motion, soft shutter", "kind": "puppet", "move": "hover", "screen": "none", "look": "raw", "background": "black", "duration": 3.0, "shutter": 6},
    "ghost-message": {"kid": "Ghost message on black", "desk": "Blue/green pull + black hologram optical", "kind": "optical", "move": "hold", "screen": "green", "look": "hologram-cyan", "background": "black", "duration": 3.0, "shutter": 1},
    "alert-ghost": {"kid": "Red warning ghost", "desk": "Keyed plate + red hologram pass", "kind": "optical", "move": "hold", "screen": "green", "look": "hologram-red", "background": "black", "duration": 3.0, "shutter": 1},
    "cartoon-show": {"kid": "Turn it into a cartoon", "desk": "Cel optical + optional key", "kind": "optical", "move": "hold", "screen": "none", "look": "cartoon-cel", "background": "keep", "duration": 3.0, "shutter": 1},
    "toon-ghost": {"kid": "Cartoon ghost", "desk": "Cel pass into hologram printer", "kind": "optical", "move": "hold", "screen": "green", "look": "toon-hologram", "background": "black", "duration": 3.0, "shutter": 1},
    "same-move": {"kid": "Do the same camera move again", "desk": "Re-run a saved motion-control path on a new plate", "kind": "rig", "move": "flyby", "screen": "none", "look": "raw", "background": "keep", "duration": 3.0, "shutter": 3},
}

MOVES = {
    "hold": {"dx": 0, "dy": 0, "dz": 0.0, "bob": 0, "steps": 0, "kid": "Stay still"},
    "flyby": {"dx": 520, "dy": -20, "dz": 0.06, "bob": 8, "steps": 1, "kid": "Whoosh across"},
    "push-in": {"dx": 0, "dy": 0, "dz": 0.28, "bob": 0, "steps": 0, "kid": "Come closer"},
    "hover": {"dx": 30, "dy": 0, "dz": 0.02, "bob": 28, "steps": 2, "kid": "Float"},
    "heavy-steps": {"dx": 280, "dy": 0, "dz": 0.0, "bob": 18, "steps": 4, "kid": "Big stomps"},
    "creature-run": {"dx": 420, "dy": 0, "dz": 0.0, "bob": 26, "steps": 6, "kid": "Run"},
    "peek": {"dx": 80, "dy": -10, "dz": 0.1, "bob": 6, "steps": 1, "kid": "Peek in"},
}


def list_jobs() -> list[dict]:
    return [{"id": job_id, **spec} for job_id, spec in JOBS.items()]
