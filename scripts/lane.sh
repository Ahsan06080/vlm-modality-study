#!/usr/bin/env bash
# Usage: scripts/lane.sh <gpus> <set> <tag> <model>...   Runs models sequentially; for each also a rep2 pass if tag=withrep.
set -u
cd "$(dirname "$0")/.."
gpus=$1; set=$2; tag=$3; shift 3
for m in "$@"; do
  slug=${m//\//__}
  echo "[$(date -u +%FT%TZ)] START $m $set" >> logs/lanes.log
  CUDA_VISIBLE_DEVICES=$gpus .venv/bin/python -m vmod run --model "$m" --set "$set" > "logs/${set}_${slug}.log" 2>&1
  echo "[$(date -u +%FT%TZ)] END $m $set exit=$?" >> logs/lanes.log
  if [ "$tag" = withrep ]; then
    CUDA_VISIBLE_DEVICES=$gpus .venv/bin/python -m vmod run --model "$m" --set "$set" --out-suffix _rep2 --shuffle-seed 631 > "logs/${set}_rep2_${slug}.log" 2>&1
    echo "[$(date -u +%FT%TZ)] END $m ${set}_rep2 exit=$?" >> logs/lanes.log
  fi
done
