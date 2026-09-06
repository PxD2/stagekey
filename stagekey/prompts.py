"""Prompt compiler for generating clean studio plates in Wan / LTX / H3 / Helios."""

from __future__ import annotations

SCREENS = {
    "green": {
        "backdrop": (
            "perfectly flat seamless chroma-key GREEN SCREEN studio cyclorama, "
            "pure #00FF00 green wall and floor meeting with no wrinkle, no hot spot, "
            "even softbox lighting on the backdrop only"
        ),
        "negative": "wrinkled fabric, uneven green, spill on face, shadows on backdrop, grid, tracking marks",
    },
    "blue": {
        "backdrop": (
            "perfectly flat seamless chroma-key BLUE SCREEN studio cyclorama, "
            "pure #0040FF blue wall and floor, even lighting, no wrinkles"
        ),
        "negative": "wrinkled fabric, uneven blue, spill on face, shadows on backdrop",
    },
    "black": {
        "backdrop": (
            "infinite BLACK VOID cyclorama, subject isolated in a dark volume, "
            "rim light only, no visible set, no floor texture, true black background"
        ),
        "negative": "gray background, visible studio, floor grid, smoke filling frame, ambient fill",
    },
}

CARTOONIST = {
    "off": "",
    "anime": "Japanese anime still, clean cel shading, sharp lineart, studio lighting, 2D animation frame",
    "cel": "classic Saturday-morning cartoon cel, bold outlines, flat color fills, limited palette",
    "comic": "American comic-book panel, heavy ink outlines, Ben-Day dots, saturated print colors",
    "ink": "high-contrast black ink cartoon, brush outlines, spare hatching, cream paper",
    "newsprint": "newspaper comic strip, cheap pulpy halftone, limited ink, slightly off-register",
    "pop": "pop-art cartoon, Warhol flats, thick graphic outlines, poster colors",
    "chibi": "chibi cartoon proportions, oversized head, tiny body, sticker-clean lines",
    "noir": "noir graphic novel, hard ink shadows, limited palette, dramatic rim light",
}

HOLOGRAM = {
    "off": "",
    "cyan": "black-studio holographic projection, cyan-teal volumetric glow, scanlines, flicker, translucent",
    "red": "crimson emergency hologram, scanlines, black void, unstable flicker",
    "amber": "warm amber tactical hologram, military HUD feel, black void, scanlines",
    "ghost": "pale ghost hologram, faint scanlines, heavy transparency, black void",
}


def build_plate_prompt(
    subject: str,
    screen: str = "green",
    cartoonist: str = "off",
    hologram: str = "off",
    camera: str = "medium shot, 35mm, locked tripod, eye level",
) -> dict:
    """Build a generation prompt that is easy to key later.

    Returns prompt, negative prompt, and recommended StageKey finish settings.
    """
    screen = screen.lower().strip()
    if screen not in SCREENS:
        raise ValueError(f"screen must be one of {list(SCREENS)}")
    cartoonist = cartoonist.lower().strip()
    if cartoonist not in CARTOONIST:
        raise ValueError(f"cartoonist must be one of {list(CARTOONIST)}")
    hologram = hologram.lower().strip()
    if hologram not in HOLOGRAM:
        raise ValueError(f"hologram must be one of {list(HOLOGRAM)}")

    subject = subject.strip()
    parts = [
        subject.rstrip("."),
        SCREENS[screen]["backdrop"],
        camera,
        "subject sharply separated from the backdrop",
        "no motion blur on the backdrop",
        "single continuous take",
    ]
    if CARTOONIST[cartoonist]:
        parts.append(CARTOONIST[cartoonist])
    if HOLOGRAM[hologram]:
        parts.append(HOLOGRAM[hologram])

    prompt = ", ".join(p for p in parts if p)
    negative = (
        "blurry, extra limbs, watermark, subtitles, text overlay, logo, "
        "busy background, crowd, morphing face, "
        + SCREENS[screen]["negative"]
    )
    return {
        "prompt": prompt,
        "negative_prompt": negative,
        "screen": screen,
        "cartoonist": cartoonist,
        "hologram": hologram,
        "finish": {
            "screen": screen if screen in {"green", "blue"} else "none",
            "background": "black" if hologram != "off" else "keep",
            "look": f"hologram-{hologram}" if hologram != "off" else (
                f"cartoon-{cartoonist}" if cartoonist != "off" else "raw"
            ),
        },
        "tip": "Generate with this prompt, then call stage() on the file. Do not bake the final background into the plate if you want to re-composite.",
    }
