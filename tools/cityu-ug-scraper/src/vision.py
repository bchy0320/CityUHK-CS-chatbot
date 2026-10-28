"""Vision-based image understanding via the CityU-hosted DeepSeek endpoint.

OCR (see images.py) extracts raw text lines but loses the *structure* of a
diagram — a curriculum map, a selection-process timeline, or a flowchart.
This module sends content images to a vision-capable LLM and asks it to
describe the image's meaning as structured Markdown (phases, branches,
relationships, course lists).

The endpoint is OpenAI-compatible (chat/completions). Configuration is read
from environment variables so no secret is committed to the repo:

  DEEPSEEK_API_KEY   (required)  API key for the CityU DeepSeek endpoint
  DEEPSEEK_BASE_URL  (optional)  default https://llm.cs.cityu.edu.hk
  DEEPSEEK_MODEL     (optional)  default CS/DeepSeek-V4-Flash-FP8

If no key is configured, or a call fails, the caller falls back to OCR so
the pipeline still produces output.
"""
from __future__ import annotations

import base64
import os
from pathlib import Path
from urllib.parse import urlparse

import httpx

# Defaults for the CityU-hosted DeepSeek endpoint (matches the project's own
# chat widget config — see .site/quartz.config.yaml / chat.js).
DEFAULT_BASE_URL = "https://llm.cs.cityu.edu.hk"
DEFAULT_MODEL = "CS/DeepSeek-V4-Flash-FP8"

# Prompt used to describe a content image. It asks for structured Markdown so
# the output is usable directly in a note. The prompt is deliberately generic
# (the model infers the diagram type) but asks for structure and relationships.
# If the image is purely decorative (a photo, logo, icon, or navigation card
# with no text or data), the model must reply with exactly "DECORATIVE" so the
# caller can skip it instead of recording noise.
_DESCRIBE_PROMPT = (
    "You are analyzing an image from a CityU Computer Science undergraduate "
    "admission or programme page. Determine whether the image contains "
    "meaningful information — a diagram, flowchart, timeline, curriculum map, "
    "infographic, table, or chart. If it does, describe its meaning as "
    "structured Markdown: list the phases/steps in order, the branches/decisions, "
    "the relationships between elements, and any dates or course names. "
    "If the image is purely decorative — a photo, logo, icon, navigation card, "
    "or any image with no text or data — respond with exactly the word "
    "DECORATIVE and nothing else. Do not invent information that is not in the image."
)


def _api_key() -> str | None:
    """Return the DeepSeek API key from the environment, or None."""
    return os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("CITYU_API_KEY") or None


def _base_url() -> str:
    return os.environ.get("DEEPSEEK_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def _model() -> str:
    return os.environ.get("DEEPSEEK_MODEL", DEFAULT_MODEL)


def is_configured() -> bool:
    """Return True if a vision API key is available."""
    return bool(_api_key())


def _image_mime(path: Path) -> str:
    """Return the MIME type for an image file based on its extension."""
    ext = path.suffix.lower()
    return {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".bmp": "image/bmp",
    }.get(ext, "image/png")


def describe_image(path: Path, timeout: float = 60.0) -> str:
    """Send an image to the vision model and return its Markdown description.

    Returns an empty string on any failure (missing key, HTTP error, empty
    response) so the caller can fall back to OCR.
    """
    key = _api_key()
    if not key:
        return ""
    if not path.exists():
        return ""

    try:
        b64 = base64.b64encode(path.read_bytes()).decode()
    except OSError:
        return ""

    mime = _image_mime(path)
    payload = {
        "model": _model(),
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": _DESCRIBE_PROMPT},
                    {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
                ],
            }
        ],
        "max_tokens": 1200,
    }
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}

    try:
        with httpx.Client(timeout=timeout) as client:
            resp = client.post(f"{_base_url()}/v1/chat/completions", headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            return (content or "").strip()
    except (httpx.HTTPError, KeyError, IndexError, ValueError):
        return ""


def process_images_vision(
    image_paths: list[Path],
    max_images: int = 5,
    timeout: float = 60.0,
) -> tuple[str, bool]:
    """Describe a list of downloaded content images with the vision model.

    Returns a tuple ``(markdown, saw_any)`` where ``markdown`` is a Markdown
    block with one section per informative image, and ``saw_any`` is True if the
    model successfully processed at least one image (whether or not it was
    informative). ``saw_any`` lets the caller distinguish "the model judged all
    images decorative" from "the vision call failed", so it can decide whether
    to fall back to OCR.

    Images the model marks as ``DECORATIVE`` (photos, logos, icons, navigation
    cards with no text or data) are skipped and not recorded.
    """
    if not is_configured():
        return "", False

    blocks: list[str] = []
    saw_any = False
    for i, path in enumerate(image_paths[:max_images]):
        description = describe_image(path, timeout=timeout)
        if not description:
            continue
        saw_any = True
        if description.strip().upper() == "DECORATIVE":
            continue
        blocks.append(f"### Image {i + 1}\n\n{description}")

    if not blocks:
        return "", saw_any
    return "\n\n".join(blocks), saw_any