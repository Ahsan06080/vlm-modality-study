"""T16 (and T18 for extension models): replication analysis across runs 1-3. Numbers, tables and figures only."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .analyze import (A, B, C, CONDITIONS, CONTENT_TYPES, PALETTE, RESULTS, TICKS, holm, load_scored, mcnemar_family,
                      model_order, savefig, setup_mpl, write_csv)

SC = RESULTS / "scored"
PRIMARY_RUNS = {1: SC / "main_all.csv.gz", 2: SC / "main_run2_all.csv.gz", 3: SC / "main_run3_all.csv.gz"}
EXT_RUNS = {1: SC / "ext" / "run1_all.csv.gz", 2: SC / "ext" / "run2_all.csv.gz", 3: SC / "ext" / "run3_all.csv.gz"}
KEY = ["model_id", "content_type", "item_id", "condition"]


def load_runs(paths: dict) -> pd.DataFrame:
    """Stack the scored runs that exist; keep only models present in every run that exists for them (>= 2 runs)."""
    dfs = []
    for run, p in paths.items():
        if p.exists():
            d = load_scored(p)
            d["run"] = run
            dfs.append(d)
    df = pd.concat(dfs, ignore_index=True)
    n_runs = df.groupby("model_id")["run"].nunique()
    return df[df.model_id.isin(n_runs[n_runs >= 2].index)]


def complete_runs(df):
    """Models with all three runs (the replication tables use only complete triples)."""
    n = df.groupby("model_id")["run"].nunique()
    return df[df.model_id.isin(n[n == 3].index)]


def fleiss_kappa_binary(x: np.ndarray) -> float:
    """x: items x raters (0/1). Fleiss' kappa for 2 categories."""
    n_r = x.shape[1]
    k1 = x.sum(axis=1)
    counts = np.stack([n_r - k1, k1], axis=1)
    p_i = ((counts ** 2).sum(axis=1) - n_r) / (n_r * (n_r - 1))
    p_bar = p_i.mean()
    p_j = counts.sum(axis=0) / counts.sum()
    pe = (p_j ** 2).sum()
    return float("nan") if pe == 1 else float((p_bar - pe) / (1 - pe))


def accuracy_table(df):
    acc = df.groupby(["model_id", "content_type", "condition", "run"])["correct"].mean().unstack("run")
    acc.columns = [f"acc_run{r}" for r in acc.columns]
    runs = [c for c in acc.columns]
    acc["n_runs"] = acc[runs].notna().sum(axis=1)
    acc["mean"] = acc[runs].mean(axis=1)
    acc["sd"] = acc[runs].std(axis=1, ddof=1)
    acc["range"] = acc[runs].max(axis=1) - acc[runs].min(axis=1)
    return acc.reset_index()


def stability_table(df):
    w = df.pivot_table(index=KEY, columns="run", values="correct", aggfunc="first").dropna().reset_index()
    rows = []
    for (mid, ct, cond), g in w.groupby(["model_id", "content_type", "condition"]):
        x = g[[1, 2, 3]].astype(int).values
        s = x.sum(axis=1)
        rows.append(dict(model_id=mid, content_type=ct, condition=cond, n_items=len(g), fleiss_kappa=fleiss_kappa_binary(x),
                         pct_correct_all3=100 * (s == 3).mean(), pct_correct_none=100 * (s == 0).mean(),
                         pct_mixed=100 * ((s > 0) & (s < 3)).mean(),
                         pct_agree_run1_run2=100 * (x[:, 0] == x[:, 1]).mean(),
                         pct_agree_run1_run3=100 * (x[:, 0] == x[:, 2]).mean(),
                         pct_agree_run2_run3=100 * (x[:, 1] == x[:, 2]).mean()))
    return pd.DataFrame(rows)


def per_run_mcnemar(df, c1, c2):
    """RQ1 McNemar with its own Holm family (one family per run), long + wide agreement table."""
    long = []
    for run, g in df.groupby("run"):
        r = mcnemar_family(g, c1, c2)
        r.insert(0, "run", run)
        long.append(r)
    long = pd.concat(long, ignore_index=True)
    long["sig_holm"] = long.p_holm < 0.05
    long["direction"] = np.sign(long["diff"]).astype(int)
    w = long.pivot_table(index=["model_id", "content_type"], columns="run",
                         values=["diff", "diff_ci_lo", "diff_ci_hi", "p_holm", "sig_holm", "direction"], aggfunc="first")
    w.columns = [f"{a}_run{b}" for a, b in w.columns]
    w = w.reset_index()
    runs = sorted(long.run.unique())
    sig = w[[f"sig_holm_run{r}" for r in runs]].astype(bool)
    dirs = w[[f"direction_run{r}" for r in runs]]
    w["n_runs_sig"] = sig.sum(axis=1)
    w["sig_agree_all_runs"] = (sig.all(axis=1) | (~sig).all(axis=1))
    w["direction_agree_all_runs"] = dirs.nunique(axis=1) == 1
    w["sig_and_direction_agree"] = w.sig_agree_all_runs & w.direction_agree_all_runs
    return long, w


def majority_vote(df):
    mv = df.groupby(KEY)["correct"].agg(["sum", "count"]).reset_index()
    mv = mv[mv["count"] == 3]
    mv["correct"] = mv["sum"] >= 2
    return mv[KEY + ["correct"]]


