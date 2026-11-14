"""Provenance stamped into every output file: study_id, git commit, UTC timestamp."""
from __future__ import annotations

import datetime as _dt
import subprocess

from .config import ROOT, load_config


def git_commit() -> str:
    try:
        sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        dirty = subprocess.call(["git", "diff", "--quiet", "HEAD", "--", "src", "config", "prompts"], cwd=ROOT) != 0
        return sha + ("-dirty" if dirty else "")
    except Exception:
        return "unknown"


def utc_now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def provenance() -> dict:
    return {"study_id": load_config()["study_id"], "git_commit": git_commit(), "created_utc": utc_now()}


def header_lines(prefix: str = "# ") -> str:
    """Comment header for CSV/markdown outputs."""
    p = provenance()
    return "".join(f"{prefix}{k}: {v}\n" for k, v in p.items())


def write_meta_sidecar(path, **extra) -> None:
    """Write <path>.meta.json next to a data file (used for jsonl/csv files whose format can't carry comments)."""
    import json
    from pathlib import Path

    p = Path(str(path) + ".meta.json")
    p.write_text(json.dumps({**provenance(), **extra}, indent=2) + "\n", encoding="utf-8")
