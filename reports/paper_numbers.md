# Paper numbers index

<!--
study_id: vlm-modality-v1
git_commit: ddde07f9da5a086ca48c0917f3cd2ab51e488bf0-dirty
created_utc: 2026-11-16T18:23:34Z
-->

Numbers and tables only. Each block names its source CSV. Full tables: `reports/summary.md`.

## Design and data

- primary models: 5; items per content type: 500; responses (run 1): 22500 — source: `results/analysis/descriptives.csv`

input length — source: `results/analysis/input_length.csv`

| content_type | n_items | chars_mean | chars_median | chars_min | chars_max | lines_mean | lines_median | lines_min | lines_max |
|---|---|---|---|---|---|---|---|---|---|
| code | 500 | 169.4 | 166.0 | 72 | 296 | 7.5 | 7 | 4 | 14 |
| math | 500 | 233.3 | 215.0 | 83 | 694 | 3.4 | 3 | 2 | 9 |
| table | 500 | 1735.3 | 1452.5 | 474 | 5880 | 20.4 | 18 | 10 | 45 |

- exclusions and sampling: `data/items/summary.json`; deviations: `reports/deviations.md`

## RQ1 modality effect (primary: run 1, 5 models, Holm within family of 15)

### Accuracy per cell (95% Wilson CI in source)
source: `results/analysis/descriptives.csv`

| model_id | content_type | A_text | B_image | C_image_transcribe |
|---|---|---|---|---|
| InternVL3-8B | code | 0.632 | 0.506 | 0.522 |
| InternVL3-8B | math | 0.920 | 0.864 | 0.894 |
| InternVL3-8B | table | 0.648 | 0.588 | 0.628 |
| Qwen2.5-VL-32B | code | 0.812 | 0.730 | 0.740 |
| Qwen2.5-VL-32B | math | 0.918 | 0.902 | 0.948 |
| Qwen2.5-VL-32B | table | 0.812 | 0.794 | 0.806 |
| Qwen2.5-VL-3B | code | 0.386 | 0.342 | 0.358 |
| Qwen2.5-VL-3B | math | 0.840 | 0.818 | 0.752 |
| Qwen2.5-VL-3B | table | 0.428 | 0.454 | 0.392 |
| Qwen2.5-VL-7B | code | 0.524 | 0.490 | 0.480 |
| Qwen2.5-VL-7B | math | 0.868 | 0.868 | 0.866 |
| Qwen2.5-VL-7B | table | 0.626 | 0.664 | 0.668 |
| gemma-3-12b | code | 0.688 | 0.494 | 0.542 |
| gemma-3-12b | math | 0.948 | 0.934 | 0.922 |
| gemma-3-12b | table | 0.734 | 0.648 | 0.726 |

### A (text) vs B (image), McNemar exact
source: `results/analysis/rq1_A_vs_B.csv`

- Holm p < .05: 5/15 cells; first > second in 5, second > first in 0

| model_id | content_type | acc_first | acc_second | diff | diff_ci_lo | diff_ci_hi | b_first_only | c_second_only | p_holm |
|---|---|---|---|---|---|---|---|---|---|
| InternVL3-8B | code | 0.632 | 0.506 | 0.126 | 0.085 | 0.166 | 89 | 26 | 4.13e-08 |
| InternVL3-8B | math | 0.920 | 0.864 | 0.056 | 0.026 | 0.087 | 43 | 15 | 0.003 |
| InternVL3-8B | table | 0.648 | 0.588 | 0.060 | 0.013 | 0.107 | 87 | 57 | 0.154 |
| Qwen2.5-VL-32B | code | 0.812 | 0.730 | 0.082 | 0.053 | 0.112 | 50 | 9 | 6.84e-07 |
| Qwen2.5-VL-32B | math | 0.918 | 0.902 | 0.016 | -0.013 | 0.046 | 31 | 23 | 1.000 |
| Qwen2.5-VL-32B | table | 0.812 | 0.794 | 0.018 | -0.012 | 0.049 | 34 | 25 | 1.000 |
| Qwen2.5-VL-3B | code | 0.386 | 0.342 | 0.044 | 6.78e-04 | 0.087 | 72 | 50 | 0.511 |
| Qwen2.5-VL-3B | math | 0.840 | 0.818 | 0.022 | -0.010 | 0.054 | 38 | 27 | 1.000 |
| Qwen2.5-VL-3B | table | 0.428 | 0.454 | -0.026 | -0.078 | 0.026 | 82 | 95 | 1.000 |
| Qwen2.5-VL-7B | code | 0.524 | 0.490 | 0.034 | -0.005 | 0.072 | 57 | 40 | 0.726 |
| Qwen2.5-VL-7B | math | 0.868 | 0.868 | 0.000 | -0.026 | 0.026 | 20 | 20 | 1.000 |
| Qwen2.5-VL-7B | table | 0.626 | 0.664 | -0.038 | -0.080 | 0.004 | 47 | 66 | 0.720 |
| gemma-3-12b | code | 0.688 | 0.494 | 0.194 | 0.151 | 0.236 | 117 | 20 | 1.07e-16 |
| gemma-3-12b | math | 0.948 | 0.934 | 0.014 | -0.007 | 0.036 | 17 | 10 | 1.000 |
| gemma-3-12b | table | 0.734 | 0.648 | 0.086 | 0.041 | 0.130 | 88 | 45 | 0.003 |

### A (text) vs C (image + transcribe)
source: `results/analysis/rq1_A_vs_C.csv`

- Holm p < .05: 4/15 cells; first > second in 4, second > first in 0

| model_id | content_type | acc_first | acc_second | diff | diff_ci_lo | diff_ci_hi | b_first_only | c_second_only | p_holm |
|---|---|---|---|---|---|---|---|---|---|
| InternVL3-8B | code | 0.632 | 0.522 | 0.110 | 0.069 | 0.151 | 85 | 30 | 4.00e-06 |
| InternVL3-8B | math | 0.920 | 0.894 | 0.026 | 0.001 | 0.052 | 26 | 13 | 0.426 |
| InternVL3-8B | table | 0.648 | 0.628 | 0.020 | -0.027 | 0.067 | 78 | 68 | 1.000 |
| Qwen2.5-VL-32B | code | 0.812 | 0.740 | 0.072 | 0.040 | 0.104 | 52 | 16 | 1.69e-04 |
| Qwen2.5-VL-32B | math | 0.918 | 0.948 | -0.030 | -0.057 | -0.005 | 13 | 28 | 0.303 |
| Qwen2.5-VL-32B | table | 0.812 | 0.806 | 0.006 | -0.024 | 0.036 | 29 | 26 | 1.000 |
| Qwen2.5-VL-3B | code | 0.386 | 0.358 | 0.028 | -0.015 | 0.071 | 67 | 53 | 1.000 |
| Qwen2.5-VL-3B | math | 0.840 | 0.752 | 0.088 | 0.049 | 0.127 | 72 | 28 | 1.64e-04 |
| Qwen2.5-VL-3B | table | 0.428 | 0.392 | 0.036 | -0.017 | 0.089 | 101 | 83 | 1.000 |
| Qwen2.5-VL-7B | code | 0.524 | 0.480 | 0.044 | 0.006 | 0.082 | 58 | 36 | 0.303 |
| Qwen2.5-VL-7B | math | 0.868 | 0.866 | 0.002 | -0.024 | 0.029 | 22 | 21 | 1.000 |
| Qwen2.5-VL-7B | table | 0.626 | 0.668 | -0.042 | -0.084 | 4.38e-04 | 48 | 69 | 0.448 |
| gemma-3-12b | code | 0.688 | 0.542 | 0.146 | 0.105 | 0.186 | 94 | 21 | 4.86e-11 |
| gemma-3-12b | math | 0.948 | 0.922 | 0.026 | 0.003 | 0.050 | 23 | 10 | 0.316 |
| gemma-3-12b | table | 0.734 | 0.726 | 0.008 | -0.036 | 0.052 | 64 | 60 | 1.000 |

### B (image) vs C (image + transcribe)
source: `results/analysis/rq1_B_vs_C.csv`

- Holm p < .05: 3/15 cells; first > second in 1, second > first in 2

