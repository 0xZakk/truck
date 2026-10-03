# Pump functional-region candidate handoff

## Contract and identity

Issue #47 / engine #1. Contributor pump_functional_junction; root integration owner. Baseline4f1fe9da2ec177e1ff61668df66ca422e37b0b7c, branch engine/source-host-interfaces-20261002. Before-CAD contract: [pump-functional-20261003-contract.md](pump-functional-20261003-contract.md). Root approved the independent functional regions, with estimated3mm backing, and subsequent machining of the pump's own declared pad planes. No neighbor masks, engine anchor movement, carrier fitting or canonical edits. Readiness remains **candidate; FAIL installation**.

WORLD millimeter assets, shaftY−32/Z170, mountingX375 and hub-seatX473.43. Do not reapply installed occurrence transforms. Stable occurrence IDs retained. Primary Carter W9046M replacement-height datum98.43mm; exact inlet/chamber/wall/bolt dimensions remain estimates. Full Carter rear and side views were inspected; the identified GMB specimen remains comparison evidence. Both show peripheral integrated inlet and distinct pads; neither supplies an internal section drawing. Bearing internals/fit, actual thread detail, heater radial registration, hydraulic performance, hoses and fan/radiator context remain unknown or simplified.

Owned files are only the pump-functional-20261003 prefixes and generated directory. Root owns repository tracking/archive publication. Issue network read failed in worker environment; no issue update claimed.

## Reproduction and assets

Entry point: `cad/engine/pump_functional_20261003.py:parts(height=98.43)` returns occurrence-name→WORLD-shape mapping, direct input paths and independently named functional region shapes. Nominal52-part candidate only;98.552mm sensitivity NOT RUN in this bounded delivery. Short-height core and formed tube are inherited from qualified height study; new inlet is estimated. Dry bosses are added independently after the declared cavity operation, and each own pad is machined toX389.

From repository root:

1. `.venv-cad/bin/python scripts/pump-functional-20261003-build.py`
2. `.venv-cad/bin/python scripts/pump-functional-20261003-check.py`
3. `.venv-cad/bin/python scripts/pump-functional-20261003-fifth.py`
4. `.venv-cad/bin/python scripts/pump-functional-20261003-seats.py`
5. `.venv-cad/bin/python scripts/pump-functional-20261003-neighbors.py`
6. `.venv-cad/bin/python scripts/pump-functional-20261003-non-spring-mesh.py` exports only the51 non-spring assets using the same checked export loop/settings. This convenience wrapper is syntax-checked; selected outputs come from the original47 exports plus the final4 tail exports. Then `.venv-cad/bin/python scripts/pump-functional-20261003-spring-export.py` reproduces the separately bounded failed spring export. The original full `...-mesh.py` was interrupted at20minutes; do not rerun that slow path blindly.
7. `.venv-cad/bin/python scripts/pump-functional-20261003-display-data.py`
8. `python3 scripts/pump-functional-20261003-render.py`
9. `python3 scripts/pump-functional-20261003-finalize.py --no-running-process` only after all commands finish. The expected overall result remains FAIL installation and FAIL spring topology.

STEP/GLB and region/witness assets: `cad/engine/generated/pump-functional-20261003/`. Reports, actual rendered images, machine arrays and logs: `reference/engine/pump-functional-20261003*`. Source originals and source-pixel composites are excluded. Existing macOS Python3.13/build123d0.10/trimesh; systemPython supplies NumPy/Matplotlib. No environment upgrades. Fine export uses0.003mm relative mesher parameter and0.025rad angular parameter, seam merge to5 decimal places in CADmm; retained0.025mm measured bounds gate. The parameter is relative in build123d's underlying mesher; measured export agreement is the acceptance evidence, not an asserted global surface-deflection bound.

## Finite local results and sensitivity

-52 nominal STEPs valid, individually one solid. Actual gasket mating face has0 missing area; its3mm backing and all four full dry boss volumes have0 missing volume. Four bores and fifth aperture have0 solid obstruction. All four declared annular pad faces and all four actual screw underside contact regions have0 missing area; each actual screw contact area88.270245mm².
- Analytic true rotational envelope of the actual disk and six rectangular vanes contains the actualv4 impeller with0 exterior volume. Housing has0 overlap with that envelope and a0.5mm radial/forward guard. This establishes the existing simplified rotor envelope, not production impeller accuracy.
- Finite inlet/heater lumen centerlines and fifth-aperture connection witnesses have0 obstruction. Four full inlet-skin sections have0 missing material after explicitly excluding intended communication with the declared pump cavity. The join's9.537855mm³ opening is labeled as cavity communication rather than a missing wall. These are finite topology/wall witnesses, not pressure containment, capacity or hydraulic certification.
- Hub/pulley named seat2982.934371mm² is fully present on both actual faces atX473.43. BearingOD23.9/housingR24 and shaftR8/bearingbore8.05 retain unqualified0.1/0.05mm radial gaps.
- Negative controls detect a backing notch42.089212mm³, shifted sealing face2902.749772mm², blocked inlet18.315833mm³, plugged bolt bore813.232674mm³ and fifth-route plug1.468091mm³. Exact scripts/reports bind geometry.

First trial failed the full dry-boss envelope because the inherited chamber cutter removed343–429mm³ per boss. Preserved first source/housing/check precede the correction. The subsequent0.1521506557mm² pad3 outer-rim face discrepancy was real overlying stock, not missing backing: the below-face0.1mm prism is fully solid while0.004218mm³ exists above it. Own-pad machining resolves it. Both full annular and actual smaller screw-contact checks remain explicit; the latter was never substituted for the former. Pre-seat source/housing/build/check/neighbor report and seat-diagnostic witness are retained.

