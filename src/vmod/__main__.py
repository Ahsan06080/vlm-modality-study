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
    p.add_argument("--out-suffix", default="", help="e.g. _rep2 -> results/raw/pilot_rep2/")
    p.add_argument("--shuffle-seed", type=int, default=None, help="shuffle request order (T07b uses 631)")
    p.add_argument("--out-dir", default=None, help="Phase 4: output dir under results/raw, e.g. main_run2 or ext/run1")
    p.add_argument("--run", type=int, default=1, help="Phase 4 run number, stored in each row")
    p.add_argument("--gpu-mem", type=float, default=0.90, help="vLLM gpu_memory_utilization")
    p.add_argument("--conditions", default=None, help="comma list, e.g. B_image (resolution control); default all three")
    p.add_argument("--image-variant", choices=["native", "896"], default="native", help="896 = stretch to 896x896 (resolution control)")
    p.add_argument("--mm-override", default=None, help='JSON merged into mm_processor_kwargs, e.g. {"do_pan_and_scan": false}')
    p.add_argument("--chunk", type=int, default=512, help="requests per vLLM call (resume granularity)")
    p = sub.add_parser("score", help="T10: score raw outputs")
    p.add_argument("--set", default="main", help="pilot, main, pilot_rep2, pilot_smoke")
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
