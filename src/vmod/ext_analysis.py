"""T18: extension models (exploratory) + combined figures + resolution table + paper_numbers index. Numbers only."""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import analyze as an
from .analyze import A, B, CONTENT_TYPES, MARKERS, PALETTE, holm, load_scored, read_csv, savefig, setup_mpl, write_csv
from .config import RESULTS

EXT1 = RESULTS / "scored" / "ext" / "run1_all.csv.gz"
SHORT = lambda m: m.split("/")[-1].replace("-Instruct", "").replace("-it", "")

FAMILY = {"Qwen/Qwen2.5-VL-3B-Instruct": "qwen2.5", "Qwen/Qwen2.5-VL-7B-Instruct": "qwen2.5",
          "Qwen/Qwen2.5-VL-32B-Instruct": "qwen2.5", "Qwen/Qwen2.5-VL-72B-Instruct-AWQ": "qwen2.5",
          "OpenGVLab/InternVL3-8B": "internvl", "OpenGVLab/InternVL3_5-8B": "internvl",
          "google/gemma-3-12b-it": "gemma3", "google/gemma-3-27b-it": "gemma3", "Qwen/Qwen3-VL-8B-Instruct": "qwen3"}
IMAGE_HANDLING = {"qwen2.5": "native resolution", "qwen3": "native resolution",
                  "internvl": "resized to 448-px tile grid (+thumbnail)", "gemma3": "resized to 896x896 (+pan-and-scan crops)"}


def ext_t11_t14(df):
    """Run the T11-T14 analyses on extension run 1 with every output file prefixed 'ext_' (own Holm families)."""
    orig = an.write_csv, an.savefig, an.read_csv
    an.write_csv = lambda d, name: orig[0](d, "ext_" + name)
    an.savefig = lambda fig, name: orig[1](fig, "ext_" + name)
    an.read_csv = lambda name: orig[2]("ext_" + name)
    try:
        an.descriptives(df)
        an.rq1(df)
        an.rq2(df)
        an.rq3(df)
        an.figures_t11(df, an.read_csv("descriptives.csv"))
    finally:
        an.write_csv, an.savefig, an.read_csv = orig


def gaps():
    """A-B gap (run 1) for every model: primary family + exploratory extension family."""
    p = read_csv("rq1_A_vs_B.csv").assign(group="primary")
    try:
        e = read_csv("ext_rq1_A_vs_B.csv").assign(group="extension (exploratory)")
        p = pd.concat([p, e], ignore_index=True)
    except FileNotFoundError:
        pass
    p["family"] = p.model_id.map(FAMILY)
    p["params_b"] = p.model_id.map(an.params_b)
    return p


def combined_figure(g):
    plt = setup_mpl()
    models = list(dict.fromkeys(g.sort_values(["group", "family", "params_b"], ascending=[False, True, True]).model_id))
    fig, axes = plt.subplots(1, 3, figsize=(11, 0.42 * len(models) + 1.2), sharey=True)
    y = np.arange(len(models))[::-1]
    for ax, ct in zip(axes, CONTENT_TYPES):
        for yi, m in zip(y, models):
            r = g[(g.model_id == m) & (g.content_type == ct)]
            if r.empty:
                continue
            r = r.iloc[0]
            prim = r.group == "primary"
            col = PALETTE[0] if prim else PALETTE[1]
            ax.errorbar(r["diff"], yi, xerr=[[r["diff"] - r.diff_ci_lo], [r.diff_ci_hi - r["diff"]]], fmt="o" if prim else "s",
                        color=col, mfc=col if prim else "white", mew=1.5, ms=6, capsize=2, elinewidth=1)
        ax.axvline(0, color="#52514e", lw=0.8)
        ax.set_title(ct)
        ax.set_xlabel("accuracy A − B (95% CI)")
    axes[0].set_yticks(y, [SHORT(m) for m in models])
    axes[-1].plot([], [], "o", color=PALETTE[0], label="primary")
    axes[-1].plot([], [], "s", color=PALETTE[1], mfc="white", mew=1.5, label="extension (exploratory)")
    axes[-1].legend(frameon=False, loc="center left", bbox_to_anchor=(1.0, 0.5))
    savefig(fig, "combined_gap_A_minus_B_all_models")
    plt.close(fig)


