# Numeric summary

<!--
study_id: vlm-modality-v1
git_commit: c91952f507ba96fede27e4f541daf902d4d43114-dirty
created_utc: 2026-11-15T19:34:20Z
-->

Numbers, tables and figures only. Figures: `results/figures/`. All CSVs: `results/analysis/`.

## Final model list

| model | params_b | revision | tp | vllm | image_processing |
|---|---|---|---|---|---|
| Qwen/Qwen2.5-VL-3B-Instruct | 3 | 66285546d2b821cf421d4f5eb2576359d3770cd3 | 1 | 0.33.0 | Qwen2.5-VL native resolution; smart_resize rounds each side to a multiple of 28 (<=14 px change), max_pixels 12.8 MP > largest image, so no downscaling |
| Qwen/Qwen2.5-VL-7B-Instruct | 7 | cc594898137f460bfe9f0759e9844b3ce807cfb5 | 1 | 0.33.0 | Qwen2.5-VL native resolution; smart_resize rounds each side to a multiple of 28 (<=14 px change), max_pixels 12.8 MP > largest image, so no downscaling |
| OpenGVLab/InternVL3-8B | 8 | 853e3a797a661694b1b8ece0cb72dc2b23e3dac9 | 1 | 0.33.0 | InternVL3 dynamic tiling, 448 px tiles, max_dynamic_patch=24 (+thumbnail); image is resized to the closest tile grid (can up- or downscale slightly) |
| google/gemma-3-12b-it | 12 | 96b6f1eccf38110c56df3a15bffe176da04bfd80 | 1 | 0.33.0 | Gemma 3 SigLIP encoder is fixed at 896x896: every image is resized to 896x896 (DOWNSCALES wide images); pan-and-scan adds 896x896 crops of the full-resolution image |
| Qwen/Qwen2.5-VL-32B-Instruct | 32 | 7cfb30d71a1f4f49a57592323337a4a4727301da | 2 | 0.33.0 | Qwen2.5-VL native resolution; smart_resize rounds each side to a multiple of 28 (<=14 px change), max_pixels 12.8 MP > largest image, so no downscaling |

## Exclusions (before sampling; reasons not mutually exclusive)

| content | total | excluded | eligible | reason_max_line_chars | reason_max_lines | reason_table_max_rows | reason_render_fails | pilot | main |
|---|---|---|---|---|---|---|---|---|---|
| code | 800 | 3 | 797 | 0 | 0 | 0 | 3 | 30 | 500 |
| math | 1319 | 0 | 1319 | 0 | 0 | 0 | 0 | 30 | 500 |
| table | 4344 | 1396 | 2948 | 1064 | 305 | 487 | 43 | 30 | 500 |

## Input length (main items)

| content_type | n_items | chars_mean | chars_median | chars_min | chars_max | lines_mean | lines_median | lines_min | lines_max |
|---|---|---|---|---|---|---|---|---|---|
| code | 500 | 169.4 | 166.0 | 72 | 296 | 7.5 | 7 | 4 | 14 |
| math | 500 | 233.3 | 215.0 | 83 | 694 | 3.4 | 3 | 2 | 9 |
| table | 500 | 1735.3 | 1452.5 | 474 | 5880 | 20.4 | 18 | 10 | 45 |

## T07b replication check (pilot, 2 runs)

| model_id | condition | n | pct_identical_text | pct_correct_agree | kappa_correct | acc_run1 | acc_run2 | abs_acc_diff |
|---|---|---|---|---|---|---|---|---|
| InternVL3-8B | A_text | 90 | 42.222 | 97.778 | 0.946 | 0.722 | 0.700 | 0.022 |
| InternVL3-8B | B_image | 90 | 37.778 | 95.556 | 0.898 | 0.689 | 0.667 | 0.022 |
| InternVL3-8B | C_image_transcribe | 90 | 40.000 | 95.556 | 0.905 | 0.633 | 0.611 | 0.022 |
| Qwen2.5-VL-32B-Instruct | A_text | 90 | 43.333 | 97.778 | 0.933 | 0.800 | 0.778 | 0.022 |
| Qwen2.5-VL-32B-Instruct | B_image | 90 | 45.556 | 97.778 | 0.942 | 0.756 | 0.733 | 0.022 |
| Qwen2.5-VL-32B-Instruct | C_image_transcribe | 90 | 34.444 | 98.889 | 0.970 | 0.744 | 0.756 | 0.011 |
| Qwen2.5-VL-3B-Instruct | A_text | 90 | 33.333 | 90.000 | 0.798 | 0.567 | 0.533 | 0.033 |
| Qwen2.5-VL-3B-Instruct | B_image | 90 | 32.222 | 92.222 | 0.844 | 0.522 | 0.511 | 0.011 |
| Qwen2.5-VL-3B-Instruct | C_image_transcribe | 90 | 28.889 | 88.889 | 0.772 | 0.578 | 0.578 | 0.000 |
| Qwen2.5-VL-7B-Instruct | A_text | 90 | 41.111 | 95.556 | 0.889 | 0.711 | 0.733 | 0.022 |
| Qwen2.5-VL-7B-Instruct | B_image | 90 | 42.222 | 94.444 | 0.878 | 0.644 | 0.656 | 0.011 |
| Qwen2.5-VL-7B-Instruct | C_image_transcribe | 90 | 48.889 | 95.556 | 0.903 | 0.656 | 0.633 | 0.022 |
| gemma-3-12b-it | A_text | 90 | 63.333 | 95.556 | 0.880 | 0.778 | 0.733 | 0.044 |
| gemma-3-12b-it | B_image | 90 | 46.667 | 98.889 | 0.972 | 0.733 | 0.722 | 0.011 |
| gemma-3-12b-it | C_image_transcribe | 90 | 35.556 | 92.222 | 0.798 | 0.733 | 0.744 | 0.011 |

- cells with correct-agreement < 95%: 5 of 15 (pre-registered threshold 95%)

## T11 accuracy per model × content × condition (95% Wilson CI)

| model_id | content_type | condition | n | accuracy | ci95_lo | ci95_hi | parse_rate | parse_rate_strict | accuracy_strict | pct_finish_length |
|---|---|---|---|---|---|---|---|---|---|---|
| Qwen2.5-VL-3B-Instruct | code | A_text | 500 | 0.386 | 0.344 | 0.429 | 0.960 | 0.948 | 0.386 | 2.800 |
| Qwen2.5-VL-3B-Instruct | code | B_image | 500 | 0.342 | 0.302 | 0.385 | 0.944 | 0.932 | 0.338 | 3.600 |
| Qwen2.5-VL-3B-Instruct | code | C_image_transcribe | 500 | 0.358 | 0.317 | 0.401 | 0.958 | 0.958 | 0.358 | 3.400 |
| Qwen2.5-VL-3B-Instruct | math | A_text | 500 | 0.840 | 0.805 | 0.870 | 0.998 | 0.992 | 0.836 | 0.000 |
| Qwen2.5-VL-3B-Instruct | math | B_image | 500 | 0.818 | 0.782 | 0.849 | 0.982 | 0.974 | 0.818 | 0.000 |
| Qwen2.5-VL-3B-Instruct | math | C_image_transcribe | 500 | 0.752 | 0.712 | 0.788 | 0.934 | 0.932 | 0.752 | 0.200 |
| Qwen2.5-VL-3B-Instruct | table | A_text | 500 | 0.428 | 0.385 | 0.472 | 0.814 | 0.814 | 0.428 | 1.400 |
| Qwen2.5-VL-3B-Instruct | table | B_image | 500 | 0.454 | 0.411 | 0.498 | 0.954 | 0.954 | 0.454 | 1.200 |
| Qwen2.5-VL-3B-Instruct | table | C_image_transcribe | 500 | 0.392 | 0.350 | 0.435 | 0.834 | 0.834 | 0.392 | 1.000 |
| Qwen2.5-VL-7B-Instruct | code | A_text | 500 | 0.524 | 0.480 | 0.567 | 0.972 | 0.972 | 0.524 | 2.600 |
| Qwen2.5-VL-7B-Instruct | code | B_image | 500 | 0.490 | 0.446 | 0.534 | 0.978 | 0.964 | 0.484 | 2.200 |
| Qwen2.5-VL-7B-Instruct | code | C_image_transcribe | 500 | 0.480 | 0.437 | 0.524 | 0.970 | 0.970 | 0.480 | 2.400 |
| Qwen2.5-VL-7B-Instruct | math | A_text | 500 | 0.868 | 0.836 | 0.895 | 0.994 | 0.990 | 0.868 | 0.400 |
| Qwen2.5-VL-7B-Instruct | math | B_image | 500 | 0.868 | 0.836 | 0.895 | 0.992 | 0.990 | 0.868 | 0.000 |
| Qwen2.5-VL-7B-Instruct | math | C_image_transcribe | 500 | 0.866 | 0.833 | 0.893 | 0.994 | 0.994 | 0.866 | 0.200 |
| Qwen2.5-VL-7B-Instruct | table | A_text | 500 | 0.626 | 0.583 | 0.667 | 0.996 | 0.996 | 0.626 | 0.200 |
| Qwen2.5-VL-7B-Instruct | table | B_image | 500 | 0.664 | 0.621 | 0.704 | 0.996 | 0.996 | 0.664 | 0.400 |
| Qwen2.5-VL-7B-Instruct | table | C_image_transcribe | 500 | 0.668 | 0.626 | 0.708 | 0.994 | 0.994 | 0.668 | 0.600 |
| InternVL3-8B | code | A_text | 500 | 0.632 | 0.589 | 0.673 | 0.994 | 0.994 | 0.632 | 0.600 |
| InternVL3-8B | code | B_image | 500 | 0.506 | 0.462 | 0.550 | 0.994 | 0.990 | 0.506 | 0.600 |
| InternVL3-8B | code | C_image_transcribe | 500 | 0.522 | 0.478 | 0.565 | 0.994 | 0.992 | 0.522 | 0.600 |
| InternVL3-8B | math | A_text | 500 | 0.920 | 0.893 | 0.941 | 0.998 | 0.998 | 0.920 | 0.200 |
| InternVL3-8B | math | B_image | 500 | 0.864 | 0.831 | 0.891 | 0.992 | 0.992 | 0.864 | 0.200 |
| InternVL3-8B | math | C_image_transcribe | 500 | 0.894 | 0.864 | 0.918 | 0.994 | 0.994 | 0.894 | 0.200 |
| InternVL3-8B | table | A_text | 500 | 0.648 | 0.605 | 0.689 | 1.000 | 1.000 | 0.648 | 0.000 |
| InternVL3-8B | table | B_image | 500 | 0.588 | 0.544 | 0.630 | 0.998 | 0.998 | 0.588 | 0.200 |
| InternVL3-8B | table | C_image_transcribe | 500 | 0.628 | 0.585 | 0.669 | 0.994 | 0.994 | 0.628 | 0.200 |
| gemma-3-12b-it | code | A_text | 500 | 0.688 | 0.646 | 0.727 | 0.998 | 0.998 | 0.688 | 0.200 |
| gemma-3-12b-it | code | B_image | 500 | 0.494 | 0.450 | 0.538 | 0.994 | 0.994 | 0.494 | 0.600 |
| gemma-3-12b-it | code | C_image_transcribe | 500 | 0.542 | 0.498 | 0.585 | 0.998 | 0.998 | 0.542 | 0.200 |
| gemma-3-12b-it | math | A_text | 500 | 0.948 | 0.925 | 0.964 | 1.000 | 1.000 | 0.948 | 0.000 |
| gemma-3-12b-it | math | B_image | 500 | 0.934 | 0.909 | 0.953 | 1.000 | 1.000 | 0.934 | 0.000 |
| gemma-3-12b-it | math | C_image_transcribe | 500 | 0.922 | 0.895 | 0.942 | 1.000 | 1.000 | 0.922 | 0.000 |
| gemma-3-12b-it | table | A_text | 500 | 0.734 | 0.694 | 0.771 | 0.998 | 0.998 | 0.734 | 0.200 |
| gemma-3-12b-it | table | B_image | 500 | 0.648 | 0.605 | 0.689 | 0.998 | 0.998 | 0.648 | 0.200 |
| gemma-3-12b-it | table | C_image_transcribe | 500 | 0.726 | 0.685 | 0.763 | 0.986 | 0.986 | 0.726 | 0.200 |
| Qwen2.5-VL-32B-Instruct | code | A_text | 500 | 0.812 | 0.775 | 0.844 | 0.998 | 0.946 | 0.768 | 0.200 |
| Qwen2.5-VL-32B-Instruct | code | B_image | 500 | 0.730 | 0.689 | 0.767 | 1.000 | 0.930 | 0.682 | 0.000 |
| Qwen2.5-VL-32B-Instruct | code | C_image_transcribe | 500 | 0.740 | 0.700 | 0.777 | 0.998 | 0.534 | 0.410 | 0.200 |
| Qwen2.5-VL-32B-Instruct | math | A_text | 500 | 0.918 | 0.891 | 0.939 | 0.990 | 0.126 | 0.114 | 0.000 |
| Qwen2.5-VL-32B-Instruct | math | B_image | 500 | 0.902 | 0.873 | 0.925 | 0.980 | 0.294 | 0.266 | 0.000 |
| Qwen2.5-VL-32B-Instruct | math | C_image_transcribe | 500 | 0.948 | 0.925 | 0.964 | 0.996 | 0.676 | 0.650 | 0.000 |
| Qwen2.5-VL-32B-Instruct | table | A_text | 500 | 0.812 | 0.775 | 0.844 | 1.000 | 1.000 | 0.812 | 0.000 |
| Qwen2.5-VL-32B-Instruct | table | B_image | 500 | 0.794 | 0.756 | 0.827 | 1.000 | 0.994 | 0.794 | 0.000 |
| Qwen2.5-VL-32B-Instruct | table | C_image_transcribe | 500 | 0.806 | 0.769 | 0.838 | 1.000 | 0.984 | 0.794 | 0.200 |

## T11 output tokens per cell

| model_id | content_type | condition | out_tok_mean | out_tok_median | out_tok_sd | out_tok_iqr | out_tok_min | out_tok_max |
|---|---|---|---|---|---|---|---|---|
| Qwen2.5-VL-3B-Instruct | code | A_text | 486.3 | 327.0 | 684.5 | 189.2 | 117 | 4096 |
| Qwen2.5-VL-3B-Instruct | code | B_image | 532.7 | 333.5 | 778.5 | 173.2 | 115 | 4096 |
| Qwen2.5-VL-3B-Instruct | code | C_image_transcribe | 530.2 | 375.5 | 705.1 | 170.5 | 167 | 4096 |
| Qwen2.5-VL-3B-Instruct | math | A_text | 246.3 | 231.5 | 84.9 | 99.2 | 90 | 594 |
| Qwen2.5-VL-3B-Instruct | math | B_image | 245.4 | 232.5 | 80.5 | 98.5 | 101 | 622 |
| Qwen2.5-VL-3B-Instruct | math | C_image_transcribe | 276.2 | 257.0 | 192.3 | 115.8 | 45 | 4096 |
| Qwen2.5-VL-3B-Instruct | table | A_text | 292.6 | 181.0 | 540.9 | 122.2 | 6 | 4096 |
| Qwen2.5-VL-3B-Instruct | table | B_image | 277.1 | 186.0 | 448.4 | 151.5 | 50 | 4096 |
| Qwen2.5-VL-3B-Instruct | table | C_image_transcribe | 730.9 | 608.5 | 497.3 | 416.2 | 187 | 4096 |
| Qwen2.5-VL-7B-Instruct | code | A_text | 525.1 | 396.0 | 626.6 | 203.8 | 141 | 4096 |
| Qwen2.5-VL-7B-Instruct | code | B_image | 490.5 | 358.5 | 586.4 | 203.8 | 139 | 4096 |
| Qwen2.5-VL-7B-Instruct | code | C_image_transcribe | 479.0 | 351.0 | 604.7 | 177.5 | 123 | 4096 |
| Qwen2.5-VL-7B-Instruct | math | A_text | 276.7 | 249.5 | 257.8 | 105.0 | 79 | 4096 |
| Qwen2.5-VL-7B-Instruct | math | B_image | 236.3 | 224.5 | 80.6 | 92.0 | 79 | 594 |
| Qwen2.5-VL-7B-Instruct | math | C_image_transcribe | 285.2 | 258.5 | 194.1 | 115.0 | 109 | 4096 |
| Qwen2.5-VL-7B-Instruct | table | A_text | 233.6 | 170.5 | 267.4 | 149.2 | 57 | 4096 |
| Qwen2.5-VL-7B-Instruct | table | B_image | 239.1 | 172.0 | 294.8 | 148.5 | 64 | 4096 |
| Qwen2.5-VL-7B-Instruct | table | C_image_transcribe | 713.6 | 615.5 | 439.8 | 416.8 | 225 | 4096 |
| InternVL3-8B | code | A_text | 381.9 | 330.0 | 317.2 | 159.5 | 146 | 4096 |
| InternVL3-8B | code | B_image | 397.2 | 344.0 | 335.7 | 154.0 | 76 | 4096 |
| InternVL3-8B | code | C_image_transcribe | 391.7 | 350.0 | 355.4 | 147.5 | 123 | 4096 |
| InternVL3-8B | math | A_text | 268.1 | 251.0 | 188.0 | 96.0 | 94 | 4096 |
| InternVL3-8B | math | B_image | 226.1 | 210.0 | 195.2 | 121.2 | 62 | 4096 |
| InternVL3-8B | math | C_image_transcribe | 298.4 | 277.5 | 193.9 | 119.0 | 109 | 4096 |
| InternVL3-8B | table | A_text | 184.2 | 141.5 | 129.5 | 120.0 | 23 | 1137 |
| InternVL3-8B | table | B_image | 200.2 | 147.0 | 234.7 | 126.0 | 26 | 4096 |
| InternVL3-8B | table | C_image_transcribe | 688.5 | 598.0 | 388.8 | 405.8 | 204 | 4096 |
| gemma-3-12b-it | code | A_text | 300.0 | 239.0 | 288.6 | 174.2 | 40 | 4096 |
| gemma-3-12b-it | code | B_image | 366.3 | 290.0 | 375.0 | 198.0 | 70 | 4096 |
| gemma-3-12b-it | code | C_image_transcribe | 408.1 | 346.5 | 294.5 | 199.2 | 122 | 4096 |
| gemma-3-12b-it | math | A_text | 169.7 | 146.0 | 106.4 | 95.0 | 53 | 1385 |
| gemma-3-12b-it | math | B_image | 171.9 | 157.0 | 88.0 | 70.0 | 73 | 1504 |
| gemma-3-12b-it | math | C_image_transcribe | 229.9 | 214.5 | 84.0 | 100.2 | 89 | 650 |
| gemma-3-12b-it | table | A_text | 142.2 | 91.0 | 214.4 | 127.2 | 16 | 4096 |
| gemma-3-12b-it | table | B_image | 125.9 | 80.0 | 201.3 | 91.0 | 26 | 4096 |
| gemma-3-12b-it | table | C_image_transcribe | 628.0 | 550.0 | 375.9 | 406.8 | 121 | 4096 |
| Qwen2.5-VL-32B-Instruct | code | A_text | 634.3 | 564.0 | 313.2 | 298.8 | 263 | 4096 |
| Qwen2.5-VL-32B-Instruct | code | B_image | 664.4 | 610.0 | 253.9 | 277.8 | 291 | 2707 |
| Qwen2.5-VL-32B-Instruct | code | C_image_transcribe | 705.1 | 638.5 | 307.8 | 272.0 | 272 | 4096 |
| Qwen2.5-VL-32B-Instruct | math | A_text | 333.0 | 316.0 | 108.7 | 127.5 | 129 | 914 |
| Qwen2.5-VL-32B-Instruct | math | B_image | 340.1 | 324.0 | 113.7 | 145.2 | 117 | 869 |
| Qwen2.5-VL-32B-Instruct | math | C_image_transcribe | 367.4 | 339.5 | 168.0 | 151.8 | 152 | 3118 |
| Qwen2.5-VL-32B-Instruct | table | A_text | 262.0 | 215.0 | 167.7 | 150.5 | 83 | 1890 |
| Qwen2.5-VL-32B-Instruct | table | B_image | 303.8 | 245.0 | 201.8 | 158.5 | 84 | 1830 |
| Qwen2.5-VL-32B-Instruct | table | C_image_transcribe | 850.1 | 749.5 | 426.5 | 466.5 | 330 | 4096 |

## T11 outliers (kept, not dropped)

- output tokens > Q3 + 3·IQR (within cell): 383 responses
- finish_reason = length: 138 responses

| model_id | content_type | condition | n | n_outlier_tokens | n_finish_length |
|---|---|---|---|---|---|
| InternVL3-8B | code | A_text | 500 | 5 | 3 |
| InternVL3-8B | code | B_image | 500 | 8 | 3 |
| InternVL3-8B | code | C_image_transcribe | 500 | 8 | 3 |
| InternVL3-8B | math | A_text | 500 | 1 | 1 |
| InternVL3-8B | math | B_image | 500 | 2 | 1 |
| InternVL3-8B | math | C_image_transcribe | 500 | 2 | 1 |
| InternVL3-8B | table | A_text | 500 | 9 | 0 |
| InternVL3-8B | table | B_image | 500 | 13 | 1 |
| InternVL3-8B | table | C_image_transcribe | 500 | 4 | 1 |
| Qwen2.5-VL-32B-Instruct | code | A_text | 500 | 6 | 1 |
| Qwen2.5-VL-32B-Instruct | code | B_image | 500 | 6 | 0 |
| Qwen2.5-VL-32B-Instruct | code | C_image_transcribe | 500 | 9 | 1 |
| Qwen2.5-VL-32B-Instruct | math | A_text | 500 | 2 | 0 |
| Qwen2.5-VL-32B-Instruct | math | B_image | 500 | 1 | 0 |
| Qwen2.5-VL-32B-Instruct | math | C_image_transcribe | 500 | 1 | 0 |
| Qwen2.5-VL-32B-Instruct | table | A_text | 500 | 8 | 0 |
| Qwen2.5-VL-32B-Instruct | table | B_image | 500 | 15 | 0 |
| Qwen2.5-VL-32B-Instruct | table | C_image_transcribe | 500 | 3 | 1 |
| Qwen2.5-VL-3B-Instruct | code | A_text | 500 | 25 | 14 |
| Qwen2.5-VL-3B-Instruct | code | B_image | 500 | 28 | 18 |
| Qwen2.5-VL-3B-Instruct | code | C_image_transcribe | 500 | 22 | 17 |
| Qwen2.5-VL-3B-Instruct | math | A_text | 500 | 1 | 0 |
| Qwen2.5-VL-3B-Instruct | math | B_image | 500 | 1 | 0 |
| Qwen2.5-VL-3B-Instruct | math | C_image_transcribe | 500 | 2 | 1 |
| Qwen2.5-VL-3B-Instruct | table | A_text | 500 | 18 | 7 |
| Qwen2.5-VL-3B-Instruct | table | B_image | 500 | 15 | 6 |
| Qwen2.5-VL-3B-Instruct | table | C_image_transcribe | 500 | 7 | 5 |
| Qwen2.5-VL-7B-Instruct | code | A_text | 500 | 19 | 13 |
| Qwen2.5-VL-7B-Instruct | code | B_image | 500 | 18 | 11 |
| Qwen2.5-VL-7B-Instruct | code | C_image_transcribe | 500 | 16 | 12 |
| Qwen2.5-VL-7B-Instruct | math | A_text | 500 | 3 | 2 |
| Qwen2.5-VL-7B-Instruct | math | B_image | 500 | 2 | 0 |
| Qwen2.5-VL-7B-Instruct | math | C_image_transcribe | 500 | 3 | 1 |
| Qwen2.5-VL-7B-Instruct | table | A_text | 500 | 10 | 1 |
| Qwen2.5-VL-7B-Instruct | table | B_image | 500 | 12 | 2 |
| Qwen2.5-VL-7B-Instruct | table | C_image_transcribe | 500 | 6 | 3 |
| gemma-3-12b-it | code | A_text | 500 | 13 | 1 |
| gemma-3-12b-it | code | B_image | 500 | 13 | 3 |
| gemma-3-12b-it | code | C_image_transcribe | 500 | 11 | 1 |
| gemma-3-12b-it | math | A_text | 500 | 4 | 0 |
| gemma-3-12b-it | math | B_image | 500 | 6 | 0 |
| gemma-3-12b-it | math | C_image_transcribe | 500 | 4 | 0 |
| gemma-3-12b-it | table | A_text | 500 | 8 | 1 |
| gemma-3-12b-it | table | B_image | 500 | 11 | 1 |
| gemma-3-12b-it | table | C_image_transcribe | 500 | 2 | 1 |

## T12 RQ1 McNemar A vs B (primary; Holm within family)

| model_id | content_type | n_pairs | acc_first | acc_second | b_first_only | c_second_only | diff | diff_ci_lo | diff_ci_hi | discordant_or | or_ci_lo | or_ci_hi | p_mcnemar_exact | p_holm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| InternVL3-8B | code | 500 | 0.632 | 0.506 | 89 | 26 | 0.126 | 0.085 | 0.166 | 3.423 | 2.190 | 5.523 | 2.95e-09 | 4.13e-08 |
| InternVL3-8B | math | 500 | 0.920 | 0.864 | 43 | 15 | 0.056 | 0.026 | 0.087 | 2.867 | 1.561 | 5.555 | 3.07e-04 | 0.003 |
| InternVL3-8B | table | 500 | 0.648 | 0.588 | 87 | 57 | 0.060 | 0.013 | 0.107 | 1.526 | 1.081 | 2.171 | 0.015 | 0.154 |
| Qwen2.5-VL-32B-Instruct | code | 500 | 0.812 | 0.730 | 50 | 9 | 0.082 | 0.053 | 0.112 | 5.556 | 2.705 | 12.850 | 5.26e-08 | 6.84e-07 |
| Qwen2.5-VL-32B-Instruct | math | 500 | 0.918 | 0.902 | 31 | 23 | 0.016 | -0.013 | 0.046 | 1.348 | 0.761 | 2.421 | 0.341 | 1.000 |
| Qwen2.5-VL-32B-Instruct | table | 500 | 0.812 | 0.794 | 34 | 25 | 0.018 | -0.012 | 0.049 | 1.360 | 0.788 | 2.378 | 0.298 | 1.000 |
| Qwen2.5-VL-3B-Instruct | code | 500 | 0.386 | 0.342 | 72 | 50 | 0.044 | 6.78e-04 | 0.087 | 1.440 | 0.990 | 2.109 | 0.057 | 0.511 |
| Qwen2.5-VL-3B-Instruct | math | 500 | 0.840 | 0.818 | 38 | 27 | 0.022 | -0.010 | 0.054 | 1.407 | 0.837 | 2.397 | 0.215 | 1.000 |
| Qwen2.5-VL-3B-Instruct | table | 500 | 0.428 | 0.454 | 82 | 95 | -0.026 | -0.078 | 0.026 | 0.863 | 0.634 | 1.172 | 0.367 | 1.000 |
| Qwen2.5-VL-7B-Instruct | code | 500 | 0.524 | 0.490 | 57 | 40 | 0.034 | -0.005 | 0.072 | 1.425 | 0.935 | 2.191 | 0.104 | 0.726 |
| Qwen2.5-VL-7B-Instruct | math | 500 | 0.868 | 0.868 | 20 | 20 | 0.000 | -0.026 | 0.026 | 1.000 | 0.511 | 1.958 | 1.000 | 1.000 |
| Qwen2.5-VL-7B-Instruct | table | 500 | 0.626 | 0.664 | 47 | 66 | -0.038 | -0.080 | 0.004 | 0.712 | 0.479 | 1.051 | 0.090 | 0.720 |
| gemma-3-12b-it | code | 500 | 0.688 | 0.494 | 117 | 20 | 0.194 | 0.151 | 0.236 | 5.850 | 3.621 | 9.928 | 7.16e-18 | 1.07e-16 |
| gemma-3-12b-it | math | 500 | 0.948 | 0.934 | 17 | 10 | 0.014 | -0.007 | 0.036 | 1.700 | 0.735 | 4.154 | 0.248 | 1.000 |
| gemma-3-12b-it | table | 500 | 0.734 | 0.648 | 88 | 45 | 0.086 | 0.041 | 0.130 | 1.956 | 1.350 | 2.867 | 2.42e-04 | 0.003 |

## T12 RQ1 McNemar A vs B (sensitivity: unparseable pairs excluded; Holm within family)

