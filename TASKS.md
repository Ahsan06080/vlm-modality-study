# TASKS: sequential run list for the lab server

Do tasks **in order**. Take the first task whose status is `TODO`. Gates do **not** block (fast-track mode, see below).
Protocol and report format: see COLLAB.md.

Statuses: `TODO` · `IN-PROGRESS` · `DONE` · `BLOCKED` (say why in COLLAB.md) · `SKIPPED` (only when approved)

Fixed inputs: `config/experiment.yaml` and `prompts/templates.md`. Code goes in `src/vmod/`, tests in `tests/`.

**Deadline (updated 2026-11-14):** paper due Nov 18. **All experiments and analysis (T00-T14) must be done by end of Nov 15.**

| By | Milestone |
|---|---|
| Nov 14 evening | T00-T05 done (setup, data, images, scorers) |
| Nov 15 morning | T06-T07b done (runner, pilot, replication check) |
| Nov 15 afternoon | T08 done (main runs) |
| Nov 15 night | T10-T14 done (scoring, analysis, summary) |

**Fast-track mode:** at each gate, post the gate report in COLLAB.md and **continue immediately**, applying the decision
rules written at the gate. Stop only if a PLANNER or OWNER message says `STOP`. Check COLLAB.md (`git pull`) at least
at the start of every task. If a step is eating time (more than 45 min stuck), take the stated fallback or post `BLOCKED`
and move on to the next task that doesn't depend on it.

---

## Phase 1: setup and data

### T00 Environment check: `DONE`
- Report: GPU model, count and memory (`nvidia-smi`), driver/CUDA version, Python version, free disk space, HF cache path.
- Check internet access to Hugging Face and GitHub, and whether `HF_TOKEN` is set (Gemma models are gated).
- Create a Python venv. Install vLLM (a version that supports the models in the config), `transformers`, `datasets`, `pillow`, `pandas`, `scipy`, `statsmodels`, `matplotlib`, `pyyaml`, `rapidfuzz`, `pytest`. Save `pip freeze` to `env/requirements.lock.txt`.
- Check that the DejaVu Sans Mono font file exists. Install it if it doesn't, and record its path.
- For each model in `config.models.local`: confirm it exists on HF and that vLLM supports it. Estimate whether it fits (and with what tensor-parallel size). Report a table: model, available (y/n), fits (y/n), TP size, notes. If a newer generation of a family is clearly better supported, say so, but do not switch without approval.
- **Done when:** the env report is in COLLAB.md and the lock file is committed.

### T01 Code skeleton: `DONE`
- `src/vmod/config.py` loads `config/experiment.yaml`. Add a CLI entry point `python -m vmod <command>` with subcommands for the later tasks (`prepare`, `render`, `selftest`, `run`, `score`, `analyze`).
- Every output file records `study_id`, git commit hash and UTC timestamp.
- **Done when:** `python -m vmod --help` works and `pytest` passes.

### T02 Download datasets: `DONE`
- Download CRUXEval, GSM8K test and WikiTableQuestions test, as named in the config.
- **Fallback for WTQ:** if neither the HF loader nor the GitHub zip works within 30 min, post `QUESTION` and continue with code and math; tables get added when resolved.
- Write `data/MANIFEST.md`: source URL, version/commit hash or file sha256, license, total item count.
- **Done when:** the manifest is committed and the licenses are listed in the report. Flag any license that forbids this use.

### T03 Build items (`vmod prepare`): `DONE`
- Build the canonical content string for each item exactly as in `prompts/templates.md`.
- Apply the exclusion rules from the config before sampling. Log every exclusion to `data/exclusions.csv` (item_id, content_type, reason).
- Sample with seed 630: a **pilot** set (`pilot_per_content`) and a **main** set (`main_per_content`) per content type, with no overlap.
- Write `data/items/{pilot,main}_{code,math,table}.jsonl`. Fields: `item_id, content_type, content, gold, n_chars, n_lines, n_table_rows (table only), source_index`.
- Gold answers:
  - **code:** CRUXEval `output`
  - **math:** the number after `####` in GSM8K
  - **table:** the WTQ target value list
- **Done when:** the files are committed and the report shows counts before and after exclusion, by reason.

### T04 Render images (`vmod render`): `DONE`
- Render each item's `content` to PNG with exactly the `render` settings: monospace font, no wrapping, black on white, size = text extent + padding.
- Save to `data/images/` (git-ignored). Write `data/images_manifest.csv`: item_id, width, height, sha256.
- Check that rendering is deterministic: re-render 20 items and confirm the sha256 values match.
- Commit `reports/render_samples/`: 4 random images per content type, plus the largest image per content type.
- **Done when:** the samples and manifest are committed and the report gives min/median/max image size per content type.

