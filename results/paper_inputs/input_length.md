# Input-length moderator (primary 5 models)

**Script:** `scripts/analysis/input_length.py`.

**Outputs:**
- `results/analysis/input_length_gap_by_tercile.csv`
- `results/analysis/input_length_interaction.csv`
- `results/figures/input_length_gap.{pdf,png}`

These are new files. The existing `input_length.csv` and `ext_input_length.csv` were not touched.

## Definitions

- **Length:** `n_chars` = number of characters in the item's canonical content string (`data/items/main_*.jsonl`, written by `prepare.py`). `n_lines` is reported too.
- **Terciles:** computed within each content type over the 500 main items, using `pd.qcut` on the rank of `n_chars`. Tied lengths at a boundary are split by item order, so groups are 167/166/167.
- **Regression:** `z_log_length` = z-score of log(`n_chars`) within each content type. For each content type and run, conditions A and B only, all 5 models pooled:
  - model: `correct ~ condition * z_log_length + model`, logit (statsmodels);
  - SEs clustered by item (`cov_type="cluster"`);
  - n = 5,000 responses (500 items × 5 models × 2 conditions); all fits converged.
- **Reading the interaction:** `condition[B]:z_log_length` is the change in the B-vs-A log-odds per 1 SD of log length. A negative value means image accuracy falls further behind text as items get longer.

## (b, c) Interaction condition[B] × z_log_length

| content | run | coef | SE (cluster item) | p | OR [95% CI] |
|---|---|---|---|---|---|
| code | 1 | 0.074 | 0.043 | 0.0842 | 1.077 [0.990, 1.171] |
| code | 2 | 0.111 | 0.041 | 0.0068 | 1.117 [1.031, 1.211] |
| code | 3 | 0.101 | 0.046 | 0.0290 | 1.106 [1.010, 1.211] |
| math | 1 | 0.031 | 0.062 | 0.6166 | 1.031 [0.914, 1.164] |
| math | 2 | 0.112 | 0.064 | 0.0793 | 1.119 [0.987, 1.268] |
| math | 3 | 0.072 | 0.065 | 0.2691 | 1.074 [0.946, 1.220] |
| table | 1 | -0.183 | 0.052 | 0.0004 | 0.833 [0.752, 0.922] |
| table | 2 | -0.157 | 0.050 | 0.0016 | 0.855 [0.776, 0.943] |
| table | 3 | -0.203 | 0.049 | 0.0000 | 0.816 [0.742, 0.898] |

## (a) A−B accuracy gap by length tercile, run 1 (n = 166-167 items per cell)

| content | model | short | middle | long |
|---|---|---|---|---|
| code | InternVL3-8B | +0.126 | +0.090 | +0.162 |
| code | Qwen2.5-VL-32B-Instruct | +0.072 | +0.108 | +0.066 |
| code | Qwen2.5-VL-3B-Instruct | +0.078 | +0.030 | +0.024 |
| code | Qwen2.5-VL-7B-Instruct | +0.048 | +0.042 | +0.012 |
| code | gemma-3-12b-it | +0.204 | +0.205 | +0.174 |
| math | InternVL3-8B | +0.042 | +0.048 | +0.078 |
| math | Qwen2.5-VL-32B-Instruct | +0.030 | -0.006 | +0.024 |
| math | Qwen2.5-VL-3B-Instruct | +0.000 | +0.054 | +0.012 |
| math | Qwen2.5-VL-7B-Instruct | +0.000 | -0.012 | +0.012 |
| math | gemma-3-12b-it | +0.006 | +0.036 | +0.000 |
| table | InternVL3-8B | +0.018 | +0.060 | +0.102 |
| table | Qwen2.5-VL-32B-Instruct | -0.018 | -0.018 | +0.090 |
| table | Qwen2.5-VL-3B-Instruct | -0.120 | +0.030 | +0.012 |
| table | Qwen2.5-VL-7B-Instruct | -0.030 | -0.042 | -0.042 |
| table | gemma-3-12b-it | +0.012 | +0.054 | +0.192 |

Tercile character ranges (min / median / max):

| content | short | middle | long |
|---|---|---|---|
| code | 72 / 101 / 140 | 140 / 166 / 195 | 195 / 231 / 296 |
| math | 83 / 148 / 179 | 180 / 215 / 257 | 257 / 313 / 694 |
| table | 474 / 889 / 1140 | 1141 / 1452.5 / 1973 | 2006 / 2488 / 5880 |

## Key numbers

- **Tables:** the B × length interaction is negative and significant in all 3 runs: OR 0.83 / 0.86 / 0.82 per SD of log length, p ≤ .002. Image accuracy falls behind text more on longer tables.
  - Gemma-12B table gap: +.012 (short) → +.192 (long).
  - InternVL3 table gap: +.018 → +.102.
  - Qwen-32B table gap: −.018 → +.090.
- **Code:** the interaction is positive: B gets relatively *better* with length. It is not significant in run 1 (p = .084) and is significant in runs 2 and 3 (p = .007, .029).
- **Math:** no interaction in any run (p ≥ .08).
- **Caveats:**
  - These are pooled-model logits with model fixed effects. A model-specific slope is not estimated.
  - p-values are not adjusted across the 9 fits.
  - In this repo, only the input-length **descriptives** are planned (`TASKS.md:159`: "Input length per content type, as chars and lines.", in `results/analysis/input_length.csv`). The moderator **test** is not in `TASKS.md`, `config/experiment.yaml` or `README.md`. If the paper's design section plans it, that plan is outside the repo. This analysis was run on 2026-11-16, after the primary results were known.
