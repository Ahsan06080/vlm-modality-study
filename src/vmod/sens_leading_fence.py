"""Sensitivity (approved after T18): 'leading code fence = transcription'.

Some models (InternVL3.5-8B, and also gemma-3-12b on code) answer condition C by starting the response with a code
fence holding the copied problem, with no <transcription> tags and no 'Transcription' heading. The frozen extractor
(scoring.extract_transcription_src) finds nothing in those responses. This rule adds ONE fallback, applied only when the
frozen extractor returns 'none': if the response begins (after whitespace) with a ``` fence, the fence body is the
transcription (source = 'leading_fence'). Metrics are the frozen transcription_metrics. Primary scored files and primary
analysis CSVs are NOT changed; every output here is suffixed 'sens_leading_fence'. Numbers only.
"""
from __future__ import annotations

import re

import pandas as pd

from . import analyze as an
from .analyze import C, load_scored, write_csv
from .config import DATA, RESULTS, CONTENT_TYPES
from .scoring import transcription_metrics

import json

SC = RESULTS / "scored"
SETS = {"primary": {1: SC / "main_all.csv.gz", 2: SC / "main_run2_all.csv.gz", 3: SC / "main_run3_all.csv.gz"},
        "ext": {1: SC / "ext" / "run1_all.csv.gz", 2: SC / "ext" / "run2_all.csv.gz", 3: SC / "ext" / "run3_all.csv.gz"}}
LEADING_FENCE = re.compile(r"\A\s*```[^\n]*\n(.*?)^[ \t]*```", re.S | re.M)
TAG = "sens_leading_fence"


def leading_fence(response):
    m = LEADING_FENCE.match(response or "")
    return m.group(1) if m else None


def items_content():
    out = {}
    for ct in CONTENT_TYPES:
        for l in open(DATA / "items" / f"main_{ct}.jsonl", encoding="utf-8"):
            r = json.loads(l)
            out[r["item_id"]] = r["content"]
    return out


def apply_rule(df, content):
    """Return a copy with the fallback applied to condition-C rows whose frozen source is 'none'."""
    df = df.copy()
    sel = (df.condition == C) & (df.transcription_source == "none")
    n_changed = 0
    for i in df.index[sel]:
        t = leading_fence(df.at[i, "response"] if isinstance(df.at[i, "response"], str) else "")
        if t is None:
            continue
        m = transcription_metrics(t, content[df.at[i, "item_id"]])
        df.at[i, "transcription"] = t
        df.at[i, "transcription_exact"] = m["transcription_exact"]
        df.at[i, "transcription_exact_lenient"] = m["transcription_exact_lenient"]
        df.at[i, "cer"] = m["cer"]
        df.at[i, "cer_raw"] = m["cer_raw"]
        df.at[i, "transcription_source"] = "leading_fence"
        n_changed += 1
    return df, n_changed


def recovered_table(before, after, label, run):
    b = before[before.condition == C]
    a = after[after.condition == C]
    rows = []
    for (mid, ct), g in a.groupby(["model_id", "content_type"]):
        gb = b[(b.model_id == mid) & (b.content_type == ct)]
        lf = g[g.transcription_source == "leading_fence"]
        cer = lf.cer.astype(float)
        ex = lambda s: s.astype(str).str.lower().eq("true")
        rows.append(dict(set=label, run=run, model_id=mid, content_type=ct, n=len(g),
                         pct_with_transcription_frozen=100 * gb.transcription.notna().mean(),
                         pct_with_transcription_sens=100 * g.transcription.notna().mean(),
                         n_recovered_leading_fence=len(lf),
                         recovered_exact_rate=ex(lf.transcription_exact).mean() if len(lf) else float("nan"),
                         recovered_pct_cer_le_002=100 * (cer <= 0.02).mean() if len(lf) else float("nan"),
                         recovered_cer_median=cer.median() if len(lf) else float("nan"),
                         exact_rate_frozen=ex(gb.transcription_exact).mean(), exact_rate_sens=ex(g.transcription_exact).mean()))
    return pd.DataFrame(rows)


def main():
    from .replication import rq2_split

    content = items_content()
    rec = []
    for label, paths in SETS.items():
        pre = "" if label == "primary" else "ext_"
        runs = {}
        for run, p in paths.items():
            d0 = load_scored(p)
            d1, n = apply_rule(d0, content)
            print(f"{label} run{run}: {n} condition-C responses recovered by the leading-fence rule")
            rec.append(recovered_table(d0, d1, label, run))
            d1["run"] = run
            runs[run] = d1
        # run 1: the full T13 RQ2 analysis (transcription table, A vs C split, logit) under the rule, own file names
        orig = an.write_csv
        an.write_csv = lambda d, name, _p=pre: orig(d, f"{_p}{name[:-4]}_{TAG}.csv")
        try:
            an.rq2(runs[1].drop(columns="run"))
        finally:
            an.write_csv = orig
        # runs 1-3: per-run split + pattern check (same as replication T16/T18)
        long, pat = rq2_split(pd.concat(runs.values(), ignore_index=True))
        rp = "replication_full" if label == "primary" else "ext_replication_full"
        write_csv(long, f"{rp}_rq2_A_vs_C_by_transcription_per_run_{TAG}.csv")
        write_csv(pat, f"{rp}_rq2_pattern_check_{TAG}.csv")
    write_csv(pd.concat(rec, ignore_index=True), f"{TAG}_recovered.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