| model_id | content_type | n_pairs | acc_first | acc_second | b_first_only | c_second_only | diff | diff_ci_lo | diff_ci_hi | discordant_or | or_ci_lo | or_ci_hi | p_mcnemar_exact | p_holm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| InternVL3-8B | code | 496 | 0.637 | 0.510 | 89 | 26 | 0.127 | 0.086 | 0.168 | 3.423 | 2.190 | 5.523 | 2.95e-09 | 4.13e-08 |
| InternVL3-8B | math | 496 | 0.921 | 0.871 | 40 | 15 | 0.050 | 0.021 | 0.081 | 2.667 | 1.441 | 5.197 | 0.001 | 0.011 |
| InternVL3-8B | table | 499 | 0.649 | 0.589 | 87 | 57 | 0.060 | 0.013 | 0.107 | 1.526 | 1.081 | 2.171 | 0.015 | 0.154 |
| Qwen2.5-VL-32B-Instruct | code | 499 | 0.814 | 0.731 | 50 | 9 | 0.082 | 0.053 | 0.112 | 5.556 | 2.705 | 12.850 | 5.26e-08 | 6.84e-07 |
| Qwen2.5-VL-32B-Instruct | math | 486 | 0.928 | 0.922 | 23 | 20 | 0.006 | -0.021 | 0.034 | 1.150 | 0.604 | 2.208 | 0.761 | 1.000 |
| Qwen2.5-VL-32B-Instruct | table | 500 | 0.812 | 0.794 | 34 | 25 | 0.018 | -0.012 | 0.049 | 1.360 | 0.788 | 2.378 | 0.298 | 1.000 |
| Qwen2.5-VL-3B-Instruct | code | 464 | 0.407 | 0.362 | 68 | 47 | 0.045 | -6.33e-05 | 0.090 | 1.447 | 0.983 | 2.145 | 0.062 | 0.527 |
| Qwen2.5-VL-3B-Instruct | math | 490 | 0.847 | 0.833 | 33 | 26 | 0.014 | -0.017 | 0.046 | 1.269 | 0.736 | 2.210 | 0.435 | 1.000 |
| Qwen2.5-VL-3B-Instruct | table | 391 | 0.524 | 0.488 | 73 | 59 | 0.036 | -0.022 | 0.093 | 1.237 | 0.866 | 1.774 | 0.258 | 1.000 |
| Qwen2.5-VL-7B-Instruct | code | 477 | 0.545 | 0.505 | 55 | 36 | 0.040 | 6.00e-04 | 0.079 | 1.528 | 0.986 | 2.394 | 0.059 | 0.527 |
| Qwen2.5-VL-7B-Instruct | math | 493 | 0.876 | 0.878 | 18 | 19 | -0.002 | -0.027 | 0.023 | 0.947 | 0.469 | 1.907 | 1.000 | 1.000 |
| Qwen2.5-VL-7B-Instruct | table | 496 | 0.629 | 0.667 | 46 | 65 | -0.038 | -0.080 | 0.003 | 0.708 | 0.474 | 1.048 | 0.087 | 0.610 |
| gemma-3-12b-it | code | 496 | 0.688 | 0.496 | 114 | 19 | 0.192 | 0.148 | 0.233 | 6.000 | 3.671 | 10.331 | 1.06e-17 | 1.58e-16 |
| gemma-3-12b-it | math | 500 | 0.948 | 0.934 | 17 | 10 | 0.014 | -0.007 | 0.036 | 1.700 | 0.735 | 4.154 | 0.248 | 1.000 |
| gemma-3-12b-it | table | 498 | 0.735 | 0.649 | 87 | 44 | 0.086 | 0.042 | 0.131 | 1.977 | 1.361 | 2.910 | 2.16e-04 | 0.003 |

## T12 RQ1 McNemar A vs B (sensitivity: strict same-line parser; Holm within family)

| model_id | content_type | n_pairs | acc_first | acc_second | b_first_only | c_second_only | diff | diff_ci_lo | diff_ci_hi | discordant_or | or_ci_lo | or_ci_hi | p_mcnemar_exact | p_holm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| InternVL3-8B | code | 500 | 0.632 | 0.506 | 89 | 26 | 0.126 | 0.085 | 0.166 | 3.423 | 2.190 | 5.523 | 2.95e-09 | 3.84e-08 |
| InternVL3-8B | math | 500 | 0.920 | 0.864 | 43 | 15 | 0.056 | 0.026 | 0.087 | 2.867 | 1.561 | 5.555 | 3.07e-04 | 0.003 |
| InternVL3-8B | table | 500 | 0.648 | 0.588 | 87 | 57 | 0.060 | 0.013 | 0.107 | 1.526 | 1.081 | 2.171 | 0.015 | 0.138 |
| Qwen2.5-VL-32B-Instruct | code | 500 | 0.768 | 0.682 | 66 | 23 | 0.086 | 0.050 | 0.122 | 2.870 | 1.762 | 4.834 | 5.69e-06 | 6.83e-05 |
| Qwen2.5-VL-32B-Instruct | math | 500 | 0.114 | 0.266 | 26 | 102 | -0.152 | -0.195 | -0.109 | 0.255 | 0.159 | 0.395 | 7.78e-12 | 1.09e-10 |
| Qwen2.5-VL-32B-Instruct | table | 500 | 0.812 | 0.794 | 34 | 25 | 0.018 | -0.012 | 0.049 | 1.360 | 0.788 | 2.378 | 0.298 | 1.000 |
| Qwen2.5-VL-3B-Instruct | code | 500 | 0.386 | 0.338 | 73 | 49 | 0.048 | 0.005 | 0.091 | 1.490 | 1.023 | 2.185 | 0.037 | 0.295 |
| Qwen2.5-VL-3B-Instruct | math | 500 | 0.836 | 0.818 | 38 | 29 | 0.018 | -0.014 | 0.051 | 1.310 | 0.787 | 2.203 | 0.328 | 1.000 |
| Qwen2.5-VL-3B-Instruct | table | 500 | 0.428 | 0.454 | 82 | 95 | -0.026 | -0.078 | 0.026 | 0.863 | 0.634 | 1.172 | 0.367 | 1.000 |
| Qwen2.5-VL-7B-Instruct | code | 500 | 0.524 | 0.484 | 59 | 39 | 0.040 | 0.001 | 0.079 | 1.513 | 0.993 | 2.329 | 0.054 | 0.381 |
| Qwen2.5-VL-7B-Instruct | math | 500 | 0.868 | 0.868 | 20 | 20 | 0.000 | -0.026 | 0.026 | 1.000 | 0.511 | 1.958 | 1.000 | 1.000 |
| Qwen2.5-VL-7B-Instruct | table | 500 | 0.626 | 0.664 | 47 | 66 | -0.038 | -0.080 | 0.004 | 0.712 | 0.479 | 1.051 | 0.090 | 0.540 |
| gemma-3-12b-it | code | 500 | 0.688 | 0.494 | 117 | 20 | 0.194 | 0.151 | 0.236 | 5.850 | 3.621 | 9.928 | 7.16e-18 | 1.07e-16 |
| gemma-3-12b-it | math | 500 | 0.948 | 0.934 | 17 | 10 | 0.014 | -0.007 | 0.036 | 1.700 | 0.735 | 4.154 | 0.248 | 1.000 |
| gemma-3-12b-it | table | 500 | 0.734 | 0.648 | 88 | 45 | 0.086 | 0.041 | 0.130 | 1.956 | 1.350 | 2.867 | 2.42e-04 | 0.003 |

## T12 RQ1 McNemar A vs C (primary; Holm within family)

| model_id | content_type | n_pairs | acc_first | acc_second | b_first_only | c_second_only | diff | diff_ci_lo | diff_ci_hi | discordant_or | or_ci_lo | or_ci_hi | p_mcnemar_exact | p_holm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| InternVL3-8B | code | 500 | 0.632 | 0.522 | 85 | 30 | 0.110 | 0.069 | 0.151 | 2.833 | 1.849 | 4.451 | 2.86e-07 | 4.00e-06 |
| InternVL3-8B | math | 500 | 0.920 | 0.894 | 26 | 13 | 0.026 | 0.001 | 0.052 | 2.000 | 0.991 | 4.239 | 0.053 | 0.426 |
| InternVL3-8B | table | 500 | 0.648 | 0.628 | 78 | 68 | 0.020 | -0.027 | 0.067 | 1.147 | 0.818 | 1.612 | 0.456 | 1.000 |
| Qwen2.5-VL-32B-Instruct | code | 500 | 0.812 | 0.740 | 52 | 16 | 0.072 | 0.040 | 0.104 | 3.250 | 1.827 | 6.098 | 1.41e-05 | 1.69e-04 |
| Qwen2.5-VL-32B-Instruct | math | 500 | 0.918 | 0.948 | 13 | 28 | -0.030 | -0.057 | -0.005 | 0.464 | 0.221 | 0.926 | 0.028 | 0.303 |
| Qwen2.5-VL-32B-Instruct | table | 500 | 0.812 | 0.806 | 29 | 26 | 0.006 | -0.024 | 0.036 | 1.115 | 0.634 | 1.971 | 0.788 | 1.000 |
| Qwen2.5-VL-3B-Instruct | code | 500 | 0.386 | 0.358 | 67 | 53 | 0.028 | -0.015 | 0.071 | 1.264 | 0.869 | 1.848 | 0.235 | 1.000 |
| Qwen2.5-VL-3B-Instruct | math | 500 | 0.840 | 0.752 | 72 | 28 | 0.088 | 0.049 | 0.127 | 2.571 | 1.641 | 4.134 | 1.26e-05 | 1.64e-04 |
| Qwen2.5-VL-3B-Instruct | table | 500 | 0.428 | 0.392 | 101 | 83 | 0.036 | -0.017 | 0.089 | 1.217 | 0.901 | 1.647 | 0.210 | 1.000 |
| Qwen2.5-VL-7B-Instruct | code | 500 | 0.524 | 0.480 | 58 | 36 | 0.044 | 0.006 | 0.082 | 1.611 | 1.045 | 2.514 | 0.030 | 0.303 |
| Qwen2.5-VL-7B-Instruct | math | 500 | 0.868 | 0.866 | 22 | 21 | 0.002 | -0.024 | 0.029 | 1.048 | 0.550 | 2.003 | 1.000 | 1.000 |
| Qwen2.5-VL-7B-Instruct | table | 500 | 0.626 | 0.668 | 48 | 69 | -0.042 | -0.084 | 4.38e-04 | 0.696 | 0.471 | 1.020 | 0.064 | 0.448 |
| gemma-3-12b-it | code | 500 | 0.688 | 0.542 | 94 | 21 | 0.146 | 0.105 | 0.186 | 4.476 | 2.767 | 7.566 | 3.24e-12 | 4.86e-11 |
| gemma-3-12b-it | math | 500 | 0.948 | 0.922 | 23 | 10 | 0.026 | 0.003 | 0.050 | 2.300 | 1.053 | 5.414 | 0.035 | 0.316 |
| gemma-3-12b-it | table | 500 | 0.734 | 0.726 | 64 | 60 | 0.008 | -0.036 | 0.052 | 1.067 | 0.738 | 1.543 | 0.788 | 1.000 |

## T12 RQ1 McNemar A vs C (sensitivity: unparseable pairs excluded; Holm within family)

| model_id | content_type | n_pairs | acc_first | acc_second | b_first_only | c_second_only | diff | diff_ci_lo | diff_ci_hi | discordant_or | or_ci_lo | or_ci_hi | p_mcnemar_exact | p_holm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| InternVL3-8B | code | 495 | 0.638 | 0.527 | 85 | 30 | 0.111 | 0.069 | 0.152 | 2.833 | 1.849 | 4.451 | 2.86e-07 | 4.00e-06 |
| InternVL3-8B | math | 497 | 0.922 | 0.899 | 24 | 13 | 0.022 | -0.002 | 0.048 | 1.846 | 0.903 | 3.948 | 0.099 | 0.729 |
| InternVL3-8B | table | 497 | 0.648 | 0.632 | 76 | 68 | 0.016 | -0.031 | 0.063 | 1.118 | 0.795 | 1.574 | 0.560 | 1.000 |
| Qwen2.5-VL-32B-Instruct | code | 499 | 0.814 | 0.741 | 52 | 16 | 0.072 | 0.040 | 0.105 | 3.250 | 1.827 | 6.098 | 1.41e-05 | 1.83e-04 |
| Qwen2.5-VL-32B-Instruct | math | 493 | 0.927 | 0.953 | 11 | 24 | -0.026 | -0.052 | -0.002 | 0.458 | 0.203 | 0.972 | 0.041 | 0.410 |
| Qwen2.5-VL-32B-Instruct | table | 500 | 0.812 | 0.806 | 29 | 26 | 0.006 | -0.024 | 0.036 | 1.115 | 0.634 | 1.971 | 0.788 | 1.000 |
| Qwen2.5-VL-3B-Instruct | code | 468 | 0.402 | 0.378 | 62 | 51 | 0.024 | -0.021 | 0.068 | 1.216 | 0.826 | 1.797 | 0.347 | 1.000 |
| Qwen2.5-VL-3B-Instruct | math | 466 | 0.837 | 0.805 | 42 | 27 | 0.032 | -0.003 | 0.068 | 1.556 | 0.937 | 2.624 | 0.091 | 0.729 |
| Qwen2.5-VL-3B-Instruct | table | 346 | 0.514 | 0.468 | 65 | 49 | 0.046 | -0.014 | 0.106 | 1.327 | 0.902 | 1.963 | 0.160 | 0.959 |
| Qwen2.5-VL-7B-Instruct | code | 472 | 0.547 | 0.502 | 54 | 33 | 0.044 | 0.006 | 0.083 | 1.636 | 1.042 | 2.605 | 0.031 | 0.377 |
| Qwen2.5-VL-7B-Instruct | math | 494 | 0.877 | 0.874 | 21 | 20 | 0.002 | -0.024 | 0.028 | 1.050 | 0.542 | 2.042 | 1.000 | 1.000 |
| Qwen2.5-VL-7B-Instruct | table | 495 | 0.628 | 0.673 | 46 | 68 | -0.044 | -0.087 | -0.002 | 0.676 | 0.455 | 0.998 | 0.049 | 0.439 |
| gemma-3-12b-it | code | 498 | 0.689 | 0.544 | 93 | 21 | 0.145 | 0.104 | 0.184 | 4.429 | 2.736 | 7.489 | 5.31e-12 | 7.97e-11 |
| gemma-3-12b-it | math | 500 | 0.948 | 0.922 | 23 | 10 | 0.026 | 0.003 | 0.050 | 2.300 | 1.053 | 5.414 | 0.035 | 0.386 |
| gemma-3-12b-it | table | 492 | 0.740 | 0.736 | 61 | 59 | 0.004 | -0.040 | 0.048 | 1.034 | 0.711 | 1.505 | 0.927 | 1.000 |

## T12 RQ1 McNemar A vs C (sensitivity: strict same-line parser; Holm within family)

| model_id | content_type | n_pairs | acc_first | acc_second | b_first_only | c_second_only | diff | diff_ci_lo | diff_ci_hi | discordant_or | or_ci_lo | or_ci_hi | p_mcnemar_exact | p_holm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| InternVL3-8B | code | 500 | 0.632 | 0.522 | 85 | 30 | 0.110 | 0.069 | 0.151 | 2.833 | 1.849 | 4.451 | 2.86e-07 | 3.43e-06 |
| InternVL3-8B | math | 500 | 0.920 | 0.894 | 26 | 13 | 0.026 | 0.001 | 0.052 | 2.000 | 0.991 | 4.239 | 0.053 | 0.426 |
| InternVL3-8B | table | 500 | 0.648 | 0.628 | 78 | 68 | 0.020 | -0.027 | 0.067 | 1.147 | 0.818 | 1.612 | 0.456 | 1.000 |
| Qwen2.5-VL-32B-Instruct | code | 500 | 0.768 | 0.410 | 196 | 17 | 0.358 | 0.309 | 0.404 | 11.529 | 7.018 | 20.195 | 9.27e-40 | 1.30e-38 |
| Qwen2.5-VL-32B-Instruct | math | 500 | 0.114 | 0.650 | 9 | 277 | -0.536 | -0.581 | -0.487 | 0.032 | 0.015 | 0.063 | 5.16e-70 | 7.75e-69 |
| Qwen2.5-VL-32B-Instruct | table | 500 | 0.812 | 0.794 | 34 | 25 | 0.018 | -0.012 | 0.049 | 1.360 | 0.788 | 2.378 | 0.298 | 1.000 |
| Qwen2.5-VL-3B-Instruct | code | 500 | 0.386 | 0.358 | 67 | 53 | 0.028 | -0.015 | 0.071 | 1.264 | 0.869 | 1.848 | 0.235 | 1.000 |
| Qwen2.5-VL-3B-Instruct | math | 500 | 0.836 | 0.752 | 70 | 28 | 0.084 | 0.046 | 0.123 | 2.500 | 1.592 | 4.026 | 2.64e-05 | 2.90e-04 |
| Qwen2.5-VL-3B-Instruct | table | 500 | 0.428 | 0.392 | 101 | 83 | 0.036 | -0.017 | 0.089 | 1.217 | 0.901 | 1.647 | 0.210 | 1.000 |
| Qwen2.5-VL-7B-Instruct | code | 500 | 0.524 | 0.480 | 58 | 36 | 0.044 | 0.006 | 0.082 | 1.611 | 1.045 | 2.514 | 0.030 | 0.298 |
| Qwen2.5-VL-7B-Instruct | math | 500 | 0.868 | 0.866 | 22 | 21 | 0.002 | -0.024 | 0.029 | 1.048 | 0.550 | 2.003 | 1.000 | 1.000 |
| Qwen2.5-VL-7B-Instruct | table | 500 | 0.626 | 0.668 | 48 | 69 | -0.042 | -0.084 | 4.38e-04 | 0.696 | 0.471 | 1.020 | 0.064 | 0.448 |
| gemma-3-12b-it | code | 500 | 0.688 | 0.542 | 94 | 21 | 0.146 | 0.105 | 0.186 | 4.476 | 2.767 | 7.566 | 3.24e-12 | 4.21e-11 |
| gemma-3-12b-it | math | 500 | 0.948 | 0.922 | 23 | 10 | 0.026 | 0.003 | 0.050 | 2.300 | 1.053 | 5.414 | 0.035 | 0.316 |
| gemma-3-12b-it | table | 500 | 0.734 | 0.726 | 64 | 60 | 0.008 | -0.036 | 0.052 | 1.067 | 0.738 | 1.543 | 0.788 | 1.000 |

## T12 RQ1 McNemar B vs C (primary; Holm within family)

| model_id | content_type | n_pairs | acc_first | acc_second | b_first_only | c_second_only | diff | diff_ci_lo | diff_ci_hi | discordant_or | or_ci_lo | or_ci_hi | p_mcnemar_exact | p_holm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| InternVL3-8B | code | 500 | 0.506 | 0.522 | 43 | 51 | -0.016 | -0.054 | 0.022 | 0.843 | 0.549 | 1.290 | 0.470 | 1.000 |
| InternVL3-8B | math | 500 | 0.864 | 0.894 | 10 | 25 | -0.030 | -0.054 | -0.007 | 0.400 | 0.171 | 0.862 | 0.017 | 0.167 |
| InternVL3-8B | table | 500 | 0.588 | 0.628 | 55 | 75 | -0.040 | -0.084 | 0.005 | 0.733 | 0.508 | 1.052 | 0.095 | 0.857 |
| Qwen2.5-VL-32B-Instruct | code | 500 | 0.730 | 0.740 | 16 | 21 | -0.010 | -0.034 | 0.014 | 0.762 | 0.372 | 1.532 | 0.511 | 1.000 |
| Qwen2.5-VL-32B-Instruct | math | 500 | 0.902 | 0.948 | 7 | 30 | -0.046 | -0.072 | -0.023 | 0.233 | 0.087 | 0.542 | 1.91e-04 | 0.003 |
| Qwen2.5-VL-32B-Instruct | table | 500 | 0.794 | 0.806 | 21 | 27 | -0.012 | -0.040 | 0.016 | 0.778 | 0.418 | 1.428 | 0.471 | 1.000 |
| Qwen2.5-VL-3B-Instruct | code | 500 | 0.342 | 0.358 | 50 | 58 | -0.016 | -0.057 | 0.025 | 0.862 | 0.579 | 1.281 | 0.501 | 1.000 |
| Qwen2.5-VL-3B-Instruct | math | 500 | 0.818 | 0.752 | 67 | 34 | 0.066 | 0.027 | 0.105 | 1.971 | 1.286 | 3.071 | 0.001 | 0.017 |
| Qwen2.5-VL-3B-Instruct | table | 500 | 0.454 | 0.392 | 91 | 60 | 0.062 | 0.014 | 0.110 | 1.517 | 1.083 | 2.138 | 0.014 | 0.158 |
| Qwen2.5-VL-7B-Instruct | code | 500 | 0.490 | 0.480 | 42 | 37 | 0.010 | -0.025 | 0.045 | 1.135 | 0.712 | 1.816 | 0.653 | 1.000 |
| Qwen2.5-VL-7B-Instruct | math | 500 | 0.868 | 0.866 | 17 | 16 | 0.002 | -0.021 | 0.025 | 1.062 | 0.505 | 2.247 | 1.000 | 1.000 |
| Qwen2.5-VL-7B-Instruct | table | 500 | 0.664 | 0.668 | 47 | 49 | -0.004 | -0.043 | 0.035 | 0.959 | 0.629 | 1.461 | 0.919 | 1.000 |
| gemma-3-12b-it | code | 500 | 0.494 | 0.542 | 27 | 51 | -0.048 | -0.082 | -0.013 | 0.529 | 0.319 | 0.860 | 0.009 | 0.105 |
| gemma-3-12b-it | math | 500 | 0.934 | 0.922 | 13 | 7 | 0.012 | -0.007 | 0.031 | 1.857 | 0.689 | 5.497 | 0.263 | 1.000 |
| gemma-3-12b-it | table | 500 | 0.648 | 0.726 | 22 | 61 | -0.078 | -0.113 | -0.043 | 0.361 | 0.211 | 0.596 | 2.18e-05 | 3.27e-04 |

## T12 RQ1 McNemar B vs C (sensitivity: unparseable pairs excluded; Holm within family)

| model_id | content_type | n_pairs | acc_first | acc_second | b_first_only | c_second_only | diff | diff_ci_lo | diff_ci_hi | discordant_or | or_ci_lo | or_ci_hi | p_mcnemar_exact | p_holm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| InternVL3-8B | code | 495 | 0.511 | 0.527 | 43 | 51 | -0.016 | -0.055 | 0.022 | 0.843 | 0.549 | 1.290 | 0.470 | 1.000 |
| InternVL3-8B | math | 494 | 0.870 | 0.899 | 8 | 22 | -0.028 | -0.052 | -0.006 | 0.364 | 0.140 | 0.848 | 0.016 | 0.201 |
| InternVL3-8B | table | 496 | 0.593 | 0.633 | 55 | 75 | -0.040 | -0.085 | 0.005 | 0.733 | 0.508 | 1.052 | 0.095 | 1.000 |
| Qwen2.5-VL-32B-Instruct | code | 499 | 0.731 | 0.741 | 16 | 21 | -0.010 | -0.034 | 0.014 | 0.762 | 0.372 | 1.532 | 0.511 | 1.000 |
| Qwen2.5-VL-32B-Instruct | math | 489 | 0.922 | 0.953 | 7 | 22 | -0.031 | -0.054 | -0.009 | 0.318 | 0.115 | 0.771 | 0.008 | 0.114 |
| Qwen2.5-VL-32B-Instruct | table | 500 | 0.794 | 0.806 | 21 | 27 | -0.012 | -0.040 | 0.016 | 0.778 | 0.418 | 1.428 | 0.471 | 1.000 |
| Qwen2.5-VL-3B-Instruct | code | 460 | 0.363 | 0.385 | 46 | 56 | -0.022 | -0.065 | 0.021 | 0.821 | 0.544 | 1.235 | 0.373 | 1.000 |
| Qwen2.5-VL-3B-Instruct | math | 459 | 0.834 | 0.806 | 41 | 28 | 0.028 | -0.007 | 0.064 | 1.464 | 0.884 | 2.459 | 0.148 | 1.000 |
| Qwen2.5-VL-3B-Instruct | table | 405 | 0.462 | 0.472 | 51 | 55 | -0.010 | -0.060 | 0.040 | 0.927 | 0.621 | 1.383 | 0.771 | 1.000 |
| Qwen2.5-VL-7B-Instruct | code | 474 | 0.511 | 0.502 | 39 | 35 | 0.008 | -0.027 | 0.044 | 1.114 | 0.688 | 1.812 | 0.728 | 1.000 |
| Qwen2.5-VL-7B-Instruct | math | 493 | 0.878 | 0.874 | 16 | 14 | 0.004 | -0.019 | 0.027 | 1.143 | 0.523 | 2.528 | 0.856 | 1.000 |
| Qwen2.5-VL-7B-Instruct | table | 495 | 0.667 | 0.673 | 45 | 48 | -0.006 | -0.044 | 0.032 | 0.938 | 0.610 | 1.438 | 0.836 | 1.000 |
| gemma-3-12b-it | code | 496 | 0.498 | 0.542 | 27 | 49 | -0.044 | -0.079 | -0.010 | 0.551 | 0.331 | 0.899 | 0.015 | 0.201 |
| gemma-3-12b-it | math | 500 | 0.934 | 0.922 | 13 | 7 | 0.012 | -0.007 | 0.031 | 1.857 | 0.689 | 5.497 | 0.263 | 1.000 |
| gemma-3-12b-it | table | 492 | 0.659 | 0.736 | 22 | 60 | -0.077 | -0.113 | -0.042 | 0.367 | 0.214 | 0.607 | 3.23e-05 | 4.85e-04 |

## T12 RQ1 McNemar B vs C (sensitivity: strict same-line parser; Holm within family)

| model_id | content_type | n_pairs | acc_first | acc_second | b_first_only | c_second_only | diff | diff_ci_lo | diff_ci_hi | discordant_or | or_ci_lo | or_ci_hi | p_mcnemar_exact | p_holm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| InternVL3-8B | code | 500 | 0.506 | 0.522 | 43 | 51 | -0.016 | -0.054 | 0.022 | 0.843 | 0.549 | 1.290 | 0.470 | 1.000 |
| InternVL3-8B | math | 500 | 0.864 | 0.894 | 10 | 25 | -0.030 | -0.054 | -0.007 | 0.400 | 0.171 | 0.862 | 0.017 | 0.150 |
| InternVL3-8B | table | 500 | 0.588 | 0.628 | 55 | 75 | -0.040 | -0.084 | 0.005 | 0.733 | 0.508 | 1.052 | 0.095 | 0.762 |
| Qwen2.5-VL-32B-Instruct | code | 500 | 0.682 | 0.410 | 152 | 16 | 0.272 | 0.226 | 0.316 | 9.500 | 5.664 | 17.044 | 5.49e-29 | 7.69e-28 |
| Qwen2.5-VL-32B-Instruct | math | 500 | 0.266 | 0.650 | 11 | 203 | -0.384 | -0.429 | -0.336 | 0.054 | 0.027 | 0.099 | 6.68e-47 | 1.00e-45 |
| Qwen2.5-VL-32B-Instruct | table | 500 | 0.794 | 0.794 | 25 | 25 | 0.000 | -0.028 | 0.028 | 1.000 | 0.551 | 1.815 | 1.000 | 1.000 |
| Qwen2.5-VL-3B-Instruct | code | 500 | 0.338 | 0.358 | 50 | 60 | -0.020 | -0.061 | 0.021 | 0.833 | 0.561 | 1.233 | 0.391 | 1.000 |
| Qwen2.5-VL-3B-Instruct | math | 500 | 0.818 | 0.752 | 67 | 34 | 0.066 | 0.027 | 0.105 | 1.971 | 1.286 | 3.071 | 0.001 | 0.016 |
| Qwen2.5-VL-3B-Instruct | table | 500 | 0.454 | 0.392 | 91 | 60 | 0.062 | 0.014 | 0.110 | 1.517 | 1.083 | 2.138 | 0.014 | 0.144 |
| Qwen2.5-VL-7B-Instruct | code | 500 | 0.484 | 0.480 | 40 | 38 | 0.004 | -0.031 | 0.039 | 1.053 | 0.658 | 1.686 | 0.910 | 1.000 |
| Qwen2.5-VL-7B-Instruct | math | 500 | 0.868 | 0.866 | 17 | 16 | 0.002 | -0.021 | 0.025 | 1.062 | 0.505 | 2.247 | 1.000 | 1.000 |
| Qwen2.5-VL-7B-Instruct | table | 500 | 0.664 | 0.668 | 47 | 49 | -0.004 | -0.043 | 0.035 | 0.959 | 0.629 | 1.461 | 0.919 | 1.000 |
| gemma-3-12b-it | code | 500 | 0.494 | 0.542 | 27 | 51 | -0.048 | -0.082 | -0.013 | 0.529 | 0.319 | 0.860 | 0.009 | 0.096 |
| gemma-3-12b-it | math | 500 | 0.934 | 0.922 | 13 | 7 | 0.012 | -0.007 | 0.031 | 1.857 | 0.689 | 5.497 | 0.263 | 1.000 |
| gemma-3-12b-it | table | 500 | 0.648 | 0.726 | 22 | 61 | -0.078 | -0.113 | -0.043 | 0.361 | 0.211 | 0.596 | 2.18e-05 | 2.83e-04 |

## T12 Cochran's Q across A/B/C (Holm)

