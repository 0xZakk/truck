# Shared estimated interface contract: expanded timing-pan seat

## Contract before geometry

Issues #32/#34, Engine #1. Baseline `70542fad9de467a5c03ad54a6f54def8550956eb`, branch `engine/timing-interface-integration`. Root explicitly approved moving the estimated transition start fromX335 toX300 and tapering inherited3mm entry walls to4mm downstream. Pan worker owns new shared analytic module, new pan/gasket candidate/check/render and this handoff; front-block worker consumes the module in a separately named adapter. Frozen prior candidates/reports unchanged. Central cover seal revision atX406+ is independent; preserve actual front arch and interfaces X365+ and all5 relocated axes.

Protected scope: all material/interfaces X≤300; all20 retained screw/washer stations, whose forwardmost retained long-rail axis isX267.5556; all5 revised axes and full local seats. New geometry may replace estimated pan flange/gasket and block seat inX300..365. Nothing is factory-exact. Keep original failures: old wet-side station20, source-tool interference, unsupported tabs,1252.77mm³ combined block collision and broken global roof proof.

## Source and functional evidence

The source-code/v2 cross sections atX335 reveal an abrupt change from the original pan flange to narrow front_blank ribbons (leftY−141..−130, right106..117). Treating those estimates as immutable manufacturing geometry forced inboard wall edges outside their support footprint. Exact-year evidence supports25 nominal pan screw/washer assemblies; it does not establish these contours, thicknesses or registration. The expanded route is an explicitly authorized model-interface correction. TEKTON nominal tool dimensions remain a separate comparison, with originalR11 failures preserved.

## Frozen common API and semantics

New module: `cad/engine/timing_pan_expanded_seat_contract.py`.

- `START=300`, `STRAIGHT_END=310`, `RETURN_END=355`, `FRONT=365`; CAD world millimeters.
- `seat_z(x)`:−32 atX300, linearly rising to−24.5 atX365. ForX365+ the existing source front arch `joint.top(y)` and its fixed flat pads remain authoritative.
- `band(bottom_offset, top_offset, footprint='pan'|'gasket', holes=False)`: side seat bandsX300..365 plus unchanged source front bandX365+, with offsets relative to gasket upper seat. Returns analytic test/model solid, not a neighbor carve.
- `pan_flange()`: `band(−6,−2,'pan',holes=True)`;4mm flange.
- `gasket_band()`: `band(−2,0,'gasket',holes=True)`;2mm gasket.
- `below_mating_seat()`: `band(−160,0,'pan',holes=False)`; **block clearance/mating-seat mask**. Its pan-footprint extension includes inboard flange overhangs, so the block cannot collide with supported pan material outside the gasket footprint. It is a shared analytic interface mask, never a subtraction of the actual pan solid.
- `upper_wall_envelope()`: `band(−160,−6,'pan',holes=False)`; wall construction must intersect this to tie upper edges to its own flange underside and prevent unsupported tabs.
- `wall_outer`, `wall_inner`: explicit XY routes. EntryX300..310 retains original straight-side tangents, varying3→4mm. Right outer return `(310,109)→(355,184)` and left `(310,−123)→(355,−121.5)`, then horizontal terminal sides toX378. Downstream inner lines are4mm normal offsets, including miter intersections; front innerX374. Interior path extends beyondX300 only as a construction mask, never modifying protected rear material.

Gasket outer edges interpolate original−141/+117 atX300 to−149/+213 atX365. Gasket inner edges interpolate−130/+106 to−115/+179. Pan-flange inner edges extend as needed to support the actual wall route, while retaining the wider original inboard overhang on the left. Thus gasket and pan flange have deliberately distinct footprints. Block uses the broader pan-footprint seat mask; full gasket-face contact still requires an independent actual check. At stations20/10, explicit existing radius8 pads retain the flat−24.5 seat, and radius4.3 clearance holes retain the fixed axes. These are deliberate mounting features, not collision-relief cuts. No retained hole is removed.

## Checks required before combined acceptance

Pan/gasket: valid intended solids, STEP/GLB bounds and watertightness; exact rearX≤300 preservation; exact unchanged frontX365+ parts; all20 retained hardware and flange/gasket seats; all5 revised hardware, nominal tool approach and local dry/wet separation; full wall-to-flange support from actual face contact/sections over the transition; wet passage/section continuity and breach/block controls. Guard input hashes, including common API.

Front-block: new shared mask only, protected rear/mounts/deck/feet/journals/wet passages; actual combined gasket/block and gasket/pan contact; collision comparisons against matching new pan/gasket plus remaining frozen neighbors. Report pair as coherent revision, not two separate passes. No installation until root review. Full oil containment remains NOT VERIFIED; do not rerun the broken unbounded roof Boolean.

## Local cavity-proof proposal (method only)

Use a bounded front-neck domain below the lowest flange underside (e.g.Z−90..−68,X330..380), with exact planar truncation portals. Extract the actual inward-facing pan face patch starting at the known front inner faceX374; traverse only shared actual edges, stopping at domain planes. Identify every boundary loop and classify its portal plane. Sew those actual wet faces with planar caps spanning only verified truncation loops; do not use a raised global roof or cap mounting holes. Check one closed oriented shell/positive-volume solid, front/shoulder/rear-portal witness containment, and zero intrusion into the actual pan. Same fixed portal caps must detect explicit wall breaches and distinguish a blocked neck. This could certify only that bounded local region and its portal connectivity, never the whole oil volume or top gasket seal. Ambiguous face membership or loop classification stops with a labeled diagnostic. No implementation is authorized by this method note alone.

## Delivery status

Contract recorded before shared API/candidate construction. Root and block worker coordinate through this API; exact module hash will be sent before block generation. Source originals not redistributed. Model/usage unavailable; no new dependencies. Generated assets unreleased. Next: freeze API, then bounded coherent pan/gasket and separately owned block candidate checks.

### Support-stock API clarification before block construction

`transition_below_seat()` clips the shared clearance mask toX300..365. `transition_seat_support(height=8)` separately returns estimated casting stock above the gasket upper face, gasket footprint only, clippedX300..365 with all fixed clearance holes retained.8mm is the root-approved explicitly provisional stock height, not a minimum-wall or strength specification. This optional stock is authorized within this shared candidate; the block worker must prove its contact with the actual new gasket, connectivity to the original casting/future land and compatibility with retained female threads, oil passages, bearings and feet. It must not overwrite socket interiors. If stock remains disconnected or conflicts with protected internals, report failure rather than silently adding bridges or reducing walls. Distinguish stock addition from the below-seat removal in reports.

Root finalized the initial stock-height hypothesis at8mm before block generation. Block worker additionally excludes complete radius10 socket neighborhoods at10/20 and retains their frozen owner material; the generic band holes are not female thread geometry.

Final combined-candidate choice is **explicit `transition_seat_support(10)`**, per root's later override relayed to the block worker; API default8 is unused. API froze at SHA256 `cb566ccb6b3fff9409f142bab5b0523d751bd466324d6f5b29ac7f6766ab4bac` before block generation and was not changed after that. Record this10mm hypothesis in the block report. Distinguish the broader pan-clearance footprint from the narrower gasket backing; the inboard pan-flange overhang is intentionally clear of the block, not assumed to be block-supported.
