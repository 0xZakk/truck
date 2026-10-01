# Component contract and handoff: timing-pan-dry-neck-candidate

## Contract

Issues #32 and #34 / Engine #1. Root integration owner. Baseline `4e480f8e40458384986b9e1792597e87e56daad7`, branch `engine/timing-clearance-revisions`. Own new source, checker, renderer, report, this handoff and `cad/engine/generated/timing-pan-dry-neck-candidate/` only. Earlier pan-access candidate and all failures remain frozen. World millimeters, identity pan frame; all25 station identities/transforms, full flange/seats/gasket lands and rear X≤335 preserved.

Functional requirement: station20 `(365.5,−132)` must lie outside the wet neck, as must station10 and the three front heads. The nominal TEKTON SHD03013 containing cylinder uses root's primary-source ledger: OD17.526, length48.26, mouth localZ0,90mm axial approach. This is a separate source-sized check; earlier R11 failures stay unchanged. No ratchet/vehicle accessibility or production stamping claim.

## Routing proposal and evidence ledger

All new pan routes are estimates. Two routes are compared before detail: (A) equal-clearance left/right terminal sides about the midpoint Y32 of the two side station axes, outerY−121.5/+185.5; (B) outerY−121.5/+184, retaining the previously reviewed right-side limit while moving only the failing left side inward. Choose B to preserve the already-working right dry-side corridor. Both retain outerfrontX378/innerfrontX374. At the straight terminal left side, station20 tool nearestY−123.237 leaves1.737mm nominal lateral clearance to outerY−121.5. This is arithmetic feasibility only until actual full approach and neighboring geometry pass.

Construct side walls from explicit XY piecewise-linear outer paths, with inward parallel lines offset4mm in their normal direction; do not merely offset steep slopes4mm inY. Outer left route `(335,−123)→(354,−121.5)→(378,−121.5)`; outer right `(335,109)→(354,184)→(378,184)`. Explicit line intersections define miters, without hardware subtraction. Preserve rear opening atX335; new inner routes extend behind it as cutting instruments only. Steep right return has a correspondingly larger Y separation to maintain4mm normal wall. Miter/corner radii remain unknown and unmodeled.

Shoulder is a4mm-thick analytic bridge Z−80..−76. Its outer footprint joins the new neck footprint to the existing lower-body outer cross-section atZ−80; its opening is the intersection of new neck interior and existing lower-body interior at that plane. This preserves a connected positive-width wet opening while supporting both upper and lower wall ends. The lower source loft's interpolated dimensions are explicitly checked against actual imported material. No blind neighbor subtraction, new fastener or flange cutting.

The source ledger for all25 nominal fasteners and their fixed revised positions remains the frozen v2 delivery. The nominal tool ledger is `reference/engine/tekton-shd03013-access-review.json`; actual truck head dimensions and tool tolerances unknown. No new factory contour is inferred from those tool dimensions.

## Planned validation

`.venv-cad/bin/python scripts/check-timing-pan-dry-neck-candidate.py`; `python3 scripts/render-timing-pan-dry-neck-candidate.py`. Predeclared overlap convention0.1mm³; material preservation/seat probes0.01mm³. Actual five hardware occurrences, nominal socket approach, rear/full-flange preservation, all sealing-neighbor overlaps, valid single STEP/watertight export, and explicit wall/shoulder sections. Positive-radius paths and dividing-wall sections establish only bounded dry/wet separation and neck-to-main connectivity. Include deliberate wall-breach/path-block controls. Never call these a full containment pass; broken global-roof Boolean remains separate and will not consume this task. Browser NOT RUN, candidate uninstalled. Source/render comparison is diagnostic only.

## Delivery and restart

In progress. API `build()` returns pan and frozen pan. Existing CAD environment, no dependency changes. Output assets not released. Model/effort and usage unavailable. Root owns shared inventory, integration and publication. Next action is construct selected analytic route and run the focused checker.

## Frozen delivery and local results

Geometry frozen at `pan.step` SHA256 `b519c1e37e6cacec5ed2326d92264c61ce7dd7f9f1a40eec7a57afeca1eb0caf`; GLB SHA256 `1dd3d5b051721796f139960a65cc5c5a35d72deec782aabdae87594b142e06bf`. Current integration branch advanced to `engine/timing-interface-integration`, base `70542fad9de467a5c03ad54a6f54def8550956eb`, while this isolated candidate retains its original bound inputs. No installation.

