from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from PIL import Image, ImageDraw, ImageFont

CoverVariant = Literal["overshirt-standing", "table-knit", "jacket-relaxed"]

CANVAS_SIZE = (1200, 630)
TITLE_BOX = (665, 96, 1120, 510)
BRAND_TEXT = "nasuta.ru"
BACKGROUND_NAMES: dict[CoverVariant, str] = {
    "overshirt-standing": "overshirt-standing.jpg",
    "table-knit": "table-knit.jpg",
    "jacket-relaxed": "jacket-relaxed.jpg",
}


@dataclass(frozen=True)
class CoverRequest:
    slug: str
    title: str
    variant: CoverVariant
    output_path: Path
    material_label: str = "СТАТЬЯ"


def _font_path() -> str:
    return "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def _sans_font_path() -> str:
    return "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def _wrap_title(draw: ImageDraw.ImageDraw, title: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = title.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if draw.textlength(candidate, font=font) <= max_width:
            current = candidate
            continue
        if not current:
            raise ValueError(f"Word is too wide for the title field: {word}")
        lines.append(current)
        current = word
    if current:
        lines.append(current)
    return lines


def _title_font(draw: ImageDraw.ImageDraw, title: str, max_width: int, max_height: int) -> tuple[ImageFont.FreeTypeFont, list[str]]:
    for size in range(52, 30, -1):
        font = ImageFont.truetype(_font_path(), size)
        lines = _wrap_title(draw, title, font, max_width)
        line_height = int(size * 1.22)
        if len(lines) * line_height <= max_height:
            return font, lines
    raise ValueError("Title cannot fit in the protected title field")


def validate_cover(path: Path) -> None:
    with Image.open(path) as image:
        if image.size != CANVAS_SIZE:
            raise ValueError(f"Expected {CANVAS_SIZE}, got {image.size}")
        if image.format != "JPEG":
            raise ValueError(f"Expected JPEG, got {image.format}")


def render_cover(request: CoverRequest, root: Path) -> Path:
    source = root / "assets" / "images" / "article-cover-sources" / BACKGROUND_NAMES[request.variant]
    if not source.is_file():
        raise FileNotFoundError(source)
    image = Image.open(source).convert("RGB").resize(CANVAS_SIZE, Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(image)
    left, top, right, bottom = TITLE_BOX
    max_width = right - left
    max_height = bottom - top
    label_font = ImageFont.truetype(_sans_font_path(), 16)
    title_font, lines = _title_font(draw, request.title, max_width, max_height - 46)
    navy = "#10263A"
    teal = "#0A7F8B"
    draw.text((left, 58), request.material_label, font=label_font, fill=teal)
    y = top
    line_height = int(title_font.size * 1.22)
    for line in lines:
        draw.text((left, y), line, font=title_font, fill=navy)
        y += line_height
    brand_font = ImageFont.truetype(_sans_font_path(), 16)
    draw.text((right, 582), BRAND_TEXT, font=brand_font, fill=navy, anchor="ra")
    request.output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(request.output_path, "JPEG", quality=92, optimize=True)
    validate_cover(request.output_path)
    return request.output_path
