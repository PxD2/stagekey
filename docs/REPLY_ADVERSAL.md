Subject: Re: Question on stagekey video pipeline

Hi Giulio,

Yes — a remote MCP ingest server belongs on StageKey's roadmap, and we would rather use yours than rebuild it.

StageKey's job is the finish: green/blue pull, black-studio hologram grades, cartoonist opticals, go-motion shutter, and a multi-look farm. Hugging Face generators and live plates give us a frame. We do not want the agent process to hold multi-hour decode + keyframe extraction in RAM. That watch work should stay on Adversal.

How PxD2 would like to work with you:

1. Adversal MCP understands a local file or public URL asynchronously (MD5 reuse, request_id, Markdown + synced frames).
2. StageKey MCP / CLI finishes selected frames as many looks at once (hologram cyan, alert red, cel, go-motion).
3. Super Grok plans the farm online. A local Mistral (Ollama) can plan the same JSON card offline. Neither planner replaces your ingest server.
4. Agents (Claude Code, Cursor, OpenCode) host both MCP servers on one client. Grok stays the long-lived planning and repo tool.

Repo: https://github.com/PxD2/stagekey
Docs: docs/ADVERSAL.md and docs/STUDIO_DESKS.md

Happy to take the 500 free minutes and pin exact adversal-cli flags with you. The contract we need from your side is small and stable: download frames into $CWD, and look up a job by MD5 so we never resubmit the same bytes.

We are not building a second watch cloud. We want to send you minutes and print the frames.

Best,
Chad Peters
PxD2
https://github.com/PxD2/stagekey
pxdsquared@gmail.com
