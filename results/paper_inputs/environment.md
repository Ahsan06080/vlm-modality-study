# Environment

Sources: `env/requirements.lock.txt` (written at T00, commit `5d8954b`, 2026-11-14 15:35 UTC; the only lock file — no Phase 4 lock was written), the installed environment now (`.venv`, built with uv 0.11.32; it has no `pip`, so versions were read with `importlib.metadata`), `nvidia-smi`, and the `vllm_version` field of every `results/raw/**/*.meta.json`.

- Python: **3.12.13** (CPython, `.venv/pyvenv.cfg`)
- vLLM recorded in every run sidecar: **0.33.0**
- CUDA: driver **580.178.04**, `nvidia-smi` CUDA version **13.0**; torch built with CUDA **13.0**, cuDNN **92400**
- GPUs: 4 × NVIDIA RTX PRO 5000 Blackwell, 48,935 MiB each (runs used GPU 0 and 1 only)

## Key packages

| package | version (lock = installed now) | used for |
|---|---|---|
| vllm | 0.33.0 |  |
| torch | 2.14.0 |  |
| torchvision | 0.29.0 |  |
| transformers | 5.20.2 |  |
| tokenizers | 0.23.3 |  |
| huggingface-hub | 2.4.0 |  |
| flashinfer-python | 0.7.2.post1 | installed; FlashInfer sampler disabled (VLLM_USE_FLASHINFER_SAMPLER=0, run.py) |
| triton | 3.8.0 |  |
| xgrammar | 0.2.8 |  |
| numpy | 2.3.5 |  |
| scipy | 1.18.1 | exact tests, GLMM optimiser |
| statsmodels | 0.15.0 | RQ2 logit, VB check of GLMM |
| patsy | 1.0.3 | design matrices (GLMM) |
| pandas | 3.1.1 |  |
| matplotlib | 3.11.2 |  |
| pillow | 13.0.0 | rendering (PIL.ImageFont/ImageDraw), image loading, 896 resize |
| fonttools | 4.68.0 | render_fails check (font cmap) |
| rapidfuzz | 3.14.6 | Levenshtein distance for CER (`rapidfuzz.distance.Levenshtein`, src/vmod/scoring.py:10) |
| pyyaml | 6.0.3 |  |
| tabulate | 0.10.0 |  |
| datasets | 5.2.0 |  |
| pyarrow | 26.0.1 |  |
| compressed-tensors | 0.17.0 | vLLM quantized-weight support |

## Changes between run 1 and later runs

- `diff` of the lock file against the installed environment (names normalised): **identical, 223/223 packages**. The only extra entry is the project package `vmod==0.1.0` (editable install of this repo).
- The environment directory was not rebuilt between runs (lock written 2026-11-14 before T06; run 1 2026-11-14 17:03; Phase 4 2026-11-15/16), and every raw sidecar records vLLM 0.33.0.
- Install record: `logs/pip_install.log` (2026-11-14 15:34 UTC): "Resolved 223 packages … Installed 223 packages"; every `*.dist-info` in `.venv` is dated 15:34:25 (one install, no later reinstall). Later directory mtimes in site-packages (16:21, 16:50) are `__pycache__` writes on first import.
- **No package version differs between run 1 and the later runs.** (The lock does not record a snapshot taken at Phase 4 time; the evidence is that the same unchanged `.venv` was used throughout and still matches the T00 lock.)

## Full lock file

See `env/requirements.lock.txt` (223 packages).
