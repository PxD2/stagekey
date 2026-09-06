"""Stage Coach floor. MCP server for the same tools."""
from __future__ import annotations

import json
import gradio as gr

from stagekey.jobs import JOBS
from stagekey.studio import make_movie, studio_bible

JOB_CHOICES = [f"{spec['title']}  —  {job_id}" for job_id, spec in JOBS.items()]


def _job_id(label: str) -> str:
    return label.split("—")[-1].strip() if "—" in label else label.strip()


def finish(media, job_label, title):
    if media is None:
        raise gr.Error("Load a plate first.")
    job = _job_id(job_label)
    card = make_movie(media, job=job, name=title or job)
    return card["shot"], json.dumps(card, indent=2)


def bible():
    return json.dumps(studio_bible(), indent=2)


with gr.Blocks(title="Stage Coach", theme=gr.themes.Base()) as demo:
    gr.Markdown(
        "# Stage Coach\n"
        "Adversal understands the source. This floor finishes the plate."
    )
    with gr.Tab("Finish"):
        media = gr.File(label="Plate", file_types=["image", "video"])
        job = gr.Radio(JOB_CHOICES, value=JOB_CHOICES[0], label="Finish")
        title = gr.Textbox(value="slate_01", label="Slate")
        go = gr.Button("Finish", variant="primary")
        movie = gr.Video(label="Take")
        card = gr.Code(language="json", label="Card")
        go.click(finish, [media, job, title], [movie, card])
    with gr.Tab("Bible"):
        box = gr.Code(language="json")
        gr.Button("Open").click(bible, outputs=box)

if __name__ == "__main__":
    demo.launch(mcp_server=True, ssr_mode=False)
