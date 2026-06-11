#!/usr/bin/env python3
"""
Semantic backlink generator — config-driven.

Embeds every atomic note in the knowledge base and links each one to its most
semantically similar siblings. Paths, link prefix, model and thresholds all come
from kb.config.json (see kb_lib), so this works for any knowledge base.

Usage:
  python tools/semantic_links.py embed                                  # build embeddings (first run / after adding notes)
  python tools/semantic_links.py report [--threshold 0.6]               # preview connection stats
  python tools/semantic_links.py inspect <slug>                         # nearest notes to one note
  python tools/semantic_links.py apply [--threshold 0.6] [--top-n 5] [--write]
"""

import json
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kb_lib  # noqa: E402

CFG = kb_lib.load_config()
CONTENT_DIR = CFG.abspath("notes")
DATA_DIR = CFG.abspath("data")
EMBEDDINGS_FILE = DATA_DIR / "embeddings.npz"
METADATA_FILE = DATA_DIR / "metadata.json"
NOTE_PREFIX = CFG.link_prefix("notes")
MODEL_NAME = CFG.semantic["model"]
DEFAULT_THRESHOLD = float(CFG.semantic.get("threshold", 0.6))
DEFAULT_TOP_N = int(CFG.semantic.get("top_n", 5))


def parse_note(filepath: Path) -> dict:
    """Extract title, slug, and body text (links/headings stripped) from a note."""
    text = filepath.read_text(encoding="utf-8")
    title_match = re.search(r'^title:\s*"?(.+?)"?\s*$', text, re.MULTILINE)
    title = title_match.group(1) if title_match else filepath.stem.replace("-", " ").title()

    parts = text.split("---", 2)
    body = parts[2].strip() if len(parts) >= 3 else text
    body = re.sub(r"\[\[.*?\|(.*?)\]\]", r"\1", body)
    body = re.sub(r"\[\[(.*?)\]\]", r"\1", body)
    body = re.sub(r"^#+\s+", "", body, flags=re.MULTILINE)
    return {"slug": filepath.stem, "title": title, "body": body, "path": str(filepath)}


def load_notes() -> list:
    notes = []
    for f in sorted(CONTENT_DIR.glob("*.md")):
        if f.stem in ("index", "_index"):
            continue
        note = parse_note(f)
        if note["body"]:
            notes.append(note)
    return notes


def cmd_embed():
    from sentence_transformers import SentenceTransformer

    print(f"Loading notes from {CONTENT_DIR} ...")
    notes = load_notes()
    print(f"Found {len(notes)} notes")
    if not notes:
        print("No notes to embed yet. Add notes first (kb-process).")
        return

    print(f"Loading model ({MODEL_NAME}) ...")
    model = SentenceTransformer(MODEL_NAME)
    print("Generating embeddings...")
    texts = [n["body"] for n in notes]
    embeddings = model.encode(texts, show_progress_bar=True, normalize_embeddings=True)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(EMBEDDINGS_FILE, embeddings=embeddings)
    metadata = [{"slug": n["slug"], "title": n["title"]} for n in notes]
    METADATA_FILE.write_text(json.dumps(metadata, indent=2))
    print(f"Saved {len(notes)} embeddings to {EMBEDDINGS_FILE}")


def load_embeddings():
    if not EMBEDDINGS_FILE.exists():
        sys.exit("No embeddings found. Run: python tools/semantic_links.py embed")
    data = np.load(EMBEDDINGS_FILE)
    metadata = json.loads(METADATA_FILE.read_text())
    return data["embeddings"], metadata


def compute_similarity(embeddings):
    return embeddings @ embeddings.T


def cmd_report(threshold=DEFAULT_THRESHOLD, top_n=DEFAULT_TOP_N):
    embeddings, metadata = load_embeddings()
    sim = compute_similarity(embeddings)
    n = len(metadata)
    np.fill_diagonal(sim, 0)
    upper = sim[np.triu_indices(n, k=1)]
    above = int(np.sum(upper >= threshold))
    total = len(upper)

    print("=== Semantic Similarity Report ===")
    print(f"Notes: {n}")
    print(f"Threshold: {threshold}")
    pct = (above / total * 100) if total else 0
    print(f"Pairs above threshold: {above} / {total} ({pct:.2f}%)")
    print(f"Average connections per note: {above * 2 / n:.1f}" if n else "")
    print("\nScore distribution:")
    for t in [0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.5]:
        count = int(np.sum(upper >= t))
        print(f"  >= {t:.2f}: {count:>6} pairs ({count * 2 / n:.1f} avg per note)" if n else "")

    print(f"\n=== Sample Connections (threshold >= {threshold}) ===")
    pairs = []
    for i in range(n):
        for j in np.argsort(sim[i])[::-1][:top_n]:
            if sim[i][j] >= threshold:
                pairs.append((sim[i][j], metadata[i], metadata[j]))
    pairs.sort(key=lambda x: -x[0])
    for score, a, b in pairs[:30]:
        print(f"  {score:.3f}  {a['title'][:50]:<50}  <->  {b['title'][:50]}")


