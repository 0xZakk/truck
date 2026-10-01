# Contract: corrected private stage changed-neighbor static audit

Root requested an independent q=0,axial=0 audit of exact `inventory/engine/corrected-engine-stage.json`, using its overridden STEP paths and opt-in `assembly_clockwise_candidate.transforms`. Canonical remains unchanged. Own only this audit script/report/witness folder/handoff. Compare actual definition STEP SHA-256 and actual world matrices against canonical atq0; all changed/new occurrences are targets. No part-name or intended-contact whitelist. Broad phase uses conservative actual CAD bounds, then exact intersections for every potentially overlapping pair containing a target. Unchanged pairs may reuse only the named hash-bound canonical static evidence and exact shape+frame identity; no whole-motion or factory proof.

Use historical0.1mm³ overlap convention unchanged. Save positive overlaps and metric exceptions, with pair IDs and locatable bounds/witnesses. Incomplete main-cover gasket/terminal sealant,2692seal/hub, rod-bolt/block and shifted pickup/pump interfaces remain open; lack of a collision does not prove absent parts, seal contact or oil flow. Spring geometry authority must be explicit: saved shared spring meshes alone cannot stand in for correct compressed occurrence shapes. If root supplies an isolated shape API, bind and use it; otherwise flag spring scope as unresolved rather than call false overlaps accepted/cleared.

Actual source/local-frame consistency is tested through stage/source hashes and independent world placement matrices. Keep source dimensions estimated. Root owns integration and interpretation of each reported defect; no geometry edits or canonical promotion by this checker.

## Delivery and evidence ledger

Completed diagnostic study, **FAIL static staged assembly; not installed**. Issues #32/#34, integration owner root, contributor pan_access_resume. Delivery branch engine/timing-drive-fit, checkpoint8c2d2d9a1400acf784e04581a61e6a6ede38d3ba. Exact private manifest SHA-256 `c09eca9a670b9d6241f04b8e082929cdf864e5c8498bed9b65bc0211d530f342`;742 definitions/1,356 occurrences. Canonical unchanged. Geometry and transforms use millimeters and actual private-stage paths; no shape rebuilt except the explicitly supplied corrected spring occurrence API.

All geometry dimensions retain their source classifications. This audit establishes model intersections and identifies their revision origin; it does not validate Ford factory contours, manufacturing strength or a permissible clearance repair. Existing missing sealing parts and flow routes remain missing regardless of intersection results.

## Results

336 occurrences changed by STEP bytes, world transform or explicit spring deformation.1,020 occurrences have identical STEP bytes and q0 world matrices. Actual conservative CAD bounds separate396,788 affected pairs;2,212 potentially intersecting changed-neighbor pairs received exact CAD intersections.519,690 pairs between unchanged occurrences reuse only the bound canonical static evidence. No contact whitelist or mesh-only collision filter was used.

There are **77 positive-overlap pairs above0.1mm³**, all confirmed by converged adaptive integration;0 metric exceptions in the completed audit.60 intersection solids provided a strict interior center witness. For the other17, the center falls outside an annular/irregular region; the exact saved intersection STEP and converged positive volume remain evidence, without inventing a point witness. All77 exact world-coordinate intersection files are retained in `cad/engine/generated/corrected-stage-changed-neighbors/` and bound by hashes.

| Category | Pairs | Representative actual overlap |
|---|---:|---|
| Changed block / FS10 internals |6|rear cylinder3,773.224469mm³; shaft3,200.293502mm³ |
| Changed cover / external neighbors |10|front FS10 cylinder17,596.474199mm³; pump housing2,550.395221mm³; pump gasket61.130672mm³; PS/AC bracket575.951442mm³ |
| Pending old seal/hub replacement |2|old front seal3,845.309408mm³; old hub480.663676mm³ |
| New main-cover hardware |3|screw3/pump housing19.265671mm³; screw6/FS10 shaft250.302411mm³ and piston5 199.235124mm³ |
| Shifted distributor / unchanged ignition leads |56|28 cap and28 terminal overlaps with jacket, core, boot and contact components; cap/boot up to527.641779mm³ |

Full exact values, IDs, bounds and witness paths are in `inventory/engine/corrected-stage-changed-neighbors.json`. Volumes for separate pairs must not be summed as a unique intersecting-material volume.

Fresh canonical q0 comparisons confirm **zero overlap for all74 pairs whose two IDs existed canonically**. The remaining3 pairs involve newly added main-cover screws. Consequently none of these77 findings is an inherited canonical-neutral intersection. This statement is about the canonical baseline, distinct from inheritance inside the earlier isolated V3 candidate.

## Exact block-stock attribution

