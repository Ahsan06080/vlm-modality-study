## Deviations from the plan

| # | where | planned | actual | reason |
|---|---|---|---|---|
| 1 | T02 WTQ source | HF `stanfordnlp/wikitablequestions` | GitHub release v1.0.2 zip (the config's stated fallback) | HF loader is script-based; current `datasets` refuses scripts |
| 2 | T03 render_fails | not specified | missing DejaVu Sans Mono glyph or control char (TAB) counts as render failure | 3 code + 43 table items excluded |
| 3 | T05 table scorer | official WTQ denotation match | py3 port of official evaluator + CoreNLP `targetCanon` (field `gold_canon`) | evaluator is Python 2 |
| 4 | T05 code sandbox | subprocess, 5 s, no network | subprocess, 5 s alarm, empty builtins, sockets disabled, 2 GB RLIMIT_AS | unprivileged network namespaces not permitted on the server |
| 5 | T05 CER | normalized char Levenshtein vs content | computed on whitespace-collapsed strings (`cer`); raw-string version kept as `cer_raw`; missing transcription = empty (cer 1) | consistent with `transcription_exact`; table padding would otherwise dominate |
| 6 | T06 parser | LAST line containing `Final answer:` | if that line has nothing after the marker (or is a bare `Final Answer` heading), the next non-empty block is the answer; strict version kept as `parse_ok_strict`/`correct_strict` and reported as sensitivity | Qwen-32B writes `### Final Answer:` + answer on next line (strict parse 0.63-0.73) |
| 7 | T06 transcription | text between `<transcription>` tags | fallback: first code fence after a "Transcription" heading; `transcription_source` column; tags-only sensitivity in RQ2 | Gemma (code) and Qwen-32B (code, some tables) ignore the tags |
| 8 | T06 image resolution | no downscaling | Qwen: native (no downscaling). InternVL3: 448-px tile grid chosen by aspect ratio, max_dynamic_patch 24 (some up-, some downscaling). Gemma 3: fixed 896×896 (downscales) + pan-and-scan crops | model-intrinsic preprocessing |
| 9 | T06 sampler | - | `VLLM_USE_FLASHINFER_SAMPLER=0` (PyTorch sampler) | FlashInfer JIT needs nvcc, not installed; greedy decoding so equivalent |
| 10 | GPUs | 4 available | at most 2 GPUs (0,1) | OWNER instruction |
| 11 | T07b | - | 5/15 model × condition cells < 95% correct-agreement between two runs; largest cell acc diff 0.100 (n=30) | vLLM greedy decoding is not batch-invariant; one run per item kept per pre-registered rule (conclusion-validity threat) |
| 12 | G2 | max_new_tokens 2048 | 4096 for all models (rule 3) | pilot cells > 5% finish_reason=length |
| 13 | T09 | API models optional | SKIPPED | no OWNER approval (fast-track default) |
| 14 | T05/T13 transcription | text between tags, exact after whitespace collapse | a markdown code fence wrapping the WHOLE transcription is removed before comparison | Qwen-7B wraps 87% of code transcriptions in ```python fences inside the tags |
| 15 | T13 sensitivity | exact, CER ≤ 0.02 | added `transcription_exact_lenient` (spaces around `|` ignored, dash runs collapsed) as an extra subset rule; primary unchanged | table header-rule dash counts encode column padding, so primary exact match is ~0% for tables |
| 16 | Phase 4 vLLM memory | gpu_memory_utilization 0.90 (run 1) | 0.80 for all Phase 4 runs | another user's jobs hold 3-6 GB on GPU 0/1; only the KV-cache size changes, decoding settings are identical |
| 17 | Phase 4 extension models | not in the pre-registered design | gemma-3-27b, Qwen3-VL-8B, InternVL3.5-8B, Qwen2.5-VL-72B-AWQ added AFTER the primary results were seen; analyzed as a separate exploratory family (own Holm correction) | PLANNER Phase 4 task (instructor asked about replication / scale) |
| 18 | Phase 4 72B | full-precision weights | Qwen2.5-VL-72B-Instruct-AWQ (4-bit AWQ) | must fit 2 GPUs (OWNER limit); quantization is a caveat for the scale comparison |
| 19 | Phase 4 Llama-3.2-11B-Vision | optional extension model | skipped | gated repo: stored HF token has no access; also no Mllama support in vLLM 0.33 |
| 20 | Phase 4 Qwen3-VL image size | model default (min 65,536 px) | shortest_edge 4096 px, longest_edge 16.8 MP | default would upscale 11 small images; lowered so no image is rescaled beyond 32-px rounding (same principle as Qwen2.5) |

## Data-quality flags (counts)

| flag | value | source |
|---|---|---|
| T07b cells with correct-agreement < 95% (conclusion-validity threat) | 5 of 15 (min 88.9%, Qwen-3B C) | results/analysis/replication_check.csv |
| Gemma-3-12B condition C, code: responses with no transcription at all | 80.0% (tags 13.2%, heading fallback 6.8%) | rq2_transcription.csv |
| Gemma-3-12B condition C, math / table: no transcription | 22.4% / 17.8% | rq2_transcription.csv |
| Qwen-32B condition C transcriptions from heading fallback (not tags): code / table | 99.6% / 38.0% | rq2_transcription.csv |
| Tables: primary transcription exact-match rate, all models | 0.000-0.004 (lenient rule 0.112-0.398) | rq2_transcription.csv |
| Qwen-7B table CER mean vs median (long repetition outputs) | 0.961 vs 0.037 | rq2_transcription.csv |
| Responses with finish_reason=length (main, all models) | 138 of 22,500 | outlier_counts.csv |
| Responses with output tokens > Q3 + 3·IQR (within cell) | 383 of 22,500 | outlier_counts.csv |
| Scorer hand-check disagreements (T10) | 1 of 30 | handcheck_t10.csv |
| GLMM (T12) | not run: no `GLMM OK` from OWNER | - |
