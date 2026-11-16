# Code identity across runs

Question: was the code that affects model outputs identical across the runs whose `*.meta.json` record different `git_commit` values?

## 1. Every distinct commit in `results/raw/**/*.meta.json`

The commit is HEAD when the run started. `-dirty` = uncommitted changes in the working tree at that moment (`src/vmod/meta.py`). Every commit is in the repo history.

| commit | commit date (UTC) | commit message | runs / models |
|---|---|---|---|
| `e26abedfdd90-dirty` | 2026-11-14T15:42:14+00:00 | T05: prompts, parser, scorers, self-test 100%; G1 report | pilot_smoke/OpenGVLab__InternVL3-8B, pilot_smoke/Qwen__Qwen2.5-VL-32B-Instruct, pilot_smoke/Qwen__Qwen2.5-VL-3B-Instruct, pilot_smoke/Qwen__Qwen2.5-VL-7B-Instruct, pilot_smoke/google__gemma-3-12b-it |
| `d4d3bbaebbb3` | 2026-11-14T16:48:03+00:00 | T06: inference runner, scorer CLI, parser next-line rule; smoke test on 5 models | pilot/OpenGVLab__InternVL3-8B, pilot/Qwen__Qwen2.5-VL-32B-Instruct, pilot/Qwen__Qwen2.5-VL-3B-Instruct, pilot/Qwen__Qwen2.5-VL-7B-Instruct, pilot/google__gemma-3-12b-it, pilot_rep2/OpenGVLab__InternVL3-8B, pilot_rep2/Qwen__Qwen2.5-VL-32B-Instruct, pilot_rep2/Qwen__Qwen2.5-VL-3B-Instruct, pilot_rep2/Qwen__Qwen2.5-VL-7B-Instruct, pilot_rep2/google__gemma-3-12b-it |
| `88ac8821b371-dirty` | 2026-11-14T17:03:36+00:00 | T07b: replication check; G2: rules applied, max_new_tokens 4096, N=500, config frozen | main/Qwen__Qwen2.5-VL-3B-Instruct, main/Qwen__Qwen2.5-VL-7B-Instruct |
| `5c8cdfa5ed5f` | 2026-11-14T17:12:43+00:00 | T08: main run Qwen2.5-VL-3B-Instruct | main/google__gemma-3-12b-it |
| `b5a3f87bef77` | 2026-11-14T17:17:52+00:00 | T08: main run Qwen2.5-VL-7B-Instruct | main/OpenGVLab__InternVL3-8B |
| `d448e0964838` | 2026-11-14T17:41:46+00:00 | T08: main run InternVL3-8B | main/Qwen__Qwen2.5-VL-32B-Instruct |
| `d9732a0a91b1` | 2026-11-15T09:44:02+00:00 | T15: started; runner Phase 4 options | main_run2/Qwen__Qwen2.5-VL-3B-Instruct, main_run2/Qwen__Qwen2.5-VL-7B-Instruct |
| `01c54e1f838d` | 2026-11-15T09:54:49+00:00 | T15: Qwen2.5-VL-3B-Instruct main_run2 | main_run3/Qwen__Qwen2.5-VL-3B-Instruct |
| `b16057b8c5f9` | 2026-11-15T10:01:50+00:00 | T15: Qwen2.5-VL-7B-Instruct main_run2 | main_run3/Qwen__Qwen2.5-VL-7B-Instruct |
| `87fa5c08ba7a` | 2026-11-15T10:05:33+00:00 | Phase 4 deviations #16-#20 | main_run2/OpenGVLab__InternVL3-8B |
| `651bfe2f637d` | 2026-11-15T10:19:22+00:00 | T15: Qwen2.5-VL-7B-Instruct main_run3 | main_run2/google__gemma-3-12b-it |
| `51c45d0b262f` | 2026-11-15T10:39:20+00:00 | T15: InternVL3-8B main_run2 | main_run3/OpenGVLab__InternVL3-8B |
| `6786c380210b` | 2026-11-15T10:52:13+00:00 | T15: gemma-3-12b-it main_run2 | main_run3/google__gemma-3-12b-it |
| `65e77da66607` | 2026-11-15T11:25:14+00:00 | T16: interim replication note | main_run2/Qwen__Qwen2.5-VL-32B-Instruct |
| `d76dd08f17d0` | 2026-11-15T12:19:00+00:00 | T15: Qwen2.5-VL-32B-Instruct main_run2 | main_run3/Qwen__Qwen2.5-VL-32B-Instruct |
| `8b1a87757287` | 2026-11-15T13:13:24+00:00 | T15: Qwen2.5-VL-32B-Instruct main_run3 | ext/pilot/google__gemma-3-27b-it |
| `b8c20a5c01c8` | 2026-11-15T13:19:26+00:00 | T17: gemma-3-27b-it ext/pilot | ext/run1/google__gemma-3-27b-it |
| `f87605cbdc24` | 2026-11-15T13:55:13+00:00 | T17: gemma-3-27b-it ext/run1 | ext/run2/google__gemma-3-27b-it |
| `fad4b42ec325` | 2026-11-15T14:31:56+00:00 | T17: gemma-3-27b-it ext/run2 | ext/run3/google__gemma-3-27b-it |
| `1d377dff837c` | 2026-11-15T15:07:43+00:00 | T17: gemma-3-27b-it ext/run3 | ext/pilot/OpenGVLab__InternVL3_5-8B, ext/pilot/Qwen__Qwen3-VL-8B-Instruct |
| `ba1320bdf294` | 2026-11-15T15:11:11+00:00 | T17: InternVL3_5-8B ext/pilot | ext/run1/OpenGVLab__InternVL3_5-8B, ext/run1/Qwen__Qwen3-VL-8B-Instruct |
| `9cd271c14c1a` | 2026-11-15T15:34:41+00:00 | T17: Qwen3-VL-8B-Instruct ext/run1 | ext/run2/Qwen__Qwen3-VL-8B-Instruct |
| `a1ea97716366` | 2026-11-15T15:49:38+00:00 | T17: InternVL3_5-8B ext/run1 | ext/run2/OpenGVLab__InternVL3_5-8B |
| `ac10d2884718` | 2026-11-15T15:58:30+00:00 | T17: Qwen3-VL-8B-Instruct ext/run2 | ext/run3/Qwen__Qwen3-VL-8B-Instruct |
| `82cdd362b8d6` | 2026-11-15T16:28:18+00:00 | T17: InternVL3_5-8B ext/run2 | ext/run3/OpenGVLab__InternVL3_5-8B |
| `b783fc7ab71d` | 2026-11-15T17:06:50+00:00 | T17: InternVL3_5-8B ext/run3 | ext/pilot/Qwen__Qwen2.5-VL-72B-Instruct-AWQ |
| `cf37829eb7af` | 2026-11-15T17:11:40+00:00 | T17: Qwen2.5-VL-72B-Instruct-AWQ ext/pilot | ext/run1/Qwen__Qwen2.5-VL-72B-Instruct-AWQ |
| `b226b576604a` | 2026-11-15T17:59:15+00:00 | T17: Qwen2.5-VL-72B-Instruct-AWQ ext/run1 | ext/run2/Qwen__Qwen2.5-VL-72B-Instruct-AWQ |
| `ddc64fe30619` | 2026-11-15T18:45:29+00:00 | T17: Qwen2.5-VL-72B-Instruct-AWQ ext/run2 | ext/run3/Qwen__Qwen2.5-VL-72B-Instruct-AWQ |
| `6bd2e201ad4e-dirty` | 2026-11-16T15:33:27+00:00 | Sensitivity: leading code fence = transcription (InternVL3.5, gemma-12b); approved by OWNER | res896/Qwen__Qwen2.5-VL-7B-Instruct, res_gemma_nopas/google__gemma-3-12b-it |
| `ad181967f2bd-dirty` | 2026-11-16T16:58:07+00:00 | RESCTL: gemma-3-12b-it res_gemma_nopas | res896/Qwen__Qwen2.5-VL-32B-Instruct |

