#!/usr/bin/env python3
"""
Unified source ingester for the knowledge-base toolkit.

Normalizes ANY source — a YouTube video, a web page / forum thread, a PDF or
manual, or a local document — into (1) a clean text capture written under the
configured `raw` dir and (2) a METADATA JSON block printed to stdout. The
kb-add-source skill reads that metadata and authors the `sources/<slug>.md` page;
this script does no LLM authoring itself.

Usage:
  python tools/ingest.py <input> [--type auto|youtube|web|pdf|local]
                                 [--kind KIND] [--pages A-B] [--title TITLE]

  <input> may be a URL, a file path, or a directory (directory => ingest each file).

Type is auto-detected:
  youtube  -> youtube.com / youtu.be URLs
  web      -> any other http(s) URL
  pdf      -> *.pdf
  local    -> *.txt / *.md / *.html / *.htm / *.docx  (or a directory of them)
"""

import argparse
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kb_lib  # noqa: E402

CFG = kb_lib.load_config()
RAW_DIR = CFG.abspath("raw")
SOURCES_DIR = CFG.abspath("sources")

YOUTUBE_RE = re.compile(r"(?:youtube\.com|youtu\.be)", re.I)
VIDEO_ID_RE = re.compile(r"(?:v=|youtu\.be/|shorts/|embed/)([A-Za-z0-9_-]{11})")
LOCAL_EXTS = {".txt", ".md", ".markdown", ".html", ".htm", ".docx"}


def _missing(pkg: str, what: str):
    sys.exit(f"error: '{pkg}' is required to ingest {what}. Install deps: pip install -r requirements.txt")


def detect_type(inp: str) -> str:
    if inp.startswith("http://") or inp.startswith("https://"):
        return "youtube" if YOUTUBE_RE.search(inp) else "web"
    p = Path(inp)
    if p.is_dir():
        return "dir"
    if p.suffix.lower() == ".pdf":
        return "pdf"
    if p.suffix.lower() in LOCAL_EXTS:
        return "local"
    sys.exit(f"error: cannot detect source type for '{inp}'. Pass --type explicitly.")


