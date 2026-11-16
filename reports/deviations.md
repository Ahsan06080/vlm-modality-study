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
| 21 | Resolution control (OWNER plan, 2026-11-16) | not in TASKS.md | condition B only, 1,500 items, run-1 revisions, frozen prompts/decoding, gpu_memory_utilization 0.80, order seed 630: Qwen2.5-VL-7B and -32B with every image stretched to 896x896 (results/raw/res896); gemma-3-12b with do_pan_and_scan=false (results/raw/res_gemma_nopas) | added after the Phase 4 results; exploratory. Runner gained --conditions, --image-variant, --mm-override (commit 58cd9fd) |
| 22 | Resolution control resampling | OWNER plan: PIL BICUBIC | PIL BILINEAR, resized in memory (no files written) | the plan's stated aim is "the same way Gemma's processor does it"; Gemma3ImageProcessor uses resample=2 (BILINEAR). image_sha256 for these rows = sha256 of the resized RGB pixel bytes |
| 23 | Replication criterion "replicates = significant, same direction, in >= 2 of 3 runs" | not in TASKS.md T16 | reported in replication_full_summary.csv | the OWNER plan that defines it was written after runs 2-3 finished, so it is post hoc, not pre-registered; the T16 tables (n_runs_sig, majority vote, permutation) are unchanged. The plan's pre-flight steps (phase4-start tag, pre-registration commit) could not be done before runs that had already happened and were not back-filled |

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
| Phase 4: InternVL3.5-8B condition C, no transcription found (code / math / table) | 99.4% / 94.4% / 81.2% (it writes the copy as a leading code fence without tags or a "Transcription" heading; the frozen extractor finds nothing) -> its RQ2 numbers are not interpretable under the frozen extractor; see the approved leading-fence sensitivity (row below) | ext_rq2_transcription.csv |
| Sensitivity (approved after T18): 'leading code fence = transcription' fallback, applied only where the frozen extractor finds nothing. Condition-C responses recovered per run: InternVL3.5 code 466-469; gemma-3-12b code 312-323, table 35-41; no other model/cell. Primary scored files and primary CSVs unchanged | code % with transcription: InternVL3.5 0.6 -> 93.8, gemma-12b 20.0 -> 82.4 (run 1) | sens_leading_fence_recovered.csv, *_sens_leading_fence.csv |
| Phase 4: Qwen3-VL-8B finish_reason=length, code A | 9.0% (highest extension cell) | ext_descriptives.csv |
| Phase 4: extension responses with finish_reason=length (run 1) | 183 of 18,000 | ext_outlier_counts.csv |
| Phase 4: extension responses with output tokens > Q3 + 3·IQR (run 1) | 456 of 18,000 | ext_outlier_counts.csv |
| Phase 4: Qwen2.5-VL-32B wall time per run | 54 min vs 35 min in run 1 (gpu_memory_utilization 0.80, GPUs shared with another user's jobs) | logs/lanes.log |
