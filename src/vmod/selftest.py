"""T05 self-test: gold answers must all score correct; hand-made wrong/unparseable answers must all score incorrect."""
from __future__ import annotations

import json

from .config import DATA, REPORTS
from .meta import provenance
from .prompts import build_prompt
from .scoring import parse_answer, score_code_batch, score_math, score_table

WRONG = [  # (content_type, response, gold, gold_canon)
    ("code", "Final answer: [1, 2, 3]", "[1, 2]", None),
    ("code", "Final answer: 'abc'", "'abd'", None),
    ("code", "Final answer: abc", "'abc'", None),                       # not a literal
    ("code", "The answer is 5", "5", None),                             # no marker
    ("code", "Final answer: __import__('os').getcwd()", "'/'", None),   # no builtins in sandbox
    ("code", "Final answer: 9**9**9", "0", None),                       # timeout / memory guard
    ("code", "Final answer: (1, 2)", "[1, 2]", None),
    ("math", "Final answer: 17", "18", None),
    ("math", "Final answer: eighteen", "18", None),
    ("math", "So 18 dollars.", "18", None),                             # no marker
    ("math", "Final answer: 18.01", "18", None),
    ("math", "Final answer:", "18", None),                              # empty
    ("math", "Final answer: 18\nWait, recheck.\nFinal answer: 20", "18", None),  # last marker line wins
    ("table", "Final answer: Germany", ["Italy"], ["Italy"]),
    ("table", "Final answer: Italy | France", ["Italy"], ["Italy"]),    # extra item
    ("table", "Final answer: Italy", ["Italy", "France"], ["Italy", "France"]),  # missing item
    ("table", "Final answer: 4", ["3"], ["3.0"]),
    ("table", "I think it is Italy", ["Italy"], ["Italy"]),             # no marker
    ("table", "Final answer: 1999-01-02", ["1999-01-03"], ["1999-01-03"]),
    ("table", "Final answer: 100", ["100,000"], ["100000.0"]),
]


def main(args=None):
    items = []
    for s in ("pilot", "main"):
        for ct in ("code", "math", "table"):
            items += [json.loads(l) for l in open(DATA / "items" / f"{s}_{ct}.jsonl", encoding="utf-8")]
    # prompts must build for every item/condition
    for it in items:
        for cond in ("A_text", "B_image", "C_image_transcribe"):
            p = build_prompt(it["content_type"], cond, it["content"])
            assert ("{" + "CONTENT}") not in p and "{INSTRUCTION}" not in p
    gold_fail = []
    code_items = []
    for it in items:
        g = " | ".join(it["gold"]) if it["content_type"] == "table" else it["gold"]
        pred, ok = parse_answer(f"Let me think.\nFinal answer: {g}", it["content_type"])
        if it["content_type"] == "code":
            code_items.append((it, pred, ok))
            continue
        good = ok and (score_math(pred, it["gold"]) if it["content_type"] == "math" else score_table(pred, it["gold"], it["gold_canon"]))
        if not good:
            gold_fail.append((it["item_id"], g, pred))
    res = score_code_batch([(p, it["gold"]) for it, p, _ in code_items])
    gold_fail += [(it["item_id"], it["gold"], p) for (it, p, ok), r in zip(code_items, res) if not (ok and r)]

    wrong_fail = []
    for ct, resp, gold, canon in WRONG:
        pred, ok = parse_answer(resp, ct)
        if ct == "code":
            r = ok and score_code_batch([(pred, gold)])[0]
        elif ct == "math":
            r = ok and score_math(pred, gold)
        else:
            r = ok and score_table(pred, gold, canon)
        if r:
            wrong_fail.append((ct, resp, gold))
    out = dict(**provenance(), gold_n=len(items), gold_correct=len(items) - len(gold_fail), gold_failures=gold_fail,
               wrong_n=len(WRONG), wrong_scored_incorrect=len(WRONG) - len(wrong_fail), wrong_failures=wrong_fail)
    REPORTS.mkdir(exist_ok=True)
    (REPORTS / "selftest.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"gold: {out['gold_correct']}/{out['gold_n']} correct; wrong: {out['wrong_scored_incorrect']}/{out['wrong_n']} incorrect")
    for f in gold_fail[:20] + wrong_fail:
        print("FAIL", f)
    return 0 if not gold_fail and not wrong_fail else 1