Source before seven supports is frozen `timing-front-block-expanded-seat-v3-candidate/block.step`. All six compressor neighbors retain their canonical poses/assets. Current intersection portions were compared directly with that source stock; new positive stock is wholly attributed to the analytic station6 support at Y251.916806725,Z74.423690331, radius8, X354.575..373.

| Compressor neighbor | Prior V3 overlap mm³ | New station6 stock overlap mm³ | Old overlap removed by new socket mm³ | Current overlap mm³ |
|---|---:|---:|---:|---:|
| rear cylinder |3773.224469|0|0|3773.224469|
| swashplate shaft |3184.202986|149.711263|133.620745|3200.293502|
| piston5 |0|312.432079|0|312.432080|
| rear shoe5 |349.306661|0|0|349.306661|
| front shoe5 |34.180035|0|0|34.180035|
| case bolt5 |282.743339|0|0|282.743339|

Thus four conflicts are entirely inherited from the isolated V3 block, piston5 is entirely introduced by station6 stock, and the shaft is mixed. The new-stock STEP witnesses are separately retained as `new-seven-support-stock__*.step`. This is attribution only; no blanket subtraction or block modification was performed.

The pump worker's separately frozen `timing-waterpump-cover-datum-audit.json` is bound by the summary. It locates the pump interference earlier in the cover construction: canonical0; early shell housing3,062.986684/gasket14.987075mm³; frontjoint/v2/2692 3,709.283500/61.130672mm³; main-seven recesses reduce housing overlap to2,550.395221mm³; pan21 changes none. This does not justify retaining the interference or changing the pump by eye.

## Controls, limits and retained failures

An artificial crank translation +100mm inZ against the exact staged block produces716,014.524233mm³ overlap and a strict interior witness. This establishes detector sensitivity; it is clearly separated from the77 actual findings.

The first import-only run was stopped when root supplied the explicit corrected spring geometry authority; it is retained under `rejected-before-spring-authority` and contributes no pair acceptance. The completed run uses `assembly_clockwise_candidate.occurrence_shape` atq0,axial0 for actual compressed springs. No spring overlap appears in this completed pose.

Classifier implementation failures—ShapeList normalization and attempting to intersect empty added stock—are preserved under the two `rejected-classifier-*` folders. Fixes only normalize returned containers and skip nonexistent stock; no dimension, threshold, pose or input shape changed. The original completed audit remained untouched.

No q0 rod-bolt/block hit was found, but the prior motion-phase failure remains open. Absent main-cover gasket/terminal sealant, pending2692 seal/hub selection, pump mounting gasket/discharge architecture and ignition wire connection acceptance cannot be established by a static non-overlap test. The new pickup-reconnection candidate is not present in this exact stage; its existence does not silently resolve this snapshot's6.5438mm inlet displacement.

## Reproduction and review

From repository root:

```
.venv-cad/bin/python scripts/check-corrected-stage-changed-neighbors.py
.venv-cad/bin/python scripts/check-corrected-stage-audit-control.py
.venv-cad/bin/python scripts/classify-corrected-stage-overlaps.py
python3 scripts/summarize-corrected-stage-neighbor-audit.py
```

Environment: existing macOS Python3.13/build123d0.10, numpy; no installs. Console files live under `cad/engine/generated/corrected-stage-*.txt`. Reports bind private/canonical manifests, actual STEP files, adapter/deformation sources, exact witnesses and source-stock comparisons. The summary additionally verifies frozen cam/valve transitive sources and the independent waterpump audit. All inputs are repository-relative; artifact publication/restoration belongs to root. No new raster rendering or browser check was performed; exact STEP witnesses are the locatable visual artifacts. Usage/model-effort unavailable.

| Quality gate | Status and scope |
|---|---|
| Application/coverage |PASS declared single-pose changed-neighbor coverage; production/BOM completeness NOT RUN|
| Dimensions/coordinates |PASS actual overridden paths, adapter transforms, source byte/matrix comparisons|
| CAD/export |PASS77 saved intersection witnesses; original component integrity inherited by bound sources, not newly certified|
| Source/visual comparison |PASS revision/stock comparison; factory image comparison NOT RUN|
| Installed interfaces |FAIL77 positive-overlap pairs; open missing connections retained|
| Motion/disassembly |NOT RUN beyondq0; prior motion failures unchanged|
| Learning/diagnostics |NOT RUN user-facing lesson; actual interference controls and attribution are engineering evidence|
| Browser integration |NOT RUN; private stage only|
| Reproduction/review |PASS hash-bound completed checks; root repair/acceptance review remains required|

Root's next action is interface-specific source/geometry review of the block/cover/accessory conflicts and coordinated ignition-lead/attachment proposals. Do not turn these witnesses into neighbor-shaped clearance cutters. Frozen audit complete; no process remains. The stage is not accepted and no canonical or source geometry was edited.
