# Stage Coach

Professional floor for StageKey. Not a toy desk.

Adversal is the workflow ingest MCP Giulio offered. Coach uses it, then finishes.

```
source (file or URL)
        ↓
Adversal MCP     understand — Markdown + synced frames
        ↓
Coach            select plates
        ↓
StageKey         finish — key, hologram, cel, go-motion, farm
        ↓
reel
```

## Run

```bash
python -m stagekey coach interview.mp4 --jobs hologram-cyan,cel --name slate_01
```

If `adversal-cli` is signed in, Coach queues the source, waits, pulls artifacts, farms the first plates. If the CLI is not on the box yet, Coach still finishes a local plate you pass as the source.

Attach MCP on Grok Build:

```bash
grok mcp add adversal -- adversal-cli
grok mcp add stagekey -- python app.py
```

Then ask Grok Build to run Coach on a clip.

## Finishes

| id | Floor |
| --- | --- |
| puppet-walk | Go-motion walk |
| flyby | Locked path |
| push-in | Repeatable move in |
| hover | Soft shutter hover |
| hologram-cyan | Key + cyan optical |
| hologram-red | Key + red optical |
| cel | Cel pass |
| cel-hologram | Cel into hologram |
| rerun | Replay a saved rig |
