#!/usr/bin/env bash
# Resolution-control pipeline: Qwen-7B@896 (GPU0) || Gemma-12B no-PAS (GPU1); then Qwen-32B@896 (GPU0,1, TP2).
cd "$(dirname "$0")/.."
scripts/res.sh 0 Qwen/Qwen2.5-VL-7B-Instruct res896 --image-variant 896 &
scripts/res.sh 1 google/gemma-3-12b-it res_gemma_nopas --mm-override '{"do_pan_and_scan": false}' &
wait
scripts/res.sh 0,1 Qwen/Qwen2.5-VL-32B-Instruct res896 --image-variant 896
echo "[$(date -u +%FT%TZ)] RESCTL ALL DONE" >> logs/lanes.log
