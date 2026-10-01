# Proposed checker contract: full pan cavity and revised front wall

Issue #32 / Engine #1. Isolated acceptance-design follow-up to `timing-pan-access-candidate`; no geometry changes. Root is integration owner. Current branch reported by root: `engine/timing-clearance-revisions`, base `4e480f8`. Frozen v2 and submitted pan STEP/report hashes remain the geometry authorities. Existing R11 tool failures and unsuitable wet-channel probe are preserved.

## Why the existing checks are insufficient

A valid, watertight material solid can have a hole from the oil space to the exterior. The submitted rectangular wet witness also intersects 162.377556923 mm³ in frozen v2, so it does not define the actual cavity or diagnose a new obstruction. Full-thickness wall samples are local checks only. None establishes containment.

## Geometry and intended aperture inventory

The source `oil_pan_joint_v9_candidate.py` builds one main mouth with two long gasket rails and curved end bridges, a shallow cavity joining a deeper rear sump, and one drain bore. `timing_cover_front_joint_candidate.py` replaces the front mouth/neck above the existing lower body; `timing_pan_access_candidate.py` changes its front and right wall/shoulder. The main mouth is nonplanar: long rails derive from Z−34..−32 gasket, rear bridge derives from the 51.1/53.1 mm estimated end radii, and front gasket derives from `top(y)` with radius59.4 and terminal plane Z−24.5 plus side transition lofts. These are source-code dimensions, not factory dimensions.

The drain has world frame `Pos(0,−12,−96) * Pos(*DRAIN_LOCAL) * Rot(*DRAIN_ROTATION)` from `oil_pan.py`; bore radius7.1, source cutter local axial interval −19..11 mm. The checker must find and verify the actual STEP bore/seat before adopting a cap. It must not assume the cutter necessarily produced an open passage. Cap only an observed drain bore aperture.

The 25 screw holes are intended dry holes, **not additional oil ports to cap**. If they communicate with the oil cavity, report failure. No cap is permitted on a newly discovered side hole or unclassified boundary. The main mouth includes the curved end regions; do not invent extra crankshaft apertures independently of the observed rim. Pickup/dipstick openings are not declared unless actual input geometry demonstrates them.

## Concrete checker sequence

1. Load candidate pan and unchanged actual pan gasket STEP. Bind input hashes. Also run frozen v2 pan with exactly the same mouth/drain cap definitions to identify inherited failures. Do not require the baseline to pass.
2. Extract the actual central inner rim of the gasket's **upper sealing boundary** from STEP edges/faces. Use frozen source geometry to identify the relevant faces, but verify the final curve against the imported STEP. Chain edges into one nonplanar closed loop with no duplicate, missing or self-intersecting segments. Explicitly classify the 25 other hole loops as dry mounting holes. Export a labeled rim-only render and JSON edge coordinates/lengths before construction. If one central loop cannot be established, stop as NOT RUN/ambiguous; never auto-fill every loop.
3. Build a temporary roof patch spanning only that central mouth loop, at the actual upper sealing boundary. Use planar/ruled regions corresponding to the actual long rails, side transitions and curved end bridges; preserve the contour rather than replacing it with a flat bounding box. Give it a small declared outward thickness (for example0.5 mm) and a narrow, declared collar landing on the gasket material, not down the revised wall. Boolean trimming must keep the collar inside actual gasket material. Export roof STEP/mesh separately. Verify its rim meets the actual gasket continuously and that its footprint does not cap dry holes. If exact construction fails, record failure, not a broad cap substitute.
4. Verify the actual drain aperture and place a thin analytic disk in its bore at the observed outer seating plane with only a small rim overlap. Disk position, normal, radius and actual contact must be reported. Do not insert a long cylinder that could hide a sump-wall breach. Other openings remain unsealed.
5. Treat `pan ∪ actual gasket ∪ temporary mouth roof ∪ verified drain disk` as the barrier. The gasket is part of the interface being evaluated; actual pan/gasket gaps remain visible to the check. Construct an enclosing box with a substantial air margin, then compute `box − barrier` and enumerate resulting connected **void solids**, retaining full topology and failing Boolean/kernel errors closed. Export every component with labels.
6. Classify exterior via contact with any enclosing-box face. Predeclared strictly interior witness points in the shallow main cavity, rear sump, and revised front neck must lie in a single positive-volume void component which touches none of those box faces. Establish each witness as strictly off all material/cap boundaries before classification; no guessed point silently moved to whichever component passes. The cavity should be a single watertight boundary-shell volume after exact temporary closure. All additional bounded void components must be reported and explained; they cannot be silently discarded as noise.
7. Prove the front-neck region and main cavity belong to that same connected volume, including points above and below the Z−80..−76 shoulder and across X335. Use positive-volume witness balls with documented clearance and exact component containment. Export a section and colored actual cavity render showing front, shoulder and rear sump membership. This checks geometric connectivity, not a rated fluid-flow area or production capacity.
8. Cross-check tessellated cavity topology: watertight mesh, one expected connected component, consistent orientation, mesh volume/bounds versus exact CAD within declared tessellation tolerance. A mesh result cannot override failed exact Booleans. Report resolution limits explicitly.

