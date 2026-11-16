# Compute: hardware and GPU-hours

## Hardware

Command: `nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv`

```
name, memory.total [MiB], driver_version
NVIDIA RTX PRO 5000 Blackwell, 48935 MiB, 580.178.04
NVIDIA RTX PRO 5000 Blackwell, 48935 MiB, 580.178.04
NVIDIA RTX PRO 5000 Blackwell, 48935 MiB, 580.178.04
NVIDIA RTX PRO 5000 Blackwell, 48935 MiB, 580.178.04
```

The server has 4 of these GPUs; runs used GPU 0 and 1 only (TP=2 jobs use both).

## GPU-hours

- `logs/` is git-ignored: `logs/lanes.log` exists only on the lab server (line numbers below refer to it).
- wall_h = END - START in `logs/lanes.log` (written by scripts/lane.sh, lane4.sh, res.sh, t17.sh): one fresh process per model-run, so it **includes model loading and vLLM warm-up**.
- n_gpus = `tensor_parallel_size` in the run's `*.jsonl.meta.json`; gpu_h = wall_h × n_gpus.
- Two jobs often ran at the same time on different GPUs, so the sum of GPU-hours is not elapsed time.
- Not included: `results/raw/pilot_smoke` (smoke test, 2 items per type) and failed launch attempts not in lanes.log.