### T05 Prompts, parser and scorers (`vmod selftest`): `DONE`
- Build prompts exactly from `prompts/templates.md`.
- **Parser:** use the LAST line containing `Final answer:`. Strip markdown, quotes around the whole answer, and trailing periods. No marker → `parse_ok=false`, and the item counts as incorrect.
- **Scorers:**
  - **code:** in a subprocess with a 5 s timeout and no network, `eval(pred) == eval(gold)`. If `pred` isn't a valid literal, it counts as incorrect.
  - **math:** remove `,`, `$` and spaces, then numeric equality with tolerance 1e-6.
  - **table:** WTQ official denotation match. Normalize case and whitespace, and compare numbers numerically. Multi-answer lists split on `|` and compare as sets.
- **Transcription (C only):** extract the text between `<transcription>` tags. `transcription_exact` = equal after collapsing all whitespace runs to one space and stripping. `cer` = normalized character Levenshtein distance against `content`.
- **Self-test:**
  - Feed `"...\nFinal answer: {gold}"` for every pilot and main item. All must score correct; report any failures.
  - Feed 20 hand-made wrong or unparseable answers. All must score incorrect.
  - Add unit tests for the parser and each scorer.
- **Done when:** the self-test passes at 100% and the tests are committed.

### GATE G1 (non-blocking): post report, then continue
Post the render sample paths, exclusion counts and self-test result. The PLANNER reviews in parallel and may post `STOP`.
The self-test must be 100% before continuing; that one is a hard requirement.

---

## Phase 2: runs

### T06 Inference runner (`vmod run --model <id> --set {pilot,main}`): `DONE`
- Use vLLM offline batch mode, one model at a time, with all 3 conditions. Use the model's own chat template, with the image placed before the text for B and C. Decoding exactly per the config.
- **Image resolution:** make sure the processor does **not** downscale our images. For example, raise Qwen `max_pixels` to cover the largest image. Record the effective resolution settings per model. If a model must downscale, report it; don't hide it.
- **Output:** `results/raw/{set}/{model_slug}.jsonl`, one row per (item, condition). Fields: `item_id, content_type, condition, model_id, model_revision (HF commit sha), prompt_sha256, image_sha256, response, input_tokens, output_tokens, finish_reason, started_utc, gen_seconds`.
- The runner must be resumable: skip any (item, condition) already written. Log items that exceed the context window to `results/raw/{set}/{model_slug}.skipped.csv`. Do not re-sample them.
- **Done when:** a smoke run of 5 items × 3 conditions on the smallest model works end to end, through scoring.

### T07 Pilot: `DONE`
- Run the **pilot** set on every local model marked available and fitting in T00.
- Report a table per model with:
  - parse rate per condition
  - accuracy per content × condition
  - mean output tokens
  - % `finish_reason=length`
  - seconds per 100 prompts
  - errors
- Estimate the total main-run time for N=500 and N=300.
- Show 3 raw responses per condition from one model, so the PLANNER can check the prompts work.
- **Done when:** the report is posted and `results/raw/pilot/` is committed.

### T07b Replication check: repeat runs: `DONE`
Purpose: show that one run per item is enough. This supports the claim that the unit of replication is the item, and that run-to-run noise is negligible next to the condition effect (conclusion validity).
- Re-run the **whole pilot set** (all items × 3 conditions) a **second time** on every model kept at T07. Use identical settings: same config, prompts, images and vLLM version, but a **fresh process** and a **different batch order** (shuffle with seed 631). Write to `results/raw/pilot_rep2/{model_slug}.jsonl`, same schema.
- Score both runs with the T05 scorers.
- For each model × condition, report:
  - % identical response text
  - % agreement on `correct` (0/1)
  - Cohen's kappa for `correct` across the two runs
  - accuracy in run 1 vs run 2
  - the largest absolute accuracy difference across all cells
- Save `results/analysis/replication_check.csv`.
- **Decision rule (pre-registered):**
  - If `correct` agreement is at least 95% in every model × condition cell, the main runs stay at one run per item.
  - If any cell is below 95%, post the numbers and **still continue with one run per item**, because there isn't time for more. Flag it as a conclusion-validity threat in `reports/summary.md`.
- **Done when:** the CSV is committed and the table is in COLLAB.md.

