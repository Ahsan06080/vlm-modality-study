"""T11-T14: descriptives, RQ1 (modality effect), RQ2 (perception vs reasoning), RQ3 (length), error sample.
Numbers, tables and figures only."""
from __future__ import annotations

import json
import math

import numpy as np
import pandas as pd
from scipy import stats

from .config import CONDITIONS, CONTENT_TYPES, RESULTS, load_config
from .meta import header_lines

ANALYSIS = RESULTS / "analysis"
FIGS = RESULTS / "figures"
SCORED = RESULTS / "scored" / "main_all.csv.gz"
A, B, C = CONDITIONS
COND_SHORT = {A: "A text", B: "B image", C: "C image+transcribe"}
PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
MARKERS = ["o", "s", "^", "D", "v", "P", "X", "*"]


# ------------------------------------------------------------------ helpers
def write_csv(df: pd.DataFrame, name: str):
    ANALYSIS.mkdir(parents=True, exist_ok=True)
    with open(ANALYSIS / name, "w", encoding="utf-8") as f:
        f.write(header_lines())
        df.to_csv(f, index=False, float_format="%.6g")


def read_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(ANALYSIS / name, comment="#")


def load_scored(path=SCORED) -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False)
    for c in ("parse_ok", "parse_ok_strict", "correct", "correct_strict"):
        df[c] = df[c].astype(bool)
    return df


def model_order(df) -> list[str]:
    ids = [m["id"] for m in load_config()["models"]["local"]]
    present = list(df["model_id"].unique())
    return [m for m in ids if m in present] + sorted(set(present) - set(ids))


def params_b(mid):
    for m in load_config()["models"]["local"]:
        if m["id"] == mid:
            return m["params_b"]
    return np.nan


def wilson(k, n, z=1.959964):
    if n == 0:
        return (np.nan, np.nan)
    p = k / n
    den = 1 + z * z / n
    cen = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (cen - half, cen + half)


def holm(p):
    p = np.asarray(p, float)
    out = np.full_like(p, np.nan)
    ok = ~np.isnan(p)
    idx = np.where(ok)[0]
    order = idx[np.argsort(p[idx])]
    m = len(order)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (m - rank) * p[i]))
        out[i] = running
    return out


def mcnemar_exact(b, c):
    n = b + c
    if n == 0:
        return 1.0
    return float(min(1.0, stats.binomtest(min(b, c), n, 0.5).pvalue))


def newcombe_paired(a, b, c, d, z=1.959964):
    """Newcombe (1998) method 10 CI for p1 - p2 with paired data. a=both correct, b=1 only, c=2 only, d=neither."""
    n = a + b + c + d
    p1, p2 = (a + b) / n, (a + c) / n
    l1, u1 = wilson(a + b, n, z)
    l2, u2 = wilson(a + c, n, z)
    den = math.sqrt((a + b) * (c + d) * (a + c) * (b + d))
    if den == 0:
        phi = 0.0
    else:
        num = a * d - b * c
        phi = (max(num - n / 2, 0) if num > 0 else num) / den
    diff = p1 - p2
    dl = math.sqrt(max(0.0, (p1 - l1) ** 2 - 2 * phi * (p1 - l1) * (u2 - p2) + (u2 - p2) ** 2))
    du = math.sqrt(max(0.0, (u1 - p1) ** 2 - 2 * phi * (u1 - p1) * (p2 - l2) + (p2 - l2) ** 2))
    return diff, diff - dl, diff + du


def discordant_or(b, c, alpha=0.05):
    """b/c with exact conditional CI (Clopper-Pearson on b ~ Bin(b+c, p), OR = p/(1-p))."""
    n = b + c
    if n == 0:
        return np.nan, np.nan, np.nan
    orr = b / c if c > 0 else np.inf
    lo = stats.beta.ppf(alpha / 2, b, n - b + 1) if b > 0 else 0.0
    hi = stats.beta.ppf(1 - alpha / 2, b + 1, n - b) if b < n else 1.0
    tr = lambda p: p / (1 - p) if p < 1 else np.inf
    return orr, tr(lo), tr(hi)


