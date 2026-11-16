"""Input-length moderator of the A-B (text vs image) gap. Primary 5 models. Numbers, tables and a figure only.

(a) descriptive: length terciles (source characters, within content type) x model -> acc A, acc B, gap, n
(b) logistic per content type on conditions A and B: correct ~ C(condition) * z_log_length + C(model),
    SEs clustered by item; term of interest condition[B]:z_log_length. Run 1 (primary).
(c) the same for runs 2 and 3 (robustness), same CSV with a `run` column.
(d) figure: A-B gap by tercile, one panel per content type, one line per model.
Outputs: results/analysis/input_length_gap_by_tercile.csv, results/analysis/input_length_interaction.csv,
         results/figures/input_length_gap.{pdf,png}. Run: .venv/bin/python scripts/analysis/input_length.py
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

from vmod.analyze import A, B, CONTENT_TYPES, MARKERS, PALETTE, load_scored, model_order, savefig, setup_mpl, write_csv
from vmod.config import DATA, RESULTS

SC = RESULTS / "scored"
RUNS = {1: SC / "main_all.csv.gz", 2: SC / "main_run2_all.csv.gz", 3: SC / "main_run3_all.csv.gz"}
SHORT = lambda m: m.split("/")[-1].replace("-Instruct", "").replace("-it", "")


def item_lengths():
    rows = []
    for ct in CONTENT_TYPES:
        for l in open(DATA / "items" / f"main_{ct}.jsonl", encoding="utf-8"):
            d = json.loads(l)
            rows.append(dict(item_id=d["item_id"], content_type=ct, n_chars=d["n_chars"], n_lines=d["n_lines"]))
    it = pd.DataFrame(rows)
    assert (it.n_chars == it.n_chars).all()
    it["log_len"] = np.log(it.n_chars)
    it["z_log_length"] = it.groupby("content_type").log_len.transform(lambda s: (s - s.mean()) / s.std(ddof=0))
    it["tercile"] = it.groupby("content_type").n_chars.transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=[1, 2, 3])).astype(int)
    return it


def prep(path, it):
    d = load_scored(path)
    d = d[d.condition.isin([A, B])].copy()
    d["correct"] = d.correct.astype(str).str.lower().eq("true").astype(int)
    d["model"] = d.model_id.map(SHORT)
    return d.merge(it, on=["item_id", "content_type"], validate="many_to_one")


def tercile_table(d, it):
    g = d.pivot_table(index=["model_id", "content_type", "tercile", "item_id"], columns="condition", values="correct").reset_index()
    t = g.groupby(["model_id", "content_type", "tercile"]).agg(n=("item_id", "size"), acc_A=(A, "mean"), acc_B=(B, "mean")).reset_index()
    t["gap_A_minus_B"] = t.acc_A - t.acc_B
    rng = it.groupby(["content_type", "tercile"]).agg(chars_min=("n_chars", "min"), chars_median=("n_chars", "median"),
                                                     chars_max=("n_chars", "max"), lines_median=("n_lines", "median")).reset_index()
    return t.merge(rng, on=["content_type", "tercile"])


def interaction(d, run):
    rows = []
    for ct in CONTENT_TYPES:
        g = d[d.content_type == ct].copy()
        groups = pd.factorize(g.item_id)[0]
        f = smf.logit("correct ~ C(condition, Treatment('A_text')) * z_log_length + C(model)", data=g)
        r = f.fit(disp=0, maxiter=200, cov_type="cluster", cov_kwds={"groups": groups})
        for term in r.params.index:
            if "z_log_length" not in term:
                continue
            rows.append(dict(run=run, content_type=ct, term=term.replace("C(condition, Treatment('A_text'))", "condition"),
                             coef=r.params[term], se_cluster_item=r.bse[term], z=r.tvalues[term], p_value=r.pvalues[term],
                             odds_ratio=np.exp(r.params[term]), or_ci_lo=np.exp(r.params[term] - 1.959964 * r.bse[term]),
                             or_ci_hi=np.exp(r.params[term] + 1.959964 * r.bse[term]), n_obs=int(r.nobs), n_items=g.item_id.nunique(),
                             n_models=g.model.nunique(), converged=bool(r.mle_retvals.get("converged", True)),
                             formula="correct ~ condition * z_log_length + model; logit; SE clustered by item",
                             length_def="z-score (within content type) of log(source characters)"))
    return pd.DataFrame(rows)


def figure(t):
    plt = setup_mpl()
    models = model_order(t)
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.4), sharey=True)
    for ax, ct in zip(axes, CONTENT_TYPES):
        for i, m in enumerate(models):
            s = t[(t.model_id == m) & (t.content_type == ct)].sort_values("tercile")
            ax.plot(s.tercile, s.gap_A_minus_B, marker=MARKERS[i], color=PALETTE[i], lw=2, ms=6, label=SHORT(m))
        ax.axhline(0, color="#52514e", lw=0.8)
        ax.set_xticks([1, 2, 3], ["short", "middle", "long"])
        ax.set_title(ct)
        ax.set_xlabel("input-length tercile (source characters)")
    axes[0].set_ylabel("accuracy A − B (run 1)")
    axes[-1].legend(frameon=False, loc="center left", bbox_to_anchor=(1.0, 0.5))
    savefig(fig, "input_length_gap")
    plt.close(fig)


def main():
    it = item_lengths()
    inter = []
    for run, p in RUNS.items():
        d = prep(p, it)
        if run == 1:
            t = tercile_table(d, it)
            write_csv(t, "input_length_gap_by_tercile.csv")
            figure(t)
        inter.append(interaction(d, run))
    write_csv(pd.concat(inter, ignore_index=True), "input_length_interaction.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
