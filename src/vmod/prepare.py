"""T03: build canonical items, apply exclusions (logged), sample pilot/main with the config seed."""
from __future__ import annotations

import csv
import json
import random
import re
from collections import Counter
from functools import lru_cache

from .config import DATA, load_config
from .content import code_content, math_content, table_content, wtq_unescape
from .meta import header_lines, write_meta_sidecar

RAW = DATA / "raw"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


@lru_cache(maxsize=1)
def font_cmap() -> set[int]:
    from fontTools.ttLib import TTFont

    return set(TTFont(FONT_PATH).getBestCmap().keys())


def render_problems(text: str) -> list[str]:
    """Characters that can't be rendered faithfully in monospace: control chars (other than newline) or missing glyphs."""
    cmap = font_cmap()
    bad = sorted({c for c in text if c != "\n" and (ord(c) < 32 or ord(c) == 127 or ord(c) not in cmap)})
    return [f"U+{ord(c):04X}" for c in bad]


def load_code():
    for i, line in enumerate(open(RAW / "cruxeval_test.jsonl", encoding="utf-8")):
        r = json.loads(line)
        yield dict(item_id=f"code-{r['id']}", content_type="code", content=code_content(r["code"], r["input"]),
                   gold=r["output"], source_index=i)


def load_math(width):
    for i, line in enumerate(open(RAW / "gsm8k_test.jsonl", encoding="utf-8")):
        r = json.loads(line)
        gold = r["answer"].split("####")[-1].strip()
        yield dict(item_id=f"math-{i:04d}", content_type="math", content=math_content(r["question"], width),
                   gold=gold, source_index=i)


def load_table():
    base = RAW / "wtq" / "WikiTableQuestions"
    canon = {}
    with open(base / "tagged" / "data" / "pristine-unseen-tables.tagged", encoding="utf-8") as f:
        th = f.readline().rstrip("\n").split("\t")
        for line in f:
            t = dict(zip(th, line.rstrip("\n").split("\t")))
            canon[t["id"]] = [wtq_unescape(v) for v in t["targetCanon"].split("|")]
    with open(base / "data" / "pristine-unseen-tables.tsv", encoding="utf-8") as f:
        header = f.readline().rstrip("\n").split("\t")
        for i, line in enumerate(f):
            r = dict(zip(header, line.rstrip("\n").split("\t")))
            tsv = base / r["context"].replace(".csv", ".tsv")
            rows = [[wtq_unescape(c) for c in l.rstrip("\n").split("\t")] for l in open(tsv, encoding="utf-8")]
            gold = [wtq_unescape(v) for v in r["targetValue"].split("|")]
            yield dict(item_id=f"table-{r['id']}", content_type="table", content=table_content(rows, r["utterance"]),
                       gold=gold, gold_canon=canon[r["id"]], source_index=i, n_table_rows=len(rows) - 1)


def exclusion_reasons(item, ex) -> list[str]:
    lines = item["content"].split("\n")
    reasons = []
    if max(len(l) for l in lines) > ex["max_line_chars"]:
        reasons.append("max_line_chars")
    if len(lines) > ex["max_lines"]:
        reasons.append("max_lines")
    if item["content_type"] == "table" and item["n_table_rows"] > ex["table_max_rows"]:
        reasons.append("table_max_rows")
    if ex.get("drop_if_render_fails") and render_problems(item["content"]):
        reasons.append("render_fails:" + ",".join(render_problems(item["content"])[:5]))
    return reasons


def main(args=None):
    cfg = load_config()
    ex, seed = cfg["exclusions"], cfg["seed"]
    n_pilot, n_main = cfg["items"]["pilot_per_content"], cfg["items"]["main_per_content"]
    out_dir = DATA / "items"
    out_dir.mkdir(parents=True, exist_ok=True)
    loaders = {"code": load_code(), "math": load_math(cfg["content_types"]["math"]["wrap_chars"]), "table": load_table()}
    excl_rows, summary = [], {}
    for ct, gen in loaders.items():
        eligible, total, reason_counts = [], 0, Counter()
        for it in gen:
            total += 1
            lines = it["content"].split("\n")
            it["n_chars"], it["n_lines"] = len(it["content"]), len(lines)
            rs = exclusion_reasons(it, ex)
            if rs:
                excl_rows.append((it["item_id"], ct, ";".join(rs)))
                for r in rs:
                    reason_counts[r.split(":")[0]] += 1
            else:
                eligible.append(it)
        eligible.sort(key=lambda d: d["source_index"])
        rng = random.Random(seed)
        picked = rng.sample(eligible, n_pilot + n_main)
        sets = {"pilot": picked[:n_pilot], "main": picked[n_pilot:]}
        for s, items in sets.items():
            p = out_dir / f"{s}_{ct}.jsonl"
            with open(p, "w", encoding="utf-8") as f:
                for it in items:
                    keys = ["item_id", "content_type", "content", "gold", "n_chars", "n_lines"] + \
                           (["n_table_rows", "gold_canon"] if ct == "table" else []) + ["source_index"]
                    f.write(json.dumps({k: it[k] for k in keys}, ensure_ascii=False) + "\n")
            write_meta_sidecar(p, seed=seed, n=len(items), sampling="random.Random(seed).sample(eligible sorted by source_index, pilot+main); first pilot_per_content = pilot")
        summary[ct] = dict(total=total, excluded=total - len(eligible), eligible=len(eligible), reasons=dict(reason_counts),
                           pilot=len(sets["pilot"]), main=len(sets["main"]))
        assert not {d["item_id"] for d in sets["pilot"]} & {d["item_id"] for d in sets["main"]}
    with open(DATA / "exclusions.csv", "w", newline="", encoding="utf-8") as f:
        f.write(header_lines())
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["item_id", "content_type", "reason"])
        w.writerows(excl_rows)
    (DATA / "items" / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
