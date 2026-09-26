# Component contract and handoff: inserted engine-oil dipstick

## Contract

- Issue: [#17](https://github.com/0xZakk/truck/issues/17); tube interface [#78](https://github.com/0xZakk/truck/issues/78); parent engine#1. Integration owner root; contributor pump_seal_finish.
- Starting commit: `5567d751abcf6a9bfac84bdf87ce0d7f0d4dac5c`, branch `engine/next-interface-contracts`. The report records the actual run revision and relevant dependency hashes.
- Scope: a rigid flexed display pose of the existing specimen-informed dipstick, fitted to the isolated tube candidate. No elastic simulation, installed manifest change, tube/block alteration or original pilot edit. The tube package stays frozen.
- Owned files: `cad/engine/dipstick_inserted_candidate.py`, `scripts/check-dipstick-inserted-candidate.py`, `inventory/engine/dipstick-inserted-candidate-validation.json`, and this handoff. Ignored exports: `cad/engine/generated/dipstick-inserted-feasibility/`.
- Units/frame: millimeters in engine CAD world coordinates; front+X, cover side+Y, up+Z. GLB maps CAD(x,y,z) to meters(x,z,-y), matching the engine exporter. No occurrence or explosion has been installed.
- Service identity: one `engine-oil-dipstick` assembly represented by metal blade and bonded handle/stop material bodies. They are not claimed to be separately serviced pieces. Exact owner identity, factory tube match and service/engineering-number equivalence remain unresolved.
- Dependencies: frozen proposed tube/block/retainer STEP, original pilot module/evidence, installed pan and relevant engine neighbors/motion transforms. Root may independently change unrelated throttle geometry and manifest entries.

## Evidence ledger and length interpretation

The [existing pilot evidence](../pilot/dipstick.md) supports a seller specimen marked **E9TE-6750-DA** with an approximately27.25-inch metal blade. Its converted **692.15mm** value is an approximate axial study length, not an established factory stop-to-tip calibration. All blade section, wave, handle, stop and stamp-position dimensions are inherited estimates. No new source claim is introduced here.

| Feature | Candidate treatment | Evidence class / limit |
|---|---|---|
| Axial route |558.476126mm in the guide +133.673874mm free extension =692.15mm | Preserves original pilot's approximate axial datum; no arbitrary truncation |
| Near-stop waves | Original polygon stations,3mm amplitude and2.2mm stem retained over53mm axial distance | Pilot estimates; wave material centerline is59.572804mm |
| Total material centerline |698.722804mm | Axial route plus6.572804mm inherited waviness; must not be confused with the seller's approximate axial measurement |
| Blade section |2.2×0.8mm stem, widening to6.5mm reading end over15mm, final tip taper retained | Pilot estimates; no manufacturing tolerance claim |
| Stamp | Existing `E9TE-6750-DA  M` specimen comparison on the widened end | Identity comparison only; no owner identification or oil-reading calibration |
| Mouth/stop datum |(-285,170,500)mm | Estimated tube candidate datum |
| Tip datum |(-315,24.163063,-150.405987)mm | Result of unshortened axial route, not an oil-level target |
| Handle/stop | Original pilot geometry; handle raised0.5mm relative to its original local origin | Pilot stop bottom originallyZ=-0.5; correction places bottom exactly on mouth without shifting the blade datum |

The narrow stem follows the guide's exact straight–spline–straight route. The sweep's transported end frame defines the reading-end orientation, preventing a disconnected or arbitrarily twisted free tip. The upper waves remain in the expanded straight mouth. The blade is one connected solid; the handle/stop is a second material body touching it at the seating datum.

The existing oil-level lettering and range remain illegible. **No ADD, FULL, NORMAL, quart increment, oil plane or sump capacity is inferred.** The old rejected -8.5° trial installation is not used.

## Delivery and reproduction

Readiness: **isolated educational flexed pose; not installed and not Done**. `parts(stamp=True)` returns two material bodies and length/datum metadata. `route()` reproduces the frozen tube centerline without changing its module.

Run from repository root:

```sh
.venv-cad/bin/python scripts/check-dipstick-inserted-candidate.py
```

This exports separate blade and handle STEP files, a combined two-body STEP, a GLB with two named material nodes, and `inserted-review.png`. CAD uses the local build123d environment; rendering uses system Python with matplotlib/numpy. Versions are recorded in the report. Context rendering uses finer angular tessellation0.1 because coarser settings can leave a small trimmed tube face unmeshed in this OCC version; no geometry or acceptance threshold was changed. Restricted photographs/manuals are not redistributed. Model/effort/usage unavailable.

The checker takes a whole-engine snapshot for neighbor selection, then freezes only relevant STEP/source inputs, occurrence ancestry and crank/rod parameters. An unrelated throttle or manifest update does not invalidate the run. The report's manifest digest is explicitly a canonical-JSON snapshot digest, not a claim that the complete current installed assembly stayed unchanged.

## Validation and review

The final validation reports **PASS bounded geometry**. Both exported bodies are valid single solids; maximum STEP volume discrepancy is0.000000020mm³. Maximum CAD/mesh bound discrepancy is0.032663mm; GLB export/reload bounds differ by0.00001124mm. The inserted review image was visually inspected for the full free tip, continuous guide route, retained near-stop waves, open loop and seated stop.

There are64 exact static comparisons and797 exact moving comparisons across73 poses, with no intersections exceeding0.1mm³. Continuous conservative envelopes also clear. Blade/guide minimum clearance is0.232261mm; blade/pan minimum distance is12.073289mm. The stop has29.845130mm² of contact on the mouth annulus; blade/handle contact is1.76mm², with zero gap and zero overlap in both interfaces. The oversized-section control intersects by8.122145mm³; the shortened-guide and raised-stop controls produce25mm and2mm gaps.

The validation JSON records exact values and input/output hashes. Gates include:

- Single-solid blade and handle validity, STEP roundtrip topology/volume and CAD-to-mesh bounds; combined GLB bounds and both named bodies survive export/reload.
- Full route-length sum, separately reported wave/material length, blade-to-guide clearance, planar stop seating area and blade/handle contact area.
- Exact intersections with the six frozen tube/interface solids and broad-phase-selected installed neighbors; minimum blade/pan distance.
- Actual crank/rod/piston STEP at73 poses through720° in10° increments, plus conservative continuous crank-cylinder, rod and piston envelopes.
- Negative controls:8mm-wide blade-section witness fails the7mm bore; shortening the guide25mm leaves the original stop unsupported and breaks the unchanged free-route length sum; raising the stop2mm loses seating.

| Gate | Scope and limit |
|---|---|
| Application/coverage | Specimen-informed; actual owner indicator/tube identity unresolved |
| Dimensions/coordinates | Pilot axial datum preserved; sections, waves, handle and tube route estimated |
| CAD/export | PASS isolated STEP/GLB, topology, bounds and roundtrip checks |
| Source/visual comparison | PARTIAL: inherits reviewed pilot evidence; generated inserted render inspected, not a factory comparison |
| Installed interfaces | PASS bounded isolated contacts/clearances; installed acceptance NOT RUN |
| Motion/disassembly | PASS sampled/conservative crank–rod–piston clearance; elastic insertion, withdrawal, twist and wave compression NOT RUN |
| Learning/diagnostics | PASS oversized-section, shortened-guide and unseated-stop controls; calibration uncertainty preserved |
| Browser integration | NOT RUN; isolated assets only |
| Reproduction/review | PASS reproducible checks and inspected render; root review pending |

The stop supplies a modeled axial bearing surface. A touching blade/handle and seated stop do not prove bond strength, friction fit, sealing, detent action or pull-out retention. No retention-force claim is made.

## Integration proposal and restart

Root can review the inserted pose beside the frozen tube candidate. Any future publication should retain one dipstick service assembly with distinct blade and handle materials, preserve the modeled seated datum and keep the withdrawn pilot presentation available without treating rigid translation as a removal simulation. Root owns shared manifest/learning/browser changes.

Before acceptance as an actual-truck reconstruction, confirm the matched indicator/tube identity, real stop-to-tip datum, section and formed waves, handle orientation, retention construction and original reading marks. Measured oil calibration is a separate requirement. Issue#17 and interface#78 remain open. No installed geometry or frozen tube files were edited. No process remains running after delivery.
