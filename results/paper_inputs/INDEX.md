# Paper inputs: index

Collected 2026-11-16 from the repo, the logs and the lab server.
- No model inference was run.
- No existing file in `results/raw`, `results/scored`, `results/analysis` or `results/figures` was modified.
- Helper scripts are in `_scripts/`.

| # | task | status | file(s) |
|---|---|---|---|
| 1 | GPU-hours and hardware | DONE | `compute.md`: 44 model-runs, **22.59 GPU-h**; 4 × RTX PRO 5000 Blackwell 48 GB, GPU 0-1 used. Wall time includes model load |
| 2 | Code identity across runs | DONE | `code_identity.md`: `VERDICT: changed (see above)`. Prompts and images are byte-identical across all 30 non-pilot runs, and decoding is identical; the runner gained Phase 4 options, `gpu_memory_utilization` went 0.90 → 0.80, and pilot used max_new_tokens 2048 |
| 3 | Rendering settings, sizes, determinism, samples | DONE | `rendering.md`, `render_samples/{code,math,table}.png`; 20/20 re-renders byte-identical |
| 4 | Pools, exclusions, sampling | DONE | `exclusions.md`; the 32% WTQ figure is confirmed (1,396 / 4,344 = 32.1%); pilot ∩ main = 0 |
| 5 | Package versions | DONE | `environment.md`; one environment for all runs, identical to the T00 lock (vLLM 0.33.0, torch 2.14.0, transformers 5.20.2) |
| 6 | Frozen prompt templates | DONE | `prompts.md`: 9 templates and a rendered Qwen chat example. Note: the Qwen and InternVL chat templates add a default system prompt |
| 7 | Analysis specifications | DONE | `analysis_specs.md` |
| 8 | Deviations and decisions | PARTIAL | `deviations_and_decisions.md`. The reason the API models were dropped is NOT FOUND beyond "skipped by default, no OWNER approval"; the author will supply it. No pre-registration file exists |
| 9 | Input-length moderator | DONE | `input_length.md`; `scripts/analysis/input_length.py`; `results/analysis/input_length_gap_by_tercile.csv`, `results/analysis/input_length_interaction.csv`, `results/figures/input_length_gap.{pdf,png}` |
| 10 | Error-coding preparation (no coding done) | DONE | `error_coding_prep.md`; no codebook existed, so a draft is at `results/coding/codebook_draft.md` |
| 11 | Transcription anomalies | DONE | `transcription_anomalies.md` |
| 12 | Repo, commits, citation commit | DONE | `repo.md`; public GitHub repo; `reports/paper_numbers.md` should cite **`6e1d795`** |
