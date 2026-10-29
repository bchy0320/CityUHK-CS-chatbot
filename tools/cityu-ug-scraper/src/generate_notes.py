"""Generate stage: text.md -> draft FAQ note with frontmatter.

Reference mode: one page -> one note. The Answer section is the extracted
main text (lightly structured), NOT a rewrite. Default status is 'draft'.
Area is chosen by the first matching rule in seeds.yaml; falls back to
default_area.
"""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlparse

import frontmatter

from .config import Config
from .fetch import FetchResult


def classify_area(config: Config, url: str, title: str, text: str) -> str:
    """Pick an area folder using the first matching rule in config.area_rules.

    Classification uses the URL *path* and page title only. The page body is
    deliberately NOT scanned: hub pages (e.g. the department home) list many
    unrelated keywords (award names, news items) that would mis-classify them
    (e.g. a stray "scholarship" award name). Path + title are the reliable,
    deterministic signals.
    """
    # Use the URL *path*, not the full URL, so a hostname like
    # "admission.cs.cityu.edu.hk" does not force every page into the
    # broad "admission" area rule.
    path = urlparse(url).path
    head = f"{path}\n{title}".lower()
    for rule in config.area_rules:
        if re.search(rule.pattern, head, re.IGNORECASE):
            return rule.area
    return config.default_area


_ACRONYMS = {"it", "ai", "msc", "bsc", "pgc", "phd", "meng", "beng", "rgc"}


def _humanize(segment: str) -> str:
    """Convert a URL slug segment to a human-readable phrase."""
    words = segment.replace("-", " ").strip().split()
    return " ".join(w.upper() if w.lower() in _ACRONYMS else w.title() for w in words)


def _programme_suffix(url: str) -> str:
    """Return a humanized section/subsection suffix for programme sub-pages.

    Many /academic-programmes/<programme>/<section>/... pages share the same
    generic <title> (just the programme name, e.g. "Bachelor of Science in
    Computer Science | Department of Computer Science"). Append the
    section/subsection from the URL path so each note has a distinct,
    descriptive title instead of a bare programme name.
    """
    parts = [p for p in urlparse(url).path.split("/") if p]
    if len(parts) >= 3 and parts[0] == "academic-programmes":
        return " - ".join(_humanize(p) for p in parts[2:])
    return ""


def _note_title(result: FetchResult) -> str:
    """Derive a human-readable note title from the page title or URL."""
    if result.title:
        title = result.title.strip()
        # CityUHK Scholars profile pages have a <title> like
        # "Cong WANG\n      -  CityUHK Scholars". Strip the trailing
        # " - CityUHK Scholars" suffix and collapse internal whitespace
        # so the note title/filename is clean and Windows-safe.
        title = re.sub(r"\s*-\s*CityUHK Scholars\s*$", "", title, flags=re.IGNORECASE)
        title = re.sub(r"\s+", " ", title).strip()
        # Disambiguate generic programme titles with the URL section/subsection.
        suffix = _programme_suffix(result.url)
        if suffix:
            title = f"{title} - {suffix}"
        return title
    return result.slug.replace("-", " ").title()


def _safe_filename(name: str) -> str:
    """Make a string safe for use as a filename on Windows."""
    # Windows-illegal characters: < > : " / \ | ? *
    name = re.sub(r'[<>:"/\\|?*]', "-", name)
    # Strip control characters (newlines, tabs) that are invalid in filenames.
    name = re.sub(r"[\x00-\x1f\x7f]", "", name)
    return name.strip()


def _unique_path(path: Path, used: set[Path]) -> Path:
    """Return a path that does not collide with an already-written note.

    When two pages share the same title (e.g. two 'Double Degree Programme'
    pages), append a numeric suffix so neither note overwrites the other.
    """
    if path not in used:
        return path
    stem, suffix = path.stem, path.suffix
    i = 2
    while True:
        candidate = path.with_name(f"{stem} ({i}){suffix}")
        if candidate not in used:
            return candidate
        i += 1


def generate_note(
    config: Config, result: FetchResult, notes_root: Path, used_paths: set[Path] | None = None
) -> Path:
    """Generate a single draft note from a fetched+extracted capture."""
    text_path = result.text_path
    if text_path is None or not text_path.exists():
        raise FileNotFoundError(f"No extracted text for {result.url}")

    text = text_path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"Empty extracted text for {result.url}")

    area = classify_area(config, result.url, result.title, text)
    title = _note_title(result)

    # Build frontmatter. source_fetched uses the capture date directory.
    fetched = result.raw_dir.parent.name  # YYYY-MM-DD
    meta = {
        "title": title,
        "type": "faq",
        "area": area,
        "vault": config.vault_name,
        "retrieved": fetched[:7],  # YYYY-MM
        "status": "draft",
        "source_url": result.url,
        "source_fetched": fetched,
    }

    body = f"# {title}\n\n"
    body += "> [!tip] Source\n"
    body += f"> Extracted from: {result.url}\n"
    body += f"> Fetched: {fetched}\n\n"
    body += "## Question\n\n"
    body += f"What does the official CityUHK page say about **{title}**?\n\n"
    body += "## Answer\n\n"
    body += text + "\n\n"
    body += "## Source\n\n"
    body += f"- URL: {result.url}\n"
    body += f"- Fetched: {fetched}\n"
    body += f"- Content hash: `{result.content_hash}`\n"

    note = frontmatter.Post(body, **meta)

    area_dir = notes_root / area
    area_dir.mkdir(parents=True, exist_ok=True)
    out_path = _unique_path(area_dir / f"{_safe_filename(title)}.md", used_paths or set())
    out_path.write_text(frontmatter.dumps(note), encoding="utf-8")
    if used_paths is not None:
        used_paths.add(out_path)
    return out_path
