# Frozen prompt templates

Source: `prompts/templates.md`, read verbatim by `src/vmod/prompts.py` (`templates()`, `build_prompt()`). Neither file changed after commit `e26abed` (2026-11-14 15:42 UTC, T05), before the pilot and run 1: `git diff --stat 88ac882 HEAD -- prompts/templates.md src/vmod/prompts.py` and `git diff --stat 7cbe190 HEAD -- …` are both empty. Tag `config-frozen-v1` covers them.

Placeholders: `⟪CONTENT⟫` = the canonical content string of the item (inserted only in condition A). In B and C the image is attached **before** the text (`src/vmod/run.py`, `messages()`: `[image_pil, text]`). Each prompt is sent as one user turn through `vllm.LLM.chat` with the model's default chat template; **the runner sends no system message**, but see the chat-template note below.

Canonical content strings (`prompts/templates.md`, `src/vmod/content.py`): code = `{code}` + blank line + `Call: f({input})`; math = question word-wrapped at 80 chars (`textwrap.fill`); table = `Table:` + newline + column-aligned table (`" | "` separator, header row, dash row) + blank line + `Question: {question}`.

## code × A, text

```
You are given a Python function and a call to it. Predict the exact value the call returns.
Think step by step. On the last line write: Final answer: <the returned value as a Python literal>

Problem:
<<<
⟪CONTENT⟫
>>>
```

## code × B, image  (image attached before this text)

```
You are given a Python function and a call to it. Predict the exact value the call returns.
Think step by step. On the last line write: Final answer: <the returned value as a Python literal>

The problem is shown in the image.
```

## code × C, image + transcribe  (image attached before this text)

```
You are given a Python function and a call to it. Predict the exact value the call returns.
Think step by step. On the last line write: Final answer: <the returned value as a Python literal>

The problem is shown in the image. First, copy all text in the image exactly, keeping line breaks and spacing, between <transcription> and </transcription>. Then solve the problem.
```

## math × A, text

```
Solve the math word problem.
Think step by step. On the last line write: Final answer: <a number only, no units>

Problem:
<<<
⟪CONTENT⟫
>>>
```

## math × B, image  (image attached before this text)

```
Solve the math word problem.
Think step by step. On the last line write: Final answer: <a number only, no units>

The problem is shown in the image.
```

## math × C, image + transcribe  (image attached before this text)

```
Solve the math word problem.
Think step by step. On the last line write: Final answer: <a number only, no units>

The problem is shown in the image. First, copy all text in the image exactly, keeping line breaks and spacing, between <transcription> and </transcription>. Then solve the problem.
```

## table × A, text

```
Answer the question using the table.
Think step by step. On the last line write: Final answer: <the answer; if there are several, separate them with " | ">

Problem:
<<<
⟪CONTENT⟫
>>>
```

## table × B, image  (image attached before this text)

```
Answer the question using the table.
Think step by step. On the last line write: Final answer: <the answer; if there are several, separate them with " | ">

The problem is shown in the image.
```

## table × C, image + transcribe  (image attached before this text)

```
Answer the question using the table.
Think step by step. On the last line write: Final answer: <the answer; if there are several, separate them with " | ">

The problem is shown in the image. First, copy all text in the image exactly, keeping line breaks and spacing, between <transcription> and </transcription>. Then solve the problem.
```

## Fully rendered example (as the model sees it)

Item `math-0611` (math), Qwen2.5-VL-7B-Instruct (revision `cc594898`), produced with the model's HF chat template (`AutoProcessor.apply_chat_template`, add_generation_prompt=True). The prompt text itself is not stored in the jsonl, only `prompt_sha256`; the sha256 of the text built here equals the logged `prompt_sha256` for all three conditions of this item, and the token count of the templated A prompt (128) equals the logged `input_tokens` (128), so vLLM applied this template. In B/C, `<|image_pad|>` is expanded by the processor into the image tokens.

### A_text

```
<|im_start|>system
You are a helpful assistant.<|im_end|>
<|im_start|>user
Solve the math word problem.
Think step by step. On the last line write: Final answer: <a number only, no units>

Problem:
<<<
John decides to build a program capable of identifying cancer cells.  He gets
initial funding of $100,000 for the first 5 months of research.  His research
ends up taking 10 times that long and every month after those first 5 took 50%
more funding per month.  How much did his research cost?
>>><|im_end|>
<|im_start|>assistant
```

### C_image_transcribe

```
<|im_start|>system
You are a helpful assistant.<|im_end|>
<|im_start|>user
<|vision_start|><|image_pad|><|vision_end|>Solve the math word problem.
Think step by step. On the last line write: Final answer: <a number only, no units>

The problem is shown in the image. First, copy all text in the image exactly, keeping line breaks and spacing, between <transcription> and </transcription>. Then solve the problem.<|im_end|>
<|im_start|>assistant
```

## Chat-template note (system prompts added by the model's own template)

The runner sends no system message, but `llm.chat` applies each model's default chat template, and some templates insert a default system prompt. Checked by rendering the A prompt of `math-0611` with each model's tokenizer at the pinned revision and comparing token counts with the logged `input_tokens` (all equal):

| model | default system prompt inserted by template | template tokens = logged input_tokens |
|---|---|---|
| Qwen2.5-VL-3B/7B/32B (and 72B-AWQ) | yes: `You are a helpful assistant.` | 128 = 128 (7B) |
| InternVL3-8B | yes: a Chinese self-introduction (`你是书生·万象，英文名是InternVL，…`) | 154 = 154 |
| gemma-3-12b-it | no | 122 = 122 |

Extension models (Qwen3-VL-8B, InternVL3.5-8B, gemma-3-27b) were not checked here.
