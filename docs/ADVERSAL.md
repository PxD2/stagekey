# Adversal ingest

Giulio Donninelli offered Adversal's MCP as a remote ingest path for StageKey and 500 processing minutes per month to early developers.

We accept that offer as users of the product he shipped.

StageKey finishes plates after Adversal returns Markdown and frames. We are not announcing a joint venture. We are wiring the client he documented.

## Install (from Adversal)

Python 3.13+, ffmpeg on PATH.

```bash
python -m pip install adversal-cli
claude mcp add adversal -- adversal-cli
```

Sign in through the browser when the MCP asks. Token: `~/.adversal/auth.txt`.

## Use

```bash
python -m stagekey ingest VIDEO_OR_URL
python -m stagekey ingest-status REQUEST_ID --wait
python -m stagekey ingest-pull REQUEST_ID --dest adversal_out
```

Follow their rules: check quota, do not submit the same bytes twice, reuse `request_id`.

Product: https://adversal.ai
