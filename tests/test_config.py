from vmod.config import load_config, model_slug
from vmod.meta import provenance


def test_config_loads():
    cfg = load_config()
    assert cfg["study_id"] == "vlm-modality-v1"
    assert cfg["seed"] == 630
    assert set(cfg["content_types"]) == {"code", "math", "table"}


def test_provenance():
    p = provenance()
    assert set(p) == {"study_id", "git_commit", "created_utc"}


def test_slug():
    assert model_slug("Qwen/Qwen2.5-VL-3B-Instruct") == "Qwen__Qwen2.5-VL-3B-Instruct"
