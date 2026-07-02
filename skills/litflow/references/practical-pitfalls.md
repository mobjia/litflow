# Practical Pitfalls

Use this reference before batch reading or figure-heavy PDF work. It contains generic operational cautions only; do not add user-specific reading logs, paper titles, author names, or private paths.

## File Naming

Some vision, OCR, and PDF tools are fragile when intermediate image paths contain spaces, non-ASCII characters, or punctuation.

Use stable ASCII prefixes for rendered pages and crops:

```python
papers = [
    (pdf_path_1, "PaperA2024"),
    (pdf_path_2, "PaperB2025"),
]
```

If two papers share a first-author surname, include year or a short title token in the prefix.

## Figure Selection

Review papers and long articles can produce many crop candidates. Do not embed everything.

Recommended selection:

- Conceptual schematic or research design.
- Main result or performance comparison.
- Mechanism, model, DFT/MD, or characterization figure.
- Summary table only when it carries key evidence.

Skip routine supplementary panels unless they are essential to the argument.

## Batch Processing

For multi-paper batches:

1. Triage every paper first.
2. Extract text and figures before note writing.
3. Deduplicate paper titles, concept names, people names, method notes, and innovation categories.
4. Keep current-paper processing lightweight; run historical backfill only when the user explicitly asks.

If subagents are used, the orchestrator remains responsible for verifying figure embeds, entity notes, method notes, and final file locations.

## Figure Cropping

Try `scripts/robust_pdf_figure_extract.py` first. It combines caption anchors, image blocks, vector drawings, table/figure direction rules, embedded-image inventory, and pixel-segment fallback.

If automatic cropping fails:

1. Render pages at a readable DPI.
2. Identify figure regions.
3. Crop conservatively.
4. Visually verify the final images.
5. Keep captions in Markdown when the caption is too long or separated from the artwork.

Reject final crops that are mostly page headers, body text, captions without artwork, or whole-page screenshots unless the full page is genuinely the figure.

## Dependency And Permission Cautions

Do not install Python packages, OCR engines, PDF tools, or plugins without user approval. If a dependency is missing, explain what it is used for and ask before installation.

## Output Hygiene

Before final delivery:

- Ensure every paper note embeds figures with `![[filename.png]]`.
- Ensure concept and people wikilinks have actual target files when they are required.
- Ensure method and innovation indexes do not create near-duplicate entries.
- Keep temporary files out of the user's vault unless the user asks to preserve them.
