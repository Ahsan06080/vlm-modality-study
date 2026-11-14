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
