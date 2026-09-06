"""FFmpeg engine for chroma key, black hologram, and cartoonist looks."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Optional

FFMPEG = shutil.which("ffmpeg") or "ffmpeg"
FFPROBE = shutil.which("ffprobe") or "ffprobe"

SCREEN_HEX = {"green": "0x00FF00", "blue": "0x0040FF"}

LOOKS = {
    "raw",
    "hologram-cyan",
    "hologram-red",
    "hologram-amber",
    "hologram-ghost",
    "cartoon-anime",
    "cartoon-cel",
    "cartoon-comic",
    "cartoon-ink",
    "cartoon-newsprint",
    "cartoon-pop",
    "cartoon-noir",
    "toon-hologram",
}


def list_modes() -> dict:
    return {
        "screens": ["green", "blue", "none"],
        "backgrounds": ["black", "transparent", "keep", "#hex or color name", "path to image/video"],
        "looks": sorted(LOOKS),
        "cartoonist": ["anime", "cel", "comic", "ink", "newsprint", "pop", "noir"],
        "hologram": ["cyan", "red", "amber", "ghost"],
        "one_tool": "stage(input, screen, look, background) — do everything",
    }


def _run(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            "ffmpeg failed\nCMD: "
            + " ".join(cmd)
            + "\n"
            + (proc.stderr[-4000:] if proc.stderr else proc.stdout)
        )


def probe(path: str | Path) -> dict:
    cmd = [FFPROBE, "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr)
    return json.loads(proc.stdout)


def _has_audio(path: str | Path) -> bool:
    data = probe(path)
    return any(s.get("codec_type") == "audio" for s in data.get("streams", []))


def _out_path(src: str | Path, suffix: str, output: Optional[str]) -> Path:
    if output:
        return Path(output)
    src = Path(src)
    return src.with_name(src.stem + suffix + src.suffix)


def _key_filter(screen: str, similarity: float, blend: float) -> str:
    color = SCREEN_HEX[screen]
    return f"colorkey={color}:{similarity}:{blend},despill=type={screen}:mix=0.5:expand=0"


def _look_filter(look: str) -> str:
    look = look.lower().strip()
    if look in {"raw", "off", "none", ""}:
        return "null"
    if look == "hologram-cyan":
        return (
            "format=yuv444p,"
            "colorchannelmixer=rr=0.15:rg=0.35:rb=0.35:gr=0.05:gg=0.85:gb=0.55:br=0.10:bg=0.75:bb=1.0,"
            "eq=contrast=1.35:brightness=0.04:saturation=1.55,"
            "chromashift=cbh=3:crh=-3,"
            "split[base][glow];"
            "[glow]boxblur=7:1,eq=brightness=0.08[g];"
            "[base][g]blend=all_mode=screen:all_opacity=0.5,"
            "geq=lum='lum(X,Y)*(0.72+0.28*lt(mod(Y,4),1)+0.08*sin(N*0.9))':cb='cb(X,Y)':cr='cr(X,Y)',"
            "noise=alls=10:allf=t+u,"
            "vignette=PI/5"
        )
    if look == "hologram-red":
        return (
            "format=yuv444p,"
            "colorchannelmixer=rr=1.1:rg=0.15:rb=0.05:gr=0.05:gg=0.18:gb=0.05:br=0.05:bg=0.05:bb=0.25,"
            "eq=contrast=1.4:saturation=1.3,"
            "split[base][glow];[glow]boxblur=6:1[g];[base][g]blend=all_mode=screen:all_opacity=0.45,"
            "geq=lum='lum(X,Y)*(0.7+0.3*lt(mod(Y,3),1)+0.1*sin(N))':cb='cb(X,Y)':cr='cr(X,Y)',"
            "noise=alls=12:allf=t+u"
        )
    if look == "hologram-amber":
        return (
            "format=yuv444p,"
            "colorchannelmixer=rr=1.05:rg=0.45:rb=0.05:gr=0.35:gg=0.7:gb=0.05:br=0.02:bg=0.12:bb=0.08,"
            "eq=contrast=1.3:saturation=1.2,"
            "split[base][glow];[glow]boxblur=6:1[g];[base][g]blend=all_mode=screen:all_opacity=0.4,"
            "geq=lum='lum(X,Y)*(0.75+0.25*lt(mod(Y,4),1))':cb='cb(X,Y)':cr='cr(X,Y)',"
            "noise=alls=8:allf=t+u"
        )
    if look == "hologram-ghost":
        return (
            "format=yuv444p,"
            "eq=contrast=1.15:brightness=0.06:saturation=0.35,"
            "colorchannelmixer=rr=0.6:rg=0.7:rb=0.8:gr=0.6:gg=0.75:gb=0.85:br=0.7:bg=0.85:bb=1,"
            "geq=lum='lum(X,Y)*(0.55+0.2*sin(N/3)+0.25*lt(mod(Y,5),1))':cb='cb(X,Y)':cr='cr(X,Y)',"
            "noise=alls=16:allf=t+u"
        )
    if look == "cartoon-anime":
        return (
            "split[c][e];"
            "[c]eq=contrast=1.28:saturation=1.45:gamma=0.95,unsharp=5:5:0.7:5:5:0.0[col];"
            "[e]format=gray,edgedetect=mode=colormix:low=0.09:high=0.22[ed];"
            "[col][ed]blend=all_mode=multiply:all_opacity=0.55"
        )
    if look == "cartoon-cel":
        return (
            "eq=contrast=1.45:saturation=1.7:gamma=0.9,"
            "unsharp=5:5:1.0,"
            "split[c][e];"
            "[e]format=gray,edgedetect=low=0.12:high=0.28,lutyuv='y=negval'[ed];"
            "[c][ed]blend=all_mode=multiply"
        )
    if look == "cartoon-comic":
        return (
            "eq=contrast=1.55:saturation=1.8,"
            "unsharp=5:5:1.2,"
            "split[c][e];"
            "[e]format=gray,edgedetect=low=0.08:high=0.2,lutyuv='y=negval'[ed];"
            "[c][ed]blend=all_mode=multiply,"
            "noise=alls=18:allf=u"
        )
    if look == "cartoon-ink":
        return (
            "format=gray,eq=contrast=1.8:brightness=0.05,"
            "edgedetect=mode=colormix:low=0.1:high=0.25,"
            "eq=contrast=1.6"
        )
    if look == "cartoon-newsprint":
        return (
            "format=gray,eq=contrast=1.7:brightness=0.02,"
            "noise=alls=28:allf=u,"
            "unsharp=5:5:0.8"
        )
    if look == "cartoon-pop":
        return (
            "eq=contrast=1.6:saturation=2.1:gamma=0.85,"
            "unsharp=5:5:1.3,"
            "split[c][e];"
            "[e]format=gray,edgedetect=low=0.1:high=0.24,lutyuv='y=negval'[ed];"
            "[c][ed]blend=all_mode=multiply"
        )
    if look == "cartoon-noir":
        return (
            "format=gray,eq=contrast=1.9:brightness=-0.04,"
            "split[c][e];"
            "[e]edgedetect=low=0.08:high=0.2,lutyuv='y=negval'[ed];"
            "[c][ed]blend=all_mode=multiply"
        )
    if look == "toon-hologram":
        return _look_filter("cartoon-cel") + "," + _look_filter("hologram-cyan")
    raise ValueError(f"Unknown look '{look}'. Choose from: {sorted(LOOKS)}")


def _background_source(background: str, size: str, duration: str) -> tuple[list[str], str]:
    background = background.strip()
    if background in {"keep", ""}:
        return [], "KEEP"
    if background == "transparent":
        return [], "ALPHA"
    if background == "black":
        return ["-f", "lavfi", "-i", f"color=c=black:s={size}:d={duration}:r=24"], "BG"
    if background.startswith("#") or background.isalpha():
        color = background if background.startswith("#") else background
        return ["-f", "lavfi", "-i", f"color=c={color}:s={size}:d={duration}:r=24"], "BG"
    path = Path(background)
    if not path.exists():
        raise FileNotFoundError(f"Background not found: {background}")
    return ["-i", str(path)], "BG"


def key_screen(
    src: str | Path,
    screen: str = "green",
    output: Optional[str] = None,
    similarity: float = 0.28,
    blend: float = 0.12,
    background: str = "black",
) -> str:
    return stage(src, screen=screen, look="raw", background=background, output=output,
                 similarity=similarity, blend=blend)


def apply_hologram(
    src: str | Path,
    style: str = "cyan",
    output: Optional[str] = None,
    screen: str = "none",
) -> str:
    look = f"hologram-{style.lower().strip()}"
    bg = "black" if screen in {"green", "blue"} else "keep"
    return stage(src, screen=screen, look=look, background=bg, output=output)


def apply_cartoon(
    src: str | Path,
    mode: str = "anime",
    output: Optional[str] = None,
    screen: str = "none",
) -> str:
    look = f"cartoon-{mode.lower().strip()}"
    return stage(src, screen=screen, look=look, background="keep", output=output)


def _join_filters(pieces: list[str]) -> str:
    graph = pieces[0]
    for piece in pieces[1:]:
        graph = f"{graph},{piece}"
    return graph


def stage(
    src: str | Path,
    screen: str = "green",
    look: str = "raw",
    background: str = "black",
    output: Optional[str] = None,
    similarity: float = 0.28,
    blend: float = 0.12,
) -> str:
    src = Path(src)
    if not src.exists():
        raise FileNotFoundError(src)
    screen = screen.lower().strip()
    look = look.lower().strip()
    info = probe(src)
    v = next(s for s in info["streams"] if s.get("codec_type") == "video")
    width = int(v.get("width", 1280))
    height = int(v.get("height", 720))
    size = f"{width}x{height}"
    duration = info.get("format", {}).get("duration", "4")
    out = _out_path(src, f"_{screen}_{look.replace('-', '_')}", output)
    out.parent.mkdir(parents=True, exist_ok=True)
    pieces = []
    if screen in SCREEN_HEX:
        pieces.append(_key_filter(screen, similarity, blend))
    look_f = _look_filter(look)
    if look_f != "null":
        pieces.append(look_f)
    fg_graph = _join_filters(pieces) if pieces else "format=rgba"
    bg_args, bg_kind = _background_source(background, size, duration)
    audio = ["-map", "0:a?", "-c:a", "aac", "-shortest"] if _has_audio(src) else ["-an"]
    if bg_kind == "KEEP":
        cmd = [FFMPEG, "-y", "-i", str(src), "-filter_complex", f"[0:v]{fg_graph}[v]", "-map", "[v]",
               "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "veryfast", *audio, str(out)]
        _run(cmd)
        return str(out)
    if bg_kind == "ALPHA":
        alpha_out = out.with_suffix(".webm")
        cmd = [FFMPEG, "-y", "-i", str(src), "-filter_complex", f"[0:v]{fg_graph},format=yuva420p[v]", "-map", "[v]",
               "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-auto-alt-ref", "0", "-crf", "30", "-b:v", "0", "-an", str(alpha_out)]
        _run(cmd)
        return str(alpha_out)
    filter_complex = (
        f"[0:v]{fg_graph},format=rgba[fg];"
        f"[1:v]scale={width}:{height}:force_original_aspect_ratio=increase,"
        f"crop={width}:{height},loop=-1:size=32767,format=rgba[bg];"
        f"[bg][fg]overlay=0:0:shortest=1,format=yuv420p[v]"
    )
    cmd = [FFMPEG, "-y", "-i", str(src), *bg_args, "-filter_complex", filter_complex, "-map", "[v]",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "veryfast", *audio, str(out)]
    _run(cmd)
    return str(out)
