#!/usr/bin/env bash
cd "$(dirname "$0")/.."
Q3=Qwen/Qwen2.5-VL-3B-Instruct; Q7=Qwen/Qwen2.5-VL-7B-Instruct; IV=OpenGVLab/InternVL3-8B; G12=google/gemma-3-12b-it; Q32=Qwen/Qwen2.5-VL-32B-Instruct
scripts/lane4.sh 0 T15 "$Q3,main,main_run2,631,2" "$Q3,main,main_run3,632,3" "$IV,main,main_run2,631,2" "$IV,main,main_run3,632,3" &
scripts/lane4.sh 1 T15 "$Q7,main,main_run2,631,2" "$Q7,main,main_run3,632,3" "$G12,main,main_run2,631,2" "$G12,main,main_run3,632,3" &
wait
scripts/lane4.sh 0,1 T15 "$Q32,main,main_run2,631,2" "$Q32,main,main_run3,632,3"
echo "[$(date -u +%FT%TZ)] T15 ALL LANES DONE" >> logs/lanes.log
