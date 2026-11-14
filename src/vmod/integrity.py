"""T08: per-model integrity check, gzip, short report."""
from __future__ import annotations

import csv
import gzip
import json
import shutil
import sys
from collections import Counter

import pandas as pd

from .config import CONDITIONS, RESULTS, model_slug
from .run import load_set
from .score import score_df


def check(model_id: str, set_name: str = "main") -> dict:
    slug = model_slug(model_id)
    p = RESULTS / "raw" / set_name / f"{slug}.jsonl"
    rows = [json.loads(l) for l in open(p, encoding="utf-8")]
    seen = Counter((r["item_id"], r["condition"]) for r in rows)
    sk = RESULTS / "raw" / set_name / f"{slug}.skipped.csv"
    skipped = {(r["item_id"], r["condition"]) for r in csv.DictReader(open(sk, encoding="utf-8"))} if sk.exists() else set()
    expected = {(it["item_id"], c) for it in load_set(set_name, None) for c in CONDITIONS}
    dup = [k for k, v in seen.items() if v > 1]
    missing = expected - set(seen) - skipped
    extra = set(seen) - expected
    both = set(seen) & skipped
    ok = not dup and not missing and not extra and not both
    df = score_df(pd.DataFrame(rows))
    acc = df.pivot_table(index="content_type", columns="condition", values="correct", aggfunc="mean")
    parse = df.groupby("condition")["parse_ok"].mean()
    res = dict(model_id=model_id, ok=ok, rows=len(rows), expected=len(expected), skipped=len(skipped),
               duplicates=len(dup), missing=len(missing), extra=len(extra),
               pct_length=round(100 * (df.finish_reason == "length").mean(), 2),
               parse={c: round(parse.get(c, float("nan")), 3) for c in CONDITIONS},
               acc={ct: {c: round(acc.loc[ct, c], 3) for c in CONDITIONS} for ct in acc.index},
               gen_hours=round(df.gen_seconds.sum() / 3600, 3))
    if ok:
        with open(p, "rb") as fi, gzip.open(str(p) + ".gz", "wb", compresslevel=9) as fo:
            shutil.copyfileobj(fi, fo)
    return res


if __name__ == "__main__":
    print(json.dumps(check(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "main"), indent=1))
