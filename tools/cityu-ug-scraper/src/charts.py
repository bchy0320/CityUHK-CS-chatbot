"""Extract Google Charts data from HTML as Markdown tables.

CityU admission pages render charts with Google Charts (JavaScript). There are
two rendering styles, both of which embed the underlying data in the HTML:

  * ``arrayToDataTable([...])`` calls in <script> tags (bar charts on the
    admission-statistics pages). trafilatura drops <script> content, so we
    parse the calls directly.
  * SVG-rendered charts (line charts, e.g. the ITPI salary chart). Google
    Charts also emits a hidden ``<div aria-label="A tabular representation of
    the data in the chart.">`` containing a <table> with the exact data, which
    we extract directly.

Both are converted to Markdown tables so the numbers are captured faithfully —
no vision call needed, and no hallucination.
"""
from __future__ import annotations

import re

# Matches an arrayToDataTable([...]) call. The data array is a JS array literal
# of rows; we capture it non-greedily up to the closing "]);".
_DATA_RE = re.compile(r"arrayToDataTable\(\s*\[(.*?)\]\s*\)", re.DOTALL)

# Matches a chart title in an options object: title: '...' (single or double quotes).
_TITLE_RE = re.compile(r"title\s*:\s*['\"]([^'\"]+)['\"]")

# Matches a JS function declaration: function Name() { ... }.
_FUNC_RE = re.compile(r"function\s+(\w+)\s*\([^)]*\)\s*\{(.*?)\n\}", re.DOTALL)


def _parse_data_array(body: str) -> list[list[str]]:
    """Parse the rows of an arrayToDataTable call into a list of lists."""
    m = _DATA_RE.search(body)
    if not m:
        return []
    raw = m.group(1)
    rows: list[list[str]] = []
    for line in raw.splitlines():
        line = line.strip().rstrip(",")
        if not line or line.startswith("//"):
            continue
        # A row is a JS array literal: ['Year', 'Applications'] or ['2022', 3429].
        if not (line.startswith("[") and line.endswith("]")):
            continue
        inner = line[1:-1].strip()
        cells: list[str] = []
        for cell in _split_cells(inner):
            cell = cell.strip()
            # Strip surrounding quotes and trailing commas.
            if len(cell) >= 2 and cell[0] == cell[-1] and cell[0] in "'\"":
                cell = cell[1:-1]
            cells.append(cell)
        rows.append(cells)
    return rows


def _split_cells(inner: str) -> list[str]:
    """Split a JS array row into cells, respecting quoted strings."""
    cells: list[str] = []
    buf: list[str] = []
    quote: str | None = None
    for ch in inner:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = None
        elif ch in "'\"":
            quote = ch
            buf.append(ch)
        elif ch == ",":
            cells.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    if buf:
        cells.append("".join(buf))
    return cells


def _rows_to_markdown(rows: list[list[str]]) -> str:
    """Convert parsed rows to a Markdown table."""
    if not rows:
        return ""
    header = rows[0]
    body = rows[1:]
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join("---" for _ in header) + " |",
    ]
    for row in body:
        # Pad/truncate to the header width so the table stays well-formed.
        cells = list(row[: len(header)])
        while len(cells) < len(header):
            cells.append("")
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


# Matches the hidden accessibility table Google Charts emits for SVG-rendered
# charts. The data is in a <table> inside a div with this aria-label.
_SVG_TABLE_RE = re.compile(
    r'<div aria-label="A tabular representation of the data in the chart\."[^>]*>(.*?)</div>\s*</div>',
    re.DOTALL,
)

# Matches a heading (h2-h4) so we can use the nearest preceding one as the
# chart title. Group 2 is the heading text.
_HEADING_RE = re.compile(r"<h([2-4])[^>]*>(.*?)</h\1>", re.DOTALL)


def _extract_svg_charts(html: str) -> list[tuple[str, list[list[str]]]]:
    """Extract data from SVG-rendered Google Charts (hidden data tables).

    Returns a list of ``(title, rows)`` where ``title`` is the nearest preceding
    heading (or a fallback) and ``rows`` is the parsed table data.
    """
    # Precompute heading positions so we can find the nearest preceding one.
    headings = [
        (m.start(), re.sub(r"<[^>]+>", "", m.group(2)).strip())
        for m in _HEADING_RE.finditer(html)
    ]
    headings = [(pos, txt) for pos, txt in headings if txt]

    charts: list[tuple[str, list[list[str]]]] = []
    for m in _SVG_TABLE_RE.finditer(html):
        block = m.group(1)
        tm = re.search(r"<table>(.*?)</table>", block, re.DOTALL)
        if not tm:
            continue
        rows: list[list[str]] = []
        for tr in re.findall(r"<tr>(.*?)</tr>", tm.group(1), re.DOTALL):
            cells = [
                re.sub(r"<[^>]+>", "", c).strip()
                for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", tr, re.DOTALL)
            ]
            if cells:
                rows.append(cells)
        if not rows:
            continue
        # Use the nearest preceding heading as the chart title.
        prev = [h for h in headings if h[0] < m.start()]
        title = prev[-1][1] if prev else "Chart"
        charts.append((title, rows))
    return charts


def extract_charts(html: str) -> str:
    """Return a Markdown block describing all Google Charts in an HTML document.

    Returns an empty string if there are no charts. Each chart is rendered as a
    ``### Chart N`` section with its title (if found) and a Markdown table of
    the data. Handles both ``arrayToDataTable`` (script) charts and
    SVG-rendered charts (hidden data tables).
    """
    sections: list[str] = []

    # 1. arrayToDataTable charts (bar charts in <script> tags).
    if "arrayToDataTable" in html:
        script_blocks = re.findall(r"<script\b[^>]*>(.*?)</script>", html, re.DOTALL)
        chart_scripts = [s for s in script_blocks if "arrayToDataTable" in s]
        for script in chart_scripts:
            funcs = _FUNC_RE.findall(script)
            if not funcs:
                funcs = [("chart", script)]
            for name, body in funcs:
                rows = _parse_data_array(body)
                if not rows:
                    continue
                title_m = _TITLE_RE.search(body)
                title = title_m.group(1) if title_m else name
                table = _rows_to_markdown(rows)
                sections.append(f"### Chart {len(sections) + 1}: {title}\n\n{table}")

    # 2. SVG-rendered charts (line charts etc.) via their hidden data tables.
    for title, rows in _extract_svg_charts(html):
        table = _rows_to_markdown(rows)
        sections.append(f"### Chart {len(sections) + 1}: {title}\n\n{table}")

    return "\n\n".join(sections)