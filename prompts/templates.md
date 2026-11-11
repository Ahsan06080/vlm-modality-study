# Prompt templates (frozen at Gate G2)

Use these strings verbatim. `{INSTRUCTION}` is the content-type instruction, `{CONTENT}` the canonical content string.
Send each as a single user turn through the model's own chat template. No system prompt.

## Content-type instructions

**code**
```
You are given a Python function and a call to it. Predict the exact value the call returns.
Think step by step. On the last line write: Final answer: <the returned value as a Python literal>
```

**math**
```
Solve the math word problem.
Think step by step. On the last line write: Final answer: <a number only, no units>
```

**table**
```
Answer the question using the table.
Think step by step. On the last line write: Final answer: <the answer; if there are several, separate them with " | ">
```

## Condition wrappers

**A_text**
```
{INSTRUCTION}

Problem:
<<<
{CONTENT}
>>>
```

**B_image** (image attached before the text)
```
{INSTRUCTION}

The problem is shown in the image.
```

**C_image_transcribe** (image attached before the text)
```
{INSTRUCTION}

The problem is shown in the image. First, copy all text in the image exactly, keeping line breaks and spacing, between <transcription> and </transcription>. Then solve the problem.
```

## Canonical content strings

- **code:** `{code}` + blank line + `Call: f({input})`
- **math:** the question, word-wrapped at 80 characters (Python `textwrap.fill`)
- **table:** `Table:` + newline + column-aligned table (`" | "` separator, header row, then a row of dashes) + blank line + `Question: {question}`
