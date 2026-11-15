"""T17: G2 rule 1 on an extension model's pilot: keep only if parse rate >= 80% in every condition. Exit 0 = keep."""
from __future__ import annotations

import json
import sys

import pandas as pd

from .config import RESULTS, model_slug
from .score import score_df


def main(model_id: str) -> int:
    p = RESULTS / "raw" / "ext" / "pilot" / f"{model_slug(model_id)}.jsonl"
    if not p.exists():
        print(json.dumps(dict(model_id=model_id, keep=False, reason="no pilot output")))
        return 1
    df = score_df(pd.DataFrame([json.loads(l) for l in open(p, encoding="utf-8")]))
    parse = df.groupby("condition")["parse_ok"].mean().round(3).to_dict()
    keep = len(df) == 270 and min(parse.values()) >= 0.80
    print(json.dumps(dict(model_id=model_id, keep=keep, n=len(df), parse=parse,
                          pct_length=round(100 * (df.finish_reason == "length").mean(), 2))))
    return 0 if keep else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
