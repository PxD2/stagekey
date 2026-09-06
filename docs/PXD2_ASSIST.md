# PxD2 assist — make Adversal minutes count

This is not a takeover brief. It is how PxD2 + Grok sit *after* Giulio's ingest and waste fewer of his minutes.

## Who we are on one page

- **PxD2** — Chad Peters. Independent shop. Public hall: https://pxd2.github.io/
- Background: Parallel Memory Optimized Compute (.PMOC) work during AMD North America software-development pilots. That is memory and repeatable compute discipline, not a claim that we speak for AMD.
- **StageKey** — local optical finish + multi-look farm. https://github.com/PxD2/stagekey
- **Grok (xAI)** — paid planning and code backbone. Writes the farm cards, grades takes, keeps the repo honest. Does not host `adversal-cli`.
- **Local Mistral** — same cards when the desk is offline.

Resume use is allowed: "film-desk integration partner for an MCP video-understand service; Grok-planned multi-look finish; measured minute discipline." Do not write "we rebuilt Adversal."

## What "more efficient" means (allowed)

Efficiency here is *his pipeline used better*, not *his pipeline rewritten*.

1. **Do not pay twice for the same bytes.** Hash first. Reuse `request_id`. His own docs already say this. StageKey `ingest` stores the MD5 locally so an agent cannot "helpfully" resubmit.
2. **Do not queue blind.** Check quota. Skip dead takes Grok/Mistral already rejected from a still or a short slate.
3. **Do not download the ocean.** Pull the report + the frames the farm will actually print, not every intermediate.
4. **Do not understand in-process.** Multi-hour decode stays on Adversal. StageKey never grows an in-RAM keyframe crawler.
5. **Measure the loop.** Minutes submitted → artifacts used → looks printed → looks kept. That ratio is the only efficiency number that belongs on a resume.

## What "more efficient" does not mean (forbidden)

- Replacing `process_video`.
- Shipping a rival watch cloud.
- Asking for their model weights or internal queue code on day one.
- Telling Giulio his architecture is wrong.

If we ever propose a change *inside* Adversal, it is a measured patch he asked for (example: a stable `get_by_md5` and `download_into_cwd`). Until he asks, we consume the public MCP.

## Pilot we can run with the 500 minutes

One clip, written up as a one-page case:

| Step | Owner | Success |
| --- | --- | --- |
| Submit once | Adversal | `request_id`, no second hash |
| Wait async | Adversal | agent not blocked |
| Plan N looks | Grok (or Mistral offline) | farm JSON |
| Print N looks | StageKey | files on disk |
| Keep 1–2 | human + Grok | wasted minutes named |

That write-up is the resume artifact for PxD2 *and* a polite gift for Giulio ("your minutes produced usable plates, here is the waste we cut").