| run             | model                            |   n_records | start_utc            | end_utc              |   wall_h |   n_gpus |   gpu_h | source                                                                                                |
|:----------------|:---------------------------------|------------:|:---------------------|:---------------------|---------:|---------:|--------:|:------------------------------------------------------------------------------------------------------|
| main            | OpenGVLab/InternVL3-8B           |        4500 | 2026-11-14T17:17:35Z | 2026-11-14T17:41:24Z |    0.397 |        1 |   0.397 | logs/lanes.log:21; logs/lanes.log:23                                                                  |
| main            | Qwen/Qwen2.5-VL-32B-Instruct     |        4500 | 2026-11-14T17:41:25Z | 2026-11-14T18:16:08Z |    0.579 |        2 |   1.157 | logs/lanes.log:24; logs/lanes.log:25                                                                  |
| main            | Qwen/Qwen2.5-VL-3B-Instruct      |        4500 | 2026-11-14T17:03:44Z | 2026-11-14T17:12:17Z |    0.142 |        1 |   0.142 | logs/lanes.log:16; logs/lanes.log:18                                                                  |
| main            | Qwen/Qwen2.5-VL-7B-Instruct      |        4500 | 2026-11-14T17:03:44Z | 2026-11-14T17:17:35Z |    0.231 |        1 |   0.231 | logs/lanes.log:17; logs/lanes.log:20                                                                  |
| main            | google/gemma-3-12b-it            |        4500 | 2026-11-14T17:12:17Z | 2026-11-14T17:36:55Z |    0.411 |        1 |   0.411 | logs/lanes.log:19; logs/lanes.log:22                                                                  |
| main_run2       | OpenGVLab/InternVL3-8B           |        4500 | 2026-11-15T10:05:25Z | 2026-11-15T10:39:18Z |    0.565 |        1 |   0.565 | logs/lanes.log:33; logs/lanes.log:36                                                                  |
| main_run2       | Qwen/Qwen2.5-VL-32B-Instruct     |        4500 | 2026-11-15T11:24:35Z | 2026-11-15T12:18:57Z |    0.906 |        2 |   1.812 | logs/lanes.log:42; logs/lanes.log:43                                                                  |
| main_run2       | Qwen/Qwen2.5-VL-3B-Instruct      |        4500 | 2026-11-15T09:44:11Z | 2026-11-15T09:54:47Z |    0.177 |        1 |   0.177 | logs/lanes.log:26; logs/lanes.log:28                                                                  |
| main_run2       | Qwen/Qwen2.5-VL-7B-Instruct      |        4500 | 2026-11-15T09:44:11Z | 2026-11-15T10:01:47Z |    0.293 |        1 |   0.293 | logs/lanes.log:27; logs/lanes.log:30                                                                  |
| main_run2       | google/gemma-3-12b-it            |        4500 | 2026-11-15T10:19:24Z | 2026-11-15T10:52:11Z |    0.546 |        1 |   0.546 | logs/lanes.log:35; logs/lanes.log:38                                                                  |
| main_run3       | OpenGVLab/InternVL3-8B           |        4500 | 2026-11-15T10:39:22Z | 2026-11-15T11:12:14Z |    0.548 |        1 |   0.548 | logs/lanes.log:37; logs/lanes.log:40                                                                  |
| main_run3       | Qwen/Qwen2.5-VL-32B-Instruct     |        4500 | 2026-11-15T12:19:02Z | 2026-11-15T13:13:21Z |    0.905 |        2 |   1.811 | logs/lanes.log:44; logs/lanes.log:45                                                                  |
| main_run3       | Qwen/Qwen2.5-VL-3B-Instruct      |        4500 | 2026-11-15T09:54:52Z | 2026-11-15T10:05:19Z |    0.174 |        1 |   0.174 | logs/lanes.log:29; logs/lanes.log:32                                                                  |
| main_run3       | Qwen/Qwen2.5-VL-7B-Instruct      |        4500 | 2026-11-15T10:01:54Z | 2026-11-15T10:19:19Z |    0.29  |        1 |   0.29  | logs/lanes.log:31; logs/lanes.log:34                                                                  |
| main_run3       | google/gemma-3-12b-it            |        4500 | 2026-11-15T10:52:15Z | 2026-11-15T11:24:31Z |    0.538 |        1 |   0.538 | logs/lanes.log:39; logs/lanes.log:41                                                                  |
| ext/run1        | OpenGVLab/InternVL3_5-8B         |        4500 | 2026-11-15T15:11:13Z | 2026-11-15T15:49:36Z |    0.64  |        1 |   0.64  | logs/lanes.log:60; logs/lanes.log:63                                                                  |
| ext/run1        | Qwen/Qwen2.5-VL-72B-Instruct-AWQ |        4500 | 2026-11-15T17:11:43Z | 2026-11-15T17:59:13Z |    0.792 |        2 |   1.583 | logs/lanes.log:73; logs/lanes.log:74                                                                  |
| ext/run1        | Qwen/Qwen3-VL-8B-Instruct        |        4500 | 2026-11-15T15:11:08Z | 2026-11-15T15:34:38Z |    0.392 |        1 |   0.392 | logs/lanes.log:58; logs/lanes.log:61                                                                  |
| ext/run1        | google/gemma-3-27b-it            |        4500 | 2026-11-15T13:19:28Z | 2026-11-15T13:55:11Z |    0.595 |        2 |   1.191 | logs/lanes.log:49; logs/lanes.log:50                                                                  |
| ext/run2        | OpenGVLab/InternVL3_5-8B         |        4500 | 2026-11-15T15:49:40Z | 2026-11-15T16:28:16Z |    0.643 |        1 |   0.643 | logs/lanes.log:64; logs/lanes.log:68                                                                  |
| ext/run2        | Qwen/Qwen2.5-VL-72B-Instruct-AWQ |        4500 | 2026-11-15T17:59:17Z | 2026-11-15T18:45:27Z |    0.769 |        2 |   1.539 | logs/lanes.log:75; logs/lanes.log:76                                                                  |
| ext/run2        | Qwen/Qwen3-VL-8B-Instruct        |        4500 | 2026-11-15T15:34:43Z | 2026-11-15T15:58:28Z |    0.396 |        1 |   0.396 | logs/lanes.log:62; logs/lanes.log:65                                                                  |
| ext/run2        | google/gemma-3-27b-it            |        4500 | 2026-11-15T13:55:15Z | 2026-11-15T14:31:54Z |    0.611 |        2 |   1.222 | logs/lanes.log:51; logs/lanes.log:52                                                                  |
| ext/run3        | OpenGVLab/InternVL3_5-8B         |        4500 | 2026-11-15T16:28:20Z | 2026-11-15T17:06:48Z |    0.641 |        1 |   0.641 | logs/lanes.log:69; logs/lanes.log:70                                                                  |
| ext/run3        | Qwen/Qwen2.5-VL-72B-Instruct-AWQ |        4500 | 2026-11-15T18:45:31Z | 2026-11-15T19:31:54Z |    0.773 |        2 |   1.546 | logs/lanes.log:77; logs/lanes.log:78                                                                  |
| ext/run3        | Qwen/Qwen3-VL-8B-Instruct        |        4500 | 2026-11-15T15:58:32Z | 2026-11-15T16:22:14Z |    0.395 |        1 |   0.395 | logs/lanes.log:66; logs/lanes.log:67                                                                  |
| ext/run3        | google/gemma-3-27b-it            |        4500 | 2026-11-15T14:31:59Z | 2026-11-15T15:07:41Z |    0.595 |        2 |   1.19  | logs/lanes.log:53; logs/lanes.log:54                                                                  |
| res896          | Qwen/Qwen2.5-VL-32B-Instruct     |        1500 | 2026-11-16T16:58:09Z | 2026-11-16T17:25:27Z |    0.455 |        2 |   0.91  | logs/lanes.log:84; logs/lanes.log:85                                                                  |
| res896          | Qwen/Qwen2.5-VL-7B-Instruct      |        1500 | 2026-11-16T16:49:08Z | 2026-11-16T16:57:37Z |    0.141 |        1 |   0.141 | logs/lanes.log:80; logs/lanes.log:82                                                                  |
| res_gemma_nopas | google/gemma-3-12b-it            |        1500 | 2026-11-16T16:49:08Z | 2026-11-16T16:58:06Z |    0.149 |        1 |   0.149 | logs/lanes.log:81; logs/lanes.log:83                                                                  |
| pilot           | OpenGVLab/InternVL3-8B           |         270 | 2026-11-14T16:51:06Z | 2026-11-14T16:53:27Z |    0.039 |        1 |   0.039 | logs/lanes.log:8; logs/lanes.log:10                                                                   |
| pilot           | Qwen/Qwen2.5-VL-32B-Instruct     |         270 | 2026-11-14T16:56:03Z | 2026-11-14T16:59:24Z |    0.056 |        2 |   0.112 | logs/lanes.log:13; logs/lanes.log:14                                                                  |
| pilot           | Qwen/Qwen2.5-VL-3B-Instruct      |         270 | 2026-11-14T16:48:15Z | 2026-11-14T16:49:27Z |    0.02  |        1 |   0.02  | logs/lanes.log:1; logs/lanes.log:3                                                                    |
| pilot           | Qwen/Qwen2.5-VL-7B-Instruct      |         270 | 2026-11-14T16:48:15Z | 2026-11-14T16:49:32Z |    0.021 |        1 |   0.021 | logs/lanes.log:2; logs/lanes.log:4                                                                    |
| pilot           | google/gemma-3-12b-it            |         270 | 2026-11-14T16:50:31Z | 2026-11-14T16:53:11Z |    0.044 |        1 |   0.044 | logs/lanes.log:6; logs/lanes.log:9                                                                    |
| pilot_rep2      | OpenGVLab/InternVL3-8B           |         270 | 2026-11-14T16:53:27Z | 2026-11-14T16:55:21Z |    0.032 |        1 |   0.032 | start = pilot END, logs/lanes.log:10 (scripts/lane.sh runs rep2 right after pilot); logs/lanes.log:11 |
| pilot_rep2      | Qwen/Qwen2.5-VL-32B-Instruct     |         270 | 2026-11-14T16:59:24Z | 2026-11-14T17:02:41Z |    0.055 |        2 |   0.109 | start = pilot END, logs/lanes.log:14 (scripts/lane.sh runs rep2 right after pilot); logs/lanes.log:15 |
| pilot_rep2      | Qwen/Qwen2.5-VL-3B-Instruct      |         270 | 2026-11-14T16:49:27Z | 2026-11-14T16:50:31Z |    0.018 |        1 |   0.018 | start = pilot END, logs/lanes.log:3 (scripts/lane.sh runs rep2 right after pilot); logs/lanes.log:5   |
| pilot_rep2      | Qwen/Qwen2.5-VL-7B-Instruct      |         270 | 2026-11-14T16:49:32Z | 2026-11-14T16:51:06Z |    0.026 |        1 |   0.026 | start = pilot END, logs/lanes.log:4 (scripts/lane.sh runs rep2 right after pilot); logs/lanes.log:7   |
| pilot_rep2      | google/gemma-3-12b-it            |         270 | 2026-11-14T16:53:11Z | 2026-11-14T16:55:55Z |    0.046 |        1 |   0.046 | start = pilot END, logs/lanes.log:9 (scripts/lane.sh runs rep2 right after pilot); logs/lanes.log:12  |
| ext/pilot       | OpenGVLab/InternVL3_5-8B         |         270 | 2026-11-15T15:07:45Z | 2026-11-15T15:11:10Z |    0.057 |        1 |   0.057 | logs/lanes.log:55; logs/lanes.log:59                                                                  |
| ext/pilot       | Qwen/Qwen2.5-VL-72B-Instruct-AWQ |         270 | 2026-11-15T17:06:52Z | 2026-11-15T17:11:39Z |    0.08  |        2 |   0.159 | logs/lanes.log:71; logs/lanes.log:72                                                                  |
| ext/pilot       | Qwen/Qwen3-VL-8B-Instruct        |         270 | 2026-11-15T15:07:45Z | 2026-11-15T15:11:05Z |    0.056 |        1 |   0.056 | logs/lanes.log:56; logs/lanes.log:57                                                                  |
| ext/pilot       | google/gemma-3-27b-it            |         270 | 2026-11-15T13:13:59Z | 2026-11-15T13:19:24Z |    0.09  |        2 |   0.181 | logs/lanes.log:47; logs/lanes.log:48                                                                  |

## Totals per group

| group       |   n_model_runs |   wall_h |   gpu_h |
|:------------|---------------:|---------:|--------:|
| primary     |              5 |    1.76  |   2.338 |
| replication |             10 |    4.942 |   6.754 |
| extension   |             12 |    7.242 |  11.378 |
| resolution  |              3 |    0.745 |   1.2   |
| pilot       |             14 |    0.64  |   0.92  |

**Grand total: 22.59 GPU-hours** over 44 model-runs (generated by `results/paper_inputs/_scripts/compute.py`).
