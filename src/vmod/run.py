"""T06-T08: vLLM offline batch inference, one model per process, all 3 conditions, resumable."""
from __future__ import annotations

import csv
import hashlib
import json
import os
import random
import time

from .config import CONDITIONS, CONTENT_TYPES, DATA, RESULTS, load_config, model_slug
from .meta import utc_now, write_meta_sidecar
from .prompts import build_prompt, sha256_text
from .render import image_path

# Per-model settings chosen so the processor does NOT downscale our images (largest is 1976x1216 = 2.09 MP).
MODEL_SETTINGS = {
    "qwen": dict(mm_processor_kwargs={"min_pixels": 28 * 28 * 4, "max_pixels": 28 * 28 * 16384},  # 12.8 MP cap
                 resolution_note="Qwen2.5-VL native resolution; smart_resize rounds each side to a multiple of 28 (<=14 px change), max_pixels 12.8 MP > largest image, so no downscaling"),
    "intern": dict(mm_processor_kwargs={}, hf_overrides={"max_dynamic_patch": 24}, trust_remote_code=True,
                   resolution_note="InternVL3 dynamic tiling, 448 px tiles, max_dynamic_patch=24 (+thumbnail); image is resized to the closest tile grid (can up- or downscale slightly)"),
    "gemma": dict(mm_processor_kwargs={"do_pan_and_scan": True},
                  resolution_note="Gemma 3 SigLIP encoder is fixed at 896x896: every image is resized to 896x896 (DOWNSCALES wide images); pan-and-scan adds 896x896 crops of the full-resolution image"),
}


def load_set(set_name: str, limit: int | None):
    items = []
    base = "pilot" if "pilot" in set_name else "main"  # main, main_run2, ext/run1 -> main items; pilot* / ext/pilot -> pilot
    for ct in CONTENT_TYPES:
        rows = [json.loads(l) for l in open(DATA / "items" / f"{base}_{ct}.jsonl", encoding="utf-8")]
        items += rows[:limit] if limit else rows
    return items


def image_shas():
    out = {}
    with open(DATA / "images_manifest.csv", encoding="utf-8") as f:
        for r in csv.DictReader(l for l in f if not l.startswith("#")):
            out[r["item_id"]] = r["sha256"]
    return out


def find_model(cfg, model_id):
    """Primary models from experiment.yaml, Phase 4 extension models from extension.yaml."""
    for m in cfg["models"]["local"]:
        if m["id"] == model_id:
            return m
    import yaml
    from .config import ROOT
    ext = yaml.safe_load(open(ROOT / "config" / "extension.yaml", encoding="utf-8"))
    return next(m for m in ext["extension_models"] if m["id"] == model_id)


def pinned_revision(model_id):
    """Phase 4: replicate runs must use the run-1 revision (from its meta sidecar) when one exists."""
    for set_dir in ("main", "ext/run1", "ext/pilot", "pilot"):
        p = RESULTS / "raw" / set_dir / f"{model_slug(model_id)}.jsonl.meta.json"
        if p.exists():
            return json.loads(p.read_text())["model_revision"]
    return None