### GATE G2 (non-blocking): apply these rules, freeze, continue
Pre-registered decision rules:
1. **Models:** keep a model if it ran the pilot without crashes and its parse rate is at least 80% in every condition. Otherwise drop it and report why.
2. **N:** keep `main_per_content: 500` if the estimated main-run wall time for all kept models is 8 hours or less. Otherwise set it to 300.
3. **max_new_tokens:** if any kept model has more than 5% `finish_reason=length` in any cell, raise it to 4096 for **all** models (never per model). Re-check rule 2 with the new estimate.

Apply the rules, commit the config change, create the tag `config-frozen-v1`, post the decisions in COLLAB.md, and start T08. After the tag, the config and prompts must not change.

### T08 Main runs, local models: `DONE`
- Run the **main** set for each model kept at G2, smallest first. Start the analysis tasks (T10-T12) on finished models while the larger ones run, if a spare GPU allows it.
- After each model:
  - Check integrity: every main item × 3 conditions appears exactly once, or is in the skipped list.
  - Commit `results/raw/main/{model_slug}.jsonl.gz`.
  - Post a short report: accuracy per content × condition, parse rate, wall time.
- **Done when:** all approved models are complete.

### T09 Main runs, API models: `SKIPPED` (needs OWNER approval)
- Do this only if the OWNER posts the approved model IDs and budget, and has set the API keys as environment variables on the server. Never write keys to files or commits.
- Same items, prompts and output schema as T08, with temperature 0. Log the exact model version string returned by the API, and the cost per model. Retry with backoff; never re-sample items.
- Stop and report if spending reaches 80% of the budget.
- If no approval is posted by the time T08 is done, mark this task SKIPPED and continue. (Default under fast-track: SKIPPED.)

---

## Phase 3: scoring and analysis

Outputs are numbers, tables and figures only. **Do not write paper prose.**

### T10 Score everything (`vmod score`): `DONE`
- Produce `results/scored/main_all.csv.gz`: all raw fields plus `pred, parse_ok, correct, transcription, transcription_exact, cer`.
- Report the parse rate per model × condition.
- Hand-check 30 random rows (10 per content type): does the scorer agree with a careful reading? Report any disagreements.

### T11 Descriptive statistics: `DONE`
- `results/analysis/descriptives.csv`: per model × content × condition, give n, accuracy, and the 95% Wilson CI.
- Output tokens per cell: mean, median, SD, IQR, min, max.
- Input length per content type, as chars and lines.
- **Figures** (`results/figures/`, PNG and PDF):
  - accuracy by condition, faceted by content type, one line per model
  - box plots of output tokens per condition, to show outliers
  - accuracy gap (A−B) vs model size for the Qwen family
- Outliers: list responses with output tokens above Q3 + 3·IQR, or with finish_reason=length. Do not drop them; report counts.

### T12 RQ1: modality effect: `DONE`
- For each model × content type, use a paired 2×2 table A vs B on the same items. Run McNemar's test (exact binomial on the discordant pairs).
- Report:
  - b (A correct, B wrong) and c (A wrong, B correct)
  - the accuracy difference with a 95% CI (Newcombe paired method)
  - the discordant odds ratio b/c with a 95% CI