def paired(df, col, c1, c2):
    """Wide frame: one row per (model, content, item) with col for both conditions."""
    w = df[df["condition"].isin([c1, c2])].pivot_table(index=["model_id", "content_type", "item_id"],
                                                         columns="condition", values=col, aggfunc="first")
    return w.dropna(subset=[c1, c2]).reset_index()


def setup_mpl():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                         "axes.edgecolor": "#52514e", "axes.labelcolor": "#0b0b0b", "xtick.color": "#52514e",
                         "ytick.color": "#52514e", "axes.grid": True, "grid.color": "#e6e5e0", "grid.linewidth": 0.6,
                         "figure.facecolor": "white", "axes.facecolor": "white", "savefig.dpi": 200})
    return plt


def savefig(fig, name):
    FIGS.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGS / f"{name}.png", bbox_inches="tight")
    fig.savefig(FIGS / f"{name}.pdf", bbox_inches="tight")


# ------------------------------------------------------------------ T11
def descriptives(df):
    rows = []
    for (mid, ct, cond), g in df.groupby(["model_id", "content_type", "condition"]):
        n, k = len(g), int(g["correct"].sum())
        lo, hi = wilson(k, n)
        ot = g["output_tokens"]
        rows.append(dict(model_id=mid, content_type=ct, condition=cond, n=n, n_correct=k, accuracy=k / n,
                         ci95_lo=lo, ci95_hi=hi, parse_rate=g["parse_ok"].mean(),
                         parse_rate_strict=g["parse_ok_strict"].mean(),
                         accuracy_strict=g["correct_strict"].mean(),
                         pct_finish_length=100 * (g["finish_reason"] == "length").mean(),
                         out_tok_mean=ot.mean(), out_tok_median=ot.median(), out_tok_sd=ot.std(),
                         out_tok_q1=ot.quantile(0.25), out_tok_q3=ot.quantile(0.75),
                         out_tok_iqr=ot.quantile(0.75) - ot.quantile(0.25), out_tok_min=ot.min(), out_tok_max=ot.max(),
                         in_tok_mean=g["input_tokens"].mean()))
    d = pd.DataFrame(rows)
    order = {m: i for i, m in enumerate(model_order(df))}
    d = d.sort_values(["model_id", "content_type", "condition"], key=lambda s: s.map(order) if s.name == "model_id" else s)
    write_csv(d, "descriptives.csv")

    # input length per content type (unique items)
    from .score import load_items

    items = load_items()
    ids = df["item_id"].unique()
    il = pd.DataFrame([dict(content_type=items[i]["content_type"], n_chars=items[i]["n_chars"],
                            n_lines=items[i]["n_lines"]) for i in ids])
    inl = il.groupby("content_type").agg(n_items=("n_chars", "size"), chars_mean=("n_chars", "mean"),
                                         chars_median=("n_chars", "median"), chars_min=("n_chars", "min"),
                                         chars_max=("n_chars", "max"), lines_mean=("n_lines", "mean"),
                                         lines_median=("n_lines", "median"), lines_min=("n_lines", "min"),
                                         lines_max=("n_lines", "max")).reset_index()
    write_csv(inl, "input_length.csv")

    # outliers: output tokens > Q3 + 3 IQR within the model x content x condition cell, or finish_reason=length
    df = df.copy()
    g = df.groupby(["model_id", "content_type", "condition"])["output_tokens"]
    q1, q3 = g.transform(lambda s: s.quantile(0.25)), g.transform(lambda s: s.quantile(0.75))
    df["outlier_tokens"] = df["output_tokens"] > q3 + 3 * (q3 - q1)
    df["outlier_length"] = df["finish_reason"] == "length"
    out = df[df["outlier_tokens"] | df["outlier_length"]]
    write_csv(out[["model_id", "content_type", "condition", "item_id", "output_tokens", "finish_reason",
                   "outlier_tokens", "outlier_length", "correct"]], "outliers.csv")
    oc = df.groupby(["model_id", "content_type", "condition"]).agg(
        n=("item_id", "size"), n_outlier_tokens=("outlier_tokens", "sum"), n_finish_length=("outlier_length", "sum")).reset_index()
    write_csv(oc, "outlier_counts.csv")
    figures_t11(df, d)
    return d


