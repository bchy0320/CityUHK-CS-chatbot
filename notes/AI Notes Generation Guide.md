# AI Notes Generation Guide

> [!tip] Purpose
> This document is for AI assistants generating notes for the CityUHK CS chatbot knowledge vault. It defines the **note format** and the **web search rules** to follow.

---

## 1. Note Format

Every note must follow this exact structure. A note is only loaded into the RAG pipeline when it has **both** a `## Question` section **and** a `> [!tip] Short answer` block (see `loadNotes()` in `src/notes.js`).

### 1.1 YAML Frontmatter

Each note starts with YAML frontmatter enclosed in `---`:

```yaml
---
area: <folder-name>
retrieved: <YYYY-MM>
source_fetched: '<YYYY-MM-DD>'
source_url: <canonical-source-url>
status: verified
title: <Note Title>
type: faq
vault: CityUHK-CS-Admission-FAQ
tags: [jupas, 1.5x, 2026]
---
```

**Field rules:**

| Field | Required | Description |
|-------|----------|-------------|
| `area` | Yes | The folder name where the note lives (e.g. `12_International-Exposure`). Must match the folder name exactly, including the numeric prefix. |
| `retrieved` | Yes | Month of retrieval, format `YYYY-MM`. |
| `source_fetched` | Yes | Date the source was fetched, format `YYYY-MM-DD`, quoted. |
| `source_url` | Yes | The canonical URL the content was extracted from. |
| `status` | Yes | `verified` for notes that have been checked against the source. |
| `title` | Yes | The note title. |
| `type` | Yes | `faq` for Q&A notes. |
| `vault` | Yes | Always `CityUHK-CS-Admission-FAQ`. |
| `tags` | Recommended | A lowercase list of core keywords that describe the note, e.g. `[jupas, 1.5x, 2026]`. Use a flow list `[a, b]` or a block list of `- item` lines. Tags are included in the embedding and keyword search, so they help the chatbot find the note. Keep them short and specific (system names, programme codes, years, topics). |

### 1.2 Body Structure

After the frontmatter, the body follows this order:

```markdown
# <Note Title>

> [!tip] Short answer
> <A concise one-paragraph summary of the answer. Use **bold** for key terms.>

> [!tip] Source
> Extracted from: <source_url>
> Fetched: <YYYY-MM-DD>

## Question

<The question this note answers. Use **bold** for key terms.>

## Answer

<The answer content. Use headings (##, ###) to organize. Use tables where helpful.>

## Source

- URL: <source_url>
- Fetched: <YYYY-MM-DD>
```

**Body rules:**

- `# Title` must match the `title` field in frontmatter.
- **Make the title carry the core keywords.** The title is the strongest signal for both keyword routing and the embedding. Prefer a specific title like `2026 JUPAS CS 1.5x Weighting Policy` over a vague one like `Policy Update`.
- The `> [!tip] Short answer` block **must come first** (before `> [!tip] Source`). The parser reads the **first** `> [!tip]` block as the short answer, so the Short answer block must precede the Source block.
- The `> [!tip] Short answer` block is a **single paragraph** that summarises the Answer content. **Put the key facts in the first 2–3 sentences** — many embedding models weight the opening most heavily. Use **bold** for key terms (programme names, codes, amounts, dates, etc.).
- The `> [!tip] Source` block must repeat the source URL and fetch date.
- `## Question` states the question being answered.
- `## Answer` contains the content, organized with subheadings and tables.
- `## Source` repeats the URL and fetch date at the end.
- Use **bold** for key terms in the Question.
- Use Markdown tables for structured data (e.g. partner universities, comparison tables).

### 1.3 File Naming

- File names use `Title - Subtitle.md` format.
- Spaces are preserved in file names (e.g. `Student Exchange - Application Process.md`).
- When linking between notes, use **relative Markdown links** with URL-encoded spaces (e.g. `[Student Exchange - Application Process](Student%20Exchange%20-%20Application%20Process.md)`), **not** `[[wikilinks]]`. This keeps links working when folders are renamed.

---

## 2. Web Search Rules

### 2.1 No Duplicate Searches

**Rule: Do NOT fetch the same URL more than once.**

- Before fetching a URL, check whether it has already been fetched in this session.
- If a URL has already been fetched, **do not fetch it again** — reuse the previously retrieved content.
- This applies to the exact URL string. A URL is considered "already fetched" if it was fetched at any earlier point in the session.

### 2.2 How to Track Fetched URLs

Maintain a running list of fetched URLs. Before each new fetch, check the list:

```
Fetched URLs (session):
1. https://www.cs.cityu.edu.hk/student-life/student-exchange/student-exchange-outbound
2. https://www.cityu.edu.hk/geo/global-opportunities
...
```

If the target URL is already in the list, **skip the fetch** and use the cached content.

### 2.3 Handling Truncated / Partial Content

- If a fetch returns truncated or partial content, **do not re-fetch the same URL**.
- Instead, either:
  - Use the partial content already retrieved, or
  - Find a **different URL** that covers the same information.
- Re-fetching the same URL repeatedly is **not allowed** — it wastes time and produces no new information.

### 2.4 Prefer Canonical Sources

- Prefer official CityUHK pages (e.g. `cityu.edu.hk`, `cs.cityu.edu.hk`, `admission.cs.cityu.edu.hk`).
- Use the most specific page that directly answers the question.
- Record the canonical URL in `source_url`.

---

## 3. Folder Organization

- Notes live under the `notes/` directory at the project root.
- Each topic gets its own folder with a **numeric prefix** (e.g. `notes/12_International-Exposure/`). The numeric prefix keeps folders sorted and must be included in the `area` field.
- The folder name becomes the `area` field in frontmatter, **including the numeric prefix**.
- Do **not** mix new notes into existing folders.
- Example: `notes/12_International-Exposure/` → `area: 12_International-Exposure`.

**Existing folder numbering (00–14):**

| Prefix | Folder |
|--------|--------|
| 00 | Vault-Map |
| 01 | JUPAS-Basics |
| 02 | JUPAS-Scores |
| 03 | NonJUPAS |
| 04 | Curriculum |
| 05 | Programmes |
| 06 | Courses |
| 07 | CityU-Scores |
| 08 | Scholarships |
| 09 | Academic-Administration-Systems |
| 10 | Academic-Staff |
| 11 | Campus-Facilities-IT |
| 12 | International-Exposure |
| 13 | Postgraduate-Programmes |
| 14 | Student-Mentor-Scheme |

When adding a new topic folder, assign the next available number (e.g. `15_...`).

---

## 4. Self-Generated Q&A

Beyond the main topics, generate additional Q&A notes that answer common questions students might ask, such as:

- What fixed study tours happen each year?
- How do I apply for exchange / study tour?
- Who is eligible?
- When should I start planning?
- What financial support is available?

Each Q&A note follows the same format (frontmatter + Short answer + Question + Answer + Source).