"""Gradio UI + MCP server. Every function is a tool."""

from __future__ import annotations

import json
from pathlib import Path

import gradio as gr

from stagekey.engine import apply_cartoon, apply_hologram, list_modes, stage
from stagekey.prompts import build_plate_prompt

OUT = Path("/tmp/stagekey")
OUT.mkdir(exist_ok=True)


def tool_list_modes() -> str:
    """List StageKey screens, hologram styles, and cartoonist modes."""
    return json.dumps(list_modes(), indent=2)


def tool_build_plate_prompt(
    subject: str,
    screen: str = "green",
    cartoonist: str = "off",
    hologram: str = "off",
) -> str:
    """Compile a video-model prompt that is easy to chroma-key later.

    Args:
        subject: Who or what is in front of the screen.
        screen: green, blue, or black void plate.
        cartoonist: off, anime, cel, comic, ink, newsprint, pop, chibi, noir.
        hologram: off, cyan, red, amber, ghost.
    """
    return json.dumps(
        build_plate_prompt(subject, screen, cartoonist, hologram),
        indent=2,
    )


def tool_stage(
    video: str,
    screen: str = "green",
    look: str = "hologram-cyan",
    background: str = "black",
) -> str:
    """Finish a plate: key green/blue, apply hologram or cartoon, composite.

    Args:
        video: Path to the source video.
        screen: green, blue, or none.
        look: raw, hologram-cyan/red/amber/ghost, cartoon-anime/cel/comic/ink/newsprint/pop/noir, toon-hologram.
        background: black, keep, transparent, a #hex color, or a background file path.
    """
    if not video:
        raise gr.Error("Upload or pass a video path.")
    dest = OUT / "staged.mp4"
    return stage(video, screen=screen, look=look, background=background, output=str(dest))


def tool_hologram(video: str, style: str = "cyan", screen: str = "green") -> str:
    """Black-hologram grade. Keys green/blue first when screen is set.

    Args:
        video: Source video path.
        style: cyan, red, amber, or ghost.
        screen: green, blue, or none.
    """
    dest = OUT / f"holo_{style}.mp4"
    return apply_hologram(video, style=style, output=str(dest), screen=screen)


def tool_cartoon(video: str, mode: str = "anime", screen: str = "none") -> str:
    """Cartoonist look.

    Args:
        video: Source video path.
        mode: anime, cel, comic, ink, newsprint, pop, noir.
        screen: green, blue, or none. Use none if the plate is already isolated.
    """
    dest = OUT / f"toon_{mode}.mp4"
    return apply_cartoon(video, mode=mode, output=str(dest), screen=screen)


with gr.Blocks(title="StageKey") as demo:
    gr.Markdown(
        """
        # StageKey
        Super simple plate finisher. Green / blue key, black hologram, cartoonist modes.
        This Space is also an MCP server.
        """
    )
    modes = gr.JSON(value=list_modes(), label="Modes")
    with gr.Tab("Stage (one shot)"):
        src = gr.Video(label="Plate")
        screen = gr.Radio(["green", "blue", "none"], value="green", label="Screen")
        look = gr.Dropdown(
            [
                "raw",
                "hologram-cyan",
                "hologram-red",
                "hologram-amber",
                "hologram-ghost",
                "cartoon-anime",
                "cartoon-cel",
                "cartoon-comic",
                "cartoon-ink",
                "cartoon-newsprint",
                "cartoon-pop",
                "cartoon-noir",
                "toon-hologram",
            ],
            value="hologram-cyan",
            label="Look",
        )
        background = gr.Textbox(value="black", label="Background (black | keep | transparent | #hex | file)")
        go = gr.Button("Stage", variant="primary")
        out = gr.Video(label="Result")
        go.click(tool_stage, [src, screen, look, background], out)
    with gr.Tab("Plate prompt"):
        subject = gr.Textbox(label="Subject", value="a jazz saxophonist in a tailored suit")
        p_screen = gr.Radio(["green", "blue", "black"], value="green")
        p_toon = gr.Dropdown(["off", "anime", "cel", "comic", "ink", "newsprint", "pop", "chibi", "noir"], value="off")
        p_holo = gr.Dropdown(["off", "cyan", "red", "amber", "ghost"], value="off")
        p_btn = gr.Button("Compile prompt")
        p_out = gr.Code(language="json")
        p_btn.click(tool_build_plate_prompt, [subject, p_screen, p_toon, p_holo], p_out)


if __name__ == "__main__":
    demo.launch(mcp_server=True, ssr_mode=False)
