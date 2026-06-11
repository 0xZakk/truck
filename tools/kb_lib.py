#!/usr/bin/env python3
"""
kb_lib — shared helpers for the knowledge-base toolkit.

Every tool (ingest.py, semantic_links.py, check_feeds.py) loads the project's
`kb.config.json` through here, so paths and conventions live in one place and
nothing is hardcoded to a particular knowledge base.
"""

import json
import re
import sys
from pathlib import Path

CONFIG_NAME = "kb.config.json"

DEFAULT_CONFIG = {
    "name": "Knowledge Base",
    "domain": "",
    "paths": {
        "root": "kb",
        "sources": "kb/sources",
        "notes": "kb/notes",
        "maps": "kb/maps",
        "raw": "kb/.raw",
        "data": "tools/data",
    },
    "note_kinds": ["concept"],
    "link_prefixes": {"sources": "sources", "notes": "notes", "maps": "maps"},
    "semantic": {"model": "BAAI/bge-base-en-v1.5", "threshold": 0.6, "top_n": 5},
    "feeds": [],
    "frontend": None,
}


def find_config(start: Path | None = None) -> Path | None:
    """Walk upward from `start` (or cwd, then this file's dir) to find kb.config.json."""
    candidates = []
    if start:
        candidates.append(Path(start).resolve())
    candidates.append(Path.cwd().resolve())
    candidates.append(Path(__file__).resolve().parent)        # tools/
    candidates.append(Path(__file__).resolve().parent.parent)  # project root

    seen = set()
    for c in candidates:
        d = c
        while d not in seen:
            seen.add(d)
            cfg = d / CONFIG_NAME
            if cfg.exists():
                return cfg
            if d.parent == d:
                break
            d = d.parent
    return None


def _deep_merge(base: dict, override: dict) -> dict:
    out = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


class Config:
    """Loaded kb.config.json with resolved absolute paths."""

    def __init__(self, config_path: Path):
        self.path = config_path
        self.root = config_path.parent
        raw = json.loads(config_path.read_text(encoding="utf-8"))
        self.data = _deep_merge(DEFAULT_CONFIG, raw)

    # --- convenience accessors -------------------------------------------
    @property
    def name(self) -> str:
        return self.data["name"]

    @property
    def domain(self) -> str:
        return self.data["domain"]

    @property
    def note_kinds(self) -> list:
        return self.data["note_kinds"]

    @property
    def semantic(self) -> dict:
        return self.data["semantic"]

    @property
    def feeds(self) -> list:
        return self.data.get("feeds", [])

    def abspath(self, key: str) -> Path:
        """Absolute path for a configured path key (sources, notes, maps, raw, data, root)."""
        rel = self.data["paths"][key]
        return (self.root / rel).resolve()

    def link_prefix(self, key: str) -> str:
        return self.data["link_prefixes"][key]


def load_config(start: Path | None = None) -> Config:
    cfg = find_config(start)
    if cfg is None:
        sys.exit(
            f"error: no {CONFIG_NAME} found (searched up from cwd). "
            f"Run the kb-init skill to scaffold a knowledge base first."
        )
    return Config(cfg)


# --- generic text helpers ------------------------------------------------

def slugify(text: str) -> str:
    """Convert text to a filesystem-safe slug."""
    text = (text or "").lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")[:80] or "untitled"


def frontmatter_value(text: str, key: str) -> str | None:
    """Pull a simple scalar value out of YAML frontmatter."""
    m = re.search(rf'^{re.escape(key)}:\s*["\']?(.+?)["\']?\s*$', text, re.MULTILINE)
    return m.group(1) if m else None


def existing_source_keys(sources_dir: Path) -> set:
    """Set of identifiers (source URLs + ids) already present in sources/, for de-dupe."""
    keys = set()
    if not sources_dir.exists():
        return keys
    for f in sources_dir.glob("*.md"):
        text = f.read_text(encoding="utf-8", errors="ignore")
        for key in ("source", "id", "videoId", "url"):
            v = frontmatter_value(text, key)
            if v:
                keys.add(v.strip())
    return keys
