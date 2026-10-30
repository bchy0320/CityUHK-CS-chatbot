# AI Notes Generation Guide

> [!tip] Purpose
> This document is for AI assistants generating notes for the CityUHK CS chatbot knowledge vault. It defines the **note format** and the **web search rules** to follow.

---

## 1. Note Format

Every note must follow this exact structure.

### 1.1 YAML Frontmatter

Each note starts with YAML frontmatter enclosed in `---`:

```yaml
---
area: <folder-name>
retrieved: <YYYY-MM>
source_fetched: '<YYYY-MM-DD>'
source_url: <canonical-source-url>
status: draft
title: <Note Title>
type: faq
vault: CityUHK-Undergraduate-FAQ
---
```

**Field rules:**

| Field | Required | Description |
|-------|----------|-------------|
| `area` | Yes | The folder name where the note lives (e.g. `Notes-International-Exposure`). Must match the folder name exactly. |
| `retrieved` | Yes | Month of retrieval, format `YYYY-MM`. |
| `source_fetched` | Yes | Date the source was fetched, format `YYYY-MM-DD`, quoted. |
| `source_url` | Yes | The canonical URL the content was extracted from. |
| `status` | Yes | `draft` (or `final` when verified). |
| `title` | Yes | The note title. |
| `type` | Yes | `faq` for Q&A notes. |
| `vault` | Yes | Always `CityUHK-Undergraduate-FAQ`. |

### 1.2 Body Structure

After the frontmatter, the body follows this order:

```markdown
# <Note Title>

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
- The `> [!tip] Source` block must repeat the source URL and fetch date.
- `## Question` states the question being answered.
- `## Answer` contains the content, organized with subheadings and tables.
- `## Source` repeats the URL and fetch date at the end.
- Use **bold** for key terms in the Question.
- Use Markdown tables for structured data (e.g. partner universities, comparison tables).

### 1.3 File Naming

- File names use `Title - Subtitle.md` format.
- Spaces are preserved in file names (e.g. `Student Exchange - Application Process.md`).
- When linking between notes, URL-encode spaces as `%20`.

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

- Notes for a new topic go in a **new folder** under `documents/`.
- The folder name becomes the `area` field in frontmatter.
- Do **not** mix new notes into existing folders under `tools/cityu-ug-scraper/notes/`.
- Example: `documents/Notes-International-Exposure/` → `area: Notes-International-Exposure`.

---

## 4. Self-Generated Q&A

Beyond the main topics, generate additional Q&A notes that answer common questions students might ask, such as:

- What fixed study tours happen each year?
- How do I apply for exchange / study tour?
- Who is eligible?
- When should I start planning?
- What financial support is available?

Each Q&A note follows the same format (frontmatter + Question + Answer + Source).