## Anti-masking guards and sensitivity

The cap is an instrument, not a new vehicle part. Its overlap with the actual pan must be zero; collar overlap belongs only to the gasket at its upper surface, and drain overlap only to the identified bore rim. Render and report distances between roof/collar and the revised wall/shoulder. A cap that descends into a wall defect invalidates the test.

Use the same fixed caps for adversarial variants. Remove explicit small rectangular wall patches below the cap in (a) the broad front wall, (b) right side transition, and (c) shoulder connection. For each, the former cavity must connect to the exterior component. Remove the drain cap as a separate control when the drain is proved open. A thin artificial barrier cutting the neck-to-main passage must cause witness components to separate. The controls may alter temporary test copies only, never the delivered candidate.

Choose breach patches well within verified wall faces and clear of the cap, flange and numerical edges; record exact coordinates and removed volume. Begin with a1 mm square through-wall breach, then a0.25 mm square sensitivity sample; these are detector-resolution controls, not production leakage tolerances. Do not accept a test that misses a known breach or passes merely because witness points were omitted.

## Scope and acceptance limits

A passing check certifies geometric enclosure and connectedness of the declared modeled cavity under temporary closure of its verified mouth and drain openings, including the revised front wall and shoulder. It does not certify real-world sealing, minimum material thickness everywhere, gasket compression, strength, oil capacity, pickup immersion or factory contour. Original R11 access failures remain independent.

Proposed owned outputs: `scripts/check-timing-pan-oil-boundary.py`, `inventory/engine/timing-pan-oil-boundary-validation.json`, this proposal/handoff and `cad/engine/generated/timing-pan-oil-boundary/` for caps, cavity, controls and renders. No source geometry, shared assembly or frozen input writes. Exact construction and control implementation remain NOT RUN pending root scope review. If the central sealing loop cannot be isolated from STEP reliably, the next deliverable is the labeled ambiguous-rim diagnostic, not an inferred pass.

## Optional source-tool follow-up

The TEKTON SHD03013 primary product page was retrieved on2026-10-01 and confirms1/4-inch drive,1/2-inch, deep six-point identity. It links the dimension graphic as specification image28. The web tool could not access `https://images.tekton.com/assets/SHD03013_spec.jpg`; numeric outer dimensions were not retrieved. No source-sized tool envelope was invented or built, and no image-download workaround was attempted. This optional tool check remains NOT RUN and does not block the proposed oil-boundary scope.

## Implemented bounded delivery — 2026-10-01

Root approved the scope above. Files are `scripts/check-timing-pan-oil-boundary.py`, `scripts/check-timing-pan-head-wet-path.py`, `scripts/render-timing-pan-oil-boundary.py`, `inventory/engine/timing-pan-oil-boundary-validation.json` and isolated `cad/engine/generated/timing-pan-oil-boundary/`. Candidate geometry and its earlier report remain frozen. This is a checker/fixture diagnostic delivery, **not oil-containment acceptance**.

Commands from repository root:

```sh
.venv-cad/bin/python scripts/check-timing-pan-oil-boundary.py
.venv-cad/bin/python scripts/check-timing-pan-head-wet-path.py
python3 scripts/render-timing-pan-oil-boundary.py
python3 -m py_compile scripts/check-timing-pan-oil-boundary.py scripts/check-timing-pan-head-wet-path.py scripts/render-timing-pan-oil-boundary.py
```

The CAD command uses the existing macOS Python3.13/build123d0.10 environment; renderer uses system Python/NumPy/Matplotlib. Model/effort and usage unavailable. No dependency changes, installation or browser calls. Generated STEP assets are not yet released; input/output paths and hashes are repository-relative.

### Actual rim and fixture findings

