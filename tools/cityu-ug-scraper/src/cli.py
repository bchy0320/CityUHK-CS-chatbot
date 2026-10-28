"""CLI entry point for the CityU UG scraper.

Usage:
  python -m src.cli pipeline --config config/seeds.yaml
  python -m src.cli fetch --config config/seeds.yaml
  python -m src.cli extract --date 2026-10-27
  python -m src.cli generate --date 2026-10-27
"""
from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from .config import load_config
from .extract import extract as extract_text
from .fetch import fetch_source
from .generate_notes import generate_note

app = typer.Typer(help="CityU UG scraper: fetch, extract, and generate draft notes.")
console = Console()

DEFAULT_CONFIG = "config/seeds.yaml"
DEFAULT_RAW = "raw"
DEFAULT_NOTES = "notes"


@app.command()
def fetch(
    config: str = typer.Option(DEFAULT_CONFIG, "--config", "-c", help="Path to seeds.yaml"),
    raw: str = typer.Option(DEFAULT_RAW, "--raw", help="Raw archive root"),
    date: str = typer.Option(None, "--date", help="Capture date (YYYY-MM-DD); default today"),
) -> None:
    """Fetch all seed URLs into the raw archive."""
    cfg = load_config(config)
    raw_root = Path(raw)
    total = 0
    for source in cfg.sources:
        console.print(f"[bold]Fetching source:[/bold] {source.name}")
        results = fetch_source(cfg, source, raw_root, date)
        for r in results:
            total += 1
            if r.error:
                console.print(f"  [red]ERROR[/red] {r.url}: {r.error}")
            else:
                console.print(f"  [green]OK[/green] {r.url} -> {r.raw_dir}")
    console.print(f"[bold]Fetched {total} URL(s).[/bold]")


@app.command()
def extract(
    raw: str = typer.Option(DEFAULT_RAW, "--raw", help="Raw archive root"),
    date: str = typer.Option(None, "--date", help="Capture date (YYYY-MM-DD); default today"),
    no_vision: bool = typer.Option(False, "--no-vision", help="Disable vision image description (use OCR)"),
) -> None:
    """Extract clean Markdown from all raw captures for a date."""
    from .fetch import FetchResult

    raw_root = Path(raw)
    date_dir = raw_root / (date or _today())
    if not date_dir.exists():
        console.print(f"[red]No captures found for {date_dir}[/red]")
        raise typer.Exit(1)

    count = 0
    for meta_path in sorted(date_dir.glob("*/meta.json")):
        import json

        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        result = FetchResult(
            url=meta["url"], slug=meta["slug"], status=meta["status"],
            content_type=meta["content_type"], content_hash=meta["content_hash"],
            title=meta.get("title", ""), raw_dir=meta_path.parent,
            html_path=meta_path.parent / "page.html",
            pdf_path=meta_path.parent / "page.pdf",
        )
        text = extract_text(result, use_vision=not no_vision)
        if text:
            count += 1
            console.print(f"  [green]OK[/green] {meta['url']} -> {result.text_path}")
        else:
            console.print(f"  [yellow]EMPTY[/yellow] {meta['url']}")
    console.print(f"[bold]Extracted {count} capture(s).[/bold]")


@app.command()
def generate(
    config: str = typer.Option(DEFAULT_CONFIG, "--config", "-c", help="Path to seeds.yaml"),
    raw: str = typer.Option(DEFAULT_RAW, "--raw", help="Raw archive root"),
    notes: str = typer.Option(DEFAULT_NOTES, "--notes", help="Notes output root"),
    date: str = typer.Option(None, "--date", help="Capture date (YYYY-MM-DD); default today"),
) -> None:
    """Generate draft notes from extracted captures."""
    import json

    from .fetch import FetchResult

    cfg = load_config(config)
    raw_root = Path(raw)
    notes_root = Path(notes)
    date_dir = raw_root / (date or _today())
    if not date_dir.exists():
        console.print(f"[red]No captures found for {date_dir}[/red]")
        raise typer.Exit(1)

    count = 0
    used_paths: set[Path] = set()
    for meta_path in sorted(date_dir.glob("*/meta.json")):
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        result = FetchResult(
            url=meta["url"], slug=meta["slug"], status=meta["status"],
            content_type=meta["content_type"], content_hash=meta["content_hash"],
            title=meta.get("title", ""), raw_dir=meta_path.parent,
            html_path=meta_path.parent / "page.html",
            pdf_path=meta_path.parent / "page.pdf",
            text_path=meta_path.parent / "text.md",
        )
        try:
            out = generate_note(cfg, result, notes_root, used_paths)
            count += 1
            console.print(f"  [green]OK[/green] {meta['url']} -> {out}")
        except (FileNotFoundError, ValueError) as exc:
            console.print(f"  [yellow]SKIP[/yellow] {meta['url']}: {exc}")
    console.print(f"[bold]Generated {count} note(s).[/bold]")


