# Roadmap answer for Adversal

**Question (Giulio Donninelli, Adversal, 2026-09):**  
Could an MCP-based video ingestion server fit into StageKey's roadmap?

**Answer:** Yes.

Adversal MCP is the StageKey **understand** desk.

- Ingest a local file or public URL through `adversal-cli`.
- Queue remotely. Return `request_id` immediately.
- Reuse the same bytes by MD5. Do not submit twice.
- Download Markdown and synced frames into the workspace.
- StageKey then finishes those frames (key, hologram, cartoon, go-motion).

StageKey will not grow its own multi-hour keyframe cloud. That work stays on Adversal.

How to run it:

```bash
python -m pip install adversal-cli
claude mcp add adversal -- adversal-cli
python -m stagekey ingest VIDEO_OR_URL
python -m stagekey ingest-status REQUEST_ID --wait
python -m stagekey ingest-pull REQUEST_ID --dest adversal_out
```

Docs: [docs/ADVERSAL.md](docs/ADVERSAL.md). Dual client config: [docs/mcp.example.json](docs/mcp.example.json).
