"""T02: download CRUXEval, GSM8K (test) and WikiTableQuestions (pristine-unseen-tables) into data/raw/."""
from __future__ import annotations

import hashlib
import json
import urllib.request
import zipfile

from .config import DATA
from .meta import header_lines

WTQ_URL = "https://github.com/ppasupat/WikiTableQuestions/releases/download/v1.0.2/WikiTableQuestions-1.0.2-compact.zip"
RAW = DATA / "raw"


def sha256_file(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main(args=None):
    from datasets import load_dataset
    from huggingface_hub import HfApi

    RAW.mkdir(parents=True, exist_ok=True)
    api = HfApi()
    rows = []
    for key, name, cfg in [("cruxeval", "cruxeval-org/cruxeval", None), ("gsm8k", "openai/gsm8k", "main")]:
        info = api.dataset_info(name)
        ds = load_dataset(name, cfg, split="test", revision=info.sha)
        out = RAW / f"{key}_test.jsonl"
        with open(out, "w", encoding="utf-8") as f:
            for r in ds:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        lic = (info.card_data or {}).get("license")
        rows.append(dict(name=key, source=f"https://huggingface.co/datasets/{name}" + (f" (config {cfg})" if cfg else ""),
                         version=f"HF commit {info.sha}", sha256=sha256_file(out), license=lic if isinstance(lic, str) else ",".join(lic or []),
                         n=len(ds), file=str(out.relative_to(DATA.parent))))

    wdir = RAW / "wtq"
    wdir.mkdir(exist_ok=True)
    zp = wdir / "wtq.zip"
    if not zp.exists():
        urllib.request.urlretrieve(WTQ_URL, zp)
    with zipfile.ZipFile(zp) as z:
        z.extractall(wdir)
    tsv = wdir / "WikiTableQuestions" / "data" / "pristine-unseen-tables.tsv"
    n = sum(1 for _ in open(tsv, encoding="utf-8")) - 1
    rows.append(dict(name="wtq", source=WTQ_URL + " (HF stanfordnlp/wikitablequestions loader is script-based and no longer supported by `datasets`)",
                     version="release v1.0.2 (repo master 7d455a5a)", sha256=f"zip {sha256_file(zp)}; tsv {sha256_file(tsv)}",
                     license="CC-BY-SA-4.0", n=n, file=str(tsv.relative_to(DATA.parent))))

    lines = ["# Data manifest\n", "\n", "<!--\n", header_lines(""), "-->\n", "\n",
             "Raw files live in `data/raw/` (git-ignored); re-create with `python -m vmod download`.\n\n",
             "| dataset | source | version | sha256 | license | items (test split) | local file |\n",
             "|---|---|---|---|---|---|---|\n"]
    for r in rows:
        lines.append(f"| {r['name']} | {r['source']} | {r['version']} | `{r['sha256']}` | {r['license']} | {r['n']} | `{r['file']}` |\n")
    lines.append("\nLicense notes: MIT (CRUXEval, GSM8K) and CC BY-SA 4.0 (WTQ) all allow research use. Redistributing derived WTQ tables "
                 "(item files) requires attribution and the same license.\n")
    (DATA / "MANIFEST.md").write_text("".join(lines), encoding="utf-8")
    for r in rows:
        print(r["name"], r["n"], r["license"])
