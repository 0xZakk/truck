# Engine CAD pipeline

Start with [developer onboarding](../../docs/onboarding/START-HERE.md), [current checkpoint](../../docs/CURRENT-STATE.md) and the [quality standard](../../docs/onboarding/QUALITY-STANDARD.md). They supersede earlier atlas counts and startup instructions.

## Current conventions

The integrated checkpoint is an in-progress educational reconstruction. The canonical hierarchy is `inventory/engine/full-assembly.json`; definitions share geometry while occurrences retain physical identity. Individual pages use `viewer/part.html?id=<occurrence-id>`; the engine explorer is `viewer/engine.html`.

Engine CAD is in millimeters. The established exporter maps CAD `(x,y,z)` to GLB `(x,z,-y)` and divides by 1000 for glTF meters; the workbench displays at scale 1000. Verify the actual local frame and occurrence transform in the parent assembly before adding a part. Do not apply legacy full-truck mesh conventions to engine parts.

`full_engine.py` coordinates component builders; `assembly_math.py` and the valve dispatch modules implement shared transforms. Builder APIs vary: inspect the target module and record the exact integration call. `cad/engine/generated/` holds generated STEP; `models/engine/` holds committed browser meshes; evidence, learning and checks live in `inventory/engine/` with source provenance in the knowledge base/reference records.

## Working safely and reproducibly

Preview the committed viewer without rebuilding. Install the CAD environment and restore STEP inputs as described in onboarding and [artifact restoration](../../docs/CAD-ARTIFACTS.md). The tested lock targets macOS/Python 3.13; other environments require export/check verification.

Run a component's documented builder/checker in an isolated branch or worktree. Full and refresh commands write artifacts and may require a particular prior build stage; inspect their dependencies first. In particular, `--refresh-source-valves` expects its documented pre-adapter inputs, not an already adapted checkpoint. Do not blindly rerun it against restored current geometry. A clean-clone full rebuild across every historical candidate is not yet certified.

The integration owner chooses a coherent build path, reviews changed dependency hashes, regenerates affected assets and runs applicable static/interface/motion/browser checks. `node scripts/check-engine-navigation.mjs` is the baseline navigation check; passing it alone does not validate CAD. Current valve motion exists, but its validated scope and production limitations are in the current inventory reports.

Earlier pipeline notes are preserved in [the historical snapshot](../../docs/archive/engine-pipeline-before-onboarding-2026-09-26.md). They are useful research history, not the default build recipe.
