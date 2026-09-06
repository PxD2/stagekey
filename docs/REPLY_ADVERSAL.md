Subject: Re: Question on stagekey video pipeline

Hi Giulio,

Thank you for writing, and for the early-developer minutes.

Yes — an MCP ingest server fits what StageKey needs. Local keyframe extraction on long video is the part we do not want inside the agent. We will use Adversal the way you described: process_video, request_id, Markdown and synced frames, no duplicate submits.

StageKey stays the finish step after your artifacts land. We are not building a watch service.

Notes on our side:
https://github.com/PxD2/stagekey/blob/main/docs/ADVERSAL.md

Happy to take the 500 minutes on a first clip and follow your install docs.

Thank you again for reaching out.

Chad Peters
PxD2
https://github.com/PxD2/stagekey
pxdsquared@gmail.com