| model_id | content_type | n_items | acc_A | acc_B | acc_C | cochran_q | df | p_value | p_holm |
|---|---|---|---|---|---|---|---|---|---|
| InternVL3-8B | code | 500 | 0.632 | 0.506 | 0.522 | 43.568 | 2 | 3.46e-10 | 4.85e-09 |
| InternVL3-8B | math | 500 | 0.920 | 0.864 | 0.894 | 17.849 | 2 | 1.33e-04 | 0.001 |
| InternVL3-8B | table | 500 | 0.648 | 0.588 | 0.628 | 6.667 | 2 | 0.036 | 0.285 |
| Qwen2.5-VL-32B-Instruct | code | 500 | 0.812 | 0.730 | 0.740 | 36.610 | 2 | 1.12e-08 | 1.46e-07 |
| Qwen2.5-VL-32B-Instruct | math | 500 | 0.918 | 0.902 | 0.948 | 12.394 | 2 | 0.002 | 0.018 |
| Qwen2.5-VL-32B-Instruct | table | 500 | 0.812 | 0.794 | 0.806 | 1.556 | 2 | 0.459 | 0.919 |
| Qwen2.5-VL-3B-Instruct | code | 500 | 0.386 | 0.342 | 0.358 | 4.251 | 2 | 0.119 | 0.358 |
| Qwen2.5-VL-3B-Instruct | math | 500 | 0.840 | 0.818 | 0.752 | 23.654 | 2 | 7.30e-06 | 8.76e-05 |
| Qwen2.5-VL-3B-Instruct | table | 500 | 0.428 | 0.454 | 0.392 | 5.680 | 2 | 0.058 | 0.312 |
| Qwen2.5-VL-7B-Instruct | code | 500 | 0.524 | 0.490 | 0.480 | 5.911 | 2 | 0.052 | 0.312 |
| Qwen2.5-VL-7B-Instruct | math | 500 | 0.868 | 0.868 | 0.866 | 0.034 | 2 | 0.983 | 0.983 |
| Qwen2.5-VL-7B-Instruct | table | 500 | 0.626 | 0.664 | 0.668 | 4.945 | 2 | 0.084 | 0.338 |
| gemma-3-12b-it | code | 500 | 0.688 | 0.494 | 0.542 | 92.812 | 2 | 7.02e-21 | 1.05e-19 |
| gemma-3-12b-it | math | 500 | 0.948 | 0.934 | 0.922 | 6.350 | 2 | 0.042 | 0.293 |
| gemma-3-12b-it | table | 500 | 0.734 | 0.648 | 0.726 | 19.918 | 2 | 4.73e-05 | 5.20e-04 |

## T13 RQ2 transcription (condition C)

| model_id | content_type | n | pct_with_transcription | pct_src_tags | pct_src_open_tag | pct_src_heading_fence | pct_src_none | exact_rate | exact_lenient_rate | pct_cer_le_002 | cer_mean | cer_sd | cer_p10 | cer_q1 | cer_median | cer_q3 | cer_p90 | cer_max |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| InternVL3-8B | code | 500 | 100.000 | 99.800 | 0.200 | 0.000 | 0.000 | 0.672 | 0.676 | 87.800 | 0.096 | 2.015 | 0.000 | 0.000 | 0.000 | 0.008 | 0.023 | 45.067 |
| InternVL3-8B | math | 500 | 100.000 | 100.000 | 0.000 | 0.000 | 0.000 | 0.936 | 0.936 | 98.600 | 0.003 | 0.026 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.335 |
| InternVL3-8B | table | 500 | 100.000 | 100.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.170 | 6.600 | 0.074 | 0.055 | 0.025 | 0.036 | 0.062 | 0.099 | 0.136 | 0.566 |
| Qwen2.5-VL-32B-Instruct | code | 500 | 99.600 | 0.000 | 0.000 | 99.600 | 0.400 | 0.778 | 0.786 | 95.000 | 0.007 | 0.064 | 0.000 | 0.000 | 0.000 | 0.000 | 0.012 | 1.000 |
| Qwen2.5-VL-32B-Instruct | math | 500 | 100.000 | 100.000 | 0.000 | 0.000 | 0.000 | 0.946 | 0.946 | 98.800 | 8.18e-04 | 0.006 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.095 |
| Qwen2.5-VL-32B-Instruct | table | 500 | 100.000 | 62.000 | 0.000 | 38.000 | 0.000 | 0.004 | 0.328 | 32.400 | 0.062 | 0.085 | 0.007 | 0.015 | 0.042 | 0.083 | 0.132 | 0.836 |
| Qwen2.5-VL-3B-Instruct | code | 500 | 100.000 | 100.000 | 0.000 | 0.000 | 0.000 | 0.670 | 0.678 | 88.800 | 0.007 | 0.014 | 0.000 | 0.000 | 0.000 | 0.009 | 0.022 | 0.122 |
| Qwen2.5-VL-3B-Instruct | math | 500 | 100.000 | 100.000 | 0.000 | 0.000 | 0.000 | 0.926 | 0.926 | 98.000 | 0.010 | 0.079 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.871 |
| Qwen2.5-VL-3B-Instruct | table | 500 | 100.000 | 97.200 | 2.800 | 0.000 | 0.000 | 0.000 | 0.112 | 6.400 | 0.128 | 0.224 | 0.027 | 0.047 | 0.076 | 0.118 | 0.222 | 3.192 |
| Qwen2.5-VL-7B-Instruct | code | 500 | 100.000 | 100.000 | 0.000 | 0.000 | 0.000 | 0.868 | 0.868 | 96.800 | 0.002 | 0.007 | 0.000 | 0.000 | 0.000 | 0.000 | 0.008 | 0.088 |
| Qwen2.5-VL-7B-Instruct | math | 500 | 100.000 | 100.000 | 0.000 | 0.000 | 0.000 | 0.816 | 0.816 | 83.400 | 0.033 | 0.078 | 0.000 | 0.000 | 0.000 | 0.000 | 0.178 | 0.323 |
| Qwen2.5-VL-7B-Instruct | table | 500 | 100.000 | 99.600 | 0.400 | 0.000 | 0.000 | 0.000 | 0.398 | 20.200 | 0.961 | 14.256 | 0.015 | 0.021 | 0.037 | 0.061 | 0.094 | 227.942 |
| gemma-3-12b-it | code | 500 | 20.000 | 13.200 | 0.000 | 6.800 | 80.000 | 0.100 | 0.100 | 16.400 | 0.802 | 0.396 | 0.004 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| gemma-3-12b-it | math | 500 | 77.600 | 77.600 | 0.000 | 0.000 | 22.400 | 0.698 | 0.698 | 77.200 | 0.224 | 0.417 | 0.000 | 0.000 | 0.000 | 0.006 | 1.000 | 1.000 |
| gemma-3-12b-it | table | 500 | 82.200 | 78.600 | 3.600 | 0.000 | 17.800 | 0.000 | 0.186 | 7.800 | 0.318 | 0.466 | 0.024 | 0.043 | 0.096 | 0.563 | 1.000 | 6.673 |

## T13 RQ2 A vs C split by transcription correctness

| model_id | content_type | subset_rule | transcription_correct | n_pairs | acc_first | acc_second | gap_A_minus_C | diff_ci_lo | diff_ci_hi | b_first_only | c_second_only | p_mcnemar_exact | p_holm_within_rule |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| InternVL3-8B | code | exact | True | 336 | 0.690 | 0.643 | 0.048 | -5.92e-04 | 0.096 | 42 | 26 | 0.068 | 1.000 |
| InternVL3-8B | math | exact | True | 468 | 0.923 | 0.908 | 0.015 | -0.008 | 0.039 | 18 | 11 | 0.265 | 1.000 |
| Qwen2.5-VL-32B-Instruct | code | exact | True | 389 | 0.859 | 0.838 | 0.021 | -0.010 | 0.051 | 21 | 13 | 0.229 | 1.000 |
| Qwen2.5-VL-32B-Instruct | math | exact | True | 473 | 0.915 | 0.953 | -0.038 | -0.065 | -0.013 | 9 | 27 | 0.004 | 0.083 |
| Qwen2.5-VL-32B-Instruct | table | exact | True | 2 | 1.000 | 1.000 | 0.000 | -0.658 | 0.658 | 0 | 0 | 1.000 | 1.000 |
| Qwen2.5-VL-3B-Instruct | code | exact | True | 335 | 0.421 | 0.418 | 0.003 | -0.050 | 0.056 | 41 | 40 | 1.000 | 1.000 |
| Qwen2.5-VL-3B-Instruct | math | exact | True | 463 | 0.842 | 0.771 | 0.071 | 0.032 | 0.111 | 60 | 27 | 5.24e-04 | 0.012 |
| Qwen2.5-VL-7B-Instruct | code | exact | True | 434 | 0.548 | 0.516 | 0.032 | -0.008 | 0.072 | 46 | 32 | 0.141 | 1.000 |
| Qwen2.5-VL-7B-Instruct | math | exact | True | 408 | 0.877 | 0.882 | -0.005 | -0.034 | 0.024 | 16 | 18 | 0.864 | 1.000 |
| gemma-3-12b-it | code | exact | True | 50 | 0.800 | 0.760 | 0.040 | -0.066 | 0.148 | 4 | 2 | 0.688 | 1.000 |
| gemma-3-12b-it | math | exact | True | 349 | 0.954 | 0.946 | 0.009 | -0.015 | 0.033 | 9 | 6 | 0.607 | 1.000 |
| InternVL3-8B | code | exact | False | 164 | 0.512 | 0.274 | 0.238 | 0.162 | 0.309 | 43 | 4 | 2.78e-09 | 6.95e-08 |
| InternVL3-8B | math | exact | False | 32 | 0.875 | 0.688 | 0.188 | -0.012 | 0.373 | 8 | 2 | 0.109 | 1.000 |
| InternVL3-8B | table | exact | False | 500 | 0.648 | 0.628 | 0.020 | -0.027 | 0.067 | 78 | 68 | 0.456 | 1.000 |
| Qwen2.5-VL-32B-Instruct | code | exact | False | 111 | 0.649 | 0.396 | 0.252 | 0.156 | 0.340 | 31 | 3 | 7.66e-07 | 1.84e-05 |
| Qwen2.5-VL-32B-Instruct | math | exact | False | 27 | 0.963 | 0.852 | 0.111 | -0.066 | 0.293 | 4 | 1 | 0.375 | 1.000 |
| Qwen2.5-VL-32B-Instruct | table | exact | False | 498 | 0.811 | 0.805 | 0.006 | -0.024 | 0.036 | 29 | 26 | 0.788 | 1.000 |
| Qwen2.5-VL-3B-Instruct | code | exact | False | 165 | 0.315 | 0.236 | 0.079 | 0.004 | 0.152 | 26 | 13 | 0.053 | 1.000 |
| Qwen2.5-VL-3B-Instruct | math | exact | False | 37 | 0.811 | 0.514 | 0.297 | 0.116 | 0.453 | 12 | 1 | 0.003 | 0.075 |
| Qwen2.5-VL-3B-Instruct | table | exact | False | 500 | 0.428 | 0.392 | 0.036 | -0.017 | 0.089 | 101 | 83 | 0.210 | 1.000 |
| Qwen2.5-VL-7B-Instruct | code | exact | False | 66 | 0.364 | 0.242 | 0.121 | 0.002 | 0.237 | 12 | 4 | 0.077 | 1.000 |
| Qwen2.5-VL-7B-Instruct | math | exact | False | 92 | 0.826 | 0.793 | 0.033 | -0.037 | 0.104 | 6 | 3 | 0.508 | 1.000 |
| Qwen2.5-VL-7B-Instruct | table | exact | False | 500 | 0.626 | 0.668 | -0.042 | -0.084 | 4.38e-04 | 48 | 69 | 0.064 | 1.000 |
| gemma-3-12b-it | code | exact | False | 450 | 0.676 | 0.518 | 0.158 | 0.114 | 0.200 | 90 | 19 | 3.10e-12 | 8.06e-11 |
| gemma-3-12b-it | math | exact | False | 151 | 0.934 | 0.868 | 0.066 | 0.010 | 0.127 | 14 | 4 | 0.031 | 0.618 |
| gemma-3-12b-it | table | exact | False | 500 | 0.734 | 0.726 | 0.008 | -0.036 | 0.052 | 64 | 60 | 0.788 | 1.000 |
| InternVL3-8B | code | cer_le_0.02 | True | 439 | 0.654 | 0.560 | 0.093 | 0.050 | 0.136 | 69 | 28 | 3.80e-05 | 0.001 |
| InternVL3-8B | math | cer_le_0.02 | True | 493 | 0.919 | 0.892 | 0.026 | 0.001 | 0.053 | 26 | 13 | 0.053 | 1.000 |
| InternVL3-8B | table | cer_le_0.02 | True | 33 | 0.727 | 0.727 | 0.000 | -0.175 | 0.175 | 4 | 4 | 1.000 | 1.000 |
| Qwen2.5-VL-32B-Instruct | code | cer_le_0.02 | True | 475 | 0.827 | 0.762 | 0.065 | 0.033 | 0.098 | 46 | 15 | 8.84e-05 | 0.002 |
| Qwen2.5-VL-32B-Instruct | math | cer_le_0.02 | True | 494 | 0.917 | 0.951 | -0.034 | -0.061 | -0.010 | 11 | 28 | 0.009 | 0.237 |
| Qwen2.5-VL-32B-Instruct | table | cer_le_0.02 | True | 162 | 0.840 | 0.852 | -0.012 | -0.064 | 0.039 | 7 | 9 | 0.804 | 1.000 |
| Qwen2.5-VL-3B-Instruct | code | cer_le_0.02 | True | 444 | 0.403 | 0.378 | 0.025 | -0.021 | 0.070 | 58 | 47 | 0.329 | 1.000 |
| Qwen2.5-VL-3B-Instruct | math | cer_le_0.02 | True | 490 | 0.837 | 0.759 | 0.078 | 0.039 | 0.116 | 66 | 28 | 1.11e-04 | 0.003 |
| Qwen2.5-VL-3B-Instruct | table | cer_le_0.02 | True | 32 | 0.406 | 0.531 | -0.125 | -0.305 | 0.071 | 3 | 7 | 0.344 | 1.000 |
| Qwen2.5-VL-7B-Instruct | code | cer_le_0.02 | True | 484 | 0.531 | 0.490 | 0.041 | 0.003 | 0.079 | 55 | 35 | 0.045 | 0.937 |
| Qwen2.5-VL-7B-Instruct | math | cer_le_0.02 | True | 417 | 0.875 | 0.882 | -0.007 | -0.036 | 0.022 | 16 | 19 | 0.736 | 1.000 |
| Qwen2.5-VL-7B-Instruct | table | cer_le_0.02 | True | 101 | 0.624 | 0.594 | 0.030 | -0.064 | 0.123 | 13 | 10 | 0.678 | 1.000 |
| gemma-3-12b-it | code | cer_le_0.02 | True | 82 | 0.695 | 0.598 | 0.098 | 0.014 | 0.179 | 10 | 2 | 0.039 | 0.849 |
| gemma-3-12b-it | math | cer_le_0.02 | True | 386 | 0.956 | 0.935 | 0.021 | -0.004 | 0.047 | 15 | 7 | 0.134 | 1.000 |
| gemma-3-12b-it | table | cer_le_0.02 | True | 39 | 0.872 | 0.872 | 0.000 | -0.156 | 0.156 | 4 | 4 | 1.000 | 1.000 |
| InternVL3-8B | code | cer_le_0.02 | False | 61 | 0.475 | 0.246 | 0.230 | 0.099 | 0.349 | 16 | 2 | 0.001 | 0.034 |
| InternVL3-8B | math | cer_le_0.02 | False | 7 | 1.000 | 1.000 | 0.000 | -0.354 | 0.354 | 0 | 0 | 1.000 | 1.000 |
| InternVL3-8B | table | cer_le_0.02 | False | 467 | 0.642 | 0.621 | 0.021 | -0.028 | 0.071 | 74 | 64 | 0.444 | 1.000 |
| Qwen2.5-VL-32B-Instruct | code | cer_le_0.02 | False | 25 | 0.520 | 0.320 | 0.200 | -0.009 | 0.381 | 6 | 1 | 0.125 | 1.000 |
| Qwen2.5-VL-32B-Instruct | math | cer_le_0.02 | False | 6 | 1.000 | 0.667 | 0.333 | -0.123 | 0.700 | 2 | 0 | 0.500 | 1.000 |
| Qwen2.5-VL-32B-Instruct | table | cer_le_0.02 | False | 338 | 0.799 | 0.784 | 0.015 | -0.022 | 0.052 | 22 | 17 | 0.522 | 1.000 |
| Qwen2.5-VL-3B-Instruct | code | cer_le_0.02 | False | 56 | 0.250 | 0.196 | 0.054 | -0.087 | 0.192 | 9 | 6 | 0.607 | 1.000 |
| Qwen2.5-VL-3B-Instruct | math | cer_le_0.02 | False | 10 | 1.000 | 0.400 | 0.600 | 0.201 | 0.832 | 6 | 0 | 0.031 | 0.719 |
| Qwen2.5-VL-3B-Instruct | table | cer_le_0.02 | False | 468 | 0.429 | 0.382 | 0.047 | -0.008 | 0.102 | 98 | 76 | 0.111 | 1.000 |
| Qwen2.5-VL-7B-Instruct | code | cer_le_0.02 | False | 16 | 0.312 | 0.188 | 0.125 | -0.143 | 0.375 | 3 | 1 | 0.625 | 1.000 |
| Qwen2.5-VL-7B-Instruct | math | cer_le_0.02 | False | 83 | 0.831 | 0.783 | 0.048 | -0.024 | 0.123 | 6 | 2 | 0.289 | 1.000 |
| Qwen2.5-VL-7B-Instruct | table | cer_le_0.02 | False | 399 | 0.627 | 0.687 | -0.060 | -0.107 | -0.013 | 35 | 59 | 0.017 | 0.413 |
| gemma-3-12b-it | code | cer_le_0.02 | False | 418 | 0.687 | 0.531 | 0.156 | 0.110 | 0.200 | 84 | 19 | 6.21e-11 | 1.86e-09 |
| gemma-3-12b-it | math | cer_le_0.02 | False | 114 | 0.921 | 0.877 | 0.044 | -0.017 | 0.110 | 8 | 3 | 0.227 | 1.000 |
| gemma-3-12b-it | table | cer_le_0.02 | False | 461 | 0.722 | 0.714 | 0.009 | -0.037 | 0.055 | 60 | 56 | 0.781 | 1.000 |
| InternVL3-8B | code | exact_lenient | True | 338 | 0.689 | 0.642 | 0.047 | -5.89e-04 | 0.095 | 42 | 26 | 0.068 | 1.000 |
| InternVL3-8B | math | exact_lenient | True | 468 | 0.923 | 0.908 | 0.015 | -0.008 | 0.039 | 18 | 11 | 0.265 | 1.000 |
| InternVL3-8B | table | exact_lenient | True | 85 | 0.718 | 0.788 | -0.071 | -0.170 | 0.029 | 6 | 12 | 0.238 | 1.000 |
| Qwen2.5-VL-32B-Instruct | code | exact_lenient | True | 393 | 0.860 | 0.837 | 0.023 | -0.007 | 0.054 | 22 | 13 | 0.175 | 1.000 |
| Qwen2.5-VL-32B-Instruct | math | exact_lenient | True | 473 | 0.915 | 0.953 | -0.038 | -0.065 | -0.013 | 9 | 27 | 0.004 | 0.098 |
| Qwen2.5-VL-32B-Instruct | table | exact_lenient | True | 164 | 0.841 | 0.854 | -0.012 | -0.066 | 0.041 | 8 | 10 | 0.815 | 1.000 |
| Qwen2.5-VL-3B-Instruct | code | exact_lenient | True | 339 | 0.416 | 0.413 | 0.003 | -0.049 | 0.055 | 41 | 40 | 1.000 | 1.000 |
| Qwen2.5-VL-3B-Instruct | math | exact_lenient | True | 463 | 0.842 | 0.771 | 0.071 | 0.032 | 0.111 | 60 | 27 | 5.24e-04 | 0.014 |
| Qwen2.5-VL-3B-Instruct | table | exact_lenient | True | 56 | 0.464 | 0.536 | -0.071 | -0.215 | 0.078 | 7 | 11 | 0.481 | 1.000 |
| Qwen2.5-VL-7B-Instruct | code | exact_lenient | True | 434 | 0.548 | 0.516 | 0.032 | -0.008 | 0.072 | 46 | 32 | 0.141 | 1.000 |
| Qwen2.5-VL-7B-Instruct | math | exact_lenient | True | 408 | 0.877 | 0.882 | -0.005 | -0.034 | 0.024 | 16 | 18 | 0.864 | 1.000 |
| Qwen2.5-VL-7B-Instruct | table | exact_lenient | True | 199 | 0.648 | 0.698 | -0.050 | -0.112 | 0.012 | 15 | 25 | 0.154 | 1.000 |
| gemma-3-12b-it | code | exact_lenient | True | 50 | 0.800 | 0.760 | 0.040 | -0.066 | 0.148 | 4 | 2 | 0.688 | 1.000 |
| gemma-3-12b-it | math | exact_lenient | True | 349 | 0.954 | 0.946 | 0.009 | -0.015 | 0.033 | 9 | 6 | 0.607 | 1.000 |
| gemma-3-12b-it | table | exact_lenient | True | 93 | 0.839 | 0.774 | 0.065 | -0.032 | 0.161 | 13 | 7 | 0.263 | 1.000 |
| InternVL3-8B | code | exact_lenient | False | 162 | 0.512 | 0.272 | 0.241 | 0.164 | 0.313 | 43 | 4 | 2.78e-09 | 8.07e-08 |
| InternVL3-8B | math | exact_lenient | False | 32 | 0.875 | 0.688 | 0.188 | -0.012 | 0.373 | 8 | 2 | 0.109 | 1.000 |
| InternVL3-8B | table | exact_lenient | False | 415 | 0.634 | 0.595 | 0.039 | -0.015 | 0.092 | 72 | 56 | 0.185 | 1.000 |
| Qwen2.5-VL-32B-Instruct | code | exact_lenient | False | 107 | 0.636 | 0.383 | 0.252 | 0.154 | 0.342 | 30 | 3 | 1.40e-06 | 3.92e-05 |
| Qwen2.5-VL-32B-Instruct | math | exact_lenient | False | 27 | 0.963 | 0.852 | 0.111 | -0.066 | 0.293 | 4 | 1 | 0.375 | 1.000 |
| Qwen2.5-VL-32B-Instruct | table | exact_lenient | False | 336 | 0.798 | 0.783 | 0.015 | -0.021 | 0.051 | 21 | 16 | 0.511 | 1.000 |
| Qwen2.5-VL-3B-Instruct | code | exact_lenient | False | 161 | 0.323 | 0.242 | 0.081 | 0.004 | 0.156 | 26 | 13 | 0.053 | 1.000 |
| Qwen2.5-VL-3B-Instruct | math | exact_lenient | False | 37 | 0.811 | 0.514 | 0.297 | 0.116 | 0.453 | 12 | 1 | 0.003 | 0.089 |
| Qwen2.5-VL-3B-Instruct | table | exact_lenient | False | 444 | 0.423 | 0.374 | 0.050 | -0.007 | 0.106 | 94 | 72 | 0.103 | 1.000 |
| Qwen2.5-VL-7B-Instruct | code | exact_lenient | False | 66 | 0.364 | 0.242 | 0.121 | 0.002 | 0.237 | 12 | 4 | 0.077 | 1.000 |
| Qwen2.5-VL-7B-Instruct | math | exact_lenient | False | 92 | 0.826 | 0.793 | 0.033 | -0.037 | 0.104 | 6 | 3 | 0.508 | 1.000 |
| Qwen2.5-VL-7B-Instruct | table | exact_lenient | False | 301 | 0.611 | 0.648 | -0.037 | -0.093 | 0.021 | 33 | 44 | 0.254 | 1.000 |
| gemma-3-12b-it | code | exact_lenient | False | 450 | 0.676 | 0.518 | 0.158 | 0.114 | 0.200 | 90 | 19 | 3.10e-12 | 9.30e-11 |
| gemma-3-12b-it | math | exact_lenient | False | 151 | 0.934 | 0.868 | 0.066 | 0.010 | 0.127 | 14 | 4 | 0.031 | 0.741 |
| gemma-3-12b-it | table | exact_lenient | False | 407 | 0.710 | 0.715 | -0.005 | -0.054 | 0.044 | 51 | 53 | 0.922 | 1.000 |
| InternVL3-8B | code | exact_tags_only | True | 336 | 0.690 | 0.643 | 0.048 | -5.92e-04 | 0.096 | 42 | 26 | 0.068 | 1.000 |
| InternVL3-8B | math | exact_tags_only | True | 468 | 0.923 | 0.908 | 0.015 | -0.008 | 0.039 | 18 | 11 | 0.265 | 1.000 |
| Qwen2.5-VL-32B-Instruct | math | exact_tags_only | True | 473 | 0.915 | 0.953 | -0.038 | -0.065 | -0.013 | 9 | 27 | 0.004 | 0.079 |
| Qwen2.5-VL-32B-Instruct | table | exact_tags_only | True | 1 | 1.000 | 1.000 | 0.000 | -0.793 | 0.793 | 0 | 0 | 1.000 | 1.000 |
| Qwen2.5-VL-3B-Instruct | code | exact_tags_only | True | 335 | 0.421 | 0.418 | 0.003 | -0.050 | 0.056 | 41 | 40 | 1.000 | 1.000 |
| Qwen2.5-VL-3B-Instruct | math | exact_tags_only | True | 463 | 0.842 | 0.771 | 0.071 | 0.032 | 0.111 | 60 | 27 | 5.24e-04 | 0.012 |
| Qwen2.5-VL-7B-Instruct | code | exact_tags_only | True | 434 | 0.548 | 0.516 | 0.032 | -0.008 | 0.072 | 46 | 32 | 0.141 | 1.000 |
| Qwen2.5-VL-7B-Instruct | math | exact_tags_only | True | 408 | 0.877 | 0.882 | -0.005 | -0.034 | 0.024 | 16 | 18 | 0.864 | 1.000 |
| gemma-3-12b-it | code | exact_tags_only | True | 27 | 0.815 | 0.815 | 0.000 | -0.141 | 0.141 | 1 | 1 | 1.000 | 1.000 |
| gemma-3-12b-it | math | exact_tags_only | True | 349 | 0.954 | 0.946 | 0.009 | -0.015 | 0.033 | 9 | 6 | 0.607 | 1.000 |
| InternVL3-8B | code | exact_tags_only | False | 163 | 0.515 | 0.276 | 0.239 | 0.163 | 0.311 | 43 | 4 | 2.78e-09 | 6.67e-08 |
| InternVL3-8B | math | exact_tags_only | False | 32 | 0.875 | 0.688 | 0.188 | -0.012 | 0.373 | 8 | 2 | 0.109 | 1.000 |
| InternVL3-8B | table | exact_tags_only | False | 500 | 0.648 | 0.628 | 0.020 | -0.027 | 0.067 | 78 | 68 | 0.456 | 1.000 |
| Qwen2.5-VL-32B-Instruct | math | exact_tags_only | False | 27 | 0.963 | 0.852 | 0.111 | -0.066 | 0.293 | 4 | 1 | 0.375 | 1.000 |
| Qwen2.5-VL-32B-Instruct | table | exact_tags_only | False | 309 | 0.809 | 0.809 | 0.000 | -0.037 | 0.037 | 16 | 16 | 1.000 | 1.000 |
| Qwen2.5-VL-3B-Instruct | code | exact_tags_only | False | 165 | 0.315 | 0.236 | 0.079 | 0.004 | 0.152 | 26 | 13 | 0.053 | 0.959 |
| Qwen2.5-VL-3B-Instruct | math | exact_tags_only | False | 37 | 0.811 | 0.514 | 0.297 | 0.116 | 0.453 | 12 | 1 | 0.003 | 0.072 |
| Qwen2.5-VL-3B-Instruct | table | exact_tags_only | False | 486 | 0.424 | 0.393 | 0.031 | -0.023 | 0.085 | 98 | 83 | 0.298 | 1.000 |
| Qwen2.5-VL-7B-Instruct | code | exact_tags_only | False | 66 | 0.364 | 0.242 | 0.121 | 0.002 | 0.237 | 12 | 4 | 0.077 | 1.000 |
| Qwen2.5-VL-7B-Instruct | math | exact_tags_only | False | 92 | 0.826 | 0.793 | 0.033 | -0.037 | 0.104 | 6 | 3 | 0.508 | 1.000 |
| Qwen2.5-VL-7B-Instruct | table | exact_tags_only | False | 498 | 0.624 | 0.671 | -0.046 | -0.088 | -0.004 | 46 | 69 | 0.040 | 0.755 |
| gemma-3-12b-it | code | exact_tags_only | False | 39 | 0.487 | 0.231 | 0.256 | 0.106 | 0.390 | 10 | 0 | 0.002 | 0.043 |
| gemma-3-12b-it | math | exact_tags_only | False | 39 | 0.974 | 0.821 | 0.154 | 0.010 | 0.304 | 7 | 1 | 0.070 | 1.000 |
| gemma-3-12b-it | table | exact_tags_only | False | 393 | 0.723 | 0.700 | 0.023 | -0.028 | 0.074 | 56 | 47 | 0.431 | 1.000 |

## T13 RQ2 logistic regression: correct(B) ~ CER(C) + model

