"""T14: reports/summary.md -- numbers and tables only (no prose)."""
from __future__ import annotations

import json
import re
import subprocess
from importlib import metadata

import pandas as pd

from .config import DATA, REPORTS, RESULTS, ROOT, load_config
from .meta import provenance

AN = RESULTS / "analysis"


def t(name):
    return pd.read_csv(AN / name, comment="#")


def md(df: pd.DataFrame, floatfmt=".3f") -> str:
    def f(x):
        if isinstance(x, float):
            if x != x:
                return ""
            if abs(x) < 1e-3 and x != 0:
                return f"{x:.2e}"
            return format(x, floatfmt)
        return str(x)

    cols = list(df.columns)
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(f(r[c]) for c in cols) + " |")
    return "\n".join(out)


def short(m):
    return m.split("/")[-1]


def gpu_hours():
    rows = []
    starts = {}
    log = ROOT / "logs" / "lanes.log"
    if not log.exists():
        return pd.DataFrame()
    for line in open(log):
        m = re.match(r"\[(\S+)\] (START|END) (\S+) (\S+)", line)
        if not m:
            continue
        ts, kind, model, s = m.groups()
        ts = pd.Timestamp(ts)
        if kind == "START":
            starts[(model, s)] = ts
        elif (model, s) in starts or s.endswith("_rep2"):
            base = s.replace("_rep2", "")
            st = starts.get((model, s)) or starts.get((model, base))
            from .run import find_model

            try:
                tp = 2 if find_model(load_config(), model)["params_b"] > 20 else 1
            except StopIteration:
                tp = 1
            rows.append(dict(model=short(model), set=s, wall_h=(ts - st).total_seconds() / 3600, gpus=tp))
            starts[(model, s.replace("_rep2", "") + "_rep2")] = ts  # rep2 starts when the first pass ends
    d = pd.DataFrame(rows)
    if len(d):
        d["gpu_h"] = d.wall_h * d.gpus
    return d


