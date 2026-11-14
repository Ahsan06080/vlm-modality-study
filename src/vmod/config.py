"""Load the fixed experiment design (config/experiment.yaml)."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "experiment.yaml"
TEMPLATES_PATH = ROOT / "prompts" / "templates.md"
DATA = ROOT / "data"
RESULTS = ROOT / "results"
REPORTS = ROOT / "reports"
CONTENT_TYPES = ("code", "math", "table")
CONDITIONS = ("A_text", "B_image", "C_image_transcribe")


@lru_cache(maxsize=1)
def load_config(path: str | Path = CONFIG_PATH) -> dict:
    with open(path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    for key in ("study_id", "seed", "items", "content_types", "conditions", "render", "decoding", "models"):
        if key not in cfg:
            raise KeyError(f"config missing key: {key}")
    return cfg


def model_slug(model_id: str) -> str:
    return model_id.replace("/", "__")
