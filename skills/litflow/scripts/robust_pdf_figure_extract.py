"""Robust first-pass figure and table extraction for academic PDFs.

This helper is built for LitFlow paper-reading notes. It does not pretend to
be a perfect PDF parser: it generates crop candidates, a manifest, and QA flags
so an agent can visually verify the final 3-5 figures before embedding them.

Usage:
    python robust_pdf_figure_extract.py paper.pdf output_dir Prefix
    python robust_pdf_figure_extract.py paper.pdf output_dir Prefix --mode caption-lite

Requires:
    pip install pymupdf pillow
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

try:
    import pymupdf as fitz
except ImportError:  # pragma: no cover - compatibility with older installs
    import fitz  # type: ignore


CAPTION_RE = re.compile(
    r"^\s*(?P<label>"
    r"extended\s+data\s+(?:fig(?:ure)?\.?|table)|"
    r"supplementary\s+(?:fig(?:ure)?\.?|table)|"
    r"fig(?:ure)?\.?|table|tab\.?|scheme|图|表"
    r")\s*(?P<num>[0-9]+[A-Za-z]?|[IVXLCDM]+)"
    r"(?:\s*[:：.\-|]|\s+|$)",
    re.IGNORECASE,
)


@dataclass
class Caption:
    figure_id: str
    kind: str
    page_index: int
    rect: fitz.Rect
    text: str


@dataclass
class CropRecord:
    figure_id: str
    kind: str
    page: int
    output: str
    caption: str
    mode: str
    top_pct: float
    bottom_pct: float
    left_pct: float
    right_pct: float
    area_ratio: float
    source: str
    qa_flags: list[str]
    needs_qa: bool = True


@dataclass
class EmbeddedImageRecord:
    page: int
    xref: int
    width: int | None
    height: int | None
    ext: str | None
    output: str | None


def text_of_block(block: dict) -> str:
    parts: list[str] = []
    for line in block.get("lines", []):
        for span in line.get("spans", []):
            parts.append(span.get("text", ""))
    return " ".join("".join(parts).split())


def normalize_kind(label: str) -> str:
    normalized = re.sub(r"\s+", " ", label.lower().replace(".", "")).strip()
    if normalized in {"table", "tab", "表"} or "table" in normalized:
        return "table"
    if normalized == "scheme":
        return "scheme"
    return "figure"


def figure_id(kind: str, label: str, number: str) -> str:
    normalized = re.sub(r"\s+", "_", label.lower().replace(".", "")).strip("_")
    if label in {"图"}:
        return f"fig{number}"
    if label in {"表"}:
        return f"table{number}"
    if normalized.startswith("extended_data"):
        prefix = "edtable" if kind == "table" else "edfig"
    elif normalized.startswith("supplementary"):
        prefix = "stable" if kind == "table" else "sfig"
    elif kind == "table":
        prefix = "table"
    elif kind == "scheme":
        prefix = "scheme"
    else:
        prefix = "fig"
    return f"{prefix}{number}"


def unique_id(base: str, seen: dict[str, int]) -> str:
    seen[base] = seen.get(base, 0) + 1
    return base if seen[base] == 1 else f"{base}_{seen[base]}"


def find_caption_blocks(page: fitz.Page, page_index: int, seen: dict[str, int]) -> list[Caption]:
    captions: list[Caption] = []
    for block in page.get_text("dict").get("blocks", []):
        if block.get("type") != 0:
            continue
        text = text_of_block(block)
        match = CAPTION_RE.match(text)
        if not match:
            continue
        label = match.group("label")
        number = match.group("num")
        kind = normalize_kind(label)
        base = figure_id(kind, label, number)
        captions.append(
            Caption(
                figure_id=unique_id(base, seen),
                kind=kind,
                page_index=page_index,
                rect=fitz.Rect(block["bbox"]),
                text=text,
            )
        )
    return captions


def visual_rects(page: fitz.Page) -> list[fitz.Rect]:
    page_rect = page.rect
    rects: list[fitz.Rect] = []
    for block in page.get_text("dict").get("blocks", []):
        if block.get("type") == 1:
            rect = fitz.Rect(block["bbox"])
            if useful_visual_rect(rect, page_rect):
                rects.append(rect)

    for drawing in page.get_drawings():
        rect = drawing.get("rect")
        if rect is None:
            continue
        candidate = fitz.Rect(rect)
        if useful_visual_rect(candidate, page_rect):
            rects.append(candidate)
    return rects


def useful_visual_rect(rect: fitz.Rect, page_rect: fitz.Rect) -> bool:
    if rect.width < 8 or rect.height < 8:
        return False
    if rect.width > page_rect.width * 0.96 and rect.height > page_rect.height * 0.9:
        return False
    if rect.y1 < page_rect.height * 0.045 or rect.y0 > page_rect.height * 0.955:
        return False
    return True


def merge_rects(rects: Iterable[fitz.Rect]) -> fitz.Rect | None:
    rects = list(rects)
    if not rects:
        return None
    merged = fitz.Rect(rects[0])
    for rect in rects[1:]:
        merged.include_rect(rect)
    return merged


def safety_zone(page: fitz.Page, cap: Caption, captions: list[Caption], completed: list[fitz.Rect]) -> fitz.Rect:
    page_w = page.rect.width
    page_h = page.rect.height
    cap_rect = cap.rect
    is_table = cap.kind == "table"
    left_x, right_x = 0.0, page_w
    top_y = cap_rect.y0 if is_table else 0.0
    bottom_y = page_h if is_table else cap_rect.y1

    for other in captions:
        if other is cap:
            continue
        other_rect = other.rect
        if abs(other_rect.y0 - cap_rect.y0) < 80:
            if other_rect.x0 < cap_rect.x0:
                left_x = max(left_x, (other_rect.x1 + cap_rect.x0) / 2)
            else:
                right_x = min(right_x, (cap_rect.x1 + other_rect.x0) / 2)
            continue

        cap_center = (cap_rect.x0 + cap_rect.x1) / 2
        other_center = (other_rect.x0 + other_rect.x1) / 2
        if abs(cap_center - other_center) < page_w * 0.35:
            if other_rect.y0 < cap_rect.y0:
                top_y = max(top_y, other_rect.y1)
            else:
                bottom_y = min(bottom_y, other_rect.y0)

    for crop in completed:
        crop_center = (crop.x0 + crop.x1) / 2
        cap_center = (cap_rect.x0 + cap_rect.x1) / 2
        if abs(crop_center - cap_center) < page_w * 0.35:
            if crop.y0 < cap_rect.y0:
                top_y = max(top_y, crop.y1)
            else:
                bottom_y = min(bottom_y, crop.y0)

    if bottom_y <= top_y:
        top_y, bottom_y = 0.0, page_h
    return fitz.Rect(left_x, top_y, right_x, bottom_y)


def rect_center(rect: fitz.Rect) -> tuple[float, float]:
    return ((rect.x0 + rect.x1) / 2, (rect.y0 + rect.y1) / 2)


def target_visuals(cap: Caption, zone: fitz.Rect, rects: list[fitz.Rect]) -> list[fitz.Rect]:
    cap_rect = cap.rect
    local: list[fitz.Rect] = []
    for rect in rects:
        cx, cy = rect_center(rect)
        if zone.x0 <= cx <= zone.x1 and zone.y0 <= cy <= zone.y1:
            local.append(rect)
    if not local:
        return []

    side: list[fitz.Rect] = []
    above: list[fitz.Rect] = []
    below: list[fitz.Rect] = []
    for rect in local:
        y_overlap = max(0, min(rect.y1, cap_rect.y1) - max(rect.y0, cap_rect.y0))
        if y_overlap > 5:
            side.append(rect)
        elif rect.y1 <= cap_rect.y0 + 18:
            above.append(rect)
        elif rect.y0 >= cap_rect.y1 - 18:
            below.append(rect)

    if cap.kind == "table":
        return (below + side) or local
    return (above + side) or local


def pixel_segment_fallback(page: fitz.Page, cap: Caption, zone: fitz.Rect) -> tuple[fitz.Rect | None, list[str]]:
    flags = ["pixel_segment_fallback"]
    try:
        from PIL import Image
    except ImportError:
        return None, flags + ["pillow_missing"]

    pix = page.get_pixmap(dpi=110, alpha=False)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples).convert("L")
    width, height = img.size
    pixels = img.load()
    rows: list[int] = []

    y0 = max(int(zone.y0 / page.rect.height * height), int(height * 0.05))
    y1 = min(int(zone.y1 / page.rect.height * height), int(height * 0.95))
    x0 = max(int(zone.x0 / page.rect.width * width), 0)
    x1 = min(int(zone.x1 / page.rect.width * width), width)
    if y1 <= y0 or x1 <= x0:
        return None, flags + ["bad_zone"]

    sample_step = max(1, (x1 - x0) // 260)
    for y in range(y0, y1):
        non_white = 0
        samples = 0
        for x in range(x0, x1, sample_step):
            samples += 1
            if pixels[x, y] < 235:
                non_white += 1
        if samples and non_white / samples > 0.018:
            rows.append(y)

    if not rows:
        return None, flags + ["no_non_white_rows"]

    segments: list[tuple[int, int]] = []
    start = rows[0]
    prev = rows[0]
    for row in rows[1:]:
        if row - prev > 12:
            segments.append((start, prev))
            start = row
        prev = row
    segments.append((start, prev))

    cap_y0 = cap.rect.y0 / page.rect.height * height
    cap_y1 = cap.rect.y1 / page.rect.height * height
    if cap.kind == "table":
        chosen = [seg for seg in segments if seg[1] >= cap_y0 - 8]
    else:
        chosen = [seg for seg in segments if seg[0] <= cap_y1 + 8]
    if not chosen:
        chosen = segments

    top = min(seg[0] for seg in chosen) / height * page.rect.height
    bottom = max(seg[1] for seg in chosen) / height * page.rect.height
    return fitz.Rect(zone.x0, top, zone.x1, bottom), flags


def estimate_crop(
    page: fitz.Page,
    cap: Caption,
    captions: list[Caption],
    completed: list[fitz.Rect],
    mode: str,
) -> tuple[fitz.Rect, str, list[str]]:
    page_rect = page.rect
    zone = safety_zone(page, cap, captions, completed)
    rects = visual_rects(page)
    visuals = target_visuals(cap, zone, rects)
    flags: list[str] = []
    source = "caption_visual_blocks"

    visual = merge_rects(visuals)
    if visual is None:
        visual, fallback_flags = pixel_segment_fallback(page, cap, zone)
        flags.extend(fallback_flags)
        source = "pixel_segment"

    if visual is None:
        flags.append("no_visual_region_detected")
        if cap.kind == "table":
            visual = fitz.Rect(zone.x0, cap.rect.y0, zone.x1, min(page_rect.height, cap.rect.y1 + page_rect.height * 0.35))
        else:
            visual = fitz.Rect(zone.x0, max(0, cap.rect.y0 - page_rect.height * 0.35), zone.x1, cap.rect.y1)

    crop = fitz.Rect(visual)
    if mode == "full-caption":
        crop.include_rect(cap.rect)
    elif mode == "caption-lite":
        lite = fitz.Rect(cap.rect)
        lite.y1 = min(lite.y1, lite.y0 + page_rect.height * 0.075)
        crop.include_rect(lite)

    pad_x = page_rect.width * 0.018
    pad_y = page_rect.height * 0.014
    crop.x0 = max(zone.x0, crop.x0 - pad_x)
    crop.x1 = min(zone.x1, crop.x1 + pad_x)
    crop.y0 = max(0, crop.y0 - pad_y)
    crop.y1 = min(page_rect.height, crop.y1 + pad_y)

    area_ratio = crop.width * crop.height / (page_rect.width * page_rect.height)
    if area_ratio > 0.65:
        flags.append("large_crop_check_for_whole_page")
    if crop.y0 < page_rect.height * 0.045:
        flags.append("near_header_check")
    if crop.height < page_rect.height * 0.035:
        flags.append("very_short_crop_check")
    return crop, source, flags


def pct_rect(rect: fitz.Rect, page_rect: fitz.Rect) -> tuple[float, float, float, float]:
    return (
        round(rect.y0 / page_rect.height * 100, 2),
        round(rect.y1 / page_rect.height * 100, 2),
        round(rect.x0 / page_rect.width * 100, 2),
        round(rect.x1 / page_rect.width * 100, 2),
    )


def embedded_images(doc: fitz.Document, output_dir: Path, prefix: str, save: bool) -> list[EmbeddedImageRecord]:
    records: list[EmbeddedImageRecord] = []
    seen_xrefs: set[int] = set()
    for page_index in range(len(doc)):
        page = doc[page_index]
        for image in page.get_images(full=True):
            xref = image[0]
            if xref in seen_xrefs:
                continue
            seen_xrefs.add(xref)
            width = image[2] if len(image) > 2 else None
            height = image[3] if len(image) > 3 else None
            output_name = None
            ext = None
            if save:
                data = doc.extract_image(xref)
                ext = data.get("ext", "bin")
                output_name = f"{prefix}_embedded_xref{xref}.{ext}"
                (output_dir / output_name).write_bytes(data["image"])
            records.append(
                EmbeddedImageRecord(
                    page=page_index + 1,
                    xref=xref,
                    width=width,
                    height=height,
                    ext=ext,
                    output=output_name,
                )
            )
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf_path")
    parser.add_argument("output_dir")
    parser.add_argument("prefix")
    parser.add_argument(
        "--mode",
        choices=["tight", "caption-lite", "full-caption"],
        default="tight",
        help="tight saves artwork/table body only; caption-lite includes the label and first caption lines.",
    )
    parser.add_argument("--dpi", type=int, default=300)
    parser.add_argument("--save-embedded", action="store_true")
    args = parser.parse_args()

    pdf_path = Path(args.pdf_path)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    seen: dict[str, int] = {}
    all_captions: dict[int, list[Caption]] = {}
    for page_index in range(len(doc)):
        captions = find_caption_blocks(doc[page_index], page_index, seen)
        all_captions[page_index] = sorted(captions, key=lambda item: (item.rect.y0, item.rect.x0))

    crop_records: list[CropRecord] = []
    for page_index in range(len(doc)):
        page = doc[page_index]
        completed: list[fitz.Rect] = []
        captions = all_captions[page_index]
        for cap in captions:
            crop, source, flags = estimate_crop(page, cap, captions, completed, args.mode)
            completed.append(crop)
            top, bottom, left, right = pct_rect(crop, page.rect)
            output_name = f"{args.prefix}_{cap.figure_id}.png"
            pix = page.get_pixmap(clip=crop, dpi=args.dpi, alpha=False)
            pix.save(output_dir / output_name)
            area_ratio = round(crop.width * crop.height / (page.rect.width * page.rect.height), 4)
            crop_records.append(
                CropRecord(
                    figure_id=cap.figure_id,
                    kind=cap.kind,
                    page=page.number + 1,
                    output=output_name,
                    caption=cap.text[:700],
                    mode=args.mode,
                    top_pct=top,
                    bottom_pct=bottom,
                    left_pct=left,
                    right_pct=right,
                    area_ratio=area_ratio,
                    source=source,
                    qa_flags=flags,
                    needs_qa=True,
                )
            )

    embedded = embedded_images(doc, output_dir, args.prefix, args.save_embedded)
    manifest = {
        "pdf": str(pdf_path),
        "prefix": args.prefix,
        "mode": args.mode,
        "dpi": args.dpi,
        "crops": [asdict(item) for item in crop_records],
        "embedded_images": [asdict(item) for item in embedded],
        "notes": [
            "Candidate crops require visual QA before embedding in Obsidian notes.",
            "Use embedded_images as raw-image inventory, not as a substitute for complete figure/table crops.",
        ],
    }
    manifest_path = output_dir / f"{args.prefix}_robust_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    doc.close()
    print(f"Generated {len(crop_records)} crop candidates")
    print(f"Embedded image records: {len(embedded)}")
    print(f"Manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