| content_type | predictor | n | n_models | coef | se | odds_ratio | or_ci_lo | or_ci_hi | z | p_value | pseudo_r2 | converged |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| code | cer | 2500 | 5 | -0.1185 | 0.1826 | 0.8883 | 0.6210 | 1.2706 | -0.6487 | 0.5166 | 0.0465 | True |
| code | cer_gt_002 | 2500 | 5 | -0.8410 | 0.1496 | 0.4313 | 0.3217 | 0.5782 | -5.6218 | 1.89e-08 | 0.0557 | True |
| code | cer_capped1 | 2500 | 5 | -0.1309 | 0.2220 | 0.8773 | 0.5678 | 1.3556 | -0.5895 | 0.5555 | 0.0461 | True |
| math | cer | 2500 | 5 | -0.5848 | 0.3610 | 0.5572 | 0.2746 | 1.1305 | -1.6201 | 0.1052 | 0.0208 | True |
| math | cer_gt_002 | 2500 | 5 | -0.5524 | 0.2207 | 0.5755 | 0.3734 | 0.8871 | -2.5027 | 0.0123 | 0.0226 | True |
| math | cer_capped1 | 2500 | 5 | -0.5848 | 0.3610 | 0.5572 | 0.2746 | 1.1305 | -1.6201 | 0.1052 | 0.0208 | True |
| table | cer | 2500 | 5 | 0.0160 | 0.0268 | 1.0161 | 0.9641 | 1.0710 | 0.5975 | 0.5502 | 0.0410 | True |
| table | cer_gt_002 | 2500 | 5 | -0.2270 | 0.1332 | 0.7970 | 0.6138 | 1.0347 | -1.7038 | 0.0884 | 0.0415 | True |
| table | cer_capped1 | 2500 | 5 | -0.0107 | 0.2179 | 0.9893 | 0.6455 | 1.5163 | -0.0492 | 0.9608 | 0.0406 | True |

## T14 RQ3 output tokens A vs B (Wilcoxon signed-rank, Holm)

| model_id | content_type | n_pairs | median_A | median_B | median_diff_A_minus_B | mean_diff_A_minus_B | wilcoxon_W | p_value | p_holm |
|---|---|---|---|---|---|---|---|---|---|
| InternVL3-8B | code | 500 | 330.0 | 344.0 | -12.0 | -15.3 | 52874.0 | 0.0 | 0.1 |
| InternVL3-8B | math | 500 | 251.0 | 210.0 | 38.0 | 42.0 | 21799.0 | 2.92e-35 | 4.38e-34 |
| InternVL3-8B | table | 500 | 141.5 | 147.0 | 3.5 | -16.1 | 60472.5 | 1.0 | 1.0 |
| Qwen2.5-VL-32B-Instruct | code | 500 | 564.0 | 610.0 | -32.0 | -30.0 | 39057.5 | 3.07e-13 | 3.38e-12 |
| Qwen2.5-VL-32B-Instruct | math | 500 | 316.0 | 324.0 | -2.0 | -7.1 | 54170.5 | 0.0 | 0.2 |
| Qwen2.5-VL-32B-Instruct | table | 500 | 215.0 | 245.0 | -18.5 | -41.8 | 33703.0 | 5.57e-18 | 6.68e-17 |
| Qwen2.5-VL-3B-Instruct | code | 500 | 327.0 | 333.5 | -9.5 | -46.5 | 53023.0 | 0.0 | 0.1 |
| Qwen2.5-VL-3B-Instruct | math | 500 | 231.5 | 232.5 | 0.0 | 0.9 | 58323.0 | 0.8 | 1.0 |
| Qwen2.5-VL-3B-Instruct | table | 500 | 181.0 | 186.0 | 1.0 | 15.5 | 60587.0 | 0.6 | 1.0 |
| Qwen2.5-VL-7B-Instruct | code | 500 | 396.0 | 358.5 | 25.5 | 34.6 | 45051.0 | 4.06e-07 | 4.06e-06 |
| Qwen2.5-VL-7B-Instruct | math | 500 | 249.5 | 224.5 | 20.5 | 40.4 | 26378.5 | 4.84e-27 | 6.29e-26 |
| Qwen2.5-VL-7B-Instruct | table | 500 | 170.5 | 172.0 | -3.0 | -5.5 | 53443.0 | 0.1 | 0.4 |
| gemma-3-12b-it | code | 500 | 239.0 | 290.0 | -35.0 | -66.3 | 25989.5 | 3.93e-29 | 5.50e-28 |
| gemma-3-12b-it | math | 500 | 146.0 | 157.0 | -6.0 | -2.3 | 53170.5 | 0.0 | 0.1 |
| gemma-3-12b-it | table | 500 | 91.0 | 80.0 | 2.5 | 16.3 | 52740.0 | 0.0 | 0.1 |

## T14 error sample

- file: `results/coding/error_sample.csv`, 300 rows
| content_type | n |
|---|---|
| code | 100 |
| math | 100 |
| table | 100 |

- available A-correct/B-wrong flips per content type:

| content_type | n_flips |
|---|---|
| code | 385 |
| math | 149 |
| table | 338 |

## T10 scorer hand-check

- rows checked: 30; scorer agrees: 29; disagreements: 1

## GPU hours (wall time × GPUs, from logs/lanes.log)

| model | set | wall_h | gpus | gpu_h |
|---|---|---|---|---|
| Qwen2.5-VL-3B-Instruct | pilot | 0.020 | 1 | 0.020 |
| Qwen2.5-VL-7B-Instruct | pilot | 0.021 | 1 | 0.021 |
| Qwen2.5-VL-3B-Instruct | pilot_rep2 | 0.018 | 1 | 0.018 |
| Qwen2.5-VL-7B-Instruct | pilot_rep2 | 0.026 | 1 | 0.026 |
| gemma-3-12b-it | pilot | 0.044 | 1 | 0.044 |
| InternVL3-8B | pilot | 0.039 | 1 | 0.039 |
| InternVL3-8B | pilot_rep2 | 0.032 | 1 | 0.032 |
| gemma-3-12b-it | pilot_rep2 | 0.046 | 1 | 0.046 |
| Qwen2.5-VL-32B-Instruct | pilot | 0.056 | 2 | 0.112 |
| Qwen2.5-VL-32B-Instruct | pilot_rep2 | 0.055 | 2 | 0.109 |
| Qwen2.5-VL-3B-Instruct | main | 0.142 | 1 | 0.142 |
| Qwen2.5-VL-7B-Instruct | main | 0.231 | 1 | 0.231 |
| gemma-3-12b-it | main | 0.411 | 1 | 0.411 |
| InternVL3-8B | main | 0.397 | 1 | 0.397 |
| Qwen2.5-VL-32B-Instruct | main | 0.579 | 2 | 1.157 |
| Qwen2.5-VL-3B-Instruct | main_run2 | 0.177 | 1 | 0.177 |
| Qwen2.5-VL-7B-Instruct | main_run2 | 0.293 | 1 | 0.293 |
| Qwen2.5-VL-3B-Instruct | main_run3 | 0.174 | 1 | 0.174 |
| Qwen2.5-VL-7B-Instruct | main_run3 | 0.290 | 1 | 0.290 |
| InternVL3-8B | main_run2 | 0.565 | 1 | 0.565 |
| gemma-3-12b-it | main_run2 | 0.546 | 1 | 0.546 |
| InternVL3-8B | main_run3 | 0.548 | 1 | 0.548 |
| gemma-3-12b-it | main_run3 | 0.538 | 1 | 0.538 |
| Qwen2.5-VL-32B-Instruct | main_run2 | 0.906 | 2 | 1.812 |
| Qwen2.5-VL-32B-Instruct | main_run3 | 0.905 | 2 | 1.811 |
| gemma-3-27b-it | ext/pilot | 0.090 | 2 | 0.181 |
| gemma-3-27b-it | ext/run1 | 0.595 | 2 | 1.191 |
| gemma-3-27b-it | ext/run2 | 0.611 | 2 | 1.222 |
| gemma-3-27b-it | ext/run3 | 0.595 | 2 | 1.190 |
| Qwen3-VL-8B-Instruct | ext/pilot | 0.056 | 1 | 0.056 |
| InternVL3_5-8B | ext/pilot | 0.057 | 1 | 0.057 |
| Qwen3-VL-8B-Instruct | ext/run1 | 0.392 | 1 | 0.392 |
| InternVL3_5-8B | ext/run1 | 0.640 | 1 | 0.640 |
| Qwen3-VL-8B-Instruct | ext/run2 | 0.396 | 1 | 0.396 |
| Qwen3-VL-8B-Instruct | ext/run3 | 0.395 | 1 | 0.395 |
| InternVL3_5-8B | ext/run2 | 0.643 | 1 | 0.643 |
| InternVL3_5-8B | ext/run3 | 0.641 | 1 | 0.641 |
| Qwen2.5-VL-72B-Instruct-AWQ | ext/pilot | 0.080 | 2 | 0.159 |
| Qwen2.5-VL-72B-Instruct-AWQ | ext/run1 | 0.792 | 2 | 1.583 |
| Qwen2.5-VL-72B-Instruct-AWQ | ext/run2 | 0.769 | 2 | 1.539 |
| Qwen2.5-VL-72B-Instruct-AWQ | ext/run3 | 0.773 | 2 | 1.546 |

- total GPU hours: 21.39

## Package versions

| package | version |
|---|---|
| vllm | 0.33.0 |
| torch | 2.14.0 |
| transformers | 5.20.2 |
| datasets | 5.2.0 |
| pillow | 13.0.0 |
| pandas | 3.1.1 |
| numpy | 2.3.5 |
| scipy | 1.18.1 |
| statsmodels | 0.15.0 |
| matplotlib | 3.11.2 |
| rapidfuzz | 3.14.6 |

Full lock file: `env/requirements.lock.txt`.

# Phase 4 (added 2026-11-15): replication runs and extension models

Run 1 of the 5 primary models remains the primary analysis. Extension models are exploratory (own Holm families).

## T16/T18 accuracy across runs, primary models

| model_id | content_type | condition | acc_run1 | acc_run2 | acc_run3 | n_runs | mean | sd | range |
|---|---|---|---|---|---|---|---|---|---|
| InternVL3-8B | code | A_text | 0.632 | 0.620 | 0.642 | 3 | 0.631 | 0.011 | 0.022 |
| InternVL3-8B | code | B_image | 0.506 | 0.510 | 0.512 | 3 | 0.509 | 0.003 | 0.006 |
| InternVL3-8B | code | C_image_transcribe | 0.522 | 0.530 | 0.528 | 3 | 0.527 | 0.004 | 0.008 |
| InternVL3-8B | math | A_text | 0.920 | 0.918 | 0.916 | 3 | 0.918 | 0.002 | 0.004 |
| InternVL3-8B | math | B_image | 0.864 | 0.866 | 0.860 | 3 | 0.863 | 0.003 | 0.006 |
| InternVL3-8B | math | C_image_transcribe | 0.894 | 0.890 | 0.894 | 3 | 0.893 | 0.002 | 0.004 |
| InternVL3-8B | table | A_text | 0.648 | 0.674 | 0.676 | 3 | 0.666 | 0.016 | 0.028 |
| InternVL3-8B | table | B_image | 0.588 | 0.588 | 0.588 | 3 | 0.588 | 0.000 | 0.000 |
| InternVL3-8B | table | C_image_transcribe | 0.628 | 0.616 | 0.614 | 3 | 0.619 | 0.008 | 0.014 |
| Qwen2.5-VL-32B-Instruct | code | A_text | 0.812 | 0.814 | 0.820 | 3 | 0.815 | 0.004 | 0.008 |
| Qwen2.5-VL-32B-Instruct | code | B_image | 0.730 | 0.728 | 0.738 | 3 | 0.732 | 0.005 | 0.010 |
| Qwen2.5-VL-32B-Instruct | code | C_image_transcribe | 0.740 | 0.754 | 0.754 | 3 | 0.749 | 0.008 | 0.014 |
| Qwen2.5-VL-32B-Instruct | math | A_text | 0.918 | 0.928 | 0.924 | 3 | 0.923 | 0.005 | 0.010 |
| Qwen2.5-VL-32B-Instruct | math | B_image | 0.902 | 0.912 | 0.908 | 3 | 0.907 | 0.005 | 0.010 |
| Qwen2.5-VL-32B-Instruct | math | C_image_transcribe | 0.948 | 0.952 | 0.944 | 3 | 0.948 | 0.004 | 0.008 |
| Qwen2.5-VL-32B-Instruct | table | A_text | 0.812 | 0.816 | 0.818 | 3 | 0.815 | 0.003 | 0.006 |
| Qwen2.5-VL-32B-Instruct | table | B_image | 0.794 | 0.780 | 0.786 | 3 | 0.787 | 0.007 | 0.014 |
| Qwen2.5-VL-32B-Instruct | table | C_image_transcribe | 0.806 | 0.798 | 0.802 | 3 | 0.802 | 0.004 | 0.008 |
| Qwen2.5-VL-3B-Instruct | code | A_text | 0.386 | 0.386 | 0.374 | 3 | 0.382 | 0.007 | 0.012 |
| Qwen2.5-VL-3B-Instruct | code | B_image | 0.342 | 0.326 | 0.320 | 3 | 0.329 | 0.011 | 0.022 |
| Qwen2.5-VL-3B-Instruct | code | C_image_transcribe | 0.358 | 0.346 | 0.372 | 3 | 0.359 | 0.013 | 0.026 |
| Qwen2.5-VL-3B-Instruct | math | A_text | 0.840 | 0.836 | 0.840 | 3 | 0.839 | 0.002 | 0.004 |
| Qwen2.5-VL-3B-Instruct | math | B_image | 0.818 | 0.830 | 0.800 | 3 | 0.816 | 0.015 | 0.030 |
| Qwen2.5-VL-3B-Instruct | math | C_image_transcribe | 0.752 | 0.750 | 0.744 | 3 | 0.749 | 0.004 | 0.008 |
| Qwen2.5-VL-3B-Instruct | table | A_text | 0.428 | 0.460 | 0.432 | 3 | 0.440 | 0.017 | 0.032 |
| Qwen2.5-VL-3B-Instruct | table | B_image | 0.454 | 0.460 | 0.462 | 3 | 0.459 | 0.004 | 0.008 |
| Qwen2.5-VL-3B-Instruct | table | C_image_transcribe | 0.392 | 0.366 | 0.380 | 3 | 0.379 | 0.013 | 0.026 |
| Qwen2.5-VL-7B-Instruct | code | A_text | 0.524 | 0.534 | 0.518 | 3 | 0.525 | 0.008 | 0.016 |
| Qwen2.5-VL-7B-Instruct | code | B_image | 0.490 | 0.490 | 0.482 | 3 | 0.487 | 0.005 | 0.008 |
| Qwen2.5-VL-7B-Instruct | code | C_image_transcribe | 0.480 | 0.474 | 0.470 | 3 | 0.475 | 0.005 | 0.010 |
| Qwen2.5-VL-7B-Instruct | math | A_text | 0.868 | 0.878 | 0.870 | 3 | 0.872 | 0.005 | 0.010 |
| Qwen2.5-VL-7B-Instruct | math | B_image | 0.868 | 0.874 | 0.872 | 3 | 0.871 | 0.003 | 0.006 |
| Qwen2.5-VL-7B-Instruct | math | C_image_transcribe | 0.866 | 0.882 | 0.870 | 3 | 0.873 | 0.008 | 0.016 |
| Qwen2.5-VL-7B-Instruct | table | A_text | 0.626 | 0.618 | 0.616 | 3 | 0.620 | 0.005 | 0.010 |
| Qwen2.5-VL-7B-Instruct | table | B_image | 0.664 | 0.650 | 0.656 | 3 | 0.657 | 0.007 | 0.014 |
| Qwen2.5-VL-7B-Instruct | table | C_image_transcribe | 0.668 | 0.666 | 0.674 | 3 | 0.669 | 0.004 | 0.008 |
| gemma-3-12b-it | code | A_text | 0.688 | 0.694 | 0.688 | 3 | 0.690 | 0.003 | 0.006 |
| gemma-3-12b-it | code | B_image | 0.494 | 0.496 | 0.500 | 3 | 0.497 | 0.003 | 0.006 |
| gemma-3-12b-it | code | C_image_transcribe | 0.542 | 0.540 | 0.542 | 3 | 0.541 | 0.001 | 0.002 |
| gemma-3-12b-it | math | A_text | 0.948 | 0.952 | 0.950 | 3 | 0.950 | 0.002 | 0.004 |
| gemma-3-12b-it | math | B_image | 0.934 | 0.934 | 0.932 | 3 | 0.933 | 0.001 | 0.002 |
| gemma-3-12b-it | math | C_image_transcribe | 0.922 | 0.940 | 0.932 | 3 | 0.931 | 0.009 | 0.018 |
| gemma-3-12b-it | table | A_text | 0.734 | 0.728 | 0.726 | 3 | 0.729 | 0.004 | 0.008 |
| gemma-3-12b-it | table | B_image | 0.648 | 0.670 | 0.664 | 3 | 0.661 | 0.011 | 0.022 |
| gemma-3-12b-it | table | C_image_transcribe | 0.726 | 0.724 | 0.732 | 3 | 0.727 | 0.004 | 0.008 |

## Item-level stability across 3 runs, primary models

| model_id | content_type | condition | n_items | fleiss_kappa | pct_correct_all3 | pct_correct_none | pct_mixed | pct_agree_run1_run2 | pct_agree_run1_run3 | pct_agree_run2_run3 |
|---|---|---|---|---|---|---|---|---|---|---|
| InternVL3-8B | code | A_text | 500 | 0.791 | 55.800 | 29.600 | 14.600 | 89.600 | 90.200 | 91.000 |
| InternVL3-8B | code | B_image | 500 | 0.792 | 43.600 | 40.800 | 15.600 | 91.200 | 88.600 | 89.000 |
| InternVL3-8B | code | C_image_transcribe | 500 | 0.864 | 47.400 | 42.400 | 10.200 | 92.400 | 94.200 | 93.000 |
| InternVL3-8B | math | A_text | 500 | 0.885 | 90.400 | 7.000 | 2.600 | 98.200 | 98.000 | 98.600 |
| InternVL3-8B | math | B_image | 500 | 0.904 | 84.800 | 11.800 | 3.400 | 97.400 | 98.000 | 97.800 |
| InternVL3-8B | math | C_image_transcribe | 500 | 0.910 | 88.000 | 9.400 | 2.600 | 98.400 | 97.600 | 98.800 |
| InternVL3-8B | table | A_text | 500 | 0.877 | 62.400 | 29.400 | 8.200 | 94.600 | 94.000 | 95.000 |
| InternVL3-8B | table | B_image | 500 | 0.854 | 53.600 | 35.800 | 10.600 | 92.800 | 93.200 | 92.800 |
| InternVL3-8B | table | C_image_transcribe | 500 | 0.833 | 56.400 | 31.800 | 11.800 | 92.800 | 91.400 | 92.200 |
| Qwen2.5-VL-32B-Instruct | code | A_text | 500 | 0.911 | 79.600 | 16.400 | 4.000 | 97.800 | 97.200 | 97.000 |
| Qwen2.5-VL-32B-Instruct | code | B_image | 500 | 0.888 | 69.600 | 23.800 | 6.600 | 95.400 | 95.600 | 95.800 |
| Qwen2.5-VL-32B-Instruct | code | C_image_transcribe | 500 | 0.879 | 71.600 | 21.600 | 6.800 | 95.800 | 95.000 | 95.600 |
| Qwen2.5-VL-32B-Instruct | math | A_text | 500 | 0.868 | 91.000 | 6.200 | 2.800 | 97.800 | 98.200 | 98.400 |
| Qwen2.5-VL-32B-Instruct | math | B_image | 500 | 0.841 | 88.600 | 7.400 | 4.000 | 97.000 | 97.400 | 97.600 |
| Qwen2.5-VL-32B-Instruct | math | C_image_transcribe | 500 | 0.932 | 94.200 | 4.800 | 1.000 | 99.600 | 99.200 | 99.200 |
| Qwen2.5-VL-32B-Instruct | table | A_text | 500 | 0.929 | 79.800 | 17.000 | 3.200 | 98.400 | 97.800 | 97.400 |
| Qwen2.5-VL-32B-Instruct | table | B_image | 500 | 0.897 | 75.800 | 19.000 | 5.200 | 97.000 | 96.800 | 95.800 |
| Qwen2.5-VL-32B-Instruct | table | C_image_transcribe | 500 | 0.920 | 78.400 | 17.800 | 3.800 | 96.800 | 98.400 | 97.200 |
| Qwen2.5-VL-3B-Instruct | code | A_text | 500 | 0.757 | 29.600 | 53.200 | 17.200 | 89.600 | 88.400 | 87.600 |
| Qwen2.5-VL-3B-Instruct | code | B_image | 500 | 0.792 | 25.800 | 60.400 | 13.800 | 90.400 | 91.400 | 90.600 |
| Qwen2.5-VL-3B-Instruct | code | C_image_transcribe | 500 | 0.797 | 29.000 | 57.000 | 14.000 | 90.000 | 91.800 | 90.200 |
| Qwen2.5-VL-3B-Instruct | math | A_text | 500 | 0.897 | 81.800 | 14.000 | 4.200 | 97.600 | 96.400 | 97.600 |
| Qwen2.5-VL-3B-Instruct | math | B_image | 500 | 0.871 | 78.800 | 15.400 | 5.800 | 96.400 | 95.800 | 96.200 |
| Qwen2.5-VL-3B-Instruct | math | C_image_transcribe | 500 | 0.830 | 70.200 | 20.200 | 9.600 | 93.800 | 93.200 | 93.800 |
| Qwen2.5-VL-3B-Instruct | table | A_text | 500 | 0.732 | 33.800 | 46.400 | 19.800 | 87.600 | 84.800 | 88.000 |
| Qwen2.5-VL-3B-Instruct | table | B_image | 500 | 0.823 | 39.400 | 47.400 | 13.200 | 91.400 | 91.200 | 91.000 |
| Qwen2.5-VL-3B-Instruct | table | C_image_transcribe | 500 | 0.754 | 29.600 | 53.000 | 17.400 | 89.400 | 88.000 | 87.800 |
| Qwen2.5-VL-7B-Instruct | code | A_text | 500 | 0.799 | 45.800 | 39.200 | 15.000 | 89.800 | 91.400 | 88.800 |
| Qwen2.5-VL-7B-Instruct | code | B_image | 500 | 0.797 | 41.200 | 43.600 | 15.200 | 90.400 | 89.200 | 90.000 |
| Qwen2.5-VL-7B-Instruct | code | C_image_transcribe | 500 | 0.874 | 42.400 | 48.200 | 9.400 | 94.200 | 92.600 | 94.400 |
| Qwen2.5-VL-7B-Instruct | math | A_text | 500 | 0.851 | 84.600 | 10.400 | 5.000 | 97.000 | 96.600 | 96.400 |
| Qwen2.5-VL-7B-Instruct | math | B_image | 500 | 0.905 | 85.200 | 11.600 | 3.200 | 97.400 | 97.600 | 98.600 |
| Qwen2.5-VL-7B-Instruct | math | C_image_transcribe | 500 | 0.910 | 85.800 | 11.200 | 3.000 | 97.600 | 98.400 | 98.000 |
| Qwen2.5-VL-7B-Instruct | table | A_text | 500 | 0.839 | 56.800 | 31.800 | 11.400 | 92.400 | 91.400 | 93.400 |
| Qwen2.5-VL-7B-Instruct | table | B_image | 500 | 0.882 | 61.600 | 30.400 | 8.000 | 94.200 | 94.800 | 95.000 |
| Qwen2.5-VL-7B-Instruct | table | C_image_transcribe | 500 | 0.883 | 63.000 | 29.200 | 7.800 | 94.600 | 94.600 | 95.200 |
| gemma-3-12b-it | code | A_text | 500 | 0.891 | 65.800 | 27.200 | 7.000 | 96.200 | 94.800 | 95.000 |
| gemma-3-12b-it | code | B_image | 500 | 0.899 | 45.600 | 46.800 | 7.600 | 95.000 | 95.000 | 94.800 |
| gemma-3-12b-it | code | C_image_transcribe | 500 | 0.936 | 51.600 | 43.600 | 4.800 | 96.600 | 97.600 | 96.200 |
| gemma-3-12b-it | math | A_text | 500 | 0.916 | 94.400 | 4.400 | 1.200 | 99.200 | 99.400 | 99.000 |
| gemma-3-12b-it | math | B_image | 500 | 0.946 | 92.800 | 6.200 | 1.000 | 99.200 | 99.400 | 99.400 |
| gemma-3-12b-it | math | C_image_transcribe | 500 | 0.875 | 91.600 | 6.000 | 2.400 | 98.200 | 97.800 | 99.200 |
| gemma-3-12b-it | table | A_text | 500 | 0.932 | 70.800 | 25.200 | 4.000 | 97.800 | 96.800 | 97.400 |
| gemma-3-12b-it | table | B_image | 500 | 0.911 | 63.200 | 30.800 | 6.000 | 95.400 | 96.000 | 96.600 |
| gemma-3-12b-it | table | C_image_transcribe | 500 | 0.849 | 68.400 | 22.600 | 9.000 | 93.000 | 95.000 | 94.000 |

## RQ1 A vs B per run (Holm within each run), primary models

| model_id | content_type | diff_run1 | p_holm_run1 | sig_holm_run1 | diff_run2 | p_holm_run2 | sig_holm_run2 | diff_run3 | p_holm_run3 | sig_holm_run3 | n_runs_sig | sig_agree_all_runs | direction_agree_all_runs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| InternVL3-8B | code | 0.126 | 4.13e-08 | True | 0.110 | 6.10e-06 | True | 0.130 | 1.70e-08 | True | 3 | True | True |
| InternVL3-8B | math | 0.056 | 0.003 | True | 0.052 | 0.014 | True | 0.056 | 0.007 | True | 3 | True | True |
| InternVL3-8B | table | 0.060 | 0.154 | False | 0.086 | 0.006 | True | 0.088 | 0.004 | True | 2 | False | True |
| Qwen2.5-VL-32B-Instruct | code | 0.082 | 6.84e-07 | True | 0.086 | 2.36e-06 | True | 0.082 | 3.62e-06 | True | 3 | True | True |
| Qwen2.5-VL-32B-Instruct | math | 0.016 | 1.000 | False | 0.016 | 1.000 | False | 0.016 | 0.906 | False | 0 | True | True |
| Qwen2.5-VL-32B-Instruct | table | 0.018 | 1.000 | False | 0.036 | 0.219 | False | 0.032 | 0.391 | False | 0 | True | True |
| Qwen2.5-VL-3B-Instruct | code | 0.044 | 0.511 | False | 0.060 | 0.059 | False | 0.054 | 0.135 | False | 0 | True | True |
| Qwen2.5-VL-3B-Instruct | math | 0.022 | 1.000 | False | 0.006 | 1.000 | False | 0.040 | 0.135 | False | 0 | True | True |
| Qwen2.5-VL-3B-Instruct | table | -0.026 | 1.000 | False | 0.000 | 1.000 | False | -0.030 | 0.906 | False | 0 | True | False |
| Qwen2.5-VL-7B-Instruct | code | 0.034 | 0.726 | False | 0.044 | 0.234 | False | 0.036 | 0.475 | False | 0 | True | True |
| Qwen2.5-VL-7B-Instruct | math | 0.000 | 1.000 | False | 0.004 | 1.000 | False | -0.002 | 1.000 | False | 0 | True | False |
| Qwen2.5-VL-7B-Instruct | table | -0.038 | 0.720 | False | -0.032 | 0.762 | False | -0.040 | 0.402 | False | 0 | True | True |
| gemma-3-12b-it | code | 0.194 | 1.07e-16 | True | 0.198 | 8.59e-18 | True | 0.188 | 1.03e-15 | True | 3 | True | True |
| gemma-3-12b-it | math | 0.014 | 1.000 | False | 0.018 | 0.732 | False | 0.018 | 0.598 | False | 0 | True | True |
| gemma-3-12b-it | table | 0.086 | 0.003 | True | 0.058 | 0.141 | False | 0.062 | 0.080 | False | 1 | False | True |

- cells significant in all runs: 4; in some but not all: 2; in none: 9 (of 15)

## RQ1 A vs B on majority vote (correct in >= 2 of 3 runs), primary models

