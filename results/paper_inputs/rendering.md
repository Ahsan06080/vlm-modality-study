# Rendering

Sources: `config/experiment.yaml` (block `render:`), `src/vmod/render.py` (`render_text`, `png_bytes`), `src/vmod/prepare.py:16` (`FONT_PATH`).

## Settings (identical for all three content types)

| setting | value | source |
|---|---|---|
| font family | DejaVu Sans Mono | experiment.yaml render.font |
| font file | `/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf` | src/vmod/prepare.py:16 |
| font size | 20 px | render.font_size_px |
| line height | 1.3 × font size = 26 px line pitch | render.line_height; render.py `pitch = round(font_size_px * line_height)` |
| DPI / scale | none: 1 image pixel = 1 rendered pixel; image size = text extent + padding (no rescaling; image size = text extent + padding) | render.dpi_note |
| colour theme / syntax highlighting | no: single colour text, no highlighting | render.foreground / background; render.py draws all text with one fill |
| padding | 24 px on every side | render.padding_px |
| background / foreground | #FFFFFF / #000000 | render.background / foreground |
| max width | none; no wrapping at render time (`wrap: false`). Width is bounded by the exclusion rule max_line_chars = 160. Math text is word-wrapped once at 80 chars in the content string (the same string is used as text in A) | render.wrap; exclusions.max_line_chars; content_types.math.wrap_chars |
| image format | PNG, RGB, `PIL.Image.save(format='PNG', optimize=False)`; Pillow 13.0.0 | render.format; render.py `png_bytes` |
| layout | width = ceil(max line length in font advance units) + 2×padding; height = (n_lines−1)×pitch + ascent + descent + 2×padding | render.py `render_text` |

## Image sizes, main set (500 per type), from `data/images_manifest.csv`

| content type | n | width min / median / max (px) | height min / median / max (px) | megapixels min / median / max |
|---|---|---|---|---|
| code | 500 | 289 / 542 / 1301 | 150 / 228 / 410 | 0.058 / 0.126 / 0.308 |
| math | 500 | 916 / 1000 / 1012 | 98 / 124 / 280 | 0.090 / 0.125 / 0.283 |
| table | 500 | 567 / 1289 / 1976 | 306 / 514 / 1216 | 0.242 / 0.655 / 2.095 |

## Determinism check

Re-rendered 20 main-set items (random.Random(630).sample of the main manifest rows) in memory with the frozen `render_text` + `png_bytes` and compared with the PNG files used in the runs (`data/images/<item_id>.png`) and the manifest sha256.

**Result: 20/20 byte-identical** (file bytes and manifest sha256).

Items: `math-0248`, `code-sample_157`, `table-nu-3393`, `code-sample_699`, `table-nu-3836`, `math-0839`, `code-sample_43`, `math-0962`, `table-nu-4062`, `code-sample_285`, `math-0258`, `table-nu-2831`, `math-0715`, `table-nu-2760`, `code-sample_505`, `code-sample_689`, `code-sample_127`, `math-1072`, `math-0877`, `table-nu-1306`

(The T04 render itself also ran a 20-item in-process check: `reports/render_samples/size_stats.json`.)

## Example images (median pixel count per type, main set)

- `render_samples/code.png` = `code-sample_357`, 554×228 px
- `render_samples/math.png` = `math-0002`, 1012×124 px
- `render_samples/table.png` = `table-nu-2437`, 1711×384 px
