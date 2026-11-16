# Analysis specifications (from the code)

All paths are relative to the repo root, and line numbers are for commit `6e1d795`. The shared statistical helpers are in `src/vmod/analyze.py`:

- `holm` (line 72): Holm step-down adjustment.
- `mcnemar_exact` (line 86): exact two-sided binomial test on the discordant pairs, `stats.binomtest(min(b, c), b + c, 0.5)`, with p = 1 when b + c = 0.
- `newcombe_paired` (line 93): Newcombe (1998) method-10 CI for a paired difference in proportions.
- `discordant_or` (line 111): odds ratio b/c on the discordant pairs.
- `mcnemar_family` (line 281): one row per model × content cell, then Holm over all rows of the call.

## 1. RQ2 logistic regression (`rq2_logit_B_on_cer.csv`)

`src/vmod/analyze.py`, `rq2()`, lines 389-410:

- **Data:** condition-B correctness merged with the condition-C transcription CER of the same model × item. Fit separately for each content type, pooled over the 5 primary models, run 1.
- **Formulas** (`statsmodels.formula.api.logit`, line 401):
  - `y ~ cer + model_id`: primary; `cer` is the continuous CER.
  - `y ~ cer_gt_002 + model_id`: sensitivity, a 0/1 indicator for CER > 0.02.
  - `y ~ cer_c + model_id`: sensitivity, CER capped at 1.0.
- **Model fixed effects:** yes, `model_id` enters as a categorical fixed effect.
- **Standard errors:** the default maximum-likelihood (inverse-Hessian) SEs, `.fit(disp=0, maxiter=200)`. There is **no clustering**: no `cov_type` argument anywhere in the code (`grep -n "cov_type\|cluster" src/vmod/*.py` finds nothing).
- **Missing transcriptions:** a missing transcription is scored against the empty string, so CER = 1 (`transcription_metrics`).

## 2. GLMM (`glmm_*.csv`)

`src/vmod/glmm.py`, added 2026-11-16 after the OWNER posted `GLMM OK`.

- **Formula** (line 24): `correct ~ condition * content_type + condition * model + (1 | item_id)`, binomial with logit link.
  - Treatment coding with reference levels `A_text`, `code` and `Qwen2.5-VL-7B`.
  - Fixed terms: intercept, condition (2), content (2), model (4), condition:content (4), condition:model (8). That is 21 fixed parameters plus the item SD.
- **No three-way term:** condition × content × model is **not** included, as in the T12 specification in TASKS.md.
- **Estimation:** written in-house, not a package's GLMM routine.
  - `GHGLMM` (lines 39-81) computes the exact marginal likelihood. The item random intercept is integrated out with **Gauss-Hermite quadrature, 40 nodes** (`numpy.polynomial.hermite_e.hermegauss`). Each item's 15 responses (5 models × 3 conditions) share one intercept.
  - The likelihood is maximised with `scipy.optimize.minimize` (L-BFGS-B, analytic gradient). The gradient was checked against finite differences: maximum absolute difference 1.4e-6.
  - SEs come from the numerical Hessian of the analytic gradient (observed information).
  - The reason for writing it: there is no R on the server, and statsmodels has only a variational-Bayes approximation.
- **Checks** (`glmm_checks.csv`):
  - 80 quadrature nodes: maximum coefficient difference 0.009.
  - `statsmodels.genmod.bayes_mixed_glm.BinomialBayesMixedGLM.fit_vb`: maximum difference 0.038.
- **Likelihood-ratio tests** (`glmm_lrt.csv`): each against a reduced model fit the same way. The reduced models drop condition:model, drop condition:content, or drop all condition terms.
- **Cell contrasts** (`cell_contrasts`, line 112): the A−B and A−C log-odds per model × content at item intercept = 0, with delta-method SEs. Holm is applied over the 15 cells per comparison per run.
- **Data:** run 1 is primary. Runs 2 and 3 are refit the same way.