Upper-face extraction initially returned30 loops. Three additional loops are finite-height radius8 seating-pad steps; their exact neighboring faces are recorded in `residual-loop-adjacency.json`. Including their vertical connecting faces53,329,330 yields27 closed loops: one outer contour, one central nonplanar mouth and25 circular dry mounting holes. Each dry loop matches the station upper center and radius4.3 within0.00001 mm; see `dry-hole-classification.json`. They are never capped. Actual coordinates, STEP curves and face data are in `classified-rim-loops.json`, `central-inner-rim.step`, `gasket-faces.json` and `rim-review.png`.

A whole-loop surface-fill trial stalled and was stopped; a triangular fill produced an invalid face; an initial ruled-volume union produced invalid/disconnected pieces. Logs and rejected fixture STEP preserve those failures. The final roof explicitly sews lower/upper ruled faces and the rim curtain into a thin test solid. The observed rim maps to a10% scale planar contour at Z0, with0.5 mm vertical fixture thickness; this raised-center shape is only an instrument, never a source-supported vehicle contour. A gasket copy shifted +0.5 mm provides the roof collar while retaining all dry holes. It extends only upward from the actual gasket footprint.

The final roof is one valid solid with one watertight mesh. Both roof and collar have zero pan overlap. The0.5 mm drain disk occupies local axial−0.5..0 and radius7.2; its radius7.1..7.2 support ring is fully supported by the actual pan, and its radius7.09 bore probe has zero obstruction. These are geometric cap checks, not physical drain-plug acceptance. Roof/section render: `roof-section-review.png`; STEP/NPZ fixtures remain in the same folder. The final fixture cannot yet be accepted solely from these checks.

### Exact cavity calculation: blocked by invalid result

For **both** candidate and frozen pan, enclosing-box subtraction succeeds for the pan, actual gasket and upward collar. Subtracting the roof produces an invalid kernel result at step3. Each invalid result is exported separately, and `diagnostic-console.txt` preserves the stage trace. No bounded cavity was accepted. No head-to-enclosed-cavity classification, breach control, artificial passage-blockage control, cavity volume or full containment claim is made. A successful cap export did not waive the failed void operation.

The next checker action is to diagnose the roof/barrier Boolean seam against `candidate-invalid-step-3.step` and `frozen-invalid-step-3.step`, preserving the same observed rim. Consider a simultaneous barrier Boolean or an explicitly sewn full void boundary, with exact cap landing rechecked. Do not alter the pan or cap unclassified apertures to force a closed result. The predeclared adversarial controls remain mandatory before acceptance.

### Independent station20 wet-side path: local failure

Root requested actual head centers for all five stations as dry-side witnesses. The full checker records that requirement, but invalid voids prevent classifying them against a bounded cavity. A separate exact path witness provides a narrower result now: a radius0.25 mm cylinder from station20 head center `(365.5,−132,−34.85)` to designated front-neck interior `(370,0,−70)` has **zero overlap with pan, gasket, roof and collar**. Its positive width contradicts dry-side isolation of that head from the intended neck region. This does not by itself establish a closed oil cavity. STEP path, bound JSON and console are `station20-head-to-front-neck-path.step`, `station20-head-wet-path.json`, `head-path-console.txt`. A1 mm cube placed at its midpoint supplies a blocked-path sensitivity control; the result is recorded in that JSON. Original R11 failures remain untouched. Root owns the separate nominal TEKTON tool comparison and its ledger/checker.

## Validation and review

| Gate | Status | Scope |
|---|---|---|
| Application/coverage | PASS bounded | Actual input topology identified; no new production claims |
| Dimensions/coordinates | PASS bounded | World mm, source drain frame verified,25 dry centers matched |
| CAD/export | PASS roof itself; FAIL void operation | Valid roof/mesh does not certify usable closed fixture |
| Source/visual comparison | PASS diagnostic only | Actual rim and roof/section exported; no factory fidelity inference |
| Installed interfaces | FAIL/open | Station20 head has direct path to intended wet neck; full containment unverified |
| Motion/disassembly | NOT RUN | Original access results preserved; no new disassembly acceptance |
| Learning/diagnostics | N/A | Acceptance-checker work, no user lesson in scope |
| Browser | NOT RUN | Uninstalled diagnostic; prior browser rejection respected |
| Reproduction/review | Local commands/hashes available; root pending | Assets not released; exact void failure preserved |

Issue #32 stays open. No candidate promotion. At handoff no background CAD process remains. Root reviews the roof, failure outputs and station20 path before further work. The next requested work is Boolean-fixture repair and the remaining controls, not a vehicle-geometry edit.