- Apply the Holm correction across all model × content tests. Give raw and adjusted p-values.
- Repeat for A vs C and B vs C, as separate Holm families.
- Run Cochran's Q across A/B/C per model × content.
- **Sensitivity check:** exclude unparseable responses and re-run the tests.
- Output `results/analysis/rq1_*.csv`.
- Mixed-effects logistic model (correct ~ condition × content + condition × model + (1 | item)): only if the OWNER posts `GLMM OK`, and only after everything else in T12-T14 is done.
  - **GLMM: `DONE`** 2026-11-16 after `GLMM OK` (results/analysis/glmm_*.csv, deviation #24).

### T13 RQ2: perception vs reasoning: `DONE`
- From condition C, report the transcription exact-match rate and CER distribution per model × content.
- On items with `transcription_exact=true`, compare A vs C with McNemar. On items with an incorrect transcription, compare A vs C again. Report the gap in each subset.
- Run a logistic regression: correct in B ~ CER from C, per content type, pooled across models, with model as a fixed effect.
- **Sensitivity check:** repeat with the CER ≤ 0.02 threshold.
- Output `results/analysis/rq2_*.csv`.

### T14 RQ3, error sample and wrap-up: `DONE`
- Run the Wilcoxon signed-rank test on output tokens A vs B per model × content (paired by item), with Holm correction. Report the median difference.
- **Error sample:** export `results/coding/error_sample.csv` for manual coding. Take 100 random flips per content type where A was correct and B wrong, across models, with seed 630. Columns: content, gold, response A, response B, transcription (if any), and empty `code` and `coder` columns. **The OWNER does the coding.** The RUNNER only exports the file.
- Write `reports/summary.md`, numbers only (include the T07b replication-check table):
  - every table
  - exclusion counts by reason
  - final model list with revisions
  - package versions
  - total GPU hours
  - any deviation from the plan
- Commit everything and post `ALL DONE` in COLLAB.md.

---

## Phase 4: replication runs and extension models (added 2026-11-15)

**Time budget:** 16 hours of wall time from when T15 starts. Hard stop at that point: finish the current run, then go straight to T18 with whatever is complete. Partial results are fine. Never leave a model with only part of a run.

**Rules:**
- Use the frozen `config-frozen-v1` settings for everything: items, prompts, rendering, decoding (max_new_tokens 4096), scorers and parser. Extra runs and models are listed in `config/extension.yaml`. Do not edit `experiment.yaml` or the prompts.
- The **primary analysis stays as it is**: run 1 of the 5 primary models. Phase 4 adds a replication analysis and an exploratory extension. It never replaces or overwrites run 1.
- Output paths: `results/raw/main_run{2,3}/` for replicates and `results/raw/ext/run{1,2,3}/` for extension models. Same schema, plus a `run` column.
- Post progress in COLLAB.md after every completed model-run, with accuracy per content × condition and wall time. Analyze as you go; don't wait until the end.

### T15 Full replicate runs 2 and 3, primary models: `DONE`
- Run the main set again for all 5 primary models, twice: run 2 with order seed 631 and run 3 with seed 632. Each run uses a fresh process. Keep the same model revisions as run 1 and check them against `reports/summary.md`.
- Integrity check per run, the same as T08.
- **Done when:** 10 model-runs are committed (`.jsonl.gz`).

### T16 Replication analysis: `DONE`
For the 5 primary models, using runs 1-3:
- Per model × content × condition: accuracy in each run, the mean, SD and range across runs.
- Item-level stability: Fleiss' kappa on `correct` across the 3 runs, % of items correct in all 3, in none, or mixed.
- **Key table:** for each run separately, the RQ1 A vs B McNemar results with Holm correction (15 tests). Show which cells are significant in run 1, run 2 and run 3, and whether the direction and significance agree across runs. Do the same for A vs C.
- **Sensitivity:**
  - **Majority vote:** an item counts as correct if it was correct in at least 2 of 3 runs. Re-run the RQ1 McNemar tests and Holm correction on that.
  - **Mean accuracy:** a paired permutation test on per-item mean correctness (A vs B), 10,000 permutations, seed 630.
- Re-run RQ2 (A vs C split by transcription correctness, primary and CER ≤ 0.02 rules) on runs 2 and 3, and report whether the code-content pattern holds.
- **Output:** `results/analysis/replication_full_*.csv` and a figure: accuracy per cell, with the 3 runs as dots.

### T17 Extension models: `DONE`
Work through `config/extension.yaml → extension_models` in priority order until the time budget runs out. For each model:
1. Check availability and fit within 2 GPUs. If the model is gated or unavailable, report it and skip it.
2. Run the pilot set (270 requests). Apply G2 rule 1: keep the model only if the parse rate is at least 80% in every condition. Rule 3 can't change max_new_tokens now (it's frozen at 4096), so only report the % of `finish_reason=length`. Record the effective image resolution handling, as in T06.
3. Do main runs 1, 2 and 3 (order seeds 630/631/632), with integrity checks.
4. Score the runs, and post a short report per model.
- Order runs to make good use of 2 GPUs: TP=1 models in parallel lanes, and TP=2 models (gemma-27b, 72B-AWQ) alone.
- **Done when:** all extension models are done or skipped, or the time budget has run out. List which models finished.

### T18 Extended analysis and summary update: `DONE`
- **Extension models, run 1:** the same descriptives, RQ1 (with its **own** Holm family, labeled *exploratory*), RQ2 and RQ3 as T11-T14. Then the same 3-run replication table as T16.
- **Combined figure:** A−B gap per content type for all models (primary and extension visually distinguished), with 95% CIs. Also a gap-vs-size figure per family (Qwen2.5: 3/7/32/72; Gemma: 12/27).
- **Resolution check:** compare the A−B code gap for models that resize images (Gemma, InternVL) with those that use native resolution (Qwen), in a table. This is descriptive only; family is a confound, so note that.
- Update `reports/summary.md`, keeping the earlier sections unchanged and adding a "Phase 4" section. Update `reports/deviations.md`: models were added after the primary results were seen, and 72B is quantized.
- Write `reports/paper_numbers.md`: a compact index of every number and table the paper will need (RQ1, RQ2, RQ3, replication, extension), each with its source CSV path. **Numbers only. No paper prose.**
- Post `PHASE 4 DONE`.
