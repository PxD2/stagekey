# Adversal ingest

Giulio offered Adversal's MCP and early-developer minutes. We use that offer.

StageKey finishes plates after Adversal returns Markdown and frames.

## Install

Python 3.13+, ffmpeg on PATH.

```bash
python -m pip install adversal-cli
```

Attach it to the agent you actually use. For PxD2 that is Grok Build:

```bash
grok mcp add adversal -- adversal-cli
```

The same binary works in any MCP client. Adversal's own page shows a Claude example. That is an example, not a requirement.

Sign in through the browser when the MCP asks. Token: `~/.adversal/auth.txt`.

## Use

```bash
python -m stagekey ingest VIDEO_OR_URL
python -m stagekey ingest-status REQUEST_ID --wait
python -m stagekey ingest-pull REQUEST_ID --dest adversal_out
```

Or ask Grok Build, after the two MCP servers are attached, to run those steps.

Check quota. Do not submit the same bytes twice. Reuse `request_id`.

Product: https://adversal.ai
Grok wiring: [GROK.md](GROK.md)
