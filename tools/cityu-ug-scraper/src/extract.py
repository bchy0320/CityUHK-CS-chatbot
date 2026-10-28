"""Extract stage: HTML/PDF -> clean Markdown main text.

Uses trafilatura for HTML (preserves tables, drops nav/boilerplate) and
pymupdf for PDFs. The output is an *extraction*, not a rewrite: numbers,
dates, and official wording are preserved verbatim.

Content images (diagrams, flowcharts, curriculum maps) are downloaded and
described — via the vision model when a key is configured, otherwise via OCR —
so their embedded information is captured too. See images.py and vision.py.
"""
from __future__ import annotations

import re
from pathlib import Path

import trafilatura

from .charts import extract_charts
from .fetch import FetchResult
from .images import process_images

# Accordion/collapsible section headings live in <div class="normal" role="button">.
# trafilatura drops role="button" elements, so the heading labels are lost even
# though the (collapsed) content below is kept. Convert them to <h3> so the
# section structure survives extraction.
_ACCORDION_HEADING_RE = re.compile(
    r'<div class="normal" role="button"[^>]*>\s*(.*?)\s*</div>', re.DOTALL
)


def _preprocess_html(html: str) -> str:
    """Normalize HTML before extraction so structure is preserved.

    - Converts accordion/collapsible headings to <h3> (trafilatura drops
      role="button" elements, losing the section labels).
    - Replaces &nbsp; with a regular space so the output isn't littered with
      U+00A0 characters.
    """
    html = _ACCORDION_HEADING_RE.sub(
        lambda m: f"<h3>{m.group(1).strip()}</h3>", html
    )
    html = html.replace("&nbsp;", " ")
    return html


def extract_html(html_path: Path) -> str:
    """Extract clean Markdown from an HTML file."""
    html = html_path.read_text(encoding="utf-8", errors="replace")
    html = _preprocess_html(html)
    text = trafilatura.extract(
        html,
        output_format="markdown",
        include_links=True,
        include_tables=True,
        include_images=False,
        favor_precision=True,
    )
    return (text or "").strip()


def extract_pdf(pdf_path: Path) -> str:
    """Extract text from a PDF file using pymupdf."""
    import fitz  # pymupdf

    doc = fitz.open(str(pdf_path))
    pages: list[str] = []
    for page in doc:
        pages.append(page.get_text("text"))
    doc.close()
    return "\n\n".join(p.strip() for p in pages if p.strip()).strip()


def extract(result: FetchResult, use_vision: bool = True) -> str:
    """Extract main text from a fetched capture, writing text.md alongside."""
    if result.pdf_path and result.pdf_path.exists():
        text = extract_pdf(result.pdf_path)
    elif result.html_path and result.html_path.exists():
        text = extract_html(result.html_path)
    else:
        return ""

    # Append content-image text so diagram/flowchart info is captured. The
    # method ("vision" or "ocr") determines the section heading.
    if result.html_path and result.html_path.exists():
        html = result.html_path.read_text(encoding="utf-8", errors="replace")
        image_text, method = process_images(
            html,
            base_url=result.url,
            raw_dir=result.raw_dir,
            headers={"User-Agent": "Mozilla/5.0", "Referer": result.url},
            use_vision=use_vision,
        )
        if image_text:
            heading = "Content Images (Vision)" if method == "vision" else "Content Images (OCR)"
            text = f"{text}\n\n## {heading}\n\n{image_text}" if text else image_text

        # Append Google Charts data (JS-rendered bar charts) as Markdown tables.
        # These are embedded in <script> tags and missed by trafilatura, so we
        # parse the arrayToDataTable calls directly to capture the numbers.
        chart_text = extract_charts(html)
        if chart_text:
            text = f"{text}\n\n## Charts\n\n{chart_text}" if text else chart_text

    text_path = result.raw_dir / "text.md"
    text_path.write_text(text, encoding="utf-8")
    result.text_path = text_path
    return text
