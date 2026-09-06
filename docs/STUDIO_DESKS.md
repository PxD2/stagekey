# Studio desks

PxD2 stands up a stack with other shops so the firm is grounded in tools people already pay for.

```
long video or URL
        ↓
 Adversal MCP              understand
 Markdown + frames
        ↓
 Agent (online or local)   plan the farm card
        ↓
 StageKey farm             finish many looks
 reel
```

| Desk | Owner | Does |
| --- | --- | --- |
| Understand | Adversal | Ingest hours of video, return notes + frames |
| Plan | Local client agent, or Mistral on Ollama | Pick StageKey jobs |
| Finish | StageKey / PxD2 | Key, grade, go-motion, farm, reel |

Adversal is a partner desk. Not an investor. Not a rival we rewrite.

## Dual MCP

```json
{
  "mcpServers": {
    "adversal": { "command": "adversal-cli" },
    "stagekey": { "command": "python", "args": ["app.py"] }
  }
}
```

## Farm

```bash
python -m stagekey farm plate.png --jobs ghost-message,alert-ghost,cartoon-show --planner agent
```
