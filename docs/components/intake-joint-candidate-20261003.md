# Coordinated intake joint educational candidate

## Contract frozen before CAD

Issue #82/intake under engine #1; root integrates. Baseline 4f1fe9da2ec177e1ff61668df66ca422e37b0b7c. Research candidate only; owned prefix files in cad/engine, scripts, generated and this handoff. No shared builder/manifest changes. Root explicitly accepts existing modeled terminal span as educational packaging scale, not a Ford dimension.

`cad/engine/intake-joint-candidate-20261003-parameters.json` SHA256 `4ee45b936aac6200273e8675af2e14f75e843c2cc74b36ad7d9cb7e3d5c5658e` freezes all geometry choices before CAD. Current `upper_intake_clearance_candidate.PORTS` endpoints ±284.48 give568.96mm. World P1=(284.48,-228,360), P6=(-284.48,-228,360). The six unequal source stations replace equal spacing without changing endpoints. No neighbor-clearance objective determines dimensions.

Actual casting view1 places the ACT/front ear away from the head flange and the center aperture toward it. Accordingly u maps-X and image v maps-Y. This is a source-compared face-sign inference, not calibrated orientation. Port diameter50mm is a rounded photo-proportion estimate at the explicitly accepted568.96 scale (approximately105/1209.8×568.96=49.4mm); gasket aperture51mm. Small apertures11mm. Flange10mm and gasket1.5mm thicknesses inherit current estimated stack. Outer circular pads32mm radius, connecting web24mm width, ear11mm radius are explicit approximate contours. No production tolerance or flow prediction.

Seven stable stud hypotheses use H1,H2,H4,H5,H6,H8,H9; studs3/5 remain unresolved alternatives, not accepted fastening roles. All nine gasket holes remain modeled. No new hardware or head-locator reinterpretation.

Versioned adapter plan: build an isolated coordinated successor using new shared layout, regenerate lower joint-side runner portions while retaining original head-side paths and seats; regenerate upper paths with existing plenum endpoints and preserved throttle/EGR/vacuum interfaces. Existing historical compact/exterior/runner guards and fixtures remain untouched. A future adapter replaces three definitions and seven explicitly mapped transforms only after root reviews this candidate. It must retain/apply existing lower head-dowel/lifting-eye/rear-mount adapters. No integration call is added now. Existing exterior shoulders cannot silently remain on old paths; candidate rebuilt paths supersede them. Decorative exterior fidelity omitted in initial geometric trial must be reported, not mistaken for an accepted replacement.

Plan: verify valid one-solid parts, coordinated openings/stack and protected datums, exported STEP/mesh bounds; demonstrate shifted-port/blocked-passage/mirrored-hole negative controls. Source comparison uses local original overlay only and shareable authored feature/CAD renders. Whole-assembly installed clearance, motion and browser acceptance remain NOT RUN unless actually tested. Conflicts will be reported rather than relocating adjacent systems.

### Construction amendment before retry

The variable-section upper loft caused a dropped flange, then an invalid union when the flange was restored. Retain those failures. Retry with circular sweeps at the already frozen32mm outer/25mm inner radii throughout each upper runner; this changes the inferred runner/plenum mouth diameter from the old16.5mm radius but preserves all six endpoint coordinates and external throttle/EGR/vacuum datums. No neighbor clearance drives this choice. Source does not resolve internal taper. This is an explicit simplified constant-section educational construction; report neighboring effects and do not transfer old upper-air-volume acceptance.

### Flange-pad construction amendment

A focused Boolean diagnostic found coincident32mm runner/pad outer surfaces responsible: both solids independently contain points in the5mm overlap, but ordinary and fuzzy unions retain two solids. A33mm pad with the unchanged32mm runner fuses into one valid solid. Revise only flange-pad outer radius to33mm on both castings and gasket; this creates an explicit1mm exterior lip and avoids coincident skins. All source-derived centers, bores, dimensions at protected interfaces and acceptance tolerances stay unchanged. This is a revised approximate flange contour, not a source measurement or clearance adjustment. The33mm contour must be source-reviewed and is recorded in a separate amendment file; original parameter freeze remains intact.

## Delivery

Readiness: **candidate, not integration-ready**. Three coordinated STEP/GLB parts and seven stable stud occurrence hypotheses are available in `cad/engine/generated/intake-joint-candidate-20261003/`. The new unequal stations, offset central hole and opposite end ears are implemented together. Paired holes remain separate apertures; no new hardware is invented. `build.json` records all seven proposed positions and marks every occurrence unaccepted, with unresolved roles for3/5. Existing smooth stud geometry/length is not validated for the changed stack; no fastening acceptance is claimed.

Entry point: `cad/engine/intake-joint-candidate-20261003.py:parts()` returns `{stable_id: shape}, lower_paths, upper_paths`. It uses the current compact plenum/end-interface stations but intentionally omits historical upper lettering/ribs/broad exterior shoulders. The lower head-side Bezier segment is retained via a de Casteljau split at0.65; only the joint-side segment and its section expand/move. Injector sockets, rail mounts, head flange and three existing lower-interface adapters are regenerated at their original datums. ACT boss geometry is not added and its axis remains unresolved. No full-engine integration hook, manifest, shared code or canonical assets changed.

Commands from repository root:

