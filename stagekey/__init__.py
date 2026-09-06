"""StageKey Studio — keyed plates, go-motion, motion-control, optical print."""

from .engine import stage, key_screen, apply_hologram, apply_cartoon, list_modes
from .gomotion import apply_rig, go_motion
from .jobs import JOBS, list_jobs
from .prompts import build_plate_prompt
from .studio import assemble_reel, make_movie, make_shot, studio_bible

__version__ = "0.2.0"
__all__ = [
    "stage", "key_screen", "apply_hologram", "apply_cartoon", "list_modes",
    "build_plate_prompt", "go_motion", "apply_rig", "make_shot", "make_movie",
    "assemble_reel", "studio_bible", "list_jobs", "JOBS",
]
