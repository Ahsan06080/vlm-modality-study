#!/usr/bin/env bash
# Usage: scripts/post_run.sh <model_id> <outdir> <task>  -> integrity check, gzip, COLLAB progress, commit+push
set -u
cd "$(dirname "$0")/.."
m=$1; out=$2; task=$3; slug=${m//\//__}; d=results/raw/$out
json=$(.venv/bin/python -m vmod.integrity "$m" "$out" 2>>logs/post.log) || json='{"ok": false, "error": "integrity script failed"}'
st=$(grep "START $m $out\$" logs/lanes.log | tail -1 | cut -c2-21); en=$(grep "END $m $out " logs/lanes.log | tail -1 | cut -c2-21)
T=$(date -u +"%Y-%m-%d %H:%M")
.venv/bin/python - "$json" "$m" "$out" "$st" "$en" "$T" "$task" >> COLLAB.md <<'PY'
import json, sys
import pandas as pd
j = json.loads(sys.argv[1]); m, out, st, en, T, task = sys.argv[2:9]
wall = round((pd.Timestamp(en) - pd.Timestamp(st)).total_seconds() / 60, 1) if st and en else "?"
C = list(j.get("parse", {})) or ["A_text", "B_image", "C_image_transcribe"]
print(f"\n### [{T} UTC] RUNNER -> PLANNER | {task} PROGRESS ({m.split('/')[-1]} {out} done)")
if "rows" not in j:
    print(f"**Summary:** integrity check FAILED to run ({j.get('error')}); see logs/post.log and the run log.")
    print("**Issues / questions:** run needs inspection"); sys.exit()
print(f"**Summary:** integrity {'OK' if j['ok'] else 'FAILED'}: {j['rows']}/{j['expected']} rows, skipped {j['skipped']}, duplicates {j['duplicates']}, missing {j['missing']}. Wall time {wall} min (generation {j['gen_hours']} h). finish_reason=length {j['pct_length']}%.")
print("**Numbers:** parse " + "/".join(c[0] for c in C) + " " + " / ".join(f"{j['parse'][c]:.3f}" for c in C) + " · accuracy " + "/".join(c[0] for c in C) + ": " +
      " · ".join(f"{ct} " + "/".join(f"{j['acc'][ct][c]:.3f}" for c in C) for ct in j["acc"]))
print(f"**Files:** results/raw/{out}/{m.replace('/', '__')}.jsonl.gz")
print("**Issues / questions:** none" if j["ok"] else "**Issues / questions:** integrity check failed, see above")
PY
git add COLLAB.md
for f in "$d/$slug.jsonl.gz" "$d/$slug.jsonl.meta.json" "$d/$slug.skipped.csv"; do [ -e "$f" ] && git add "$f"; done
case $out in *pilot*) [ -e "$d/$slug.jsonl" ] && git add "$d/$slug.jsonl";; esac
git commit -qm "$task: ${m##*/} $out"
git stash -q 2>/dev/null; git pull -q --rebase; git push -q; git stash pop -q 2>/dev/null || true
echo "posted $m $out"
