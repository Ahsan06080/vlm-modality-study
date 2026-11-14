# Numeric summary

<!--
study_id: vlm-modality-v1
git_commit: 7cbe190369258f64a3cc325ae523fbfb299ab47a-dirty
created_utc: 2026-11-14T18:18:48Z
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

- total GPU hours: 2.81

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