| model_id | content_type | acc_first | acc_second | diff | diff_ci_lo | diff_ci_hi | b_first_only | c_second_only | p_holm |
|---|---|---|---|---|---|---|---|---|---|
| InternVL3-8B | code | 0.506 | 0.522 | -0.016 | -0.054 | 0.022 | 43 | 51 | 1.000 |
| InternVL3-8B | math | 0.864 | 0.894 | -0.030 | -0.054 | -0.007 | 10 | 25 | 0.167 |
| InternVL3-8B | table | 0.588 | 0.628 | -0.040 | -0.084 | 0.005 | 55 | 75 | 0.857 |
| Qwen2.5-VL-32B | code | 0.730 | 0.740 | -0.010 | -0.034 | 0.014 | 16 | 21 | 1.000 |
| Qwen2.5-VL-32B | math | 0.902 | 0.948 | -0.046 | -0.072 | -0.023 | 7 | 30 | 0.003 |
| Qwen2.5-VL-32B | table | 0.794 | 0.806 | -0.012 | -0.040 | 0.016 | 21 | 27 | 1.000 |
| Qwen2.5-VL-3B | code | 0.342 | 0.358 | -0.016 | -0.057 | 0.025 | 50 | 58 | 1.000 |
| Qwen2.5-VL-3B | math | 0.818 | 0.752 | 0.066 | 0.027 | 0.105 | 67 | 34 | 0.017 |
| Qwen2.5-VL-3B | table | 0.454 | 0.392 | 0.062 | 0.014 | 0.110 | 91 | 60 | 0.158 |
| Qwen2.5-VL-7B | code | 0.490 | 0.480 | 0.010 | -0.025 | 0.045 | 42 | 37 | 1.000 |
| Qwen2.5-VL-7B | math | 0.868 | 0.866 | 0.002 | -0.021 | 0.025 | 17 | 16 | 1.000 |
| Qwen2.5-VL-7B | table | 0.664 | 0.668 | -0.004 | -0.043 | 0.035 | 47 | 49 | 1.000 |
| gemma-3-12b | code | 0.494 | 0.542 | -0.048 | -0.082 | -0.013 | 27 | 51 | 0.105 |
| gemma-3-12b | math | 0.934 | 0.922 | 0.012 | -0.007 | 0.031 | 13 | 7 | 1.000 |
| gemma-3-12b | table | 0.648 | 0.726 | -0.078 | -0.113 | -0.043 | 22 | 61 | 3.27e-04 |

- A vs B sensitivity: unparseable pairs excluded: Holm p < .05 in 5/15 — source: `results/analysis/rq1_A_vs_B_sens_parseable.csv`
- A vs B sensitivity: strict same-line parser: Holm p < .05 in 6/15 — source: `results/analysis/rq1_A_vs_B_sens_strict_parser.csv`
- Cochran's Q (A/B/C) Holm p < .05: 7/15 — source: `results/analysis/rq1_cochran_q.csv`

## RQ2 perception vs reasoning (condition C transcription)

### Transcription quality
source: `results/analysis/rq2_transcription.csv`

| model_id | content_type | pct_with_transcription | exact_rate | exact_lenient_rate | pct_cer_le_002 | cer_median | cer_mean |
|---|---|---|---|---|---|---|---|
| InternVL3-8B | code | 100.000 | 0.672 | 0.676 | 87.800 | 0.000 | 0.096 |
| InternVL3-8B | math | 100.000 | 0.936 | 0.936 | 98.600 | 0.000 | 0.003 |
| InternVL3-8B | table | 100.000 | 0.000 | 0.170 | 6.600 | 0.062 | 0.074 |
| Qwen2.5-VL-32B | code | 99.600 | 0.778 | 0.786 | 95.000 | 0.000 | 0.007 |
| Qwen2.5-VL-32B | math | 100.000 | 0.946 | 0.946 | 98.800 | 0.000 | 8.18e-04 |
| Qwen2.5-VL-32B | table | 100.000 | 0.004 | 0.328 | 32.400 | 0.042 | 0.062 |
| Qwen2.5-VL-3B | code | 100.000 | 0.670 | 0.678 | 88.800 | 0.000 | 0.007 |
| Qwen2.5-VL-3B | math | 100.000 | 0.926 | 0.926 | 98.000 | 0.000 | 0.010 |
| Qwen2.5-VL-3B | table | 100.000 | 0.000 | 0.112 | 6.400 | 0.076 | 0.128 |
| Qwen2.5-VL-7B | code | 100.000 | 0.868 | 0.868 | 96.800 | 0.000 | 0.002 |
| Qwen2.5-VL-7B | math | 100.000 | 0.816 | 0.816 | 83.400 | 0.000 | 0.033 |
| Qwen2.5-VL-7B | table | 100.000 | 0.000 | 0.398 | 20.200 | 0.037 | 0.961 |
| gemma-3-12b | code | 20.000 | 0.100 | 0.100 | 16.400 | 1.000 | 0.802 |
| gemma-3-12b | math | 77.600 | 0.698 | 0.698 | 77.200 | 0.000 | 0.224 |
| gemma-3-12b | table | 82.200 | 0.000 | 0.186 | 7.800 | 0.096 | 0.318 |

