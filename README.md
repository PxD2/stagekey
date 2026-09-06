---
title: Stage Coach
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

# Stage Coach

Professional finish floor for long-form sources.

[Adversal](https://adversal.ai) is the workflow ingest MCP — the offer Giulio made. Coach uses it for Markdown and synced frames. This repo keys, grades, and farms the plates.

Company pack: [pxd2.github.io](https://pxd2.github.io/)  
Workflow: [docs/STAGECOACH.md](docs/STAGECOACH.md)  
Ingest: [docs/ADVERSAL.md](docs/ADVERSAL.md)  
Grok Build: [docs/GROK.md](docs/GROK.md)

## Workflow

```bash
python -m stagekey coach interview.mp4 --jobs hologram-cyan,cel --name slate_01
```

```
source → Adversal understand → Coach select → StageKey finish → reel
```

## Floor

```bash
python -m stagekey stage screen.mp4 --screen green --look hologram-cyan --background black
python -m stagekey farm plate.png --jobs hologram-cyan,hologram-red,cel --name slate_01
python -m stagekey go plate.png --move heavy-steps --shutter 5
python app.py
```

## Install

FFmpeg on PATH. Python 3.10+ (3.13+ for `adversal-cli`).

```bash
python -m pip install -e .
python -m pip install adversal-cli
grok mcp add adversal -- adversal-cli
grok mcp add stagekey -- python app.py
```
