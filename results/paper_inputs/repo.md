# Repository

## Remote

```
$ git remote -v
origin	git@github.com:Ahsan06080/vlm-modality-study.git (fetch)
origin	git@github.com:Ahsan06080/vlm-modality-study.git (push)
```

- **Public URL:** https://github.com/Ahsan06080/vlm-modality-study. `gh repo view --json visibility,url` returns `"visibility":"PUBLIC"`.

## Commits and tags

- **Results HEAD before this collection:** `6e1d795ba1efdcbdf989c2c9a1c0853967598836` (2026-11-16T18:24:04Z, "T12 GLMM (GLMM OK): …"). It is pushed to `origin/main`.
- **`git describe --tags --always`:** `config-frozen-v1-58-g6e1d795`. The only tag is **`config-frozen-v1`** (the design freeze before run 1). No release or paper tag exists.
- **This collection** (`results/paper_inputs/`, the input-length outputs, `scripts/analysis/input_length.py`, `results/coding/codebook_draft.md`) is added by the next commit, "Collect paper inputs". Its hash is printed when the commit is made; a file cannot contain the hash of the commit that adds it.

## Which commit `reports/paper_numbers.md` should cite: **`6e1d795`**

Analysis outputs record the HEAD at generation time. `-dirty` means there were uncommitted changes then. For each such state:

| files stamped | uncommitted changes at that time | committed in | effect on numbers |
|---|---|---|---|
| `reports/paper_numbers.md` (`ddde07f…-dirty`); `glmm_*.csv` | `src/vmod/glmm.py` (new), `src/vmod/paper_numbers.py`, `reports/deviations.md`, `TASKS.md`, `COLLAB.md` | **`6e1d795`** (`git diff --stat ddde07f 6e1d795`) | none. These are the code and text that produced the files; nothing changed after |
| `res_B_vs_B.csv`, `res_gap_A_minus_B_by_setting.csv`, `replication_full_{rq1,summary,agreement}.csv`, `ext_rq1_A_vs_B_family6.csv`, `results/scored/res*_all.csv.gz` (`505fe94…-dirty`) | `src/vmod/paper_numbers.py`, `reports/deviations.md`, `reports/paper_numbers.md`, `COLLAB.md`. The generating code (`src/vmod/plan_tables.py`) was already committed in `58cd9fd` | **`9609db7`** (`git diff --stat 505fe94 9609db7`) | none. `plan_tables.py`, `analyze.py` and `replication.py` are identical in `9609db7` and `6e1d795` |
| `results/figures/gap_vs_size_all.*` | n/a. `ddde07f` itself only re-commits this figure (same size, regenerated) | `ddde07f` | none |
| 19 run-1 analysis CSVs (`7cbe190…-dirty`) | 5 lines in `src/vmod/analyze.py` | `bab2074` (`git diff --stat 7cbe190 bab2074 -- src/vmod/analyze.py`) | none |

So every uncommitted change behind a `-dirty` stamp was committed by `6e1d795`, and `6e1d795` contains all the code and outputs that `reports/paper_numbers.md` indexes. **Cite `6e1d795`.**

For the input-length analysis and `results/paper_inputs/`, cite the "Collect paper inputs" commit. The input-length CSVs are stamped `6e1d795`, because the script was not yet committed when it ran; it is added in that commit unchanged.
