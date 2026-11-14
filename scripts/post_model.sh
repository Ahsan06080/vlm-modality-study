#!/usr/bin/env bash
# Usage: scripts/post_model.sh <model_id>  -> integrity check, gzip, COLLAB report, commit+push
set -eu
cd "$(dirname "$0")/.."
m=$1; slug=${m//\//__}
json=$(.venv/bin/python -m vmod.integrity "$m" 2>/dev/null)
st=$(grep "START $m main" logs/lanes.log | tail -1 | cut -c2-21); en=$(grep "END $m main" logs/lanes.log | tail -1 | cut -c2-21)
wall=$(.venv/bin/python -c "import pandas as pd; print(round((pd.Timestamp('$en')-pd.Timestamp('$st')).total_seconds()/60,1))")
T=$(date -u +"%Y-%m-%d %H:%M")
.venv/bin/python - "$json" "$m" "$wall" "$T" >> COLLAB.md <<'PY'
import json, sys
j = json.loads(sys.argv[1]); m, wall, T = sys.argv[2], sys.argv[3], sys.argv[4]
C = ["A_text", "B_image", "C_image_transcribe"]
print(f"\n### [{T} UTC] RUNNER -> PLANNER | T08 PROGRESS ({m.split('/')[-1]} done)")
print(f"**Summary:** integrity {'OK' if j['ok'] else 'FAILED'}: {j['rows']}/{j['expected']} rows, skipped {j['skipped']}, duplicates {j['duplicates']}, missing {j['missing']}. Wall time {wall} min (generation {j['gen_hours']} h). finish_reason=length {j['pct_length']}%.")
print("**Numbers:** parse A/B/C " + " / ".join(f"{j['parse'][c]:.3f}" for c in C) + " · accuracy A/B/C: " +
      " · ".join(f"{ct} " + "/".join(f"{j['acc'][ct][c]:.3f}" for c in C) for ct in j["acc"]))
print(f"**Files:** results/raw/main/{m.replace('/', '__')}.jsonl.gz")
print("**Issues / questions:** none" if j["ok"] else "**Issues / questions:** integrity check failed, see above")
PY
git add COLLAB.md "results/raw/main/${slug}.jsonl.gz" "results/raw/main/${slug}.jsonl.meta.json" "results/raw/main/${slug}.skipped.csv"
git commit -qm "T08: main run ${m##*/}"
git stash -q 2>/dev/null; git pull -q --rebase; git push -q; git stash pop -q 2>/dev/null || true
echo "posted $m"
