# Data manifest

<!--
study_id: vlm-modality-v1
git_commit: 1d05d95279ef232be7943d7091cd83fb97166eea
created_utc: 2026-11-14T15:37:01Z
-->

Raw files live in `data/raw/` (git-ignored); re-create with `python -m vmod download`.

| dataset | source | version | sha256 | license | items (test split) | local file |
|---|---|---|---|---|---|---|
| cruxeval | https://huggingface.co/datasets/cruxeval-org/cruxeval | HF commit b96af0450242eb4da433032b90998f25588a5d0f | `055901f5e2c0742a71f347e09b25987253a70de777fa5ef9892873d7777950e6` | mit | 800 | `data/raw/cruxeval_test.jsonl` |
| gsm8k | https://huggingface.co/datasets/openai/gsm8k (config main) | HF commit 740312add88f781978c0658806c59bc2815b9866 | `752adc99f23132275139f1f7be57126b08735a55daf0c56859ee6df70abafbac` | mit | 1319 | `data/raw/gsm8k_test.jsonl` |
| wtq | https://github.com/ppasupat/WikiTableQuestions/releases/download/v1.0.2/WikiTableQuestions-1.0.2-compact.zip (HF stanfordnlp/wikitablequestions loader is script-based and no longer supported by `datasets`) | release v1.0.2 (repo master 7d455a5a) | `zip 7c9ca7cc1ccd75fe4be0255b44be63f7b566761005f4ee6ce67e51c129d8b085; tsv df232f69e78e5b7b61b9aa62efcaa01c75697a7411fd80348cf55107ad9fbdcd` | CC-BY-SA-4.0 | 4344 | `data/raw/wtq/WikiTableQuestions/data/pristine-unseen-tables.tsv` |

License notes: MIT (CRUXEval, GSM8K) and CC BY-SA 4.0 (WTQ) all allow research use. Redistributing derived WTQ tables (item files) requires attribution and the same license.