| model_id | content_type | n_pairs | acc_first | acc_second | b_first_only | c_second_only | diff | diff_ci_lo | diff_ci_hi | p_mcnemar_exact | p_holm |
|---|---|---|---|---|---|---|---|---|---|---|---|
| InternVL3-8B | code | 500 | 0.632 | 0.500 | 91 | 25 | 0.132 | 0.091 | 0.172 | 5.31e-10 | 7.44e-09 |
| InternVL3-8B | math | 500 | 0.920 | 0.860 | 46 | 16 | 0.060 | 0.030 | 0.092 | 1.76e-04 | 0.002 |
| InternVL3-8B | table | 500 | 0.668 | 0.586 | 96 | 55 | 0.082 | 0.034 | 0.129 | 0.001 | 0.012 |
| Qwen2.5-VL-32B-Instruct | code | 500 | 0.814 | 0.738 | 47 | 9 | 0.076 | 0.047 | 0.105 | 2.57e-07 | 3.34e-06 |
| Qwen2.5-VL-32B-Instruct | math | 500 | 0.922 | 0.910 | 27 | 21 | 0.012 | -0.016 | 0.040 | 0.471 | 1.000 |
| Qwen2.5-VL-32B-Instruct | table | 500 | 0.818 | 0.792 | 36 | 23 | 0.026 | -0.004 | 0.057 | 0.117 | 0.822 |
| Qwen2.5-VL-3B-Instruct | code | 500 | 0.382 | 0.334 | 63 | 39 | 0.048 | 0.008 | 0.087 | 0.022 | 0.201 |
| Qwen2.5-VL-3B-Instruct | math | 500 | 0.838 | 0.814 | 37 | 25 | 0.024 | -0.007 | 0.055 | 0.162 | 0.971 |
| Qwen2.5-VL-3B-Instruct | table | 500 | 0.446 | 0.456 | 89 | 94 | -0.010 | -0.063 | 0.043 | 0.768 | 1.000 |
| Qwen2.5-VL-7B-Instruct | code | 500 | 0.510 | 0.486 | 53 | 41 | 0.024 | -0.014 | 0.062 | 0.256 | 1.000 |
| Qwen2.5-VL-7B-Instruct | math | 500 | 0.874 | 0.878 | 17 | 19 | -0.004 | -0.028 | 0.020 | 0.868 | 1.000 |
| Qwen2.5-VL-7B-Instruct | table | 500 | 0.610 | 0.658 | 41 | 65 | -0.048 | -0.088 | -0.008 | 0.025 | 0.201 |
| gemma-3-12b-it | code | 500 | 0.684 | 0.502 | 110 | 19 | 0.182 | 0.140 | 0.223 | 9.11e-17 | 1.37e-15 |
| gemma-3-12b-it | math | 500 | 0.950 | 0.934 | 18 | 10 | 0.016 | -0.006 | 0.039 | 0.185 | 0.971 |
| gemma-3-12b-it | table | 500 | 0.732 | 0.658 | 82 | 45 | 0.074 | 0.030 | 0.118 | 0.001 | 0.013 |

## RQ1 A vs C per run (Holm within each run), primary models

| model_id | content_type | diff_run1 | p_holm_run1 | sig_holm_run1 | diff_run2 | p_holm_run2 | sig_holm_run2 | diff_run3 | p_holm_run3 | sig_holm_run3 | n_runs_sig | sig_agree_all_runs | direction_agree_all_runs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| InternVL3-8B | code | 0.110 | 4.00e-06 | True | 0.090 | 3.02e-04 | True | 0.114 | 4.07e-07 | True | 3 | True | True |
| InternVL3-8B | math | 0.026 | 0.426 | False | 0.028 | 0.269 | False | 0.022 | 0.757 | False | 0 | True | True |
| InternVL3-8B | table | 0.020 | 1.000 | False | 0.058 | 0.155 | False | 0.062 | 0.113 | False | 0 | True | True |
| Qwen2.5-VL-32B-Instruct | code | 0.072 | 1.69e-04 | True | 0.060 | 0.003 | True | 0.066 | 0.001 | True | 3 | True | True |
| Qwen2.5-VL-32B-Instruct | math | -0.030 | 0.303 | False | -0.024 | 0.301 | False | -0.020 | 0.860 | False | 0 | True | True |
| Qwen2.5-VL-32B-Instruct | table | 0.006 | 1.000 | False | 0.018 | 1.000 | False | 0.016 | 1.000 | False | 0 | True | True |
| Qwen2.5-VL-3B-Instruct | code | 0.028 | 1.000 | False | 0.040 | 0.310 | False | 0.002 | 1.000 | False | 0 | True | True |
| Qwen2.5-VL-3B-Instruct | math | 0.088 | 1.64e-04 | True | 0.086 | 2.07e-04 | True | 0.096 | 3.56e-05 | True | 3 | True | True |
| Qwen2.5-VL-3B-Instruct | table | 0.036 | 1.000 | False | 0.094 | 0.006 | True | 0.052 | 0.650 | False | 1 | False | True |
| Qwen2.5-VL-7B-Instruct | code | 0.044 | 0.303 | False | 0.060 | 0.035 | True | 0.048 | 0.213 | False | 1 | False | True |
| Qwen2.5-VL-7B-Instruct | math | 0.002 | 1.000 | False | -0.004 | 1.000 | False | 0.000 | 1.000 | False | 0 | True | False |
| Qwen2.5-VL-7B-Instruct | table | -0.042 | 0.448 | False | -0.048 | 0.211 | False | -0.058 | 0.103 | False | 0 | True | True |
| gemma-3-12b-it | code | 0.146 | 4.86e-11 | True | 0.154 | 3.83e-12 | True | 0.146 | 1.69e-11 | True | 3 | True | True |
| gemma-3-12b-it | math | 0.026 | 0.316 | False | 0.012 | 1.000 | False | 0.018 | 0.860 | False | 0 | True | True |
| gemma-3-12b-it | table | 0.008 | 1.000 | False | 0.004 | 1.000 | False | -0.006 | 1.000 | False | 0 | True | False |

- cells significant in all runs: 4; in some but not all: 2; in none: 9 (of 15)

## RQ1 A vs C on majority vote (correct in >= 2 of 3 runs), primary models

| model_id | content_type | n_pairs | acc_first | acc_second | b_first_only | c_second_only | diff | diff_ci_lo | diff_ci_hi | p_mcnemar_exact | p_holm |
|---|---|---|---|---|---|---|---|---|---|---|---|
| InternVL3-8B | code | 500 | 0.632 | 0.530 | 79 | 28 | 0.102 | 0.062 | 0.141 | 8.42e-07 | 1.18e-05 |
| InternVL3-8B | math | 500 | 0.920 | 0.892 | 27 | 13 | 0.028 | 0.003 | 0.054 | 0.038 | 0.269 |
| InternVL3-8B | table | 500 | 0.668 | 0.612 | 84 | 56 | 0.056 | 0.010 | 0.102 | 0.022 | 0.199 |
| Qwen2.5-VL-32B-Instruct | code | 500 | 0.814 | 0.748 | 50 | 17 | 0.066 | 0.034 | 0.098 | 6.74e-05 | 8.09e-04 |
| Qwen2.5-VL-32B-Instruct | math | 500 | 0.922 | 0.950 | 12 | 26 | -0.028 | -0.054 | -0.004 | 0.034 | 0.268 |
| Qwen2.5-VL-32B-Instruct | table | 500 | 0.818 | 0.800 | 32 | 23 | 0.018 | -0.011 | 0.048 | 0.281 | 1.000 |
| Qwen2.5-VL-3B-Instruct | code | 500 | 0.382 | 0.356 | 60 | 47 | 0.026 | -0.015 | 0.066 | 0.246 | 1.000 |
| Qwen2.5-VL-3B-Instruct | math | 500 | 0.838 | 0.746 | 73 | 27 | 0.092 | 0.053 | 0.131 | 4.69e-06 | 6.10e-05 |
| Qwen2.5-VL-3B-Instruct | table | 500 | 0.446 | 0.372 | 114 | 77 | 0.074 | 0.020 | 0.127 | 0.009 | 0.090 |
| Qwen2.5-VL-7B-Instruct | code | 500 | 0.510 | 0.482 | 57 | 43 | 0.028 | -0.011 | 0.067 | 0.193 | 1.000 |
| Qwen2.5-VL-7B-Instruct | math | 500 | 0.874 | 0.872 | 21 | 20 | 0.002 | -0.024 | 0.028 | 1.000 | 1.000 |
| Qwen2.5-VL-7B-Instruct | table | 500 | 0.610 | 0.670 | 43 | 73 | -0.060 | -0.102 | -0.018 | 0.007 | 0.075 |
| gemma-3-12b-it | code | 500 | 0.684 | 0.544 | 90 | 20 | 0.140 | 0.100 | 0.179 | 8.64e-12 | 1.30e-10 |
| gemma-3-12b-it | math | 500 | 0.950 | 0.938 | 17 | 11 | 0.012 | -0.010 | 0.034 | 0.345 | 1.000 |
| gemma-3-12b-it | table | 500 | 0.732 | 0.724 | 63 | 59 | 0.008 | -0.035 | 0.051 | 0.786 | 1.000 |

## RQ1 A vs B paired permutation test on per-item mean correctness (10,000 perms, seed 630), primary models

| model_id | content_type | comparison | n_items | mean_acc_first | mean_acc_second | mean_diff | n_perm | seed | p_perm | p_holm |
|---|---|---|---|---|---|---|---|---|---|---|
| InternVL3-8B | code | A_text vs B_image | 500 | 0.631 | 0.509 | 0.122 | 10000 | 630 | 1.00e-04 | 0.001 |
| InternVL3-8B | math | A_text vs B_image | 500 | 0.918 | 0.863 | 0.055 | 10000 | 630 | 1.00e-04 | 0.001 |
| InternVL3-8B | table | A_text vs B_image | 500 | 0.666 | 0.588 | 0.078 | 10000 | 630 | 5.00e-04 | 0.005 |
| Qwen2.5-VL-32B-Instruct | code | A_text vs B_image | 500 | 0.815 | 0.732 | 0.083 | 10000 | 630 | 1.00e-04 | 0.001 |
| Qwen2.5-VL-32B-Instruct | math | A_text vs B_image | 500 | 0.923 | 0.907 | 0.016 | 10000 | 630 | 0.234 | 0.702 |
| Qwen2.5-VL-32B-Instruct | table | A_text vs B_image | 500 | 0.815 | 0.787 | 0.029 | 10000 | 630 | 0.052 | 0.364 |
| Qwen2.5-VL-3B-Instruct | code | A_text vs B_image | 500 | 0.382 | 0.329 | 0.053 | 10000 | 630 | 0.004 | 0.037 |
| Qwen2.5-VL-3B-Instruct | math | A_text vs B_image | 500 | 0.839 | 0.816 | 0.023 | 10000 | 630 | 0.134 | 0.560 |
| Qwen2.5-VL-3B-Instruct | table | A_text vs B_image | 500 | 0.440 | 0.459 | -0.019 | 10000 | 630 | 0.458 | 0.916 |
| Qwen2.5-VL-7B-Instruct | code | A_text vs B_image | 500 | 0.525 | 0.487 | 0.038 | 10000 | 630 | 0.021 | 0.170 |
| Qwen2.5-VL-7B-Instruct | math | A_text vs B_image | 500 | 0.872 | 0.871 | 6.67e-04 | 10000 | 630 | 1.000 | 1.000 |
| Qwen2.5-VL-7B-Instruct | table | A_text vs B_image | 500 | 0.620 | 0.657 | -0.037 | 10000 | 630 | 0.054 | 0.364 |
| gemma-3-12b-it | code | A_text vs B_image | 500 | 0.690 | 0.497 | 0.193 | 10000 | 630 | 1.00e-04 | 0.001 |
| gemma-3-12b-it | math | A_text vs B_image | 500 | 0.950 | 0.933 | 0.017 | 10000 | 630 | 0.112 | 0.560 |
| gemma-3-12b-it | table | A_text vs B_image | 500 | 0.729 | 0.661 | 0.069 | 10000 | 630 | 0.002 | 0.024 |

## RQ2 A−C gap, wrong vs correct transcription, per run, primary models

| model_id | content_type | subset_rule | run | gap_A_minus_C_wrong | gap_A_minus_C_correct | n_pairs_wrong | n_pairs_correct | gap_wrong_minus_correct | pattern_wrong_gt_correct |
|---|---|---|---|---|---|---|---|---|---|
| InternVL3-8B | code | cer_le_0.02 | 1 | 0.230 | 0.093 | 61 | 439.000 | 0.136 | True |
| InternVL3-8B | code | cer_le_0.02 | 2 | 0.167 | 0.080 | 60 | 440.000 | 0.087 | True |
| InternVL3-8B | code | cer_le_0.02 | 3 | 0.172 | 0.106 | 58 | 442.000 | 0.066 | True |
| InternVL3-8B | code | exact | 1 | 0.238 | 0.048 | 164 | 336.000 | 0.190 | True |
| InternVL3-8B | code | exact | 2 | 0.165 | 0.054 | 164 | 336.000 | 0.111 | True |
| InternVL3-8B | code | exact | 3 | 0.217 | 0.065 | 161 | 339.000 | 0.152 | True |
| InternVL3-8B | math | cer_le_0.02 | 1 | 0.000 | 0.026 | 7 | 493.000 | -0.026 | False |
| InternVL3-8B | math | cer_le_0.02 | 2 | 0.000 | 0.028 | 8 | 492.000 | -0.028 | False |
| InternVL3-8B | math | cer_le_0.02 | 3 | 0.000 | 0.022 | 8 | 492.000 | -0.022 | False |
| InternVL3-8B | math | exact | 1 | 0.188 | 0.015 | 32 | 468.000 | 0.173 | True |
| InternVL3-8B | math | exact | 2 | 0.219 | 0.015 | 32 | 468.000 | 0.204 | True |
| InternVL3-8B | math | exact | 3 | 0.212 | 0.009 | 33 | 467.000 | 0.204 | True |
| InternVL3-8B | table | cer_le_0.02 | 1 | 0.021 | 0.000 | 467 | 33.000 | 0.021 | True |
| InternVL3-8B | table | cer_le_0.02 | 2 | 0.064 | -0.030 | 467 | 33.000 | 0.095 | True |
| InternVL3-8B | table | cer_le_0.02 | 3 | 0.066 | 0.000 | 472 | 28.000 | 0.066 | True |
| InternVL3-8B | table | exact | 1 | 0.020 |  | 500 |  |  | False |
| InternVL3-8B | table | exact | 2 | 0.058 |  | 500 |  |  | False |
| InternVL3-8B | table | exact | 3 | 0.062 |  | 500 |  |  | False |
| Qwen2.5-VL-32B-Instruct | code | cer_le_0.02 | 1 | 0.200 | 0.065 | 25 | 475.000 | 0.135 | True |
| Qwen2.5-VL-32B-Instruct | code | cer_le_0.02 | 2 | 0.167 | 0.055 | 24 | 476.000 | 0.112 | True |
| Qwen2.5-VL-32B-Instruct | code | cer_le_0.02 | 3 | 0.154 | 0.061 | 26 | 474.000 | 0.093 | True |
| Qwen2.5-VL-32B-Instruct | code | exact | 1 | 0.252 | 0.021 | 111 | 389.000 | 0.232 | True |
| Qwen2.5-VL-32B-Instruct | code | exact | 2 | 0.245 | 0.008 | 110 | 390.000 | 0.238 | True |
| Qwen2.5-VL-32B-Instruct | code | exact | 3 | 0.220 | 0.023 | 109 | 391.000 | 0.197 | True |
| Qwen2.5-VL-32B-Instruct | math | cer_le_0.02 | 1 | 0.333 | -0.034 | 6 | 494.000 | 0.368 | True |
| Qwen2.5-VL-32B-Instruct | math | cer_le_0.02 | 2 | 0.200 | -0.026 | 5 | 495.000 | 0.226 | True |
| Qwen2.5-VL-32B-Instruct | math | cer_le_0.02 | 3 | 0.143 | -0.022 | 7 | 493.000 | 0.165 | True |
| Qwen2.5-VL-32B-Instruct | math | exact | 1 | 0.111 | -0.038 | 27 | 473.000 | 0.149 | True |
| Qwen2.5-VL-32B-Instruct | math | exact | 2 | 0.077 | -0.030 | 26 | 474.000 | 0.106 | True |
| Qwen2.5-VL-32B-Instruct | math | exact | 3 | 0.071 | -0.025 | 28 | 472.000 | 0.097 | True |
| Qwen2.5-VL-32B-Instruct | table | cer_le_0.02 | 1 | 0.015 | -0.012 | 338 | 162.000 | 0.027 | True |
| Qwen2.5-VL-32B-Instruct | table | cer_le_0.02 | 2 | 0.021 | 0.012 | 337 | 163.000 | 0.009 | True |
| Qwen2.5-VL-32B-Instruct | table | cer_le_0.02 | 3 | 0.021 | 0.006 | 332 | 168.000 | 0.015 | True |
| Qwen2.5-VL-32B-Instruct | table | exact | 1 | 0.006 | 0.000 | 498 | 2.000 | 0.006 | True |
| Qwen2.5-VL-32B-Instruct | table | exact | 2 | 0.018 | 0.000 | 498 | 2.000 | 0.018 | True |
| Qwen2.5-VL-32B-Instruct | table | exact | 3 | 0.016 | 0.000 | 499 | 1.000 | 0.016 | True |
| Qwen2.5-VL-3B-Instruct | code | cer_le_0.02 | 1 | 0.054 | 0.025 | 56 | 444.000 | 0.029 | True |
| Qwen2.5-VL-3B-Instruct | code | cer_le_0.02 | 2 | 0.052 | 0.038 | 58 | 442.000 | 0.013 | True |
| Qwen2.5-VL-3B-Instruct | code | cer_le_0.02 | 3 | 0.069 | -0.007 | 58 | 442.000 | 0.076 | True |
| Qwen2.5-VL-3B-Instruct | code | exact | 1 | 0.079 | 0.003 | 165 | 335.000 | 0.076 | True |
| Qwen2.5-VL-3B-Instruct | code | exact | 2 | 0.083 | 0.018 | 168 | 332.000 | 0.065 | True |
| Qwen2.5-VL-3B-Instruct | code | exact | 3 | 0.078 | -0.036 | 167 | 333.000 | 0.114 | True |
| Qwen2.5-VL-3B-Instruct | math | cer_le_0.02 | 1 | 0.600 | 0.078 | 10 | 490.000 | 0.522 | True |
| Qwen2.5-VL-3B-Instruct | math | cer_le_0.02 | 2 | 0.273 | 0.082 | 11 | 489.000 | 0.191 | True |
| Qwen2.5-VL-3B-Instruct | math | cer_le_0.02 | 3 | 0.556 | 0.088 | 9 | 491.000 | 0.468 | True |
| Qwen2.5-VL-3B-Instruct | math | exact | 1 | 0.297 | 0.071 | 37 | 463.000 | 0.226 | True |
| Qwen2.5-VL-3B-Instruct | math | exact | 2 | 0.216 | 0.076 | 37 | 463.000 | 0.141 | True |
| Qwen2.5-VL-3B-Instruct | math | exact | 3 | 0.206 | 0.088 | 34 | 466.000 | 0.118 | True |
| Qwen2.5-VL-3B-Instruct | table | cer_le_0.02 | 1 | 0.047 | -0.125 | 468 | 32.000 | 0.172 | True |
| Qwen2.5-VL-3B-Instruct | table | cer_le_0.02 | 2 | 0.113 | -0.200 | 470 | 30.000 | 0.313 | True |
| Qwen2.5-VL-3B-Instruct | table | cer_le_0.02 | 3 | 0.058 | -0.030 | 467 | 33.000 | 0.088 | True |
| Qwen2.5-VL-3B-Instruct | table | exact | 1 | 0.036 |  | 500 |  |  | False |
| Qwen2.5-VL-3B-Instruct | table | exact | 2 | 0.094 |  | 500 |  |  | False |
| Qwen2.5-VL-3B-Instruct | table | exact | 3 | 0.052 |  | 500 |  |  | False |
| Qwen2.5-VL-7B-Instruct | code | cer_le_0.02 | 1 | 0.125 | 0.041 | 16 | 484.000 | 0.084 | True |
| Qwen2.5-VL-7B-Instruct | code | cer_le_0.02 | 2 | 0.062 | 0.060 | 16 | 484.000 | 0.003 | True |
| Qwen2.5-VL-7B-Instruct | code | cer_le_0.02 | 3 | 0.062 | 0.048 | 16 | 484.000 | 0.015 | True |
| Qwen2.5-VL-7B-Instruct | code | exact | 1 | 0.121 | 0.032 | 66 | 434.000 | 0.089 | True |
| Qwen2.5-VL-7B-Instruct | code | exact | 2 | 0.123 | 0.051 | 65 | 435.000 | 0.073 | True |
| Qwen2.5-VL-7B-Instruct | code | exact | 3 | 0.108 | 0.039 | 65 | 435.000 | 0.069 | True |
| Qwen2.5-VL-7B-Instruct | math | cer_le_0.02 | 1 | 0.048 | -0.007 | 83 | 417.000 | 0.055 | True |
| Qwen2.5-VL-7B-Instruct | math | cer_le_0.02 | 2 | 0.057 | -0.017 | 87 | 413.000 | 0.074 | True |
| Qwen2.5-VL-7B-Instruct | math | cer_le_0.02 | 3 | 0.049 | -0.010 | 82 | 418.000 | 0.058 | True |
| Qwen2.5-VL-7B-Instruct | math | exact | 1 | 0.033 | -0.005 | 92 | 408.000 | 0.038 | True |
| Qwen2.5-VL-7B-Instruct | math | exact | 2 | 0.053 | -0.017 | 95 | 405.000 | 0.070 | True |
| Qwen2.5-VL-7B-Instruct | math | exact | 3 | 0.033 | -0.007 | 90 | 410.000 | 0.041 | True |
| Qwen2.5-VL-7B-Instruct | table | cer_le_0.02 | 1 | -0.060 | 0.030 | 399 | 101.000 | -0.090 | False |
| Qwen2.5-VL-7B-Instruct | table | cer_le_0.02 | 2 | -0.058 | -0.010 | 396 | 104.000 | -0.048 | False |
| Qwen2.5-VL-7B-Instruct | table | cer_le_0.02 | 3 | -0.089 | 0.057 | 394 | 106.000 | -0.145 | False |
| Qwen2.5-VL-7B-Instruct | table | exact | 1 | -0.042 |  | 500 |  |  | False |
| Qwen2.5-VL-7B-Instruct | table | exact | 2 | -0.048 |  | 500 |  |  | False |
| Qwen2.5-VL-7B-Instruct | table | exact | 3 | -0.058 |  | 500 |  |  | False |
| gemma-3-12b-it | code | cer_le_0.02 | 1 | 0.156 | 0.098 | 418 | 82.000 | 0.058 | True |
| gemma-3-12b-it | code | cer_le_0.02 | 2 | 0.178 | 0.014 | 428 | 72.000 | 0.164 | True |
| gemma-3-12b-it | code | cer_le_0.02 | 3 | 0.160 | 0.066 | 424 | 76.000 | 0.095 | True |
| gemma-3-12b-it | code | exact | 1 | 0.158 | 0.040 | 450 | 50.000 | 0.118 | True |
| gemma-3-12b-it | code | exact | 2 | 0.171 | -0.022 | 455 | 45.000 | 0.194 | True |
| gemma-3-12b-it | code | exact | 3 | 0.158 | 0.023 | 456 | 44.000 | 0.135 | True |
| gemma-3-12b-it | math | cer_le_0.02 | 1 | 0.044 | 0.021 | 114 | 386.000 | 0.023 | True |
| gemma-3-12b-it | math | cer_le_0.02 | 2 | 0.027 | 0.008 | 112 | 388.000 | 0.019 | True |
| gemma-3-12b-it | math | cer_le_0.02 | 3 | 0.035 | 0.013 | 113 | 387.000 | 0.022 | True |
| gemma-3-12b-it | math | exact | 1 | 0.066 | 0.009 | 151 | 349.000 | 0.058 | True |
| gemma-3-12b-it | math | exact | 2 | 0.053 | -0.006 | 150 | 350.000 | 0.059 | True |
| gemma-3-12b-it | math | exact | 3 | 0.054 | 0.003 | 149 | 351.000 | 0.051 | True |
| gemma-3-12b-it | table | cer_le_0.02 | 1 | 0.009 | 0.000 | 461 | 39.000 | 0.009 | True |
| gemma-3-12b-it | table | cer_le_0.02 | 2 | 0.004 | 0.000 | 463 | 37.000 | 0.004 | True |
| gemma-3-12b-it | table | cer_le_0.02 | 3 | -0.007 | 0.000 | 459 | 41.000 | -0.007 | False |
| gemma-3-12b-it | table | exact | 1 | 0.008 |  | 500 |  |  | False |
| gemma-3-12b-it | table | exact | 2 | 0.004 |  | 500 |  |  | False |
| gemma-3-12b-it | table | exact | 3 | -0.006 |  | 500 |  |  | False |

## T16/T18 accuracy across runs, extension models (exploratory)

| model_id | content_type | condition | acc_run1 | acc_run2 | acc_run3 | n_runs | mean | sd | range |
|---|---|---|---|---|---|---|---|---|---|
| InternVL3_5-8B | code | A_text | 0.734 | 0.728 | 0.722 | 3 | 0.728 | 0.006 | 0.012 |
| InternVL3_5-8B | code | B_image | 0.626 | 0.630 | 0.634 | 3 | 0.630 | 0.004 | 0.008 |
| InternVL3_5-8B | code | C_image_transcribe | 0.642 | 0.658 | 0.656 | 3 | 0.652 | 0.009 | 0.016 |
| InternVL3_5-8B | math | A_text | 0.954 | 0.952 | 0.958 | 3 | 0.955 | 0.003 | 0.006 |
| InternVL3_5-8B | math | B_image | 0.838 | 0.834 | 0.838 | 3 | 0.837 | 0.002 | 0.004 |
| InternVL3_5-8B | math | C_image_transcribe | 0.942 | 0.942 | 0.944 | 3 | 0.943 | 0.001 | 0.002 |
| InternVL3_5-8B | table | A_text | 0.766 | 0.772 | 0.762 | 3 | 0.767 | 0.005 | 0.010 |
| InternVL3_5-8B | table | B_image | 0.716 | 0.716 | 0.720 | 3 | 0.717 | 0.002 | 0.004 |
| InternVL3_5-8B | table | C_image_transcribe | 0.746 | 0.730 | 0.730 | 3 | 0.735 | 0.009 | 0.016 |
| Qwen2.5-VL-72B-Instruct-AWQ | code | A_text | 0.798 | 0.812 | 0.820 | 3 | 0.810 | 0.011 | 0.022 |
| Qwen2.5-VL-72B-Instruct-AWQ | code | B_image | 0.758 | 0.746 | 0.750 | 3 | 0.751 | 0.006 | 0.012 |
| Qwen2.5-VL-72B-Instruct-AWQ | code | C_image_transcribe | 0.754 | 0.762 | 0.764 | 3 | 0.760 | 0.005 | 0.010 |
| Qwen2.5-VL-72B-Instruct-AWQ | math | A_text | 0.966 | 0.966 | 0.966 | 3 | 0.966 | 1.36e-16 | 0.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | math | B_image | 0.956 | 0.958 | 0.958 | 3 | 0.957 | 0.001 | 0.002 |
| Qwen2.5-VL-72B-Instruct-AWQ | math | C_image_transcribe | 0.960 | 0.964 | 0.958 | 3 | 0.961 | 0.003 | 0.006 |
| Qwen2.5-VL-72B-Instruct-AWQ | table | A_text | 0.812 | 0.816 | 0.822 | 3 | 0.817 | 0.005 | 0.010 |
| Qwen2.5-VL-72B-Instruct-AWQ | table | B_image | 0.808 | 0.804 | 0.804 | 3 | 0.805 | 0.002 | 0.004 |
| Qwen2.5-VL-72B-Instruct-AWQ | table | C_image_transcribe | 0.816 | 0.818 | 0.806 | 3 | 0.813 | 0.006 | 0.012 |
| Qwen3-VL-8B-Instruct | code | A_text | 0.808 | 0.796 | 0.784 | 3 | 0.796 | 0.012 | 0.024 |
| Qwen3-VL-8B-Instruct | code | B_image | 0.686 | 0.698 | 0.684 | 3 | 0.689 | 0.008 | 0.014 |
| Qwen3-VL-8B-Instruct | code | C_image_transcribe | 0.702 | 0.694 | 0.696 | 3 | 0.697 | 0.004 | 0.008 |
| Qwen3-VL-8B-Instruct | math | A_text | 0.952 | 0.946 | 0.948 | 3 | 0.949 | 0.003 | 0.006 |
| Qwen3-VL-8B-Instruct | math | B_image | 0.942 | 0.940 | 0.942 | 3 | 0.941 | 0.001 | 0.002 |
| Qwen3-VL-8B-Instruct | math | C_image_transcribe | 0.954 | 0.954 | 0.958 | 3 | 0.955 | 0.002 | 0.004 |
| Qwen3-VL-8B-Instruct | table | A_text | 0.828 | 0.816 | 0.828 | 3 | 0.824 | 0.007 | 0.012 |
| Qwen3-VL-8B-Instruct | table | B_image | 0.778 | 0.768 | 0.778 | 3 | 0.775 | 0.006 | 0.010 |
| Qwen3-VL-8B-Instruct | table | C_image_transcribe | 0.798 | 0.800 | 0.804 | 3 | 0.801 | 0.003 | 0.006 |
| gemma-3-27b-it | code | A_text | 0.758 | 0.746 | 0.764 | 3 | 0.756 | 0.009 | 0.018 |
| gemma-3-27b-it | code | B_image | 0.612 | 0.612 | 0.612 | 3 | 0.612 | 0.000 | 0.000 |
| gemma-3-27b-it | code | C_image_transcribe | 0.684 | 0.676 | 0.682 | 3 | 0.681 | 0.004 | 0.008 |
| gemma-3-27b-it | math | A_text | 0.972 | 0.970 | 0.966 | 3 | 0.969 | 0.003 | 0.006 |
| gemma-3-27b-it | math | B_image | 0.946 | 0.948 | 0.948 | 3 | 0.947 | 0.001 | 0.002 |
| gemma-3-27b-it | math | C_image_transcribe | 0.948 | 0.948 | 0.942 | 3 | 0.946 | 0.003 | 0.006 |
| gemma-3-27b-it | table | A_text | 0.778 | 0.764 | 0.766 | 3 | 0.769 | 0.008 | 0.014 |
| gemma-3-27b-it | table | B_image | 0.742 | 0.736 | 0.736 | 3 | 0.738 | 0.003 | 0.006 |
| gemma-3-27b-it | table | C_image_transcribe | 0.746 | 0.754 | 0.758 | 3 | 0.753 | 0.006 | 0.012 |

