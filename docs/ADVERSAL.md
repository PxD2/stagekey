# Adversal

Thank you to Giulio Donninelli and Adversal for the early-developer processing minutes and for asking whether MCP ingest belongs on this repo.

We accept that offer. Today we start wiring Stage Coach around it and will see where the work leads.

Adversal understands the source. StageKey finishes the plate.

Product: https://adversal.ai

## Install

Python 3.13+, ffmpeg on PATH.

```bash
python -m pip install adversal-cli
grok mcp add adversal -- adversal-cli
```

Sign in through the browser when asked. Follow their quota rules. Do not submit the same bytes twice.

## Coach

```bash
python -m stagekey coach SOURCE --jobs hologram-cyan,cel --name slate_01
```