## 3. Outlier rule (`outliers.csv`, `outlier_counts.csv`)

`src/vmod/analyze.py`, `descriptives()`, lines 184-195: within each **model × content type × condition** cell, a response is an outlier if

- `outlier_tokens`: `output_tokens > Q3 + 3 × (Q3 − Q1)`, where Q1 and Q3 are the 25th and 75th percentiles (`pandas.Series.quantile`) of output tokens in that cell. So **k = 3**.
- `outlier_length`: `finish_reason == "length"`, meaning the 4,096-token cap was hit.

`outliers.csv` lists every response that meets either rule. `outlier_counts.csv` counts both per cell. Outliers are **reported only, never excluded**.

## 4. CER and transcription exactness

`src/vmod/scoring.py`:

- **Extraction**, `extract_transcription_src` (line 192), in order:
  1. text between `<transcription>` and `</transcription>`;
  2. if the tag is never closed, the rest of the response after `<transcription>`;
  3. a code fence after a "Transcription" heading line;
  4. otherwise none.
- **Fence stripping:** `strip_fence` (line 212) then removes a markdown code fence that wraps the whole transcription.
- **Metrics**, `transcription_metrics` (line 235). `t` is the extracted transcription (the empty string if missing); `c` is the item's canonical content string.
  - `ws_norm` (line 224): `" ".join(s.split())`, which collapses every whitespace run, including newlines, to one space and strips the ends. **Case is preserved; nothing else is changed.**
  - **exact**: `ws_norm(t) == ws_norm(c)`.
  - **exact_lenient** (sensitivity, deviation #15): `lenient_norm(t) == lenient_norm(c)`. `lenient_norm` (line 228) applies `ws_norm`, removes spaces around `|`, and collapses runs of 2+ `-` to one `-`, so table column padding and rule width don't count.
  - **cer** (primary): `Levenshtein.distance(ws_norm(t), ws_norm(c)) / max(1, len(ws_norm(c)))`, using `rapidfuzz.distance.Levenshtein`. The denominator is the length of the **whitespace-normalised reference**. CER can exceed 1 when the transcription is much longer than the reference.
  - **cer_raw**: the same on the raw strings, `Levenshtein.distance(t.strip("\n"), c) / max(1, len(c))`.
- **"Correct transcription" for the RQ2 splits:** `exact` (primary) or `cer ≤ 0.02` (sensitivity).

## 5. Answer parsers

`src/vmod/scoring.py`. Both parsers look for the **last** line containing the marker `Final answer:` (case-insensitive, optional `**` or `__` around it; `_MARKER_RE`, line 38).

- **Strict** `parse_answer_strict` (line 80):
  - The answer must be on the marker line, after the marker.
  - It is then cleaned by `_finish`/`_strip_md`, which removes `**`, `__`, `` ` `` and `*` wrappers at the edges, `$…$`, `\boxed{}`, `\text{}`, `\[ \]` and a trailing period.
  - For math and table only, it removes one pair of matching outer quotes. Code keeps its quotes, since they are part of the Python literal.
- **Relaxed/primary** `parse_answer` (line 90):
  - It also accepts a bare heading as the marker (`### Final Answer`, `**Final Answer**`, colon optional; `_HEADING_RE`, line 40).
  - If nothing follows the marker on its line, the answer is the next non-empty block of lines, with code fences and `\[`, `\]`, `$$` lines skipped (`_following_block`, line 51).
  - Whenever the strict parser succeeds, the relaxed parser returns the identical prediction.
- **Which is used where:**
  - The **relaxed parser is the primary parser for every model, content type and condition** (`score_df`, `src/vmod/score.py` line 38: `parse_answer`).
  - The strict parser is used only for sensitivity: column `parse_ok_strict`, `correct_strict = correct & parse_ok_strict` (score.py line 58), and `rq1_*_sens_strict_parser.csv`.
- **Scoring after parsing:**
  - code: `eval(pred) == eval(gold)` in a sandboxed subprocess (empty builtins, no network, 2 GB, 5 s per item; `score_code_batch`, line 131).
  - math: numeric equality after removing `,`, `$` and spaces, tolerance 1e-6 (`score_math`, line 164).
  - table: the official WTQ denotation match (`score_table`, line 172, `src/vmod/wtq_eval.py`). Multiple answers are split on `|`.

## 6. Leading-fence sensitivity (`*_sens_leading_fence*`)

`src/vmod/sens_leading_fence.py`, approved by the OWNER on 2026-11-16.

- **What it adds:** one fallback to transcription extraction, applied **only** to condition-C responses where the frozen extractor found nothing (`transcription_source == "none"`).
- **The rule:** if the response begins, after whitespace, with a ``` code fence, the fence body becomes the transcription, with source `leading_fence` (`LEADING_FENCE`, line 26; `apply_rule`, line 44).
- **Metrics:** recomputed with the frozen `transcription_metrics`.
- **What it does not change:** primary scored files and primary analysis CSVs are untouched; every output has the `_sens_leading_fence` suffix.
- **Responses recovered:**
  - InternVL3.5-8B code: 466-469 per run.
  - gemma-3-12b code: 312-323 per run.
  - gemma-3-12b table: 35-41 per run.
  - No other model or cell (`sens_leading_fence_recovered.csv`).

## 7. Holm families

Every family is one call of `holm()` and applies **within one run**.

| analysis | family | source |
|---|---|---|
| RQ1 McNemar A vs B, A vs C, B vs C (run 1) | each comparison separately: 15 cells (5 models × 3 content types) | `rq1()`, analyze.py:301; one `mcnemar_family` call per comparison |
| RQ1 sensitivities (parseable-only, strict parser) | same 15-cell family per comparison, per sensitivity | `rq1()` |
| Cochran's Q (A/B/C) | 15 cells | `rq1()` |
| RQ2 A vs C split by transcription correctness | per subset rule (exact, cer_le_0.02, exact_lenient, exact_tags_only): 30 rows (15 cells × correct/wrong). For tables under `exact`, the "correct" subset is empty, so the family is smaller | `rq2()`, `p_holm_within_rule` |
| RQ3 Wilcoxon output tokens A vs B | 15 cells | `rq3()`, analyze.py:414 |
| Replication, per run | A vs B and A vs C each: 15 cells per run (one family per run) | `per_run_mcnemar`, replication.py:73 |
| Replication majority vote | 15 cells per comparison | `main()` in replication.py |
| Replication permutation test | 15 cells | `permutation_mean`, replication.py:104 |
| Replication RQ2 split | per run × subset rule | `rq2_split`, replication.py:140 |
| Extension models (exploratory) | their own families: 12 cells (4 models × 3 content types) per comparison. The OWNER plan's 6-cell family (Gemma-27B + Qwen-72B only) is in `ext_rq1_A_vs_B_family6.csv` | `ext_t11_t14` (ext_analysis.py); `plan_tables.ext_family6` |
| Resolution control | 9 cells (3 arms × 3 content types) for B-original vs B-control; separately 18 rows for the A−B gap under each setting | `plan_tables.res_b_vs_b` |
| GLMM cell contrasts | 15 cells per comparison per run | `glmm.cell_contrasts` |

## 8. Majority vote (replication)

`src/vmod/replication.py`, `majority_vote()` (line 97):

- For each model × content × item × condition, sum `correct` over runs 1-3, keeping only keys present in all 3 runs.
- `correct_mv = (sum ≥ 2)`, i.e. correct in at least 2 of 3 runs.
- The McNemar family (`mcnemar_family`, Holm over 15) is then run on these majority-vote outcomes.

Related: `permutation_mean` (line 104) is a paired sign-flip permutation test on per-item **mean** correctness across the 3 runs (A − B), with 10,000 permutations, seed 630, two-sided, p = (#|perm| ≥ |obs| + 1)/(n_perm + 1).