## Item-level stability across 3 runs, extension models (exploratory)

| model_id | content_type | condition | n_items | fleiss_kappa | pct_correct_all3 | pct_correct_none | pct_mixed | pct_agree_run1_run2 | pct_agree_run1_run3 | pct_agree_run2_run3 |
|---|---|---|---|---|---|---|---|---|---|---|
| InternVL3_5-8B | code | A_text | 500 | 0.862 | 68.600 | 23.200 | 8.200 | 94.600 | 95.200 | 93.800 |
| InternVL3_5-8B | code | B_image | 500 | 0.877 | 59.000 | 32.400 | 8.600 | 95.200 | 93.600 | 94.000 |
| InternVL3_5-8B | code | C_image_transcribe | 500 | 0.906 | 62.000 | 31.600 | 6.400 | 95.200 | 95.400 | 96.600 |
| InternVL3_5-8B | math | A_text | 500 | 0.923 | 94.800 | 4.200 | 1.000 | 99.000 | 99.600 | 99.400 |
| InternVL3_5-8B | math | B_image | 500 | 0.868 | 81.000 | 13.600 | 5.400 | 97.600 | 95.200 | 96.400 |
| InternVL3_5-8B | math | C_image_transcribe | 500 | 0.914 | 93.600 | 5.000 | 1.400 | 99.200 | 99.000 | 99.000 |
| InternVL3_5-8B | table | A_text | 500 | 0.944 | 75.200 | 21.800 | 3.000 | 97.400 | 98.000 | 98.600 |
| InternVL3_5-8B | table | B_image | 500 | 0.895 | 68.400 | 25.200 | 6.400 | 96.000 | 96.000 | 95.200 |
| InternVL3_5-8B | table | C_image_transcribe | 500 | 0.887 | 70.200 | 23.200 | 6.600 | 95.200 | 94.800 | 96.800 |
| Qwen2.5-VL-72B-Instruct-AWQ | code | A_text | 500 | 0.909 | 78.800 | 17.000 | 4.200 | 97.000 | 97.000 | 97.600 |
| Qwen2.5-VL-72B-Instruct-AWQ | code | B_image | 500 | 0.900 | 72.600 | 21.800 | 5.600 | 96.800 | 96.000 | 96.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | code | C_image_transcribe | 500 | 0.931 | 74.000 | 22.200 | 3.800 | 97.600 | 97.000 | 97.800 |
| Qwen2.5-VL-72B-Instruct-AWQ | math | A_text | 500 | 0.959 | 96.400 | 3.200 | 0.400 | 99.600 | 99.600 | 100.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | math | B_image | 500 | 0.918 | 95.200 | 3.800 | 1.000 | 99.400 | 99.000 | 99.600 |
| Qwen2.5-VL-72B-Instruct-AWQ | math | C_image_transcribe | 500 | 0.929 | 95.600 | 3.600 | 0.800 | 99.600 | 99.400 | 99.400 |
| Qwen2.5-VL-72B-Instruct-AWQ | table | A_text | 500 | 0.911 | 79.800 | 16.200 | 4.000 | 97.600 | 97.000 | 97.400 |
| Qwen2.5-VL-72B-Instruct-AWQ | table | B_image | 500 | 0.945 | 79.200 | 18.200 | 2.600 | 98.400 | 98.400 | 98.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | table | C_image_transcribe | 500 | 0.903 | 79.000 | 16.600 | 4.400 | 97.400 | 96.600 | 97.200 |
| Qwen3-VL-8B-Instruct | code | A_text | 500 | 0.832 | 75.600 | 16.200 | 8.200 | 94.000 | 94.800 | 94.800 |
| Qwen3-VL-8B-Instruct | code | B_image | 500 | 0.835 | 63.800 | 25.600 | 10.600 | 92.800 | 93.800 | 92.200 |
| Qwen3-VL-8B-Instruct | code | C_image_transcribe | 500 | 0.883 | 65.800 | 26.800 | 7.400 | 94.800 | 95.400 | 95.000 |
| Qwen3-VL-8B-Instruct | math | A_text | 500 | 0.904 | 94.200 | 4.400 | 1.400 | 99.000 | 99.200 | 99.000 |
| Qwen3-VL-8B-Instruct | math | B_image | 500 | 0.928 | 93.600 | 5.200 | 1.200 | 99.000 | 99.200 | 99.400 |
| Qwen3-VL-8B-Instruct | math | C_image_transcribe | 500 | 0.875 | 94.600 | 3.800 | 1.600 | 98.800 | 98.800 | 99.200 |
| Qwen3-VL-8B-Instruct | table | A_text | 500 | 0.857 | 79.200 | 14.600 | 6.200 | 95.200 | 96.400 | 96.000 |
| Qwen3-VL-8B-Instruct | table | B_image | 500 | 0.863 | 74.000 | 18.800 | 7.200 | 95.000 | 95.200 | 95.400 |
| Qwen3-VL-8B-Instruct | table | C_image_transcribe | 500 | 0.862 | 76.800 | 16.600 | 6.600 | 95.400 | 95.000 | 96.400 |
| gemma-3-27b-it | code | A_text | 500 | 0.924 | 73.400 | 22.400 | 4.200 | 96.800 | 98.200 | 96.600 |
| gemma-3-27b-it | code | B_image | 500 | 0.921 | 58.600 | 35.800 | 5.600 | 95.600 | 96.400 | 96.800 |
| gemma-3-27b-it | code | C_image_transcribe | 500 | 0.939 | 66.200 | 29.800 | 4.000 | 97.200 | 97.000 | 97.800 |
| gemma-3-27b-it | math | A_text | 500 | 0.910 | 96.400 | 2.800 | 0.800 | 99.800 | 99.400 | 99.200 |
| gemma-3-27b-it | math | B_image | 500 | 0.960 | 94.400 | 5.000 | 0.600 | 99.800 | 99.400 | 99.600 |
| gemma-3-27b-it | math | C_image_transcribe | 500 | 0.935 | 94.200 | 4.800 | 1.000 | 99.200 | 99.400 | 99.400 |
| gemma-3-27b-it | table | A_text | 500 | 0.940 | 75.400 | 21.400 | 3.200 | 97.800 | 98.000 | 97.800 |
| gemma-3-27b-it | table | B_image | 500 | 0.945 | 72.200 | 24.600 | 3.200 | 98.200 | 97.400 | 98.000 |
| gemma-3-27b-it | table | C_image_transcribe | 500 | 0.950 | 74.000 | 23.200 | 2.800 | 98.400 | 98.000 | 98.000 |

## RQ1 A vs B per run (Holm within each run), extension models (exploratory)

| model_id | content_type | diff_run1 | p_holm_run1 | sig_holm_run1 | diff_run2 | p_holm_run2 | sig_holm_run2 | diff_run3 | p_holm_run3 | sig_holm_run3 | n_runs_sig | sig_agree_all_runs | direction_agree_all_runs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| InternVL3_5-8B | code | 0.108 | 2.44e-07 | True | 0.098 | 5.60e-07 | True | 0.088 | 2.59e-05 | True | 3 | True | True |
| InternVL3_5-8B | math | 0.116 | 9.18e-13 | True | 0.118 | 4.94e-13 | True | 0.120 | 2.66e-13 | True | 3 | True | True |
| InternVL3_5-8B | table | 0.050 | 0.106 | False | 0.056 | 0.059 | False | 0.042 | 0.329 | False | 0 | True | True |
| Qwen2.5-VL-72B-Instruct-AWQ | code | 0.040 | 0.133 | False | 0.066 | 8.98e-04 | True | 0.070 | 3.11e-04 | True | 2 | False | True |
| Qwen2.5-VL-72B-Instruct-AWQ | math | 0.010 | 0.680 | False | 0.008 | 1.000 | False | 0.008 | 1.000 | False | 0 | True | True |
| Qwen2.5-VL-72B-Instruct-AWQ | table | 0.004 | 0.905 | False | 0.012 | 1.000 | False | 0.018 | 1.000 | False | 0 | True | True |
| Qwen3-VL-8B-Instruct | code | 0.122 | 1.64e-09 | True | 0.098 | 2.26e-06 | True | 0.100 | 3.11e-06 | True | 3 | True | True |
| Qwen3-VL-8B-Instruct | math | 0.010 | 0.767 | False | 0.006 | 1.000 | False | 0.006 | 1.000 | False | 0 | True | True |
| Qwen3-VL-8B-Instruct | table | 0.050 | 0.047 | True | 0.048 | 0.059 | False | 0.050 | 0.041 | True | 2 | False | True |
| gemma-3-27b-it | code | 0.146 | 7.00e-12 | True | 0.134 | 6.72e-10 | True | 0.152 | 4.16e-13 | True | 3 | True | True |
| gemma-3-27b-it | math | 0.026 | 0.074 | False | 0.022 | 0.173 | False | 0.018 | 0.610 | False | 0 | True | True |
| gemma-3-27b-it | table | 0.036 | 0.380 | False | 0.028 | 0.809 | False | 0.030 | 0.703 | False | 0 | True | True |

- cells significant in all runs: 4; in some but not all: 2; in none: 6 (of 12)

## RQ1 A vs B on majority vote (correct in >= 2 of 3 runs), extension models (exploratory)

| model_id | content_type | n_pairs | acc_first | acc_second | b_first_only | c_second_only | diff | diff_ci_lo | diff_ci_hi | p_mcnemar_exact | p_holm |
|---|---|---|---|---|---|---|---|---|---|---|---|
| InternVL3_5-8B | code | 500 | 0.730 | 0.624 | 69 | 16 | 0.106 | 0.071 | 0.141 | 5.24e-09 | 5.15e-08 |
| InternVL3_5-8B | math | 500 | 0.958 | 0.836 | 65 | 4 | 0.122 | 0.092 | 0.155 | 3.11e-15 | 3.74e-14 |
| InternVL3_5-8B | table | 500 | 0.766 | 0.720 | 62 | 39 | 0.046 | 0.007 | 0.085 | 0.028 | 0.140 |
| Qwen2.5-VL-72B-Instruct-AWQ | code | 500 | 0.812 | 0.746 | 51 | 18 | 0.066 | 0.034 | 0.099 | 8.77e-05 | 7.01e-04 |
| Qwen2.5-VL-72B-Instruct-AWQ | math | 500 | 0.966 | 0.958 | 8 | 4 | 0.008 | -0.007 | 0.024 | 0.388 | 1.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | table | 500 | 0.814 | 0.806 | 35 | 31 | 0.008 | -0.024 | 0.040 | 0.712 | 1.000 |
| Qwen3-VL-8B-Instruct | code | 500 | 0.794 | 0.686 | 71 | 17 | 0.108 | 0.072 | 0.144 | 5.15e-09 | 5.15e-08 |
| Qwen3-VL-8B-Instruct | math | 500 | 0.948 | 0.940 | 12 | 8 | 0.008 | -0.011 | 0.027 | 0.503 | 1.000 |
| Qwen3-VL-8B-Instruct | table | 500 | 0.826 | 0.772 | 51 | 24 | 0.054 | 0.020 | 0.088 | 0.002 | 0.017 |
| gemma-3-27b-it | code | 500 | 0.758 | 0.608 | 91 | 16 | 0.150 | 0.111 | 0.188 | 6.45e-14 | 7.09e-13 |
| gemma-3-27b-it | math | 500 | 0.972 | 0.948 | 17 | 5 | 0.024 | 0.005 | 0.045 | 0.017 | 0.101 |
| gemma-3-27b-it | table | 500 | 0.768 | 0.738 | 60 | 45 | 0.030 | -0.010 | 0.070 | 0.172 | 0.686 |

## RQ1 A vs C per run (Holm within each run), extension models (exploratory)

| model_id | content_type | diff_run1 | p_holm_run1 | sig_holm_run1 | diff_run2 | p_holm_run2 | sig_holm_run2 | diff_run3 | p_holm_run3 | sig_holm_run3 | n_runs_sig | sig_agree_all_runs | direction_agree_all_runs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| InternVL3_5-8B | code | 0.092 | 7.34e-06 | True | 0.070 | 4.27e-04 | True | 0.066 | 0.008 | True | 3 | True | True |
| InternVL3_5-8B | math | 0.012 | 1.000 | False | 0.010 | 1.000 | False | 0.014 | 0.946 | False | 0 | True | True |
| InternVL3_5-8B | table | 0.020 | 1.000 | False | 0.042 | 0.322 | False | 0.032 | 0.932 | False | 0 | True | True |
| Qwen2.5-VL-72B-Instruct-AWQ | code | 0.044 | 0.083 | False | 0.050 | 0.032 | True | 0.056 | 0.012 | True | 2 | False | True |
| Qwen2.5-VL-72B-Instruct-AWQ | math | 0.006 | 1.000 | False | 0.002 | 1.000 | False | 0.008 | 1.000 | False | 0 | True | True |
| Qwen2.5-VL-72B-Instruct-AWQ | table | -0.004 | 1.000 | False | -0.002 | 1.000 | False | 0.016 | 1.000 | False | 0 | True | False |
| Qwen3-VL-8B-Instruct | code | 0.106 | 1.00e-07 | True | 0.102 | 8.69e-07 | True | 0.088 | 2.58e-05 | True | 3 | True | True |
| Qwen3-VL-8B-Instruct | math | -0.002 | 1.000 | False | -0.008 | 1.000 | False | -0.010 | 1.000 | False | 0 | True | True |
| Qwen3-VL-8B-Instruct | table | 0.030 | 0.638 | False | 0.016 | 1.000 | False | 0.024 | 0.932 | False | 0 | True | True |
| gemma-3-27b-it | code | 0.074 | 0.002 | True | 0.070 | 0.003 | True | 0.082 | 2.78e-04 | True | 3 | True | True |
| gemma-3-27b-it | math | 0.024 | 0.068 | False | 0.022 | 0.154 | False | 0.024 | 0.135 | False | 0 | True | True |
| gemma-3-27b-it | table | 0.032 | 0.752 | False | 0.010 | 1.000 | False | 0.008 | 1.000 | False | 0 | True | True |

- cells significant in all runs: 3; in some but not all: 1; in none: 8 (of 12)

## RQ1 A vs C on majority vote (correct in >= 2 of 3 runs), extension models (exploratory)

| model_id | content_type | n_pairs | acc_first | acc_second | b_first_only | c_second_only | diff | diff_ci_lo | diff_ci_hi | p_mcnemar_exact | p_holm |
|---|---|---|---|---|---|---|---|---|---|---|---|
| InternVL3_5-8B | code | 500 | 0.730 | 0.652 | 60 | 21 | 0.078 | 0.043 | 0.113 | 1.69e-05 | 1.86e-04 |
| InternVL3_5-8B | math | 500 | 0.958 | 0.942 | 15 | 7 | 0.016 | -0.003 | 0.037 | 0.134 | 0.909 |
| InternVL3_5-8B | table | 500 | 0.766 | 0.736 | 56 | 41 | 0.030 | -0.009 | 0.069 | 0.155 | 0.909 |
| Qwen2.5-VL-72B-Instruct-AWQ | code | 500 | 0.812 | 0.762 | 46 | 21 | 0.050 | 0.018 | 0.082 | 0.003 | 0.025 |
| Qwen2.5-VL-72B-Instruct-AWQ | math | 500 | 0.966 | 0.962 | 6 | 4 | 0.004 | -0.010 | 0.019 | 0.754 | 1.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | table | 500 | 0.814 | 0.816 | 28 | 29 | -0.002 | -0.032 | 0.028 | 1.000 | 1.000 |
| Qwen3-VL-8B-Instruct | code | 500 | 0.794 | 0.702 | 63 | 17 | 0.092 | 0.058 | 0.127 | 2.27e-07 | 2.72e-06 |
| Qwen3-VL-8B-Instruct | math | 500 | 0.948 | 0.958 | 6 | 11 | -0.010 | -0.028 | 0.007 | 0.332 | 1.000 |
| Qwen3-VL-8B-Instruct | table | 500 | 0.826 | 0.800 | 38 | 25 | 0.026 | -0.005 | 0.058 | 0.130 | 0.909 |
| gemma-3-27b-it | code | 500 | 0.758 | 0.678 | 65 | 25 | 0.080 | 0.043 | 0.117 | 2.97e-05 | 2.97e-04 |
| gemma-3-27b-it | math | 500 | 0.972 | 0.944 | 17 | 3 | 0.028 | 0.010 | 0.048 | 0.003 | 0.023 |
| gemma-3-27b-it | table | 500 | 0.768 | 0.750 | 52 | 43 | 0.018 | -0.020 | 0.056 | 0.412 | 1.000 |

## RQ1 A vs B paired permutation test on per-item mean correctness (10,000 perms, seed 630), extension models (exploratory)

| model_id | content_type | comparison | n_items | mean_acc_first | mean_acc_second | mean_diff | n_perm | seed | p_perm | p_holm |
|---|---|---|---|---|---|---|---|---|---|---|
| InternVL3_5-8B | code | A_text vs B_image | 500 | 0.728 | 0.630 | 0.098 | 10000 | 630 | 1.00e-04 | 0.001 |
| InternVL3_5-8B | math | A_text vs B_image | 500 | 0.955 | 0.837 | 0.118 | 10000 | 630 | 1.00e-04 | 0.001 |
| InternVL3_5-8B | table | A_text vs B_image | 500 | 0.767 | 0.717 | 0.049 | 10000 | 630 | 0.013 | 0.076 |
| Qwen2.5-VL-72B-Instruct-AWQ | code | A_text vs B_image | 500 | 0.810 | 0.751 | 0.059 | 10000 | 630 | 1.00e-04 | 0.001 |
| Qwen2.5-VL-72B-Instruct-AWQ | math | A_text vs B_image | 500 | 0.966 | 0.957 | 0.009 | 10000 | 630 | 0.216 | 0.649 |
| Qwen2.5-VL-72B-Instruct-AWQ | table | A_text vs B_image | 500 | 0.817 | 0.805 | 0.011 | 10000 | 630 | 0.492 | 0.885 |
| Qwen3-VL-8B-Instruct | code | A_text vs B_image | 500 | 0.796 | 0.689 | 0.107 | 10000 | 630 | 1.00e-04 | 0.001 |
| Qwen3-VL-8B-Instruct | math | A_text vs B_image | 500 | 0.949 | 0.941 | 0.007 | 10000 | 630 | 0.442 | 0.885 |
| Qwen3-VL-8B-Instruct | table | A_text vs B_image | 500 | 0.824 | 0.775 | 0.049 | 10000 | 630 | 0.002 | 0.012 |
| gemma-3-27b-it | code | A_text vs B_image | 500 | 0.756 | 0.612 | 0.144 | 10000 | 630 | 1.00e-04 | 0.001 |
| gemma-3-27b-it | math | A_text vs B_image | 500 | 0.969 | 0.947 | 0.022 | 10000 | 630 | 0.024 | 0.119 |
| gemma-3-27b-it | table | A_text vs B_image | 500 | 0.769 | 0.738 | 0.031 | 10000 | 630 | 0.123 | 0.491 |

## RQ2 A−C gap, wrong vs correct transcription, per run, extension models (exploratory)

| model_id | content_type | subset_rule | run | gap_A_minus_C_wrong | gap_A_minus_C_correct | n_pairs_wrong | n_pairs_correct | gap_wrong_minus_correct | pattern_wrong_gt_correct |
|---|---|---|---|---|---|---|---|---|---|
| InternVL3_5-8B | code | cer_le_0.02 | 1 | 0.093 | 0.000 | 497 | 3.000 | 0.093 | True |
| InternVL3_5-8B | code | cer_le_0.02 | 2 | 0.073 | -0.250 | 496 | 4.000 | 0.323 | True |
| InternVL3_5-8B | code | cer_le_0.02 | 3 | 0.069 | -0.250 | 496 | 4.000 | 0.319 | True |
| InternVL3_5-8B | code | exact | 1 | 0.093 | 0.000 | 497 | 3.000 | 0.093 | True |
| InternVL3_5-8B | code | exact | 2 | 0.070 | 0.000 | 497 | 3.000 | 0.070 | True |
| InternVL3_5-8B | code | exact | 3 | 0.066 | 0.000 | 497 | 3.000 | 0.066 | True |
| InternVL3_5-8B | math | cer_le_0.02 | 1 | 0.011 | 0.040 | 475 | 25.000 | -0.029 | False |
| InternVL3_5-8B | math | cer_le_0.02 | 2 | 0.008 | 0.045 | 478 | 22.000 | -0.037 | False |
| InternVL3_5-8B | math | cer_le_0.02 | 3 | 0.013 | 0.045 | 478 | 22.000 | -0.033 | False |
| InternVL3_5-8B | math | exact | 1 | 0.011 | 0.042 | 476 | 24.000 | -0.031 | False |
| InternVL3_5-8B | math | exact | 2 | 0.008 | 0.045 | 478 | 22.000 | -0.037 | False |
| InternVL3_5-8B | math | exact | 3 | 0.013 | 0.048 | 479 | 21.000 | -0.035 | False |
| InternVL3_5-8B | table | cer_le_0.02 | 1 | 0.025 | -0.105 | 481 | 19.000 | 0.130 | True |
| InternVL3_5-8B | table | cer_le_0.02 | 2 | 0.044 | 0.000 | 477 | 23.000 | 0.044 | True |
| InternVL3_5-8B | table | cer_le_0.02 | 3 | 0.036 | -0.040 | 475 | 25.000 | 0.076 | True |
| InternVL3_5-8B | table | exact | 1 | 0.020 |  | 500 |  |  | False |
| InternVL3_5-8B | table | exact | 2 | 0.042 |  | 500 |  |  | False |
| InternVL3_5-8B | table | exact | 3 | 0.032 |  | 500 |  |  | False |
| Qwen2.5-VL-72B-Instruct-AWQ | code | cer_le_0.02 | 1 | 0.200 | 0.042 | 5 | 495.000 | 0.158 | True |
| Qwen2.5-VL-72B-Instruct-AWQ | code | cer_le_0.02 | 2 | 0.200 | 0.048 | 5 | 495.000 | 0.152 | True |
| Qwen2.5-VL-72B-Instruct-AWQ | code | cer_le_0.02 | 3 | 0.400 | 0.053 | 5 | 495.000 | 0.347 | True |
| Qwen2.5-VL-72B-Instruct-AWQ | code | exact | 1 | 0.292 | 0.018 | 48 | 452.000 | 0.274 | True |
| Qwen2.5-VL-72B-Instruct-AWQ | code | exact | 2 | 0.286 | 0.024 | 49 | 451.000 | 0.261 | True |
| Qwen2.5-VL-72B-Instruct-AWQ | code | exact | 3 | 0.306 | 0.029 | 49 | 451.000 | 0.277 | True |
| Qwen2.5-VL-72B-Instruct-AWQ | math | cer_le_0.02 | 1 | 0.000 | 0.006 | 4 | 496.000 | -0.006 | False |
| Qwen2.5-VL-72B-Instruct-AWQ | math | cer_le_0.02 | 2 | 0.000 | 0.002 | 3 | 497.000 | -0.002 | False |
| Qwen2.5-VL-72B-Instruct-AWQ | math | cer_le_0.02 | 3 | 0.000 | 0.008 | 4 | 496.000 | -0.008 | False |
| Qwen2.5-VL-72B-Instruct-AWQ | math | exact | 1 | 0.000 | 0.006 | 7 | 493.000 | -0.006 | False |
| Qwen2.5-VL-72B-Instruct-AWQ | math | exact | 2 | 0.000 | 0.002 | 6 | 494.000 | -0.002 | False |
| Qwen2.5-VL-72B-Instruct-AWQ | math | exact | 3 | 0.000 | 0.008 | 7 | 493.000 | -0.008 | False |
| Qwen2.5-VL-72B-Instruct-AWQ | table | cer_le_0.02 | 1 | 0.003 | -0.015 | 296 | 204.000 | 0.018 | True |
| Qwen2.5-VL-72B-Instruct-AWQ | table | cer_le_0.02 | 2 | 0.007 | -0.015 | 296 | 204.000 | 0.021 | True |
| Qwen2.5-VL-72B-Instruct-AWQ | table | cer_le_0.02 | 3 | 0.017 | 0.015 | 297 | 203.000 | 0.002 | True |
| Qwen2.5-VL-72B-Instruct-AWQ | table | exact | 1 | -0.004 | 0.000 | 498 | 2.000 | -0.004 | False |
| Qwen2.5-VL-72B-Instruct-AWQ | table | exact | 2 | -0.002 | 0.000 | 498 | 2.000 | -0.002 | False |
| Qwen2.5-VL-72B-Instruct-AWQ | table | exact | 3 | 0.016 | 0.000 | 499 | 1.000 | 0.016 | True |
| Qwen3-VL-8B-Instruct | code | cer_le_0.02 | 1 | 0.286 | 0.095 | 28 | 472.000 | 0.190 | True |
| Qwen3-VL-8B-Instruct | code | cer_le_0.02 | 2 | 0.222 | 0.095 | 27 | 473.000 | 0.127 | True |
| Qwen3-VL-8B-Instruct | code | cer_le_0.02 | 3 | 0.321 | 0.074 | 28 | 472.000 | 0.247 | True |
| Qwen3-VL-8B-Instruct | code | exact | 1 | 0.345 | 0.036 | 113 | 387.000 | 0.309 | True |
| Qwen3-VL-8B-Instruct | code | exact | 2 | 0.286 | 0.049 | 112 | 388.000 | 0.237 | True |
| Qwen3-VL-8B-Instruct | code | exact | 3 | 0.312 | 0.023 | 112 | 388.000 | 0.289 | True |
| Qwen3-VL-8B-Instruct | math | cer_le_0.02 | 1 | 0.031 | -0.004 | 32 | 468.000 | 0.036 | True |
| Qwen3-VL-8B-Instruct | math | cer_le_0.02 | 2 | 0.000 | -0.009 | 33 | 467.000 | 0.009 | True |
| Qwen3-VL-8B-Instruct | math | cer_le_0.02 | 3 | 0.000 | -0.011 | 36 | 464.000 | 0.011 | True |
| Qwen3-VL-8B-Instruct | math | exact | 1 | 0.021 | -0.004 | 48 | 452.000 | 0.025 | True |
| Qwen3-VL-8B-Instruct | math | exact | 2 | 0.000 | -0.009 | 51 | 449.000 | 0.009 | True |
| Qwen3-VL-8B-Instruct | math | exact | 3 | 0.000 | -0.011 | 53 | 447.000 | 0.011 | True |
| Qwen3-VL-8B-Instruct | table | cer_le_0.02 | 1 | 0.034 | 0.011 | 409 | 91.000 | 0.023 | True |
| Qwen3-VL-8B-Instruct | table | cer_le_0.02 | 2 | 0.017 | 0.011 | 411 | 89.000 | 0.006 | True |
| Qwen3-VL-8B-Instruct | table | cer_le_0.02 | 3 | 0.025 | 0.021 | 406 | 94.000 | 0.003 | True |
| Qwen3-VL-8B-Instruct | table | exact | 1 | 0.030 |  | 500 |  |  | False |
| Qwen3-VL-8B-Instruct | table | exact | 2 | 0.016 |  | 500 |  |  | False |
| Qwen3-VL-8B-Instruct | table | exact | 3 | 0.024 |  | 500 |  |  | False |
| gemma-3-27b-it | code | cer_le_0.02 | 1 | 0.289 | 0.053 | 45 | 455.000 | 0.236 | True |
| gemma-3-27b-it | code | cer_le_0.02 | 2 | 0.279 | 0.050 | 43 | 457.000 | 0.229 | True |
| gemma-3-27b-it | code | cer_le_0.02 | 3 | 0.289 | 0.062 | 45 | 455.000 | 0.227 | True |
| gemma-3-27b-it | code | exact | 1 | 0.233 | -0.012 | 176 | 324.000 | 0.245 | True |
| gemma-3-27b-it | code | exact | 2 | 0.220 | -0.009 | 173 | 327.000 | 0.229 | True |
| gemma-3-27b-it | code | exact | 3 | 0.230 | 0.003 | 174 | 326.000 | 0.227 | True |
| gemma-3-27b-it | math | cer_le_0.02 | 1 | 0.333 | 0.022 | 3 | 497.000 | 0.311 | True |
| gemma-3-27b-it | math | cer_le_0.02 | 2 | 0.333 | 0.020 | 3 | 497.000 | 0.313 | True |
| gemma-3-27b-it | math | cer_le_0.02 | 3 | 0.333 | 0.022 | 3 | 497.000 | 0.311 | True |
| gemma-3-27b-it | math | exact | 1 | 0.110 | 0.007 | 82 | 418.000 | 0.103 | True |
| gemma-3-27b-it | math | exact | 2 | 0.131 | 0.000 | 84 | 416.000 | 0.131 | True |
| gemma-3-27b-it | math | exact | 3 | 0.126 | 0.002 | 87 | 413.000 | 0.124 | True |
| gemma-3-27b-it | table | cer_le_0.02 | 1 | 0.043 | -0.049 | 439 | 61.000 | 0.092 | True |
| gemma-3-27b-it | table | cer_le_0.02 | 2 | 0.018 | -0.052 | 442 | 58.000 | 0.070 | True |
| gemma-3-27b-it | table | cer_le_0.02 | 3 | 0.018 | -0.066 | 439 | 61.000 | 0.084 | True |
| gemma-3-27b-it | table | exact | 1 | 0.032 |  | 500 |  |  | False |
| gemma-3-27b-it | table | exact | 2 | 0.010 |  | 500 |  |  | False |
| gemma-3-27b-it | table | exact | 3 | 0.008 |  | 500 |  |  | False |

