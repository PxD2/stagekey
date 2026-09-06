"""Go-motion and motion-control rigs. The puppet moves while the shutter is open."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from .engine import FFMPEG, _run, probe
from .jobs import MOVES


def _as_video(src: Path, duration: float, fps: int = 24) -> Path:
    """Still images become a short hold so later filters can animate them."""
    info = None
    try:
        info = probe(src)
    except Exception:
        info = None
    streams = (info or {}).get("streams") or []
    if any(s.get("codec_type") == "video" and s.get("nb_frames") not in {None, "1", "0"} for s in streams):
        if src.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            return src
    hold = src.with_name(src.stem + "_hold.mp4")
    _run([
        FFMPEG, "-y", "-loop", "1", "-i", str(src),
        "-t", f"{duration:.3f}", "-r", str(fps),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-an", str(hold),
    ])
    return hold


def go_motion(
    src: str | Path,
    move: str = "heavy-steps",
    shutter: int = 5,
    duration: float = 3.0,
    output: Optional[str] = None,
) -> str:
    """Move the plate across the frame with open-shutter blur."""
    src = Path(src)
    if not src.exists():
        raise FileNotFoundError(src)
    spec = MOVES.get(move) or MOVES["hold"]
    out = Path(output) if output else src.with_name(src.stem + f"_{move}.mp4")
    plate = _as_video(src, duration)
    info = probe(plate)
    v = next(s for s in info["streams"] if s.get("codec_type") == "video")
    w = int(v.get("width", 1280))
    h = int(v.get("height", 720))
    dx, dy, dz = spec["dx"], spec["dy"], spec["dz"]
    bob, steps = spec["bob"], spec["steps"]
    frames = max(1, int(duration * 24))
    z0 = 1.0
    z1 = 1.0 + max(0.0, float(dz))
    x_expr = f"(in_w-out_w)/2+({dx})*on/{frames}"
    y_expr = f"(in_h-out_h)/2+({dy})*on/{frames}+({bob})*sin(on*{max(steps, 1)}*2*PI/{frames})"
    blur = max(0, min(int(shutter), 12))
    vf = (
        f"scale={w * 2}:{h * 2},"
        f"zoompan=z='{z0}+({z1}-{z0})*on/{frames}':x='{x_expr}':y='{y_expr}':"
        f"d={frames}:s={w}x{h}:fps=24"
    )
    if blur:
        vf += ",minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:me_mode=bidir"
        vf += f",tmix=frames={blur}:weights='1'"
    _run([
        FFMPEG, "-y", "-i", str(plate), "-vf", vf, "-frames:v", str(frames),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-an", str(out),
    ])
    rig = {
        "move": move,
        "shutter": shutter,
        "duration": duration,
        "dx": dx, "dy": dy, "dz": dz, "bob": bob, "steps": steps,
        "source": str(src),
        "output": str(out),
    }
    Path(str(out) + ".rig.json").write_text(json.dumps(rig, indent=2))
    return str(out)


def apply_rig(src: str | Path, rig_path: str | Path, output: Optional[str] = None) -> str:
    """Re-run a saved camera.rig.json on a new plate."""
    rig = json.loads(Path(rig_path).read_text())
    out = output or str(Path(src).with_name(Path(src).stem + "_rerun.mp4"))
    return go_motion(
        src,
        move=rig.get("move", "flyby"),
        shutter=int(rig.get("shutter", 3)),
        duration=float(rig.get("duration", 3.0)),
        output=out,
    )
