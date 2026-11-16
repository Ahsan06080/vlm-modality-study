# Exclusions, pools and sampling

Sources: `data/MANIFEST.md` (datasets), `config/experiment.yaml` (`exclusions`, `items`, `seed`), `src/vmod/prepare.py` (`exclusion_reasons`, `main`), `data/items/summary.json` and `data/exclusions.csv` (T03 output).

## Sources (verbatim rows from `data/MANIFEST.md`)

| dataset | source | version | sha256 | license | items (test split) | local file |
|---|---|---|---|---|---|---|
| cruxeval | https://huggingface.co/datasets/cruxeval-org/cruxeval | HF commit b96af0450242eb4da433032b90998f25588a5d0f | `055901f5e2c0742a71f347e09b25987253a70de777fa5ef9892873d7777950e6` | mit | 800 | `data/raw/cruxeval_test.jsonl` |
| gsm8k | https://huggingface.co/datasets/openai/gsm8k (config main) | HF commit 740312add88f781978c0658806c59bc2815b9866 | `752adc99f23132275139f1f7be57126b08735a55daf0c56859ee6df70abafbac` | mit | 1319 | `data/raw/gsm8k_test.jsonl` |
| wtq | https://github.com/ppasupat/WikiTableQuestions/releases/download/v1.0.2/WikiTableQuestions-1.0.2-compact.zip (HF stanfordnlp/wikitablequestions loader is script-based and no longer supported by `datasets`) | release v1.0.2 (repo master 7d455a5a) | `zip 7c9ca7cc1ccd75fe4be0255b44be63f7b566761005f4ee6ce67e51c129d8b085; tsv df232f69e78e5b7b61b9aa62efcaa01c75697a7411fd80348cf55107ad9fbdcd` | CC-BY-SA-4.0 | 4344 | `data/raw/wtq/WikiTableQuestions/data/pristine-unseen-tables.tsv` |

- code = CRUXEval, output-prediction task (`config/experiment.yaml` content_types.code); math = GSM8K config `main` test; table = WikiTableQuestions `pristine-unseen-tables` (the test split), from the GitHub release because the HF loader is script-based.

## Exclusion criteria (applied before sampling; `src/vmod/prepare.py` `exclusion_reasons`)

1. `max_line_chars`: any line of the content string longer than **160** characters
2. `max_lines`: content longer than **60** lines
3. `table_max_rows`: table with more than **40** data rows (table only)
4. `render_fails`: content contains a character that DejaVu Sans Mono cannot draw (no glyph in the font cmap) or a control character other than newline
5. `drop_if_over_context`: checked per model at run time. **0 requests were skipped** in any run (every `*.skipped.csv` is empty; integrity posts in COLLAB.md).

One item can fail several criteria, so per-criterion counts overlap.

## Counts

| content type | pool | max_line_chars | max_lines | table_max_rows | render_fails | items excluded | eligible | % excluded |
|---|---|---|---|---|---|---|---|---|
| code | 800 | 0 | 0 | 0 | 3 | 3 | 797 | 0.4% |
| math | 1319 | 0 | 0 | 0 | 0 | 0 | 1319 | 0.0% |
| table | 4344 | 1064 | 305 | 487 | 43 | 1396 | 2948 | 32.1% |

Items excluded by exactly one criterion (from `data/exclusions.csv`): code render_fails: 3; table max_line_chars: 896; table render_fails: 3; table table_max_rows: 144. Items with 2+ reasons: table: 208; table: 140; table: 5.

**Check of "32% of WTQ items excluded":** 1396 / 4344 = 32.14% → **confirmed (32%)**.

## Sampling

- seed **630** (`config/experiment.yaml` seed); per content type `random.Random(seed).sample(eligible sorted by source_index, 30 + 500)`; the first 30 = pilot, the remaining 500 = main (`src/vmod/prepare.py`, `main`).
- main per type: code 500, math 500, table 500; pilot per type: code 30, math 30, table 30 (`data/items/summary.json`).
- disjointness, checked now by item_id over `data/items/{pilot,main}_*.jsonl`: |pilot ∩ main| = **0** (90 pilot ids, 1500 main ids). The same assertion is in `prepare.py`.