## T18 extension run 1: accuracy (95% Wilson CI)

| model_id | content_type | condition | n | accuracy | ci95_lo | ci95_hi | parse_rate | parse_rate_strict | pct_finish_length |
|---|---|---|---|---|---|---|---|---|---|
| InternVL3_5-8B | code | A_text | 500 | 0.734 | 0.694 | 0.771 | 0.998 | 0.998 | 0.200 |
| InternVL3_5-8B | code | B_image | 500 | 0.626 | 0.583 | 0.667 | 1.000 | 1.000 | 0.000 |
| InternVL3_5-8B | code | C_image_transcribe | 500 | 0.642 | 0.599 | 0.683 | 0.994 | 0.994 | 0.600 |
| InternVL3_5-8B | math | A_text | 500 | 0.954 | 0.932 | 0.969 | 1.000 | 1.000 | 0.000 |
| InternVL3_5-8B | math | B_image | 500 | 0.838 | 0.803 | 0.868 | 0.888 | 0.888 | 0.200 |
| InternVL3_5-8B | math | C_image_transcribe | 500 | 0.942 | 0.918 | 0.959 | 0.996 | 0.996 | 0.400 |
| InternVL3_5-8B | table | A_text | 500 | 0.766 | 0.727 | 0.801 | 0.998 | 0.998 | 0.200 |
| InternVL3_5-8B | table | B_image | 500 | 0.716 | 0.675 | 0.754 | 0.998 | 0.998 | 0.000 |
| InternVL3_5-8B | table | C_image_transcribe | 500 | 0.746 | 0.706 | 0.782 | 0.998 | 0.998 | 0.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | code | A_text | 500 | 0.798 | 0.761 | 0.831 | 0.998 | 0.992 | 0.200 |
| Qwen2.5-VL-72B-Instruct-AWQ | code | B_image | 500 | 0.758 | 0.719 | 0.793 | 0.998 | 0.998 | 0.200 |
| Qwen2.5-VL-72B-Instruct-AWQ | code | C_image_transcribe | 500 | 0.754 | 0.714 | 0.790 | 1.000 | 1.000 | 0.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | math | A_text | 500 | 0.966 | 0.946 | 0.979 | 1.000 | 0.986 | 0.200 |
| Qwen2.5-VL-72B-Instruct-AWQ | math | B_image | 500 | 0.956 | 0.934 | 0.971 | 0.998 | 0.998 | 0.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | math | C_image_transcribe | 500 | 0.960 | 0.939 | 0.974 | 1.000 | 1.000 | 0.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | table | A_text | 500 | 0.812 | 0.775 | 0.844 | 1.000 | 1.000 | 0.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | table | B_image | 500 | 0.808 | 0.771 | 0.840 | 0.998 | 0.998 | 0.200 |
| Qwen2.5-VL-72B-Instruct-AWQ | table | C_image_transcribe | 500 | 0.816 | 0.780 | 0.848 | 0.994 | 0.994 | 0.600 |
| Qwen3-VL-8B-Instruct | code | A_text | 500 | 0.808 | 0.771 | 0.840 | 0.914 | 0.914 | 9.000 |
| Qwen3-VL-8B-Instruct | code | B_image | 500 | 0.686 | 0.644 | 0.725 | 0.922 | 0.922 | 7.800 |
| Qwen3-VL-8B-Instruct | code | C_image_transcribe | 500 | 0.702 | 0.660 | 0.740 | 0.938 | 0.938 | 6.200 |
| Qwen3-VL-8B-Instruct | math | A_text | 500 | 0.952 | 0.930 | 0.968 | 0.990 | 0.986 | 1.200 |
| Qwen3-VL-8B-Instruct | math | B_image | 500 | 0.942 | 0.918 | 0.959 | 0.992 | 0.990 | 1.200 |
| Qwen3-VL-8B-Instruct | math | C_image_transcribe | 500 | 0.954 | 0.932 | 0.969 | 0.990 | 0.990 | 1.000 |
| Qwen3-VL-8B-Instruct | table | A_text | 500 | 0.828 | 0.792 | 0.859 | 0.972 | 0.972 | 2.800 |
| Qwen3-VL-8B-Instruct | table | B_image | 500 | 0.778 | 0.740 | 0.812 | 0.988 | 0.988 | 1.200 |
| Qwen3-VL-8B-Instruct | table | C_image_transcribe | 500 | 0.798 | 0.761 | 0.831 | 0.982 | 0.982 | 1.800 |
| gemma-3-27b-it | code | A_text | 500 | 0.758 | 0.719 | 0.793 | 1.000 | 1.000 | 0.000 |
| gemma-3-27b-it | code | B_image | 500 | 0.612 | 0.569 | 0.654 | 0.996 | 0.996 | 0.400 |
| gemma-3-27b-it | code | C_image_transcribe | 500 | 0.684 | 0.642 | 0.723 | 1.000 | 1.000 | 0.000 |
| gemma-3-27b-it | math | A_text | 500 | 0.972 | 0.954 | 0.983 | 1.000 | 1.000 | 0.000 |
| gemma-3-27b-it | math | B_image | 500 | 0.946 | 0.923 | 0.963 | 1.000 | 1.000 | 0.000 |
| gemma-3-27b-it | math | C_image_transcribe | 500 | 0.948 | 0.925 | 0.964 | 1.000 | 1.000 | 0.000 |
| gemma-3-27b-it | table | A_text | 500 | 0.778 | 0.740 | 0.812 | 1.000 | 1.000 | 0.000 |
| gemma-3-27b-it | table | B_image | 500 | 0.742 | 0.702 | 0.778 | 1.000 | 1.000 | 0.000 |
| gemma-3-27b-it | table | C_image_transcribe | 500 | 0.746 | 0.706 | 0.782 | 0.990 | 0.990 | 1.000 |

## T18 extension RQ1 McNemar A vs B (exploratory; Holm within the extension family)

| model_id | content_type | n_pairs | acc_first | acc_second | b_first_only | c_second_only | diff | diff_ci_lo | diff_ci_hi | p_mcnemar_exact | p_holm |
|---|---|---|---|---|---|---|---|---|---|---|---|
| InternVL3_5-8B | code | 500 | 0.734 | 0.626 | 75 | 21 | 0.108 | 0.070 | 0.145 | 2.71e-08 | 2.44e-07 |
| InternVL3_5-8B | math | 500 | 0.954 | 0.838 | 63 | 5 | 0.116 | 0.086 | 0.149 | 7.65e-14 | 9.18e-13 |
| InternVL3_5-8B | table | 500 | 0.766 | 0.716 | 64 | 39 | 0.050 | 0.010 | 0.090 | 0.018 | 0.106 |
| Qwen2.5-VL-72B-Instruct-AWQ | code | 500 | 0.798 | 0.758 | 47 | 27 | 0.040 | 0.006 | 0.074 | 0.027 | 0.133 |
| Qwen2.5-VL-72B-Instruct-AWQ | math | 500 | 0.966 | 0.956 | 8 | 3 | 0.010 | -0.004 | 0.026 | 0.227 | 0.680 |
| Qwen2.5-VL-72B-Instruct-AWQ | table | 500 | 0.812 | 0.808 | 36 | 34 | 0.004 | -0.029 | 0.037 | 0.905 | 0.905 |
| Qwen3-VL-8B-Instruct | code | 500 | 0.808 | 0.686 | 78 | 17 | 0.122 | 0.085 | 0.159 | 1.64e-10 | 1.64e-09 |
| Qwen3-VL-8B-Instruct | math | 500 | 0.952 | 0.942 | 13 | 8 | 0.010 | -0.009 | 0.030 | 0.383 | 0.767 |
| Qwen3-VL-8B-Instruct | table | 500 | 0.828 | 0.778 | 51 | 26 | 0.050 | 0.016 | 0.085 | 0.006 | 0.047 |
| gemma-3-27b-it | code | 500 | 0.758 | 0.612 | 91 | 18 | 0.146 | 0.107 | 0.185 | 6.37e-13 | 7.00e-12 |
| gemma-3-27b-it | math | 500 | 0.972 | 0.946 | 18 | 5 | 0.026 | 0.007 | 0.047 | 0.011 | 0.074 |
| gemma-3-27b-it | table | 500 | 0.778 | 0.742 | 61 | 43 | 0.036 | -0.004 | 0.076 | 0.095 | 0.380 |

## T18 extension RQ1 McNemar A vs C (exploratory; Holm within the extension family)

| model_id | content_type | n_pairs | acc_first | acc_second | b_first_only | c_second_only | diff | diff_ci_lo | diff_ci_hi | p_mcnemar_exact | p_holm |
|---|---|---|---|---|---|---|---|---|---|---|---|
| InternVL3_5-8B | code | 500 | 0.734 | 0.642 | 66 | 20 | 0.092 | 0.056 | 0.128 | 6.67e-07 | 7.34e-06 |
| InternVL3_5-8B | math | 500 | 0.954 | 0.942 | 15 | 9 | 0.012 | -0.008 | 0.033 | 0.307 | 1.000 |
| InternVL3_5-8B | table | 500 | 0.766 | 0.746 | 53 | 43 | 0.020 | -0.019 | 0.059 | 0.358 | 1.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | code | 500 | 0.798 | 0.754 | 45 | 23 | 0.044 | 0.012 | 0.077 | 0.010 | 0.083 |
| Qwen2.5-VL-72B-Instruct-AWQ | math | 500 | 0.966 | 0.960 | 5 | 2 | 0.006 | -0.006 | 0.020 | 0.453 | 1.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | table | 500 | 0.812 | 0.816 | 30 | 32 | -0.004 | -0.035 | 0.027 | 0.899 | 1.000 |
| Qwen3-VL-8B-Instruct | code | 500 | 0.808 | 0.702 | 70 | 17 | 0.106 | 0.070 | 0.142 | 8.35e-09 | 1.00e-07 |
| Qwen3-VL-8B-Instruct | math | 500 | 0.952 | 0.954 | 8 | 9 | -0.002 | -0.020 | 0.016 | 1.000 | 1.000 |
| Qwen3-VL-8B-Instruct | table | 500 | 0.828 | 0.798 | 42 | 27 | 0.030 | -0.003 | 0.063 | 0.091 | 0.638 |
| gemma-3-27b-it | code | 500 | 0.758 | 0.684 | 65 | 28 | 0.074 | 0.036 | 0.111 | 1.58e-04 | 0.002 |
| gemma-3-27b-it | math | 500 | 0.972 | 0.948 | 15 | 3 | 0.024 | 0.007 | 0.044 | 0.008 | 0.068 |
| gemma-3-27b-it | table | 500 | 0.778 | 0.746 | 56 | 40 | 0.032 | -0.007 | 0.071 | 0.125 | 0.752 |

## T18 extension RQ1 McNemar B vs C (exploratory; Holm within the extension family)

| model_id | content_type | n_pairs | acc_first | acc_second | b_first_only | c_second_only | diff | diff_ci_lo | diff_ci_hi | p_mcnemar_exact | p_holm |
|---|---|---|---|---|---|---|---|---|---|---|---|
| InternVL3_5-8B | code | 500 | 0.626 | 0.642 | 32 | 40 | -0.016 | -0.049 | 0.017 | 0.410 | 1.000 |
| InternVL3_5-8B | math | 500 | 0.838 | 0.942 | 8 | 60 | -0.104 | -0.137 | -0.073 | 5.75e-11 | 6.90e-10 |
| InternVL3_5-8B | table | 500 | 0.716 | 0.746 | 34 | 49 | -0.030 | -0.066 | 0.006 | 0.124 | 1.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | code | 500 | 0.758 | 0.754 | 30 | 28 | 0.004 | -0.026 | 0.034 | 0.896 | 1.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | math | 500 | 0.956 | 0.960 | 2 | 4 | -0.004 | -0.017 | 0.008 | 0.688 | 1.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | table | 500 | 0.808 | 0.816 | 19 | 23 | -0.008 | -0.034 | 0.018 | 0.644 | 1.000 |
| Qwen3-VL-8B-Instruct | code | 500 | 0.686 | 0.702 | 28 | 36 | -0.016 | -0.048 | 0.016 | 0.382 | 1.000 |
| Qwen3-VL-8B-Instruct | math | 500 | 0.942 | 0.954 | 4 | 10 | -0.012 | -0.029 | 0.004 | 0.180 | 1.000 |
| Qwen3-VL-8B-Instruct | table | 500 | 0.778 | 0.798 | 26 | 36 | -0.020 | -0.051 | 0.011 | 0.253 | 1.000 |
| gemma-3-27b-it | code | 500 | 0.612 | 0.684 | 16 | 52 | -0.072 | -0.104 | -0.040 | 1.41e-05 | 1.55e-04 |
| gemma-3-27b-it | math | 500 | 0.946 | 0.948 | 5 | 6 | -0.002 | -0.017 | 0.013 | 1.000 | 1.000 |
| gemma-3-27b-it | table | 500 | 0.742 | 0.746 | 30 | 32 | -0.004 | -0.035 | 0.027 | 0.899 | 1.000 |

## T18 extension RQ2 transcription (condition C)

| model_id | content_type | n | pct_with_transcription | pct_src_tags | pct_src_open_tag | pct_src_heading_fence | pct_src_none | exact_rate | exact_lenient_rate | pct_cer_le_002 | cer_mean | cer_sd | cer_p10 | cer_q1 | cer_median | cer_q3 | cer_p90 | cer_max |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| InternVL3_5-8B | code | 500 | 0.600 | 0.600 | 0.000 | 0 | 99.400 | 0.006 | 0.006 | 0.600 | 0.994 | 0.077 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| InternVL3_5-8B | math | 500 | 5.600 | 5.600 | 0.000 | 0 | 94.400 | 0.048 | 0.048 | 5.000 | 0.948 | 0.221 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| InternVL3_5-8B | table | 500 | 18.800 | 18.800 | 0.000 | 0 | 81.200 | 0.000 | 0.096 | 3.800 | 0.821 | 0.372 | 0.042 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | code | 500 | 100.000 | 100.000 | 0.000 | 0 | 0.000 | 0.904 | 0.904 | 99.000 | 0.001 | 0.004 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.039 |
| Qwen2.5-VL-72B-Instruct-AWQ | math | 500 | 100.000 | 100.000 | 0.000 | 0 | 0.000 | 0.986 | 0.986 | 99.200 | 5.00e-04 | 0.006 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.101 |
| Qwen2.5-VL-72B-Instruct-AWQ | table | 500 | 100.000 | 99.400 | 0.600 | 0 | 0.000 | 0.004 | 0.482 | 40.800 | 0.118 | 0.843 | 0.007 | 0.013 | 0.026 | 0.071 | 0.124 | 10.967 |
| Qwen3-VL-8B-Instruct | code | 500 | 100.000 | 100.000 | 0.000 | 0 | 0.000 | 0.774 | 0.774 | 94.400 | 0.006 | 0.022 | 0.000 | 0.000 | 0.000 | 0.000 | 0.014 | 0.248 |
| Qwen3-VL-8B-Instruct | math | 500 | 94.200 | 94.200 | 0.000 | 0 | 5.800 | 0.904 | 0.904 | 93.600 | 0.060 | 0.238 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 |
| Qwen3-VL-8B-Instruct | table | 500 | 100.000 | 100.000 | 0.000 | 0 | 0.000 | 0.000 | 0.454 | 18.200 | 0.065 | 0.102 | 0.014 | 0.023 | 0.035 | 0.062 | 0.107 | 0.722 |
| gemma-3-27b-it | code | 500 | 100.000 | 100.000 | 0.000 | 0 | 0.000 | 0.648 | 0.648 | 91.000 | 0.007 | 0.015 | 0.000 | 0.000 | 0.000 | 0.009 | 0.019 | 0.190 |
| gemma-3-27b-it | math | 500 | 100.000 | 100.000 | 0.000 | 0 | 0.000 | 0.836 | 0.836 | 99.400 | 0.001 | 0.003 | 0.000 | 0.000 | 0.000 | 0.000 | 0.004 | 0.034 |
| gemma-3-27b-it | table | 500 | 100.000 | 99.000 | 1.000 | 0 | 0.000 | 0.000 | 0.328 | 12.200 | 0.305 | 2.537 | 0.017 | 0.029 | 0.048 | 0.083 | 0.131 | 38.853 |

## T18 extension RQ2 A vs C split by transcription correctness

