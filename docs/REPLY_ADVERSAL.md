Subject: Re: Question on stagekey video pipeline

Hi Giulio,

Yes — a remote MCP ingest server belongs on StageKey's roadmap, and we would rather use yours than rebuild it.

StageKey's job is the finish: green/blue pull, black-studio hologram grades, cartoonist opticals, go-motion shutter, and repeatable motion-control rigs. Hugging Face generators give us a plate. We do not want the agent process to hold multi-hour decode + keyframe extraction in RAM.

Split we are shipping in https://github.com/PxD2/stagekey :

1. Adversal MCP understands a local file or public URL asynchronously (MD5 reuse, request_id, Markdown + synced frames).
2. StageKey MCP / CLI finishes selected frames or derived plates locally with FFmpeg.
3. Agents (Claude Code, Cursor, and Grok on the repo) orchestrate. Grok is the long-lived planning/code tool; Adversal is the remote watch desk.

We added `stagekey ingest | ingest-status | ingest-pull` plus docs/ADVERSAL.md so a developer can run both servers on one client. Happy to take the 500 free minutes and pin exact `adversal-cli` flags with you so the adapter is not heuristic.

If you want a tighter loop: expose a stable "download frames into $CWD" tool and a "same-bytes lookup by MD5" tool. That is the whole contract StageKey needs.

Best,
Chad Peters
PxD2
https://github.com/PxD2/stagekey
pxdsquared@gmail.com
