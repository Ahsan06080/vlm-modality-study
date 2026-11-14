"""Build prompts verbatim from prompts/templates.md."""
from __future__ import annotations

import hashlib
import re
from functools import lru_cache

from .config import TEMPLATES_PATH


@lru_cache(maxsize=1)
def templates() -> dict:
    md = TEMPLATES_PATH.read_text(encoding="utf-8")
    out = {}
    for name in ("code", "math", "table", "A_text", "B_image", "C_image_transcribe"):
        m = re.search(r"^\*\*" + re.escape(name) + r"\*\*[^\n]*\n```\n(.*?)\n```", md, re.S | re.M)
        if not m:
            raise ValueError(f"template {name} not found in templates.md")
        out[name] = m.group(1)
    return out


def build_prompt(content_type: str, condition: str, content: str) -> str:
    t = templates()
    text = t[condition].replace("{INSTRUCTION}", t[content_type])
    if condition == "A_text":
        text = text.replace("{CONTENT}", content)
    return text


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()
