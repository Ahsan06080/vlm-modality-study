import pytest

from vmod.prompts import build_prompt
from vmod.scoring import (extract_transcription, parse_answer, score_code_batch, score_math, score_table,
                          transcription_metrics)


@pytest.mark.parametrize("resp,ct,want", [
    ("Final answer: 18", "math", "18"),
    ("**Final answer:** 18", "math", "18"),
    ("**Final answer: 18**", "math", "18"),
    ("Final answer: **18**", "math", "18"),
    ("Final answer: $18$", "math", "18"),
    ("Final answer: \\boxed{18}", "math", "18"),
    ("Final answer: 18.", "math", "18"),
    ("final answer: 18", "math", "18"),
    ("Final answer: \"Italy\"", "table", "Italy"),
    ("Final answer: \"A\" | \"B\"", "table", "\"A\" | \"B\""),
    ("Final answer: `'abc'`", "code", "'abc'"),
    ("Final answer: 'abc'", "code", "'abc'"),
    ("Final answer: 'aa++___bb'", "code", "'aa++___bb'"),
    ("Final answer: '5*83*23***'", "code", "'5*83*23***'"),
    ("Final answer: [1, 2].", "code", "[1, 2]"),
    ("step\nFinal answer: 1\nmore\nFinal answer: 2", "math", "2"),
])
def test_parse(resp, ct, want):
    pred, ok = parse_answer(resp, ct)
    assert ok and pred == want


@pytest.mark.parametrize("resp", [None, "", "no marker here", "Final answer:", "Final answer: **"])
def test_parse_fail(resp):
    assert parse_answer(resp, "math")[1] is False


def test_code():
    assert score_code_batch([("[1, 2]", "[1, 2]"), ("{'a': 1}", "{'a':1}"), ("(1,)", "(1,)"),
                             ("[1]", "[2]"), (None, "1"), ("foo", "'foo'"), ("open('/etc/passwd')", "''")]) == \
        [True, True, True, False, False, False, False]


def test_code_timeout():
    assert score_code_batch([("9**9**9", "0")], timeout=1) == [False]


def test_math():
    assert score_math("1,000", "1000")
    assert score_math("$18", "18")
    assert score_math("18.0000001", "18")
    assert not score_math("18.1", "18")
    assert not score_math("x", "18")


def test_table():
    assert score_table("italy", ["Italy"], ["Italy"])
    assert score_table("100000", ["100,000"], ["100000.0"])
    assert score_table("100,000", ["100,000"], ["100000.0"])
    assert score_table("France | Italy", ["Italy", "France"], ["Italy", "France"])
    assert not score_table("Italy", ["Italy", "France"], ["Italy", "France"])
    assert score_table("3", ["3"], ["3.0"])
    assert not score_table("4", ["3"], ["3.0"])


def test_transcription():
    r = "<transcription>\ndef f(x):\n  return x\n</transcription>\nFinal answer: 1"
    t = extract_transcription(r)
    m = transcription_metrics(t, "def f(x):\n    return x")
    assert m["transcription_exact"] and m["cer"] == 0
    m = transcription_metrics(None, "abc")
    assert not m["transcription_exact"] and m["cer"] == 1.0
    assert transcription_metrics("abd", "abc")["cer"] == pytest.approx(1 / 3)


def test_prompts():
    p = build_prompt("math", "A_text", "2+2?")
    assert p.startswith("Solve the math word problem.") and "<<<\n2+2?\n>>>" in p
    p = build_prompt("code", "C_image_transcribe", "x")
    assert "<transcription>" in p and "x" not in p.split("\n")[-1][:1]
    assert "{CONTENT}" not in build_prompt("table", "B_image", "x")


@pytest.mark.parametrize("resp,ct,want", [
    ("### Final Answer:\n\\[\n\\boxed{24}\n\\]", "math", "24"),
    ("### Final Answer:\n\\[ \\boxed{24} \\]", "math", "24"),
    ("### Final Answer\n```python\n'mgIRt'\n```", "code", "'mgIRt'"),
    ("### Final Answer:\n```python\n[(\"a\", 1), (\"b\", 45)]\n```", "code", "[(\"a\", 1), (\"b\", 45)]"),
    ("**Final Answer:**\nItaly", "table", "Italy"),
    ("Final answer: 5\nmore text\n### Final Answer:\n7", "math", "7"),
])
def test_parse_next_line(resp, ct, want):
    from vmod.scoring import parse_answer_strict
    pred, ok = parse_answer(resp, ct)
    assert ok and pred == want
    assert parse_answer_strict(resp, ct)[1] is False or parse_answer_strict(resp, ct)[0] == want


def test_strict_agrees_when_ok():
    from vmod.scoring import parse_answer_strict
    for r in ["Final answer: 18", "**Final answer:** 'a__b'", "x\nFinal answer: [1, 2]."]:
        s = parse_answer_strict(r, "code")
        assert s[1] and s == parse_answer(r, "code")
