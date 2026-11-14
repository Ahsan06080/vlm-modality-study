"""T05: answer parser, per-content scorers, transcription metrics."""
from __future__ import annotations

import json
import math
import re
import subprocess
import sys

from rapidfuzz.distance import Levenshtein

from . import wtq_eval

MARKER = "Final answer:"


# ---------------------------------------------------------------- parser
def _strip_md(s: str) -> str:
    """Strip markdown/LaTeX wrappers at the edges only (never inside the answer), then a trailing period."""
    s = s.strip()
    for _ in range(5):
        old = s
        for w in ("**", "__", "`", "*"):
            if len(s) > 2 * len(w) and s.startswith(w) and s.endswith(w):
                s = s[len(w):-len(w)].strip()
        m = re.fullmatch(r"\$+(.+?)\$+", s)  # LaTeX-wrapped answer: $42$ or $$42$$
        if m:
            s = m.group(1).strip()
        s = re.sub(r"^\\boxed\{(.*)\}$", r"\1", s)
        s = re.sub(r"^\\text\{(.*)\}$", r"\1", s)
        if s.endswith("."):
            s = s[:-1].rstrip()
        if s == old:
            break
    return s


_MARKER_RE = re.compile(r"(?:\*\*|__)?\s*final answer\s*:\s*(?:\*\*|__)?", re.I)
# A markdown heading used as the marker, colon optional: '### Final Answer' / '**Final Answer**'
_HEADING_RE = re.compile(r"^\s*(?:#+\s*|\*\*\s*)?final answer\s*:?\s*(?:\*\*)?\s*$", re.I)


def _same_line(line: str) -> str:
    m = list(_MARKER_RE.finditer(line))[-1]
    pred = line[m.end():].strip()
    if pred.endswith("**") and not pred.startswith("**"):
        pred = pred[:-2]  # '**Final answer: 5**'
    return pred


def _following_block(lines: list[str], i: int) -> str:
    """Answer written on the lines after a bare marker: first non-empty block, code fences and \\[ \\] removed."""
    block = []
    for l in lines[i + 1:]:
        t = l.strip()
        if t.startswith("```") or t in ("\\[", "\\]", "$$"):
            if block and t.startswith("```"):
                break
            continue
        if not t:
            if block:
                break
            continue
        block.append(t)
    return " ".join(block).strip()


def _finish(pred: str, content_type: str) -> tuple[str | None, bool]:
    pred = _strip_md(pred)
    if pred.startswith("\\[") and pred.endswith("\\]"):
        pred = _strip_md(pred[2:-2])
    if content_type != "code":  # code answers are Python literals: quotes are part of the value
        if len(pred) >= 2 and pred[0] == pred[-1] and pred[0] in "\"'" and pred[0] not in pred[1:-1]:
            pred = pred[1:-1].strip()
    if pred == "":
        return None, False
    return pred, True


def parse_answer_strict(response: str | None, content_type: str) -> tuple[str | None, bool]:
    """Literal rule: LAST line containing 'Final answer:'; the answer must be on that line."""
    if not response:
        return None, False
    lines = [l for l in response.splitlines() if _MARKER_RE.search(l)]
    if not lines:
        return None, False
    return _finish(_same_line(lines[-1]), content_type)


def parse_answer(response: str | None, content_type: str) -> tuple[str | None, bool]:
    """Primary parser. LAST marker line ('Final answer:' anywhere in a line, or a bare 'Final Answer' heading).
    Answer = text after the marker on that line; if that is empty, the next non-empty block of lines.
    Whenever the strict parser succeeds, this returns the identical prediction."""
    if not response:
        return None, False
    lines = response.splitlines()
    idx = [i for i, l in enumerate(lines) if _MARKER_RE.search(l) or _HEADING_RE.match(l)]
    if not idx:
        return None, False
    i = idx[-1]
    pred = _same_line(lines[i]) if _MARKER_RE.search(lines[i]) else ""
    if not _strip_md(pred):
        pred = _following_block(lines, i)
    return _finish(pred, content_type)


# ---------------------------------------------------------------- code (sandboxed eval in a subprocess)
_CHILD = r"""
import json, signal, sys, resource, socket
resource.setrlimit(resource.RLIMIT_AS, (2 << 30, 2 << 30))
def _no_net(*a, **k): raise OSError("network disabled")
socket.socket = _no_net; socket.create_connection = _no_net
class TO(Exception): pass
def h(*a): raise TO()
signal.signal(signal.SIGALRM, h)
SAFE = {"__builtins__": {}, "inf": float("inf"), "nan": float("nan"), "set": set, "frozenset": frozenset, "True": True, "False": False, "None": None}
for line in sys.stdin:
    pred, gold = json.loads(line)
    r = False
    try:
        signal.alarm(TIMEOUT)
        r = bool(eval(pred, dict(SAFE), {}) == eval(gold, dict(SAFE), {}))
    except BaseException:
        r = False
    finally:
        signal.alarm(0)
    print(json.dumps(r), flush=True)
"""


