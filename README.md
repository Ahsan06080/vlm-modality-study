# Text vs. image input in vision-language models

CS 630 term project (controlled experiment). Does giving a vision-language model the same problem as an image instead of text change its accuracy (RQ1)? If it does, is the gap from misreading or from reasoning (RQ2)? Do the responses differ in length and error type (RQ3)?

## Design at a glance
- **Design:** a paired within-item experiment. Every item goes to every model in every condition.
- **Factors:**
  - **Input modality:** A text · B image · C image, transcribe then solve
  - **Content type:** code (CRUXEval) · math (GSM8K) · tables (WikiTableQuestions)
  - **Model (blocking):** open-weight VLMs at several sizes, plus optional API models
- **Responses:** correctness (1/0), transcription fidelity (CER, condition C), output tokens.
- **Closest prior work:** IsoBench (Fu et al., COLM 2024).

## Repo map
| Path | What |
|---|---|
| `COLLAB.md` | Message board between the owner, the planner (laptop) and the runner (lab server) |
| `TASKS.md` | The ordered run list for the lab server |
| `config/experiment.yaml` | All fixed design parameters |
| `prompts/templates.md` | Exact prompt text |
| `src/vmod/` | Pipeline code (written by the runner) |
| `data/` | Item files and manifests (images are git-ignored) |
| `results/` | Raw outputs, scored data, analysis tables, figures |
| `reports/` | Render samples, final numeric summary |

## Starting the runner on the lab server
```bash
git clone https://github.com/Ahsan06080/vlm-modality-study.git
cd vlm-modality-study
claude
```
Then tell it: *"You are the RUNNER. Read CLAUDE.md, COLLAB.md and TASKS.md, then start the loop."*
