# COLLAB: message board between the planner, the lab server and the owner

## Roles
- **OWNER:** Ahsan. Makes all decisions, writes the paper, codes the error sample, and holds the API keys.
- **PLANNER:** Claude on the owner's laptop. Designs tasks, reviews reports, and approves gates when the owner agrees.
- **RUNNER:** Claude on the lab server. Implements and runs the tasks in TASKS.md, in order.

## Loop for the RUNNER
1. `git pull --rebase`. Read the newest messages here, then TASKS.md.
2. Take the first `TODO` task. Set it to `IN-PROGRESS`, commit and push. Work on that task only.
3. When it's done (or blocked), set the status in TASKS.md, append a report below, then commit and push. Commit message: `T0x: <short summary>`.
4. Gates are non-blocking (fast-track mode): post the gate report, apply the decision rules in TASKS.md, and continue. Stop only on a `STOP` message. `git pull` at the start of every task.
5. If something in the plan looks wrong, post a `QUESTION` and wait. Don't silently change the design.

## Rules
- `config/experiment.yaml` and `prompts/templates.md` change only through an approved message. After the tag `config-frozen-v1`, they don't change at all.
- Never commit secrets, tokens, model weights or `data/images/`.
- Never write paper text (the course forbids AI-written paper content). Produce numbers, tables and figures only.
- Report failures honestly, with the error output. Never invent numbers.
- Long jobs: run them with `nohup` or `tmux`, log to `logs/` (git-ignored), and post progress at least every 2 hours.

## Message format
Append new messages at the **bottom**. Never edit old ones.

```
### [YYYY-MM-DD HH:MM UTC] RUNNER -> PLANNER | T03 DONE
**Summary:** one or two lines
**Numbers:** key counts and results (tables welcome)
**Files:** paths committed
**Issues / questions:** anything needing a decision (or "none")
```
Allowed tags after the task ID: `STARTED`, `PROGRESS`, `DONE`, `BLOCKED`, `QUESTION`, `APPROVED Gx`, `DECISION`, `ALL DONE`.

---

## Log

### [2026-11-11] PLANNER -> RUNNER | KICKOFF
**Summary:** The repo is set up. Start with T00 and work down TASKS.md. The deadline is tight (paper due Nov 16), so keep each report short and post promptly. Stop at G1 and G2.
**Files:** README.md, TASKS.md, config/experiment.yaml, prompts/templates.md
**Issues / questions:** In T00, tell us whether `HF_TOKEN` is set (Gemma is gated) and whether the 72B model fits in 4×48 GB with room for KV cache.

### [2026-11-14] PLANNER -> RUNNER | FAST-TRACK
**Summary:** The deadline moved, and experiments must now be finished by **end of Nov 15**. Fast-track mode is on: gates no longer block (see TASKS.md for the G2 decision rules). The model list is cut to 5 (see config). Default for T09 (API models) is SKIPPED unless the OWNER approves.
**Files:** TASKS.md, config/experiment.yaml, COLLAB.md
**Issues / questions:** Post progress at least every 2 hours. If something blocks for more than 45 min, take the fallback or post `BLOCKED` and move on.

### [2026-11-14 15:40 UTC] RUNNER -> PLANNER | T00 DONE
**Summary:** Env ready. 4× NVIDIA RTX PRO 5000 Blackwell (48 GB each, sm_120), driver 580.178.04 / CUDA 13.0. vLLM 0.33.0 (torch 2.14.0+cu130, transformers 5.20.2) installed in `.venv` and GPU matmul tested OK. All 5 models available, all fit.
**Numbers:**
- Host `scerbcs-bebe3fs`, Python 3.12.3, 64 CPU, 251 GB RAM, 1.3 TB free disk. HF cache: `~/.cache/huggingface/hub`
- Internet: HF and GitHub reachable. `HF_TOKEN` env var is **not** set, but a stored HF login (`~/.cache/huggingface/token`) exists and **has Gemma access** (gated config download OK).
- Font: `/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf` (already installed)

| model | available | fits | TP | notes |
|---|---|---|---|---|
| Qwen/Qwen2.5-VL-3B-Instruct | y | y | 1 | 7.5 GB bf16, rev 66285546 |
| Qwen/Qwen2.5-VL-7B-Instruct | y | y | 1 | 16.6 GB, rev cc594898 |
| OpenGVLab/InternVL3-8B | y | y | 1 | 15.9 GB, rev 853e3a79, vLLM `InternVLChatModel` |
| google/gemma-3-12b-it | y | y | 1 | 24.4 GB, ~15 GB left for KV, rev 96b6f1ec |
| Qwen/Qwen2.5-VL-32B-Instruct | y | y | 2 | 68.3 GB, TP=2 leaves ~25 GB KV, rev 7cfb30d7 |

- The 72B model (from the kickoff question) would need TP=4 (~146 GB weights, ~45 GB KV). It would fit, but it's dropped in the fast-track list.
- Plan for speed: run TP=1 models in parallel on separate GPUs (one model per GPU, still one vLLM process per model).
- Newer generations (Qwen3-VL, InternVL3.5) exist and are supported, but I'm not switching without approval.
**Files:** env/requirements.lock.txt
**Issues / questions:** none. Weights are downloading in the background.

### [2026-11-14 15:45 UTC] RUNNER -> PLANNER | T01 DONE
**Summary:** Package `src/vmod/` (pip-installed editable in `.venv`). `python -m vmod --help` lists download/prepare/render/selftest/run/score/analyze. Provenance helper (`vmod.meta`) stamps study_id, git commit and UTC time into every output (CSV header comments, or a `.meta.json` sidecar for jsonl). pytest: 3 passed.
**Files:** pyproject.toml, src/vmod/{__init__,__main__,config,meta}.py, tests/test_config.py
**Issues / questions:** I added a `download` subcommand for T02.

### [2026-11-14 15:37 UTC] RUNNER -> PLANNER | T02 DONE
**Summary:** All three datasets downloaded. WTQ comes from the GitHub release zip v1.0.2, because the HF `stanfordnlp/wikitablequestions` loader is script-based and current `datasets` refuses to run it. No WTQ QUESTION is needed.
**Numbers:** CRUXEval test 800 (MIT) · GSM8K main test 1,319 (MIT) · WTQ pristine-unseen-tables 4,344 (CC BY-SA 4.0). No license forbids this use. WTQ is share-alike, so the committed item files carry that license and need attribution.
**Files:** data/MANIFEST.md, src/vmod/download.py
**Issues / questions:** none. (Note: my T00/T01 header times were approximate. From now on they come from `date -u`.)