```sh
.venv-cad/bin/python scripts/intake-joint-candidate-20261003-build.py
.venv-cad/bin/python scripts/intake-joint-candidate-20261003-check.py
.venv-cad/bin/python scripts/intake-joint-candidate-20261003-passages.py
.venv-cad/bin/python scripts/intake-joint-candidate-20261003-context.py
MPLCONFIGDIR=/tmp/intake-joint-candidate-mpl python3 scripts/intake-joint-candidate-20261003-source-review.py
```

The temporary path above is only a disposable plotting cache; no evidence or build inputs depend on it. CAD runtime uses the repository `.venv-cad`; plots use system Python with numpy/matplotlib because the CAD environment lacks matplotlib. Runtime versions are in the delivery ledger. Export follows the reviewed intake mesh pipeline:0.07mm/0.08rad tessellation, CAD(X,Y,Z)mm→viewer(X,Z,-Y)m, float32 GLB, zero-area-face removal, reloaded mesh verification. No image originals are included. The generated package is approximately17MB; root owns artifact release/preservation and its URL is not yet assigned.

## Validation and review

| Gate | Result and exact scope |
|---|---|
| Application/coverage | PASS for identified replacement six-port/nine-aperture topology. Exact1994 casting dimensions and paired-hole roles remain unknown. |
| Dimensions/coordinates | PASS explicit estimated frame/scale contract; NOT factory metrology. Source port-row straightening displaces internal centers0.92–1.25mm at the approved estimated scale. End centers stay fixed. |
| CAD/export | PASS three valid one-solid shapes and three valid one-solid STEP reloads. Upper volume roundtrip difference2.5433mm³ over2,941,379mm³ is within existing relative1e-5 convention. All three GLBs watertight; bounds errors lower0.004975mm, upper0.000990mm, gasket0.001328mm. |
| Source/visual comparison | PASS bounded gasket/landmark comparison and actual mesh inspection. Authored `source-feature-comparison.png` shows6/9 pattern and short front gap. Port ring/web/ear contours are approximate. Upper exterior decorative fidelity is intentionally incomplete. |
| Joint interfaces | PASS six49mm-diameter interface probes and nine10.5mm aperture probes through shared joint material: zero obstruction. Shared mating-footprint slab difference0mm³. Whole unmasked slab difference50.6676mm³ is the separate lower rail-mount material, excluded only by the explicit joint footprint. No production sealing/preload claim. |
| Passage sampling | PASS198 lower and99 upper centerline samples per runner, six runners. Does not prove minimum section, off-axis clearance, wall thickness or airflow. |
| Negative controls | Shifted port5mm adds2223.02mm³ obstruction; inserted blocking disc adds2136.73mm³. Mirrored front-ear center misses nearest actual hole by70.8245mm. The mirrored probe alone intersects zero because it lies outside gasket material; registration, not a collision-only test, detects that fault. |
| Protected datums | Throttle seat, EGR seat and regulator receiver bounded symmetric differences0mm³. Six injector-axis and three rail-axis probes clear. Broader head/injector region comparison returns `Null TopoDS_Shape object`: ERROR, not zero and not a preservation pass. |
| Neighbor context | Bounded static check26 pairs: both castings versus13 named neighbors (cover, cap, rail, regulator fitting, throttle housing, EGR body, head locator and six injector metal bodies). All candidate overlaps0mm³; no errors or new overlaps. This excludes neither untested neighbors nor moving/removal envelopes. |
| Fastening stack/installed interfaces | NOT RUN/UNRESOLVED beyond geometric holes. Stud3/5 roles and real thread/engagement unsupported; reused stud envelope itself is provisional. Candidate is not integration-ready. |
| Motion/disassembly | NOT RUN; cap withdrawal, throttle/cable/rocker sweeps and exploded/reassembly require current-context audit. Static cap clearance is not withdrawal proof. |
| Learning/diagnostics | N/A for this isolated geometry candidate; existing product learning untouched. |
| Browser integration | NOT RUN; no installation requested. |
| Reproduction/review | Source, inputs and artifacts hash-bound in `cad/engine/intake-joint-candidate-20261003-delivery.json`; root review pending. No commit by contributor. |

Actual mesh review paths: `efi-upper-intake.png`, `efi-lower-intake.png`, `efi-upper-intake-gasket.png`, and `source-feature-comparison.png` in the generated directory. Their mesh coordinates come from reloaded GLB, not a schematic. Inspection confirms asymmetric ears, offset central aperture, six separate open passages and distinct combined castings; it does not certify the unspecified production contours. Broad web/body shape and upper ribs still differ from the actual casting photos.

Failures preserved: initial ShapeList export handling, dropped flange with coincident32mm skins, invalid variable-loft flange restoration, and roundtrip/tessellation slivers from separately cut tangent inner sections. Final continuous single-wire upper bores eliminate those slivers. Earlier diagnostic JSON/logs are historical failures only and are never acceptance evidence. A missing plotting dependency was resolved by splitting mesh export from the plot runtime, not by changing the CAD model.

## Tracking and restart

Issue remains open. Root next reviews the new source-compared layout and estimated diameters before any coordinated adapter work. Resolve the broad protected head-region Boolean comparison, map paired-hole roles and complete fastening/whole-neighbor/motion checks. No clearance-optimized relocation was performed. Keep prior accepted exterior fixtures immutable; rebuilding this successor invalidates their old flange/air/added-material proofs. If root accepts the bounded educational candidate for preservation, archive generated artifacts and retain this explicit non-installed status. No background process remains after delivery. Model/effort billing data unavailable.
