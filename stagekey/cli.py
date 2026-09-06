"""CLI: python -m stagekey stage plate.mp4 --screen green --look hologram-cyan"""

from __future__ import annotations

import argparse
import json

from .engine import apply_cartoon, apply_hologram, list_modes, stage
from .prompts import build_plate_prompt


def main() -> None:
    p = argparse.ArgumentParser(prog="stagekey", description="Key, hologram, and cartoonist finish for video plates")
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

    args = p.parse_args()
    if args.cmd == "modes":
        print(json.dumps(list_modes(), indent=2))
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


if __name__ == "__main__":
    main()
