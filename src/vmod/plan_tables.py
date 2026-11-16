"""OWNER's Phase 4 plan (pasted 2026-11-16): the output files that plan names, built from the existing runs, plus the
resolution-control comparison. Numbers only.

NOTE: the 'replicates' rule (significant, same direction, in >= 2 of 3 runs) comes from the OWNER's plan, which was
written AFTER runs 2-3 finished. It is therefore post hoc, not pre-registered; the file says so.
"""
from __future__ import annotations

import itertools

import numpy as np
import pandas as pd

from . import analyze as an
from .analyze import A, B, holm, load_scored, mcnemar_family, read_csv, write_csv
from .config import RESULTS
from .replication import PRIMARY_RUNS, load_runs

SC = RESULTS / "scored"
RUN_LABEL = {1: "main", 2: "rep2", 3: "rep3"}


def replication_rq1():
    r = read_csv("replication_full_rq1_A_vs_B_per_run.csv")
    r.insert(1, "run_label", r.run.map(RUN_LABEL))
    write_csv(r, "replication_full_rq1.csv")
    return r


def replication_summary(r):
    rows = []
    for (mid, ct), g in r.groupby(["model_id", "content_type"]):
        sig = g[g.p_holm < 0.05]
        # 'same direction': count significant runs in each direction, take the larger
        n_pos, n_neg = int((sig["diff"] > 0).sum()), int((sig["diff"] < 0).sum())
        n_same = max(n_pos, n_neg)
        run1 = g[g.run == 1].iloc[0]
        rows.append(dict(model_id=mid, content_type=ct, n_runs=len(g), n_sig_same_dir=n_same,
                         sig_direction="A>B" if n_pos >= n_neg and n_same else ("B>A" if n_same else "none"),
                         replicates=n_same >= 2, sig_run1=bool(run1.p_holm < 0.05),
                         n_runs_agree_with_run1=int(((g.p_holm < 0.05) == (run1.p_holm < 0.05)).sum()) - 1,
                         diff_run1=run1["diff"], diff_mean=g["diff"].mean(), diff_min=g["diff"].min(), diff_max=g["diff"].max(),
                         max_abs_diff_across_runs=g["diff"].max() - g["diff"].min(),
                         rule="post hoc (OWNER plan written after runs 2-3): replicates = p_Holm < .05 same direction in >= 2 of 3 runs"))
    s = pd.DataFrame(rows)
    write_csv(s, "replication_full_summary.csv")
    return s


def cohen_kappa(x, y):
    x, y = np.asarray(x, bool), np.asarray(y, bool)
    po = (x == y).mean()
    pe = x.mean() * y.mean() + (1 - x.mean()) * (1 - y.mean())
    return float("nan") if pe == 1 else (po - pe) / (1 - pe)


def replication_agreement():
    df = load_runs(PRIMARY_RUNS)
    key = ["model_id", "content_type", "condition", "item_id"]
    rows = []
    for (mid, cond), g in df.groupby(["model_id", "condition"]):
        w_c = g.pivot_table(index=["content_type", "item_id"], columns="run", values="correct", aggfunc="first")
        w_t = g.pivot_table(index=["content_type", "item_id"], columns="run", values="response", aggfunc="first")
        for r1, r2 in itertools.combinations(sorted(g.run.unique()), 2):
            c = w_c[[r1, r2]].dropna().astype(bool)
            t = w_t[[r1, r2]].dropna()
            rows.append(dict(model_id=mid, condition=cond, pair=f"{RUN_LABEL[r1]}-{RUN_LABEL[r2]}", n_items=len(c),
                             pct_identical_text=100 * (t[r1] == t[r2]).mean(),
                             pct_correct_agree=100 * (c[r1] == c[r2]).mean(), cohen_kappa=cohen_kappa(c[r1], c[r2]),
                             acc_first=c[r1].mean(), acc_second=c[r2].mean(), abs_delta_acc=abs(c[r1].mean() - c[r2].mean())))
    a = pd.DataFrame(rows)
    write_csv(a, "replication_full_agreement.csv")
    return a


def ext_family6():
    """The plan's extension family was Gemma-27B + Qwen-72B only (Holm over 6). We ran 4 extension models (family of 12,
    ext_rq1_A_vs_B.csv); this re-Holms the plan's 6 cells for comparability."""
    e = read_csv("ext_rq1_A_vs_B.csv")
    e = e[e.model_id.isin(["google/gemma-3-27b-it", "Qwen/Qwen2.5-VL-72B-Instruct-AWQ"])].copy()
    e = e.rename(columns={"p_holm": "p_holm_family12"})
    e["p_holm_family6"] = holm(e["p_mcnemar_exact"])
    write_csv(e, "ext_rq1_A_vs_B_family6.csv")


RES_ARMS = [("Qwen/Qwen2.5-VL-7B-Instruct", "res896", "native resolution", "stretched to 896x896"),
            ("Qwen/Qwen2.5-VL-32B-Instruct", "res896", "native resolution", "stretched to 896x896"),
            ("google/gemma-3-12b-it", "res_gemma_nopas", "896x896 + pan-and-scan", "896x896, no pan-and-scan")]


def res_b_vs_b():
    """Paired McNemar, condition B in run 1 (original setting) vs condition B under the resolution-control setting.
    Holm over all arm x content cells. Also the A-B gap under each setting (A is unchanged: run-1 A)."""
    main = load_scored(SC / "main_all.csv.gz")
    out, gaps = [], []
    for mid, rs, lab1, lab2 in RES_ARMS:
        p = SC / f"{rs}_all.csv.gz"
        if not p.exists():
            continue
        rc = load_scored(p)
        rc = rc[(rc.model_id == mid) & (rc.condition == B)]
        if rc.empty:
            continue
        m = main[main.model_id == mid]
        both = pd.concat([m[m.condition == B], rc.assign(condition="B_rescontrol")], ignore_index=True)
        r = mcnemar_family(both, B, "B_rescontrol")
        r.insert(2, "setting_first", lab1)
        r.insert(3, "setting_second", lab2)
        out.append(r)
        for setting, bdf in ((lab1, m[m.condition == B]), (lab2, rc)):
            g = mcnemar_family(pd.concat([m[m.condition == A], bdf.assign(condition=B)], ignore_index=True), A, B)
            g.insert(2, "B_setting", setting)
            gaps.append(g.drop(columns="p_holm"))
    if not out:
        return None
    r = pd.concat(out, ignore_index=True)
    r["p_holm"] = holm(r["p_mcnemar_exact"])
    r = r.rename(columns={"acc_first": "acc_B_original", "acc_second": "acc_B_rescontrol", "diff": "diff_original_minus_rescontrol"})
    write_csv(r, "res_B_vs_B.csv")
    g = pd.concat(gaps, ignore_index=True).rename(columns={"diff": "gap_A_minus_B"})
    g["p_holm"] = holm(g["p_mcnemar_exact"])
    write_csv(g, "res_gap_A_minus_B_by_setting.csv")
    return r


def gap_vs_size_all():
    """The plan's file name for the size figure: the T18 figure (Qwen2.5 3/7/32/72B, Gemma 12/27B; open = extension)."""
    from .ext_analysis import gaps, size_figure

    orig = an.savefig
    import vmod.ext_analysis as ea

    ea.savefig = lambda fig, name: orig(fig, "gap_vs_size_all")
    try:
        size_figure(gaps())
    finally:
        ea.savefig = orig


def main():
    r = replication_rq1()
    replication_summary(r)
    replication_agreement()
    ext_family6()
    res_b_vs_b()
    gap_vs_size_all()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
