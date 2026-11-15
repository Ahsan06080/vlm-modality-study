#!/usr/bin/env bash
# Phase 4 lane. Usage: scripts/lane4.sh <gpus> <task> <job>...   job = model,set,outdir,seed,run
# Runs jobs sequentially on <gpus> (fresh process each), then posts each (integrity, gzip, COLLAB, commit).
set -u
cd "$(dirname "$0")/.."
gpus=$1; task=$2; shift 2
for job in "$@"; do
  IFS=, read -r m set out seed run <<< "$job"
  slug=${m//\//__}; lg="logs/${out//\//_}_${slug}.log"
  echo "[$(date -u +%FT%TZ)] START $m $out" >> logs/lanes.log
  CUDA_VISIBLE_DEVICES=$gpus .venv/bin/python -m vmod run --model "$m" --set "$set" --out-dir "$out" \
      --shuffle-seed "$seed" --run "$run" --gpu-mem "${GPU_MEM:-0.80}" > "$lg" 2>&1
  rc=$?
  echo "[$(date -u +%FT%TZ)] END $m $out exit=$rc" >> logs/lanes.log
  flock logs/git.lock scripts/post_run.sh "$m" "$out" "$task" >> logs/post.log 2>&1
done