| model_id | content_type | subset_rule | transcription_correct | comparison | n_pairs | both_correct | b_first_only | c_second_only | both_wrong | acc_first | acc_second | diff | diff_ci_lo | diff_ci_hi | discordant_or | or_ci_lo | or_ci_hi | p_mcnemar_exact | p_holm | gap_A_minus_C | p_holm_within_rule |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| InternVL3_5-8B | code | exact | True | A_text vs C_image_transcribe | 3 | 3 | 0 | 0 | 0 | 1.000 | 1.000 | 0.000 | -0.561 | 0.561 |  |  |  | 1.000 | 1.000 | 0.000 | 1.000 |
| InternVL3_5-8B | math | exact | True | A_text vs C_image_transcribe | 24 | 23 | 1 | 0 | 0 | 1.000 | 0.958 | 0.042 | -0.101 | 0.202 | inf | 0.026 | inf | 1.000 | 1.000 | 0.042 | 1.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | code | exact | True | A_text vs C_image_transcribe | 452 | 344 | 28 | 20 | 60 | 0.823 | 0.805 | 0.018 | -0.013 | 0.048 | 1.400 | 0.761 | 2.622 | 0.312 | 1.000 | 0.018 | 1.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | math | exact | True | A_text vs C_image_transcribe | 493 | 473 | 5 | 2 | 13 | 0.970 | 0.963 | 0.006 | -0.007 | 0.020 | 2.500 | 0.409 | 26.253 | 0.453 | 1.000 | 0.006 | 1.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | table | exact | True | A_text vs C_image_transcribe | 2 | 2 | 0 | 0 | 0 | 1.000 | 1.000 | 0.000 | -0.658 | 0.658 |  |  |  | 1.000 | 1.000 | 0.000 | 1.000 |
| Qwen3-VL-8B-Instruct | code | exact | True | A_text vs C_image_transcribe | 387 | 296 | 29 | 15 | 47 | 0.840 | 0.804 | 0.036 | 0.002 | 0.071 | 1.933 | 1.003 | 3.880 | 0.049 | 0.439 | 0.036 | 0.780 |
| Qwen3-VL-8B-Instruct | math | exact | True | A_text vs C_image_transcribe | 452 | 424 | 6 | 8 | 14 | 0.951 | 0.956 | -0.004 | -0.023 | 0.014 | 0.750 | 0.214 | 2.465 | 0.791 | 1.000 | -0.004 | 1.000 |
| gemma-3-27b-it | code | exact | True | A_text vs C_image_transcribe | 324 | 246 | 16 | 20 | 42 | 0.809 | 0.821 | -0.012 | -0.050 | 0.025 | 0.800 | 0.388 | 1.625 | 0.618 | 1.000 | -0.012 | 1.000 |
| gemma-3-27b-it | math | exact | True | A_text vs C_image_transcribe | 418 | 398 | 6 | 3 | 11 | 0.967 | 0.959 | 0.007 | -0.009 | 0.025 | 2.000 | 0.427 | 12.359 | 0.508 | 1.000 | 0.007 | 1.000 |
| InternVL3_5-8B | code | exact | False | A_text vs C_image_transcribe | 497 | 298 | 66 | 20 | 113 | 0.732 | 0.640 | 0.093 | 0.057 | 0.128 | 3.300 | 1.976 | 5.747 | 6.67e-07 | 6.67e-06 | 0.093 | 1.27e-05 |
| InternVL3_5-8B | math | exact | False | A_text vs C_image_transcribe | 476 | 439 | 14 | 9 | 14 | 0.952 | 0.941 | 0.011 | -0.010 | 0.032 | 1.556 | 0.627 | 4.074 | 0.405 | 1.000 | 0.011 | 1.000 |
| InternVL3_5-8B | table | exact | False | A_text vs C_image_transcribe | 500 | 330 | 53 | 43 | 74 | 0.766 | 0.746 | 0.020 | -0.019 | 0.059 | 1.233 | 0.809 | 1.888 | 0.358 | 1.000 | 0.020 | 1.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | code | exact | False | A_text vs C_image_transcribe | 48 | 10 | 17 | 3 | 18 | 0.562 | 0.271 | 0.292 | 0.116 | 0.441 | 5.667 | 1.639 | 30.181 | 0.003 | 0.023 | 0.292 | 0.046 |
| Qwen2.5-VL-72B-Instruct-AWQ | math | exact | False | A_text vs C_image_transcribe | 7 | 5 | 0 | 0 | 2 | 0.714 | 0.714 | 0.000 | -0.271 | 0.271 |  |  |  | 1.000 | 1.000 | 0.000 | 1.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | table | exact | False | A_text vs C_image_transcribe | 498 | 374 | 30 | 32 | 62 | 0.811 | 0.815 | -0.004 | -0.036 | 0.027 | 0.938 | 0.550 | 1.593 | 0.899 | 1.000 | -0.004 | 1.000 |
| Qwen3-VL-8B-Instruct | code | exact | False | A_text vs C_image_transcribe | 113 | 38 | 41 | 2 | 32 | 0.699 | 0.354 | 0.345 | 0.244 | 0.433 | 20.500 | 5.325 | 174.955 | 2.15e-10 | 2.58e-09 | 0.345 | 4.52e-09 |
| Qwen3-VL-8B-Instruct | math | exact | False | A_text vs C_image_transcribe | 48 | 44 | 2 | 1 | 1 | 0.958 | 0.938 | 0.021 | -0.079 | 0.126 | 2.000 | 0.104 | 117.994 | 1.000 | 1.000 | 0.021 | 1.000 |
| Qwen3-VL-8B-Instruct | table | exact | False | A_text vs C_image_transcribe | 500 | 372 | 42 | 27 | 59 | 0.828 | 0.798 | 0.030 | -0.003 | 0.063 | 1.556 | 0.937 | 2.624 | 0.091 | 0.638 | 0.030 | 1.000 |
| gemma-3-27b-it | code | exact | False | A_text vs C_image_transcribe | 176 | 68 | 49 | 8 | 51 | 0.665 | 0.432 | 0.233 | 0.154 | 0.307 | 6.125 | 2.877 | 14.976 | 2.72e-08 | 2.99e-07 | 0.233 | 5.43e-07 |
| gemma-3-27b-it | math | exact | False | A_text vs C_image_transcribe | 82 | 73 | 9 | 0 | 0 | 1.000 | 0.890 | 0.110 | 0.042 | 0.196 | inf | 1.974 | inf | 0.004 | 0.031 | 0.110 | 0.066 |
| gemma-3-27b-it | table | exact | False | A_text vs C_image_transcribe | 500 | 333 | 56 | 40 | 71 | 0.778 | 0.746 | 0.032 | -0.007 | 0.071 | 1.400 | 0.917 | 2.156 | 0.125 | 0.752 | 0.032 | 1.000 |
| InternVL3_5-8B | code | cer_le_0.02 | True | A_text vs C_image_transcribe | 3 | 3 | 0 | 0 | 0 | 1.000 | 1.000 | 0.000 | -0.561 | 0.561 |  |  |  | 1.000 | 1.000 | 0.000 | 1.000 |
| InternVL3_5-8B | math | cer_le_0.02 | True | A_text vs C_image_transcribe | 25 | 24 | 1 | 0 | 0 | 1.000 | 0.960 | 0.040 | -0.097 | 0.195 | inf | 0.026 | inf | 1.000 | 1.000 | 0.040 | 1.000 |
| InternVL3_5-8B | table | cer_le_0.02 | True | A_text vs C_image_transcribe | 19 | 14 | 1 | 3 | 1 | 0.789 | 0.895 | -0.105 | -0.338 | 0.135 | 0.333 | 0.006 | 4.151 | 0.625 | 1.000 | -0.105 | 1.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | code | cer_le_0.02 | True | A_text vs C_image_transcribe | 495 | 353 | 44 | 23 | 75 | 0.802 | 0.760 | 0.042 | 0.010 | 0.075 | 1.913 | 1.130 | 3.319 | 0.014 | 0.127 | 0.042 | 0.265 |
| Qwen2.5-VL-72B-Instruct-AWQ | math | cer_le_0.02 | True | A_text vs C_image_transcribe | 496 | 476 | 5 | 2 | 13 | 0.970 | 0.964 | 0.006 | -0.007 | 0.020 | 2.500 | 0.409 | 26.253 | 0.453 | 1.000 | 0.006 | 1.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | table | cer_le_0.02 | True | A_text vs C_image_transcribe | 204 | 152 | 12 | 15 | 25 | 0.804 | 0.819 | -0.015 | -0.066 | 0.037 | 0.800 | 0.342 | 1.831 | 0.701 | 1.000 | -0.015 | 1.000 |
| Qwen3-VL-8B-Instruct | code | cer_le_0.02 | True | A_text vs C_image_transcribe | 472 | 325 | 60 | 15 | 72 | 0.816 | 0.720 | 0.095 | 0.060 | 0.131 | 4.000 | 2.243 | 7.585 | 1.59e-07 | 1.91e-06 | 0.095 | 3.81e-06 |
| Qwen3-VL-8B-Instruct | math | cer_le_0.02 | True | A_text vs C_image_transcribe | 468 | 438 | 7 | 9 | 14 | 0.951 | 0.955 | -0.004 | -0.023 | 0.014 | 0.778 | 0.246 | 2.347 | 0.804 | 1.000 | -0.004 | 1.000 |
| Qwen3-VL-8B-Instruct | table | cer_le_0.02 | True | A_text vs C_image_transcribe | 91 | 77 | 4 | 3 | 7 | 0.890 | 0.879 | 0.011 | -0.056 | 0.079 | 1.333 | 0.226 | 9.102 | 1.000 | 1.000 | 0.011 | 1.000 |
| gemma-3-27b-it | code | cer_le_0.02 | True | A_text vs C_image_transcribe | 455 | 300 | 51 | 27 | 77 | 0.771 | 0.719 | 0.053 | 0.015 | 0.091 | 1.889 | 1.163 | 3.133 | 0.009 | 0.096 | 0.053 | 0.184 |
| gemma-3-27b-it | math | cer_le_0.02 | True | A_text vs C_image_transcribe | 497 | 469 | 14 | 3 | 11 | 0.972 | 0.950 | 0.022 | 0.005 | 0.041 | 4.667 | 1.302 | 25.326 | 0.013 | 0.127 | 0.022 | 0.255 |
| gemma-3-27b-it | table | cer_le_0.02 | True | A_text vs C_image_transcribe | 61 | 41 | 4 | 7 | 9 | 0.738 | 0.787 | -0.049 | -0.161 | 0.063 | 0.571 | 0.123 | 2.248 | 0.549 | 1.000 | -0.049 | 1.000 |
| InternVL3_5-8B | code | cer_le_0.02 | False | A_text vs C_image_transcribe | 497 | 298 | 66 | 20 | 113 | 0.732 | 0.640 | 0.093 | 0.057 | 0.128 | 3.300 | 1.976 | 5.747 | 6.67e-07 | 8.00e-06 | 0.093 | 1.53e-05 |
| InternVL3_5-8B | math | cer_le_0.02 | False | A_text vs C_image_transcribe | 475 | 438 | 14 | 9 | 14 | 0.952 | 0.941 | 0.011 | -0.010 | 0.032 | 1.556 | 0.627 | 4.074 | 0.405 | 1.000 | 0.011 | 1.000 |
| InternVL3_5-8B | table | cer_le_0.02 | False | A_text vs C_image_transcribe | 481 | 316 | 52 | 40 | 73 | 0.765 | 0.740 | 0.025 | -0.014 | 0.064 | 1.300 | 0.844 | 2.015 | 0.251 | 1.000 | 0.025 | 1.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | code | cer_le_0.02 | False | A_text vs C_image_transcribe | 5 | 1 | 1 | 0 | 3 | 0.400 | 0.200 | 0.200 | -0.285 | 0.588 | inf | 0.026 | inf | 1.000 | 1.000 | 0.200 | 1.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | math | cer_le_0.02 | False | A_text vs C_image_transcribe | 4 | 2 | 0 | 0 | 2 | 0.500 | 0.500 | 0.000 | -0.350 | 0.350 |  |  |  | 1.000 | 1.000 | 0.000 | 1.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | table | cer_le_0.02 | False | A_text vs C_image_transcribe | 296 | 224 | 18 | 17 | 37 | 0.818 | 0.814 | 0.003 | -0.037 | 0.044 | 1.059 | 0.515 | 2.186 | 1.000 | 1.000 | 0.003 | 1.000 |
| Qwen3-VL-8B-Instruct | code | cer_le_0.02 | False | A_text vs C_image_transcribe | 28 | 9 | 10 | 2 | 7 | 0.679 | 0.393 | 0.286 | 0.047 | 0.480 | 5.000 | 1.066 | 46.933 | 0.039 | 0.386 | 0.286 | 0.694 |
| Qwen3-VL-8B-Instruct | math | cer_le_0.02 | False | A_text vs C_image_transcribe | 32 | 30 | 1 | 0 | 1 | 0.969 | 0.938 | 0.031 | -0.088 | 0.164 | inf | 0.026 | inf | 1.000 | 1.000 | 0.031 | 1.000 |
| Qwen3-VL-8B-Instruct | table | cer_le_0.02 | False | A_text vs C_image_transcribe | 409 | 295 | 38 | 24 | 52 | 0.814 | 0.780 | 0.034 | -0.004 | 0.072 | 1.583 | 0.925 | 2.759 | 0.098 | 0.784 | 0.034 | 1.000 |
| gemma-3-27b-it | code | cer_le_0.02 | False | A_text vs C_image_transcribe | 45 | 14 | 14 | 1 | 16 | 0.622 | 0.333 | 0.289 | 0.130 | 0.423 | 14.000 | 2.130 | 591.968 | 9.77e-04 | 0.011 | 0.289 | 0.021 |
| gemma-3-27b-it | math | cer_le_0.02 | False | A_text vs C_image_transcribe | 3 | 2 | 1 | 0 | 0 | 1.000 | 0.667 | 0.333 | -0.291 | 0.792 | inf | 0.026 | inf | 1.000 | 1.000 | 0.333 | 1.000 |
| gemma-3-27b-it | table | cer_le_0.02 | False | A_text vs C_image_transcribe | 439 | 292 | 52 | 33 | 62 | 0.784 | 0.740 | 0.043 | 0.002 | 0.085 | 1.576 | 1.000 | 2.516 | 0.050 | 0.452 | 0.043 | 0.854 |
| InternVL3_5-8B | code | exact_lenient | True | A_text vs C_image_transcribe | 3 | 3 | 0 | 0 | 0 | 1.000 | 1.000 | 0.000 | -0.561 | 0.561 |  |  |  | 1.000 | 1.000 | 0.000 | 1.000 |
| InternVL3_5-8B | math | exact_lenient | True | A_text vs C_image_transcribe | 24 | 23 | 1 | 0 | 0 | 1.000 | 0.958 | 0.042 | -0.101 | 0.202 | inf | 0.026 | inf | 1.000 | 1.000 | 0.042 | 1.000 |
| InternVL3_5-8B | table | exact_lenient | True | A_text vs C_image_transcribe | 48 | 39 | 4 | 3 | 2 | 0.896 | 0.875 | 0.021 | -0.103 | 0.146 | 1.333 | 0.226 | 9.102 | 1.000 | 1.000 | 0.021 | 1.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | code | exact_lenient | True | A_text vs C_image_transcribe | 452 | 344 | 28 | 20 | 60 | 0.823 | 0.805 | 0.018 | -0.013 | 0.048 | 1.400 | 0.761 | 2.622 | 0.312 | 1.000 | 0.018 | 1.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | math | exact_lenient | True | A_text vs C_image_transcribe | 493 | 473 | 5 | 2 | 13 | 0.970 | 0.963 | 0.006 | -0.007 | 0.020 | 2.500 | 0.409 | 26.253 | 0.453 | 1.000 | 0.006 | 1.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | table | exact_lenient | True | A_text vs C_image_transcribe | 241 | 189 | 15 | 15 | 22 | 0.846 | 0.846 | 0.000 | -0.046 | 0.046 | 1.000 | 0.456 | 2.195 | 1.000 | 1.000 | 0.000 | 1.000 |
| Qwen3-VL-8B-Instruct | code | exact_lenient | True | A_text vs C_image_transcribe | 387 | 296 | 29 | 15 | 47 | 0.840 | 0.804 | 0.036 | 0.002 | 0.071 | 1.933 | 1.003 | 3.880 | 0.049 | 0.536 | 0.036 | 0.829 |
| Qwen3-VL-8B-Instruct | math | exact_lenient | True | A_text vs C_image_transcribe | 452 | 424 | 6 | 8 | 14 | 0.951 | 0.956 | -0.004 | -0.023 | 0.014 | 0.750 | 0.214 | 2.465 | 0.791 | 1.000 | -0.004 | 1.000 |
| Qwen3-VL-8B-Instruct | table | exact_lenient | True | A_text vs C_image_transcribe | 227 | 178 | 16 | 8 | 25 | 0.855 | 0.819 | 0.035 | -0.008 | 0.080 | 2.000 | 0.808 | 5.398 | 0.152 | 1.000 | 0.035 | 1.000 |
| gemma-3-27b-it | code | exact_lenient | True | A_text vs C_image_transcribe | 324 | 246 | 16 | 20 | 42 | 0.809 | 0.821 | -0.012 | -0.050 | 0.025 | 0.800 | 0.388 | 1.625 | 0.618 | 1.000 | -0.012 | 1.000 |
| gemma-3-27b-it | math | exact_lenient | True | A_text vs C_image_transcribe | 418 | 398 | 6 | 3 | 11 | 0.967 | 0.959 | 0.007 | -0.009 | 0.025 | 2.000 | 0.427 | 12.359 | 0.508 | 1.000 | 0.007 | 1.000 |
| gemma-3-27b-it | table | exact_lenient | True | A_text vs C_image_transcribe | 164 | 127 | 4 | 15 | 18 | 0.799 | 0.866 | -0.067 | -0.122 | -0.014 | 0.267 | 0.064 | 0.837 | 0.019 | 0.231 | -0.067 | 0.346 |
| InternVL3_5-8B | code | exact_lenient | False | A_text vs C_image_transcribe | 497 | 298 | 66 | 20 | 113 | 0.732 | 0.640 | 0.093 | 0.057 | 0.128 | 3.300 | 1.976 | 5.747 | 6.67e-07 | 6.67e-06 | 0.093 | 1.47e-05 |
| InternVL3_5-8B | math | exact_lenient | False | A_text vs C_image_transcribe | 476 | 439 | 14 | 9 | 14 | 0.952 | 0.941 | 0.011 | -0.010 | 0.032 | 1.556 | 0.627 | 4.074 | 0.405 | 1.000 | 0.011 | 1.000 |
| InternVL3_5-8B | table | exact_lenient | False | A_text vs C_image_transcribe | 452 | 291 | 49 | 40 | 72 | 0.752 | 0.732 | 0.020 | -0.021 | 0.061 | 1.225 | 0.790 | 1.909 | 0.397 | 1.000 | 0.020 | 1.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | code | exact_lenient | False | A_text vs C_image_transcribe | 48 | 10 | 17 | 3 | 18 | 0.562 | 0.271 | 0.292 | 0.116 | 0.441 | 5.667 | 1.639 | 30.181 | 0.003 | 0.023 | 0.292 | 0.054 |
| Qwen2.5-VL-72B-Instruct-AWQ | math | exact_lenient | False | A_text vs C_image_transcribe | 7 | 5 | 0 | 0 | 2 | 0.714 | 0.714 | 0.000 | -0.271 | 0.271 |  |  |  | 1.000 | 1.000 | 0.000 | 1.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | table | exact_lenient | False | A_text vs C_image_transcribe | 259 | 187 | 15 | 17 | 40 | 0.780 | 0.788 | -0.008 | -0.052 | 0.036 | 0.882 | 0.410 | 1.878 | 0.860 | 1.000 | -0.008 | 1.000 |
| Qwen3-VL-8B-Instruct | code | exact_lenient | False | A_text vs C_image_transcribe | 113 | 38 | 41 | 2 | 32 | 0.699 | 0.354 | 0.345 | 0.244 | 0.433 | 20.500 | 5.325 | 174.955 | 2.15e-10 | 2.58e-09 | 0.345 | 5.17e-09 |
| Qwen3-VL-8B-Instruct | math | exact_lenient | False | A_text vs C_image_transcribe | 48 | 44 | 2 | 1 | 1 | 0.958 | 0.938 | 0.021 | -0.079 | 0.126 | 2.000 | 0.104 | 117.994 | 1.000 | 1.000 | 0.021 | 1.000 |
| Qwen3-VL-8B-Instruct | table | exact_lenient | False | A_text vs C_image_transcribe | 273 | 194 | 26 | 19 | 34 | 0.806 | 0.780 | 0.026 | -0.023 | 0.075 | 1.368 | 0.729 | 2.616 | 0.371 | 1.000 | 0.026 | 1.000 |
| gemma-3-27b-it | code | exact_lenient | False | A_text vs C_image_transcribe | 176 | 68 | 49 | 8 | 51 | 0.665 | 0.432 | 0.233 | 0.154 | 0.307 | 6.125 | 2.877 | 14.976 | 2.72e-08 | 2.99e-07 | 0.233 | 6.25e-07 |
| gemma-3-27b-it | math | exact_lenient | False | A_text vs C_image_transcribe | 82 | 73 | 9 | 0 | 0 | 1.000 | 0.890 | 0.110 | 0.042 | 0.196 | inf | 1.974 | inf | 0.004 | 0.027 | 0.110 | 0.074 |
| gemma-3-27b-it | table | exact_lenient | False | A_text vs C_image_transcribe | 336 | 206 | 52 | 25 | 53 | 0.768 | 0.688 | 0.080 | 0.029 | 0.131 | 2.080 | 1.268 | 3.498 | 0.003 | 0.023 | 0.080 | 0.056 |
| InternVL3_5-8B | code | exact_tags_only | True | A_text vs C_image_transcribe | 3 | 3 | 0 | 0 | 0 | 1.000 | 1.000 | 0.000 | -0.561 | 0.561 |  |  |  | 1.000 | 1.000 | 0.000 | 1.000 |
| InternVL3_5-8B | math | exact_tags_only | True | A_text vs C_image_transcribe | 24 | 23 | 1 | 0 | 0 | 1.000 | 0.958 | 0.042 | -0.101 | 0.202 | inf | 0.026 | inf | 1.000 | 1.000 | 0.042 | 1.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | code | exact_tags_only | True | A_text vs C_image_transcribe | 452 | 344 | 28 | 20 | 60 | 0.823 | 0.805 | 0.018 | -0.013 | 0.048 | 1.400 | 0.761 | 2.622 | 0.312 | 1.000 | 0.018 | 1.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | math | exact_tags_only | True | A_text vs C_image_transcribe | 493 | 473 | 5 | 2 | 13 | 0.970 | 0.963 | 0.006 | -0.007 | 0.020 | 2.500 | 0.409 | 26.253 | 0.453 | 1.000 | 0.006 | 1.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | table | exact_tags_only | True | A_text vs C_image_transcribe | 2 | 2 | 0 | 0 | 0 | 1.000 | 1.000 | 0.000 | -0.658 | 0.658 |  |  |  | 1.000 | 1.000 | 0.000 | 1.000 |
| Qwen3-VL-8B-Instruct | code | exact_tags_only | True | A_text vs C_image_transcribe | 387 | 296 | 29 | 15 | 47 | 0.840 | 0.804 | 0.036 | 0.002 | 0.071 | 1.933 | 1.003 | 3.880 | 0.049 | 0.439 | 0.036 | 0.780 |
| Qwen3-VL-8B-Instruct | math | exact_tags_only | True | A_text vs C_image_transcribe | 452 | 424 | 6 | 8 | 14 | 0.951 | 0.956 | -0.004 | -0.023 | 0.014 | 0.750 | 0.214 | 2.465 | 0.791 | 1.000 | -0.004 | 1.000 |
| gemma-3-27b-it | code | exact_tags_only | True | A_text vs C_image_transcribe | 324 | 246 | 16 | 20 | 42 | 0.809 | 0.821 | -0.012 | -0.050 | 0.025 | 0.800 | 0.388 | 1.625 | 0.618 | 1.000 | -0.012 | 1.000 |
| gemma-3-27b-it | math | exact_tags_only | True | A_text vs C_image_transcribe | 418 | 398 | 6 | 3 | 11 | 0.967 | 0.959 | 0.007 | -0.009 | 0.025 | 2.000 | 0.427 | 12.359 | 0.508 | 1.000 | 0.007 | 1.000 |
| InternVL3_5-8B | math | exact_tags_only | False | A_text vs C_image_transcribe | 4 | 4 | 0 | 0 | 0 | 1.000 | 1.000 | 0.000 | -0.490 | 0.490 |  |  |  | 1.000 | 1.000 | 0.000 | 1.000 |
| InternVL3_5-8B | table | exact_tags_only | False | A_text vs C_image_transcribe | 94 | 75 | 5 | 6 | 8 | 0.851 | 0.862 | -0.011 | -0.087 | 0.065 | 0.833 | 0.201 | 3.277 | 1.000 | 1.000 | -0.011 | 1.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | code | exact_tags_only | False | A_text vs C_image_transcribe | 48 | 10 | 17 | 3 | 18 | 0.562 | 0.271 | 0.292 | 0.116 | 0.441 | 5.667 | 1.639 | 30.181 | 0.003 | 0.023 | 0.292 | 0.046 |
| Qwen2.5-VL-72B-Instruct-AWQ | math | exact_tags_only | False | A_text vs C_image_transcribe | 7 | 5 | 0 | 0 | 2 | 0.714 | 0.714 | 0.000 | -0.271 | 0.271 |  |  |  | 1.000 | 1.000 | 0.000 | 1.000 |
| Qwen2.5-VL-72B-Instruct-AWQ | table | exact_tags_only | False | A_text vs C_image_transcribe | 495 | 374 | 27 | 32 | 62 | 0.810 | 0.820 | -0.010 | -0.041 | 0.021 | 0.844 | 0.486 | 1.454 | 0.603 | 1.000 | -0.010 | 1.000 |
| Qwen3-VL-8B-Instruct | code | exact_tags_only | False | A_text vs C_image_transcribe | 113 | 38 | 41 | 2 | 32 | 0.699 | 0.354 | 0.345 | 0.244 | 0.433 | 20.500 | 5.325 | 174.955 | 2.15e-10 | 2.37e-09 | 0.345 | 4.31e-09 |
| Qwen3-VL-8B-Instruct | math | exact_tags_only | False | A_text vs C_image_transcribe | 19 | 16 | 1 | 1 | 1 | 0.895 | 0.895 | 0.000 | -0.210 | 0.210 | 1.000 | 0.013 | 78.497 | 1.000 | 1.000 | 0.000 | 1.000 |
| Qwen3-VL-8B-Instruct | table | exact_tags_only | False | A_text vs C_image_transcribe | 500 | 372 | 42 | 27 | 59 | 0.828 | 0.798 | 0.030 | -0.003 | 0.063 | 1.556 | 0.937 | 2.624 | 0.091 | 0.638 | 0.030 | 1.000 |
| gemma-3-27b-it | code | exact_tags_only | False | A_text vs C_image_transcribe | 176 | 68 | 49 | 8 | 51 | 0.665 | 0.432 | 0.233 | 0.154 | 0.307 | 6.125 | 2.877 | 14.976 | 2.72e-08 | 2.72e-07 | 0.233 | 5.16e-07 |
| gemma-3-27b-it | math | exact_tags_only | False | A_text vs C_image_transcribe | 82 | 73 | 9 | 0 | 0 | 1.000 | 0.890 | 0.110 | 0.042 | 0.196 | inf | 1.974 | inf | 0.004 | 0.031 | 0.110 | 0.066 |
| gemma-3-27b-it | table | exact_tags_only | False | A_text vs C_image_transcribe | 495 | 333 | 53 | 40 | 69 | 0.780 | 0.754 | 0.026 | -0.012 | 0.065 | 1.325 | 0.862 | 2.050 | 0.213 | 1.000 | 0.026 | 1.000 |

## T18 extension RQ3 output tokens A vs B (Wilcoxon, Holm)

| model_id | content_type | n_pairs | median_A | median_B | median_diff_A_minus_B | mean_diff_A_minus_B | wilcoxon_W | p_value | p_holm |
|---|---|---|---|---|---|---|---|---|---|
| InternVL3_5-8B | code | 500 | 407.0 | 365.0 | 23.0 | 26.2 | 42598.5 | 2.54e-09 | 1.27e-08 |
| InternVL3_5-8B | math | 500 | 281.5 | 272.0 | 8.0 | 2.5 | 49887.0 | 1.82e-04 | 7.28e-04 |
| InternVL3_5-8B | table | 500 | 181.0 | 147.0 | 22.0 | 42.6 | 30376.5 | 8.67e-22 | 7.80e-21 |
| Qwen2.5-VL-72B-Instruct-AWQ | code | 500 | 395.5 | 349.0 | 41.0 | 50.1 | 29360.0 | 2.02e-24 | 2.02e-23 |
| Qwen2.5-VL-72B-Instruct-AWQ | math | 500 | 257.0 | 234.5 | 11.0 | 24.3 | 33735.5 | 1.40e-16 | 9.82e-16 |
| Qwen2.5-VL-72B-Instruct-AWQ | table | 500 | 182.5 | 187.5 | 0.0 | -28.8 | 57646.0 | 0.2 | 0.2 |
| Qwen3-VL-8B-Instruct | code | 500 | 359.0 | 436.0 | -64.5 | -30.4 | 25518.0 | 8.75e-26 | 9.63e-25 |
| Qwen3-VL-8B-Instruct | math | 500 | 175.0 | 217.0 | -42.0 | -36.4 | 16302.0 | 6.18e-46 | 7.42e-45 |
| Qwen3-VL-8B-Instruct | table | 500 | 228.0 | 270.0 | -46.0 | 13.8 | 34245.5 | 2.45e-17 | 1.96e-16 |
| gemma-3-27b-it | code | 500 | 251.5 | 269.5 | -24.5 | -51.4 | 35637.5 | 1.66e-16 | 9.98e-16 |
| gemma-3-27b-it | math | 500 | 160.0 | 155.0 | 2.0 | 9.9 | 48302.0 | 0.0 | 0.0 |
| gemma-3-27b-it | table | 500 | 94.0 | 97.0 | -6.0 | 0.3 | 50868.0 | 0.0 | 0.0 |

## T18 A−B gap, all models (run 1)

| model_id | group | content_type | acc_first | acc_second | diff | diff_ci_lo | diff_ci_hi | p_holm |
|---|---|---|---|---|---|---|---|---|
| InternVL3-8B | primary | code | 0.632 | 0.506 | 0.126 | 0.085 | 0.166 | 4.13e-08 |
| InternVL3-8B | primary | math | 0.920 | 0.864 | 0.056 | 0.026 | 0.087 | 0.003 |
| InternVL3-8B | primary | table | 0.648 | 0.588 | 0.060 | 0.013 | 0.107 | 0.154 |
| Qwen2.5-VL-32B-Instruct | primary | code | 0.812 | 0.730 | 0.082 | 0.053 | 0.112 | 6.84e-07 |
| Qwen2.5-VL-32B-Instruct | primary | math | 0.918 | 0.902 | 0.016 | -0.013 | 0.046 | 1.000 |
| Qwen2.5-VL-32B-Instruct | primary | table | 0.812 | 0.794 | 0.018 | -0.012 | 0.049 | 1.000 |
| Qwen2.5-VL-3B-Instruct | primary | code | 0.386 | 0.342 | 0.044 | 6.78e-04 | 0.087 | 0.511 |
| Qwen2.5-VL-3B-Instruct | primary | math | 0.840 | 0.818 | 0.022 | -0.010 | 0.054 | 1.000 |
| Qwen2.5-VL-3B-Instruct | primary | table | 0.428 | 0.454 | -0.026 | -0.078 | 0.026 | 1.000 |
| Qwen2.5-VL-7B-Instruct | primary | code | 0.524 | 0.490 | 0.034 | -0.005 | 0.072 | 0.726 |
| Qwen2.5-VL-7B-Instruct | primary | math | 0.868 | 0.868 | 0.000 | -0.026 | 0.026 | 1.000 |
| Qwen2.5-VL-7B-Instruct | primary | table | 0.626 | 0.664 | -0.038 | -0.080 | 0.004 | 0.720 |
| gemma-3-12b-it | primary | code | 0.688 | 0.494 | 0.194 | 0.151 | 0.236 | 1.07e-16 |
| gemma-3-12b-it | primary | math | 0.948 | 0.934 | 0.014 | -0.007 | 0.036 | 1.000 |
| gemma-3-12b-it | primary | table | 0.734 | 0.648 | 0.086 | 0.041 | 0.130 | 0.003 |
| InternVL3_5-8B | extension (exploratory) | code | 0.734 | 0.626 | 0.108 | 0.070 | 0.145 | 2.44e-07 |
| InternVL3_5-8B | extension (exploratory) | math | 0.954 | 0.838 | 0.116 | 0.086 | 0.149 | 9.18e-13 |
| InternVL3_5-8B | extension (exploratory) | table | 0.766 | 0.716 | 0.050 | 0.010 | 0.090 | 0.106 |
| Qwen2.5-VL-72B-Instruct-AWQ | extension (exploratory) | code | 0.798 | 0.758 | 0.040 | 0.006 | 0.074 | 0.133 |
| Qwen2.5-VL-72B-Instruct-AWQ | extension (exploratory) | math | 0.966 | 0.956 | 0.010 | -0.004 | 0.026 | 0.680 |
| Qwen2.5-VL-72B-Instruct-AWQ | extension (exploratory) | table | 0.812 | 0.808 | 0.004 | -0.029 | 0.037 | 0.905 |
| Qwen3-VL-8B-Instruct | extension (exploratory) | code | 0.808 | 0.686 | 0.122 | 0.085 | 0.159 | 1.64e-09 |
| Qwen3-VL-8B-Instruct | extension (exploratory) | math | 0.952 | 0.942 | 0.010 | -0.009 | 0.030 | 0.767 |
| Qwen3-VL-8B-Instruct | extension (exploratory) | table | 0.828 | 0.778 | 0.050 | 0.016 | 0.085 | 0.047 |
| gemma-3-27b-it | extension (exploratory) | code | 0.758 | 0.612 | 0.146 | 0.107 | 0.185 | 7.00e-12 |
| gemma-3-27b-it | extension (exploratory) | math | 0.972 | 0.946 | 0.026 | 0.007 | 0.047 | 0.074 |
| gemma-3-27b-it | extension (exploratory) | table | 0.778 | 0.742 | 0.036 | -0.004 | 0.076 | 0.380 |

## T18 resolution check: A−B code gap by image handling (descriptive; family is a confound)

| model_id | group | family | params_b | image_handling | resizes_image | acc_A | acc_B | gap_A_minus_B_run1 | diff_ci_lo | diff_ci_hi | p_holm_own_family | gap_mean_3runs | n_runs_sig |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Qwen2.5-VL-3B-Instruct | primary | qwen2.5 | 3 | native resolution | False | 0.386 | 0.342 | 0.044 | 6.78e-04 | 0.087 | 0.511 | 0.053 | 0 |
| Qwen2.5-VL-7B-Instruct | primary | qwen2.5 | 7 | native resolution | False | 0.524 | 0.490 | 0.034 | -0.005 | 0.072 | 0.726 | 0.038 | 0 |
| Qwen2.5-VL-32B-Instruct | primary | qwen2.5 | 32 | native resolution | False | 0.812 | 0.730 | 0.082 | 0.053 | 0.112 | 6.84e-07 | 0.083 | 3 |
| Qwen2.5-VL-72B-Instruct-AWQ | extension (exploratory) | qwen2.5 | 72 | native resolution | False | 0.798 | 0.758 | 0.040 | 0.006 | 0.074 | 0.133 | 0.059 | 2 |
| Qwen3-VL-8B-Instruct | extension (exploratory) | qwen3 | 8 | native resolution | False | 0.808 | 0.686 | 0.122 | 0.085 | 0.159 | 1.64e-09 | 0.107 | 3 |
| gemma-3-12b-it | primary | gemma3 | 12 | resized to 896x896 (+pan-and-scan crops) | True | 0.688 | 0.494 | 0.194 | 0.151 | 0.236 | 1.07e-16 | 0.193 | 3 |
| gemma-3-27b-it | extension (exploratory) | gemma3 | 27 | resized to 896x896 (+pan-and-scan crops) | True | 0.758 | 0.612 | 0.146 | 0.107 | 0.185 | 7.00e-12 | 0.144 | 3 |
| InternVL3-8B | primary | internvl | 8 | resized to 448-px tile grid (+thumbnail) | True | 0.632 | 0.506 | 0.126 | 0.085 | 0.166 | 4.13e-08 | 0.122 | 3 |
| InternVL3_5-8B | extension (exploratory) | internvl | 8 | resized to 448-px tile grid (+thumbnail) | True | 0.734 | 0.626 | 0.108 | 0.070 | 0.145 | 2.44e-07 | 0.098 | 3 |

## T18 resolution check summary

| resizes_image | n_models | mean_gap_run1 | min_gap_run1 | max_gap_run1 | note |
|---|---|---|---|---|---|
| False | 5 | 0.064 | 0.034 | 0.122 | descriptive only; family is confounded with image handling |
| True | 4 | 0.143 | 0.108 | 0.194 | descriptive only; family is confounded with image handling |

## T17 extension pilot gate (G2 rule 1: parse >= 80% in every condition)

```
{"model_id": "google/gemma-3-27b-it", "keep": true, "n": 270, "parse": {"A_text": 0.989, "B_image": 0.989, "C_image_transcribe": 0.989}, "pct_length": 1.11}
{"model_id": "Qwen/Qwen3-VL-8B-Instruct", "keep": true, "n": 270, "parse": {"A_text": 0.967, "B_image": 0.944, "C_image_transcribe": 0.956}, "pct_length": 4.44}
{"model_id": "OpenGVLab/InternVL3_5-8B", "keep": true, "n": 270, "parse": {"A_text": 1.0, "B_image": 0.944, "C_image_transcribe": 1.0}, "pct_length": 0.0}
{"model_id": "Qwen/Qwen2.5-VL-72B-Instruct-AWQ", "keep": true, "n": 270, "parse": {"A_text": 1.0, "B_image": 1.0, "C_image_transcribe": 1.0}, "pct_length": 0.0}
```

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
| Phase 4: InternVL3.5-8B condition C, no transcription found (code / math / table) | 99.4% / 94.4% / 81.2% (it writes the copy as a leading code fence without tags or a "Transcription" heading; the frozen extractor finds nothing) -> its RQ2 numbers are not interpretable | ext_rq2_transcription.csv |
| Phase 4: Qwen3-VL-8B finish_reason=length, code A | 9.0% (highest extension cell) | ext_descriptives.csv |
| Phase 4: extension responses with finish_reason=length (run 1) | 183 of 18,000 | ext_outlier_counts.csv |
| Phase 4: extension responses with output tokens > Q3 + 3·IQR (run 1) | 456 of 18,000 | ext_outlier_counts.csv |
| Phase 4: Qwen2.5-VL-32B wall time per run | 54 min vs 35 min in run 1 (gpu_memory_utilization 0.80, GPUs shared with another user's jobs) | logs/lanes.log |


## T19 GLMM note (2026-11-16)

- Model: correct ~ condition * content_type + condition * model + (1 | item_id), binomial logit; reference levels A_text, math, Qwen2.5-VL-7B; run 1, 5 primary models, 22,500 responses, 1,500 items. Exact ML (Gauss-Hermite quadrature); R/lme4 and pymer4 are not installed (deviation #25).
- All 4 fits converged with no warnings (results/analysis/glmm_t19_fit_info.csv). Primary: log-lik -9060.67, AIC 18165.3, BIC 18341.8; item variance 5.001 [4.479, 5.584] (results/analysis/glmm_t19_random_effects.csv).
- LRTs, primary (results/analysis/glmm_t19_lrt.csv): all condition terms χ²(14) = 184.1; condition:content_type χ²(4) = 37.6; condition:model χ²(8) = 63.8; all p < .001.
- B−A odds ratio per content type, models averaged (results/analysis/glmm_t19_emm_contrasts.csv): math 0.643 [0.510, 0.813], code 0.468 [0.400, 0.548], table 0.846 [0.726, 0.985]; Holm p .0004 / < .0001 / .031.
- Per model × content type, p_holm < .05: B−A 8/15, C−A 7/15 (primary); majority vote 9 / 8; + (1 | item_id:model) 11 / 8; extension 11/12 / 4/12.
- Full tables: reports/paper_numbers.md (section "T19 GLMM"); model summaries: results/analysis/glmm_model_summary.txt.