def permutation_mean(df, c1, c2, n_perm=10000, seed=630):
    """Paired sign-flip permutation test on per-item mean correctness across runs (c1 - c2), two-sided; Holm over cells."""
    m = df.groupby(KEY)["correct"].mean().unstack("condition")
    rng = np.random.default_rng(seed)
    rows = []
    for (mid, ct), g in m.groupby(level=["model_id", "content_type"]):
        d = (g[c1] - g[c2]).dropna().values
        obs = d.mean()
        signs = rng.choice([-1.0, 1.0], size=(n_perm, len(d)))
        perm = (signs * d).mean(axis=1)
        p = (np.sum(np.abs(perm) >= abs(obs) - 1e-12) + 1) / (n_perm + 1)
        rows.append(dict(model_id=mid, content_type=ct, comparison=f"{c1} vs {c2}", n_items=len(d),
                         mean_acc_first=g[c1].mean(), mean_acc_second=g[c2].mean(), mean_diff=obs,
                         n_perm=n_perm, seed=seed, p_perm=p))
    r = pd.DataFrame(rows)
    r["p_holm"] = holm(r["p_perm"])
    return r


def rq2_split(df):
    """A vs C McNemar split by condition-C transcription correctness (exact, CER <= 0.02), per run."""
    out = []
    for run, g in df.groupby("run"):
        cdf = g[g.condition == C].copy()
        cdf["exact"] = cdf["transcription_exact"].astype(str).str.lower().eq("true")
        cdf["cer_ok"] = cdf["cer"].astype(float) <= 0.02
        for rule, col in (("exact", "exact"), ("cer_le_0.02", "cer_ok")):
            parts = []
            for good in (True, False):
                sel = cdf[cdf[col] == good][["model_id", "content_type", "item_id"]]
                r = mcnemar_family(g.merge(sel, on=["model_id", "content_type", "item_id"]), A, C)
                r.insert(0, "run", run)
                r.insert(3, "subset_rule", rule)
                r.insert(4, "transcription_correct", good)
                parts.append(r)
            p = pd.concat(parts, ignore_index=True)
            p["p_holm_within_rule_run"] = holm(p["p_mcnemar_exact"])
            out.append(p)
    long = pd.concat(out, ignore_index=True).rename(columns={"diff": "gap_A_minus_C"})
    # pattern check: gap among wrong transcriptions > gap among correct ones, per run
    w = long.pivot_table(index=["model_id", "content_type", "subset_rule", "run"], columns="transcription_correct",
                         values=["gap_A_minus_C", "n_pairs"], aggfunc="first")
    w.columns = [f"{a}_{'correct' if b else 'wrong'}" for a, b in w.columns]
    w = w.reset_index()
    w["gap_wrong_minus_correct"] = w["gap_A_minus_C_wrong"] - w["gap_A_minus_C_correct"]
    w["pattern_wrong_gt_correct"] = w["gap_wrong_minus_correct"] > 0
    return long, w


def figure(acc, name, title_suffix=""):
    plt = setup_mpl()
    models = model_order(acc)
    short = lambda m: m.split("/")[-1].replace("-Instruct", "").replace("-it", "")
    colors = dict(zip(CONDITIONS, PALETTE[:3]))
    runs = [c for c in acc.columns if c.startswith("acc_run")]
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8), sharey=True)
    w = 0.26
    for ax, ct in zip(axes, CONTENT_TYPES):
        for j, cond in enumerate(CONDITIONS):
            for i, m in enumerate(models):
                s = acc[(acc.model_id == m) & (acc.content_type == ct) & (acc.condition == cond)]
                if s.empty:
                    continue
                xpos = i + (j - 1) * w
                ys = s[runs].values.ravel()
                ys = ys[~np.isnan(ys)]
                ax.scatter(np.full(len(ys), xpos), ys, s=14, color=colors[cond], edgecolor="white", linewidth=0.6,
                           zorder=3, label=TICKS[j].replace("\n", " ") if (i == 0 and ct == CONTENT_TYPES[-1]) else None)
                ax.plot([xpos - w * 0.4, xpos + w * 0.4], [ys.mean()] * 2, color="#0b0b0b", lw=1.2, zorder=4)
        ax.set_title(ct)
        ax.set_xticks(range(len(models)), [short(m) for m in models], rotation=35, ha="right")
        ax.set_ylim(0, 1)
    axes[0].set_ylabel("accuracy (dots = runs, bar = mean)")
    axes[-1].legend(frameon=False, loc="center left", bbox_to_anchor=(1.0, 0.5), title="condition" + title_suffix)
    savefig(fig, name)
    plt.close(fig)


def main(which="primary"):
    paths, pre = (PRIMARY_RUNS, "replication_full") if which == "primary" else (EXT_RUNS, "ext_replication_full")
    df = load_runs(paths)
    acc = accuracy_table(df)
    write_csv(acc, f"{pre}_accuracy.csv")
    figure(acc, f"{pre}_accuracy_runs")
    full = complete_runs(df)
    if full.empty:
        print("no model with all 3 runs yet")
        return 0
    write_csv(stability_table(full), f"{pre}_stability.csv")
    for c1, c2, tag in ((A, B, "A_vs_B"), (A, C, "A_vs_C")):
        long, wide = per_run_mcnemar(full, c1, c2)
        write_csv(long, f"{pre}_rq1_{tag}_per_run.csv")
        write_csv(wide, f"{pre}_rq1_{tag}_agreement.csv")
        mv = mcnemar_family(majority_vote(full), c1, c2)
        write_csv(mv, f"{pre}_rq1_{tag}_majority_vote.csv")
    write_csv(permutation_mean(full, A, B), f"{pre}_rq1_A_vs_B_permutation_mean.csv")
    long, pat = rq2_split(full)
    write_csv(long, f"{pre}_rq2_A_vs_C_by_transcription_per_run.csv")
    write_csv(pat, f"{pre}_rq2_pattern_check.csv")
    print(f"{pre}: models with 3 runs: {sorted(full.model_id.unique())}")
    return 0
