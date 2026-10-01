# Front seal integration stage

## Contract

Root owns this separate asset-staging step for #32, baseline `a66b33cdbb33c77fb74167bbe814b8e646660e47`, branch `engine/timing-pan-seal-joints`. Inputs are the frozen 2692 delivery, canonical manifest, and existing assembly transform helper. World CAD units are millimeters; browser meshes use the existing `(X,Z,-Y)/1000` basis.

Convert the world-space candidate cover and hub into the existing occurrence-local frames, preserving their parents and motion. Stage the three separate seal constituents under a proposed stationary `front-seal-assembly`, positioned at the old seal occurrence datum. The existing `front-seal` identifier must remain a navigation alias to that assembly when the future coordinated installer retires the old annular definition. Do not install the seal candidate independently of the revised timing cover and surrounding assembly.

Owned files: this handoff, `scripts/stage-front-seal-2692-assets.py`, its dedicated generated folder and validation report. No canonical files or frozen candidate assets may change. Exclude the free-case comparison from the installed component count. Readiness remains candidate.

## Planned validation

Verify every frozen delivery binding, preserve canonical poses for cover/hub, export localized STEP, and reconstruct world-space bounds. Translate the already verified native GLB without retessellation; check every reconstructed vertex against the original world mesh and retain watertightness/winding. A deliberately doubled placement must fail the same placement tolerance. The stage writes an explicit five-part registration proposal, not a full engine manifest or installed acceptance. Applicable local export/coordinate gates must pass; source fidelity and local contact evidence reuse the frozen delivery. Combined engine interfaces, disassembly, old-link alias handling and browser acceptance remain NOT RUN.

Command: `.venv-cad/bin/python scripts/stage-front-seal-2692-assets.py`. Use the existing CAD environment. Root reviews the report before any promotion. Large generated files follow `docs/CAD-ARTIFACTS.md`; no purchased sources or owner photographs are copied. Model/usage unavailable.

## Delivery

All five localized STEP/GLB pairs pass. Reconstructed STEP world bounds are unchanged; maximum GLB vertex error is below 0.000001 mm. Face topology is preserved and all five meshes remain watertight with consistent winding. Deliberately applying placement twice produces errors over 100 mm and is rejected. The canonical manifest and frozen source assets retain their original hashes. Report: `inventory/engine/front-seal-2692-stage-validation.json`; generated assets: `cad/engine/generated/front-seal-2692-integration-stage/`. No background process remains for this step.

This resolves asset-coordinate preparation only. The coordinated installer must still register the three seal parts, learning/source records, assembly and old deep-link alias, then validate the revised complete timing neighborhood and browser behavior. Do not load this asset stage as an accepted full-engine manifest.