def figures_t11(df, d):
    plt = setup_mpl()
    models = model_order(df)
    colors = {m: PALETTE[i] for i, m in enumerate(models)}
    marks = {m: MARKERS[i] for i, m in enumerate(models)}
    short = lambda m: m.split("/")[-1].replace("-Instruct", "").replace("-it", "")

    # accuracy by condition, faceted by content type
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.4), sharey=True)
    x = np.arange(len(CONDITIONS))
    for ax, ct in zip(axes, CONTENT_TYPES):
        for m in models:
            s = d[(d.model_id == m) & (d.content_type == ct)].set_index("condition").reindex(CONDITIONS)
            yerr = np.vstack([s.accuracy - s.ci95_lo, s.ci95_hi - s.accuracy])
            ax.errorbar(x, s.accuracy, yerr=yerr, color=colors[m], marker=marks[m], ms=6, lw=2, capsize=2,
                        elinewidth=1, label=short(m))
        ax.set_title(ct, color="#0b0b0b")
        ax.set_xticks(x, [COND_SHORT[c].replace(" ", "\n", 1) for c in CONDITIONS])
        ax.set_ylim(0, 1)
    axes[0].set_ylabel("accuracy (95% Wilson CI)")
    axes[-1].legend(frameon=False, loc="center left", bbox_to_anchor=(1.0, 0.5))
    savefig(fig, "accuracy_by_condition")
    plt.close(fig)

    # output-token box plots per condition (faceted by content, grouped by model)
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.6), sharey=True)
    w = 0.8 / len(models)
    for ax, ct in zip(axes, CONTENT_TYPES):
        for i, m in enumerate(models):
            data = [df[(df.model_id == m) & (df.content_type == ct) & (df.condition == c)]["output_tokens"].values
                    for c in CONDITIONS]
            pos = x + (i - (len(models) - 1) / 2) * w
            bp = ax.boxplot(data, positions=pos, widths=w * 0.85, patch_artist=True, showfliers=True,
                            flierprops=dict(marker=".", ms=2, markeredgecolor=colors[m], alpha=0.5),
                            medianprops=dict(color="#0b0b0b", lw=1), whiskerprops=dict(color=colors[m]),
                            capprops=dict(color=colors[m]), boxprops=dict(edgecolor="white", lw=0.5))
            for b in bp["boxes"]:
                b.set_facecolor(colors[m])
            if ct == CONTENT_TYPES[-1]:
                ax.plot([], [], color=colors[m], lw=6, label=short(m))
        ax.set_yscale("log")
        ax.set_title(ct)
        ax.set_xticks(x, [COND_SHORT[c].replace(" ", "\n", 1) for c in CONDITIONS])
    axes[0].set_ylabel("output tokens (log scale)")
    axes[-1].legend(frameon=False, loc="center left", bbox_to_anchor=(1.0, 0.5))
    savefig(fig, "output_tokens_boxplot")
    plt.close(fig)

    # accuracy gap (A - B) vs model size, Qwen family, from the paired Newcombe CIs if available
    q = [m for m in models if "Qwen" in m]
    if q:
        fig, ax = plt.subplots(figsize=(4.8, 3.4))
        ct_colors = {ct: PALETTE[i] for i, ct in enumerate(CONTENT_TYPES)}
        try:
            r = read_csv("rq1_A_vs_B.csv")
        except FileNotFoundError:
            r = None
        for j, ct in enumerate(CONTENT_TYPES):
            xs, ys, lo, hi = [], [], [], []
            for m in q:
                xs.append(params_b(m))
                if r is not None:
                    row = r[(r.model_id == m) & (r.content_type == ct)].iloc[0]
                    ys.append(row["diff"]); lo.append(row["diff"] - row["diff_ci_lo"]); hi.append(row["diff_ci_hi"] - row["diff"])
                else:
                    s = d[(d.model_id == m) & (d.content_type == ct)].set_index("condition")
                    ys.append(s.accuracy[A] - s.accuracy[B]); lo.append(0); hi.append(0)
            ax.errorbar(np.array(xs) * (1 + (j - 1) * 0.04), ys, yerr=[lo, hi], color=ct_colors[ct], marker=MARKERS[j],
                        ms=6, lw=2, capsize=2, elinewidth=1, label=ct)
        ax.axhline(0, color="#52514e", lw=0.8)
        ax.set_xscale("log")
        ax.set_xticks([params_b(m) for m in q], [f"{params_b(m):g}B" for m in q])
        ax.minorticks_off()
        ax.set_xlabel("Qwen2.5-VL size (parameters)")
        ax.set_ylabel("accuracy A − B (95% CI)")
        ax.legend(frameon=False)
        savefig(fig, "gap_A_minus_B_vs_size_qwen")
        plt.close(fig)


