# Component contract and handoff: clockwise linkage pose stage

## Contract

- Issue #32 / Engine #1. Root integration owner; baseline PR104 `8c2d2d9a1400acf784e04581a61e6a6ede38d3ba`, canonical SHA `91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6`.
- Stage a serialized occurrence-only proposal for corrected inclined linkage rest frames. Preserve IDs, parents, definitions and nonmotion data. Set explicit candidate metadata; do not load with legacy dispatch or apply to canonical inventory.
- Owned files: this handoff, dedicated stage script/patch/report. CAD candidate modules and browser numeric helper are read-only dependencies. Coworkers own composed cam and front joint assets.
- Geometry dependencies: inclined head/gasket/passages, corrected crest/rocker, corrected cam and drive. Poses alone do not establish assembled acceptance.
- Use actual CAD candidate no-lift poses at each cylinder's firing TDC, not dynamic q=0 poses as rest. This prevents double valve displacement in the browser. Preserve mm and CAD axes, relative-to-parent transforms.
- Compare serialized neutral frames plus actual JS pose deltas with independent CAD linkage frames over selected poses/endplay. Tolerance 1e-8 matrix elements; deliberately shifted rest pose must fail. Springs remain separately labeled: metadata updated, compressed mesh/contact not verified here.

## Delivery / validation

Candidate stage executed; canonical untouched. `scripts/stage-clockwise-linkage-poses.py` writes the guarded occurrence patch and report. 228 updates comprise216 neutral linkage frames plus12 spring model tags. JSON replay plus JS motion deltas match CAD over2,592 frames at six event angles and both axial endpoints: maximum matrix difference1.137e-13. A1mm wrong-rest control fails. No-lift rest avoids double application of nonzero q=0 valve displacement.

`scripts/stage-clockwise-linkage-assets.py` binds three existing definition-local assets: inclined head, gasket and corrected crest rocker.14 occurrence world STEP/mesh bounds pass (<0.000006mm); intended single solids and closed consistent positive meshes checked. Patch changes neither IDs nor parents nor paths; it carries hash-bound copy proposals for later coordinated application. These are bounds/serialization checks, not new collision acceptance.

`node scripts/check-clockwise-spring-mesh.mjs` verifies12 actual rest/half/peak compressed meshes at both existing display resolutions (50,864 triangles): closed edges, outward winding and both ground caps. Exhaust minimumheight27.3047973134mm. No spring contact/sweep claim.

Commands fromrepo root use `XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python` for both stage scripts, then Node spring checker. Exact hashes are in `clockwise-linkage-pose-stage-validation.json`, `clockwise-linkage-asset-patch.json` and `clockwise-spring-mesh-validation.json` underinventory/engine. No temporary input artifact needed. Root authored/reviewed the stage; actual assembly/browser gates remain NOT RUN. Source dimensions and inferred linkage remain as classified in corrected cam and inclined-linkage handoffs. No original manuals/photos required. Reproduction uses CAD lock and Node, with exact input bindings. Board desired In progress; component remains open.
