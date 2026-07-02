# Advanced PDF Figure Extraction

Use this reference when figure extraction quality matters, auto-crop fails, or a paper contains vector-heavy diagrams, dense tables, Chinese captions, Extended Data, Supplementary figures, or Article-in-Press page furniture.

## Mental Model

PDF "image extraction" means three different things:

| Need | Best method | Output |
|---|---|---|
| Preserve raw embedded bitmap objects | `Page.get_images()` / `Document.extract_image()` / `pdfimages` | Original image files, often incomplete for scientific figures |
| Save reusable paper figures/tables | Caption-anchored page-region crop | Complete visual area with panels, axes, legends, labels |
| Recover vector/scanned/complex layouts | Render page, segment non-white visual regions, then crop | Screenshot crop candidate requiring QA |

For literature notes, prefer complete figure/table crops over raw embedded images. Raw objects are useful evidence but often omit vector labels, legends, axes, panel letters, and table text.

## Default Local Workflow

1. Run:

```bash
python scripts/robust_pdf_figure_extract.py paper.pdf <OBSIDIAN_VAULT>\99-Attachments Prefix --mode tight
```

2. Open `Prefix_robust_manifest.json`.
3. Review `crops`: pick the 3-5 figures/tables most central to the paper.
4. Visually inspect at least 2-3 crop PNGs before writing the note.
5. Recrop any candidate with QA flags such as `large_crop_check_for_whole_page`, `near_header_check`, `pixel_segment_fallback`, or `no_visual_region_detected`.

Use `--mode caption-lite` when the crop should include the figure number/title line. Use `--mode full-caption` rarely; it often pollutes reusable images with正文.

Use `--save-embedded` when diagnosing missing figures or when the user explicitly wants original image objects:

```bash
python scripts/robust_pdf_figure_extract.py paper.pdf out Prefix --save-embedded
```

## What The Robust Extractor Does

- Finds captions with `Figure/Fig/Table/Tab/Scheme`, `Extended Data`, `Supplementary`, and Chinese `图/表`.
- Treats figures/schemes as usually above captions and tables as usually below captions.
- Builds same-row "caption walls" so side-by-side figures do not merge.
- Uses previous completed crops as blockers to avoid overlapping crops.
- Includes raster image blocks and vector drawing rectangles.
- Falls back to rendered-page non-white row segmentation when no visual PDF blocks are detected.
- Writes a JSON manifest with crop coordinates, page numbers, captions, source mode, area ratio, embedded-image inventory, and QA flags.

## Failure Triage

| Symptom | Likely cause | Next action |
|---|---|---|
| Crop is a whole page | Figure spans much of page or text got merged | Tighten crop by percentage coordinates; reject if mostly正文 |
| Crop has only header/caption | Vector drawing not detected or caption split | Use manual fallback: render page, identify visual region, crop |
| Raw embedded images look like fragments | Figure is vector/text composite | Use page-region crop, not raw image extraction |
| Table missed | Table is text-only without drawing lines | Crop from caption downward; use `caption-lite` if table title matters |
| Chinese figures missed | Caption text not selectable or OCR needed | Render page and use manual/vision workflow; consider PaddleOCR |
| Same figure repeated | Duplicate caption or cross-page caption | Check manifest `page`, `caption`, and `source`; keep only the correct crop |

## External Tools Worth Considering

Use these only when local PyMuPDF workflows are not enough:

- **PDFFigures2**: scholarly PDF figures/tables/captions; useful baseline for English papers.
- **GROBID**: TEI extraction with figure/table coordinates; good when metadata and structure also matter.
- **Docling**: modern PDF-to-Markdown/JSON pipeline for layout, tables, images, reading order, OCR.
- **PaddleOCR PP-Structure**: stronger for Chinese/scanned/complex layout pages.
- **Adobe PDF Extract API**: commercial cloud option; use only with user approval and privacy review.

Do not silently upload unpublished PDFs or private manuscripts to cloud APIs.

## QA Rules

Accept only crops that contain the complete visual evidence: all panels, axes, labels, legends, scale bars, and table body. Reject crops dominated by body text, page headers/footers, references, or whitespace.

For Obsidian notes, keep the image clean and write interpretation below:

```markdown
### Fig 2 - Mechanism validation
![[Prefix_fig2.png]]
> [!note] 图表解读
> 这张图说明...
```


