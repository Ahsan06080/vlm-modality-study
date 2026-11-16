#!/usr/bin/env bash
# Resolution control (condition B only). Usage: scripts/res.sh <gpus> <model> <outdir> [extra vmod run args...]
set -u
cd "$(dirname "$0")/.."
gpus=$1; m=$2; out=$3; shift 3
slug=${m//\//__}; lg="logs/${out//\//_}_${slug}.log"
echo "[$(date -u +%FT%TZ)] START $m $out" >> logs/lanes.log
CUDA_VISIBLE_DEVICES=$gpus .venv/bin/python -m vmod run --model "$m" --set main --out-dir "$out" --conditions B_image \
    --shuffle-seed 630 --run 1 --gpu-mem "${GPU_MEM:-0.80}" "$@" > "$lg" 2>&1
rc=$?
echo "[$(date -u +%FT%TZ)] END $m $out exit=$rc" >> logs/lanes.log
flock logs/git.lock scripts/post_run.sh "$m" "$out" RESCTL >> logs/post.log 2>&1
