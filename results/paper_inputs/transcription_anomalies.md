# Transcription anomalies in condition C

**Method:**
- Data: raw responses from the jsonl.gz files, joined with `transcription_source` from the scored files.
- Every condition-C response was classified automatically by how it starts. Then 5 responses per content type with no extracted transcription were drawn (`DataFrame.sample(5, random_state=630)`) and read.
- The excerpts below are the first ~250 characters, with ⏎ marking a newline.
- The frozen extractor accepts, in order: `<transcription>` tags; an unclosed tag; or a code fence after a "Transcription" heading line (`src/vmod/scoring.py`, `extract_transcription_src`).

## InternVL3.5-8B (extension, run 1, `results/raw/ext/run1/OpenGVLab__InternVL3_5-8B.jsonl.gz`)

| content | no transcription found | what those responses do |
|---|---|---|
| code | 497 / 500 | **466 start with a bare code fence** holding a copy of the code and the `Call:` line, with no tags and no heading; then step-by-step reasoning and `Final answer:`. 27 start with `<think>` and contain no copy. 4 other. |
| math | 472 / 500 | **All 472 start with a `<think>` … `</think>` reasoning block and never copy the problem.** After `</think>` there is usually only the final line (median 19 characters, e.g. `Final answer: 5`). |
| table | 406 / 500 | 398 start with `<think>` and copy nothing; they paraphrase the relevant rows inside the reasoning. 8 mention a transcription without tags. |

- **`<think>` blocks:** 997 of the 1,500 condition-C responses start with `<think>`, and 99.5% of those close it. A `<think>` block is never treated as a transcription.
- **Tags:** `<transcription>` tags appear in only 125 responses: code 3, math 28, table 94. Of these, 100 start with a `<think>` block and have the tags later (code 3, math 28, table 69); the other 25 (table) don't start with `<think>`.
- **Leading-fence sensitivity:** with the approved rule, code coverage rises from 0.6% to 93.8%. Math and table cannot be recovered, because there is no copy in the response (`sens_leading_fence_recovered.csv`).

Sampled responses with no transcription (5 per content type):

- code `code-sample_472`: ` ```python⏎def f(text):⏎    d = {}⏎    for char in text.replace('-', '').lower():⏎        d[char] = d[char] + 1 if char in d else 1⏎    d = sorted(d.items(), key=lambda x: x[1])⏎    return [val for i, val in d]⏎⏎Call: f("x--y-z-5-C")⏎```⏎⏎Let's break down the f…`
- code `code-sample_283`, `code-sample_695`, `code-sample_549`, `code-sample_526`: same pattern. A leading ```` ```python ```` fence with the copied code and `Call:` line, then "Let's break down/analyze the function…".
- math `math-0117`: `<think>⏎So, John has 3 children, and he buys 2 pairs of shoes for each child. That means he buys 2 pairs per child times 3 children, which is 2 * 3 = 6 pairs …`
- math `math-0639`, `math-1262`, `math-1011`, `math-0797`: same pattern. Reasoning inside `<think>` restates the facts in prose; no verbatim copy.
- table `table-nu-1663`: `<think>⏎So, looking at the table, I need to count how many times "Downhill" appears in the "Discipline" column. Let's go through each row:⏎⏎1. 1993: Discipline is Downhill⏎2. 1994: Discipline is Super G …`
- table `table-nu-921`, `table-nu-2840`, `table-nu-1152`, `table-nu-305`: same pattern. Rows are listed selectively inside `<think>`; no full table copy.

## Gemma-3-12B, code (primary model, run 1, `results/raw/main/google__gemma-3-12b-it.jsonl.gz`)

**Frozen extractor, condition C code:**
- tags: 66
- heading + fence: 34
- **none: 400 of 500 (80%)**

Of those 400:

| pattern | n | description |
|---|---|---|
| starts with a bare code fence | 312 | copy of the code and `Call:` line in a fence (sometimes ```` ```python ````), no tags, no heading; then an explanation and `Final answer:` |
| intro sentence, then a fence | 88 | first line is a sentence, not a heading the extractor accepts. Most common: "Here's the transcription of the code:" (37), "Here's a step-by-step breakdown of the code's execution:" (17), "Here's the transcription of the code and the step-by-step so…" (13), "Here's a breakdown of the Python code and the predicted …" (≈13). 79.5% of these 88 contain a fence later. The heading rule fails because the line has more than 20 characters before "transcription" or doesn't contain the word. |

No `<think>` blocks occur in Gemma output.

**Leading-fence sensitivity:** code coverage rises from 20.0% to 82.4% (312 recovered). The 88 intro-sentence responses are still not extracted.

Sampled responses with no transcription (5):

- `code-sample_739`: ` ```⏎def f(st, pattern):⏎    for p in pattern:⏎        if not st.startswith(p): return False⏎        st = st[len(p):]⏎    return True⏎⏎Call: f('qwbnjrx', ['jr', 'b', 'r', 'qw'])⏎```⏎⏎The function `f` takes a string `st` and a list of strings …`
- `code-sample_538`, `code-sample_725`: the same bare leading fence, then "The function `f` takes …".
- `code-sample_451`: `Here's the transcription of the code:⏎⏎```⏎def f(text, char):⏎    text = list(text)⏎ …` (an intro sentence; the heading rule does not match).
- `code-sample_287`: `Here's a breakdown of the code and the predicted output:⏎⏎**Code:**⏎⏎```python⏎def f(name): …` (the copy sits under a `**Code:**` heading).

**Other cells, for reference** (frozen extractor; not inspected in detail):
- Gemma-12B math: 112 of 500 with no transcription.
- Gemma-12B table: 89 of 500 with no transcription. Of these, 41 start with a fence and are recovered by the sensitivity rule.
