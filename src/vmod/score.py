"""T10: score raw outputs -> results/scored/{set}_all.csv.gz."""
from __future__ import annotations

import gzip
import json

import pandas as pd

from .config import DATA, RESULTS
from .meta import provenance
from .scoring import (extract_transcription_src, strip_fence, parse_answer, parse_answer_strict, score_code_batch, score_math, score_table,
                      transcription_metrics)


def load_items():
    items = {}
    for p in (DATA / "items").glob("*.jsonl"):
        for l in open(p, encoding="utf-8"):
            d = json.loads(l)
            items[d["item_id"]] = d
    return items


def read_raw(set_name: str) -> pd.DataFrame:
    rows = []
    d = RESULTS / "raw" / set_name
    for p in sorted(d.glob("*.jsonl")) + sorted(d.glob("*.jsonl.gz")):
        if p.suffix == ".gz" and p.with_suffix("").exists():
            continue  # prefer the uncompressed file
        op = gzip.open if p.suffix == ".gz" else open
        with op(p, "rt", encoding="utf-8") as f:
            rows += [json.loads(l) for l in f]
    return pd.DataFrame(rows)


def score_df(df: pd.DataFrame) -> pd.DataFrame:
    items = load_items()
    parsed = [parse_answer(r, ct) for r, ct in zip(df["response"], df["content_type"])]
    df = df.copy()
    preds = [p for p, _ in parsed]
    df["pred"] = preds
    df["parse_ok"] = [ok for _, ok in parsed]
    df["parse_ok_strict"] = [parse_answer_strict(r, ct)[1] for r, ct in zip(df["response"], df["content_type"])]
    correct = [False] * len(df)
    code_idx = []
    for i, (iid, ct, pred) in enumerate(zip(df["item_id"], df["content_type"], preds)):
        it = items[iid]
        if ct == "math":
            correct[i] = score_math(pred, it["gold"])
        elif ct == "table":
            correct[i] = score_table(pred, it["gold"], it["gold_canon"])
        else:
            code_idx.append(i)
    res = score_code_batch([(preds[i], items[df["item_id"].iat[i]]["gold"]) for i in code_idx])
    for i, r in zip(code_idx, res):
        correct[i] = r
    df["correct"] = correct
    df["correct_strict"] = df["correct"] & df["parse_ok_strict"]  # strict parse => identical pred
    tr, ex, cer, cer_raw, src, exl = [], [], [], [], [], []
    for resp, cond, iid in zip(df["response"], df["condition"], df["item_id"]):
        if cond != "C_image_transcribe":
            tr.append(None); ex.append(None); cer.append(None); cer_raw.append(None); src.append(None); exl.append(None)
            continue
        t, sc = extract_transcription_src(resp)
        t = strip_fence(t)
        src.append(sc)
        m = transcription_metrics(t, items[iid]["content"])
        exl.append(m["transcription_exact_lenient"])
        tr.append(t); ex.append(m["transcription_exact"]); cer.append(m["cer"]); cer_raw.append(m["cer_raw"])
    df["transcription"], df["transcription_exact"], df["cer"], df["cer_raw"] = tr, ex, cer, cer_raw
    df["transcription_source"] = src
    df["transcription_exact_lenient"] = exl
    return df


def main(args):
    set_name = args.set
    df = read_raw(set_name)
    if df.empty:
        print("no raw results for", set_name)
        return 1
    df = score_df(df)
    out = RESULTS / "scored" / f"{set_name}_all.csv.gz"
    out.parent.mkdir(parents=True, exist_ok=True)
    prov = provenance()
    for k, v in prov.items():
        df[k] = v
    df.to_csv(out, index=False, compression="gzip")
    print(f"wrote {out} ({len(df)} rows)")
    print(df.groupby(["model_id", "condition"])["parse_ok"].mean().unstack().round(3).to_string())
    print(df.groupby(["model_id", "content_type", "condition"])["correct"].mean().unstack().round(3).to_string())
    return 0
