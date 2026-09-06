---
title: StageKey Studio
emoji: 🎬
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 5.49.1
app_file: app.py
pinned: false
license: apache-2.0
tags:
  - mcp-server
  - go-motion
  - motion-control
  - chroma-key
  - hologram
  - video
---

# StageKey Studio

A film desk a kid can press, and a crew can finish.

Company pack: [pxd2.github.io](https://pxd2.github.io/). Close clock and terms live there.

72-hour desk: [ROADMAP.md](ROADMAP.md)

## How a long video gets here

[Adversal](https://adversal.ai) offered an MCP ingest server and early-developer minutes. StageKey uses that offer: their service returns Markdown and synced frames. This repo finishes the plate (key, hologram, cartoon, go-motion, farm).

Install notes: [docs/ADVERSAL.md](docs/ADVERSAL.md). Client example: [docs/mcp.example.json](docs/mcp.example.json).

## Kid desk

```bash
python -m stagekey movie toy.png --job toy-walk --name walker
python -m stagekey farm toy.png --jobs ghost-message,alert-ghost,cartoon-show
```

Open the kid UI: `python app.py`

## Crew desk

```bash
python -m stagekey go plate.png --move heavy-steps --shutter 5
python -m stagekey stage screen.mp4 --screen green --look hologram-cyan --background black
python -m stagekey ingest long-interview.mp4
python -m stagekey ingest-status REQUEST_ID --wait
python -m stagekey ingest-pull REQUEST_ID --dest adversal_out
```

## Install

FFmpeg on PATH. Python 3.10+ (3.13+ for `adversal-cli`).

```bash
python -m pip install -e .
python -m stagekey bible
```
