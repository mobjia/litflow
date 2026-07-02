# Manual Crop Fallback

Use when `robust_pdf_figure_extract.py` produces bad crops (e.g., only page headers or caption labels without figure content). This happens with vector-only PDFs, scanned pages, table-as-text layouts, or figures split across pages.

## Detection

Run `robust_pdf_figure_extract.py` first. If the output crops show:
- Only page header/footer text
- Only "Figure X" labels without actual content
- Blank areas or text columns instead of figures

→ Fall back to manual workflow.

## Manual Workflow

### Step 1: Render pages at 200 dpi

```python
import pymupdf
doc = pymupdf.open("paper.pdf")
for i in range(len(doc) - 1):  # skip last page (references)
    pix = doc[i].get_pixmap(dpi=200)
    pix.save(f"temp_page_{i+1}.png")
```

### Step 2: Vision-based figure identification

Use `vision_analyze` on each rendered page. For each page ask:
"Identify ALL figures on this page. For each, give crop coordinates as percentages: top%, bottom%, left%, right%."

Vision models can see the rendered PNG and identify figure boundaries accurately, even for vector figures that pymupdf's text-layer analysis misses.

### Step 3: Crop with pymupdf using percentage coordinates

```python
import pymupdf
doc = pymupdf.open("temp_page_3.png")  # the rendered PNG
page = doc[0]
w, h = page.rect.width, page.rect.height
rect = pymupdf.Rect(
    w * left_pct / 100,
    h * top_pct / 100,
    w * right_pct / 100,
    h * bottom_pct / 100
)
pix = page.get_pixmap(clip=rect, dpi=300)
pix.save("output_figure.png")
```

### Step 4: QA the crop

Load the output with `vision_analyze` and ask:
"Does this cropped figure contain the complete figure body with all panels, labels, axes, legends, and scale bars? Is anything cut off? Does it include any unrelated body text?"

For Obsidian/PPT reuse, prefer figure-body-only crops. If caption text bleeds in from adjacent paragraphs, tighten the bottom boundary by 2-3% and keep the explanation in Markdown.

### Step 5: Clean up temp renders

Delete all `temp_page_*.png` files after final crops are verified.

## Tips

- Render at 200 dpi for identification, crop at 300 dpi for final output
- Include the caption in the crop only when it is directly attached and does not bring in body text
- For review papers with many figures, process page by page systematically
- If a figure spans two pages, crop each page separately and embed both


