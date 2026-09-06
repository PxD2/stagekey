# Studio desks — dual and multi mode

Giulio's Adversal MCP and StageKey are not rivals. They sit on different benches.

```
long video or URL
        |
        v
 Adversal MCP          understand desk (remote, async)
 Markdown + frames     MD5 reuse, request_id, quota
        |
        +------------------+------------------+
        v                  v                  v
 Super Grok           local Mistral        human kid desk
 (online planner)     (Ollama offline)     (app.py buttons)
 shot card JSON       same JSON schema     same jobs
        |
        v
 StageKey farm         finish desk (local FFmpeg)
 many looks at once    hologram / cel / go-motion / reel
```

## Who owns what

| Desk | Owner | Allowed to do | Must not do |
| --- | --- | --- | --- |
| Understand | Adversal | Ingest hours of video, return notes + frames | Become a color-finishing house |
| Plan online | Super Grok | Pick jobs, write cards, code the repo, grade takes | Pretend to host adversal-cli inside grok.com chat |
| Plan offline | Mistral via Ollama | Same cards when the ranch has no WAN | Invent a second ingest cloud |
| Finish | StageKey / PxD2 | Key, grade, go-motion, optical stack, multi-render farm | Re-extract multi-hour keyframes in-process |

That map is how PxD2 assists Adversal instead of stepping on them. Their minutes get used. Our printer gets used. Grok is the multi-render brain, not a clone of their pipeline.

## Dual MCP (local host)

One client process can hold both servers: Claude Code, Cursor, or an Ollama MCP bridge.

```json
{
  "mcpServers": {
    "adversal": { "command": "adversal-cli" },
    "stagekey": { "command": "python", "args": ["app.py"] }
  }
}
```

Offline Mistral does **not** replace Adversal. It only plans which StageKey jobs to run after frames exist. Use Ollama (`mistral-small` / `mistral`) plus a bridge if you want the local model to call those MCP tools. Small local models are fine for "run ghost-message and cartoon-cel on frame 12". They are weak at long-video understanding — that is why Giulio's service exists.

## Super Grok as the multi-render tool

Grok's job on a take:

1. Read Adversal Markdown (what happened in the source).
2. Pick 3–9 StageKey jobs, not one.
3. Emit a farm card.
4. You run `python -m stagekey farm plate.png --jobs ghost-message,alert-ghost,cartoon-show --planner grok`.
5. Grok grades the reel and the shot cards.

Same card works if the planner string is `mistral` after an overnight Ollama pass.

## Partnership tone with Giulio

Say this, not "we also ingest video":

- StageKey will send watch-work to Adversal.
- StageKey will not ship a competing keyframe cloud.
- PxD2 + Grok will be a finish + multi-look farm that consumes their artifacts.
- We want their stable download-to-cwd and MD5-lookup tools so the farm is deterministic.
