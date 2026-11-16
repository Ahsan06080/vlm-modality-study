"""T18: reports/paper_numbers.md -- compact index of every number/table the paper needs, each with its source CSV.
Numbers only, no prose."""
from __future__ import annotations

import pandas as pd

from .config import REPORTS, RESULTS
from .meta import provenance
from .summary import md

AN = RESULTS / "analysis"
SRC = lambda n: f"`results/analysis/{n}`"


def _r(name):
    p = AN / name
    return pd.read_csv(p, comment="#") if p.exists() else None


def _short(df):
    df = df.copy()
    df["model_id"] = df.model_id.str.split("/").str[-1].str.replace("-Instruct", "").str.replace("-it", "")
    return df


def rq1_block(name, title):
    r = _r(name)
    if r is None:
        return []
    r = _short(r)
    sig = r[r.p_holm < 0.05]
    t = r[["model_id", "content_type", "acc_first", "acc_second", "diff", "diff_ci_lo", "diff_ci_hi", "b_first_only",
           "c_second_only", "p_holm"]]
    return [f"### {title}", f"source: {SRC(name)}", "",
            f"- Holm p < .05: {len(sig)}/{len(r)} cells; first > second in {int((sig['diff'] > 0).sum())}, second > first in {int((sig['diff'] < 0).sum())}",
            "", md(t), ""]


