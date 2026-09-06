"""CLI: python -m stagekey stage plate.mp4 --screen green --look hologram-cyan"""

from __future__ import annotations

import argparse
import json

from .adversal import help_text, pipeline_card, pull, status, submit
from .engine import apply_cartoon, apply_hologram, list_modes, stage
from .gomotion import apply_rig, go_motion
from .jobs import list_jobs
from .prompts import build_plate_prompt
from .studio import assemble_reel, make_shot, studio_bible


def main() -> None:
    p = argparse.ArgumentParser(prog="stagekey", description="Key, hologram, cartoon, go-motion, Adversal ingest")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("stage", help="One-shot finish")
    s.add_argument("src")
    s.add_argument("--screen", default="green", choices=["green", "blue", "none"])
    s.add_argument("--look", default="raw")
    s.add_argument("--background", default="black")
    s.add_argument("--out", default=None)
    s.add_argument("--similarity", type=float, default=0.28)
    s.add_argument("--blend", type=float, default=0.12)

    h = sub.add_parser("hologram")
    h.add_argument("src")
    h.add_argument("--style", default="cyan", choices=["cyan", "red", "amber", "ghost"])
    h.add_argument("--screen", default="none")
    h.add_argument("--out", default=None)

    c = sub.add_parser("cartoon")
    c.add_argument("src")
    c.add_argument("--mode", default="anime")
    c.add_argument("--screen", default="none")
    c.add_argument("--out", default=None)

    pr = sub.add_parser("prompt", help="Compile a plate prompt for Wan/LTX/H3")
    pr.add_argument("subject")
    pr.add_argument("--screen", default="green")
    pr.add_argument("--cartoonist", default="off")
    pr.add_argument("--hologram", default="off")

    sub.add_parser("modes", help="Print available screens and looks")
    sub.add_parser("bible", help="Print the studio bible")
    sub.add_parser("jobs", help="List kid-desk jobs")

    mv = sub.add_parser("movie", help="Kid desk: one job, one shot")
    mv.add_argument("src")
    mv.add_argument("--job", default="toy-walk")
    mv.add_argument("--name", default="shot")
    mv.add_argument("--rig", default=None)

    go = sub.add_parser("go", help="Go-motion a plate")
    go.add_argument("src")
    go.add_argument("--kind", default="puppet")
    go.add_argument("--move", default="heavy-steps")
    go.add_argument("--shutter", type=int, default=5)
    go.add_argument("--duration", type=float, default=3.0)
    go.add_argument("--out", default=None)

    rr = sub.add_parser("rerun", help="Re-run a saved camera.rig.json")
    rr.add_argument("src")
    rr.add_argument("rig")
    rr.add_argument("--out", default=None)

    rl = sub.add_parser("reel", help="Concat finished shots")
    rl.add_argument("clips", nargs="+")
    rl.add_argument("--name", default="reel")
    rl.add_argument("--out", default=None)

    ing = sub.add_parser("ingest", help="Queue a video on Adversal (remote understand)")
    ing.add_argument("source", help="Local file or public URL")
    ing.add_argument("--artifact", default="report", help="report | frames | transcript")
    ing.add_argument("--wait", action="store_true")

    st = sub.add_parser("ingest-status", help="Check an Adversal request_id")
    st.add_argument("request_id")
    st.add_argument("--wait", action="store_true")

    pl = sub.add_parser("ingest-pull", help="Download Adversal artifacts")
    pl.add_argument("request_id")
    pl.add_argument("--dest", default="adversal_out")

    sub.add_parser("ingest-probe", help="See if adversal-cli is installed and signed in")

    args = p.parse_args()
    if args.cmd == "modes":
        print(json.dumps(list_modes(), indent=2))
        return
    if args.cmd == "bible":
        print(json.dumps(studio_bible(), indent=2))
        return
    if args.cmd == "jobs":
        print(json.dumps(list_jobs(), indent=2))
        return
    if args.cmd == "prompt":
        print(json.dumps(build_plate_prompt(args.subject, args.screen, args.cartoonist, args.hologram), indent=2))
        return
    if args.cmd == "stage":
        print(stage(args.src, args.screen, args.look, args.background, args.out, args.similarity, args.blend))
        return
    if args.cmd == "hologram":
        print(apply_hologram(args.src, args.style, args.out, args.screen))
        return
    if args.cmd == "cartoon":
        print(apply_cartoon(args.src, args.mode, args.out, args.screen))
        return
    if args.cmd == "movie":
        print(json.dumps(make_shot(args.src, job=args.job, name=args.name, rig=args.rig), indent=2))
        return
    if args.cmd == "go":
        print(go_motion(args.src, move=args.move, shutter=args.shutter, duration=args.duration, output=args.out))
        return
    if args.cmd == "rerun":
        print(apply_rig(args.src, args.rig, output=args.out))
        return
    if args.cmd == "reel":
        print(assemble_reel(args.clips, name=args.name, output=args.out))
        return
    if args.cmd == "ingest":
        print(json.dumps(submit(args.source, artifact=args.artifact, wait=args.wait), indent=2))
        return
    if args.cmd == "ingest-status":
        print(json.dumps(status(args.request_id, wait=args.wait), indent=2))
        return
    if args.cmd == "ingest-pull":
        print(json.dumps(pull(args.request_id, dest=args.dest), indent=2))
        return
    if args.cmd == "ingest-probe":
        card = pipeline_card()
        card["help"] = help_text()[-1500:]
        print(json.dumps(card, indent=2))
        return


if __name__ == "__main__":
    main()
