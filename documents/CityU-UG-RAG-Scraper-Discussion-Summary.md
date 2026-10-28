# CityU Undergraduate RAG / Scraper — Discussion Summary

> **Purpose**: Handoff document for humans and AI agents. Captures context, decisions, constraints, and the proposed tool design so further work can continue without re-deriving the background.
>
> **Date of discussion**: 2026-10-27  
> **Related repo**: https://github.com/dive4dec/CityUHK-CS-Admission-FAQ  
> **Live site**: https://dive4dec.github.io/CityUHK-CS-Admission-FAQ/

---

## 1. Background: What the Existing System Is

The repo is **not** a traditional backend RAG service. It is:

| Layer | Description |
|-------|-------------|
| **Knowledge base** | Structured Obsidian vault (~700–1000 Markdown FAQ notes), organized by topic folders (`00_Vault-Map` … `08_Scholarships`) |
| **Note format** | YAML frontmatter + fixed FAQ sections (`Question` / `Answer` / `Related` / `Source`) |
| **Static site** | Quartz builds the vault into a GitHub Pages site |
| **Chatbot** | Client-side AI widget (WebLLM or OpenAI-compatible endpoint). Build-time emits `static/knowledge-index.json` for **local Keyword-RAG**. Agent tools include `search_knowledge_base`, `read_current_page`, `navigate_to_page`. Designed so site notes are authoritative; web is secondary / optional |

### Canonical note shape (example)

```yaml
---
title: "JS1204 2026 JUPAS Score Formula"
type: faq
area: 01_JUPAS-Basics
vault: CityUHK-CS-Admission-FAQ
retrieved: "2026-09"
status: verified   # or draft
---
```

Body structure:

- `# Title`
- `> [!tip] Short answer`
- `## Question`
- `## Answer`
- `## Related` (wikilinks)
- `## Source` (official document + retrieval context)

Integrity tooling already exists: `verify_vault.py` (dangling wikilinks, split GFM tables), Makefile targets for site build/deploy.

---

## 2. User Goals

1. **Expand scope** from “CS Admission FAQ” to broader **undergraduate-related information** (not only CS admission).
2. **Add notes into the RAG** (same vault / same local index pattern).
3. **Batch extract** content from CityU-related websites and **categorize** it.
4. **Accuracy constraints**:
   - Extracted website data should **not be altered** (preserve original wording, numbers, tables).
   - The chatbot must **not search the live web**; it should use **only the current local knowledge base**.

---

## 3. Agreed Design Principles

| Principle | Meaning |
|-----------|---------|
| **Local-only answers** | Chatbot retrieval is restricted to the vault / `knowledge-index.json`. No runtime web search for factual answers. |
| **Immutable raw archive** | First store original HTML/PDF + metadata; never overwrite. Notes are derived views. |
| **Traceability** | Every note carries `source_url`, `retrieved` / `source_fetched`, and a human-readable `## Source` section. |
| **Draft → verified** | Auto-generated notes default to `status: draft`; human (or strict check) promotes to `verified`. |
| **Minimal rewriting** | Prefer “clean extraction + light structure” over paraphrasing. Numbers, dates, and official terms stay intact. |
| **Incremental expansion** | Start with a small set of high-value URLs; validate pipeline; then widen seed list. |

---

## 4. Proposed Tool: Scraper + Note Generator

Working name / folder idea: `cityu-ug-scraper/` (or similar). Can live next to the vault or as a sibling project that outputs notes into the vault.

### 4.1 Directory layout

```
cityu-ug-scraper/
├── config/
│   ├── seeds.yaml           # seed URLs + area classification rules
│   └── note_template.md     # optional template reference
├── raw/                     # IMMUTABLE captures
│   └── YYYY-MM-DD/
│       └── <slug_or_hash>/
│           ├── meta.json    # url, fetched_at, status, content_hash, title, ...
│           ├── page.html    # or .pdf
│           └── text.md      # cleaned main text (extraction result, not rewrite)
├── notes/                   # generated draft FAQ notes (review before merge into vault)
│   ├── 09_Undergraduate-General/
│   ├── 10_Fees-Housing/
│   └── ...
├── src/
│   ├── fetch.py
│   ├── extract.py
│   ├── classify.py
│   ├── generate_notes.py
│   └── cli.py
├── requirements.txt
└── README.md
```

### 4.2 Pipeline stages

```
seeds.yaml  →  fetch (raw/)  →  extract (text.md)  →  classify (area)  →  generate_notes (notes/)  →  [human review]  →  merge into vault  →  rebuild knowledge-index
```

| Stage | Responsibility | Notes |
|-------|----------------|-------|
| **fetch** | Download HTML/PDF; write `meta.json` + binary/text; content hash; respect delay/robots | Prefer `httpx`; Playwright only where needed |
| **extract** | HTML → clean Markdown/main text; preserve tables | Prefer `trafilatura` (or readability); no semantic rewrite |
| **classify** | Map URL/title/text → `area` folder via rules in `seeds.yaml` | Rules first; optional light LLM for labeling only |
| **generate_notes** | Emit frontmatter + FAQ sections | Default `status: draft`; include `source_url` / `source_fetched` |

### 4.3 Two generation modes

| Mode | Behavior | Use when |
|------|----------|----------|
| **Reference note** | One page → one note; Answer ≈ extracted main content, lightly structured | Policies, fees, programme overviews (safest) |
| **FAQ-style note** | Split into Q/A; Answer still grounded in extracted passages | High-frequency student questions (after reference path is stable) |

