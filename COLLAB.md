# COLLAB: message board between the planner, the lab server and the owner

## Roles
- **OWNER:** Ahsan. Makes all decisions, writes the paper, codes the error sample, and holds the API keys.
- **PLANNER:** Claude on the owner's laptop. Designs tasks, reviews reports, and approves gates when the owner agrees.
- **RUNNER:** Claude on the lab server. Implements and runs the tasks in TASKS.md, in order.

## Loop for the RUNNER
1. `git pull --rebase`. Read the newest messages here, then TASKS.md.
2. Take the first `TODO` task. Set it to `IN-PROGRESS`, commit and push. Work on that task only.
3. When it's done (or blocked), set the status in TASKS.md, append a report below, then commit and push. Commit message: `T0x: <short summary>`.
4. At a ⛔ GATE, stop until a message here says `APPROVED Gx`. Check every few minutes with `git pull`.
5. If something in the plan looks wrong, post a `QUESTION` and wait. Don't silently change the design.

## Rules
- `config/experiment.yaml` and `prompts/templates.md` change only through an approved message. After the tag `config-frozen-v1`, they don't change at all.
- Never commit secrets, tokens, model weights or `data/images/`.
- Never write paper text (the course forbids AI-written paper content). Produce numbers, tables and figures only.
- Report failures honestly, with the error output. Never invent numbers.
- Long jobs: run them with `nohup` or `tmux`, log to `logs/` (git-ignored), and post progress at least every 2 hours.

## Message format
Append new messages at the **bottom**. Never edit old ones.

```
### [YYYY-MM-DD HH:MM UTC] RUNNER -> PLANNER | T03 DONE
**Summary:** one or two lines
**Numbers:** key counts and results (tables welcome)
**Files:** paths committed
**Issues / questions:** anything needing a decision (or "none")
```
Allowed tags after the task ID: `STARTED`, `PROGRESS`, `DONE`, `BLOCKED`, `QUESTION`, `APPROVED Gx`, `DECISION`, `ALL DONE`.

---

## Log

### [2026-11-11] PLANNER -> RUNNER | KICKOFF
**Summary:** The repo is set up. Start with T00 and work down TASKS.md. The deadline is tight (paper due Nov 16), so keep each report short and post promptly. Stop at G1 and G2.
**Files:** README.md, TASKS.md, config/experiment.yaml, prompts/templates.md
**Issues / questions:** In T00, tell us whether `HF_TOKEN` is set (Gemma is gated) and whether the 72B model fits in 4×48 GB with room for KV cache.
