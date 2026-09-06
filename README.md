---
title: StageKey
emoji: 🟩
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 5.49.1
app_file: app.py
pinned: false
license: apache-2.0
tags:
  - mcp-server
  - chroma-key
  - hologram
  - cartoon
  - video
---

# StageKey

An MCP that did not exist: **one tool** that finishes AI video plates for

- green screen
- blue screen
- black hologram (cyan / red / amber / ghost)
- cartoonist modes (anime, cel, comic, ink, newsprint, pop, noir)
- toon + hologram stacked

Generic video MCPs expose a chroma-key slider. StageKey is a **stage language** for generated plates: compile the prompt, pull the screen, drop the subject on black, grade the look.

No GPU required for the finish. FFmpeg only.

## Super simple

```bash
python -m stagekey prompt "a dancer in a windbreaker" --screen green --hologram cyan
python -m stagekey stage plate.mp4 --screen green --look hologram-cyan --background black
```

Or one MCP call:

```
stage(video, screen="green", look="hologram-cyan", background="black")
```

## Beyond-simple looks

| look | what you get |
| --- | --- |
| `raw` | clean key only |
| `hologram-cyan` | scanlines, teal glow, chromatic split, flicker on black |
| `hologram-red` | emergency / alert hologram |
| `hologram-amber` | tactical HUD hologram |
| `hologram-ghost` | faint unstable projection |
| `cartoon-anime` | cel shade + line |
| `cartoon-cel` | Saturday-morning flats |
| `cartoon-comic` | ink + print grain |
| `cartoon-ink` | brush comic |
| `cartoon-newsprint` | pulpy strip |
| `cartoon-pop` | poster graphic |
| `cartoon-noir` | graphic-novel ink |
| `toon-hologram` | cartoon, then cyan hologram |

Background can be `black`, `keep`, `transparent` (WebM alpha), a `#hex`, or another video/image.

## MCP

Gradio launch already serves MCP:

```bash
pip install -r requirements.txt
python app.py
```

Client:

```json
{
  "mcpServers": {
    "stagekey": {
      "command": "python",
      "args": ["app.py"],
      "cwd": "/path/to/stagekey"
    }
  }
}
```

After you push this as a Hugging Face Space:

```
https://<user>-stagekey.hf.space/gradio_api/mcp/sse
```

Add it at https://huggingface.co/settings/mcp next to the official Hub MCP.

Tools the agent sees:

- `tool_list_modes`
- `tool_build_plate_prompt`
- `tool_stage`
- `tool_hologram`
- `tool_cartoon`

## Full HF workflow

1. `tool_build_plate_prompt` → copy into Wan 2.1 / LTX-2 / MiniMax H3 / Helios.
2. Save the clip.
3. `tool_stage` with `screen=green` and `look=hologram-cyan`.
4. Composite over any set later (`background=/path/to/set.mp4`).

Do **not** bake the final set into the generation if you want to re-key.

## Install

```bash
# ffmpeg must be on PATH
python -m pip install -e .
python -m stagekey modes
```