# ------------------------------------------------------------------ T12
def mcnemar_family(df, c1, c2, col="correct"):
    w = paired(df, col, c1, c2)
    rows = []
    for (mid, ct), g in w.groupby(["model_id", "content_type"]):
        x1, x2 = g[c1].astype(bool).values, g[c2].astype(bool).values
        a, b = int((x1 & x2).sum()), int((x1 & ~x2).sum())
        c, d = int((~x1 & x2).sum()), int((~x1 & ~x2).sum())
        n = a + b + c + d
        diff, lo, hi = newcombe_paired(a, b, c, d)
        orr, olo, ohi = discordant_or(b, c)
        rows.append(dict(model_id=mid, content_type=ct, comparison=f"{c1} vs {c2}", n_pairs=n, both_correct=a,
                         b_first_only=b, c_second_only=c, both_wrong=d, acc_first=(a + b) / n, acc_second=(a + c) / n,
                         diff=diff, diff_ci_lo=lo, diff_ci_hi=hi, discordant_or=orr, or_ci_lo=olo, or_ci_hi=ohi,
                         p_mcnemar_exact=mcnemar_exact(b, c)))
    r = pd.DataFrame(rows)
    if len(r):
        r["p_holm"] = holm(r["p_mcnemar_exact"])
    return r


def rq1(df):
    fams = {"A_vs_B": (A, B), "A_vs_C": (A, C), "B_vs_C": (B, C)}
    out = {}
    for name, (c1, c2) in fams.items():
        r = mcnemar_family(df, c1, c2)
        write_csv(r, f"rq1_{name}.csv")
        out[name] = r
        # sensitivity: exclude unparseable responses (drop the pair if either response is unparseable)
        keep = paired(df, "parse_ok", c1, c2)
        keep = keep[keep[c1].astype(bool) & keep[c2].astype(bool)][["model_id", "content_type", "item_id"]]
        sub = df.merge(keep, on=["model_id", "content_type", "item_id"])
        rs = mcnemar_family(sub, c1, c2)
        write_csv(rs, f"rq1_{name}_sens_parseable.csv")
        # sensitivity 2: strict literal parser (unparseable under the strict rule = incorrect)
        rs2 = mcnemar_family(df, c1, c2, col="correct_strict")
        write_csv(rs2, f"rq1_{name}_sens_strict_parser.csv")
    # Cochran's Q across A/B/C
    from statsmodels.stats.contingency_tables import cochrans_q

    rows = []
    w = df.pivot_table(index=["model_id", "content_type", "item_id"], columns="condition", values="correct",
                       aggfunc="first").dropna().reset_index()
    for (mid, ct), g in w.groupby(["model_id", "content_type"]):
        x = g[list(CONDITIONS)].astype(int).values
        if (x.min(axis=1) == x.max(axis=1)).all():
            q, p = 0.0, 1.0
        else:
            res = cochrans_q(x)
            q, p = float(res.statistic), float(res.pvalue)
        rows.append(dict(model_id=mid, content_type=ct, n_items=len(g), acc_A=x[:, 0].mean(), acc_B=x[:, 1].mean(),
                         acc_C=x[:, 2].mean(), cochran_q=q, df=2, p_value=p))
    cq = pd.DataFrame(rows)
    cq["p_holm"] = holm(cq["p_value"])
    write_csv(cq, "rq1_cochran_q.csv")
    out["cochran"] = cq
    return out