LLM (if used) must be constrained: no invented numbers/dates; keep official wording; mark gaps explicitly.

### 4.4 Suggested CLI

```bash
python -m src.cli fetch --config config/seeds.yaml
python -m src.cli extract --date 2026-10-27
python -m src.cli generate --date 2026-10-27 --mode reference
python -m src.cli pipeline --config config/seeds.yaml
# later: diff between fetches; list-drafts
```

### 4.5 Suggested stack (minimal)

- `httpx`, `trafilatura`, `beautifulsoup4`, `pyyaml`, `python-frontmatter`, `pydantic`, `typer`/`click`, `rich`
- Optional: `pymupdf` (PDF), `playwright` (JS-heavy pages)

### 4.6 Example `seeds.yaml` shape

```yaml
vault_name: CityUHK-Undergraduate-FAQ
default_area: 09_Undergraduate-General

sources:
  - name: cityu_admission
    base_urls:
      - https://www.cityu.edu.hk/admissions/
      - https://www.cityu.edu.hk/ug/
    include_patterns: ["/admissions/", "/ug/", "/programme/"]
    exclude_patterns: ["/news/", "/event/"]
    area_rules:
      - pattern: "tuition|fee|charges"
        area: 10_Fees-Housing
      - pattern: "scholarship|award"
        area: 08_Scholarships
      - pattern: "jupas|non-jupas|admission"
        area: 01_JUPAS-Basics  # or a new admission area
```

### 4.7 Target note frontmatter (extended)

```yaml
---
title: "..."
type: faq
area: 09_Undergraduate-General
vault: CityUHK-Undergraduate-FAQ
retrieved: "2026-10"
status: draft
source_url: "https://..."
source_fetched: "2026-10-27"
---
```

---

## 5. Scope Guidance (Undergraduate Expansion)

Do **not** crawl the entire CityU site blindly. Define a bounded undergraduate scope first, for example:

- Admission (JUPAS / non-JUPAS, dates, requirements)
- Programme lists and overviews (beyond CS only)
- Fees / tuition / housing (if in scope)
- Scholarships
- Academic regulations / curriculum records
- Internship / exchange (where relevant)

Prioritize stable official pages and PDFs (score formulas, curriculum records) over news/events.

---

## 6. Integration with Existing Vault & Chatbot

1. Generated notes land in `notes/` as drafts.
2. After review, promote `status: verified` and move/copy into the vault folder structure.
3. Rebuild site / `knowledge-index.json` (existing Quartz + emitter path).
4. Ensure chatbot configuration **disables or does not expose** live web search tools for factual Q&A; answers must come from the local index only.
5. Optionally extend `verify_vault.py`-style checks for new areas and frontmatter fields (`source_url`, etc.).

---

## 7. Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Semantic drift when “cleaning” HTML | Raw archive + extraction-only step; human spot-check |
| Stale data | `retrieved` / `source_fetched`; periodic re-fetch + hash diff |
| Over-broad crawl | Seed list + include/exclude patterns; start small |
| LLM invention in FAQ mode | Strict prompts; prefer reference mode first; draft status |
| Tables / numbers broken | Keep tables in Markdown; reuse vault verify checks |
| Site ToS / robots | Respect robots.txt; polite rate limits |

---

## 8. Decisions Already Aligned

- Keep the **notes + local Keyword-RAG** model; do not switch to live-web RAG for admission/UG facts.
- **Raw captures are immutable**; notes are regenerable.
- Default new notes to **`status: draft`**.
- Prefer **rule-based classification** and **reference-style notes** before aggressive FAQ splitting.
- Chatbot must answer **only from local data**.

---

## 9. Open Items / Next Steps for the Next Agent

Pick one (or sequence them):

1. **Implement MVP pipeline**  
   - `seeds.yaml` with a small real CityU URL set  
   - `fetch.py` + `extract.py` + `generate_notes.py` (reference mode) + CLI  
   - Output under `raw/` and `notes/`

2. **Note template + constrained LLM prompt**  
   - For FAQ-style generation that refuses to invent facts

3. **Area taxonomy + classification rules**  
   - Map undergraduate topics to vault folders (`09_…`, `10_…`, etc.)

4. **Vault merge + verify**  
   - Script to merge reviewed notes into the existing repo layout and run integrity checks

5. **Chatbot lock-down checklist**  
   - Confirm how to disable external search in the Quartz AI chat plugin / agent tools

**Useful inputs the user may still provide:**

- Priority URL list (admission, fees, programmes, …)
- Preferred new folder names / vault name
- Whether PDF-heavy sources are in scope for v1
- Whether the scraper should live inside the existing repo or as a sibling project

---

## 10. Quick Reference Links

- Repo: https://github.com/dive4dec/CityUHK-CS-Admission-FAQ  
- Site: https://dive4dec.github.io/CityUHK-CS-Admission-FAQ/  
- Example note (raw): `01_JUPAS-Basics/JS1204 2026 JUPAS Score Formula.md`  
- Freshness note: `00_Vault-Map/Vault Freshness and Verification Status.md`  
- Chat/RAG implementation notes: see repo `CHANGELOG.md` (knowledge-index, AI chat widget, agent tools)

---

*End of handoff summary. Agents: treat §3–§4 as the current design target; treat §9 as the work queue.*
