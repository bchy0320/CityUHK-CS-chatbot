"""Content-image handling: locate, download, and OCR meaningful images.

CityU pages embed a lot of decorative images (logos, icons, social buttons,
news thumbnails) that carry no admission information. This module focuses on
*content* images — diagrams, flowcharts, curriculum maps, and infographics —
whose text is not present in the page's HTML.

Pipeline:
  1. Parse the HTML for <img> tags and keep only "content" candidates
     (skip logos, icons, social buttons, and tiny/background images).
  2. Resolve each candidate to an absolute URL using the page's base URL.
  3. Download the image with browser-like headers (CityU blocks the default
     httpx User-Agent and requires the correct host).
  4. Describe the image: prefer the vision model (see vision.py) for a
       structured, semantic description; fall back to RapidOCR for raw text.

  The description is appended to the extracted Markdown so downstream note
  generation can use it. Nothing is rewritten: the output is verbatim.
  """
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

import httpx

from . import vision

# Image extensions we can OCR. SVG is vector (no raster text) and is skipped.
_RASTER_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tif", ".tiff"}

# Substrings that mark an image as decorative rather than content-bearing.
_DECORATIVE_MARKERS = (
    "logo",
    "icon",
    "icons",
    "social",
    "facebook",
    "youtube",
    "twitter",
    "linkedin",
    "instagram",
    "navbar",
    "footer",
    "banner",
    "background",
    "bg.",
    "arrow",
    "qm.png",
    "search",
    "toggler",
    "item_bg",
    "event_arrow",
    "arrow_prev",
    "arrow_next",
    "cup.jpg",
    "vpn.png",
    "cstour.png",
    "bsccs_game.jpg",
    "menu-img",           # navigation menu thumbnails
    "istock",             # stock photo placeholders
    "programme-default",  # default programme placeholder
    "header/",            # page-header imagery
    "themes/custom",      # theme assets (menus, headers)
)

# CSS class substrings that mark an image as a navigation/decoration card
# rather than a content-bearing diagram. CityU's Sitecore theme uses
# "image-style-crop-*" for intro tiles, section headers, and news thumbnails,
# and "card-img" for staff/student photo cards. These carry no admission info.
_DECORATIVE_CLASS_MARKERS = (
    "image-style-crop-",   # intro tiles, section headers, news thumbnails
    "card-img",            # staff/student photo cards
    "menu-img",            # navigation menu thumbnails
    "news-block",          # news thumbnail images
)

# Minimum dimensions (px) for a content image. Tiny images are icons/decoration.
_MIN_WIDTH = 120
_MIN_HEIGHT = 80


def _is_content_image(src: str, alt: str, width: int, height: int, css_class: str = "") -> bool:
    """Return True if an image looks like it carries content rather than decoration."""
    if not src:
        return False
    ext = Path(urlparse(src).path).suffix.lower()
    if ext not in _RASTER_EXT:
        return False
    if width and width < _MIN_WIDTH:
        return False
    if height and height < _MIN_HEIGHT:
        return False
    low = f"{src} {alt}".lower()
    if any(marker in low for marker in _DECORATIVE_MARKERS):
        return False
    # Skip navigation/decoration cards identified by their CSS class.
    low_class = css_class.lower()
    if any(marker in low_class for marker in _DECORATIVE_CLASS_MARKERS):
        return False
    return True


def find_content_images(html: str, base_url: str) -> list[str]:
    """Return absolute URLs of content-bearing images found in an HTML document.

    Uses the page's own <img> tags. Width/height are read from the tag's
    width/height attributes when present; otherwise the image is kept as a
    candidate (we cannot know its real size without downloading).
    """
    candidates: list[str] = []
    for m in re.finditer(r"<img\b[^>]*>", html, re.IGNORECASE):
        tag = m.group(0)
        src_m = re.search(r'src\s*=\s*["\']([^"\']+)["\']', tag, re.IGNORECASE)
        if not src_m:
            continue
        src = src_m.group(1)
        # HTML entities in attribute values (e.g. &amp;) must be decoded so the
        # URL is valid for an HTTP request.
        src = src.replace("&amp;", "&")
        alt_m = re.search(r'alt\s*=\s*["\']([^"\']*)["\']', tag, re.IGNORECASE)
        alt = alt_m.group(1) if alt_m else ""
        class_m = re.search(r'class\s*=\s*["\']([^"\']*)["\']', tag, re.IGNORECASE)
        css_class = class_m.group(1) if class_m else ""
        width = _attr_int(tag, "width")
        height = _attr_int(tag, "height")
        if _is_content_image(src, alt, width, height, css_class):
            candidates.append(urljoin(base_url, src))
    # De-duplicate while preserving order.
    seen: set[str] = set()
    unique: list[str] = []
    for url in candidates:
        if url not in seen:
            seen.add(url)
            unique.append(url)
    return unique


