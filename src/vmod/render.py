"""T04: render each item's content to PNG (config.render): monospace, no wrapping, black on white, size = text extent + padding."""
from __future__ import annotations

import csv
import hashlib
import json
import math
import random
import shutil
import statistics

from PIL import Image, ImageDraw, ImageFont

from .config import DATA, REPORTS, load_config
from .meta import header_lines
from .prepare import FONT_PATH

IMAGES = DATA / "images"


def load_items(sets=("pilot", "main")):
    items = []
    for s in sets:
        for ct in ("code", "math", "table"):
            for line in open(DATA / "items" / f"{s}_{ct}.jsonl", encoding="utf-8"):
                d = json.loads(line)
                d["set"] = s
                items.append(d)
    return items


def render_text(text: str, rcfg: dict) -> Image.Image:
    assert not rcfg["wrap"]
    font = ImageFont.truetype(FONT_PATH, rcfg["font_size_px"])
    pitch = round(rcfg["font_size_px"] * rcfg["line_height"])
    pad = rcfg["padding_px"]
    lines = text.split("\n")
    ascent, descent = font.getmetrics()
    width = math.ceil(max(font.getlength(l) for l in lines)) + 2 * pad
    height = (len(lines) - 1) * pitch + ascent + descent + 2 * pad
    img = Image.new("RGB", (width, height), rcfg["background"])
    draw = ImageDraw.Draw(img)
    for i, l in enumerate(lines):
        draw.text((pad, pad + i * pitch), l, font=font, fill=rcfg["foreground"])
    return img


def png_bytes(img) -> bytes:
    import io

    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=False)
    return buf.getvalue()


def image_path(item_id: str):
    return IMAGES / f"{item_id}.png"


def main(args=None):
    cfg = load_config()
    rcfg = cfg["render"]
    IMAGES.mkdir(parents=True, exist_ok=True)
    items = load_items()
    rows = []
    for it in items:
        b = png_bytes(render_text(it["content"], rcfg))
        image_path(it["item_id"]).write_bytes(b)
        img = Image.open(image_path(it["item_id"]))
        rows.append(dict(item_id=it["item_id"], content_type=it["content_type"], set=it["set"], width=img.width,
                         height=img.height, sha256=hashlib.sha256(b).hexdigest()))
    with open(DATA / "images_manifest.csv", "w", newline="", encoding="utf-8") as f:
        f.write(header_lines())
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    # determinism: re-render N random items in-process and compare hashes
    n = getattr(args, "check_determinism", 20) if args else 20
    rng = random.Random(cfg["seed"])
    by_id = {r["item_id"]: r for r in rows}
    chk = rng.sample(items, n)
    mism = [it["item_id"] for it in chk if hashlib.sha256(png_bytes(render_text(it["content"], rcfg))).hexdigest() != by_id[it["item_id"]]["sha256"]]
    print(f"determinism: {n - len(mism)}/{n} identical", mism)

    sdir = REPORTS / "render_samples"
    shutil.rmtree(sdir, ignore_errors=True)
    sdir.mkdir(parents=True)
    stats = {}
    for ct in ("code", "math", "table"):
        sub = [r for r in rows if r["content_type"] == ct]
        for r in rng.sample(sub, 4):
            shutil.copy(image_path(r["item_id"]), sdir / f"{ct}_random_{r['item_id']}.png")
        big = max(sub, key=lambda r: r["width"] * r["height"])
        shutil.copy(image_path(big["item_id"]), sdir / f"{ct}_largest_{big['item_id']}.png")
        ws, hs, px = [r["width"] for r in sub], [r["height"] for r in sub], [r["width"] * r["height"] for r in sub]
        stats[ct] = {k: (min(v), statistics.median(v), max(v)) for k, v in (("width", ws), ("height", hs), ("pixels", px))}
    print(json.dumps(stats, indent=1))
    (REPORTS / "render_samples" / "size_stats.json").write_text(json.dumps(dict(determinism=f"{n - len(mism)}/{n}", mismatches=mism, stats=stats), indent=1) + "\n")
    return 1 if mism else 0