# ------------------------------------------------------------------ T13
def rq2(df):
    cdf = df[df.condition == C].copy()
    cdf["transcription_exact"] = cdf["transcription_exact"].astype(str).str.lower().eq("true")
    cdf["has_transcription"] = cdf["transcription"].notna()
    rows = []
    for (mid, ct), g in cdf.groupby(["model_id", "content_type"]):
        cer = g["cer"].astype(float)
        srcs = g["transcription_source"].value_counts()
        rows.append(dict(model_id=mid, content_type=ct, n=len(g), pct_with_transcription=100 * g.has_transcription.mean(),
                         pct_src_tags=100 * srcs.get("tags", 0) / len(g), pct_src_open_tag=100 * srcs.get("open_tag", 0) / len(g),
                         pct_src_heading_fence=100 * srcs.get("heading_fence", 0) / len(g),
                         pct_src_none=100 * srcs.get("none", 0) / len(g),
                         exact_rate=g.transcription_exact.mean(), pct_cer_le_002=100 * (cer <= 0.02).mean(),
                         cer_mean=cer.mean(), cer_sd=cer.std(), cer_p10=cer.quantile(0.1), cer_q1=cer.quantile(0.25),
                         cer_median=cer.median(), cer_q3=cer.quantile(0.75), cer_p90=cer.quantile(0.9), cer_max=cer.max()))
    write_csv(pd.DataFrame(rows), "rq2_transcription.csv")

    # A vs C McNemar within subsets defined by condition-C transcription quality
    tq = cdf[["model_id", "content_type", "item_id", "transcription_exact", "cer"]]
    sub_rows = []
    for label, flag in (("exact", lambda t: t.transcription_exact), ("cer_le_0.02", lambda t: t.cer.astype(float) <= 0.02)):
        for good in (True, False):
            sel = tq[flag(tq) == good][["model_id", "content_type", "item_id"]]
            r = mcnemar_family(df.merge(sel, on=["model_id", "content_type", "item_id"]), A, C)
            r.insert(2, "subset_rule", label)
            r.insert(3, "transcription_correct", good)
            r["gap_A_minus_C"] = r["diff"]
            sub_rows.append(r)
    # sensitivity: only responses whose transcription came from the <transcription> tags (no heading fallback)
    tags = cdf[cdf["transcription_source"] == "tags"][["model_id", "content_type", "item_id", "transcription_exact"]]
    for good in (True, False):
        sel = tags[tags.transcription_exact == good][["model_id", "content_type", "item_id"]]
        r = mcnemar_family(df.merge(sel, on=["model_id", "content_type", "item_id"]), A, C)
        r.insert(2, "subset_rule", "exact_tags_only")
        r.insert(3, "transcription_correct", good)
        r["gap_A_minus_C"] = r["diff"]
        sub_rows.append(r)
    sr = pd.concat(sub_rows, ignore_index=True)
    sr["p_holm_within_rule"] = np.nan
    for rule in sr.subset_rule.unique():
        m = sr.subset_rule == rule
        sr.loc[m, "p_holm_within_rule"] = holm(sr.loc[m, "p_mcnemar_exact"])
    write_csv(sr, "rq2_A_vs_C_by_transcription.csv")

    # logistic: correct in B ~ CER from C + model (fixed effect), per content type, pooled over models
    import statsmodels.formula.api as smf

    bb = df[df.condition == B][["model_id", "content_type", "item_id", "correct"]].merge(
        tq, on=["model_id", "content_type", "item_id"])
    bb["y"] = bb["correct"].astype(int)
    bb["cer"] = bb["cer"].astype(float)
    bb["cer_gt_002"] = (bb["cer"] > 0.02).astype(int)
    lr = []
    for ct, g in bb.groupby("content_type"):
        for pred, formula in (("cer", "y ~ cer + model_id"), ("cer_gt_002", "y ~ cer_gt_002 + model_id"),
                              ("cer_capped1", "y ~ cer_c + model_id")):
            g = g.assign(cer_c=g["cer"].clip(upper=1.0))
            try:
                fit = smf.logit(formula, data=g).fit(disp=0, maxiter=200)
                term = "cer_c" if pred == "cer_capped1" else pred
                b_, se = fit.params[term], fit.bse[term]
                lr.append(dict(content_type=ct, predictor=pred, n=len(g), n_models=g.model_id.nunique(), coef=b_, se=se,
                               odds_ratio=math.exp(b_), or_ci_lo=math.exp(b_ - 1.96 * se), or_ci_hi=math.exp(b_ + 1.96 * se),
                               z=fit.tvalues[term], p_value=fit.pvalues[term], pseudo_r2=fit.prsquared,
                               converged=bool(fit.mle_retvals.get("converged", True))))
            except Exception as e:
                lr.append(dict(content_type=ct, predictor=pred, n=len(g), error=repr(e)[:200]))
    write_csv(pd.DataFrame(lr), "rq2_logit_B_on_cer.csv")


