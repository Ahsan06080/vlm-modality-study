# Error-coding preparation (no rows were coded)

**The sheet:** `results/coding/error_sample.csv`, exported at T14 (commit `bab2074`, 2026-11-14).
- **Spec** (`TASKS.md:189`): "100 random flips per content type where A was correct and B wrong, across models, with seed 630 … empty `code` and `coder` columns. **The OWNER does the coding.**"
- **Code:** `src/vmod/analyze.py`, `error_sample()`. The sample is drawn with `DataFrame.sample(n=100, random_state=630)` per content type.

## Rows

| content type | rows | with a condition-C transcription (`transcription_C` non-empty) |
|---|---|---|
| code | 100 | 78 |
| math | 100 | 96 |
| table | 100 | 95 |
| **total** | **300** | 269 |

Rows per model:

| model | code | math | table |
|---|---|---|---|
| InternVL3-8B | 22 | 29 | 22 |
| Qwen2.5-VL-32B-Instruct | 14 | 20 | 10 |
| Qwen2.5-VL-3B-Instruct | 15 | 29 | 26 |
| Qwen2.5-VL-7B-Instruct | 20 | 12 | 16 |
| gemma-3-12b-it | 29 | 10 | 26 |

- **Columns:** `sample_id, content_type, model_id, item_id, content, gold, response_A, response_B, transcription_C, code, coder`.
- **Status:** `code` and `coder` are empty in all 300 rows (checked now: 0 non-empty values). Nothing was filled in, by hand or by a model.

## Labels and codebook

- **Allowed labels:** none defined anywhere in the repo. Searched `TASKS.md`, `COLLAB.md`, `README.md`, `config/`, `reports/` and `results/coding/` (`grep -i codebook|label|perception`; `find -iname '*codebook*'`). T14 specifies only "manual coding".
- **Codebook file:** none existed, so a draft was written at **`results/coding/codebook_draft.md`**.
  - Labels: perception / reasoning / format/parse / other.
  - It has one decision rule per label and one illustrative example each. The examples are constructed, not taken from the sheet.
  - It still needs OWNER review.