The report `inventory/engine/timing-pan-dry-neck-candidate-validation.json` binds the exported STEP/GLB/preview and exact checker/module inputs by SHA256. All five actual screw/washer overlaps and seat deficits are zero. Nominal socket approach clearance is0.85217mm at20,1.33465mm at10 and1.6mm at the three front stations. Rear X≤335 and full front flange have zero material changes/removal respectively; all five sealing neighbors have zero overlap. STEP is one valid solid, mesh one watertight component; roundtrip volume delta0.000000614mm³, GLB-bounds delta0.00001450mm. Independent winding check: GLB winding consistent and positive volume.

All five head-to-wet witness tubes are blocked by actual wall material; explicit rectangular test breaches make those paths clear. Wet-side endpoints connect by clear radius0.25mm tubes to the front-neck witness. The exact prior station20 path changes from zero obstruction to0.813208mm³, replayed against both bound inputs. Six horizontal sections (Z−70,−78,−82,−100,−160,−240) each contain one material ring with two boundary loops; all five axes are outside the outer loops, and designated wet witnesses are inside the inner loops. A deliberate front-wall breach changes the Z−70 section from two loops to one. Radius1mm bent paths connect neck, shoulder and main-cavity witnesses with zero obstruction; deliberate blocks are detected. The rejected initial straight path clipped the shoulder by1.511111mm³ and is preserved in `first-straight-path-validation.json`/console; geometry was not changed to satisfy that probe.

The dry-head controls are independent of wall construction: the checker defines fixed witness endpoints and explicit breach boxes, reads actual frozen hardware/nominal tool dimensions, and performs exact intersections against the resulting pan. The CAD module never imports those paths, boxes or checker predicates, and no path/hardware shape is subtracted during construction. These are bounded geometric controls, not global containment.

Original actual section render is `review.png`; analytic alternatives are `route-proposal.png`. Root reviewed the sections positively and requested clearer whole-mesh shading. `python3 scripts/render-timing-pan-dry-neck-shaded.py` reads the actual GLB via the CAD environment and renders it with system Matplotlib; no dependency was installed. Additional `shaded-glb-review.png` SHA256 `b63159334fa3c1c781a6294f22bba5e883e5289f3b1bb8c907da42a2d94c4b56` is bound in `inventory/engine/timing-pan-dry-neck-render-review.json`. Original render preserved. Actual shaded view exposes unsupported entry tabs, not hidden smoothing.

## Combined-interface failure: do not integrate

The front-block worker's separate hash-bound pair check finds1252.76851294mm³ overlap with this pan nearX335..343.58,Y100..126.59 (conservative Z bounds−32..0). Its report/witness reside with `timing-front-block-adapter-candidate`; block and pan remain frozen. Local passes do not waive this combined failure.

Diagnosis: the wall was extruded toZ0 and trimmed by the source `front_blank` footprint, which does not cover all new inboard wall material nearX335. The right normal offset reachesY92.71 where the narrow source flange isY106..117; the left wall also lies outside its source ribbon. Some wall consequently survives above the intended mating seat. A broad cap-height fix alone would not demonstrate flange support or sealing continuity. Root permits a separately scoped coordinated wall/flange/gasket/block-seat revision, including an earlier transition boundary if justified. No neighbor subtraction or silent correction of this frozen candidate.

| Gate | Status | Scope |
|---|---|---|
| Application/dimensions | PASS bounded | Nominal source tool; pan contours estimated |
| CAD/export | PASS | Bound valid single solid, watertight/winding-consistent GLB |
| Visual review | PASS diagnostic | Root reviewed sections; extra shaded actual GLB exposes limitations |
| Installed interfaces | FAIL | Combined block collision; entry support unresolved |
| Motion/disassembly | PASS nominal pan-only axial tool; broader NOT RUN | No ratchet/vehicle access claim |
| Local wet/dry topology | PASS bounded | Section/path controls only; full containment NOT VERIFIED |
| Learning/browser | NOT RUN | Uninstalled study, no new lesson/browser acceptance |
| Reproduction/review | Available for root | Hashes, commands, logs and failures preserved; no release yet |

Next work is a new coordinated entry-seat contract and separately named candidate. Original files remain frozen. No further export writes are planned for this delivery. Root owns integration/publication and issue status. Available usage unavailable.
