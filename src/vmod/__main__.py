"""CLI: python -m vmod <command>."""
from __future__ import annotations

import argparse
import sys


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="vmod", description="Text vs image VLM modality study")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("download", help="T02: download datasets and write data/MANIFEST.md")
    sub.add_parser("prepare", help="T03: build canonical items, apply exclusions, sample pilot/main")
    p = sub.add_parser("render", help="T04: render item content to PNG")
    p.add_argument("--check-determinism", type=int, default=20)
    sub.add_parser("selftest", help="T05: gold/wrong-answer self-test of parser and scorers")
    p = sub.add_parser("run", help="T06-T08: vLLM offline inference")
    p.add_argument("--model", required=True)
    p.add_argument("--set", choices=["pilot", "main"], required=True)
    p.add_argument("--limit", type=int, default=None, help="items per content type (smoke test)")
    p.add_argument("--tp", type=int, default=None)
    p.add_argument("--out-suffix", default="")
    p = sub.add_parser("score", help="T10: score raw outputs")
    p.add_argument("--set", choices=["pilot", "main"], default="main")
    p = sub.add_parser("analyze", help="T11-T14: statistics, figures, summary")
    p.add_argument("--what", default="all")

    args = ap.parse_args(argv)
    if args.cmd == "download":
        from .download import main as f
    elif args.cmd == "prepare":
        from .prepare import main as f
    elif args.cmd == "render":
        from .render import main as f
    elif args.cmd == "selftest":
        from .selftest import main as f
    elif args.cmd == "run":
        from .run import main as f
    elif args.cmd == "score":
        from .score import main as f
    else:
        from .analyze import main as f
    return f(args) or 0


if __name__ == "__main__":
    sys.exit(main())