def _attr_int(tag: str, name: str) -> int:
    m = re.search(rf'{name}\s*=\s*["\']?(\d+)', tag, re.IGNORECASE)
    return int(m.group(1)) if m else 0


def download_image(url: str, dest: Path, headers: dict[str, str]) -> bool:
    """Download an image to dest. Returns True on success."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        with httpx.Client(
            timeout=30,
            headers={
                "User-Agent": headers.get("User-Agent", "Mozilla/5.0"),
                "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": headers.get("Referer", ""),
            },
            follow_redirects=True,
        ) as client:
            resp = client.get(url)
            resp.raise_for_status()
            ctype = resp.headers.get("content-type", "").lower()
            if "image" not in ctype:
                return False
            dest.write_bytes(resp.content)
            return True
    except httpx.HTTPError:
        return False


def ocr_image(path: Path) -> str:
    """OCR an image with RapidOCR and return recognized text lines."""
    try:
        from rapidocr_onnxruntime import RapidOCR
    except ImportError:
        return ""

    engine = getattr(ocr_image, "_engine", None)
    if engine is None:
        engine = RapidOCR()
        ocr_image._engine = engine

    result, _ = engine(str(path))
    if not result:
        return ""
    lines = [line[1] for line in result if len(line) > 1 and line[1]]
    return "\n".join(lines).strip()


def process_images(
    html: str,
    base_url: str,
    raw_dir: Path,
    headers: dict[str, str],
    max_images: int = 5,
    use_vision: bool = True,
) -> tuple[str, str]:
    """Download content images from an HTML page and describe them.

    When a vision API key is configured (see vision.py), each content image is
    sent to the vision model for a structured, semantic description (phases,
    branches, relationships). Otherwise, or on failure, the image is OCR'd as a
    fallback so raw text is still captured.

    Returns a tuple ``(markdown, method)`` where ``method`` is ``"vision"`` or
    ``"ocr"``, or ``("", "")`` if there are no content images. Images are saved
    under raw_dir/images/ so the raw capture is self-contained.
    """
    urls = find_content_images(html, base_url)
    if not urls:
        return "", ""

    img_dir = raw_dir / "images"
    downloaded: list[Path] = []
    for i, url in enumerate(urls[:max_images]):
        ext = Path(urlparse(url).path).suffix.lower() or ".png"
        dest = img_dir / f"image-{i + 1}{ext}"
        if download_image(url, dest, headers):
            downloaded.append(dest)

    if not downloaded:
        return "", ""

    # Prefer the vision model when configured; fall back to OCR per image.
    if use_vision and vision.is_configured():
        blocks, saw_any = _describe_with_vision(downloaded)
        if blocks:
            return "\n\n".join(blocks), "vision"
        # The vision model ran and judged every image decorative (or found no
        # informative content). Don't fall back to OCR ? decorative images
        # would produce noise. Only fall back if the vision call itself failed.
        if saw_any:
            return "", ""
        # Vision was configured but the call failed (network/API error).
        # Fall back to OCR so content is still captured.

    # OCR fallback (also used when vision is disabled or unavailable).
    blocks = _describe_with_ocr(downloaded)
    if not blocks:
        return "", ""
    return "\n\n".join(blocks), "ocr"


def _describe_with_vision(image_paths: list[Path]) -> tuple[list[str], bool]:
    """Describe images with the vision model.

    Returns a tuple ``(blocks, saw_any)`` where ``blocks`` is a list of
    Markdown blocks for informative images and ``saw_any`` is True if the model
    processed at least one image (whether or not it was informative).
    """
    from .vision import process_images_vision

    text, saw_any = process_images_vision(image_paths)
    if not text:
        return [], saw_any
    # process_images_vision already returns "### Image N\n\n..." blocks joined
    # with blank lines. Return the whole string as a single block so the model's
    # own Markdown headings (e.g. "### Phase 1") are not split apart.
    return [text], saw_any


def _describe_with_ocr(image_paths: list[Path]) -> list[str]:
    """OCR images with RapidOCR. Returns a list of Markdown blocks."""
    blocks: list[str] = []
    for i, dest in enumerate(image_paths):
        text = ocr_image(dest)
        if not text:
            continue
        # Drop OCR results that are too short or look like noise (e.g. a logo
        # fragment or mojibake). Content images yield several meaningful lines.
        if len(text.strip()) < 20:
            continue
        blocks.append(f"### Image {i + 1}\n\n{text}")
    return blocks