def main(args):
    cfg = load_config()
    mcfg = find_model(cfg, args.model)
    dec = cfg["decoding"]
    settings = MODEL_SETTINGS[mcfg["family"]]
    tp = args.tp or (2 if mcfg["params_b"] > 20 else 1)
    set_name = args.out_dir or (args.set + args.out_suffix)
    out_dir = RESULTS / "raw" / set_name
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = model_slug(args.model)
    out_path, skip_path = out_dir / f"{slug}.jsonl", out_dir / f"{slug}.skipped.csv"

    done = set()
    if out_path.exists():
        for l in open(out_path, encoding="utf-8"):
            r = json.loads(l)
            done.add((r["item_id"], r["condition"]))
    if skip_path.exists():
        for r in csv.DictReader(open(skip_path, encoding="utf-8")):
            done.add((r["item_id"], r["condition"]))

    items = load_set(args.set, args.limit)
    shas = image_shas()
    reqs = [(it, c) for it in items for c in CONDITIONS if (it["item_id"], c) not in done]
    if getattr(args, "shuffle_seed", None) is not None:
        random.Random(args.shuffle_seed).shuffle(reqs)
    print(f"{args.model}: {len(reqs)} requests to run ({len(done)} already done)", flush=True)
    if not reqs:
        return 0

    # FlashInfer's sampler JIT-compiles with nvcc (not installed); decoding is greedy so the PyTorch sampler is equivalent.
    os.environ.setdefault("VLLM_USE_FLASHINFER_SAMPLER", "0")
    from huggingface_hub import HfApi
    from PIL import Image
    from vllm import LLM, SamplingParams

    revision = (None if args.out_dir is None and args.run == 1 else pinned_revision(args.model)) or HfApi().model_info(args.model).sha
    max_len = 16384
    llm = LLM(model=args.model, revision=revision, tensor_parallel_size=tp, max_model_len=max_len,
              limit_mm_per_prompt={"image": 1, "video": 0}, mm_processor_kwargs=settings["mm_processor_kwargs"],
              hf_overrides=settings.get("hf_overrides"),
              trust_remote_code=settings.get("trust_remote_code", False), seed=cfg["seed"],
              gpu_memory_utilization=args.gpu_mem, max_num_seqs=128, **settings.get("llm_kwargs", {}))
    sp = SamplingParams(temperature=dec["temperature"], top_p=dec["top_p"], max_tokens=dec["max_new_tokens"],
                        n=dec["n"], seed=cfg["seed"])
    write_meta_sidecar(out_path, model_id=args.model, model_revision=revision, tensor_parallel_size=tp,
                       max_model_len=max_len, mm_processor_kwargs=settings["mm_processor_kwargs"],
                       hf_overrides=settings.get("hf_overrides"), resolution_note=settings["resolution_note"], decoding=dec, run=args.run, order_seed=args.shuffle_seed,
                       gpu_memory_utilization=args.gpu_mem,
                       vllm_version=__import__("vllm").__version__, chat_template="model default (llm.chat), no system message")

    def messages(it, cond):
        text = build_prompt(it["content_type"], cond, it["content"])
        if cond == "A_text":
            content = [{"type": "text", "text": text}]
        else:
            img = Image.open(image_path(it["item_id"])).convert("RGB")
            content = [{"type": "image_pil", "image_pil": img}, {"type": "text", "text": text}]
        return [{"role": "user", "content": content}], text

    def row(it, cond, text, o, started, secs):
        c = o.outputs[0]
        return dict(item_id=it["item_id"], content_type=it["content_type"], condition=cond, model_id=args.model,
                    model_revision=revision, prompt_sha256=sha256_text(text),
                    image_sha256=None if cond == "A_text" else shas[it["item_id"]], response=c.text,
                    input_tokens=len(o.prompt_token_ids), output_tokens=len(c.token_ids), finish_reason=c.finish_reason,
                    started_utc=started, gen_seconds=round(secs, 4), run=args.run)

    chunk = args.chunk
    skipf_new = not skip_path.exists()
    t_all = time.time()
    with open(out_path, "a", encoding="utf-8") as fout, open(skip_path, "a", newline="", encoding="utf-8") as fskip:
        sk = csv.writer(fskip, lineterminator="\n")
        if skipf_new:
            sk.writerow(["item_id", "condition", "reason"])
        for s in range(0, len(reqs), chunk):
            batch = reqs[s:s + chunk]
            built = [messages(it, c) for it, c in batch]
            started, t0 = utc_now(), time.time()
            try:
                outs = llm.chat([m for m, _ in built], sp, use_tqdm=False)
                pairs = list(zip(batch, built, outs))
                per = (time.time() - t0) / len(batch)
                results = [(b, bt, o, per) for b, bt, o in pairs]
            except Exception as e:  # fall back to one-by-one to isolate over-context / bad requests
                print("batch failed, retrying one by one:", repr(e)[:300], flush=True)
                results = []
                for b, bt in zip(batch, built):
                    t1 = time.time()
                    try:
                        o = llm.chat([bt[0]], sp, use_tqdm=False)[0]
                        results.append((b, bt, o, time.time() - t1))
                    except Exception as e1:
                        msg = repr(e1)
                        reason = "over_context" if ("longer than" in msg or "max_model_len" in msg or "context" in msg) else "error"
                        sk.writerow([b[0]["item_id"], b[1], f"{reason}: {msg[:200]}"])
                        fskip.flush()
            for (it, cond), (_, text), o, secs in results:
                fout.write(json.dumps(row(it, cond, text, o, started, secs), ensure_ascii=False) + "\n")
            fout.flush()
            print(f"  {min(s + chunk, len(reqs))}/{len(reqs)} done, {time.time() - t_all:.0f}s elapsed", flush=True)
    print(f"finished {args.model} {set_name}: {time.time() - t_all:.0f}s", flush=True)
    return 0
