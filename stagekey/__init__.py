"""StageKey — keyed plates, black hologram, cartoonist looks."""

from .engine import stage, key_screen, apply_hologram, apply_cartoon, list_modes
from .prompts import build_plate_prompt

__version__ = "0.1.0"
__all__ = [
    "stage",
    "key_screen",
    "apply_hologram",
    "apply_cartoon",
    "list_modes",
    "build_plate_prompt",
]
