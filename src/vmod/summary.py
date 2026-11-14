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
            tp = 2 if "32B" in model else 1
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
    dev = REPORTS / "deviations.md"
    if dev.exists():
        L += [dev.read_text()]
    (REPORTS / "summary.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("wrote reports/summary.md")
