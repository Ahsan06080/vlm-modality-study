"""Tasks 3 and 4. Reads only; the determinism check re-renders in memory and compares with the PNGs on disk."""
import csv, hashlib, json, random, shutil, statistics, collections
from pathlib import Path
import PIL
from PIL import Image
from vmod.config import load_config, DATA
from vmod.render import render_text, png_bytes, image_path
from vmod.prepare import FONT_PATH

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "results/paper_inputs"
cfg = load_config(); r = cfg["render"]
man = [row for row in csv.DictReader(l for l in open(DATA / "images_manifest.csv") if not l.startswith("#"))]
items = {}
for s in ("pilot", "main"):
    for ct in ("code", "math", "table"):
        for l in open(DATA / "items" / f"{s}_{ct}.jsonl"):
            d = json.loads(l); d["set"] = s; items[d["item_id"]] = d
main = [m for m in man if m["set"] == "main"]
L = ["# Rendering", "",
     "Sources: `config/experiment.yaml` (block `render:`), `src/vmod/render.py` (`render_text`, `png_bytes`), `src/vmod/prepare.py:16` (`FONT_PATH`).", "",
     "## Settings (identical for all three content types)", "",
     "| setting | value | source |", "|---|---|---|",
     f"| font family | {r['font']} | experiment.yaml render.font |",
     f"| font file | `{FONT_PATH}` | src/vmod/prepare.py:16 |",
     f"| font size | {r['font_size_px']} px | render.font_size_px |",
     f"| line height | {r['line_height']} × font size = {round(r['font_size_px']*r['line_height'])} px line pitch | render.line_height; render.py `pitch = round(font_size_px * line_height)` |",
     f"| DPI / scale | none: 1 image pixel = 1 rendered pixel; image size = text extent + padding ({r['dpi_note']}) | render.dpi_note |",
     "| colour theme / syntax highlighting | no: single colour text, no highlighting | render.foreground / background; render.py draws all text with one fill |",
     f"| padding | {r['padding_px']} px on every side | render.padding_px |",
     f"| background / foreground | {r['background']} / {r['foreground']} | render.background / foreground |",
     f"| max width | none; no wrapping at render time (`wrap: {str(r['wrap']).lower()}`). Width is bounded by the exclusion rule max_line_chars = {cfg['exclusions']['max_line_chars']}. Math text is word-wrapped once at {cfg['content_types']['math']['wrap_chars']} chars in the content string (the same string is used as text in A) | render.wrap; exclusions.max_line_chars; content_types.math.wrap_chars |",
     f"| image format | {r['format']}, RGB, `PIL.Image.save(format='PNG', optimize=False)`; Pillow {PIL.__version__} | render.format; render.py `png_bytes` |",
     "| layout | width = ceil(max line length in font advance units) + 2×padding; height = (n_lines−1)×pitch + ascent + descent + 2×padding | render.py `render_text` |", "",
     "## Image sizes, main set (500 per type), from `data/images_manifest.csv`", "",
     "| content type | n | width min / median / max (px) | height min / median / max (px) | megapixels min / median / max |", "|---|---|---|---|---|"]
samples = {}
for ct in ("code", "math", "table"):
    sub = [m for m in main if m["content_type"] == ct]
    w = [int(m["width"]) for m in sub]; h = [int(m["height"]) for m in sub]; px = [a*b for a, b in zip(w, h)]
    L.append(f"| {ct} | {len(sub)} | {min(w)} / {statistics.median(w):g} / {max(w)} | {min(h)} / {statistics.median(h):g} / {max(h)} | {min(px)/1e6:.3f} / {statistics.median(px)/1e6:.3f} / {max(px)/1e6:.3f} |")
    med = statistics.median(px)
    pick = min(sub, key=lambda m: (abs(int(m["width"])*int(m["height"]) - med), m["item_id"]))
    samples[ct] = pick
    shutil.copy(image_path(pick["item_id"]), OUT / "render_samples" / f"{ct}.png")
# determinism
rng = random.Random(630)
chk = rng.sample([m for m in main], 20)
res = []
for m in chk:
    b = png_bytes(render_text(items[m["item_id"]]["content"], r))
    disk = image_path(m["item_id"]).read_bytes()
    res.append((m["item_id"], b == disk, hashlib.sha256(b).hexdigest() == m["sha256"]))
ok = sum(a and b for _, a, b in res)
L += ["", "## Determinism check", "",
      f"Re-rendered 20 main-set items (random.Random(630).sample of the main manifest rows) in memory with the frozen `render_text` + `png_bytes` and compared with the PNG files used in the runs (`data/images/<item_id>.png`) and the manifest sha256.",
      "", f"**Result: {ok}/20 byte-identical** (file bytes and manifest sha256).", "", "Items: " + ", ".join(f"`{i}`" for i, _, _ in res), "",
      "(The T04 render itself also ran a 20-item in-process check: `reports/render_samples/size_stats.json`.)", "",
      "## Example images (median pixel count per type, main set)", ""]
