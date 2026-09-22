# Archived whole-truck prototype

Archived on 2026-09-22 at the owner's request. This is historical work, not the
current reconstruction or a source of verified geometry. New development belongs
in `viewer/atlas.js`, `cad/engine/`, `models/engine/` and `inventory/engine/`.

Open `/archive/2026-09-22-legacy-truck/viewer/` using the normal repository server
(`python3 scripts/serve.py` from the repository root). The archive retains the old
viewer, procedural builders, lighting asset, mesh exports, CAD sources, inventory
and associated modeling scripts. Its viewer reads its own archived inventory and
models. The engine link leads to the current explorer.

Manuals, reference photos, knowledge-base sources, the extracted parts catalog
(`inventory/bom.json`) and its extraction script remain in their original locations
for use in the new reconstruction. The current piston study is also retained.

`original-file-hashes.json` records the original locations and SHA-256 hashes of
all moved files. Archive routing, the archive title and helper script paths were
adjusted after moving; inventory model paths were made archive-relative. All model geometry and other
inventory fields are unchanged.
Historical CAD scripts may depend on the original locally installed tools.
