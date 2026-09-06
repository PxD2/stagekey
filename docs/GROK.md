# Grok as the StageKey agent

PxD2 works in Grok. Claude is not required.

Adversal's docs show `claude mcp add` because that is one client. The same `adversal-cli` binary attaches to Grok Build.

Official MCP on Grok Build: https://x.ai/docs/build/features/mcp-servers

## Install Grok Build

macOS / Linux / WSL:

```bash
curl -fsSL https://x.ai/cli/install.sh | bash
grok login
```

Windows PowerShell:

```powershell
irm https://x.ai/cli/install.ps1 | iex
grok login
```

## Attach both desks

From the StageKey repo:

```bash
python -m pip install adversal-cli
python -m pip install -e .

grok mcp add adversal -- adversal-cli
grok mcp add stagekey -- python app.py
grok mcp list
grok mcp doctor adversal
```

Or copy [grok.config.toml.example](grok.config.toml.example) to `~/.grok/config.toml` (user-wide) or `.grok/config.toml` (this repo only).

Then:

```bash
cd /path/to/stagekey
grok
```

Ask Grok in that terminal to `ingest` a clip and `farm` the frames. Grok is the agent. Adversal is ingest. StageKey is finish.

## This grok.com chat

The chat you are in already drives the GitHub repo. It does not replace Grok Build on the machine that has `adversal-cli` and ffmpeg. Use both: this chat for the repo and the close; Grok Build in the project folder for MCP tool calls.

Connectors on grok.com that speak HTTP can also be added under Custom MCP if a server is reachable at a URL. Local `adversal-cli` is stdio, so Grok Build on the box is the direct path.
