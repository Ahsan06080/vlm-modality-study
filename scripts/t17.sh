#!/usr/bin/env bash
# T17: extension models. Waits for T15 to finish, then: gemma-27b (TP=2) -> Qwen3-VL-8B || InternVL3.5-8B (TP=1) -> 72B-AWQ (TP=2).
cd "$(dirname "$0")/.."
until grep -q "T15 ALL LANES DONE" logs/lanes.log; do sleep 60; done
deadline=$(cat logs/phase4_deadline)   # epoch seconds: T15 start + 16 h
ext_model() {  # gpus model
  local g=$1 m=$2
  if [ "$(date +%s)" -ge "$deadline" ]; then echo "[$(date -u +%FT%TZ)] BUDGET SKIP $m" >> logs/lanes.log; return; fi
  scripts/lane4.sh "$g" T17 "$m,pilot,ext/pilot,630,1"
  if ! .venv/bin/python -m vmod.ext_gate "$m" >> logs/ext_gate.log 2>>logs/post.log; then
    echo "[$(date -u +%FT%TZ)] GATE DROP $m" >> logs/lanes.log; return; fi
  for r in 1 2 3; do
    if [ "$(date +%s)" -ge "$deadline" ]; then echo "[$(date -u +%FT%TZ)] BUDGET STOP $m before run$r" >> logs/lanes.log; return; fi
    scripts/lane4.sh "$g" T17 "$m,main,ext/run$r,$((629+r)),$r"
  done
}
ext_model 0,1 google/gemma-3-27b-it
ext_model 0 Qwen/Qwen3-VL-8B-Instruct &
ext_model 1 OpenGVLab/InternVL3_5-8B &
wait
ext_model 0,1 Qwen/Qwen2.5-VL-72B-Instruct-AWQ
echo "[$(date -u +%FT%TZ)] T17 ALL LANES DONE" >> logs/lanes.log
