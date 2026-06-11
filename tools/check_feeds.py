#!/usr/bin/env python3
"""
Feed checker — find sources you haven't ingested yet.

Reads `feeds` from kb.config.json and compares each feed's items against the URLs
and ids already present in sources/. Prints the new items so the kb-add-source
skill (or you) can decide what to ingest. Does NOT ingest anything itself.

feeds entries look like:
  { "type": "youtube", "channel_id": "UCxxxx", "label": "Some Channel" }
  { "type": "rss",     "url": "https://forum.example.com/forum/5.rss", "label": "Forum X" }

Usage:
  python tools/check_feeds.py
"""

import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kb_lib  # noqa: E402

CFG = kb_lib.load_config()
SOURCES_DIR = CFG.abspath("sources")

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
}


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (kb-toolkit)"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def parse_youtube(channel_id: str) -> list:
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    root = ET.fromstring(fetch(url))
    items = []
    for entry in root.findall("atom:entry", NS):
        vid = entry.find("yt:videoId", NS)
        title = entry.find("atom:title", NS)
        if vid is None:
            continue
        items.append({
            "id": vid.text,
            "title": title.text if title is not None else vid.text,
            "url": f"https://www.youtube.com/watch?v={vid.text}",
        })
    return items


def parse_rss(url: str) -> list:
    root = ET.fromstring(fetch(url))
    items = []
    # RSS 2.0
    for it in root.iter("item"):
        link = it.findtext("link") or ""
        title = it.findtext("title") or link
        items.append({"id": link, "title": title, "url": link})
    # Atom
    for entry in root.findall("atom:entry", NS):
        link_el = entry.find("atom:link", NS)
        link = link_el.get("href") if link_el is not None else ""
        title = entry.findtext("atom:title", default=link, namespaces=NS)
        items.append({"id": link, "title": title, "url": link})
    return items


def main():
    feeds = CFG.feeds
    if not feeds:
        print("No feeds configured. Add a `feeds` array to kb.config.json.")
        return 0

    have = kb_lib.existing_source_keys(SOURCES_DIR)
    total_new = 0
    for feed in feeds:
        label = feed.get("label", feed.get("url") or feed.get("channel_id", "?"))
        try:
            if feed.get("type") == "youtube":
                items = parse_youtube(feed["channel_id"])
            else:
                items = parse_rss(feed["url"])
        except Exception as e:  # noqa: BLE001
            print(f"[{label}] error: {e}", file=sys.stderr)
            continue
        new = [it for it in items if it["id"] not in have and it["url"] not in have]
        print(f"\n[{label}] {len(items)} in feed, {len(new)} new:")
        for it in new:
            print(f"  - {it['title']}\n    {it['url']}")
        total_new += len(new)

    print(f"\nTotal new sources available: {total_new}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