def main(args=None):
    L = ["# Paper numbers index", "", "<!--", *(f"{k}: {v}" for k, v in provenance().items()), "-->", "",
         "Numbers and tables only. Each block names its source CSV. Full tables: `reports/summary.md`.", ""]

    # design / data
    L += ["## Design and data", ""]
    d = _r("descriptives.csv")
    if d is not None:
        L += [f"- primary models: {d.model_id.nunique()}; items per content type: {int(d.n.iloc[0])}; responses (run 1): {int(d.n.sum())} — source: {SRC('descriptives.csv')}"]
    il = _r("input_length.csv")
    if il is not None:
        L += ["", f"input length — source: {SRC('input_length.csv')}", "", md(il, ".1f"), ""]
    L += ["- exclusions and sampling: `data/items/summary.json`; deviations: `reports/deviations.md`", ""]

    # RQ1
    L += ["## RQ1 modality effect (primary: run 1, 5 models, Holm within family of 15)", ""]
    if d is not None:
        a = _short(d).pivot_table(index=["model_id", "content_type"], columns="condition", values="accuracy").reset_index()
        L += [f"### Accuracy per cell (95% Wilson CI in source)", f"source: {SRC('descriptives.csv')}", "", md(a), ""]
    L += rq1_block("rq1_A_vs_B.csv", "A (text) vs B (image), McNemar exact")
    L += rq1_block("rq1_A_vs_C.csv", "A (text) vs C (image + transcribe)")
    L += rq1_block("rq1_B_vs_C.csv", "B (image) vs C (image + transcribe)")
    for name, title in (("rq1_A_vs_B_sens_parseable.csv", "sensitivity: unparseable pairs excluded"),
                        ("rq1_A_vs_B_sens_strict_parser.csv", "sensitivity: strict same-line parser")):
        r = _r(name)
        if r is not None:
            L += [f"- A vs B {title}: Holm p < .05 in {int((r.p_holm < .05).sum())}/{len(r)} — source: {SRC(name)}"]
    cq = _r("rq1_cochran_q.csv")
    if cq is not None:
        L += [f"- Cochran's Q (A/B/C) Holm p < .05: {int((cq.p_holm < .05).sum())}/{len(cq)} — source: {SRC('rq1_cochran_q.csv')}", ""]

    # RQ2
    L += ["## RQ2 perception vs reasoning (condition C transcription)", ""]
    t = _r("rq2_transcription.csv")
    if t is not None:
        L += [f"### Transcription quality", f"source: {SRC('rq2_transcription.csv')}", "",
              md(_short(t)[["model_id", "content_type", "pct_with_transcription", "exact_rate", "exact_lenient_rate",
                            "pct_cer_le_002", "cer_median", "cer_mean"]]), "",
              "- table measures: CER ≤ 0.02 and lenient exact (primary exact ≈ 0 for tables; deviation #15)", ""]
    s = _r("rq2_A_vs_C_by_transcription.csv")
    if s is not None:
        s = _short(s)
        w = s.pivot_table(index=["model_id", "content_type", "subset_rule"], columns="transcription_correct",
                          values=["gap_A_minus_C", "n_pairs"], aggfunc="first")
        w.columns = [f"{a}_{'correct' if b else 'wrong'}" for a, b in w.columns]
        L += ["### A−C gap split by transcription correctness", f"source: {SRC('rq2_A_vs_C_by_transcription.csv')}", "",
              md(w.reset_index()), ""]
    lg = _r("rq2_logit_B_on_cer.csv")
    if lg is not None:
        L += ["### Logit correct(B) ~ CER(C) + model", f"source: {SRC('rq2_logit_B_on_cer.csv')}", "",
              md(lg[["content_type", "predictor", "n", "coef", "se", "odds_ratio", "or_ci_lo", "or_ci_hi", "p_value"]], ".4f"), ""]

    # RQ3
    r3 = _r("rq3_tokens_wilcoxon.csv")
    if r3 is not None:
        L += ["## RQ3 output length A vs B (Wilcoxon signed-rank, Holm)", f"source: {SRC('rq3_tokens_wilcoxon.csv')}", "",
              f"- Holm p < .05: {int((r3.p_holm < .05).sum())}/{len(r3)}", "",
              md(_short(r3)[["model_id", "content_type", "median_A", "median_B", "median_diff_A_minus_B", "p_holm"]], ".1f"), ""]
    fc = _r("flip_counts.csv")
    if fc is not None:
        L += [f"- A-correct/B-wrong flips available per content type — source: {SRC('flip_counts.csv')}; coded sample: `results/coding/error_sample.csv`", "",
              md(fc, ".0f"), ""]

    # replication
    for pre, title in (("replication_full", "primary models"), ("ext_replication_full", "extension models (exploratory)")):
        a = _r(f"{pre}_accuracy.csv")
        if a is None:
            continue
        L += [f"## Replication, runs 1-3, {title}", "",
              f"- cell accuracy SD across runs: max {a.sd.max():.4f}; range: max {a['range'].max():.3f} — source: {SRC(pre + '_accuracy.csv')}"]
        st = _r(f"{pre}_stability.csv")
        if st is not None:
            L += [f"- Fleiss' kappa per cell: min {st.fleiss_kappa.min():.3f}, median {st.fleiss_kappa.median():.3f}, max {st.fleiss_kappa.max():.3f}; "
                  f"% items mixed: min {st.pct_mixed.min():.1f}, median {st.pct_mixed.median():.1f}, max {st.pct_mixed.max():.1f} — source: {SRC(pre + '_stability.csv')}"]
        for tag in ("A_vs_B", "A_vs_C"):
            w = _r(f"{pre}_rq1_{tag}_agreement.csv")
            if w is None:
                continue
            nr = len([c for c in w.columns if c.startswith("sig_holm_run")])
            w = _short(w)
            L += [f"- {tag.replace('_', ' ')} significant in all {nr} runs: {int((w.n_runs_sig == nr).sum())}/{len(w)} "
                  f"({', '.join(w[w.n_runs_sig == nr].model_id + ' ' + w[w.n_runs_sig == nr].content_type)}); "
                  f"in some runs: {int(((w.n_runs_sig > 0) & (w.n_runs_sig < nr)).sum())}; direction agrees in all runs: "
                  f"{int(w.direction_agree_all_runs.sum())}/{len(w)} — source: {SRC(pre + '_rq1_' + tag + '_agreement.csv')}"]
            mv = _r(f"{pre}_rq1_{tag}_majority_vote.csv")
            if mv is not None:
                L += [f"- {tag.replace('_', ' ')} majority vote Holm p < .05: {int((mv.p_holm < .05).sum())}/{len(mv)} — source: {SRC(pre + '_rq1_' + tag + '_majority_vote.csv')}"]
        pm = _r(f"{pre}_rq1_A_vs_B_permutation_mean.csv")
        if pm is not None:
            L += [f"- A vs B permutation test on per-item mean correctness, Holm p < .05: {int((pm.p_holm < .05).sum())}/{len(pm)} — source: {SRC(pre + '_rq1_A_vs_B_permutation_mean.csv')}"]
        pc = _r(f"{pre}_rq2_pattern_check.csv")
        if pc is not None:
            g = pc.groupby(["content_type", "subset_rule"]).pattern_wrong_gt_correct.agg(["sum", "count"]).reset_index()
            g = g.rename(columns={"sum": "n_gap_wrong_gt_correct", "count": "n_model_runs"})
            L += ["", f"RQ2 pattern (A−C gap larger when transcription is wrong), per model × run — source: {SRC(pre + '_rq2_pattern_check.csv')}", "", md(g, ".0f")]
        w = _r(f"{pre}_rq1_A_vs_B_agreement.csv")
        if w is not None:
            cols = ["model_id", "content_type"] + [c for c in w.columns if c.startswith(("diff_run", "p_holm_run"))] + ["n_runs_sig"]
            L += ["", f"A vs B per run — source: {SRC(pre + '_rq1_A_vs_B_agreement.csv')}", "", md(_short(w)[cols])]
        L += [""]

    # extension
    if _r("ext_rq1_A_vs_B.csv") is not None:
        L += ["## Extension models, run 1 (exploratory; own Holm family)", ""]
        e = _r("ext_descriptives.csv")
        if e is not None:
            a = _short(e).pivot_table(index=["model_id", "content_type"], columns="condition", values="accuracy").reset_index()
            L += [f"source: {SRC('ext_descriptives.csv')}", "", md(a), ""]
        L += rq1_block("ext_rq1_A_vs_B.csv", "Extension A vs B")
        L += rq1_block("ext_rq1_A_vs_C.csv", "Extension A vs C")
        t = _r("ext_rq2_transcription.csv")
        if t is not None:
            L += [f"### Extension transcription quality", f"source: {SRC('ext_rq2_transcription.csv')}", "",
                  md(_short(t)[["model_id", "content_type", "pct_with_transcription", "exact_rate", "exact_lenient_rate", "pct_cer_le_002", "cer_median"]]), ""]
        r3 = _r("ext_rq3_tokens_wilcoxon.csv")
        if r3 is not None:
            L += [f"- extension RQ3 Wilcoxon Holm p < .05: {int((r3.p_holm < .05).sum())}/{len(r3)} — source: {SRC('ext_rq3_tokens_wilcoxon.csv')}", ""]
    for name, title in (("combined_gap_A_minus_B_all_models.csv", "A−B gap, all models (run 1)"),
                        ("resolution_check_code_gap.csv", "Resolution check: A−B code gap by image handling (descriptive; family confound)"),
                        ("resolution_check_code_gap_summary.csv", "Resolution check summary")):
        r = _r(name)
        if r is not None:
            if "model_id" in r:
                r = _short(r)
            if name.startswith("combined"):
                r = r[["model_id", "group", "content_type", "diff", "diff_ci_lo", "diff_ci_hi", "p_holm"]]
            L += [f"## {title}", f"source: {SRC(name)}", "", md(r), ""]

    rc = _r("sens_leading_fence_recovered.csv")
    if rc is not None:
        rc = _short(rc[rc.n_recovered_leading_fence > 0])
        L += ["## Sensitivity: leading code fence = transcription (approved after T18)", f"source: {SRC('sens_leading_fence_recovered.csv')}", "",
              md(rc[["set", "run", "model_id", "content_type", "pct_with_transcription_frozen", "pct_with_transcription_sens",
                     "n_recovered_leading_fence", "recovered_exact_rate", "recovered_pct_cer_le_002", "exact_rate_frozen", "exact_rate_sens"]]), ""]
        for pre in ("replication_full", "ext_replication_full"):
            pc = _r(f"{pre}_rq2_pattern_check_sens_leading_fence.csv")
            if pc is None:
                continue
            pc = _short(pc[pc.model_id.isin(["google/gemma-3-12b-it", "OpenGVLab/InternVL3_5-8B"]) & (pc.content_type == "code")])
            g = _r(f"{pre}_rq2_pattern_check_sens_leading_fence.csv").groupby(["content_type", "subset_rule"]).pattern_wrong_gt_correct.agg(["sum", "count"])
            L += [f"- {pre} RQ2 pattern under the rule, code: " + ", ".join(f"{r}: {int(g.loc[('code', r), 'sum'])}/{int(g.loc[('code', r), 'count'])}" for r in ("exact", "cer_le_0.02"))
                  + f" — source: {SRC(pre + '_rq2_pattern_check_sens_leading_fence.csv')}", "",
                  md(pc[["model_id", "subset_rule", "run", "gap_A_minus_C_correct", "gap_A_minus_C_wrong", "n_pairs_correct", "n_pairs_wrong"]]), ""]

    # OWNER Phase 4 plan files (2026-11-16)
    s = _r("replication_full_summary.csv")
    if s is not None:
        L += ["## Replication summary, OWNER plan rule (post hoc: replicates = Holm-sig same direction in >= 2/3 runs)",
              f"source: {SRC('replication_full_summary.csv')}", "",
              f"- replicates: {int(s.replicates.sum())}/{len(s)} cells", "",
              md(_short(s)[["model_id", "content_type", "n_sig_same_dir", "sig_direction", "replicates", "diff_run1", "diff_min",
                            "diff_max", "max_abs_diff_across_runs"]]), ""]
    ag = _r("replication_full_agreement.csv")
    if ag is not None:
        L += ["### Run-to-run agreement per model × condition", f"source: {SRC('replication_full_agreement.csv')}", "",
              f"- % identical response text: {ag.pct_identical_text.min():.1f}-{ag.pct_identical_text.max():.1f}; "
              f"% correctness agreement: {ag.pct_correct_agree.min():.1f}-{ag.pct_correct_agree.max():.1f}; "
              f"Cohen's kappa: {ag.cohen_kappa.min():.3f}-{ag.cohen_kappa.max():.3f}; |Δacc| max {ag.abs_delta_acc.max():.3f}", "",
              md(_short(ag)[["model_id", "condition", "pair", "pct_identical_text", "pct_correct_agree", "cohen_kappa", "abs_delta_acc"]]), ""]
    f6 = _r("ext_rq1_A_vs_B_family6.csv")
    if f6 is not None:
        L += ["### Extension A vs B, plan's Holm family of 6 (Gemma-27B, Qwen-72B-AWQ)", f"source: {SRC('ext_rq1_A_vs_B_family6.csv')}", "",
              md(_short(f6)[["model_id", "content_type", "acc_first", "acc_second", "diff", "diff_ci_lo", "diff_ci_hi", "p_holm_family12", "p_holm_family6"]]), ""]
    rb = _r("res_B_vs_B.csv")
    if rb is not None:
        L += ["## Resolution control (exploratory; condition B only)", f"source: {SRC('res_B_vs_B.csv')}", "",
              f"- Holm over {len(rb)} cells; p_holm < .05: {int((rb.p_holm < .05).sum())}", "",
              md(_short(rb)[["model_id", "content_type", "setting_first", "setting_second", "acc_B_original", "acc_B_rescontrol",
                             "diff_original_minus_rescontrol", "diff_ci_lo", "diff_ci_hi", "b_first_only", "c_second_only", "p_holm"]]), ""]
        gg = _r("res_gap_A_minus_B_by_setting.csv")
        if gg is not None:
            L += ["### A−B gap under each image setting (A = run-1 text)", f"source: {SRC('res_gap_A_minus_B_by_setting.csv')}", "",
                  md(_short(gg)[["model_id", "content_type", "B_setting", "acc_first", "acc_second", "gap_A_minus_B", "diff_ci_lo", "diff_ci_hi", "p_holm"]]), ""]

    L += ["## Figures", "", *[f"- `results/figures/{p.name}`" for p in sorted((RESULTS / "figures").glob("*.png"))], ""]
    (REPORTS / "paper_numbers.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("wrote reports/paper_numbers.md")
    return 0