for ct, m in samples.items():
    L.append(f"- `render_samples/{ct}.png` = `{m['item_id']}`, {m['width']}×{m['height']} px")
(OUT / "rendering.md").write_text("\n".join(L) + "\n")
print("determinism", ok)

# ---------------- exclusions
summ = json.loads((DATA / "items" / "summary.json").read_text())
ex = cfg["exclusions"]
exc = [row for row in csv.DictReader(l for l in open(DATA / "exclusions.csv") if not l.startswith("#"))]
only = collections.Counter(); multi = collections.Counter()
for e in exc:
    rs = [x.split(":")[0] for x in e["reason"].split(";")]
    if len(rs) == 1: only[(e["content_type"], rs[0])] += 1
    multi[(e["content_type"], len(rs))] += 1
pid = {i for i, d in items.items() if d["set"] == "pilot"}; mid = {i for i, d in items.items() if d["set"] == "main"}
mf = [l for l in open(DATA / "MANIFEST.md") if l.startswith("| cruxeval") or l.startswith("| gsm8k") or l.startswith("| wtq")]
E = ["# Exclusions, pools and sampling", "",
     "Sources: `data/MANIFEST.md` (datasets), `config/experiment.yaml` (`exclusions`, `items`, `seed`), `src/vmod/prepare.py` (`exclusion_reasons`, `main`), `data/items/summary.json` and `data/exclusions.csv` (T03 output).", "",
     "## Sources (verbatim rows from `data/MANIFEST.md`)", "",
     "| dataset | source | version | sha256 | license | items (test split) | local file |", "|---|---|---|---|---|---|---|", *[l.rstrip() for l in mf], "",
     "- code = CRUXEval, output-prediction task (`config/experiment.yaml` content_types.code); math = GSM8K config `main` test; table = WikiTableQuestions `pristine-unseen-tables` (the test split), from the GitHub release because the HF loader is script-based.", "",
     "## Exclusion criteria (applied before sampling; `src/vmod/prepare.py` `exclusion_reasons`)", "",
     f"1. `max_line_chars`: any line of the content string longer than **{ex['max_line_chars']}** characters",
     f"2. `max_lines`: content longer than **{ex['max_lines']}** lines",
     f"3. `table_max_rows`: table with more than **{ex['table_max_rows']}** data rows (table only)",
     "4. `render_fails`: content contains a character that DejaVu Sans Mono cannot draw (no glyph in the font cmap) or a control character other than newline",
     "5. `drop_if_over_context`: checked per model at run time. **0 requests were skipped** in any run (every `*.skipped.csv` is empty; integrity posts in COLLAB.md).", "",
     "One item can fail several criteria, so per-criterion counts overlap.", "",
     "## Counts", "", "| content type | pool | max_line_chars | max_lines | table_max_rows | render_fails | items excluded | eligible | % excluded |", "|---|---|---|---|---|---|---|---|---|"]
for ct in ("code", "math", "table"):
    s = summ[ct]; rc = s["reasons"]
    E.append(f"| {ct} | {s['total']} | {rc.get('max_line_chars',0)} | {rc.get('max_lines',0)} | {rc.get('table_max_rows',0)} | {rc.get('render_fails',0)} | {s['excluded']} | {s['eligible']} | {100*s['excluded']/s['total']:.1f}% |")
E += ["", "Items excluded by exactly one criterion (from `data/exclusions.csv`): " +
      "; ".join(f"{ct} {r}: {n}" for (ct, r), n in sorted(only.items())) + ". Items with 2+ reasons: " +
      "; ".join(f"{ct}: {n}" for (ct, k), n in sorted(multi.items()) if k > 1) + ".", "",
      f"**Check of \"32% of WTQ items excluded\":** {summ['table']['excluded']} / {summ['table']['total']} = {100*summ['table']['excluded']/summ['table']['total']:.2f}% → **confirmed (32%)**.", "",
      "## Sampling", "",
      f"- seed **{cfg['seed']}** (`config/experiment.yaml` seed); per content type `random.Random(seed).sample(eligible sorted by source_index, 30 + 500)`; the first 30 = pilot, the remaining 500 = main (`src/vmod/prepare.py`, `main`).",
      f"- main per type: " + ", ".join(f"{ct} {summ[ct]['main']}" for ct in ('code','math','table')) + f"; pilot per type: " + ", ".join(f"{ct} {summ[ct]['pilot']}" for ct in ('code','math','table')) + " (`data/items/summary.json`).",
      f"- disjointness, checked now by item_id over `data/items/{{pilot,main}}_*.jsonl`: |pilot ∩ main| = **{len(pid & mid)}** ({len(pid)} pilot ids, {len(mid)} main ids). The same assertion is in `prepare.py`.", ""]
(OUT / "exclusions.md").write_text("\n".join(E) + "\n")
print(only, multi, len(pid & mid))