## 2. Files that affect outputs

- prompt construction: `src/vmod/prompts.py`, `prompts/templates.md`
- item content / rendering / image preprocessing: `src/vmod/prepare.py`, `src/vmod/content.py`, `src/vmod/render.py`, and the per-model processor settings (`MODEL_SETTINGS`) in `src/vmod/run.py`
- vLLM call and decoding: `src/vmod/run.py`, `config/experiment.yaml` (decoding, seed), `config/extension.yaml` (extension models)
- parser and scorers: `src/vmod/scoring.py`, `src/vmod/score.py`, `src/vmod/wtq_eval.py`; shared constants `src/vmod/config.py`

## 3. Diffs between consecutive commits (commit-date order)

Command per pair: `git diff --stat <a> <b> -- src/vmod/prompts.py prompts/templates.md src/vmod/render.py src/vmod/run.py config/experiment.yaml config/extension.yaml src/vmod/scoring.py src/vmod/score.py src/vmod/wtq_eval.py src/vmod/content.py src/vmod/prepare.py src/vmod/config.py`. Pairs with no change to these files are omitted.

### `e26abed..d4d3bba`

```
src/vmod/run.py     | 145 ++++++++++++++++++++++++++++++++++++++++++++++++++++
 src/vmod/score.py   |  87 +++++++++++++++++++++++++++++++
 src/vmod/scoring.py |  64 +++++++++++++++++++----
 3 files changed, 286 insertions(+), 10 deletions(-)
```

### `d4d3bba..88ac882`

```
config/experiment.yaml |  2 +-
 src/vmod/score.py      | 10 ++++++----
 src/vmod/scoring.py    | 28 +++++++++++++++++++++++-----
 3 files changed, 30 insertions(+), 10 deletions(-)
```