def score_code_batch(pairs: list[tuple[str | None, str]], timeout: int = 5) -> list[bool]:
    """eval(pred) == eval(gold) in a subprocess: empty builtins, sockets disabled, 2 GB memory, per-item 5 s alarm."""
    todo = [(i, p, g) for i, (p, g) in enumerate(pairs) if p is not None]
    res = [False] * len(pairs)
    if not todo:
        return res
    child = _CHILD.replace("TIMEOUT", str(timeout))
    inp = "".join(json.dumps([p, g]) + "\n" for _, p, g in todo)
    try:
        out = subprocess.run([sys.executable, "-I", "-c", child], input=inp, capture_output=True, text=True,
                             timeout=timeout * len(todo) + 30, env={"PATH": "/usr/bin:/bin"})
        vals = [json.loads(l) for l in out.stdout.splitlines()]
        if len(vals) != len(todo):
            raise RuntimeError("child output truncated")
    except Exception:
        if len(todo) == 1:
            return res
        vals = [score_code_batch([(p, g)], timeout)[0] for _, p, g in todo]
    for (i, _, _), v in zip(todo, vals):
        res[i] = bool(v)
    return res


# ---------------------------------------------------------------- math
def _num(s: str):
    s = s.replace(",", "").replace("$", "").replace(" ", "")
    try:
        v = float(s)
        return v if math.isfinite(v) else None
    except ValueError:
        return None


def score_math(pred: str | None, gold: str) -> bool:
    if pred is None:
        return False
    p, g = _num(pred), _num(gold)
    return p is not None and g is not None and abs(p - g) <= 1e-6


# ---------------------------------------------------------------- table (official WTQ denotation match)
def score_table(pred: str | None, gold: list[str], gold_canon: list[str] | None = None) -> bool:
    if pred is None:
        return False
    target = wtq_eval.to_value_list(gold, gold_canon)
    pv = wtq_eval.to_value_list([x.strip() for x in pred.split("|") if x.strip()])
    return wtq_eval.check_denotation(target, pv)


def score_one(content_type: str, pred, item) -> bool:
    if content_type == "math":
        return score_math(pred, item["gold"])
    if content_type == "table":
        return score_table(pred, item["gold"], item.get("gold_canon"))
    return score_code_batch([(pred, item["gold"])])[0]


# ---------------------------------------------------------------- transcription (condition C)
_TR_HEADING = re.compile(r"^\W*(?:#+\s*)?(?:\*\*)?[\w ]{0,20}transcription\b[^\n]{0,20}$", re.I | re.M)


def extract_transcription_src(response: str | None) -> tuple[str | None, str]:
    """Primary: text between <transcription> tags. Unclosed tag: rest of the response.
    Fallback (models that ignore the tags): first code fence after a 'Transcription' heading line.
    Returns (text, source) with source in tags | open_tag | heading_fence | none."""
    if not response:
        return None, "none"
    m = re.search(r"<transcription>(.*?)</transcription>", response, re.S)
    if m:
        return m.group(1), "tags"
    m = re.search(r"<transcription>(.*)$", response, re.S)
    if m:
        return m.group(1), "open_tag"
    h = _TR_HEADING.search(response)
    if h:
        f = re.search(r"^[ \t]*```[^\n]*\n(.*?)^[ \t]*```", response[h.end():], re.S | re.M)
        if f:
            return f.group(1), "heading_fence"
    return None, "none"


def extract_transcription(response: str | None) -> str | None:
    return extract_transcription_src(response)[0]


def ws_norm(s: str) -> str:
    return " ".join(s.split())


def transcription_metrics(transcription: str | None, content: str) -> dict:
    """exact: equal after collapsing whitespace runs; cer: Levenshtein / len, on whitespace-normalized strings
    (primary, consistent with exact); cer_raw: same on raw strings. Missing transcription = empty string."""
    t = transcription if transcription is not None else ""
    tn, cn = ws_norm(t), ws_norm(content)
    return dict(transcription_exact=tn == cn,
                cer=Levenshtein.distance(tn, cn) / max(1, len(cn)),
                cer_raw=Levenshtein.distance(t.strip("\n"), content) / max(1, len(content)))
