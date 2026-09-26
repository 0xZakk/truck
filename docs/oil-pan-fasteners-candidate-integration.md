# Oil-pan fastening candidate integration

This isolated candidate adds two definitions and fifty occurrences: 25 source-counted screw/washer pairs. It does **not** establish a measured pan-hole pattern or complete the gasket. Do not promote an isolated pass to a full assembled-engine pass.

## Integration

1. Import `oil_pan_fasteners` in `cad/engine/full_engine.py`.
2. Apply `oil_pan_fasteners.block_interface(block)` to the final block before `define('block', ...)`. Retain existing interface adapters. Append this module's sources and limitations to the block's evidence.
3. At **both** `build_oil_pan(...)` call sites, wrap the existing six-element API tuple with `oil_pan_fasteners.pan_api(...)`. It drills the pan and both existing side gasket studies in their definition-local frames.
4. Immediately after the initial oil-pan build call, call `oil_pan_fasteners.build((define, add, group))` once. The new branch is `oil-pan-fastener-assembly`, parent `oil-pan-assembly`.
5. Merge `inventory/engine/oil-pan-fasteners-learning.json` into the normal learning registration. The existing `truck-oil-pan-hardware` source registration supports the facts; a separate assumption record is `reference/engine/oil-pan-fasteners-candidate-evidence.json`.
6. Rebuild; inspect the assembled and exploded pan views; verify newly installed STEP shapes against the isolated candidate. Run current full static and navigation/source audits. Do not silently relax overlap thresholds.

## Isolated checker

`.venv-cad/bin/python scripts/check-oil-pan-fasteners-candidate.py`

It tests six single-solid STEP roundtrips, all 25 screw/washer contacts, pan bearing areas, open blind sockets and their solid floors, and static neighbors. Its saved manifest hash identifies the audited starting assembly. Use `--installed` after integration. That mode reads installed hardware, checks its symmetric difference against the intended screw/washer shapes, and skips self/duplicate candidate comparisons. Full-root static QC must additionally cover the altered block. Both modes fingerprint every loaded STEP and reject a changing assembly.

## Important limits

Ford's diagram establishes 25 assemblies, nominal 5/16-18 thread and .87-inch screw length. It supplies no measured coordinate table. The candidate uses an explicitly arbitrary 13/12 side-rail arrangement. Washer/head details, retaining construction, block pads, socket geometry, clearances and thread form remain illustrative. The washers are represented as separate pieces without a verified captive construction. The existing flange geometry and incomplete side-gasket studies are retained apart from holes. No clamp-load, oil-tightness or production-fit assertion is made.