### `b5a3f87..d448e09`

```
src/vmod/score.py   |  9 ++++++---
 src/vmod/scoring.py | 18 +++++++++++++++++-
 2 files changed, 23 insertions(+), 4 deletions(-)
```

### `d448e09..d9732a0`

```
config/extension.yaml | 20 ++++++++++++++++++++
 src/vmod/run.py       | 35 ++++++++++++++++++++++++++++-------
 2 files changed, 48 insertions(+), 7 deletions(-)
```

### `d9732a0..01c54e1`

```
src/vmod/run.py | 4 ++++
 1 file changed, 4 insertions(+)
```

### `6bd2e20..ad18196`

```
src/vmod/run.py | 23 +++++++++++++++++++----
 1 file changed, 19 insertions(+), 4 deletions(-)
```

## 4. What changed (summary)

| diff | runs on each side | change | affects model outputs? |
|---|---|---|---|
| `e26abed..d4d3bba` | pilot_smoke → pilot | runner created (`run.py` new), scorer CLI, parser next-line rule | pilot_smoke is a smoke test only; not used in any analysis |
| `d4d3bba..88ac882` | pilot / pilot_rep2 → main run 1 | `config/experiment.yaml`: `max_new_tokens` 2048 → 4096 (G2 rule 3, deviation logged); parser/scorer edits | **yes, pilot vs main**: pilot used 2,048 max tokens. All main, replication, extension and resolution runs used 4,096 (all 30 meta sidecars: `{"max_new_tokens": 4096, "n": 1, "temperature": 0, "top_p": 1.0}`) |
| `b5a3f87..d448e09` | inside main run 1 (between InternVL3 and Qwen-32B starts) | scorer only (`7113e67`: strip whole-transcription code fences; lenient exact metric) | no effect on inference. Every scored file was produced after `7113e67`, the last commit that touched the scorer (`git log -- src/vmod/scoring.py src/vmod/score.py`). Scored-file provenance: main_all `ad6f51c`, main_run{2,3}_all `cf37829`, ext/run*_all `c91952f`, res*_all `505fe94-dirty` |
| `d448e09..d9732a0` | main run 1 → Phase 4 (replication, extension) | `run.py`: `--out-dir`, `--run`, revision pinned to the run-1 sidecar, `gpu_memory_utilization` 0.90 hard-coded → `--gpu-mem` (Phase 4 used 0.80), `run` field in rows, `find_model` for extension models; `config/extension.yaml` added | prompts, images, decoding, model revisions, processor settings for the 5 primary models: unchanged. **gpu_memory_utilization 0.90 → 0.80** (deviation #16) changes KV-cache size, hence vLLM batch composition, so greedy outputs are not bit-identical across runs (see note) |
| `d9732a0..01c54e1` | replication runs | `run.py`: `qwen3` entry in `MODEL_SETTINGS` (Qwen3-VL only) | none for the primary models |
| `6bd2e20..ad18196` | resolution control | `run.py`: `--conditions`, `--image-variant 896`, `--mm-override` (committed in `58cd9fd`; the `6bd2e20-dirty` sidecars are these uncommitted edits) | only when those flags are passed (resolution-control runs only, deviations #21-22) |

No change to prompt templates (`prompts/templates.md`, `src/vmod/prompts.py`), rendering (`src/vmod/render.py`), item building (`src/vmod/prepare.py`, `src/vmod/content.py`) or WTQ evaluator after `e26abed` (`git log` of those files: last commits `e26abed`, `fe44000`, `bc63171`, all before the pilot).

**`-dirty` sidecars:**
- main/Qwen2.5-VL-3B and -7B (`88ac882-dirty`): `git diff --stat 88ac882 5c8cdfa` on the output files is empty. The next commit (`af6cb16`) touched only `analyze.py`, `integrity.py`, `summary.py`, `post_model.sh`, `.gitignore` and `deviations.md`, none of which affect outputs.
- res896 and res_gemma_nopas (`6bd2e20-dirty`, `ad18196-dirty`): the resolution-control flags, later committed in `58cd9fd`.
- The working-tree contents of a dirty run cannot be recovered exactly from git.

**Empirical check:** over all 30 non-pilot raw files (main, main_run2, main_run3, ext/run1-3, res896, res_gemma_nopas):
- every (item_id, condition) has exactly one distinct `prompt_sha256` (4,500 keys);
- every image condition has exactly one distinct `image_sha256`, excluding res896, which hashes the resized pixels by design.

So the prompts and images sent to the models were byte-identical across runs.

**Note on non-identical outputs:** at temperature 0, 35.8-62.1% of responses are textually identical between runs (`results/analysis/replication_full_agreement.csv`). Order seeds (630/631/632) and gpu_memory_utilization differ, which changes batching; that is the expected source.

VERDICT: changed (see above)
