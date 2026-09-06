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

PxD2 ships this desk in the open so the firm sits on a real stack with other shops — not a closed hallway. Company pack: [pxd2.github.io](https://pxd2.github.io/). Close clock and terms live there. This repo is the public printer.

72-hour desk: [ROADMAP.md](ROADMAP.md)

## The stack

| Desk | Partner | Job |
| --- | --- | --- |
| Understand | [Adversal](https://adversal.ai) MCP | Long video or URL → Markdown + synced frames |
| Finish | StageKey | Key, hologram, cartoon, go-motion, farm, reel |
| Plan | Any agent on the client | Pick jobs, write the farm card |
| Offline plan | Local Mistral (Ollama) | Same card when the desk has no WAN |

Adversal asked if MCP ingest fits the roadmap. It does. They are not investors. They are a desk we plug in so StageKey does not pretend to watch multi-hour video alone.

Dual client config: [docs/mcp.example.json](docs/mcp.example.json). Ingest notes: [docs/ADVERSAL.md](docs/ADVERSAL.md).

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
