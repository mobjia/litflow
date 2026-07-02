"""Generate figure crop candidates for academic PDFs.

This script is a first-pass helper, not a perfect detector. It finds caption
blocks such as "Fig. 1", "Figure 2", "Scheme 1", or "Table 1" in the PDF text
layer, estimates a crop region containing the figure artwork, and writes
candidate PNGs plus a JSON manifest for QA.

Usage:
    python caption_anchor_crop.py paper.pdf output_dir Prefix
    python caption_anchor_crop.py paper.pdf output_dir Prefix --mode full-caption

Requires:
    pip install pymupdf
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import fitz  # pymupdf


CAPTION_RE = re.compile(
    r"^\s*(fig(?:ure)?\.?|scheme|table)\s*[\dA-Z]+[\.\:\s]",
    re.IGNORECASE,
)


@dataclass
class CropCandidate:
    figure_id: str
    page: int
    output: str
    caption: str
    mode: str
    top_pct: float
    bottom_pct: float
    left_pct: float
    right_pct: float
    source: str
    qa_flags: list[str]
    needs_qa: bool = True


def text_of_block(block: dict) -> str:
    parts: list[str] = []
    for line in block.get("lines", []):
        for span in line.get("spans", []):
            parts.append(span.get("text", ""))
    return " ".join("".join(parts).split())


def find_caption_blocks(page: fitz.Page) -> list[tuple[fitz.Rect, str]]:
    blocks = page.get_text("dict").get("blocks", [])
    captions: list[tuple[fitz.Rect, str]] = []
    for block in blocks:
        if block.get("type") != 0:
            continue
        text = text_of_block(block)
        if CAPTION_RE.search(text):
            captions.append((fitz.Rect(block["bbox"]), text))
    return captions


def image_like_blocks(page: fitz.Page) -> list[fitz.Rect]:
    rects: list[fitz.Rect] = []
    for block in page.get_text("dict").get("blocks", []):
        # type 1 catches raster image blocks; vector-only figures may not appear.
        if block.get("type") == 1:
            rects.append(fitz.Rect(block["bbox"]))
    drawings = page.get_drawings()
    for drawing in drawings:
        rect = drawing.get("rect")
        if rect and rect.width > 40 and rect.height > 25:
            rects.append(fitz.Rect(rect))
    return rects


def merge_rects(rects: Iterable[fitz.Rect]) -> fitz.Rect | None:
    rects = list(rects)
    if not rects:
        return None
    merged = fitz.Rect(rects[0])
    for rect in rects[1:]:
        merged.include_rect(rect)
    return merged


def page_visual_rect(page: fitz.Page) -> fitz.Rect | None:
    """Return the dominant visual area on a page, excluding page furniture."""
    page_rect = page.rect
    rects = []
    for rect in image_like_blocks(page):
        if rect.width < page_rect.width * 0.04 or rect.height < page_rect.height * 0.025:
            continue
        if rect.y1 < page_rect.height * 0.05 or rect.y0 > page_rect.height * 0.94:
            continue
        rects.append(rect)
    return merge_rects(rects)


def estimate_crop(
    doc: fitz.Document,
    page_index: int,
    caption_rect: fitz.Rect,
    mode: str,
) -> tuple[fitz.Page, fitz.Rect, str, list[str]]:
    page = doc[page_index]
    page_rect = page.rect
    flags: list[str] = []
    candidates = []
    for rect in image_like_blocks(page):
        # Prefer visual elements above the caption and horizontally overlapping it.
        overlaps_x = rect.x1 > caption_rect.x0 - 30 and rect.x0 < caption_rect.x1 + 30
        above_caption = rect.y0 < caption_rect.y0
        close_enough = caption_rect.y0 - rect.y1 < page_rect.height * 0.55
        if overlaps_x and above_caption and close_enough:
            candidates.append(rect)

    visual = merge_rects(candidates)
    source = "same_page"
    if visual is None:
        # Some journals put the artwork and caption on adjacent pages. Do not
        # crop the caption page as a fake figure.
        if caption_rect.y0 < page_rect.height * 0.25 and page_index > 0:
            linked_page = doc[page_index - 1]
            visual = page_visual_rect(linked_page)
            if visual is not None:
                page = linked_page
                page_rect = page.rect
                source = "previous_page_visual"
                flags.append("caption_on_next_page")
        elif caption_rect.y0 > page_rect.height * 0.62 and page_index + 1 < len(doc):
            linked_page = doc[page_index + 1]
            visual = page_visual_rect(linked_page)
            if visual is not None:
                page = linked_page
                page_rect = page.rect
                source = "next_page_visual"
                flags.append("caption_on_previous_page")

    if visual is None:
        # Last resort: generate a bounded candidate, but flag it loudly for QA.
        flags.append("no_visual_blocks_detected")
        visual = fitz.Rect(
            page_rect.width * 0.06,
            max(page_rect.height * 0.06, caption_rect.y0 - page_rect.height * 0.45),
            page_rect.width * 0.94,
            max(caption_rect.y0 - 4, page_rect.height * 0.12),
        )

    crop = fitz.Rect(visual)
    if mode == "full-caption" and source == "same_page":
        crop.include_rect(caption_rect)
    elif mode == "caption-lite" and source == "same_page":
        caption_lite = fitz.Rect(caption_rect)
        caption_lite.y1 = min(caption_lite.y1, caption_lite.y0 + page_rect.height * 0.07)
        crop.include_rect(caption_lite)

    pad_x = page_rect.width * 0.015
    pad_y = page_rect.height * 0.012
    crop.x0 = max(0, crop.x0 - pad_x)
    crop.x1 = min(page_rect.width, crop.x1 + pad_x)
    crop.y0 = max(0, crop.y0 - pad_y)
    crop.y1 = min(page_rect.height, crop.y1 + pad_y)

    area_ratio = (crop.width * crop.height) / (page_rect.width * page_rect.height)
    if area_ratio > 0.78:
        flags.append("large_crop_check_for_whole_page")
    if crop.y0 < page_rect.height * 0.05:
        flags.append("near_header_check")
    return page, crop, source, flags


def pct_rect(rect: fitz.Rect, page_rect: fitz.Rect) -> tuple[float, float, float, float]:
    return (
        round(rect.y0 / page_rect.height * 100, 2),
        round(rect.y1 / page_rect.height * 100, 2),
        round(rect.x0 / page_rect.width * 100, 2),
        round(rect.x1 / page_rect.width * 100, 2),
    )


def safe_figure_id(caption: str, fallback: str) -> str:
    match = re.search(r"(fig(?:ure)?\.?|scheme|table)\s*([\dA-Z]+)", caption, re.I)
    if not match:
        return fallback
    label = match.group(1).lower().replace("figure", "fig").replace(".", "")
    num = match.group(2)
    return f"{label}{num}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf_path")
    parser.add_argument("output_dir")
    parser.add_argument("prefix")
    parser.add_argument(
        "--mode",
        choices=["tight", "caption-lite", "full-caption"],
        default="tight",
        help="tight is the default for Obsidian/PPT reuse: figure artwork only.",
    )
    args = parser.parse_args()

    pdf_path = Path(args.pdf_path)
    output_dir = Path(args.output_dir)
    prefix = args.prefix
    output_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    manifest: list[CropCandidate] = []
    seen: dict[str, int] = {}

    for page_index in range(len(doc)):
        page = doc[page_index]
        for caption_rect, caption in find_caption_blocks(page):
            base_id = safe_figure_id(caption, f"fig{len(manifest) + 1}")
            seen[base_id] = seen.get(base_id, 0) + 1
            figure_id = base_id if seen[base_id] == 1 else f"{base_id}_{seen[base_id]}"
            crop_page, crop, source, flags = estimate_crop(doc, page_index, caption_rect, args.mode)
            top, bottom, left, right = pct_rect(crop, crop_page.rect)
            output_name = f"{prefix}_{figure_id}.png"
            pix = crop_page.get_pixmap(clip=crop, dpi=300)
            pix.save(output_dir / output_name)
            manifest.append(
                CropCandidate(
                    figure_id=figure_id,
                    page=crop_page.number + 1,
                    output=output_name,
                    caption=caption[:500],
                    mode=args.mode,
                    top_pct=top,
                    bottom_pct=bottom,
                    left_pct=left,
                    right_pct=right,
                    source=source,
                    qa_flags=flags,
                    needs_qa=True if flags else args.mode != "tight",
                )
            )

    manifest_path = output_dir / f"{prefix}_crop_manifest.json"
    manifest_path.write_text(
        json.dumps([asdict(item) for item in manifest], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Generated {len(manifest)} candidate crops")
    print(f"Manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


