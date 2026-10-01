# Component contract and handoff: core and drive serialized integration stage

## Contract before staging

Issues #32/#34, root sole canonical/motion integration owner; pan_access_resume owns new stage assets, scripts, patch proposals and reports. Creation baseline26d0fdc4e7cdd3de0c621309499d1535d8c5131e; engine/timing-drive-fit. Canonical manifest SHA91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6. Coordinate root's216-frame valvetrain/spring neutral stage and pump worker's separate frontjoint assets; do not edit either.

Ready neutral core serialization scope: corrected crank, composed corrected cam, two timing gears, rigid key/spacer, four stationary bearings, rear plug, plate and its two bolts/washers. Use frozen coupled-core occurrence-world assets except corrected crank/composed cam overrides. Convert each explicitly through target occurrence world frame inverse; never apply occurrence-world exports directly to local definitions. Preserve IDs, parents and explode fields. Shared repeated bearing/bolt/washer definitions must reconstruct every occurrence before inclusion.

Core pose proposal shifts cam-motion neutral parent to the revised axis, shifts cam-retention-assembly by the declared delta, and moves four bearing/rear-plug occurrence datums. Motion tags remain unchanged pending root's explicit corrected crank/cam/endplay JS implementation. A neutral serialized patch is not runnable corrected animation by itself.

Separate conditional drive proposal: shift distributor-assembly/oil-drive-assembly/oil-pump-assembly by delta[0,5.109820990161097,4.087856792128875], preserve their rotations and descendants, and replace distributor gear only in its original definition-local frame (corrected gear-centered source translated localZ−85). Do not silently include oil-pickup-assembly. Source inlet point is oil_drive_layout.PUMP_FRAME*[-34,0,5]; moving pump without changing tube displaces that connection. Block outlet, distributor clamp/seat/harness/wire reach and pickup/screen placement require independent ownership/evidence; failed or unresolved links keep branch proposal conditional.

Acceptance: hash-guarded before/after definition/assembly/occurrence objects, no canonical writes; actual staged STEP reconstructed world bounds<0.01mm, mesh vertices<0.01mm, mesh/CAD bounds per inherited0.15mm, solid/face preservation and positive watertight export. Validate repeated definition localization, descendants, stable IDs/parents and serialized replay. Reject stale manifest/before object/asset hash. Carry through only reports with verified hashes and documented scope; no manufacturing, oil pressure, whole-engine/browser or new spring acceptance. All source estimates remain estimates.

## Delivery

Readiness: serialized candidate ready for root composition, **not installed**. Canonical manifest, shared builder/runtime and other workers' assets remain unchanged. Three separate guarded proposals:

1. `inventory/engine/timing-core-integration-patch.json`:11 definition-local replacements serving16 core occurrences; two assembly neutral translations; five bearing/rear-plug occurrence translations. Existing identity/parent/explode fields preserved.
2. `inventory/engine/timing-corrected-slider-neutral-patch.json`:12 rod/piston groups receive explicit `event_phase_deg` and `physical_rest_phase_deg=−event`; original `phase_deg` is retained as event metadata.90 descendant occurrence neutral world matrices are supplied as a contract, not an extra transform. Root's corrected runtime must consume the physical phase once. Old runtime remains invalid for this purpose.
3. `inventory/engine/timing-conditional-drive-integration-patch.json`:one localized corrected distributor-gear definition and three parent translations covering45 occurrences. This is explicitly conditional; pickup assembly stays unchanged and external connection gates remain open.

Local assets are in `cad/engine/generated/timing-core-drive-integration-stage/`; canonical destination paths and exact staged asset hashes are embedded in each definition patch. Source world exports are inverted through each intended occurrence frame. Repeated bearing/bolt/washer definitions have exact local two-way differences0 across their uses. The distributor source required localZ−85 conversion; supplying its gear-centered source directly would produce79.873873mm world-coordinate error.

No gear/profile, spring, block, pan, frontjoint, pickup or bearing dimensions were changed. Evidence classes and omissions inherit frozen inputs: qualified replacement/source dimensions stay qualified, estimates remain estimates, production calibration/fit unknowns remain open. Moving a model part does not establish factory routing or oil flow.

## Results

