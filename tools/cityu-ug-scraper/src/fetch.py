"""Fetch stage: download HTML/PDF into an immutable raw archive.

Each capture is written under raw/YYYY-MM-DD/<slug>/:
  - meta.json   : url, fetched_at, status, content_hash, title, content_type, ...
  - page.html   : original HTML (or page.pdf for PDF sources)
  - text.md     : cleaned main text (extraction result, not a rewrite)

Raw captures are never overwritten. Re-fetching the same URL on a later day
writes to a new date directory; a content_hash lets us detect drift.
"""
from __future__ import annotations

import hashlib
import json
import re
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import httpx

from .config import Config, Source


def _slugify(url: str) -> str:
    """Build a filesystem-safe slug from a URL."""
    parsed = urlparse(url)
    path = parsed.path.strip("/") or "index"
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", path).strip("-")
    return slug[:80] or "index"


def _content_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@dataclass
class FetchResult:
    url: str
    slug: str
    status: str
    content_type: str
    content_hash: str
    title: str
    raw_dir: Path
    html_path: Path | None = None
    pdf_path: Path | None = None
    text_path: Path | None = None
    error: str | None = None


class Fetcher:
    """Polite HTTP fetcher that archives raw captures."""

    def __init__(self, config: Config, raw_root: Path, date_str: str | None = None):
        self.config = config
        self.raw_root = Path(raw_root)
        self.date_str = date_str or datetime.now(timezone.utc).strftime("%Y-%m-%d")
        self._last_request: dict[str, float] = {}
        # CityU's Sitecore site blocks the default python-httpx User-Agent.
        # Send browser-like headers so the request is accepted.
        self._client = httpx.Client(
            timeout=config.fetch.timeout_seconds,
            headers={
                "User-Agent": config.fetch.user_agent,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            },
            follow_redirects=True,
        )

    def _respect_delay(self, host: str) -> None:
        delay = self.config.fetch.delay_seconds
        last = self._last_request.get(host)
        if last is not None:
            elapsed = time.monotonic() - last
            if elapsed < delay:
                time.sleep(delay - elapsed)
        self._last_request[host] = time.monotonic()

    def fetch(self, url: str) -> FetchResult:
        """Fetch a single URL and archive the raw capture."""
        parsed = urlparse(url)
        host = parsed.netloc
        self._respect_delay(host)

        slug = _slugify(url)
        raw_dir = self.raw_root / self.date_str / slug
        raw_dir.mkdir(parents=True, exist_ok=True)

        try:
            resp = self._client.get(url)
            resp.raise_for_status()
        except httpx.HTTPError as exc:
            return FetchResult(
                url=url, slug=slug, status="error", content_type="",
                content_hash="", title="", raw_dir=raw_dir, error=str(exc),
            )

        content_type = resp.headers.get("content-type", "").lower()
        data = resp.content
        ctype = _content_hash(data)

        # Determine title from HTML <title> if available.
        title = ""
        if "html" in content_type:
            title = _extract_title(data)

        meta = {
            "url": url,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "status": resp.status_code,
            "content_type": content_type,
            "content_hash": ctype,
            "title": title,
            "slug": slug,
        }

        html_path = pdf_path = text_path = None
        if "pdf" in content_type:
            pdf_path = raw_dir / "page.pdf"
            pdf_path.write_bytes(data)
            meta["kind"] = "pdf"
        else:
            html_path = raw_dir / "page.html"
            html_path.write_bytes(data)
            meta["kind"] = "html"

        (raw_dir / "meta.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        return FetchResult(
            url=url, slug=slug, status=str(resp.status_code),
            content_type=content_type, content_hash=ctype, title=title,
            raw_dir=raw_dir, html_path=html_path, pdf_path=pdf_path,
            text_path=text_path,
        )

    def close(self) -> None:
        self._client.close()


def _extract_title(html: bytes) -> str:
    """Best-effort <title> extraction without a full parse."""
    import re as _re
    m = _re.search(rb"<title[^>]*>(.*?)</title>", html, _re.IGNORECASE | _re.DOTALL)
    if not m:
        return ""
    return m.group(1).decode("utf-8", errors="replace").strip()


def fetch_source(config: Config, source: Source, raw_root: Path, date_str: str | None = None) -> list[FetchResult]:
    """Fetch all base URLs for a source. Returns results (including errors)."""
    fetcher = Fetcher(config, raw_root, date_str)
    results: list[FetchResult] = []
    try:
        for url in source.base_urls:
            results.append(fetcher.fetch(url))
    finally:
        fetcher.close()
    return results
