# PDF Image Workflow

Use this reference when a paper note needs figures or when existing figure extraction fails.

## Rule

Crop individual figures by default in `tight` mode: include the figure body, panel labels, axes, legends, scale bars, and in-figure annotations. Do not include surrounding正文段落, page headers/footers, references, or unrelated table text.

Use `full-caption` only when the caption is directly attached to the figure and can be included without body text. For Obsidian/PPT reuse, prefer `tight` crops and write the figure interpretation in Markdown.

Never accept whole-page screenshots as final figures unless the page itself is a full-page figure with no surrounding正文. Same-sized "figure" PNGs that match page dimensions are suspect and must be recropped.

## Preferred Method: Robust Hybrid Extraction

**MANDATORY: Try `robust_pdf_figure_extract.py` FIRST. Do NOT skip to manual vision-based cropping.**

In real sessions, manually guessing percentage coordinates from `vision_analyze` took 5+ rounds of re-cropping per paper (vision gives coordinates off by 10-20%). The script does it in one pass for most raster-based PDFs.

Workflow:

1. **Run `scripts/robust_pdf_figure_extract.py`** — this is step 1, not optional.
2. Review the generated crop manifest and candidate PNGs.
3. Visually QA 2-3 crops per paper with `vision_analyze`.
4. Keep good crops, adjust bad crops with percentage coordinates, then rerun cropping.
5. Final crop must include the complete figure body, with no unrelated正文. Add the interpretation below the image in Markdown.

Example:

```bash
python scripts/robust_pdf_figure_extract.py paper.pdf <OBSIDIAN_VAULT>\99-Attachments FirstAuthor2026 --mode tight
python scripts/robust_pdf_figure_extract.py paper.pdf <OBSIDIAN_VAULT>\99-Attachments FirstAuthor2026 --mode caption-lite
```

Use `--save-embedded` only when you also want raw embedded image objects for inspection. These raw objects are not automatically complete figures; they often miss vector labels, axes, legends, captions, or multi-panel context.

**Only fall back to manual vision + percentage coordinates when:**
- The script produces empty/broken output (vector-heavy PDFs)
- Figures are split across pages
- The crop clearly misses the figure body

Why this works better:

- Captions locate the numbered figure and its page relationship.
- The final image remains reusable for Obsidian and PPT because it is not polluted by正文.
- It reduces the common failure where the crop includes the next body paragraph or an entire text page.

Use manual percentage cropping only after the robust candidate is visibly wrong.

Read `advanced-pdf-figure-extraction.md` for the decision tree behind the robust extractor, external alternatives, and failure-mode triage.

## Crop Modes

Use these modes deliberately:

- `tight`: figure body only, including panel labels, axes, legends, and scale bars. This is the default.
- `caption-lite`: figure body plus figure number/title and the first 1-2 caption lines.
- `full-caption`: figure body plus complete caption. Use only when it does not pull in正文.

In `full-caption`, the lower crop boundary should stop at the end of the figure caption. Do not extend into the next正文段落, section heading, author contribution note, or reference block.

If the caption is on an adjacent page, crop the artwork page in `tight` mode and keep the caption/interpretation as Markdown text. Do not stitch caption-only pages into the image.

## Render Pages

Render body pages to PNG at 250-300 dpi. Prefer writing a small local script and running it with Python so long commands do not become brittle.

```python
import pymupdf, os

pdf_path = r"path\\to\\paper.pdf"
output_dir = r"<OBSIDIAN_VAULT>\\99-Attachments"
prefix = "FirstAuthor_Year"
os.makedirs(output_dir, exist_ok=True)
doc = pymupdf.open(pdf_path)
for page_num in range(max(0, len(doc) - 2)):
    pix = doc[page_num].get_pixmap(dpi=250)
    pix.save(os.path.join(output_dir, f"{prefix}_p{page_num + 1}.png"))
doc.close()
print(f"Rendered {page_num + 1} pages")
```

**Pattern:** save the snippet as a temporary script in the workspace, run it with Python, then delete or ignore the temporary file after QA.

## Pick Figures

Choose 3-5 figures:

1. Schematic or conceptual design
2. Main performance/result figure
3. Mechanism/model/simulation figure
4. Comparison figure or important table

Avoid routine supplementary plots unless they are central to the argument.

## Determine Crop Coordinates

Inspect rendered pages visually. Record crop boxes as percentages:

```text
output_name, source_page, top%, bottom%, left%, right%
Author_2026_Fig1.png, Author_2026_p2.png, 5, 68, 3, 97
```

Percentage coordinates are preferred over pixels because page sizes vary across PDFs.

Default to `tight`: include the complete visual body, then stop. Do not use a fixed `bottom% + 10-15%` rule; it often captures正文. If using `caption-lite` or `full-caption`, identify the caption block:

- It usually starts with `Fig.`, `Figure`, `Table`, or a bold figure number.
- It ends before the next normal正文 paragraph, next section heading, next figure/table, or page footer.
- If the caption is in smaller font, include all small-font caption lines but stop when normal body text resumes.
- If a crop includes more than one unrelated正文 paragraph, tighten it.
- If a crop exceeds 75% of the page height, verify it is truly a full-page figure plus caption.

For journals that split artwork and captions across pages:

- Caption at top of page + no figure above it: inspect the previous page for the artwork.
- Caption at bottom of page + no figure above it: inspect the next page for the artwork.
- Save the artwork as `*_clean.png` or `*_tight.png`; keep caption details in the note.

## QA Checklist

Accept a crop only when:

- The visual body is complete: all panels, axes, legends, scale bars, and labels are visible.
- The image is a clean figure crop. The full original caption is optional and should be in the image only when it does not drag in正文.
- No unrelated正文 paragraph is included below or above the caption.
- Neighboring figures/tables are not included unless they are part of the same numbered figure.
- Page header, footer, and references are excluded.
- Text remains readable at normal Obsidian width.

Reject and recrop when:

- More than 15-20% of the crop height is unrelated whitespace/body text.
- The caption continues below the crop.
- The crop cuts off panel labels, legends, or axis labels.
- A multi-panel figure is split in a way that loses the caption's meaning.
- A set of exported figures all have identical page-like dimensions.
- The "figure" contains mostly two-column正文 and only a small or missing visual block.

## Crop Figures

```python
import os
import pymupdf

output_dir = r"<OBSIDIAN_VAULT>\99-Attachments"
crops = [
    # (source, destination, top, bottom, left, right)
    ("Author_2026_p2.png", "Author_2026_Fig1.png", 5, 68, 3, 97),
]

for src, dst, top, bottom, left, right in crops:
    doc = pymupdf.open(os.path.join(output_dir, src))
    page = doc[0]
    w, h = page.rect.width, page.rect.height
    rect = pymupdf.Rect(w * left / 100, h * top / 100, w * right / 100, h * bottom / 100)
    pix = page.get_pixmap(clip=rect, dpi=300)
    pix.save(os.path.join(output_dir, dst))
```

## Embed in Markdown

```markdown
### Fig 1 - Mechanism schematic
![[Author_2026_Fig1.png]]
> 图注说明：这张图展示了作者的核心机制假设，以及它如何支撑后续实验设计。
```

## Cleanup

After confirming notes reference only cropped figures, remove temporary page renders if desired. Do not delete source PDFs or final cropped figures.


