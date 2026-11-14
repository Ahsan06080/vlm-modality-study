"""Canonical content strings (prompts/templates.md, 'Canonical content strings')."""
from __future__ import annotations

import textwrap


def code_content(code: str, inp: str) -> str:
    return f"{code}\n\nCall: f({inp})"


def math_content(question: str, width: int = 80) -> str:
    return textwrap.fill(question, width)


def wtq_unescape(cell: str) -> str:
    # WTQ TSV escapes: \n newline, \\ backslash, \p pipe. Cell newlines become a space so each table row stays on one line.
    out, i = [], 0
    while i < len(cell):
        c = cell[i]
        if c == "\\" and i + 1 < len(cell):
            nxt = cell[i + 1]
            out.append({"n": " ", "p": "|", "\\": "\\"}.get(nxt, "\\" + nxt))
            i += 2
            continue
        out.append(c)
        i += 1
    return " ".join("".join(out).split())


def format_table(rows: list[list[str]]) -> str:
    """Column-aligned table: ' | ' separator, header row, then a row of dashes, then data rows. Lines right-stripped."""
    ncol = max(len(r) for r in rows)
    rows = [r + [""] * (ncol - len(r)) for r in rows]
    widths = [max(1, max(len(r[j]) for r in rows)) for j in range(ncol)]
    fmt = lambda r: " | ".join(c.ljust(w) for c, w in zip(r, widths)).rstrip()
    lines = [fmt(rows[0]), " | ".join("-" * w for w in widths)] + [fmt(r) for r in rows[1:]]
    return "\n".join(lines)


def table_content(rows: list[list[str]], question: str) -> str:
    return f"Table:\n{format_table(rows)}\n\nQuestion: {question}"