`timing-core-drive-stage-review.json` records16 reconstructed core occurrences: maximum STEP world-bounds error8.90e−12mm, mesh vertex error3.72e−6mm, mesh/CAD world-bounds error0.01289909mm, volume roundtrip difference0.00017882mm³. Intended solid/face counts, positive volume and welded watertight/winding-consistent meshes pass. Repeated definition identity passes without creating duplicate IDs.

`timing-corrected-slider-neutral-review.json` records12 groups/90 descendants, independent journal-center error0; old rest-frame fault reaches103.092633mm. This demonstrates why corrected crank geometry cannot use old rest poses. Neutral frames preserve measured crank throw centers and positive event scheduling; it is not a fresh whole-engine collision study.

`timing-core-drive-stage-replay.json` replays all proposals in memory, checks before objects, immutable IDs/parents and asset hashes, and detects stale manifest, stale before object, bad asset hash and duplicate ownership. Core frame error0; distributor mesh world-vertex error3.47e−6mm. All retained45 branch STEP/GLB assets are also bound. Source neutral linkage/asset patch ownership is disjoint from root's228 occurrence/three-definition stage. No canonical file is written.

External connection finding: shifted pump versus unchanged source pickup inlet differs6.543763726209mm. The source tube begins at pump localX−34,Y0,Z5; the remaining spline and rear bell/screen are fixed. Therefore the pickup is intentionally absent from the rigid branch proposal. Inclined-linkage worker owns a separate upstream connection audit/revision. It also identified that the source housing lacks a complete discharge/block route and the exact-year procedure calls a pump gasket; pump feet and shaft alignment cannot certify that oil circuit. Distributor mounting/clamp, harness/wire reach, chosen block support compatibility and strainer/pan placement require their own checks.

## Reproduction and evidence

From repository root:

```
.venv-cad/bin/python scripts/stage-timing-core-drive-assets.py
.venv-cad/bin/python scripts/stage-corrected-slider-neutral-poses.py
.venv-cad/bin/python scripts/verify-timing-core-drive-stage.py
```

Environment: macOS, Python3.13/build123d0.10 with numpy/trimesh, existing environment only. Logs are `cad/engine/generated/timing-core-drive-stage-console.txt` and tool-reported slider/replay results. Required assets are all repository-relative; release publication/restoration belongs to root. Existing actual renders in composed-cam, corrected-crank and coupled-core handoffs remain the geometry views because this stage only serializes unchanged solids; no new visual-fidelity claim. New preview/browser rendering is NOT RUN. Model/effort/usage unavailable.

Bound source reports include composed-cam proof/delivery, coupled-core, corrected crank, endplay and original direction studies. Their hashes are verified, but a binding is not automatic promotion of excluded checks: old full-direction failures, factory unknowns, whole-engine contact limits and external branch gaps remain explicit. Core retention/all-angle support results apply only to the unchanged supported regions/rigid members, not a whole corrected engine.

## Quality gates

| Gate | Result | Limit |
|---|---|---|
| Application/coverage | PASS declared serialized scope; production completeness NOT RUN |16 core occurrences and45 conditional branch occurrences only |
| Dimensions/coordinates | PASS | explicit inverse world-to-local frames, repeated definitions and neutral physical phases |
| CAD/export | PASS stage | intended solids/faces, world reconstruction, positive/watertight meshes |
| Source/visual comparison | Existing geometry evidence reused; new factory comparison NOT RUN | no shape revision in this stage |
| Installed interfaces | NOT RUN installed; local proof bindings only | pickup/discharge/clamp/external block joints still open |
| Motion/disassembly | Neutral contracts PASS; corrected runtime owned by root | old legacy runtime explicitly not accepted; whole-engine sweep/disassembly NOT RUN |
| Learning/diagnostics | NOT RUN | no lesson produced |
| Browser integration | NOT RUN | canonical remains unchanged |
| Reproduction/review | PASS in-memory replay and adversarial guards | root private composition and review next |

## Tracking and restart

Frozen stage complete, no process remains. Root next action: privately compose core and slider proposals with neutral linkage/spring and frontjoint patches using the isolated corrected runtime, verify new matrices and chosen assets, and keep the conditional drive proposal separate until external connection work is accepted. Root owns all shared integration and publishing. Issues #32/#34 remain open. No request to install, no implicit oil-pressure/containment acceptance.
