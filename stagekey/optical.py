"""Optical printer: stack passes the way a contact printer would."""
from __future__ import annotations
from pathlib import Path
from typing import Optional
from .engine import _run, probe, stage

def add_shadow(fg: str | Path, output: Optional[str] = None, offset: int = 18) -> str:
    fg = Path(fg)
    out = Path(output) if output else fg.with_name(fg.stem + "_shadow.mp4")
    info = probe(fg)
    v = next(s for s in info["streams"] if s.get("codec_type") == "video")
    filter_complex = (
        f"[0:v]split[a][b];"
        f"[b]format=gray,eq=brightness=-0.6:contrast=1.4,boxblur=12:1,"
        f"colorchannelmixer=aa=0.45[sh];"
        f"[a][sh]overlay=x={offset}:y={offset}:shortest=1,format=yuv420p[v]"
    )
    _run(["ffmpeg", "-y", "-i", str(fg), "-filter_complex", filter_complex, "-map", "[v]",
          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-an", str(out)])
    return str(out)

def add_tracers(src: str | Path, output: Optional[str] = None, count: int = 3) -> str:
    src = Path(src)
    out = Path(output) if output else src.with_name(src.stem + "_tracers.mp4")
    info = probe(src)
    v = next(s for s in info["streams"] if s.get("codec_type") == "video")
    h = int(v["height"])
    overlays, labels = [], ["[0:v]"]
    for i in range(count):
        y = int(h * (0.25 + 0.2 * i))
        color = ["0x7CFFFB", "0xFF4A3A", "0xFFC14A"][i % 3]
        overlays.append(f"color=c={color}@0.9:s=260x5:d=12:r=24,format=rgba[t{i}]")
        prev = labels[-1]
        overlays.append(f"{prev}[t{i}]overlay=x='{-200}+{280 + 90 * i}*t':y={y}:shortest=1[o{i}]")
        labels.append(f"[o{i}]")
    last = labels[-1]
    graph = ";".join(overlays) + f";{last}format=yuv420p[v]"
    _run(["ffmpeg", "-y", "-i", str(src), "-filter_complex", graph, "-map", "[v]",
          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-an", str(out)])
    return str(out)

def print_shot(src: str | Path, output: Optional[str] = None, screen: str = "none",
               look: str = "raw", background: str = "black", shadow: bool = False,
               tracers: bool = False) -> str:
    src = Path(src)
    out = Path(output) if output else src.with_name(src.stem + "_print.mp4")
    current = stage(src, screen=screen, look=look, background=background, output=str(out))
    if shadow:
        current = add_shadow(current, output=str(out.with_name(out.stem + "_sh.mp4")))
    if tracers:
        current = add_tracers(current, output=str(out.with_name(out.stem + "_tr.mp4")))
    if Path(current) != out:
        _run(["ffmpeg", "-y", "-i", current, "-c", "copy", str(out)])
    return str(out)
