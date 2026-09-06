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

The front has jobs with plain names. Under the floor are three original-trilogy techniques that still beat a one-shot generator:

1. **Go-motion** — the puppet moves *while the shutter is open*, so the frame carries real blur instead of a chopped stop-motion stutter.
2. **Motion control** — the same camera path is a JSON rig. Run it on the beauty pass, then on the screen pass, then on the glow pass. They lock.
3. **Optical printing** — key, shadow, hologram, cartoon, tracers stacked in order, not hoped-for in a single prompt.

A giant model can invent a pretty shot once. It cannot repeat the move, hold the matte, or give you shutter-true blur on command. That is the competition.

## Two desks, one agent

| Layer | Tool | Does |
| --- | --- | --- |
| Understand long video | [Adversal MCP](https://adversal.ai) (`adversal-cli`) | Upload / URL → remote queue → Markdown + synced frames. Async. MD5 reuse. |
| Finish the plate | StageKey | Key, hologram, cartoon, go-motion, rerun a rig, reel. |
| Plan and code | Grok + this repo | Architecture and GitHub. Grok chat is not an MCP host for Adversal. |

See [docs/ADVERSAL.md](docs/ADVERSAL.md). Dual-server config: [docs/mcp.example.json](docs/mcp.example.json).

## Kid desk

```bash
python -m stagekey movie toy.png --job toy-walk --name walker
```

| Button the kid sees | What the desk actually does |
| --- | --- |
| Make the toy walk | Go-motion puppet, heavy shutter, stomp bob |
| Fly it across the sky | Motion-control flyby, saved rig |
| Walk the camera in | Repeatable push-in |
| Make it float | Hover go-motion |
| Ghost message on black | Pull green/blue, print cyan hologram |
| Red warning ghost | Same printer, red hologram |
| Turn it into a cartoon | Cel optical |
| Cartoon ghost | Cel then hologram |
| Do the same camera move again | Re-run camera.rig.json on a new plate |

Then cut:

```bash
python -m stagekey reel shotA.mp4 shotB.mp4 --name first-reel
```

Open the kid UI:

```bash
python app.py
```

Three steps: add a picture, pick a job, press **Make the shot**.

## Crew desk

```bash
python -m stagekey go plate.png --kind puppet --move heavy-steps --shutter 5
python -m stagekey rerun other-plate.png camera.rig.json
python -m stagekey stage screen.mp4 --screen green --look hologram-cyan --background black
python -m stagekey ingest long-interview.mp4
python -m stagekey ingest-status REQUEST_ID --wait
python -m stagekey ingest-pull REQUEST_ID --dest adversal_out
```

## Install

FFmpeg on PATH. Python 3.10+ (3.13+ if you also install `adversal-cli`).

```bash
python -m pip install -e .
python -m stagekey bible
python -m stagekey ingest-probe
```
