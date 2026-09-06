# StageKey x Adversal

Giulio Donninelli (Adversal) asked whether an MCP video-ingestion server belongs on the StageKey roadmap.

**Yes.** Split the work:

| Desk | Who | Job |
| --- | --- | --- |
| Understand long video | Adversal MCP (`adversal-cli`) | Hash + upload, queue remotely, return Markdown + synced frames. Do not block the agent. |
| Finish the plate | StageKey | Chroma key, hologram, cartoon, go-motion, motion-control rerun, optical stack, reel. |
| Plan / code / GitHub | Grok | Architecture, shot cards, repo work. Grok chat is **not** an MCP host for `adversal-cli`. |

Adversal already said the hard part out loud: extracting keyframes from multi-hour video inside an agent process is memory-heavy. StageKey should never try to become that service.

## Install Adversal (their docs)

Python 3.13+, ffmpeg/ffprobe on PATH.

```bash
python -m pip install adversal-cli
# macOS
brew install ffmpeg
# Debian / Ubuntu
sudo apt install ffmpeg
# Windows
winget install ffmpeg
```

Auth is browser-based. No API key in MCP config. Token: `~/.adversal/auth.txt`.

Claude Code:

```bash
claude mcp add adversal -- adversal-cli
```

If a tool returns `AUTHENTICATION REQUIRED`, call `authenticate`, finish the browser sign-in, retry the tool. Do not restart MCP.

## Dual MCP on a local client

Put both servers on Cursor / Claude Code / OpenCode. Copy `docs/mcp.example.json`.

Typical Adversal tools (from their public MCP page):

- `authenticate`
- `process_video` — returns `request_id` in seconds, does not download the artifact
- `check_video_status` / `get_request_id`
- download frames / download report

Rules they document:

- Check quota before submit.
- Do not submit the same video bytes twice. Reuse `request_id`.
- A completed job whose artifact is missing can be released and submitted again.

## StageKey CLI bridge

```bash
python -m stagekey ingest-probe
python -m stagekey ingest path/or/url.mp4
python -m stagekey ingest-status REQUEST_ID --wait
python -m stagekey ingest-pull REQUEST_ID --dest adversal_out
python -m stagekey movie adversal_out/frame_0001.png --job ghost-message --name ghost
```

`ingest` talks to `adversal-cli` when it is on PATH. If the binary's flags differ from what we probe, the command stores a local job card and prints `--help` so we can pin exact flags later.

## What Grok can and cannot do in this chat

Grok can write StageKey, push GitHub, and tell you the exact local commands.

Grok cannot attach `adversal-cli` as a live MCP server inside this hosted chat. Run Adversal + StageKey MCP on your machine (or Hugging Face Gradio MCP for StageKey via `python app.py`). Bring the Markdown / frames back here when you want Grok to grade a shot.

## Reply we can send Giulio

See `docs/REPLY_ADVERSAL.md`.
