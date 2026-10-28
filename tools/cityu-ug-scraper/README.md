# CityU UG Scraper

A small, polite scraper that fetches official CityUHK undergraduate pages,
extracts clean Markdown, and generates **draft** FAQ notes for the Obsidian
vault. It is designed to be **faithful**: raw captures are immutable and the
extracted text is not rewritten.

## Scope (v1)

- Admission (JUPAS / non-JUPAS) official pages
- Programme overviews
- Curriculum / course records
- PDF sources (e.g. curriculum records) via pymupdf
- Content images (diagrams, flowcharts, curriculum maps) via vision model
  (DeepSeek) with OCR fallback
- JS-rendered Google Charts (bar charts) via direct data extraction

Deliberately **excluded** for now: news, events, and dynamic pages.

## Design principles

| Principle | Meaning |
|-----------|---------|
| Local-only answers | Notes feed the local knowledge base; no live-web RAG. |
| Immutable raw archive | `raw/` captures are never overwritten; notes are regenerable. |
| Traceability | Every note carries `source_url`, `source_fetched`, `content_hash`. |
| Draft → verified | Generated notes default to `status: draft`; promote after review. |
| Minimal rewriting | Clean extraction + light structure; numbers/dates stay intact. |

## Layout

```
tools/cityu-ug-scraper/
├── config/seeds.yaml      # seed URLs + area classification rules
├── raw/                   # IMMUTABLE captures (gitignored)
│   └── YYYY-MM-DD/<slug>/
│       ├── meta.json      # url, fetched_at, content_hash, title, ...
│       ├── page.html      # or page.pdf
│       └── text.md        # cleaned main text (extraction, not rewrite)
├── notes/                 # generated draft notes (review before merge)
│   └── <area>/
├── src/
│   ├── config.py          # seeds.yaml -> typed Config
│   ├── fetch.py           # download + archive raw captures
│   ├── extract.py         # HTML/PDF -> clean Markdown
│   ├── images.py          # locate + download + describe content images
│   ├── vision.py          # vision-model image understanding (DeepSeek)
│   ├── charts.py          # extract Google Charts data -> Markdown tables
│   ├── generate_notes.py  # text.md -> draft note with frontmatter
│   └── cli.py             # pipeline / fetch / extract / generate
└── requirements.txt
```

## Setup

```bash
cd tools/cityu-ug-scraper
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### Vision (optional)

Content images are described by a vision-capable LLM (DeepSeek) when an API
key is configured; otherwise the tool falls back to OCR. Configure via
environment variables (no secret is committed to the repo):

```bash
# CityU-hosted DeepSeek endpoint (defaults shown)
set DEEPSEEK_API_KEY=sk-...      # required for vision
set DEEPSEEK_BASE_URL=https://llm.cs.cityu.edu.hk
set DEEPSEEK_MODEL=CS/DeepSeek-V4-Flash-FP8
```

The endpoint is OpenAI-compatible (`/v1/chat/completions`). If no key is set,
or a vision call fails, the pipeline still produces output via OCR.

## Usage

```bash
# Run the whole pipeline (fetch -> extract -> generate)
python -m src.cli pipeline --config config/seeds.yaml

# Or run stages individually
python -m src.cli fetch --config config/seeds.yaml
python -m src.cli extract --date 2026-10-27
python -m src.cli generate --date 2026-10-27
```

## Workflow

1. `pipeline` fetches seed URLs into `raw/YYYY-MM-DD/`, extracts text, and
   writes draft notes into `notes/<area>/`.
2. Review the drafts; promote `status: draft` → `status: verified`.
3. Merge verified notes into the vault folder structure.
4. Rebuild the site / `knowledge-index.json` (existing Quartz path).

## Notes on faithfulness

- The `Answer` section is the extracted main text, **not** a paraphrase.
- Numbers, dates, and official terms are preserved verbatim.
- If a page yields no useful text, the capture is skipped (not fabricated).
- Content images (diagrams, flowcharts, curriculum maps) are downloaded and
  described by a vision model (DeepSeek) when a key is configured; the
  structured description is appended under a `Content Images (Vision)` section.
  Without a key, the tool falls back to OCR (`Content Images (OCR)`).
- Only *information-bearing* images are recorded. The vision model is asked to
  judge each image: if it is purely decorative (a photo, logo, icon, or
  navigation card with no text or data), it is skipped. Decorative images are
  also filtered out up front by their CSS class (e.g. `image-style-crop-*`,
  `card-img`, `menu-img`) and by `src`/`alt` markers (logos, icons, social
  buttons, news thumbnails).
- JS-rendered Google Charts are extracted directly and written as Markdown
  tables under a `## Charts` section. This captures the exact numbers (no vision
  call, no hallucination). Two rendering styles are handled:
  - `arrayToDataTable` calls in `<script>` tags (bar charts on the
    admission-statistics pages).
  - SVG-rendered charts (line charts, e.g. the ITPI salary chart), via the
    hidden accessibility `<table>` Google Charts embeds alongside the SVG.
- Accordion/collapsible section headings (e.g. "General Entrance Requirements",
  "Interview Arrangements") are converted to `<h3>` before extraction, so the
  section structure is preserved even though trafilatura would otherwise drop
  the `role="button"` elements.
- `&nbsp;` entities are normalized to regular spaces so the output isn't
  littered with U+00A0 characters.
- Respects `robots.txt` and a polite delay between requests.