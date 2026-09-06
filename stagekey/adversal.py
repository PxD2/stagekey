"""Adversal remote ingest adapter.

Adversal returns Markdown + synced frames.
StageKey finishes plates (key, hologram, cartoon, go-motion).
The CLI talks to adversal-cli when it is on PATH.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import time
from pathlib import Path
from typing import Optional

ADVERSAL_BIN = shutil.which("adversal-cli") or shutil.which("adversal")
AUTH_FILE = Path.home() / ".adversal" / "auth.txt"
REGISTRY = Path.home() / ".stagekey" / "adversal_jobs.json"
DOCS = "https://adversal.ai"


def _registry() -> dict:
    if REGISTRY.exists():
        try:
            return json.loads(REGISTRY.read_text())
        except json.JSONDecodeError:
            return {"jobs": []}
    return {"jobs": []}


def _save(reg: dict) -> None:
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY.write_text(json.dumps(reg, indent=2))


def file_md5(path: str | Path) -> str:
    h = hashlib.md5()
    with Path(path).open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def probe_cli() -> dict:
    return {
        "binary": ADVERSAL_BIN,
        "on_path": bool(ADVERSAL_BIN),
        "auth_file": str(AUTH_FILE),
        "signed_in": AUTH_FILE.exists() and AUTH_FILE.stat().st_size > 0,
        "docs": DOCS,
        "python_need": "3.13+",
        "ffmpeg_need": bool(shutil.which("ffmpeg") and shutil.which("ffprobe")),
        "note": (
            "Install: python -m pip install adversal-cli && ffmpeg on PATH. "
            "If a tool returns AUTHENTICATION REQUIRED, run authenticate, "
            "finish browser sign-in, retry. Token lives in ~/.adversal/auth.txt."
        ),
    }


def _run_cli(args: list[str], timeout: int = 60) -> subprocess.CompletedProcess:
    if not ADVERSAL_BIN:
        raise FileNotFoundError(
            "adversal-cli is not on PATH. Install with: python -m pip install adversal-cli"
        )
    return subprocess.run([ADVERSAL_BIN, *args], capture_output=True, text=True, timeout=timeout)


def help_text() -> str:
    if not ADVERSAL_BIN:
        return probe_cli()["note"]
    try:
        proc = _run_cli(["--help"])
        return (proc.stdout or proc.stderr or "").strip() or probe_cli()["note"]
    except Exception as exc:
        return f"{type(exc).__name__}: {exc}\n{probe_cli()['note']}"


def find_existing(md5: str) -> Optional[dict]:
    for job in _registry().get("jobs", []):
        if job.get("md5") == md5 and job.get("status") not in {"failed", "error"}:
            return job
    return None


def submit(source: str, artifact: str = "report", wait: bool = False, timeout: int = 600) -> dict:
    source = source.strip()
    path = Path(source)
    md5 = file_md5(path) if path.exists() else hashlib.md5(source.encode()).hexdigest()
    existing = find_existing(md5)
    if existing:
        existing["reused"] = True
        existing["tip"] = "Same bytes already queued. Use status / pull instead of resubmitting."
        return existing
    job = {
        "source": source,
        "md5": md5,
        "artifact": artifact,
        "submitted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "status": "queued_local",
    }
    attempts = [
        ["process", source, "--artifact", artifact],
        ["process-video", source],
        ["submit", source],
        [source],
    ]
    last = ""
    if ADVERSAL_BIN:
        for args in attempts:
            try:
                proc = _run_cli(args, timeout=30)
            except Exception as exc:
                last = str(exc)
                continue
            text = (proc.stdout or "") + "\n" + (proc.stderr or "")
            last = text.strip()
            if proc.returncode == 0:
                job["status"] = "submitted"
                job["cli_args"] = args
                job["cli_out"] = text[-4000:]
                for token in text.replace(",", " ").split():
                    if "request" in text.lower() and token not in {source, artifact}:
                        if token.lower().startswith("req") or (len(token) >= 8 and token.replace("-", "").isalnum()):
                            job["request_id"] = token.strip(".:'\"")
                break
        else:
            job["status"] = "needs_mcp_or_cli_flags"
            job["cli_out"] = last[-4000:]
            job["help"] = help_text()[-2000:]
    else:
        job["status"] = "cli_missing"
        job["help"] = help_text()
    if "request_id" not in job:
        job["request_id"] = f"local-{md5[:12]}"
    reg = _registry()
    reg.setdefault("jobs", []).append(job)
    _save(reg)
    if wait and job.get("status") == "submitted":
        return status(job["request_id"], wait=True, timeout=timeout)
    return job


def status(request_id: str, wait: bool = False, timeout: int = 600) -> dict:
    deadline = time.time() + timeout
    current = {"request_id": request_id, "status": "unknown"}
    for job in _registry().get("jobs", []):
        if job.get("request_id") == request_id:
            current = dict(job)
            break
    if not ADVERSAL_BIN:
        current["probe"] = probe_cli()
        return current
    while True:
        for args in (["status", request_id], ["check", request_id], ["check-video-status", request_id]):
            try:
                proc = _run_cli(args, timeout=30)
            except Exception:
                continue
            text = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()
            if proc.returncode == 0 and text:
                current["cli_out"] = text[-4000:]
                low = text.lower()
                if "complete" in low or "done" in low:
                    current["status"] = "complete"
                elif "fail" in low or "error" in low:
                    current["status"] = "failed"
                elif "auth" in low:
                    current["status"] = "auth_required"
                else:
                    current["status"] = "running"
                break
        if not wait or current.get("status") in {"complete", "failed", "auth_required"}:
            return current
        if time.time() > deadline:
            current["status"] = "timeout"
            return current
        time.sleep(8)


def pull(request_id: str, dest: str | Path = "adversal_out") -> dict:
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    result = {"request_id": request_id, "dest": str(dest), "files": []}
    if not ADVERSAL_BIN:
        result["probe"] = probe_cli()
        result["status"] = "cli_missing"
        return result
    for args in (
        ["download", request_id, "--out", str(dest)],
        ["pull", request_id, str(dest)],
        ["download-report", request_id, str(dest)],
        ["download-frames", request_id, str(dest)],
    ):
        try:
            proc = _run_cli(args, timeout=120)
        except Exception:
            continue
        if proc.returncode == 0:
            result["cli_args"] = args
            result["cli_out"] = ((proc.stdout or "") + (proc.stderr or ""))[-2000:]
            result["files"] = sorted(p.name for p in dest.iterdir())
            result["status"] = "pulled"
            return result
    result["status"] = "needs_mcp_download"
    result["help"] = help_text()[-2000:]
    result["hint"] = (
        "After process_video completes, download the report and frames "
        "into this workspace, then run stagekey farm or stage on the frames."
    )
    return result


def pipeline_card() -> dict:
    return {
        "roles": {
            "adversal": "Understand: ingest URL or file, queue by MD5, return Markdown + frames.",
            "stagekey": "Finish: chroma key, hologram, cartoon, go-motion, farm, reel.",
            "agent": "Plan: write the farm card from those frames.",
        },
        "mcp_clients": ["Claude Code", "Cursor", "OpenCode"],
        "install_adversal": [
            "python -m pip install adversal-cli",
            "ffmpeg on PATH",
            "claude mcp add adversal -- adversal-cli",
        ],
        "install_stagekey": [
            "python -m pip install -e .",
            "python app.py",
        ],
        "do_not": "Do not resubmit the same video bytes. Reuse request_id via status/pull.",
        "probe": probe_cli(),
    }
