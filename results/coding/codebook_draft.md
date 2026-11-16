# Error-coding codebook (DRAFT, for the human coder; not applied to any row)

Sheet: `results/coding/error_sample.csv`, 300 rows.
- Each row is an A-correct / B-wrong flip: the model solved the text version (condition A) but not the image-only version (condition B).
- The code describes **why the B response is wrong**.
- Fill `code` with one label below and `coder` with your initials.
- Use `response_B` as the main evidence. `content`, `gold` and `response_A` are context.
- `transcription_C` comes from a **different call** (condition C, same model and item). It is only a hint about how the model reads this image; it is not the B response.

## Labels

| label | definition |
|---|---|
| `perception` | The wrong answer comes from misreading the image: a character, number, operator, indentation, cell or row is read differently from `content`, and the reasoning that follows is consistent with the misread input. |
| `reasoning` | Everything the B response quotes or uses from the image matches `content`, but the computation or logic is wrong. |
| `format/parse` | The B answer is actually correct, or equivalent to `gold`, but the parser could not extract it or scored it wrong: missing or garbled `Final answer:` line, the answer is in a different form, or the response was truncated at the token limit before the final line. |
| `other` | None of the above, or not decidable: refusal, empty or looping output, the answer is about a different problem, or the evidence is insufficient to separate perception from reasoning. |

## Decision rules (apply in order)

1. **format/parse first.** If the value in `response_B` would be correct under a reasonable reading of `gold`, code `format/parse`, whatever the reasoning looked like.
   - *Illustrative example (constructed, not from the sheet):* gold `42`; B ends "**The answer is 42.**" with no `Final answer:` line.
2. **perception** if the B response visibly uses at least one input value or token that differs from `content`, and the wrong answer follows from that difference. If the response never restates the input, use `transcription_C` only as supporting evidence; on its own it is not enough.
   - *Illustrative example:* content has `x[1:]`; B reasons "the function takes `x[:1]`" and returns the first character.
3. **reasoning** if all restated inputs match `content` and the error is in the steps.
   - *Illustrative example:* the table is read correctly row by row, but B counts 7 matching rows instead of 8.
4. **other** for everything else.
   - *Illustrative example:* B repeats the problem statement until the 4,096-token limit with no answer. Exception: if a correct answer was already reached before the truncation, rule 1 applies.

## Notes

- **One label per row.** If both perception and reasoning errors are present, code `perception` when the misread alone would make the answer wrong. Otherwise code `reasoning`.
- **Inter-rater reliability (optional):** a second coder codes a random subset, e.g. 20% (60 rows), and Cohen's kappa is reported.
- **Status:** this codebook is a draft. No label definition existed in the repo before (searched `TASKS.md`, `COLLAB.md`, `reports/`, `results/coding/`). The OWNER should finalise it before coding.