def size_figure(g):
    plt = setup_mpl()
    fams = [("qwen2.5", "Qwen2.5-VL"), ("gemma3", "Gemma 3")]
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.4), sharey=True)
    for ax, (fam, title) in zip(axes, fams):
        f = g[g.family == fam]
        sizes = sorted(f.params_b.unique())
        for j, ct in enumerate(CONTENT_TYPES):
            s = f[f.content_type == ct].sort_values("params_b")
            if s.empty:
                continue
            ax.errorbar(s.params_b * (1 + (j - 1) * 0.04), s["diff"], yerr=[s["diff"] - s.diff_ci_lo, s.diff_ci_hi - s["diff"]],
                        color=PALETTE[j], marker=MARKERS[j], ms=6, lw=2, capsize=2, elinewidth=1, label=ct)
            ext = s[s.group != "primary"]
            ax.scatter(ext.params_b * (1 + (j - 1) * 0.04), ext["diff"], s=70, facecolor="none", edgecolor="#0b0b0b", lw=0.8, zorder=5)
        ax.axhline(0, color="#52514e", lw=0.8)
        ax.set_xscale("log")
        ax.set_xticks(sizes, [f"{x:g}B" for x in sizes])
        ax.minorticks_off()
        ax.set_title(title)
        ax.set_xlabel("parameters (circled = extension model)")
    axes[0].set_ylabel("accuracy A − B (95% CI)")
    axes[-1].legend(frameon=False, loc="center left", bbox_to_anchor=(1.0, 0.5))
    savefig(fig, "gap_A_minus_B_vs_size_by_family")
    plt.close(fig)


def resolution_table(g):
    c = g[g.content_type == "code"].copy()
    c["image_handling"] = c.family.map(IMAGE_HANDLING)
    c["resizes_image"] = c.family.isin(["gemma3", "internvl"])
    # mean gap across runs if the replication tables exist
    for pre in ("replication_full", "ext_replication_full"):
        try:
            w = read_csv(f"{pre}_rq1_A_vs_B_agreement.csv")
            w = w[w.content_type == "code"].set_index("model_id")
            runs = [k for k in w.columns if k.startswith("diff_run")]
            c.loc[c.model_id.isin(w.index), "gap_mean_3runs"] = c.model_id.map(w[runs].mean(axis=1))
            c.loc[c.model_id.isin(w.index), "n_runs_sig"] = c.model_id.map(w["n_runs_sig"])
        except FileNotFoundError:
            pass
    cols = ["model_id", "group", "family", "params_b", "image_handling", "resizes_image", "acc_first", "acc_second",
            "diff", "diff_ci_lo", "diff_ci_hi", "p_holm", "gap_mean_3runs", "n_runs_sig"]
    t = c.reindex(columns=cols).rename(columns={"acc_first": "acc_A", "acc_second": "acc_B", "diff": "gap_A_minus_B_run1",
                                                "p_holm": "p_holm_own_family"})
    t = t.sort_values(["resizes_image", "family", "params_b"])
    write_csv(t, "resolution_check_code_gap.csv")
    summ = t.groupby("resizes_image").agg(n_models=("model_id", "size"), mean_gap_run1=("gap_A_minus_B_run1", "mean"),
                                          min_gap_run1=("gap_A_minus_B_run1", "min"), max_gap_run1=("gap_A_minus_B_run1", "max")).reset_index()
    summ["note"] = "descriptive only; family is confounded with image handling"
    write_csv(summ, "resolution_check_code_gap_summary.csv")
    return t


def main():
    if EXT1.exists():
        ext_t11_t14(load_scored(EXT1))
        from .replication import main as rep

        rep("ext")
    g = gaps()
    write_csv(g, "combined_gap_A_minus_B_all_models.csv")
    combined_figure(g)
    size_figure(g)
    resolution_table(g)
    return 0