- table measures: CER ≤ 0.02 and lenient exact (primary exact ≈ 0 for tables; deviation #15)

### A−C gap split by transcription correctness
source: `results/analysis/rq2_A_vs_C_by_transcription.csv`

| model_id | content_type | subset_rule | gap_A_minus_C_wrong | gap_A_minus_C_correct | n_pairs_wrong | n_pairs_correct |
|---|---|---|---|---|---|---|
| InternVL3-8B | code | cer_le_0.02 | 0.230 | 0.093 | 61.000 | 439.000 |
| InternVL3-8B | code | exact | 0.238 | 0.048 | 164.000 | 336.000 |
| InternVL3-8B | code | exact_lenient | 0.241 | 0.047 | 162.000 | 338.000 |
| InternVL3-8B | code | exact_tags_only | 0.239 | 0.048 | 163.000 | 336.000 |
| InternVL3-8B | math | cer_le_0.02 | 0.000 | 0.026 | 7.000 | 493.000 |
| InternVL3-8B | math | exact | 0.188 | 0.015 | 32.000 | 468.000 |
| InternVL3-8B | math | exact_lenient | 0.188 | 0.015 | 32.000 | 468.000 |
| InternVL3-8B | math | exact_tags_only | 0.188 | 0.015 | 32.000 | 468.000 |
| InternVL3-8B | table | cer_le_0.02 | 0.021 | 0.000 | 467.000 | 33.000 |
| InternVL3-8B | table | exact | 0.020 |  | 500.000 |  |
| InternVL3-8B | table | exact_lenient | 0.039 | -0.071 | 415.000 | 85.000 |
| InternVL3-8B | table | exact_tags_only | 0.020 |  | 500.000 |  |
| Qwen2.5-VL-32B | code | cer_le_0.02 | 0.200 | 0.065 | 25.000 | 475.000 |
| Qwen2.5-VL-32B | code | exact | 0.252 | 0.021 | 111.000 | 389.000 |
| Qwen2.5-VL-32B | code | exact_lenient | 0.252 | 0.023 | 107.000 | 393.000 |
| Qwen2.5-VL-32B | math | cer_le_0.02 | 0.333 | -0.034 | 6.000 | 494.000 |
| Qwen2.5-VL-32B | math | exact | 0.111 | -0.038 | 27.000 | 473.000 |
| Qwen2.5-VL-32B | math | exact_lenient | 0.111 | -0.038 | 27.000 | 473.000 |
| Qwen2.5-VL-32B | math | exact_tags_only | 0.111 | -0.038 | 27.000 | 473.000 |
| Qwen2.5-VL-32B | table | cer_le_0.02 | 0.015 | -0.012 | 338.000 | 162.000 |
| Qwen2.5-VL-32B | table | exact | 0.006 | 0.000 | 498.000 | 2.000 |
| Qwen2.5-VL-32B | table | exact_lenient | 0.015 | -0.012 | 336.000 | 164.000 |
| Qwen2.5-VL-32B | table | exact_tags_only | 0.000 | 0.000 | 309.000 | 1.000 |
| Qwen2.5-VL-3B | code | cer_le_0.02 | 0.054 | 0.025 | 56.000 | 444.000 |
| Qwen2.5-VL-3B | code | exact | 0.079 | 0.003 | 165.000 | 335.000 |
| Qwen2.5-VL-3B | code | exact_lenient | 0.081 | 0.003 | 161.000 | 339.000 |
| Qwen2.5-VL-3B | code | exact_tags_only | 0.079 | 0.003 | 165.000 | 335.000 |
| Qwen2.5-VL-3B | math | cer_le_0.02 | 0.600 | 0.078 | 10.000 | 490.000 |
| Qwen2.5-VL-3B | math | exact | 0.297 | 0.071 | 37.000 | 463.000 |
| Qwen2.5-VL-3B | math | exact_lenient | 0.297 | 0.071 | 37.000 | 463.000 |
| Qwen2.5-VL-3B | math | exact_tags_only | 0.297 | 0.071 | 37.000 | 463.000 |
| Qwen2.5-VL-3B | table | cer_le_0.02 | 0.047 | -0.125 | 468.000 | 32.000 |
| Qwen2.5-VL-3B | table | exact | 0.036 |  | 500.000 |  |
| Qwen2.5-VL-3B | table | exact_lenient | 0.050 | -0.071 | 444.000 | 56.000 |
| Qwen2.5-VL-3B | table | exact_tags_only | 0.031 |  | 486.000 |  |
| Qwen2.5-VL-7B | code | cer_le_0.02 | 0.125 | 0.041 | 16.000 | 484.000 |
| Qwen2.5-VL-7B | code | exact | 0.121 | 0.032 | 66.000 | 434.000 |
| Qwen2.5-VL-7B | code | exact_lenient | 0.121 | 0.032 | 66.000 | 434.000 |
| Qwen2.5-VL-7B | code | exact_tags_only | 0.121 | 0.032 | 66.000 | 434.000 |
| Qwen2.5-VL-7B | math | cer_le_0.02 | 0.048 | -0.007 | 83.000 | 417.000 |
| Qwen2.5-VL-7B | math | exact | 0.033 | -0.005 | 92.000 | 408.000 |
| Qwen2.5-VL-7B | math | exact_lenient | 0.033 | -0.005 | 92.000 | 408.000 |
| Qwen2.5-VL-7B | math | exact_tags_only | 0.033 | -0.005 | 92.000 | 408.000 |
| Qwen2.5-VL-7B | table | cer_le_0.02 | -0.060 | 0.030 | 399.000 | 101.000 |
| Qwen2.5-VL-7B | table | exact | -0.042 |  | 500.000 |  |
| Qwen2.5-VL-7B | table | exact_lenient | -0.037 | -0.050 | 301.000 | 199.000 |
| Qwen2.5-VL-7B | table | exact_tags_only | -0.046 |  | 498.000 |  |
| gemma-3-12b | code | cer_le_0.02 | 0.156 | 0.098 | 418.000 | 82.000 |
| gemma-3-12b | code | exact | 0.158 | 0.040 | 450.000 | 50.000 |
| gemma-3-12b | code | exact_lenient | 0.158 | 0.040 | 450.000 | 50.000 |
| gemma-3-12b | code | exact_tags_only | 0.256 | 0.000 | 39.000 | 27.000 |
| gemma-3-12b | math | cer_le_0.02 | 0.044 | 0.021 | 114.000 | 386.000 |
| gemma-3-12b | math | exact | 0.066 | 0.009 | 151.000 | 349.000 |
| gemma-3-12b | math | exact_lenient | 0.066 | 0.009 | 151.000 | 349.000 |
| gemma-3-12b | math | exact_tags_only | 0.154 | 0.009 | 39.000 | 349.000 |
| gemma-3-12b | table | cer_le_0.02 | 0.009 | 0.000 | 461.000 | 39.000 |
| gemma-3-12b | table | exact | 0.008 |  | 500.000 |  |
| gemma-3-12b | table | exact_lenient | -0.005 | 0.065 | 407.000 | 93.000 |
| gemma-3-12b | table | exact_tags_only | 0.023 |  | 393.000 |  |

### Logit correct(B) ~ CER(C) + model
source: `results/analysis/rq2_logit_B_on_cer.csv`

| content_type | predictor | n | coef | se | odds_ratio | or_ci_lo | or_ci_hi | p_value |
|---|---|---|---|---|---|---|---|---|
| code | cer | 2500 | -0.1185 | 0.1826 | 0.8883 | 0.6210 | 1.2706 | 0.5166 |
| code | cer_gt_002 | 2500 | -0.8410 | 0.1496 | 0.4313 | 0.3217 | 0.5782 | 1.89e-08 |
| code | cer_capped1 | 2500 | -0.1309 | 0.2220 | 0.8773 | 0.5678 | 1.3556 | 0.5555 |
| math | cer | 2500 | -0.5848 | 0.3610 | 0.5572 | 0.2746 | 1.1305 | 0.1052 |
| math | cer_gt_002 | 2500 | -0.5524 | 0.2207 | 0.5755 | 0.3734 | 0.8871 | 0.0123 |
| math | cer_capped1 | 2500 | -0.5848 | 0.3610 | 0.5572 | 0.2746 | 1.1305 | 0.1052 |
| table | cer | 2500 | 0.0160 | 0.0268 | 1.0161 | 0.9641 | 1.0710 | 0.5502 |
| table | cer_gt_002 | 2500 | -0.2270 | 0.1332 | 0.7970 | 0.6138 | 1.0347 | 0.0884 |
| table | cer_capped1 | 2500 | -0.0107 | 0.2179 | 0.9893 | 0.6455 | 1.5163 | 0.9608 |

## RQ3 output length A vs B (Wilcoxon signed-rank, Holm)
source: `results/analysis/rq3_tokens_wilcoxon.csv`

- Holm p < .05: 6/15

| model_id | content_type | median_A | median_B | median_diff_A_minus_B | p_holm |
|---|---|---|---|---|---|
| InternVL3-8B | code | 330.0 | 344.0 | -12.0 | 0.1 |
| InternVL3-8B | math | 251.0 | 210.0 | 38.0 | 4.38e-34 |
| InternVL3-8B | table | 141.5 | 147.0 | 3.5 | 1.0 |
| Qwen2.5-VL-32B | code | 564.0 | 610.0 | -32.0 | 3.38e-12 |
| Qwen2.5-VL-32B | math | 316.0 | 324.0 | -2.0 | 0.2 |
| Qwen2.5-VL-32B | table | 215.0 | 245.0 | -18.5 | 6.68e-17 |
| Qwen2.5-VL-3B | code | 327.0 | 333.5 | -9.5 | 0.1 |
| Qwen2.5-VL-3B | math | 231.5 | 232.5 | 0.0 | 1.0 |
| Qwen2.5-VL-3B | table | 181.0 | 186.0 | 1.0 | 1.0 |
| Qwen2.5-VL-7B | code | 396.0 | 358.5 | 25.5 | 4.06e-06 |
| Qwen2.5-VL-7B | math | 249.5 | 224.5 | 20.5 | 6.29e-26 |
| Qwen2.5-VL-7B | table | 170.5 | 172.0 | -3.0 | 0.4 |
| gemma-3-12b | code | 239.0 | 290.0 | -35.0 | 5.50e-28 |
| gemma-3-12b | math | 146.0 | 157.0 | -6.0 | 0.1 |
| gemma-3-12b | table | 91.0 | 80.0 | 2.5 | 0.1 |

- A-correct/B-wrong flips available per content type — source: `results/analysis/flip_counts.csv`; coded sample: `results/coding/error_sample.csv`

| content_type | n_flips |
|---|---|
| code | 385 |
| math | 149 |
| table | 338 |

## Replication, runs 1-3, primary models

- cell accuracy SD across runs: max 0.0174; range: max 0.032 — source: `results/analysis/replication_full_accuracy.csv`
- Fleiss' kappa per cell: min 0.732, median 0.877, max 0.946; % items mixed: min 1.0, median 6.8, max 19.8 — source: `results/analysis/replication_full_stability.csv`
- A vs B significant in all 3 runs: 4/15 (InternVL3-8B code, InternVL3-8B math, Qwen2.5-VL-32B code, gemma-3-12b code); in some runs: 2; direction agrees in all runs: 13/15 — source: `results/analysis/replication_full_rq1_A_vs_B_agreement.csv`
- A vs B majority vote Holm p < .05: 6/15 — source: `results/analysis/replication_full_rq1_A_vs_B_majority_vote.csv`
- A vs C significant in all 3 runs: 4/15 (InternVL3-8B code, Qwen2.5-VL-32B code, Qwen2.5-VL-3B math, gemma-3-12b code); in some runs: 2; direction agrees in all runs: 13/15 — source: `results/analysis/replication_full_rq1_A_vs_C_agreement.csv`
- A vs C majority vote Holm p < .05: 4/15 — source: `results/analysis/replication_full_rq1_A_vs_C_majority_vote.csv`
- A vs B permutation test on per-item mean correctness, Holm p < .05: 7/15 — source: `results/analysis/replication_full_rq1_A_vs_B_permutation_mean.csv`

RQ2 pattern (A−C gap larger when transcription is wrong), per model × run — source: `results/analysis/replication_full_rq2_pattern_check.csv`

| content_type | subset_rule | n_gap_wrong_gt_correct | n_model_runs |
|---|---|---|---|
| code | cer_le_0.02 | 15 | 15 |
| code | exact | 15 | 15 |
| math | cer_le_0.02 | 12 | 15 |
| math | exact | 15 | 15 |
| table | cer_le_0.02 | 11 | 15 |
| table | exact | 3 | 15 |

A vs B per run — source: `results/analysis/replication_full_rq1_A_vs_B_agreement.csv`

| model_id | content_type | diff_run1 | diff_run2 | diff_run3 | p_holm_run1 | p_holm_run2 | p_holm_run3 | n_runs_sig |
|---|---|---|---|---|---|---|---|---|
| InternVL3-8B | code | 0.126 | 0.110 | 0.130 | 4.13e-08 | 6.10e-06 | 1.70e-08 | 3 |
| InternVL3-8B | math | 0.056 | 0.052 | 0.056 | 0.003 | 0.014 | 0.007 | 3 |
| InternVL3-8B | table | 0.060 | 0.086 | 0.088 | 0.154 | 0.006 | 0.004 | 2 |
| Qwen2.5-VL-32B | code | 0.082 | 0.086 | 0.082 | 6.84e-07 | 2.36e-06 | 3.62e-06 | 3 |
| Qwen2.5-VL-32B | math | 0.016 | 0.016 | 0.016 | 1.000 | 1.000 | 0.906 | 0 |
| Qwen2.5-VL-32B | table | 0.018 | 0.036 | 0.032 | 1.000 | 0.219 | 0.391 | 0 |
| Qwen2.5-VL-3B | code | 0.044 | 0.060 | 0.054 | 0.511 | 0.059 | 0.135 | 0 |
| Qwen2.5-VL-3B | math | 0.022 | 0.006 | 0.040 | 1.000 | 1.000 | 0.135 | 0 |
| Qwen2.5-VL-3B | table | -0.026 | 0.000 | -0.030 | 1.000 | 1.000 | 0.906 | 0 |
| Qwen2.5-VL-7B | code | 0.034 | 0.044 | 0.036 | 0.726 | 0.234 | 0.475 | 0 |
| Qwen2.5-VL-7B | math | 0.000 | 0.004 | -0.002 | 1.000 | 1.000 | 1.000 | 0 |
| Qwen2.5-VL-7B | table | -0.038 | -0.032 | -0.040 | 0.720 | 0.762 | 0.402 | 0 |
| gemma-3-12b | code | 0.194 | 0.198 | 0.188 | 1.07e-16 | 8.59e-18 | 1.03e-15 | 3 |
| gemma-3-12b | math | 0.014 | 0.018 | 0.018 | 1.000 | 0.732 | 0.598 | 0 |
| gemma-3-12b | table | 0.086 | 0.058 | 0.062 | 0.003 | 0.141 | 0.080 | 1 |

## Replication, runs 1-3, extension models (exploratory)

- cell accuracy SD across runs: max 0.0120; range: max 0.024 — source: `results/analysis/ext_replication_full_accuracy.csv`
- Fleiss' kappa per cell: min 0.832, median 0.911, max 0.960; % items mixed: min 0.4, median 4.0, max 10.6 — source: `results/analysis/ext_replication_full_stability.csv`
- A vs B significant in all 3 runs: 4/12 (InternVL3_5-8B code, InternVL3_5-8B math, Qwen3-VL-8B code, gemma-3-27b code); in some runs: 2; direction agrees in all runs: 12/12 — source: `results/analysis/ext_replication_full_rq1_A_vs_B_agreement.csv`
- A vs B majority vote Holm p < .05: 6/12 — source: `results/analysis/ext_replication_full_rq1_A_vs_B_majority_vote.csv`
- A vs C significant in all 3 runs: 3/12 (InternVL3_5-8B code, Qwen3-VL-8B code, gemma-3-27b code); in some runs: 1; direction agrees in all runs: 11/12 — source: `results/analysis/ext_replication_full_rq1_A_vs_C_agreement.csv`
- A vs C majority vote Holm p < .05: 5/12 — source: `results/analysis/ext_replication_full_rq1_A_vs_C_majority_vote.csv`
- A vs B permutation test on per-item mean correctness, Holm p < .05: 6/12 — source: `results/analysis/ext_replication_full_rq1_A_vs_B_permutation_mean.csv`

RQ2 pattern (A−C gap larger when transcription is wrong), per model × run — source: `results/analysis/ext_replication_full_rq2_pattern_check.csv`

| content_type | subset_rule | n_gap_wrong_gt_correct | n_model_runs |
|---|---|---|---|
| code | cer_le_0.02 | 12 | 12 |
| code | exact | 12 | 12 |
| math | cer_le_0.02 | 6 | 12 |
| math | exact | 6 | 12 |
| table | cer_le_0.02 | 12 | 12 |
| table | exact | 1 | 12 |

A vs B per run — source: `results/analysis/ext_replication_full_rq1_A_vs_B_agreement.csv`

| model_id | content_type | diff_run1 | diff_run2 | diff_run3 | p_holm_run1 | p_holm_run2 | p_holm_run3 | n_runs_sig |
|---|---|---|---|---|---|---|---|---|
| InternVL3_5-8B | code | 0.108 | 0.098 | 0.088 | 2.44e-07 | 5.60e-07 | 2.59e-05 | 3 |
| InternVL3_5-8B | math | 0.116 | 0.118 | 0.120 | 9.18e-13 | 4.94e-13 | 2.66e-13 | 3 |
| InternVL3_5-8B | table | 0.050 | 0.056 | 0.042 | 0.106 | 0.059 | 0.329 | 0 |
| Qwen2.5-VL-72B-AWQ | code | 0.040 | 0.066 | 0.070 | 0.133 | 8.98e-04 | 3.11e-04 | 2 |
| Qwen2.5-VL-72B-AWQ | math | 0.010 | 0.008 | 0.008 | 0.680 | 1.000 | 1.000 | 0 |
| Qwen2.5-VL-72B-AWQ | table | 0.004 | 0.012 | 0.018 | 0.905 | 1.000 | 1.000 | 0 |
| Qwen3-VL-8B | code | 0.122 | 0.098 | 0.100 | 1.64e-09 | 2.26e-06 | 3.11e-06 | 3 |
| Qwen3-VL-8B | math | 0.010 | 0.006 | 0.006 | 0.767 | 1.000 | 1.000 | 0 |
| Qwen3-VL-8B | table | 0.050 | 0.048 | 0.050 | 0.047 | 0.059 | 0.041 | 2 |
| gemma-3-27b | code | 0.146 | 0.134 | 0.152 | 7.00e-12 | 6.72e-10 | 4.16e-13 | 3 |
| gemma-3-27b | math | 0.026 | 0.022 | 0.018 | 0.074 | 0.173 | 0.610 | 0 |
| gemma-3-27b | table | 0.036 | 0.028 | 0.030 | 0.380 | 0.809 | 0.703 | 0 |

## Extension models, run 1 (exploratory; own Holm family)

source: `results/analysis/ext_descriptives.csv`

| model_id | content_type | A_text | B_image | C_image_transcribe |
|---|---|---|---|---|
| InternVL3_5-8B | code | 0.734 | 0.626 | 0.642 |
| InternVL3_5-8B | math | 0.954 | 0.838 | 0.942 |
| InternVL3_5-8B | table | 0.766 | 0.716 | 0.746 |
| Qwen2.5-VL-72B-AWQ | code | 0.798 | 0.758 | 0.754 |
| Qwen2.5-VL-72B-AWQ | math | 0.966 | 0.956 | 0.960 |
| Qwen2.5-VL-72B-AWQ | table | 0.812 | 0.808 | 0.816 |
| Qwen3-VL-8B | code | 0.808 | 0.686 | 0.702 |
| Qwen3-VL-8B | math | 0.952 | 0.942 | 0.954 |
| Qwen3-VL-8B | table | 0.828 | 0.778 | 0.798 |
| gemma-3-27b | code | 0.758 | 0.612 | 0.684 |
| gemma-3-27b | math | 0.972 | 0.946 | 0.948 |
| gemma-3-27b | table | 0.778 | 0.742 | 0.746 |

### Extension A vs B
source: `results/analysis/ext_rq1_A_vs_B.csv`

- Holm p < .05: 5/12 cells; first > second in 5, second > first in 0

| model_id | content_type | acc_first | acc_second | diff | diff_ci_lo | diff_ci_hi | b_first_only | c_second_only | p_holm |
|---|---|---|---|---|---|---|---|---|---|
| InternVL3_5-8B | code | 0.734 | 0.626 | 0.108 | 0.070 | 0.145 | 75 | 21 | 2.44e-07 |
| InternVL3_5-8B | math | 0.954 | 0.838 | 0.116 | 0.086 | 0.149 | 63 | 5 | 9.18e-13 |
| InternVL3_5-8B | table | 0.766 | 0.716 | 0.050 | 0.010 | 0.090 | 64 | 39 | 0.106 |
| Qwen2.5-VL-72B-AWQ | code | 0.798 | 0.758 | 0.040 | 0.006 | 0.074 | 47 | 27 | 0.133 |
| Qwen2.5-VL-72B-AWQ | math | 0.966 | 0.956 | 0.010 | -0.004 | 0.026 | 8 | 3 | 0.680 |
| Qwen2.5-VL-72B-AWQ | table | 0.812 | 0.808 | 0.004 | -0.029 | 0.037 | 36 | 34 | 0.905 |
| Qwen3-VL-8B | code | 0.808 | 0.686 | 0.122 | 0.085 | 0.159 | 78 | 17 | 1.64e-09 |
| Qwen3-VL-8B | math | 0.952 | 0.942 | 0.010 | -0.009 | 0.030 | 13 | 8 | 0.767 |
| Qwen3-VL-8B | table | 0.828 | 0.778 | 0.050 | 0.016 | 0.085 | 51 | 26 | 0.047 |
| gemma-3-27b | code | 0.758 | 0.612 | 0.146 | 0.107 | 0.185 | 91 | 18 | 7.00e-12 |
| gemma-3-27b | math | 0.972 | 0.946 | 0.026 | 0.007 | 0.047 | 18 | 5 | 0.074 |
| gemma-3-27b | table | 0.778 | 0.742 | 0.036 | -0.004 | 0.076 | 61 | 43 | 0.380 |

### Extension A vs C
source: `results/analysis/ext_rq1_A_vs_C.csv`

- Holm p < .05: 3/12 cells; first > second in 3, second > first in 0

| model_id | content_type | acc_first | acc_second | diff | diff_ci_lo | diff_ci_hi | b_first_only | c_second_only | p_holm |
|---|---|---|---|---|---|---|---|---|---|
| InternVL3_5-8B | code | 0.734 | 0.642 | 0.092 | 0.056 | 0.128 | 66 | 20 | 7.34e-06 |
| InternVL3_5-8B | math | 0.954 | 0.942 | 0.012 | -0.008 | 0.033 | 15 | 9 | 1.000 |
| InternVL3_5-8B | table | 0.766 | 0.746 | 0.020 | -0.019 | 0.059 | 53 | 43 | 1.000 |
| Qwen2.5-VL-72B-AWQ | code | 0.798 | 0.754 | 0.044 | 0.012 | 0.077 | 45 | 23 | 0.083 |
| Qwen2.5-VL-72B-AWQ | math | 0.966 | 0.960 | 0.006 | -0.006 | 0.020 | 5 | 2 | 1.000 |
| Qwen2.5-VL-72B-AWQ | table | 0.812 | 0.816 | -0.004 | -0.035 | 0.027 | 30 | 32 | 1.000 |
| Qwen3-VL-8B | code | 0.808 | 0.702 | 0.106 | 0.070 | 0.142 | 70 | 17 | 1.00e-07 |
| Qwen3-VL-8B | math | 0.952 | 0.954 | -0.002 | -0.020 | 0.016 | 8 | 9 | 1.000 |
| Qwen3-VL-8B | table | 0.828 | 0.798 | 0.030 | -0.003 | 0.063 | 42 | 27 | 0.638 |
| gemma-3-27b | code | 0.758 | 0.684 | 0.074 | 0.036 | 0.111 | 65 | 28 | 0.002 |
| gemma-3-27b | math | 0.972 | 0.948 | 0.024 | 0.007 | 0.044 | 15 | 3 | 0.068 |
| gemma-3-27b | table | 0.778 | 0.746 | 0.032 | -0.007 | 0.071 | 56 | 40 | 0.752 |

### Extension transcription quality
source: `results/analysis/ext_rq2_transcription.csv`

| model_id | content_type | pct_with_transcription | exact_rate | exact_lenient_rate | pct_cer_le_002 | cer_median |
|---|---|---|---|---|---|---|
| InternVL3_5-8B | code | 0.600 | 0.006 | 0.006 | 0.600 | 1.000 |
| InternVL3_5-8B | math | 5.600 | 0.048 | 0.048 | 5.000 | 1.000 |
| InternVL3_5-8B | table | 18.800 | 0.000 | 0.096 | 3.800 | 1.000 |
| Qwen2.5-VL-72B-AWQ | code | 100.000 | 0.904 | 0.904 | 99.000 | 0.000 |
| Qwen2.5-VL-72B-AWQ | math | 100.000 | 0.986 | 0.986 | 99.200 | 0.000 |
| Qwen2.5-VL-72B-AWQ | table | 100.000 | 0.004 | 0.482 | 40.800 | 0.026 |
| Qwen3-VL-8B | code | 100.000 | 0.774 | 0.774 | 94.400 | 0.000 |
| Qwen3-VL-8B | math | 94.200 | 0.904 | 0.904 | 93.600 | 0.000 |
| Qwen3-VL-8B | table | 100.000 | 0.000 | 0.454 | 18.200 | 0.035 |
| gemma-3-27b | code | 100.000 | 0.648 | 0.648 | 91.000 | 0.000 |
| gemma-3-27b | math | 100.000 | 0.836 | 0.836 | 99.400 | 0.000 |
| gemma-3-27b | table | 100.000 | 0.000 | 0.328 | 12.200 | 0.048 |

- extension RQ3 Wilcoxon Holm p < .05: 11/12 — source: `results/analysis/ext_rq3_tokens_wilcoxon.csv`

## A−B gap, all models (run 1)
source: `results/analysis/combined_gap_A_minus_B_all_models.csv`

| model_id | group | content_type | diff | diff_ci_lo | diff_ci_hi | p_holm |
|---|---|---|---|---|---|---|
| InternVL3-8B | primary | code | 0.126 | 0.085 | 0.166 | 4.13e-08 |
| InternVL3-8B | primary | math | 0.056 | 0.026 | 0.087 | 0.003 |
| InternVL3-8B | primary | table | 0.060 | 0.013 | 0.107 | 0.154 |
| Qwen2.5-VL-32B | primary | code | 0.082 | 0.053 | 0.112 | 6.84e-07 |
| Qwen2.5-VL-32B | primary | math | 0.016 | -0.013 | 0.046 | 1.000 |
| Qwen2.5-VL-32B | primary | table | 0.018 | -0.012 | 0.049 | 1.000 |
| Qwen2.5-VL-3B | primary | code | 0.044 | 6.78e-04 | 0.087 | 0.511 |
| Qwen2.5-VL-3B | primary | math | 0.022 | -0.010 | 0.054 | 1.000 |
| Qwen2.5-VL-3B | primary | table | -0.026 | -0.078 | 0.026 | 1.000 |
| Qwen2.5-VL-7B | primary | code | 0.034 | -0.005 | 0.072 | 0.726 |
| Qwen2.5-VL-7B | primary | math | 0.000 | -0.026 | 0.026 | 1.000 |
| Qwen2.5-VL-7B | primary | table | -0.038 | -0.080 | 0.004 | 0.720 |
| gemma-3-12b | primary | code | 0.194 | 0.151 | 0.236 | 1.07e-16 |
| gemma-3-12b | primary | math | 0.014 | -0.007 | 0.036 | 1.000 |
| gemma-3-12b | primary | table | 0.086 | 0.041 | 0.130 | 0.003 |
| InternVL3_5-8B | extension (exploratory) | code | 0.108 | 0.070 | 0.145 | 2.44e-07 |
| InternVL3_5-8B | extension (exploratory) | math | 0.116 | 0.086 | 0.149 | 9.18e-13 |
| InternVL3_5-8B | extension (exploratory) | table | 0.050 | 0.010 | 0.090 | 0.106 |
| Qwen2.5-VL-72B-AWQ | extension (exploratory) | code | 0.040 | 0.006 | 0.074 | 0.133 |
| Qwen2.5-VL-72B-AWQ | extension (exploratory) | math | 0.010 | -0.004 | 0.026 | 0.680 |
| Qwen2.5-VL-72B-AWQ | extension (exploratory) | table | 0.004 | -0.029 | 0.037 | 0.905 |
| Qwen3-VL-8B | extension (exploratory) | code | 0.122 | 0.085 | 0.159 | 1.64e-09 |
| Qwen3-VL-8B | extension (exploratory) | math | 0.010 | -0.009 | 0.030 | 0.767 |
| Qwen3-VL-8B | extension (exploratory) | table | 0.050 | 0.016 | 0.085 | 0.047 |
| gemma-3-27b | extension (exploratory) | code | 0.146 | 0.107 | 0.185 | 7.00e-12 |
| gemma-3-27b | extension (exploratory) | math | 0.026 | 0.007 | 0.047 | 0.074 |
| gemma-3-27b | extension (exploratory) | table | 0.036 | -0.004 | 0.076 | 0.380 |

## Resolution check: A−B code gap by image handling (descriptive; family confound)
source: `results/analysis/resolution_check_code_gap.csv`

| model_id | group | family | params_b | image_handling | resizes_image | acc_A | acc_B | gap_A_minus_B_run1 | diff_ci_lo | diff_ci_hi | p_holm_own_family | gap_mean_3runs | n_runs_sig |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Qwen2.5-VL-3B | primary | qwen2.5 | 3 | native resolution | False | 0.386 | 0.342 | 0.044 | 6.78e-04 | 0.087 | 0.511 | 0.053 | 0 |
| Qwen2.5-VL-7B | primary | qwen2.5 | 7 | native resolution | False | 0.524 | 0.490 | 0.034 | -0.005 | 0.072 | 0.726 | 0.038 | 0 |
| Qwen2.5-VL-32B | primary | qwen2.5 | 32 | native resolution | False | 0.812 | 0.730 | 0.082 | 0.053 | 0.112 | 6.84e-07 | 0.083 | 3 |
| Qwen2.5-VL-72B-AWQ | extension (exploratory) | qwen2.5 | 72 | native resolution | False | 0.798 | 0.758 | 0.040 | 0.006 | 0.074 | 0.133 | 0.059 | 2 |
| Qwen3-VL-8B | extension (exploratory) | qwen3 | 8 | native resolution | False | 0.808 | 0.686 | 0.122 | 0.085 | 0.159 | 1.64e-09 | 0.107 | 3 |
| gemma-3-12b | primary | gemma3 | 12 | resized to 896x896 (+pan-and-scan crops) | True | 0.688 | 0.494 | 0.194 | 0.151 | 0.236 | 1.07e-16 | 0.193 | 3 |
| gemma-3-27b | extension (exploratory) | gemma3 | 27 | resized to 896x896 (+pan-and-scan crops) | True | 0.758 | 0.612 | 0.146 | 0.107 | 0.185 | 7.00e-12 | 0.144 | 3 |
| InternVL3-8B | primary | internvl | 8 | resized to 448-px tile grid (+thumbnail) | True | 0.632 | 0.506 | 0.126 | 0.085 | 0.166 | 4.13e-08 | 0.122 | 3 |
| InternVL3_5-8B | extension (exploratory) | internvl | 8 | resized to 448-px tile grid (+thumbnail) | True | 0.734 | 0.626 | 0.108 | 0.070 | 0.145 | 2.44e-07 | 0.098 | 3 |

## Resolution check summary
source: `results/analysis/resolution_check_code_gap_summary.csv`

| resizes_image | n_models | mean_gap_run1 | min_gap_run1 | max_gap_run1 | note |
|---|---|---|---|---|---|
| False | 5 | 0.064 | 0.034 | 0.122 | descriptive only; family is confounded with image handling |
| True | 4 | 0.143 | 0.108 | 0.194 | descriptive only; family is confounded with image handling |

## Sensitivity: leading code fence = transcription (approved after T18)
source: `results/analysis/sens_leading_fence_recovered.csv`

| set | run | model_id | content_type | pct_with_transcription_frozen | pct_with_transcription_sens | n_recovered_leading_fence | recovered_exact_rate | recovered_pct_cer_le_002 | exact_rate_frozen | exact_rate_sens |
|---|---|---|---|---|---|---|---|---|---|---|
| primary | 1 | gemma-3-12b | code | 20.000 | 82.400 | 312 | 0.529 | 84.936 | 0.100 | 0.430 |
| primary | 1 | gemma-3-12b | table | 82.200 | 90.400 | 41 | 0.000 | 7.317 | 0.000 | 0.000 |
| primary | 2 | gemma-3-12b | code | 18.000 | 82.200 | 321 | 0.536 | 85.047 | 0.090 | 0.434 |
| primary | 2 | gemma-3-12b | table | 82.400 | 89.400 | 35 | 0.000 | 8.571 | 0.000 | 0.000 |
| primary | 3 | gemma-3-12b | code | 18.000 | 82.600 | 323 | 0.529 | 84.830 | 0.088 | 0.430 |
| primary | 3 | gemma-3-12b | table | 82.000 | 89.800 | 39 | 0.000 | 7.692 | 0.000 | 0.000 |
| ext | 1 | InternVL3_5-8B | code | 0.600 | 93.800 | 466 | 0.695 | 87.768 | 0.006 | 0.654 |
| ext | 2 | InternVL3_5-8B | code | 0.800 | 94.600 | 469 | 0.697 | 88.273 | 0.006 | 0.660 |
| ext | 3 | InternVL3_5-8B | code | 0.800 | 94.200 | 467 | 0.696 | 88.223 | 0.006 | 0.656 |

- replication_full RQ2 pattern under the rule, code: exact: 15/15, cer_le_0.02: 15/15 — source: `results/analysis/replication_full_rq2_pattern_check_sens_leading_fence.csv`

| model_id | subset_rule | run | gap_A_minus_C_correct | gap_A_minus_C_wrong | n_pairs_correct | n_pairs_wrong |
|---|---|---|---|---|---|---|
| gemma-3-12b | cer_le_0.02 | 1 | 0.095 | 0.261 | 347.000 | 153 |
| gemma-3-12b | cer_le_0.02 | 2 | 0.096 | 0.284 | 345.000 | 155 |
| gemma-3-12b | cer_le_0.02 | 3 | 0.109 | 0.233 | 350.000 | 150 |
| gemma-3-12b | exact | 1 | 0.051 | 0.218 | 215.000 | 285 |
| gemma-3-12b | exact | 2 | 0.037 | 0.244 | 217.000 | 283 |
| gemma-3-12b | exact | 3 | 0.060 | 0.211 | 215.000 | 285 |

- ext_replication_full RQ2 pattern under the rule, code: exact: 12/12, cer_le_0.02: 12/12 — source: `results/analysis/ext_replication_full_rq2_pattern_check_sens_leading_fence.csv`

| model_id | subset_rule | run | gap_A_minus_C_correct | gap_A_minus_C_wrong | n_pairs_correct | n_pairs_wrong |
|---|---|---|---|---|---|---|
| InternVL3_5-8B | cer_le_0.02 | 1 | 0.087 | 0.114 | 412.000 | 88 |
| InternVL3_5-8B | cer_le_0.02 | 2 | 0.062 | 0.110 | 418.000 | 82 |
| InternVL3_5-8B | cer_le_0.02 | 3 | 0.048 | 0.155 | 416.000 | 84 |
| InternVL3_5-8B | exact | 1 | 0.046 | 0.179 | 327.000 | 173 |
| InternVL3_5-8B | exact | 2 | 0.018 | 0.171 | 330.000 | 170 |
| InternVL3_5-8B | exact | 3 | 0.009 | 0.174 | 328.000 | 172 |

## GLMM: correct ~ condition × content + condition × model + (1 | item), run 1 (exact ML, Gauss-Hermite 40 nodes)
source: `results/analysis/glmm_fixed_effects.csv`

- n obs 22500, items 1500; log-lik -9060.67; sd(item) 2.236; latent ICC 0.603

| term | coef | se | z | p_value | odds_ratio | or_ci_lo | or_ci_hi |
|---|---|---|---|---|---|---|---|
| Intercept | 0.3092 | 0.1323 | 2.3366 | 0.0195 | 1.3624 | 1.0511 | 1.7658 |
| condition[T.B_image] | -0.2973 | 0.1247 | -2.3831 | 0.0172 | 0.7428 | 0.5817 | 0.9486 |
| condition[T.C_image_transcribe] | -0.3100 | 0.1248 | -2.4839 | 0.0130 | 0.7334 | 0.5742 | 0.9367 |
| content[T.math] | 3.0660 | 0.1853 | 16.5480 | 1.66e-61 | 21.4555 | 14.9219 | 30.8496 |
| content[T.table] | 0.2243 | 0.1621 | 1.3836 | 0.1665 | 1.2515 | 0.9108 | 1.7196 |
| model[T.InternVL3-8B] | 0.5502 | 0.1104 | 4.9842 | 6.22e-07 | 1.7336 | 1.3963 | 2.1524 |
| model[T.Qwen2.5-VL-32B] | 1.8248 | 0.1237 | 14.7489 | 3.13e-49 | 6.2016 | 4.8662 | 7.9035 |
| model[T.Qwen2.5-VL-3B] | -0.9923 | 0.1057 | -9.3904 | 5.98e-21 | 0.3707 | 0.3014 | 0.4560 |
| model[T.gemma-3-12b] | 1.1288 | 0.1152 | 9.7995 | 1.13e-22 | 3.0921 | 2.4672 | 3.8753 |
| condition[T.B_image]:content[T.math] | 0.3178 | 0.1430 | 2.2228 | 0.0262 | 1.3741 | 1.0383 | 1.8184 |
| condition[T.C_image_transcribe]:content[T.math] | 0.2542 | 0.1437 | 1.7694 | 0.0768 | 1.2894 | 0.9730 | 1.7087 |
| condition[T.B_image]:content[T.table] | 0.5913 | 0.1114 | 5.3075 | 1.11e-07 | 1.8064 | 1.4520 | 2.2473 |
| condition[T.C_image_transcribe]:content[T.table] | 0.5943 | 0.1122 | 5.2986 | 1.17e-07 | 1.8118 | 1.4543 | 2.2574 |
| condition[T.B_image]:model[T.InternVL3-8B] | -0.7347 | 0.1541 | -4.7676 | 1.86e-06 | 0.4796 | 0.3546 | 0.6488 |
| condition[T.C_image_transcribe]:model[T.InternVL3-8B] | -0.4625 | 0.1545 | -2.9939 | 0.0028 | 0.6297 | 0.4652 | 0.8524 |
| condition[T.B_image]:model[T.Qwen2.5-VL-32B] | -0.4778 | 0.1694 | -2.8205 | 0.0048 | 0.6202 | 0.4449 | 0.8644 |
| condition[T.C_image_transcribe]:model[T.Qwen2.5-VL-32B] | -0.1784 | 0.1712 | -1.0419 | 0.2974 | 0.8366 | 0.5981 | 1.1702 |
| condition[T.B_image]:model[T.Qwen2.5-VL-3B] | -0.1256 | 0.1490 | -0.8426 | 0.3994 | 0.8820 | 0.6586 | 1.1812 |
| condition[T.C_image_transcribe]:model[T.Qwen2.5-VL-3B] | -0.3897 | 0.1489 | -2.6177 | 0.0089 | 0.6772 | 0.5058 | 0.9067 |
| condition[T.B_image]:model[T.gemma-3-12b] | -0.9690 | 0.1584 | -6.1185 | 9.44e-10 | 0.3795 | 0.2782 | 0.5176 |
| condition[T.C_image_transcribe]:model[T.gemma-3-12b] | -0.5940 | 0.1593 | -3.7289 | 1.92e-04 | 0.5521 | 0.4040 | 0.7544 |
| sd(item intercept) | 2.2363 | 0.0628 |  |  |  | 2.1164 | 2.3630 |

### Likelihood-ratio tests (runs 1-3)
source: `results/analysis/glmm_lrt.csv`

| run | test | loglik_full | loglik_reduced | lr_stat | df | p_value |
|---|---|---|---|---|---|---|
| 1 | no condition:model | -9061 | -9093 | 63.78 | 8 | 8.41e-11 |
| 1 | no condition:content | -9061 | -9079 | 37.57 | 4 | 1.37e-07 |
| 1 | no condition terms | -9061 | -9153 | 184.1 | 14 | 9.47e-32 |
| 2 | no condition:model | -8895 | -8928 | 65.22 | 8 | 4.37e-11 |
| 2 | no condition:content | -8895 | -8909 | 27.87 | 4 | 1.33e-05 |
| 2 | no condition terms | -8895 | -8993 | 196.2 | 14 | 3.23e-34 |
| 3 | no condition:model | -9015 | -9045 | 60.46 | 8 | 3.78e-10 |
| 3 | no condition:content | -9015 | -9031 | 31.86 | 4 | 2.05e-06 |
| 3 | no condition terms | -9015 | -9107 | 184.7 | 14 | 7.29e-32 |

### A vs B per cell from the GLMM (conditional odds ratio, Holm over 15 per run)
source: `results/analysis/glmm_cell_contrasts.csv`

- p_holm < .05: run 1 8/15, run 2 10/15, run 3 9/15

| model | content_type | odds_ratio_run1 | odds_ratio_run2 | odds_ratio_run3 | p_holm_within_comparison_run1 | p_holm_within_comparison_run2 | p_holm_within_comparison_run3 |
|---|---|---|---|---|---|---|---|
| InternVL3-8B | code | 2.8068 | 2.8826 | 3.0897 | 5.38e-15 | 1.83e-15 | 1.33e-17 |
| InternVL3-8B | math | 2.0427 | 1.9687 | 2.3634 | 3.65e-05 | 1.61e-04 | 3.36e-07 |
| InternVL3-8B | table | 1.5538 | 1.6643 | 1.7172 | 0.0035 | 4.76e-04 | 1.49e-04 |
| Qwen2.5-VL-32B | code | 2.1708 | 2.3881 | 2.3103 | 6.03e-07 | 1.95e-08 | 7.51e-08 |
| Qwen2.5-VL-32B | math | 1.5798 | 1.6309 | 1.7673 | 0.0592 | 0.0397 | 0.0081 |
| Qwen2.5-VL-32B | table | 1.2017 | 1.3788 | 1.2840 | 0.6342 | 0.1354 | 0.3410 |
| Qwen2.5-VL-3B | code | 1.5264 | 1.6367 | 1.6024 | 0.0047 | 5.83e-04 | 0.0010 |
| Qwen2.5-VL-3B | math | 1.1108 | 1.1178 | 1.2257 | 0.9169 | 1.0000 | 0.4515 |
| Qwen2.5-VL-3B | table | 0.8450 | 0.9450 | 0.8906 | 0.6342 | 1.0000 | 0.6657 |
| Qwen2.5-VL-7B | code | 1.3462 | 1.4163 | 1.3227 | 0.0991 | 0.0397 | 0.1250 |
| Qwen2.5-VL-7B | math | 0.9797 | 0.9672 | 1.0118 | 0.9169 | 1.0000 | 0.9383 |
| Qwen2.5-VL-7B | table | 0.7452 | 0.8177 | 0.7351 | 0.0991 | 0.4185 | 0.0736 |
| gemma-3-12b | code | 3.5476 | 3.3700 | 3.2489 | 6.56e-21 | 6.44e-19 | 4.27e-18 |
| gemma-3-12b | math | 2.5818 | 2.3015 | 2.4852 | 4.19e-08 | 3.92e-06 | 1.74e-07 |
| gemma-3-12b | table | 1.9639 | 1.9457 | 1.8056 | 2.03e-06 | 4.37e-06 | 5.61e-05 |

- checks (run 1): GH 40 vs 80 nodes and statsmodels VB — source: `results/analysis/glmm_checks.csv`

## Replication summary, OWNER plan rule (post hoc: replicates = Holm-sig same direction in >= 2/3 runs)
source: `results/analysis/replication_full_summary.csv`

- replicates: 5/15 cells

| model_id | content_type | n_sig_same_dir | sig_direction | replicates | diff_run1 | diff_min | diff_max | max_abs_diff_across_runs |
|---|---|---|---|---|---|---|---|---|
| InternVL3-8B | code | 3 | A>B | True | 0.126 | 0.110 | 0.130 | 0.020 |
| InternVL3-8B | math | 3 | A>B | True | 0.056 | 0.052 | 0.056 | 0.004 |
| InternVL3-8B | table | 2 | A>B | True | 0.060 | 0.060 | 0.088 | 0.028 |
| Qwen2.5-VL-32B | code | 3 | A>B | True | 0.082 | 0.082 | 0.086 | 0.004 |
| Qwen2.5-VL-32B | math | 0 | none | False | 0.016 | 0.016 | 0.016 | 0.000 |
| Qwen2.5-VL-32B | table | 0 | none | False | 0.018 | 0.018 | 0.036 | 0.018 |
| Qwen2.5-VL-3B | code | 0 | none | False | 0.044 | 0.044 | 0.060 | 0.016 |
| Qwen2.5-VL-3B | math | 0 | none | False | 0.022 | 0.006 | 0.040 | 0.034 |
| Qwen2.5-VL-3B | table | 0 | none | False | -0.026 | -0.030 | 0.000 | 0.030 |
| Qwen2.5-VL-7B | code | 0 | none | False | 0.034 | 0.034 | 0.044 | 0.010 |
| Qwen2.5-VL-7B | math | 0 | none | False | 0.000 | -0.002 | 0.004 | 0.006 |
| Qwen2.5-VL-7B | table | 0 | none | False | -0.038 | -0.040 | -0.032 | 0.008 |
| gemma-3-12b | code | 3 | A>B | True | 0.194 | 0.188 | 0.198 | 0.010 |
| gemma-3-12b | math | 0 | none | False | 0.014 | 0.014 | 0.018 | 0.004 |
| gemma-3-12b | table | 1 | A>B | False | 0.086 | 0.058 | 0.086 | 0.028 |

### Run-to-run agreement per model × condition
source: `results/analysis/replication_full_agreement.csv`

- % identical response text: 35.8-62.1; % correctness agreement: 89.9-98.0; Cohen's kappa: 0.795-0.932; |Δacc| max 0.013

| model_id | condition | pair | pct_identical_text | pct_correct_agree | cohen_kappa | abs_delta_acc |
|---|---|---|---|---|---|---|
| InternVL3-8B | A_text | main-rep2 | 38.667 | 94.133 | 0.849 | 0.004 |
| InternVL3-8B | A_text | main-rep3 | 37.267 | 94.067 | 0.846 | 0.011 |
| InternVL3-8B | A_text | rep2-rep3 | 37.067 | 94.867 | 0.866 | 0.007 |
| InternVL3-8B | B_image | main-rep2 | 41.667 | 93.800 | 0.863 | 0.002 |
| InternVL3-8B | B_image | main-rep3 | 43.133 | 93.267 | 0.851 | 6.67e-04 |
| InternVL3-8B | B_image | rep2-rep3 | 41.267 | 93.200 | 0.850 | 0.001 |
| InternVL3-8B | C_image_transcribe | main-rep2 | 40.667 | 94.533 | 0.874 | 0.003 |
| InternVL3-8B | C_image_transcribe | main-rep3 | 39.200 | 94.400 | 0.871 | 0.003 |
| InternVL3-8B | C_image_transcribe | rep2-rep3 | 40.800 | 94.667 | 0.878 | 0.000 |
| Qwen2.5-VL-32B | A_text | main-rep2 | 46.867 | 98.000 | 0.922 | 0.005 |
| Qwen2.5-VL-32B | A_text | main-rep3 | 45.200 | 97.733 | 0.911 | 0.007 |
| Qwen2.5-VL-32B | A_text | rep2-rep3 | 47.333 | 97.600 | 0.904 | 0.001 |
| Qwen2.5-VL-32B | B_image | main-rep2 | 46.867 | 96.467 | 0.886 | 0.002 |
| Qwen2.5-VL-32B | B_image | main-rep3 | 46.933 | 96.600 | 0.890 | 0.002 |
| Qwen2.5-VL-32B | B_image | rep2-rep3 | 45.133 | 96.400 | 0.884 | 0.004 |
| Qwen2.5-VL-32B | C_image_transcribe | main-rep2 | 38.333 | 97.400 | 0.907 | 0.003 |
| Qwen2.5-VL-32B | C_image_transcribe | main-rep3 | 38.400 | 97.533 | 0.912 | 0.002 |
| Qwen2.5-VL-32B | C_image_transcribe | rep2-rep3 | 41.933 | 97.333 | 0.904 | 0.001 |
| Qwen2.5-VL-3B | A_text | main-rep2 | 40.267 | 91.600 | 0.830 | 0.009 |
| Qwen2.5-VL-3B | A_text | main-rep3 | 38.800 | 89.867 | 0.795 | 0.003 |
| Qwen2.5-VL-3B | A_text | rep2-rep3 | 39.000 | 91.067 | 0.819 | 0.012 |
| Qwen2.5-VL-3B | B_image | main-rep2 | 38.733 | 92.733 | 0.854 | 6.67e-04 |
| Qwen2.5-VL-3B | B_image | main-rep3 | 39.600 | 92.800 | 0.855 | 0.011 |
| Qwen2.5-VL-3B | B_image | rep2-rep3 | 39.200 | 92.600 | 0.851 | 0.011 |
| Qwen2.5-VL-3B | C_image_transcribe | main-rep2 | 35.800 | 91.067 | 0.821 | 0.013 |
| Qwen2.5-VL-3B | C_image_transcribe | main-rep3 | 37.133 | 91.000 | 0.820 | 0.002 |
| Qwen2.5-VL-3B | C_image_transcribe | rep2-rep3 | 38.533 | 90.600 | 0.812 | 0.011 |
| Qwen2.5-VL-7B | A_text | main-rep2 | 39.267 | 93.067 | 0.842 | 0.004 |
| Qwen2.5-VL-7B | A_text | main-rep3 | 38.533 | 93.133 | 0.845 | 0.005 |
| Qwen2.5-VL-7B | A_text | rep2-rep3 | 39.667 | 92.867 | 0.838 | 0.009 |
| Qwen2.5-VL-7B | B_image | main-rep2 | 45.533 | 94.000 | 0.864 | 0.003 |
| Qwen2.5-VL-7B | B_image | main-rep3 | 46.400 | 93.867 | 0.861 | 0.004 |
| Qwen2.5-VL-7B | B_image | rep2-rep3 | 43.933 | 94.533 | 0.876 | 0.001 |
| Qwen2.5-VL-7B | C_image_transcribe | main-rep2 | 45.600 | 95.467 | 0.897 | 0.003 |
| Qwen2.5-VL-7B | C_image_transcribe | main-rep3 | 45.400 | 95.200 | 0.891 | 0.000 |
| Qwen2.5-VL-7B | C_image_transcribe | rep2-rep3 | 44.600 | 95.867 | 0.906 | 0.003 |
| gemma-3-12b | A_text | main-rep2 | 62.133 | 97.733 | 0.932 | 0.001 |
| gemma-3-12b | A_text | main-rep3 | 61.333 | 97.000 | 0.910 | 0.002 |
| gemma-3-12b | A_text | rep2-rep3 | 61.267 | 97.133 | 0.914 | 0.003 |
| gemma-3-12b | B_image | main-rep2 | 52.867 | 96.533 | 0.918 | 0.008 |
| gemma-3-12b | B_image | main-rep3 | 52.800 | 96.800 | 0.924 | 0.007 |
| gemma-3-12b | B_image | rep2-rep3 | 52.667 | 96.933 | 0.927 | 0.001 |
| gemma-3-12b | C_image_transcribe | main-rep2 | 47.333 | 95.933 | 0.896 | 0.005 |
| gemma-3-12b | C_image_transcribe | main-rep3 | 47.400 | 96.800 | 0.918 | 0.005 |
| gemma-3-12b | C_image_transcribe | rep2-rep3 | 46.733 | 96.467 | 0.909 | 6.67e-04 |

### Extension A vs B, plan's Holm family of 6 (Gemma-27B, Qwen-72B-AWQ)
source: `results/analysis/ext_rq1_A_vs_B_family6.csv`

| model_id | content_type | acc_first | acc_second | diff | diff_ci_lo | diff_ci_hi | p_holm_family12 | p_holm_family6 |
|---|---|---|---|---|---|---|---|---|
| Qwen2.5-VL-72B-AWQ | code | 0.798 | 0.758 | 0.040 | 0.006 | 0.074 | 0.133 | 0.106 |
| Qwen2.5-VL-72B-AWQ | math | 0.966 | 0.956 | 0.010 | -0.004 | 0.026 | 0.680 | 0.453 |
| Qwen2.5-VL-72B-AWQ | table | 0.812 | 0.808 | 0.004 | -0.029 | 0.037 | 0.905 | 0.905 |
| gemma-3-27b | code | 0.758 | 0.612 | 0.146 | 0.107 | 0.185 | 7.00e-12 | 3.82e-12 |
| gemma-3-27b | math | 0.972 | 0.946 | 0.026 | 0.007 | 0.047 | 0.074 | 0.053 |
| gemma-3-27b | table | 0.778 | 0.742 | 0.036 | -0.004 | 0.076 | 0.380 | 0.285 |

## Resolution control (exploratory; condition B only)
source: `results/analysis/res_B_vs_B.csv`

- Holm over 9 cells; p_holm < .05: 0

| model_id | content_type | setting_first | setting_second | acc_B_original | acc_B_rescontrol | diff_original_minus_rescontrol | diff_ci_lo | diff_ci_hi | b_first_only | c_second_only | p_holm |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Qwen2.5-VL-7B | code | native resolution | stretched to 896x896 | 0.490 | 0.486 | 0.004 | -0.031 | 0.039 | 40 | 38 | 1.000 |
| Qwen2.5-VL-7B | math | native resolution | stretched to 896x896 | 0.868 | 0.872 | -0.004 | -0.029 | 0.021 | 18 | 20 | 1.000 |
| Qwen2.5-VL-7B | table | native resolution | stretched to 896x896 | 0.664 | 0.650 | 0.014 | -0.021 | 0.049 | 42 | 35 | 1.000 |
| Qwen2.5-VL-32B | code | native resolution | stretched to 896x896 | 0.730 | 0.764 | -0.034 | -0.066 | -0.002 | 25 | 42 | 0.398 |
| Qwen2.5-VL-32B | math | native resolution | stretched to 896x896 | 0.902 | 0.906 | -0.004 | -0.030 | 0.022 | 20 | 22 | 1.000 |
| Qwen2.5-VL-32B | table | native resolution | stretched to 896x896 | 0.794 | 0.782 | 0.012 | -0.015 | 0.039 | 26 | 20 | 1.000 |
| gemma-3-12b | code | 896x896 + pan-and-scan | 896x896, no pan-and-scan | 0.494 | 0.492 | 0.002 | -0.019 | 0.023 | 14 | 13 | 1.000 |
| gemma-3-12b | math | 896x896 + pan-and-scan | 896x896, no pan-and-scan | 0.934 | 0.928 | 0.006 | -0.004 | 0.017 | 3 | 0 | 1.000 |
| gemma-3-12b | table | 896x896 + pan-and-scan | 896x896, no pan-and-scan | 0.648 | 0.594 | 0.054 | 0.015 | 0.093 | 64 | 37 | 0.084 |

### A−B gap under each image setting (A = run-1 text)
source: `results/analysis/res_gap_A_minus_B_by_setting.csv`

| model_id | content_type | B_setting | acc_first | acc_second | gap_A_minus_B | diff_ci_lo | diff_ci_hi | p_holm |
|---|---|---|---|---|---|---|---|---|
| Qwen2.5-VL-7B | code | native resolution | 0.524 | 0.490 | 0.034 | -0.005 | 0.072 | 1.000 |
| Qwen2.5-VL-7B | math | native resolution | 0.868 | 0.868 | 0.000 | -0.026 | 0.026 | 1.000 |
| Qwen2.5-VL-7B | table | native resolution | 0.626 | 0.664 | -0.038 | -0.080 | 0.004 | 1.000 |
| Qwen2.5-VL-7B | code | stretched to 896x896 | 0.524 | 0.486 | 0.038 | -0.004 | 0.079 | 1.000 |
| Qwen2.5-VL-7B | math | stretched to 896x896 | 0.868 | 0.872 | -0.004 | -0.031 | 0.023 | 1.000 |
| Qwen2.5-VL-7B | table | stretched to 896x896 | 0.626 | 0.650 | -0.024 | -0.064 | 0.016 | 1.000 |
| Qwen2.5-VL-32B | code | native resolution | 0.812 | 0.730 | 0.082 | 0.053 | 0.112 | 7.90e-07 |
| Qwen2.5-VL-32B | math | native resolution | 0.918 | 0.902 | 0.016 | -0.013 | 0.046 | 1.000 |
| Qwen2.5-VL-32B | table | native resolution | 0.812 | 0.794 | 0.018 | -0.012 | 0.049 | 1.000 |
| Qwen2.5-VL-32B | code | stretched to 896x896 | 0.812 | 0.764 | 0.048 | 0.015 | 0.081 | 0.073 |
| Qwen2.5-VL-32B | math | stretched to 896x896 | 0.918 | 0.906 | 0.012 | -0.018 | 0.042 | 1.000 |
| Qwen2.5-VL-32B | table | stretched to 896x896 | 0.812 | 0.782 | 0.030 | -0.002 | 0.063 | 1.000 |
| gemma-3-12b | code | 896x896 + pan-and-scan | 0.688 | 0.494 | 0.194 | 0.151 | 0.236 | 1.29e-16 |
| gemma-3-12b | math | 896x896 + pan-and-scan | 0.948 | 0.934 | 0.014 | -0.007 | 0.036 | 1.000 |
| gemma-3-12b | table | 896x896 + pan-and-scan | 0.734 | 0.648 | 0.086 | 0.041 | 0.130 | 0.003 |
| gemma-3-12b | code | 896x896, no pan-and-scan | 0.688 | 0.492 | 0.196 | 0.152 | 0.239 | 2.67e-16 |
| gemma-3-12b | math | 896x896, no pan-and-scan | 0.948 | 0.928 | 0.020 | -0.001 | 0.043 | 1.000 |
| gemma-3-12b | table | 896x896, no pan-and-scan | 0.734 | 0.594 | 0.140 | 0.095 | 0.184 | 4.09e-08 |

## Figures

- `results/figures/accuracy_by_condition.png`
- `results/figures/combined_gap_A_minus_B_all_models.png`
- `results/figures/ext_accuracy_by_condition.png`
- `results/figures/ext_gap_A_minus_B_vs_size_qwen.png`
- `results/figures/ext_output_tokens_boxplot.png`
- `results/figures/ext_replication_full_accuracy_runs.png`
- `results/figures/gap_A_minus_B_vs_size_by_family.png`
- `results/figures/gap_A_minus_B_vs_size_qwen.png`
- `results/figures/gap_vs_size_all.png`
- `results/figures/output_tokens_boxplot.png`
- `results/figures/replication_full_accuracy_runs.png`