def cmd_inspect(slug):
    embeddings, metadata = load_embeddings()
    sim = compute_similarity(embeddings)
    idx = next((i for i, m in enumerate(metadata) if m["slug"] == slug), None)
    if idx is None:
        print(f"Note not found: {slug}")
        print("Available slugs (first 20):", [m["slug"] for m in metadata[:20]])
        return
    print(f"=== Connections for: {metadata[idx]['title']} ({slug}) ===")
    scores = sim[idx].copy()
    scores[idx] = 0
    for rank, j in enumerate(np.argsort(scores)[::-1][:20], 1):
        print(f"  {rank:>2}. {scores[j]:.3f}  {metadata[j]['title']}")


def cmd_apply(threshold=DEFAULT_THRESHOLD, top_n=DEFAULT_TOP_N, dry_run=True):
    embeddings, metadata = load_embeddings()
    sim = compute_similarity(embeddings)
    np.fill_diagonal(sim, 0)
    n = len(metadata)
    slug_to_idx = {m["slug"]: i for i, m in enumerate(metadata)}
    changes = 0

    for i in range(n):
        slug = metadata[i]["slug"]
        filepath = CONTENT_DIR / f"{slug}.md"
        if not filepath.exists():
            continue
        ranked = np.argsort(sim[i])[::-1]
        matches = [metadata[j] for j in ranked[:top_n] if sim[i][j] >= threshold]
        if not matches:
            continue
        content = filepath.read_text(encoding="utf-8")
        new_matches = [m for m in matches if f"{NOTE_PREFIX}/{m['slug']}" not in content]
        if not new_matches:
            continue
        changes += 1
        if dry_run:
            print(f"\n{metadata[i]['title']}:")
            for m in new_matches:
                print(f"  + [{sim[i][slug_to_idx[m['slug']]]:.3f}] {m['title']}")
        else:
            new_links = [f"- [[{NOTE_PREFIX}/{m['slug']}|{m['title']}]]" for m in new_matches]
            if "## Related Concepts" in content:
                insertion = content.index("## Related Concepts")
                nxt = re.search(r"\n## ", content[insertion + 20:])
                insert_at = insertion + 20 + nxt.start() if nxt else len(content)
                content = content[:insert_at].rstrip() + "\n" + "\n".join(new_links) + "\n" + content[insert_at:]
            elif "## Source" in content:
                insert_at = content.index("## Source")
                content = content[:insert_at] + "## Related Concepts\n\n" + "\n".join(new_links) + "\n\n" + content[insert_at:]
            else:
                content = content.rstrip() + "\n\n## Related Concepts\n\n" + "\n".join(new_links) + "\n"
            filepath.write_text(content, encoding="utf-8")

    print(f"\n{'Would update' if dry_run else 'Updated'} {changes} notes")


def _flag(name, cast, default):
    for i, a in enumerate(sys.argv):
        if a == name and i + 1 < len(sys.argv):
            return cast(sys.argv[i + 1])
    return default


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    cmd = sys.argv[1]
    if cmd == "embed":
        cmd_embed()
    elif cmd == "report":
        cmd_report(threshold=_flag("--threshold", float, DEFAULT_THRESHOLD))
    elif cmd == "inspect":
        if len(sys.argv) < 3:
            sys.exit("Usage: semantic_links.py inspect <slug>")
        cmd_inspect(sys.argv[2])
    elif cmd == "apply":
        cmd_apply(
            threshold=_flag("--threshold", float, DEFAULT_THRESHOLD),
            top_n=_flag("--top-n", int, DEFAULT_TOP_N),
            dry_run="--write" not in sys.argv,
        )
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