### [2026-11-14] PLANNER -> RUNNER | NEW TASK T07b
**Summary:** I added T07b (a replication check) between T07 and Gate G2: re-run the pilot set once more on every kept model and report run-to-run agreement. The instructor asked how replication is handled. This task documents it. It is short (pilot size only), so do not skip it.
**Files:** TASKS.md
**Issues / questions:** none
### [2026-11-14 15:38 UTC] RUNNER -> PLANNER | T03 DONE
**Summary:** Items built per templates.md, exclusions applied before sampling (seed 630, `random.Random(630).sample` of eligible items sorted by source index; the first 30 are pilot, the next 500 main, no overlap). If G2 drops N to 300, main = the first 300 of the 500 main items.
**Numbers:** counts are before exclusion → after exclusion. Reasons are not mutually exclusive.

| content | total | excluded | eligible | max_line_chars | max_lines | table_max_rows | render_fails | pilot | main |
|---|---|---|---|---|---|---|---|---|---|
| code | 800 | 3 | 797 | 0 | 0 | – | 3 | 30 | 500 |
| math | 1319 | 0 | 1319 | 0 | 0 | – | 0 | 30 | 500 |
| table | 4344 | 1396 | 2948 | 1064 | 305 | 487 | 43 | 30 | 500 |

**Implementation choices (please check):** `render_fails` = a character with no glyph in DejaVu Sans Mono (e.g. CJK, Hebrew), or a control character other than newline (2 CRUXEval items contain literal TAB). Table format: cells padded to column width and joined with `" | "`; the dash row is per-column dashes joined by `" | "`; line ends right-stripped; WTQ escapes decoded, with in-cell newlines turned into spaces. GSM8K double spaces after sentences are kept as `textwrap.fill` leaves them.
**Files:** src/vmod/{content,prepare}.py, data/items/*.jsonl (+ .meta.json), data/items/summary.json, data/exclusions.csv
**Issues / questions:** The OWNER limited me to **at most 2 GPUs** (GPU 0,1). The 32B model will run at TP=2. TP=1 models run at most 2 at a time.

### [2026-11-14 15:39 UTC] RUNNER -> PLANNER | T04 DONE
**Summary:** 1,590 PNGs rendered (pilot + main) with DejaVu Sans Mono 20 px, line pitch 26 px (20×1.3), 24 px padding, black on white, no wrapping, no rescaling. Width = ceil(longest line advance) + 48. Height = (lines−1)·26 + ascent + descent + 48. Determinism: **20/20** re-renders sha256-identical.
**Numbers:** image size (px, min / median / max)

| content | width | height | pixels |
|---|---|---|---|
| code | 289 / 542 / 1301 | 150 / 228 / 410 | 56k / 126k / 308k |
| math | 916 / 1000 / 1012 | 98 / 124 / 280 | 90k / 125k / 283k |
| table | 567 / 1289 / 1976 | 306 / 514 / 1216 | 242k / 657k / 2.09M |

The largest image (2.09 MP) is under Qwen2.5-VL's default max_pixels (12.8 MP), so no downscaling is expected there. I'll check per model in T06.
**Files:** src/vmod/render.py, data/images_manifest.csv, reports/render_samples/ (4 random + largest per type, size_stats.json)
**Issues / questions:** none

### [2026-11-14 15:42 UTC] RUNNER -> PLANNER | T05 DONE
**Summary:** Prompts are parsed verbatim from templates.md. The parser takes the last line with `Final answer:` and tolerates `**`/`__` around the marker, edge-only markdown (`**x**`, backticks, `$x$`, `\boxed{}`) and a trailing period. Outer quotes are stripped for math/table only, and only when no matching quote appears inside. They are **not** stripped for code, because there the quotes are part of the Python literal. Scorers follow T05. Table scoring uses a py3 port of the **official WTQ evaluator** (`src/vmod/wtq_eval.py`, logic unchanged) with the CoreNLP canonical targets (`targetCanon`, now stored as `gold_canon` in the table items; sampling unchanged). Code scoring: one subprocess per batch, `eval` with empty builtins, sockets disabled, a 2 GB memory limit and a 5 s alarm per item. Unprivileged network namespaces (`unshare -n`) aren't permitted here, so "no network" means no builtins/import plus disabled sockets.
**Numbers:** self-test gold **1590/1590** correct · hand-made wrong/unparseable **20/20** incorrect · pytest 30 passed. The first self-test run caught 4 parser bugs (markdown stripped inside code literals; quote stripping on `"A" | "B"`). They are fixed and now covered by tests.
**Transcription choice (please check):** `cer` is computed on whitespace-collapsed strings, consistent with `transcription_exact` (otherwise table column padding would dominate). `cer_raw` on raw strings is also stored. A missing transcription counts as an empty string (cer = 1).
**Files:** src/vmod/{prompts,scoring,wtq_eval,selftest}.py, tests/test_scoring.py, reports/selftest.json, data/items/*_table.jsonl (gold_canon added)
**Issues / questions:** none

### [2026-11-14 15:42 UTC] RUNNER -> PLANNER | G1 report (non-blocking)
**Summary:** Render samples are in `reports/render_samples/` (4 random + largest per content type). Exclusions: code 3, math 0, table 1,396 of 4,344 (details in the T03 report and `data/exclusions.csv`). Self-test **100%** (hard requirement met). Continuing to T06.

### [2026-11-14 16:48 UTC] RUNNER -> PLANNER | T06 DONE
**Summary:** `vmod run` works on all 5 models: vLLM 0.33 offline `llm.chat` with each model's own chat template, one user turn, image before text for B/C, greedy decoding (T=0, top_p=1, max 2048, n=1, seed 630), max_model_len 16384, resumable (a rerun skips done rows), over-context requests logged to `*.skipped.csv`. Smoke test (5 items × 3 types × 3 conditions = 45 requests per model) passed through scoring on all 5 models. `vmod score` writes `results/scored/{set}_all.csv.gz`.
**Effective image resolution (please read):**
- **Qwen2.5-VL (3B/7B/32B):** native resolution. max_pixels = 12.8 MP > largest image (2.09 MP). Each side rounds to a multiple of 28 (≤14 px). Image tokens match native size. **No downscaling.**
- **InternVL3-8B:** fixed 448 px tiles chosen by *aspect ratio*, not size. I raised max_dynamic_patch to 24 (default 12), plus the thumbnail. Small images are often upscaled (e.g. 446×254 → 16 tiles), and some wide tables are **downscaled** (e.g. 1241×618 → 2×1 tiles = 896×448 + thumbnail). This is the model's own preprocessing; I did not hack around it.
- **Gemma-3-12B:** the SigLIP encoder is fixed at 896×896, so every image is resized to 896², which **downscales** wide tables and math. I enabled pan-and-scan, which adds 896² crops at higher resolution (tables get 2–4 crops; short code/math images get none).
**Deviation (please review/veto):** the parser now also handles a bare marker line. Qwen-32B usually writes `### Final Answer:` (sometimes without the colon) and puts the answer on the **next** line(s), inside a code fence or `\[\boxed{..}\]`. Under the literal rule its smoke parse rate was 60–80%, with the answers plainly present. New rule: if nothing follows the marker on the last marker line, take the next non-empty block. Whenever the strict rule parses, the prediction is identical. The strict version is kept as `parse_ok_strict` / `correct_strict` in the scored file for a sensitivity analysis. After the change the 32B smoke parse rate is 100%. Tests: 37 passed. Self-test still 1590/1590 and 20/20.
**Ops notes:** FlashInfer's sampler JIT needs nvcc (not installed), so `VLLM_USE_FLASHINFER_SAMPLER=0` is set (decoding is greedy, so this is equivalent). GPU limit: 2 (GPU 0,1).
**Files:** src/vmod/{run,score,scoring}.py, tests/test_scoring.py, results/raw/pilot_smoke/
**Issues / questions:** the parser deviation above.

### [2026-11-14 17:02 UTC] RUNNER -> PLANNER | T07 DONE
**Summary:** Pilot (30 items × 3 types × 3 conditions = 270 requests per model) ran on all 5 models. 0 crashes, 0 skipped. Parse rate uses the primary parser; "strict" = the literal same-line rule.
**Numbers:** accuracy (A / B / C)

| model | parse A/B/C | strict parse A/B/C | code | math | table | mean out tok A/B/C | max %length cell | s/100 prompts |
|---|---|---|---|---|---|---|---|---|
| Qwen2.5-VL-3B | .94/.93/.93 | .93/.93/.93 | .47/.40/.53 | .77/.73/.83 | .47/.43/.37 | 248/318/449 | 6.7 (table B) | 9.8 |
| Qwen2.5-VL-7B | .97/.96/.98 | .97/.94/.98 | .50/.57/.53 | .90/.73/.80 | .73/.63/.63 | 343/323/466 | 10.0 (code A) | 15.5 |
| InternVL3-8B | 1/1/1 | 1/1/1 | .53/.50/.47 | .90/.87/.87 | .73/.70/.57 | 274/267/439 | 3.3 | 33.3 |
| Gemma-3-12B | .99/1/.99 | .99/1/.99 | .67/.63/.63 | .93/.87/.90 | .73/.70/.67 | 205/227/418 | 3.3 | 32.2 |
| Qwen2.5-VL-32B | .99/.99/1 | .63/.72/.73 | .77/.73/.67 | .97/.90/.90 | .67/.63/.67 | 432/456/622 | 3.3 | 47.3 |

Estimated main-run generation time (scaled from the pilot): N=500 → 3B 0.12 h, 7B 0.19 h, InternVL 0.42 h, Gemma 0.40 h, 32B 0.59 h. **Total ≈ 1.7 GPU-h, ≈ 1.2 h wall** with 2 lanes (+ ~2 min load per model). N=300 → ≈ 1.0 GPU-h. Full table in `results/analysis/pilot_report.csv`.
Raw responses: 3 per condition from Qwen-7B in `reports/pilot_samples.md`. The prompts work as intended: step-by-step reasoning, then a `Final answer:` line.
**Second deviation (please review/veto):** in condition C, Gemma (code, 27/30) and Qwen-32B (code 30/30, table 10/30) often ignore the `<transcription>` tags and write a `**Transcription:**` / `### Transcription` heading followed by a code fence. When there are no tags, the extractor now falls back to the first code fence after a "Transcription" heading. A new column `transcription_source` (tags / open_tag / heading_fence / none) records which rule applied, and RQ2 will add a tags-only sensitivity check. Responses with no transcription at all keep CER = 1.
**Files:** results/raw/pilot/, results/analysis/pilot_report.csv, results/analysis/pilot_estimates.json, reports/pilot_samples.md, src/vmod/{pilot,analyze}.py, scripts/lane.sh
**Issues / questions:** the transcription fallback above. T07b rep2 runs are done for 4/5 models; 32B is running.

### [2026-11-14 17:03 UTC] RUNNER -> PLANNER | T07b DONE
**Summary:** Whole pilot re-run on all 5 models (fresh process, request order shuffled with seed 631, identical settings, vLLM 0.33.0). Per model × condition, n = 90:

| model | cond | % identical text | % correct agree | κ | acc run1 | acc run2 |
|---|---|---|---|---|---|---|
| Qwen-3B | A / B / C | 33.3 / 32.2 / 28.9 | **90.0 / 92.2 / 88.9** | .80 / .84 / .77 | .567 / .522 / .578 | .533 / .511 / .578 |
| Qwen-7B | A / B / C | 41.1 / 42.2 / 48.9 | 95.6 / **94.4** / 95.6 | .89 / .88 / .90 | .711 / .644 / .656 | .733 / .656 / .633 |
| InternVL3-8B | A / B / C | 42.2 / 37.8 / 40.0 | 97.8 / 95.6 / 95.6 | .95 / .90 / .91 | .722 / .689 / .633 | .700 / .667 / .611 |
| Gemma-3-12B | A / B / C | 63.3 / 46.7 / 35.6 | 95.6 / 98.9 / **92.2** | .88 / .97 / .80 | .778 / .733 / .733 | .733 / .722 / .744 |
| Qwen-32B | A / B / C | 43.3 / 45.6 / 34.4 | 97.8 / 97.8 / 98.9 | .93 / .94 / .97 | .800 / .756 / .744 | .778 / .733 / .756 |

Largest |acc run1 − run2| over all model × content × condition cells (n = 30): **0.100** (Gemma, code, A). Largest at the model × condition level (n = 90): 0.044.
**Decision (pre-registered rule):** 5 of 15 cells are below 95% correct-agreement (bold). Per the rule we **continue with one run per item**, and this will be flagged as a conclusion-validity threat in `reports/summary.md`. Observed cause: greedy decoding in vLLM is not batch-invariant (a different batch composition gives different float rounding), so responses diverge after the first changed token. vLLM has a batch-invariant mode that could remove this, but it is not used (no time, and it would change the setup).
**Files:** results/raw/pilot_rep2/, results/analysis/replication_check.csv, src/vmod/pilot.py

### [2026-11-14 17:03 UTC] RUNNER -> PLANNER | APPROVED G2 (rules applied, fast-track)
**Decisions:**
1. **Models:** all 5 kept. Each ran the pilot with no crash and parse rate ≥ 0.93 in every condition (primary parser). Final list: Qwen2.5-VL-3B (66285546), Qwen2.5-VL-7B (cc594898), InternVL3-8B (853e3a79), gemma-3-12b-it (96b6f1ec), Qwen2.5-VL-32B (7cfb30d7). Note: under the *strict* same-line parser, Qwen-32B would be at 0.63/0.72/0.73. It passes only because of the parser deviation in T06.
2. **max_new_tokens:** pilot cells over 5% `finish_reason=length`: Qwen-7B code A 10.0%, code B 6.7%; Qwen-3B table B 6.7%. Raised to **4096 for all models**.
3. **N:** estimated main-run time ≈ 1.7 GPU-h (≈ 1.2 h wall on 2 GPUs). Even assuming 2× longer outputs at 4096, that's ≤ 3.5 GPU-h, which is **≤ 8 h, so main_per_content stays 500**.
Config committed and tagged **config-frozen-v1**. Starting T08 now (smallest first, 2 lanes: GPU0 3B→Gemma-12B, GPU1 7B→InternVL-8B, then 32B on TP=2).

### [2026-11-14 17:12 UTC] RUNNER -> PLANNER | T08 PROGRESS (Qwen2.5-VL-3B-Instruct done)
**Summary:** integrity OK: 4500/4500 rows, skipped 0, duplicates 0, missing 0. Wall time 8.6 min (generation 0.129 h). finish_reason=length 1.51%.
**Numbers:** parse A/B/C 0.924 / 0.960 / 0.909 · accuracy A/B/C: code 0.386/0.342/0.358 · math 0.840/0.818/0.752 · table 0.428/0.454/0.392
**Files:** results/raw/main/Qwen__Qwen2.5-VL-3B-Instruct.jsonl.gz
**Issues / questions:** none

### [2026-11-14 17:17 UTC] RUNNER -> PLANNER | T08 PROGRESS (Qwen2.5-VL-7B-Instruct done)
**Summary:** integrity OK: 4500/4500 rows, skipped 0, duplicates 0, missing 0. Wall time 13.8 min (generation 0.217 h). finish_reason=length 1.0%.
**Numbers:** parse A/B/C 0.987 / 0.989 / 0.986 · accuracy A/B/C: code 0.524/0.490/0.480 · math 0.868/0.868/0.866 · table 0.626/0.664/0.668
**Files:** results/raw/main/Qwen__Qwen2.5-VL-7B-Instruct.jsonl.gz
**Issues / questions:** none

### [2026-11-14 17:37 UTC] RUNNER -> PLANNER | T08 PROGRESS (gemma-3-12b-it done)
**Summary:** integrity OK: 4500/4500 rows, skipped 0, duplicates 0, missing 0. Wall time 24.6 min (generation 0.392 h). finish_reason=length 0.18%.
**Numbers:** parse A/B/C 0.999 / 0.997 / 0.995 · accuracy A/B/C: code 0.688/0.494/0.542 · math 0.948/0.934/0.922 · table 0.734/0.648/0.726
**Files:** results/raw/main/google__gemma-3-12b-it.jsonl.gz
**Issues / questions:** none

### [2026-11-14 17:41 UTC] RUNNER -> PLANNER | T08 PROGRESS (InternVL3-8B done)
**Summary:** integrity OK: 4500/4500 rows, skipped 0, duplicates 0, missing 0. Wall time 23.8 min (generation 0.385 h). finish_reason=length 0.31%.
**Numbers:** parse A/B/C 0.997 / 0.995 / 0.994 · accuracy A/B/C: code 0.632/0.506/0.522 · math 0.920/0.864/0.894 · table 0.648/0.588/0.628
**Files:** results/raw/main/OpenGVLab__InternVL3-8B.jsonl.gz
**Issues / questions:** none

### [2026-11-14 18:16 UTC] RUNNER -> PLANNER | T08 PROGRESS (Qwen2.5-VL-32B-Instruct done)
**Summary:** integrity OK: 4500/4500 rows, skipped 0, duplicates 0, missing 0. Wall time 34.7 min (generation 0.559 h). finish_reason=length 0.07%.
**Numbers:** parse A/B/C 0.996 / 0.993 / 0.998 · accuracy A/B/C: code 0.812/0.730/0.740 · math 0.918/0.902/0.948 · table 0.812/0.794/0.806
**Files:** results/raw/main/Qwen__Qwen2.5-VL-32B-Instruct.jsonl.gz
**Issues / questions:** none

### [2026-11-14 18:16 UTC] RUNNER -> PLANNER | T08 DONE
**Summary:** Main set (500 items × 3 content types × 3 conditions = 4,500 requests per model) is complete for all 5 G2 models. Every model passes integrity: each item × condition appears exactly once, 0 skipped (nothing over context at max_model_len 16384). Wall time 17:03–18:16 UTC (1 h 12 min) on GPU 0–1.
**Files:** results/raw/main/*.jsonl.gz (+ .meta.json, .skipped.csv)

### [2026-11-14 18:16 UTC] RUNNER -> PLANNER | T09 SKIPPED
**Summary:** No OWNER approval for API models was posted, so T09 is skipped (fast-track default). No API calls were made.

### [2026-11-14 18:17 UTC] RUNNER -> PLANNER | T10 DONE
**Summary:** `results/scored/main_all.csv.gz`: 22,500 rows (5 models × 1,500 items × 3 conditions). Contains all raw fields plus pred, parse_ok, correct, transcription, transcription_exact, cer, plus the extras parse_ok_strict, correct_strict, cer_raw, transcription_source, transcription_exact_lenient.
**Numbers:** parse rate, primary parser (strict same-line rule in brackets)

| model | A | B | C |
|---|---|---|---|
| Qwen2.5-VL-3B | .924 (.918) | .960 (.953) | .909 (.908) |
| Qwen2.5-VL-7B | .987 (.986) | .989 (.983) | .986 (.986) |
| InternVL3-8B | .997 (.997) | .995 (.993) | .994 (.993) |
| Gemma-3-12B | .999 (.999) | .997 (.997) | .995 (.995) |
| Qwen2.5-VL-32B | .996 (.691) | .993 (.739) | .998 (.731) |

Hand-check of 30 random rows (10 per content type, seed 630): the scorer agrees with a careful reading on **29/30**. The 1 disagreement: table-nu-2290, pred "Reggie Johnson" vs gold "Johnson". It's the same entity, but the official WTQ string match marks it incorrect. This is a known strictness of the official metric and I kept it as specified. Details: `results/analysis/handcheck_t10.csv`.
**Files:** results/scored/main_all.csv.gz, results/analysis/handcheck_t10.csv
**Issues / questions:** after T07 I made one more scoring fix, applied to all data: a code fence wrapping the whole transcription is stripped (Qwen-7B wrapped 87% of code transcriptions in ```python inside the tags). I also added a lenient exact metric for tables as a sensitivity check only. Both are listed in `reports/deviations.md`.

### [2026-11-14 18:18 UTC] RUNNER -> PLANNER | T11 DONE
**Summary:** Descriptives per model × content × condition (n, accuracy, 95% Wilson CI, parse rates, output-token mean/median/SD/IQR/min/max), input length per content type, and outlier lists. Figures (PNG + PDF): accuracy by condition faceted by content type; output-token box plots (log scale); A−B gap vs size for the Qwen family (Newcombe CIs).
**Numbers:** accuracy A / B / C. code: 3B .386/.342/.358 · 7B .524/.490/.480 · InternVL .632/.506/.522 · Gemma .688/.494/.542 · 32B .812/.730/.740. math: .840/.818/.752 · .868/.868/.866 · .920/.864/.894 · .948/.934/.922 · .918/.902/.948. table: .428/.454/.392 · .626/.664/.668 · .648/.588/.628 · .734/.648/.726 · .812/.794/.806. Outliers (kept): 383 responses > Q3+3·IQR, 138 with finish_reason=length (of 22,500).
**Files:** results/analysis/{descriptives,input_length,outliers,outlier_counts}.csv, results/figures/{accuracy_by_condition,output_tokens_boxplot,gap_A_minus_B_vs_size_qwen}.{png,pdf}

### [2026-11-14 18:18 UTC] RUNNER -> PLANNER | T12 DONE
**Summary:** Paired McNemar (exact), Newcombe paired CI, discordant OR with exact CI, and Holm within each family (A vs B, A vs C, B vs C; 15 tests each). Cochran's Q with Holm. Two sensitivity checks: unparseable pairs excluded, and the strict same-line parser.
**Numbers:** A vs B, Holm p < .05 in 5/15 cells, all with A > B: InternVL code (b/c 89/26, diff .126 [.085, .166]), InternVL math (43/15, .056), 32B code (50/9, .082), Gemma code (117/20, .194 [.151, .236]), Gemma table (88/45, .086). Sensitivity: 5/15 with unparseable pairs excluded, 6/15 with the strict parser. A vs C: 5/15 significant. B vs C: 3/15 (32B math and Gemma table with C > B; 3B math with B > C). Cochran's Q Holm p < .05: 7/15.
**Files:** results/analysis/rq1_{A_vs_B,A_vs_C,B_vs_C}{,_sens_parseable,_sens_strict_parser}.csv, rq1_cochran_q.csv
**Issues / questions:** GLMM not run (no `GLMM OK`).

### [2026-11-14 18:18 UTC] RUNNER -> PLANNER | T13 DONE
**Summary:** Transcription exact rate and CER distribution per model × content. A vs C McNemar split by transcription correctness under 4 rules: exact (primary), CER ≤ 0.02, lenient exact, and exact with tags only. Logit: correct(B) ~ CER(C) + model, per content type.
**Numbers:** exact rate code/math/table: 3B .670/.926/.000 · 7B .868/.816/.000 · InternVL .672/.936/.000 · Gemma .100/.698/.000 · 32B .778/.946/.004. **Primary exact match is ~0 for tables for every model** (dash-rule widths). The CER ≤ 0.02 and lenient rules give the table subsets. A−C gap on code, wrong transcription vs exact transcription: InternVL .238 vs .048, 32B .252 vs .021, Gemma .158 vs .040, 7B .121 vs .032, 3B .079 vs .003. Logit (pooled, model FE, n = 2,500 per type): CER coefficient not significant for any type (p = .52 / .11 / .55). CER > 0.02 indicator: OR .43 (p < .001) code, .58 (p = .012) math, .80 (p = .088) table.
**Files:** results/analysis/rq2_{transcription,A_vs_C_by_transcription,logit_B_on_cer}.csv
**Issues / questions:** Gemma gave no transcription in 80% of code C responses, so its code RQ2 numbers rest on 50 exact items. Flagged in summary.

### [2026-11-14 18:18 UTC] RUNNER -> PLANNER | T14 DONE
**Summary:** Wilcoxon signed-rank on output tokens A vs B (paired, Holm). Error sample exported. `reports/summary.md` written (numbers and tables only: every table, exclusions, models + revisions, package versions, GPU hours, deviations, data-quality flags, including the T07b replication table).
**Numbers:** Holm p < .05 in 7/15 cells. Median A−B tokens: Gemma code −35, 32B code −32, 32B table −18.5, 7B code +25.5, 7B math +20.5, InternVL math +38. Error sample: 100 A-correct/B-wrong flips per content type (available: code 385, math 149, table 338), seed 630, with empty `code`/`coder` columns for the OWNER. Total GPU hours: 2.81 (pilot + rep2 + main; smoke tests excluded, < 0.1 h).
**Files:** results/analysis/rq3_tokens_wilcoxon.csv, flip_counts.csv, results/coding/error_sample.csv, reports/summary.md, reports/deviations.md

### [2026-11-14 18:18 UTC] RUNNER -> PLANNER | ALL DONE
**Summary:** T00–T14 complete (T09 skipped, GLMM not run). Everything is committed. Please review the parser and transcription deviations (#6, #7, #14, #15 in `reports/deviations.md`). Strict-parser and tags-only sensitivity results are included for each, so you can veto any of them without re-running inference.

### [2026-11-15] PLANNER -> RUNNER | PHASE 4: replication runs + extension models
**Summary:** I reviewed T00-T14, and the OWNER checked the RQ1 numbers independently: they reproduce exactly from `main_all.csv.gz`. New tasks T15-T18 are in TASKS.md, under a **16-hour wall-time budget** from the start of T15:
1. Full replicate runs 2 and 3 for the 5 primary models (top priority, because the instructor asked about replication).
2. Replication analysis.
3. Extension models from `config/extension.yaml`, in priority order: gemma-3-27b, Qwen3-VL-8B, InternVL3.5-8B, Qwen2.5-VL-72B-AWQ, Llama-3.2-11B-Vision (optional). Each gets a pilot plus 3 runs.
4. Extended analysis, plus `reports/paper_numbers.md`.
The frozen config is unchanged and run 1 stays the primary analysis. The extension is labeled exploratory.
**Accepted deviations:** #6, #7, #14 and #15 are accepted, with their sensitivity analyses kept as reported. For RQ2 on **tables**, the primary exact-match measure is unusable (about 0%), so report CER ≤ 0.02 and the lenient rule as the table measures, and keep the note in deviations.md.
**Issues / questions:** GPU limit stays at 2 unless the OWNER says otherwise. Post after every completed model-run.

### [2026-11-15] PLANNER -> RUNNER | CORRECTION to the PHASE 4 message
**Summary:** Two corrections. (1) The PLANNER recomputed the RQ1 numbers, not the OWNER. (2) Deviations #6/#7/#14/#15 are accepted **provisionally**, as the PLANNER's recommendation; the OWNER may still veto them. Keep all sensitivity versions so a veto needs no re-run. Everything else in the PHASE 4 message stands.

### [2026-11-15] OWNER (via PLANNER) -> RUNNER | DECISION: GPU limit
**Summary:** The OWNER confirms: use **2 GPUs (GPU 0,1) only** for Phase 4 (T15-T18). Run the replicate runs first. Then do the extension models in priority order and stop at the 16-hour budget; it's fine if lower-priority models don't finish.

### [2026-11-15 09:44 UTC] RUNNER -> PLANNER | T15 STARTED
**Summary:** Phase 4 started; the 16-hour budget runs from now (2026-11-15 09:44 UTC). Replicate runs 2 and 3 (seeds 631/632) for the 5 primary models on GPU 0,1 only: lane GPU0 = 3B, InternVL; lane GPU1 = 7B, Gemma-12B; then 32B (TP=2). Revisions are pinned to run 1 (read from the run-1 meta sidecars).
**Files:** src/vmod/run.py (--out-dir, --run column, revision pin, --gpu-mem), scripts/lane4.sh, scripts/post_run.sh
**Issues / questions:** Another user's training jobs hold 3-6 GB on GPU 0 and 1, so vLLM gpu_memory_utilization is 0.80 instead of 0.90. That only shrinks the KV cache; decoding settings are unchanged. Logged as a deviation.

### [2026-11-15 09:54 UTC] RUNNER -> PLANNER | T15 PROGRESS (Qwen2.5-VL-3B-Instruct main_run2 done)
**Summary:** integrity OK: 4500/4500 rows, skipped 0, duplicates 0, missing 0. Wall time 10.6 min (generation 0.159 h). finish_reason=length 1.8%.
**Numbers:** parse A/B/C 0.928 / 0.960 / 0.906 · accuracy A/B/C: code 0.386/0.326/0.346 · math 0.836/0.830/0.750 · table 0.460/0.460/0.366
**Files:** results/raw/main_run2/Qwen__Qwen2.5-VL-3B-Instruct.jsonl.gz
**Issues / questions:** none

### [2026-11-15 10:01 UTC] RUNNER -> PLANNER | T15 PROGRESS (Qwen2.5-VL-7B-Instruct main_run2 done)
**Summary:** integrity OK: 4500/4500 rows, skipped 0, duplicates 0, missing 0. Wall time 17.6 min (generation 0.275 h). finish_reason=length 0.82%.
**Numbers:** parse A/B/C 0.991 / 0.991 / 0.989 · accuracy A/B/C: code 0.534/0.490/0.474 · math 0.878/0.874/0.882 · table 0.618/0.650/0.666
**Files:** results/raw/main_run2/Qwen__Qwen2.5-VL-7B-Instruct.jsonl.gz
**Issues / questions:** none

### [2026-11-15 10:05 UTC] RUNNER -> PLANNER | T15 PROGRESS (Qwen2.5-VL-3B-Instruct main_run3 done)
**Summary:** integrity OK: 4500/4500 rows, skipped 0, duplicates 0, missing 0. Wall time 10.4 min (generation 0.157 h). finish_reason=length 1.67%.
**Numbers:** parse A/B/C 0.925 / 0.952 / 0.907 · accuracy A/B/C: code 0.374/0.320/0.372 · math 0.840/0.800/0.744 · table 0.432/0.462/0.380
**Files:** results/raw/main_run3/Qwen__Qwen2.5-VL-3B-Instruct.jsonl.gz
**Issues / questions:** none

### [2026-11-15 10:19 UTC] RUNNER -> PLANNER | T15 PROGRESS (Qwen2.5-VL-7B-Instruct main_run3 done)
**Summary:** integrity OK: 4500/4500 rows, skipped 0, duplicates 0, missing 0. Wall time 17.4 min (generation 0.273 h). finish_reason=length 1.07%.
**Numbers:** parse A/B/C 0.990 / 0.986 / 0.987 · accuracy A/B/C: code 0.518/0.482/0.470 · math 0.870/0.872/0.870 · table 0.616/0.656/0.674
**Files:** results/raw/main_run3/Qwen__Qwen2.5-VL-7B-Instruct.jsonl.gz
**Issues / questions:** none

### [2026-11-15 10:39 UTC] RUNNER -> PLANNER | T15 PROGRESS (InternVL3-8B main_run2 done)
**Summary:** integrity OK: 4500/4500 rows, skipped 0, duplicates 0, missing 0. Wall time 33.9 min (generation 0.54 h). finish_reason=length 0.44%.
**Numbers:** parse A/B/C 0.998 / 0.992 / 0.993 · accuracy A/B/C: code 0.620/0.510/0.530 · math 0.918/0.866/0.890 · table 0.674/0.588/0.616
**Files:** results/raw/main_run2/OpenGVLab__InternVL3-8B.jsonl.gz
**Issues / questions:** none

### [2026-11-15 10:52 UTC] RUNNER -> PLANNER | T15 PROGRESS (gemma-3-12b-it main_run2 done)
**Summary:** integrity OK: 4500/4500 rows, skipped 0, duplicates 0, missing 0. Wall time 32.8 min (generation 0.526 h). finish_reason=length 0.18%.
**Numbers:** parse A/B/C 0.998 / 0.997 / 0.995 · accuracy A/B/C: code 0.694/0.496/0.540 · math 0.952/0.934/0.940 · table 0.728/0.670/0.724
**Files:** results/raw/main_run2/google__gemma-3-12b-it.jsonl.gz
**Issues / questions:** none

### [2026-11-15 11:12 UTC] RUNNER -> PLANNER | T15 PROGRESS (InternVL3-8B main_run3 done)
**Summary:** integrity OK: 4500/4500 rows, skipped 0, duplicates 0, missing 0. Wall time 32.9 min (generation 0.534 h). finish_reason=length 0.33%.
**Numbers:** parse A/B/C 0.998 / 0.995 / 0.993 · accuracy A/B/C: code 0.642/0.512/0.528 · math 0.916/0.860/0.894 · table 0.676/0.588/0.614
**Files:** results/raw/main_run3/OpenGVLab__InternVL3-8B.jsonl.gz
**Issues / questions:** none

### [2026-11-15 11:24 UTC] RUNNER -> PLANNER | T15 PROGRESS (gemma-3-12b-it main_run3 done)
**Summary:** integrity OK: 4500/4500 rows, skipped 0, duplicates 0, missing 0. Wall time 32.3 min (generation 0.518 h). finish_reason=length 0.11%.
**Numbers:** parse A/B/C 0.999 / 0.997 / 0.997 · accuracy A/B/C: code 0.688/0.500/0.542 · math 0.950/0.932/0.932 · table 0.726/0.664/0.732
**Files:** results/raw/main_run3/google__gemma-3-12b-it.jsonl.gz
**Issues / questions:** none

### [2026-11-15 11:25 UTC] RUNNER -> PLANNER | T16 PROGRESS (interim, 4 of 5 models)
**Summary:** Interim replication analysis on runs 1-3 for 3B, 7B, InternVL3-8B and Gemma-12B (32B runs 2-3 are in progress). Holm here is over 12 cells, not 15, so p-values will change slightly in the final table. These CSVs are not committed yet.
**Numbers:** A−B diff, runs 1/2/3: InternVL code .126/.110/.130 (significant in 3/3), InternVL math .056/.052/.056 (3/3), Gemma code .194/.198/.188 (3/3), InternVL table .060/.086/.088 (2/3), Gemma table .086/.058/.062 (1/3: run 1 only), 3B code .044/.060/.054 (1/3: run 2 only). The other 6 cells are non-significant in all runs. Cell accuracy SD across runs is at most .017 (max range .032). Fleiss' kappa per cell is .73-.95, with a median of 8.1% of items mixed across runs. RQ2 code pattern (A−C gap larger when the transcription is wrong) holds in every model × run under both the exact and CER ≤ 0.02 rules (12/12 each).
**Issues / questions:** none

### [2026-11-15 12:18 UTC] RUNNER -> PLANNER | T15 PROGRESS (Qwen2.5-VL-32B-Instruct main_run2 done)
**Summary:** integrity OK: 4500/4500 rows, skipped 0, duplicates 0, missing 0. Wall time 54.4 min (generation 0.879 h). finish_reason=length 0.04%.
**Numbers:** parse A/B/C 0.997 / 0.995 / 0.998 · accuracy A/B/C: code 0.814/0.728/0.754 · math 0.928/0.912/0.952 · table 0.816/0.780/0.798
**Files:** results/raw/main_run2/Qwen__Qwen2.5-VL-32B-Instruct.jsonl.gz
**Issues / questions:** none

### [2026-11-15 13:13 UTC] RUNNER -> PLANNER | T15 PROGRESS (Qwen2.5-VL-32B-Instruct main_run3 done)
**Summary:** integrity OK: 4500/4500 rows, skipped 0, duplicates 0, missing 0. Wall time 54.3 min (generation 0.887 h). finish_reason=length 0.07%.
**Numbers:** parse A/B/C 0.997 / 0.993 / 0.998 · accuracy A/B/C: code 0.820/0.738/0.754 · math 0.924/0.908/0.944 · table 0.818/0.786/0.802
**Files:** results/raw/main_run3/Qwen__Qwen2.5-VL-32B-Instruct.jsonl.gz
**Issues / questions:** none

### [2026-11-15 13:19 UTC] RUNNER -> PLANNER | T17 PROGRESS (gemma-3-27b-it ext/pilot done)
**Summary:** integrity OK: 270/270 rows, skipped 0, duplicates 0, missing 0. Wall time 5.4 min (generation 0.054 h). finish_reason=length 1.11%.
**Numbers:** parse A/B/C 0.989 / 0.989 / 0.989 · accuracy A/B/C: code 0.733/0.667/0.700 · math 1.000/0.933/0.933 · table 0.767/0.867/0.767
**Files:** results/raw/ext/pilot/google__gemma-3-27b-it.jsonl.gz
**Issues / questions:** none

### [2026-11-15 13:55 UTC] RUNNER -> PLANNER | T17 PROGRESS (gemma-3-27b-it ext/run1 done)
**Summary:** integrity OK: 4500/4500 rows, skipped 0, duplicates 0, missing 0. Wall time 35.7 min (generation 0.573 h). finish_reason=length 0.16%.
**Numbers:** parse A/B/C 1.000 / 0.999 / 0.997 · accuracy A/B/C: code 0.758/0.612/0.684 · math 0.972/0.946/0.948 · table 0.778/0.742/0.746
**Files:** results/raw/ext/run1/google__gemma-3-27b-it.jsonl.gz
**Issues / questions:** none

### [2026-11-15 14:31 UTC] RUNNER -> PLANNER | T17 PROGRESS (gemma-3-27b-it ext/run2 done)
**Summary:** integrity OK: 4500/4500 rows, skipped 0, duplicates 0, missing 0. Wall time 36.6 min (generation 0.59 h). finish_reason=length 0.16%.
**Numbers:** parse A/B/C 1.000 / 0.999 / 0.997 · accuracy A/B/C: code 0.746/0.612/0.676 · math 0.970/0.948/0.948 · table 0.764/0.736/0.754
**Files:** results/raw/ext/run2/google__gemma-3-27b-it.jsonl.gz
**Issues / questions:** none

### [2026-11-15 15:07 UTC] RUNNER -> PLANNER | T17 PROGRESS (gemma-3-27b-it ext/run3 done)
**Summary:** integrity OK: 4500/4500 rows, skipped 0, duplicates 0, missing 0. Wall time 35.7 min (generation 0.575 h). finish_reason=length 0.11%.
**Numbers:** parse A/B/C 0.999 / 0.999 / 0.998 · accuracy A/B/C: code 0.764/0.612/0.682 · math 0.966/0.948/0.942 · table 0.766/0.736/0.758
**Files:** results/raw/ext/run3/google__gemma-3-27b-it.jsonl.gz
**Issues / questions:** none

### [2026-11-15 15:11 UTC] RUNNER -> PLANNER | T17 PROGRESS (Qwen3-VL-8B-Instruct ext/pilot done)
**Summary:** integrity OK: 270/270 rows, skipped 0, duplicates 0, missing 0. Wall time 3.3 min (generation 0.029 h). finish_reason=length 4.44%.
**Numbers:** parse A/B/C 0.967 / 0.944 / 0.956 · accuracy A/B/C: code 0.800/0.767/0.767 · math 1.000/0.867/0.900 · table 0.767/0.700/0.800
**Files:** results/raw/ext/pilot/Qwen__Qwen3-VL-8B-Instruct.jsonl.gz
**Issues / questions:** none

### [2026-11-15 15:11 UTC] RUNNER -> PLANNER | T17 PROGRESS (InternVL3_5-8B ext/pilot done)
**Summary:** integrity OK: 270/270 rows, skipped 0, duplicates 0, missing 0. Wall time 3.4 min (generation 0.038 h). finish_reason=length 0.0%.
**Numbers:** parse A/B/C 1.000 / 0.944 / 1.000 · accuracy A/B/C: code 0.667/0.667/0.533 · math 0.933/0.667/0.867 · table 0.767/0.800/0.767
**Files:** results/raw/ext/pilot/OpenGVLab__InternVL3_5-8B.jsonl.gz
**Issues / questions:** none

### [2026-11-15 15:34 UTC] RUNNER -> PLANNER | T17 PROGRESS (Qwen3-VL-8B-Instruct ext/run1 done)
**Summary:** integrity OK: 4500/4500 rows, skipped 0, duplicates 0, missing 0. Wall time 23.5 min (generation 0.377 h). finish_reason=length 3.58%.
**Numbers:** parse A/B/C 0.959 / 0.967 / 0.970 · accuracy A/B/C: code 0.808/0.686/0.702 · math 0.952/0.942/0.954 · table 0.828/0.778/0.798
**Files:** results/raw/ext/run1/Qwen__Qwen3-VL-8B-Instruct.jsonl.gz
**Issues / questions:** none

### [2026-11-15 15:49 UTC] RUNNER -> PLANNER | T17 PROGRESS (InternVL3_5-8B ext/run1 done)
**Summary:** integrity OK: 4500/4500 rows, skipped 0, duplicates 0, missing 0. Wall time 38.4 min (generation 0.627 h). finish_reason=length 0.18%.
**Numbers:** parse A/B/C 0.999 / 0.962 / 0.996 · accuracy A/B/C: code 0.734/0.626/0.642 · math 0.954/0.838/0.942 · table 0.766/0.716/0.746
**Files:** results/raw/ext/run1/OpenGVLab__InternVL3_5-8B.jsonl.gz
**Issues / questions:** none

### [2026-11-15 15:58 UTC] RUNNER -> PLANNER | T17 PROGRESS (Qwen3-VL-8B-Instruct ext/run2 done)
**Summary:** integrity OK: 4500/4500 rows, skipped 0, duplicates 0, missing 0. Wall time 23.8 min (generation 0.382 h). finish_reason=length 3.93%.
**Numbers:** parse A/B/C 0.958 / 0.960 / 0.971 · accuracy A/B/C: code 0.796/0.698/0.694 · math 0.946/0.940/0.954 · table 0.816/0.768/0.800
**Files:** results/raw/ext/run2/Qwen__Qwen3-VL-8B-Instruct.jsonl.gz
**Issues / questions:** none

### [2026-11-15 16:22 UTC] RUNNER -> PLANNER | T17 PROGRESS (Qwen3-VL-8B-Instruct ext/run3 done)
**Summary:** integrity OK: 4500/4500 rows, skipped 0, duplicates 0, missing 0. Wall time 23.7 min (generation 0.379 h). finish_reason=length 3.89%.
**Numbers:** parse A/B/C 0.962 / 0.959 / 0.972 · accuracy A/B/C: code 0.784/0.684/0.696 · math 0.948/0.942/0.958 · table 0.828/0.778/0.804
**Files:** results/raw/ext/run3/Qwen__Qwen3-VL-8B-Instruct.jsonl.gz
**Issues / questions:** none
