# Knowledge-base authoring conventions

Conventions for any LLM agent authoring content in this knowledge base. The machine
settings (paths, note kinds, link prefixes, embedding model) live in `kb.config.json`;
this file covers the human/authoring conventions.

## What this is

A plain-markdown knowledge base. No build step required.

- `kb/sources/` — one page per ingested item (a video, web/forum thread, PDF, manual, doc)
- `kb/notes/` — atomic notes, one idea per file, cross-linked
- `kb/maps/` — curated overview pages that group related notes (systems / themes)
- `kb/.raw/` — normalized raw captures from ingestion (transcripts, extracted text)
- `tools/` — the kb-toolkit Python tools (ingest, semantic_links, check_feeds)

## The two-step pipeline

1. **Ingest → source page** (`kb-add-source`): run `python tools/ingest.py <input>`,
   then write `kb/sources/<slug>.md` from the metadata + raw capture. Set `processed: false`.
2. **Source → notes** (`kb-process`): extract atomic notes into `kb/notes/`, cross-link
   them, set the source's `processed: true`, then run the semantic backlinker.

## Source pages

Frontmatter:
```yaml
---
title: "Human title"
source: <url-or-path>
type: youtube | web | pdf | local
date: YYYY-MM-DD
author: "..."
tags: [ ... ]
processed: false
---
```
Body: optional embed (YouTube), `## Summary` (2-4 paragraphs), `## Key Points`,
`## Notable Excerpts`, `## Captured Content`. Do NOT add an H1 — the `title` is the heading.

## Notes (atomic)

Each note is ONE idea, expressible as a single sentence (the title). 2-4 paragraphs of
plain prose. Frontmatter carries a `kind` (one of `note_kinds` in `kb.config.json`):
```yaml
---
title: "A complete sentence stating one idea"
kind: how-it-works
source: "[[sources/source-slug|Source Title]]"
related:
  - "[[notes/other-note|Other Note Title]]"
tags: [ ... ]
---
```
End every note with `## Related Concepts` and `## Source`. Before writing, search for
existing notes to cross-link: `grep -ri "KEYWORD" kb/notes/ -l`.

How many notes per source? Enough to capture the distinct ideas — often 3-8 for a rich
source, fewer for a short one. Don't pad; one strong idea per note.

## Maps

Curated, narrated overview pages (not auto-generated). Use them as entry points for a
system or theme: a paragraph of orientation with inline `[[notes/...]]` links, then
`## Key Notes`, optionally `## Common Issues`, and `## Sources`.

## Conventions

**Wiki links always include the folder prefix** (they resolve from `kb/`):
```
[[notes/slug|Display Title]]
[[sources/slug|Source Title]]
[[maps/slug|Map Name]]
```
Never bare `[[slug]]`.

**Slugs:** lowercase, hyphenated, slugified from the title.

**No H1 in content** — frontmatter `title` is the heading.

**Note titles are sentences** stating the idea ("The IACV controls idle speed by bypassing
the throttle plate"), not topic labels ("IACV").

## Tools

```bash
python tools/ingest.py <url-or-path> [--type ...] [--kind ...] [--pages A-B]
python tools/semantic_links.py embed
python tools/semantic_links.py apply --threshold 0.6 --top-n 5 --write
python tools/check_feeds.py
```
Install deps once: `pip install -r requirements.txt`. No API keys required — transcripts
via yt-dlp, web via trafilatura, embeddings via a local sentence-transformers model.
