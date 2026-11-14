"""T07 pilot report and T07b replication check."""
from __future__ import annotations

import csv
import json

import numpy as np
import pandas as pd

from .config import CONDITIONS, RESULTS, load_config, model_slug
from .meta import header_lines
from .score import read_raw, score_df

ANALYSIS = RESULTS / "analysis"


def skipped_count(set_name, model_id):
    p = RESULTS / "raw" / set_name / f"{model_slug(model_id)}.skipped.csv"
    if not p.exists():
        return 0
    return sum(1 for _ in csv.DictReader(open(p, encoding="utf-8")))


def pilot_report(set_name="pilot"):
    cfg = load_config()
    df = score_df(read_raw(set_name))
    out = []
    lines = []
    est = {}
    for mid, g in df.groupby("model_id", sort=False):
        n_req = len(g)
        secs = g["gen_seconds"].sum()
        sp100 = 100 * secs / n_req
        parse = g.groupby("condition")["parse_ok"].mean()
        parse_s = g.groupby("condition")["parse_ok_strict"].mean()
        acc = g.pivot_table(index="content_type", columns="condition", values="correct", aggfunc="mean")
        length = g.groupby(["content_type", "condition"])["finish_reason"].apply(lambda s: (s == "length").mean())
        mot = g.groupby("condition")["output_tokens"].mean()
        est[mid] = {N: secs / n_req * N * 3 * 3 for N in (500, 300)}
        lines.append(f"#### {mid}  (requests {n_req}, skipped {skipped_count(set_name, mid)}, {sp100:.1f} s/100 prompts)")
        lines.append("| | " + " | ".join(CONDITIONS) + " |")
        lines.append("|---|" + "---|" * len(CONDITIONS))
        lines.append("| parse rate | " + " | ".join(f"{parse.get(c, np.nan):.3f}" for c in CONDITIONS) + " |")
        lines.append("| parse rate (strict) | " + " | ".join(f"{parse_s.get(c, np.nan):.3f}" for c in CONDITIONS) + " |")
        for ct in acc.index:
            lines.append(f"| acc {ct} | " + " | ".join(f"{acc.loc[ct].get(c, np.nan):.3f}" for c in CONDITIONS) + " |")
        lines.append("| mean out tokens | " + " | ".join(f"{mot.get(c, np.nan):.0f}" for c in CONDITIONS) + " |")
        lines.append("| max % length (over content) | " + " | ".join(
            f"{100 * length.xs(c, level='condition').max():.1f}" for c in CONDITIONS) + " |")
        lines.append("")
        for c in CONDITIONS:
            out.append(dict(model_id=mid, condition=c, parse_rate=parse.get(c), parse_rate_strict=parse_s.get(c),
                            mean_output_tokens=mot.get(c),
                            max_pct_length=100 * length.xs(c, level="condition").max(),
                            **{f"acc_{ct}": acc.loc[ct].get(c) for ct in acc.index},
                            sec_per_100=sp100, skipped=skipped_count(set_name, mid)))
    ANALYSIS.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(out).to_csv(ANALYSIS / f"{set_name}_report.csv", index=False)
    (ANALYSIS / f"{set_name}_estimates.json").write_text(json.dumps(est, indent=1))
    print("\n".join(lines))
    print("main-run time estimates (hours, generation only):")
    for mid, e in est.items():
        print(f"  {mid}: N=500 {e[500] / 3600:.2f} h, N=300 {e[300] / 3600:.2f} h")
    return df


def kappa(a, b):
    a, b = np.asarray(a, bool), np.asarray(b, bool)
    po = (a == b).mean()
    pe = a.mean() * b.mean() + (1 - a.mean()) * (1 - b.mean())
    return float("nan") if pe == 1 else (po - pe) / (1 - pe)


def replication_check():
    r1 = score_df(read_raw("pilot"))
    r2 = score_df(read_raw("pilot_rep2"))
    key = ["model_id", "item_id", "condition"]
    m = r1.merge(r2, on=key, suffixes=("_1", "_2"))
    rows = []
    for (mid, c), g in m.groupby(["model_id", "condition"], sort=False):
        rows.append(dict(model_id=mid, condition=c, n=len(g),
                         pct_identical_text=100 * (g["response_1"] == g["response_2"]).mean(),
                         pct_correct_agree=100 * (g["correct_1"] == g["correct_2"]).mean(),
                         kappa_correct=kappa(g["correct_1"], g["correct_2"]),
                         acc_run1=g["correct_1"].mean(), acc_run2=g["correct_2"].mean()))
    df = pd.DataFrame(rows)
    df["abs_acc_diff"] = (df["acc_run1"] - df["acc_run2"]).abs()
    # largest abs accuracy difference across all model x content x condition cells
    cell = m.groupby(["model_id", "content_type_1", "condition"])[["correct_1", "correct_2"]].mean()
    max_cell = (cell["correct_1"] - cell["correct_2"]).abs()
    ANALYSIS.mkdir(parents=True, exist_ok=True)
    with open(ANALYSIS / "replication_check.csv", "w", encoding="utf-8") as f:
        f.write(header_lines())
        df.to_csv(f, index=False, float_format="%.4f")
    print(df.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print(f"largest |acc run1 - run2| over model x content x condition cells: {max_cell.max():.3f} at {max_cell.idxmax()}")
    print("min correct agreement:", df["pct_correct_agree"].min())
    return df, max_cell