# ------------------------------------------------------------------ T14
def rq3(df):
    w = paired(df, "output_tokens", A, B)
    rows = []
    for (mid, ct), g in w.groupby(["model_id", "content_type"]):
        dlt = g[A].astype(float) - g[B].astype(float)
        if (dlt == 0).all():
            stat, p = np.nan, 1.0
        else:
            res = stats.wilcoxon(g[A].astype(float), g[B].astype(float), zero_method="wilcox")
            stat, p = float(res.statistic), float(res.pvalue)
        rows.append(dict(model_id=mid, content_type=ct, n_pairs=len(g), median_A=g[A].median(), median_B=g[B].median(),
                         median_diff_A_minus_B=dlt.median(), mean_diff_A_minus_B=dlt.mean(),
                         wilcoxon_W=stat, p_value=p))
    r = pd.DataFrame(rows)
    r["p_holm"] = holm(r["p_value"])
    write_csv(r, "rq3_tokens_wilcoxon.csv")
    return r


def error_sample(df, n_per=100):
    from .score import load_items

    items = load_items()
    seed = load_config()["seed"]
    key = ["model_id", "content_type", "item_id"]
    a = df[df.condition == A].set_index(key)
    b = df[df.condition == B].set_index(key)
    c = df[df.condition == C].set_index(key)
    j = a[["correct", "response"]].join(b[["correct", "response"]], lsuffix="_A", rsuffix="_B", how="inner")
    j = j.join(c[["transcription"]], how="left")
    flips = j[j.correct_A & ~j.correct_B].reset_index()
    write_csv(flips.groupby(["content_type"]).size().rename("n_flips").reset_index(), "flip_counts.csv")
    out = []
    for ct in CONTENT_TYPES:
        f = flips[flips.content_type == ct].sort_values(key)
        s = f.sample(n=min(n_per, len(f)), random_state=seed)
        for _, r in s.iterrows():
            it = items[r.item_id]
            out.append(dict(sample_id=f"{ct}-{len(out):04d}", content_type=ct, model_id=r.model_id, item_id=r.item_id,
                            content=it["content"], gold=json.dumps(it["gold"], ensure_ascii=False) if ct == "table" else it["gold"],
                            response_A=r.response_A, response_B=r.response_B,
                            transcription_C=r.transcription if isinstance(r.transcription, str) else "",
                            code="", coder=""))
    e = pd.DataFrame(out)
    p = RESULTS / "coding" / "error_sample.csv"
    p.parent.mkdir(parents=True, exist_ok=True)
    e.to_csv(p, index=False)
    return flips.groupby("content_type").size(), e.groupby("content_type").size()


def main(args):
    what = getattr(args, "what", "all")
    if what in ("pilot",):
        from .pilot import pilot_report

        pilot_report("pilot")
        return 0
    if what == "replication":
        from .pilot import replication_check

        replication_check()
        return 0
    df = load_scored()
    if what in ("all", "t11", "desc"):
        descriptives(df)
    if what in ("all", "t12", "rq1"):
        rq1(df)
        if what != "all":
            figures_t11(df, read_csv("descriptives.csv"))  # refresh gap figure with paired CIs
    if what in ("all", "t13", "rq2"):
        rq2(df)
    if what in ("all", "t14", "rq3"):
        rq3(df)
        print(error_sample(df))
    if what == "all":
        figures_t11(df, read_csv("descriptives.csv"))
    if what in ("all", "summary"):
        from .summary import main as summ

        summ()
    return 0