def emit(meta: dict, raw_text: str):
    """Write the raw capture and print the METADATA block the skill consumes."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    slug = meta.get("suggested_slug") or kb_lib.slugify(meta.get("title", "source"))
    raw_path = RAW_DIR / f"{slug}.txt"
    raw_path.write_text(raw_text.strip() + "\n", encoding="utf-8")
    meta["suggested_slug"] = slug
    meta["raw_path"] = str(raw_path)
    meta["word_count"] = len(raw_text.split())
    print("\n--- METADATA ---")
    print(json.dumps(meta, indent=2, ensure_ascii=False))
    print("--- END METADATA ---")


def already_ingested(key: str) -> bool:
    return key in kb_lib.existing_source_keys(SOURCES_DIR)


# --- YouTube --------------------------------------------------------------

def _clean_vtt(vtt: str) -> str:
    lines, seen = [], set()
    for line in vtt.splitlines():
        line = line.strip()
        if not line or line.startswith("WEBVTT") or "-->" in line or re.match(r"^\d+$", line):
            continue
        line = re.sub(r"<[^>]+>", "", line).strip()
        if line and line not in seen:
            seen.add(line)
            lines.append(line)
    return " ".join(lines)


def ingest_youtube(url: str, kind: str | None):
    try:
        import yt_dlp  # noqa: F401  (presence check; we invoke it via -m for venv safety)
    except ImportError:
        _missing("yt-dlp", "YouTube videos")
    ytdlp = [sys.executable, "-m", "yt_dlp"]

    m = VIDEO_ID_RE.search(url) or re.match(r"^([A-Za-z0-9_-]{11})$", url)
    if not m:
        sys.exit(f"error: cannot extract video id from {url}")
    vid = m.group(1)
    full_url = f"https://www.youtube.com/watch?v={vid}"
    if already_ingested(full_url) or already_ingested(vid):
        print(f"Already ingested: {vid}")
        return

    # metadata
    meta_cmd = ytdlp + ["--no-warnings", "--skip-download",
                        "--print", "%(title)s\t%(duration_string)s\t%(upload_date)s\t%(uploader)s", full_url]
    r = subprocess.run(meta_cmd, capture_output=True, text=True)
    parts = (r.stdout.strip().split("\t") + ["", "", "", ""])[:4]
    title, duration, raw_date, uploader = parts
    title = title or vid
    date = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:]}" if len(raw_date) == 8 else datetime.now().strftime("%Y-%m-%d")

    # captions
    with tempfile.TemporaryDirectory() as tmp:
        cap_cmd = ytdlp + ["--write-auto-sub", "--skip-download", "--sub-lang", "en",
                           "--sub-format", "vtt", "--no-warnings", "-o", str(Path(tmp) / vid), full_url]
        subprocess.run(cap_cmd, capture_output=True, text=True)
        vtts = list(Path(tmp).glob("*.vtt"))
        transcript = _clean_vtt(vtts[0].read_text(encoding="utf-8")) if vtts else ""
    if not transcript:
        print("  warning: no captions found; source will have metadata only", file=sys.stderr)

    emit({
        "type": "youtube", "kind": kind, "title": title, "source": full_url,
        "id": vid, "date": date, "author": uploader, "duration": duration,
        "embed": f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{vid}" frameborder="0" allowfullscreen></iframe>',
        "suggested_slug": kb_lib.slugify(title),
    }, transcript)


# --- Web / forum ----------------------------------------------------------

def ingest_web(url: str, kind: str | None):
    if already_ingested(url):
        print(f"Already ingested: {url}")
        return
    try:
        import trafilatura
    except ImportError:
        _missing("trafilatura", "web pages / forums")
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        sys.exit(f"error: could not fetch {url}")
    text = trafilatura.extract(downloaded, include_comments=True, include_links=False,
                               favor_recall=True, output_format="markdown") or ""
    meta = trafilatura.extract_metadata(downloaded)
    title = (meta.title if meta and meta.title else url)
    date = (meta.date if meta and meta.date else datetime.now().strftime("%Y-%m-%d"))
    author = (meta.author if meta and meta.author else "")
    if not text.strip():
        sys.exit(f"error: no extractable content at {url}")
    emit({
        "type": "web", "kind": kind, "title": title, "source": url,
        "date": date, "author": author or "", "suggested_slug": kb_lib.slugify(title),
    }, text)


# --- PDF ------------------------------------------------------------------

def _parse_pages(spec: str | None, total: int):
    if not spec:
        return range(total)
    a, _, b = spec.partition("-")
    start = max(1, int(a)) - 1
    end = int(b) if b else int(a)
    return range(start, min(end, total))


def ingest_pdf(path: str, kind: str | None, pages: str | None, title_override: str | None):
    try:
        from pypdf import PdfReader
    except ImportError:
        _missing("pypdf", "PDFs")
    p = Path(path)
    reader = PdfReader(str(p))
    idxs = _parse_pages(pages, len(reader.pages))
    text = "\n\n".join((reader.pages[i].extract_text() or "") for i in idxs)
    info = reader.metadata or {}
    title = title_override or (info.title if getattr(info, "title", None) else p.stem.replace("-", " "))
    page_label = f" (pp. {pages})" if pages else ""
    emit({
        "type": "pdf", "kind": kind, "title": f"{title}{page_label}", "source": str(p),
        "date": datetime.now().strftime("%Y-%m-%d"), "author": getattr(info, "author", "") or "",
        "pages": pages or f"1-{len(reader.pages)}",
        "suggested_slug": kb_lib.slugify(f"{title}{('-' + pages) if pages else ''}"),
    }, text)


# --- Local documents ------------------------------------------------------

def _read_local(p: Path) -> tuple[str, str]:
    """Return (title, text) for a local file."""
    ext = p.suffix.lower()
    if ext in (".html", ".htm"):
        try:
            import trafilatura
        except ImportError:
            _missing("trafilatura", "HTML files")
        raw = p.read_text(encoding="utf-8", errors="ignore")
        text = trafilatura.extract(raw, include_comments=False, favor_recall=True,
                                   output_format="markdown") or ""
        meta = trafilatura.extract_metadata(raw)
        title = meta.title if meta and meta.title else p.stem
        return title, text
    if ext == ".docx":
        try:
            import docx  # python-docx
        except ImportError:
            _missing("python-docx", "Word documents")
        d = docx.Document(str(p))
        return p.stem, "\n\n".join(para.text for para in d.paragraphs)
    # txt / md
    return p.stem, p.read_text(encoding="utf-8", errors="ignore")


def ingest_local(path: str, kind: str | None, title_override: str | None):
    p = Path(path)
    if already_ingested(str(p)):
        print(f"Already ingested: {p}")
        return
    title, text = _read_local(p)
    if not text.strip():
        sys.exit(f"error: no extractable text in {p}")
    title = title_override or title
    emit({
        "type": "local", "kind": kind, "title": title, "source": str(p),
        "date": datetime.now().strftime("%Y-%m-%d"), "author": "",
        "suggested_slug": kb_lib.slugify(title),
    }, text)


def main():
    ap = argparse.ArgumentParser(description="Ingest a source into the knowledge base.")
    ap.add_argument("input", help="URL, file path, or directory")
    ap.add_argument("--type", default="auto",
                    choices=["auto", "youtube", "web", "pdf", "local"])
    ap.add_argument("--kind", default=None, help="note-kind hint recorded in metadata")
    ap.add_argument("--pages", default=None, help="PDF page range, e.g. 12-20")
    ap.add_argument("--title", default=None, help="override the source title")
    args = ap.parse_args()

    t = args.type if args.type != "auto" else detect_type(args.input)

    if t == "dir":
        files = [f for f in sorted(Path(args.input).iterdir())
                 if f.suffix.lower() in LOCAL_EXTS or f.suffix.lower() == ".pdf"]
        if not files:
            sys.exit(f"No ingestable files in {args.input}")
        print(f"Ingesting {len(files)} files from {args.input} ...")
        for f in files:
            sub = "pdf" if f.suffix.lower() == ".pdf" else "local"
            print(f"\n=== {f.name} ===")
            (ingest_pdf if sub == "pdf" else ingest_local)(
                *( (str(f), args.kind, args.pages, args.title) if sub == "pdf"
                   else (str(f), args.kind, args.title) ))
        return

    if t == "youtube":
        ingest_youtube(args.input, args.kind)
    elif t == "web":
        ingest_web(args.input, args.kind)
    elif t == "pdf":
        ingest_pdf(args.input, args.kind, args.pages, args.title)
    elif t == "local":
        ingest_local(args.input, args.kind, args.title)


if __name__ == "__main__":
    main()