def main(args=None):
    cfg = load_config()
    L = ["# Numeric summary", "", "<!--", *(f"{k}: {v}" for k, v in provenance().items()), "-->", "",
         "Numbers, tables and figures only. Figures: `results/figures/`. All CSVs: `results/analysis/`.", ""]

    # models
    L += ["## Final model list", ""]
    meta = []
    for m in cfg["models"]["local"]:
        p = RESULTS / "raw" / "main" / f"{m['id'].replace('/', '__')}.jsonl.meta.json"
        if p.exists():
            j = json.loads(p.read_text())
            meta.append(dict(model=m["id"], params_b=m["params_b"], revision=j["model_revision"], tp=j["tensor_parallel_size"],
                             vllm=j["vllm_version"], image_processing=j["resolution_note"]))
    L += [md(pd.DataFrame(meta)), ""]

    # exclusions
    s = json.loads((DATA / "items" / "summary.json").read_text())
    ex = pd.DataFrame([dict(content=k, total=v["total"], excluded=v["excluded"], eligible=v["eligible"],
                            **{f"reason_{r}": v["reasons"].get(r, 0) for r in ("max_line_chars", "max_lines", "table_max_rows", "render_fails")},
                            pilot=v["pilot"], main=v["main"]) for k, v in s.items()])
    L += ["## Exclusions (before sampling; reasons not mutually exclusive)", "", md(ex), ""]
    L += ["## Input length (main items)", "", md(t("input_length.csv"), ".1f"), ""]

    # replication
    if (AN / "replication_check.csv").exists():
        r = t("replication_check.csv")
        r["model_id"] = r.model_id.map(short)
        L += ["## T07b replication check (pilot, 2 runs)", "", md(r), "",
              f"- cells with correct-agreement < 95%: {int((r.pct_correct_agree < 95).sum())} of {len(r)} (pre-registered threshold 95%)", ""]

    # descriptives
    d = t("descriptives.csv")
    d["model_id"] = d.model_id.map(short)
    L += ["## T11 accuracy per model × content × condition (95% Wilson CI)", "",
          md(d[["model_id", "content_type", "condition", "n", "accuracy", "ci95_lo", "ci95_hi", "parse_rate",
                "parse_rate_strict", "accuracy_strict", "pct_finish_length"]]), ""]
    L += ["## T11 output tokens per cell", "",
          md(d[["model_id", "content_type", "condition", "out_tok_mean", "out_tok_median", "out_tok_sd", "out_tok_iqr",
                "out_tok_min", "out_tok_max"]], ".1f"), ""]
    oc = t("outlier_counts.csv")
    L += ["## T11 outliers (kept, not dropped)", "",
          f"- output tokens > Q3 + 3·IQR (within cell): {int(oc.n_outlier_tokens.sum())} responses",
          f"- finish_reason = length: {int(oc.n_finish_length.sum())} responses", ""]
    oc["model_id"] = oc.model_id.map(short)
    L += [md(oc[(oc.n_outlier_tokens > 0) | (oc.n_finish_length > 0)], ".0f"), ""]

    # RQ1
    cols = ["model_id", "content_type", "n_pairs", "acc_first", "acc_second", "b_first_only", "c_second_only", "diff",
            "diff_ci_lo", "diff_ci_hi", "discordant_or", "or_ci_lo", "or_ci_hi", "p_mcnemar_exact", "p_holm"]
    for fam in ("A_vs_B", "A_vs_C", "B_vs_C"):
        for suffix, title in (("", "primary"), ("_sens_parseable", "sensitivity: unparseable pairs excluded"),
                              ("_sens_strict_parser", "sensitivity: strict same-line parser")):
            r = t(f"rq1_{fam}{suffix}.csv")
            r["model_id"] = r.model_id.map(short)
            L += [f"## T12 RQ1 McNemar {fam.replace('_', ' ')} ({title}; Holm within family)", "", md(r[cols]), ""]
    cq = t("rq1_cochran_q.csv")
    cq["model_id"] = cq.model_id.map(short)
    L += ["## T12 Cochran's Q across A/B/C (Holm)", "", md(cq), ""]

    # RQ2
    r = t("rq2_transcription.csv")
    r["model_id"] = r.model_id.map(short)
    L += ["## T13 RQ2 transcription (condition C)", "", md(r), ""]
    r = t("rq2_A_vs_C_by_transcription.csv")
    r["model_id"] = r.model_id.map(short)
    L += ["## T13 RQ2 A vs C split by transcription correctness", "",
          md(r[["model_id", "content_type", "subset_rule", "transcription_correct", "n_pairs", "acc_first", "acc_second",
                "gap_A_minus_C", "diff_ci_lo", "diff_ci_hi", "b_first_only", "c_second_only", "p_mcnemar_exact",
                "p_holm_within_rule"]]), ""]
    L += ["## T13 RQ2 logistic regression: correct(B) ~ CER(C) + model", "", md(t("rq2_logit_B_on_cer.csv"), ".4f"), ""]

    # RQ3
    r = t("rq3_tokens_wilcoxon.csv")
    r["model_id"] = r.model_id.map(short)
    L += ["## T14 RQ3 output tokens A vs B (Wilcoxon signed-rank, Holm)", "", md(r, ".1f"), ""]
    if (RESULTS / "coding" / "error_sample.csv").exists():
        e = pd.read_csv(RESULTS / "coding" / "error_sample.csv")
        L += ["## T14 error sample", "", f"- file: `results/coding/error_sample.csv`, {len(e)} rows",
              md(e.groupby("content_type").size().rename("n").reset_index(), ".0f"), ""]
        fl = AN / "flip_counts.csv"
        if fl.exists():
            L += ["- available A-correct/B-wrong flips per content type:", "", md(t("flip_counts.csv"), ".0f"), ""]

    # hand check, GPU hours, versions, deviations
    hc = AN / "handcheck_t10.csv"
    if hc.exists():
        h = t("handcheck_t10.csv")
        L += ["## T10 scorer hand-check", "", f"- rows checked: {len(h)}; scorer agrees: {int(h.agree.sum())}; disagreements: {int((~h.agree.astype(bool)).sum())}", ""]
    g = gpu_hours()
    if len(g):
        L += ["## GPU hours (wall time × GPUs, from logs/lanes.log)", "", md(g, ".3f"), "",
              f"- total GPU hours: {g.gpu_h.sum():.2f}", ""]
    pk = ["vllm", "torch", "transformers", "datasets", "pillow", "pandas", "numpy", "scipy", "statsmodels", "matplotlib", "rapidfuzz"]
    L += ["## Package versions", "", md(pd.DataFrame([dict(package=p, version=metadata.version(p)) for p in pk])), "",
          "Full lock file: `env/requirements.lock.txt`.", ""]
    L += phase4_section()
    dev = REPORTS / "deviations.md"
    if dev.exists():
        L += [dev.read_text()]
    (REPORTS / "summary.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("wrote reports/summary.md")


# ---------------------------------------------------------------- Phase 4 (T15-T18)
def _opt(name):
    return t(name) if (AN / name).exists() else None


def _sh(df):
    if df is not None and "model_id" in df:
        df = df.copy()
        df["model_id"] = df.model_id.map(short)
    return df


def phase4_section():
    L = []
    if not (AN / "replication_full_accuracy.csv").exists():
        return L
    L += ["# Phase 4 (added 2026-11-15): replication runs and extension models", "",
          "Run 1 of the 5 primary models remains the primary analysis. Extension models are exploratory (own Holm families).", ""]
    for pre, title in (("replication_full", "primary models"), ("ext_replication_full", "extension models (exploratory)")):
        a = _sh(_opt(f"{pre}_accuracy.csv"))
        if a is None:
            continue
        L += [f"## T16/T18 accuracy across runs, {title}", "", md(a), ""]
        st = _sh(_opt(f"{pre}_stability.csv"))
        if st is not None:
            L += [f"## Item-level stability across 3 runs, {title}", "", md(st), ""]
        for tag in ("A_vs_B", "A_vs_C"):
            w = _sh(_opt(f"{pre}_rq1_{tag}_agreement.csv"))
            if w is None:
                continue
            runs = sorted(int(c[-1]) for c in w.columns if c.startswith("sig_holm_run"))
            cols = ["model_id", "content_type"] + [f"{k}_run{r}" for r in runs for k in ("diff", "p_holm", "sig_holm")] + \
                   ["n_runs_sig", "sig_agree_all_runs", "direction_agree_all_runs"]
            L += [f"## RQ1 {tag.replace('_', ' ')} per run (Holm within each run), {title}", "", md(w[cols]), "",
                  f"- cells significant in all runs: {int((w.n_runs_sig == len(runs)).sum())}; in some but not all: "
                  f"{int(((w.n_runs_sig > 0) & (w.n_runs_sig < len(runs))).sum())}; in none: {int((w.n_runs_sig == 0).sum())} (of {len(w)})", ""]
            mv = _sh(_opt(f"{pre}_rq1_{tag}_majority_vote.csv"))
            if mv is not None:
                L += [f"## RQ1 {tag.replace('_', ' ')} on majority vote (correct in >= 2 of 3 runs), {title}", "",
                      md(mv[["model_id", "content_type", "n_pairs", "acc_first", "acc_second", "b_first_only", "c_second_only",
                             "diff", "diff_ci_lo", "diff_ci_hi", "p_mcnemar_exact", "p_holm"]]), ""]
        pm = _sh(_opt(f"{pre}_rq1_A_vs_B_permutation_mean.csv"))
        if pm is not None:
            L += [f"## RQ1 A vs B paired permutation test on per-item mean correctness (10,000 perms, seed 630), {title}", "", md(pm), ""]
        pc = _sh(_opt(f"{pre}_rq2_pattern_check.csv"))
        if pc is not None:
            L += [f"## RQ2 A−C gap, wrong vs correct transcription, per run, {title}", "", md(pc), ""]
    for name, title in (("ext_descriptives.csv", "T18 extension run 1: accuracy (95% Wilson CI)"),):
        d = _sh(_opt(name))
        if d is not None:
            L += [f"## {title}", "", md(d[["model_id", "content_type", "condition", "n", "accuracy", "ci95_lo", "ci95_hi",
                                         "parse_rate", "parse_rate_strict", "pct_finish_length"]]), ""]
    for fam in ("A_vs_B", "A_vs_C", "B_vs_C"):
        r = _sh(_opt(f"ext_rq1_{fam}.csv"))
        if r is not None:
            L += [f"## T18 extension RQ1 McNemar {fam.replace('_', ' ')} (exploratory; Holm within the extension family)", "",
                  md(r[["model_id", "content_type", "n_pairs", "acc_first", "acc_second", "b_first_only", "c_second_only", "diff",
                        "diff_ci_lo", "diff_ci_hi", "p_mcnemar_exact", "p_holm"]]), ""]
    for name, title, ff in (("ext_rq2_transcription.csv", "T18 extension RQ2 transcription (condition C)", ".3f"),
                            ("ext_rq2_A_vs_C_by_transcription.csv", "T18 extension RQ2 A vs C split by transcription correctness", ".3f"),
                            ("ext_rq3_tokens_wilcoxon.csv", "T18 extension RQ3 output tokens A vs B (Wilcoxon, Holm)", ".1f"),
                            ("combined_gap_A_minus_B_all_models.csv", "T18 A−B gap, all models (run 1)", ".3f"),
                            ("resolution_check_code_gap.csv", "T18 resolution check: A−B code gap by image handling (descriptive; family is a confound)", ".3f"),
                            ("resolution_check_code_gap_summary.csv", "T18 resolution check summary", ".3f")):
        d = _sh(_opt(name))
        if d is not None:
            if name == "combined_gap_A_minus_B_all_models.csv":
                d = d[["model_id", "group", "content_type", "acc_first", "acc_second", "diff", "diff_ci_lo", "diff_ci_hi", "p_holm"]]
            L += [f"## {title}", "", md(d, ff), ""]
    ext = ROOT / "logs" / "ext_gate.log"
    if ext.exists():
        L += ["## T17 extension pilot gate (G2 rule 1: parse >= 80% in every condition)", "", "```", ext.read_text().strip(), "```", ""]
    return L