Historical fullX<=389 slab preservation remains FAIL: added14985.908691mm³, removed565.248555mm³. This is not erased by the approved regional contract.

## Actual v4 affected neighbors

Final nominalq0 audit:90 exact affected pairs, zero metric exceptions;101 unchanged rigid translated internal relations remain inherited, not newly accepted. All v4 original STEP hashes and all occurrence matrices were validated against the frozen971-pair report before bounds reuse. Broadphase uses2mm padding; threshold remains0.1mm³.

| Actual pair | Overlap mm³ |
|---|---:|
| Timing cover / housing |746.749983|
| Thermactor engine bolt1 / housing |427.729722|
| ALT/AP common carrier / housing |3012.300371|
| Timing-cover mounting screw3 / housing |19.265671|
| ALT/AP common carrier / heater tube |217.135106|

Witness STEPs and hashes are in the neighbor report. No carrier/cover was altered. The explicitly estimated carrier needs coordinated source/interface review. Housing conflicts with actual cover/fastener remain equally binding. Static results do not establish motion or removal access.

## Quality gates

| Gate | Result | Evidence and limit |
|---|---|---|
|Application/coverage|PASS replacement comparison; partial physical coverage|Carter applicable height; inherited simplified rotor, seal and bearing|
|Dimensions/coordinates|PASS stated candidate datums; production unresolved|WORLDmm and qualified98.43mm; other dimensions estimated|
|CAD/export|FAIL aggregate|52 valid single STEPs;51 non-spring GLBs watertight/winding consistent, maximum bounds error0.001779261mm; spring bounds corrected but nonmanifold export remains|
|Source/visual|PARTIAL; source shape acceptance open|Actual four-view export render inspected by worker/root; not camera-registered; relative azimuth and proportions unverified|
|Installed interfaces|FAIL|Five actualv4 conflicts; finite functional-region checks pass; retention gaps persist|
|Motion/disassembly|NOT RUN|Static candidate only; inherited tool failures not superseded|
|Learning/diagnostics|N/A new lesson|Existing source notes preserved; no installed learning changes|
|Browser integration|NOT RUN|No installation|
|Reproduction/review|PASS local preservation; root final review pending|Commands/logs/reports and frozen ledger retained; root owns publication and independent review|

Source comparison: candidate follows separate pads, peripheral beaded inlet, bearing tower and formed heater tube. Broad ruled inlet, inherited approximate flange/rotor and absent Carter-style threaded hub nose remain visible differences. Inlet and tube proportions are hypotheses, not production dimensions. Final actual render inspected. Root separately flags Carter rearface heater/inlet relative angles versus this model as unresolved: bolt-pattern and camera registration must precede any mirror/rotation conclusion. The final exterior render uses display-only coarser tessellation and unified triangle sorting; full QC GLBs are unchanged. The first dense-mesh render is retained as a superseded collection-depth-sorting attempt.

## Tracking and restart

Issue47 stays open. No installation patch. Next bounded action is Carter-only six-static/24-turntable registration, explicitly registering the rear bolt pattern and quantifying heater/inlet relative azimuth, short tower and blended inlet proportions against the same W9046M98.43mm dimension. Do not silently tweak this trial or combine Carter height and GMB contours as established equivalence. Then compare both pump and cover/carrier owners against sources before coordinated interface changes; no repeated clearance tuning or neighbor cuts. This preserved functional trial is a step toward accurate installed parts, not the end of pump scope. Candidate code may be preserved independently of installation.

All processes completed or explicitly stopped. Relative mesher session62200/PID47133 was stopped at20m14s,100%CPU,1,489,872KiB RSS, exit143 after the approved runtime budget; its47 successful non-spring exports/report/log were preserved. Four final rebuilt parts were exported separately. Absolute spring export session29543 completed39.19s; display render63466 completed and was inspected. Other local/build/neighbor checks are complete. No background work remains.

Model/effort and usage unavailable; no billing inference. Root owns Git/PR/archive publication. The frozen ledger records all own files/generated assets and selected current input hashes; historical failed reports are labeled history, not current acceptance. Some pre-seat witness filenames were reused by the final fresh neighbor audit; preserved pre-seat source/housing/report can reproduce that historical state, but its historical witness hashes must not be represented as current artifacts.

## Spring export diagnosis retained

The source spring is clipped to localX15.5..20, transformed toWORLD406.93..411.43. Ordinary OpenCascade AddOptimal returns a loose axial spline box406.13008..412.23027. The faithful scoped exporter tightens only those bounds using independently declared source clipping planes, verifies both actual planar end faces and zero shape outside that slab, and leaves transverse conservative CAD bounds unchanged. The absolute0.01mm/angular0.06rad mesh has measured bounds error0.000418491mm, below the unchanged0.025mm gate.

The same export still fails topology: raw1,041,402triangles include88nonmanifold edges/150degenerate faces. Removing only zero-area/repeated triangles leaves a nonwatertight result. No arbitrary hole fill or vertex sculpting was used. A separate numerical seam-weld diagnostic across1e−5..3e−4mm did not fix15boundary/6nonmanifold edges; those variants were not adopted. Raw and cleaned failed GLBs remain separate artifacts. The topology is an unresolved export defect, not a factory geometry acceptance.

An attempted six-plane nearest-distance bounding method is also preserved as a rejected diagnostic: it selected a local Y minimum on the multi-turn helix. Actual legacy mesh extremeY−47.899935 lies within1.523e−6mm of the STEP, disproving that candidate support minimum. Do not reuse the rejected transverse bounds as exact global extrema.

Next mesh work should inspect the specific trimmed spring face/edge triangulation and export a faithful manifold surface; no threshold relaxation or unsourced spring replacement. This is independent of the more consequential source registration and installed neighbor failures above.
