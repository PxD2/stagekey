"""Kid desk on the left. Full studio on the right. Also an MCP server."""
from __future__ import annotations
import json
import gradio as gr
from stagekey.jobs import JOBS
from stagekey.studio import make_movie, studio_bible

JOB_CHOICES = [f"{spec['kid']}  —  {job_id}" for job_id, spec in JOBS.items()]

def _job_id(label: str) -> str:
    return label.split("—")[-1].strip() if "—" in label else label.strip()

def kid_make(media, job_label, title):
    """One big button. A kid can finish a shot."""
    if media is None:
        raise gr.Error("Add a picture or a video first.")
    job = _job_id(job_label)
    card = make_movie(media, job=job, name=title or job)
    return card["shot"], json.dumps(card, indent=2)

def bible():
    return json.dumps(studio_bible(), indent=2)

with gr.Blocks(title="StageKey Studio") as demo:
    gr.Markdown("# StageKey Studio\nBig buttons for kids. Go-motion, motion-control, and optical printing underneath.")
    with gr.Tab("Make a shot"):
        media = gr.File(label="Picture or video", file_types=["image", "video"])
        job = gr.Radio(JOB_CHOICES, value=JOB_CHOICES[0], label="What should it do?")
        title = gr.Textbox(value="My shot", label="Shot name")
        go = gr.Button("Make the shot", variant="primary")
        movie = gr.Video(label="Shot")
        card = gr.Code(language="json", label="Shot card")
        go.click(kid_make, [media, job, title], [movie, card])
    with gr.Tab("Studio bible"):
        box = gr.Code(language="json")
        gr.Button("Open bible").click(bible, outputs=box)

if __name__ == "__main__":
    demo.launch(mcp_server=True, ssr_mode=False)