@app.command()
def pipeline(
    config: str = typer.Option(DEFAULT_CONFIG, "--config", "-c", help="Path to seeds.yaml"),
    raw: str = typer.Option(DEFAULT_RAW, "--raw", help="Raw archive root"),
    notes: str = typer.Option(DEFAULT_NOTES, "--notes", help="Notes output root"),
    date: str = typer.Option(None, "--date", help="Capture date (YYYY-MM-DD); default today"),
    no_vision: bool = typer.Option(False, "--no-vision", help="Disable vision image description (use OCR)"),
) -> None:
    """Run the full pipeline: fetch -> extract -> generate."""
    cfg = load_config(config)
    raw_root = Path(raw)
    notes_root = Path(notes)
    date_str = date or _today()

    console.print("[bold]Stage 1/3: fetch[/bold]")
    for source in cfg.sources:
        results = fetch_source(cfg, source, raw_root, date_str)
        for r in results:
            if r.error:
                console.print(f"  [red]ERROR[/red] {r.url}: {r.error}")
            else:
                console.print(f"  [green]OK[/green] {r.url}")

    console.print("[bold]Stage 2/3: extract[/bold]")
    _run_extract(raw_root, date_str, use_vision=not no_vision)

    console.print("[bold]Stage 3/3: generate[/bold]")
    _run_generate(cfg, raw_root, notes_root, date_str)

    console.print("[bold green]Pipeline complete.[/bold green]")


def _run_extract(raw_root: Path, date_str: str, use_vision: bool = True) -> None:
    import json

    from .fetch import FetchResult

    date_dir = raw_root / date_str
    if not date_dir.exists():
        console.print(f"[red]No captures found for {date_dir}[/red]")
        return
    for meta_path in sorted(date_dir.glob("*/meta.json")):
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        result = FetchResult(
            url=meta["url"], slug=meta["slug"], status=meta["status"],
            content_type=meta["content_type"], content_hash=meta["content_hash"],
            title=meta.get("title", ""), raw_dir=meta_path.parent,
            html_path=meta_path.parent / "page.html",
            pdf_path=meta_path.parent / "page.pdf",
        )
        text = extract_text(result, use_vision=use_vision)
        console.print(f"  {'OK' if text else 'EMPTY'} {meta['url']}")


def _run_generate(cfg, raw_root: Path, notes_root: Path, date_str: str) -> None:
    import json

    from .fetch import FetchResult

    date_dir = raw_root / date_str
    if not date_dir.exists():
        return
    used_paths: set[Path] = set()
    for meta_path in sorted(date_dir.glob("*/meta.json")):
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        result = FetchResult(
            url=meta["url"], slug=meta["slug"], status=meta["status"],
            content_type=meta["content_type"], content_hash=meta["content_hash"],
            title=meta.get("title", ""), raw_dir=meta_path.parent,
            html_path=meta_path.parent / "page.html",
            pdf_path=meta_path.parent / "page.pdf",
            text_path=meta_path.parent / "text.md",
        )
        try:
            out = generate_note(cfg, result, notes_root, used_paths)
            console.print(f"  OK {meta['url']} -> {out}")
        except (FileNotFoundError, ValueError) as exc:
            console.print(f"  SKIP {meta['url']}: {exc}")


def _today() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


if __name__ == "__main__":
    app()
