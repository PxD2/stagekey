# StageKey × Adversal

Adversal asked whether an MCP video-ingestion server belongs on StageKey's roadmap.

**Yes.** They are a desk in the stack. They are not a check.

| Desk | Who | Job |
| --- | --- | --- |
| Understand | Adversal MCP (`adversal-cli`) | Hash + upload, remote queue, Markdown + synced frames |
| Finish | StageKey | Key, hologram, cartoon, go-motion, farm, reel |
| Plan | Agent on the local client | Farm card from those frames |

StageKey does not ingest multi-hour video inside the agent process. That watch work stays on Adversal.

## Install

Python 3.13+, ffmpeg/ffprobe on PATH.

```bash
python -m pip install adversal-cli
claude mcp add adversal -- adversal-cli
```

Auth is browser-based. Token: `~/.adversal/auth.txt`.
If a tool returns `AUTHENTICATION REQUIRED`, call `authenticate`, finish the browser page, retry.

## Dual MCP

Copy [mcp.example.json](mcp.example.json) into the client that hosts both servers.

Adversal tools we consume:

- `authenticate`
- `process_video` — returns `request_id` immediately
- status / request lookup
- download frames / download report

Do not submit the same bytes twice. Reuse `request_id`. Check quota first.

## StageKey bridge

```bash
python -m stagekey ingest-probe
python -m stagekey ingest path/or/url.mp4
python -m stagekey ingest-status REQUEST_ID --wait
python -m stagekey ingest-pull REQUEST_ID --dest adversal_out
python -m stagekey farm adversal_out/frame.png --jobs ghost-message,cartoon-show
```

Reply draft: [REPLY_ADVERSAL.md](REPLY_ADVERSAL.md).
