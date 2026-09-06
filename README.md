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

**72-hour close desk (through 8 Sep 2026, 12:43 Arizona):** [ROADMAP.md](ROADMAP.md)  
Company pack (not an offering): [pxd2.github.io](https://pxd2.github.io/)

The front has jobs with plain names. Under the floor are three original-trilogy techniques that still beat a one-shot generator:

1. **Go-motion** — the puppet moves *while the shutter is open*.
2. **Motion control** — the same camera path is a JSON rig.
3. **Optical printing** — key, hologram, cartoon stacked in order.

## Two desks, one agent

| Layer | Tool | Does |
| --- | --- | --- |
| Understand long video | [Adversal MCP](https://adversal.ai) (`adversal-cli`) | Upload / URL → remote queue → Markdown + synced frames |
| Finish the plate | StageKey | Key, hologram, cartoon, go-motion, farm, reel |
| Plan | Grok (online) or local Mistral | Farm cards. Grok chat is not an MCP host for Adversal |

See [docs/ADVERSAL.md](docs/ADVERSAL.md). Dual-server config: [docs/mcp.example.json](docs/mcp.example.json).

## Kid desk

```bash
python -m stagekey movie toy.png --job toy-walk --name walker
python -m stagekey farm toy.png --jobs ghost-message,alert-ghost,cartoon-show --planner grok
```

Open the kid UI: `python app.py`

## Crew desk

```bash
python -m stagekey go plate.png --move heavy-steps --shutter 5
python -m stagekey stage screen.mp4 --screen green --look hologram-cyan --background black
python -m stagekey ingest long-interview.mp4
```

## Install

FFmpeg on PATH. Python 3.10+ (3.13+ for `adversal-cli`).

```bash
python -m pip install -e .
python -m stagekey bible
```
