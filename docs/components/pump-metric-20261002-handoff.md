# Pump metric dimension contract — 2026-10-02

## Contract

Issue #47 under engine #1; root integration owner. Baseline54c2abf7aae73a8a5818321ee48ad81c8b7346ad. Research only, owned pump-metric-20261002* source captures, scripts, reports and KB pages. No canonical, frozen geometry or shared-file writes. Source photographs are local review evidence, not redistributed assets.

Question: can primary applicable pump dimensions and perspective camera fitting resolve the inherited143mm axial-span/70mm hub mismatch? Coordinate system: mounting face X0, shaft along+X; pump-relative YZ matches previous estimated hole pattern. Pulley mating face differs from projecting pilot. Millimeter dimensions remain replacement comparisons or explicit estimates. No engine-clearance objective enters the solve.

Planned checks: actual four-view landmarks with declared uncertainty; explicit perspective projections, held-out features, alternative proportions/camera solutions, input hashes. No CAD without supported joint dimensions. Prior frozen reports remain unchanged. Geometry/interface/motion/browser gates N/A for research; installed fit remains open.

## Evidence and actual face extraction

Carter primary product page `https://carterengineered.com/engine-water-pump-w9046m` gives hub height98.43mm /3.88in. Its CWP-M5-2023 catalog PDF page162 explicitly maps F1501993–1996 4.9L toW9046M. This is newly captured **applicable replacement comparison**, not factory or photographed GMB identity.3.88in converts to98.552mm; the0.122mm discrepancy is retained as a second catalog representation, not tolerance. The manufacturer's existing hub-height guide defines engine mounting face→pulley mating face, excluding pilot. GMB's own page lists only package dimensions; none are adopted. Carter's malformed thread designation is not adopted either.

Actual posed v4 STEP planes: drive hub pulley seatX522 (area2992.4mm²), pulley rear seatX522 (area3670.9mm²); hub rear faceX514, pilot tipX547.5. Conditional heater housing rear mounting faceX375 (3685.2mm²). Thus actual mating-face span147mm, versus earlier143mm center-based span. Area extraction identifies axial faces, not a new contact or pressure proof. `pump-metric-20261002-faces.json` binds all selected assets/runtime/manifest. Initial extraction failed on a retired monolithic seal ID; the failed log is preserved, successful run extracts13 actual parts including all six present seal pieces.

## Perspective experiment

Six bounded nonlinear pinhole fits use all four source views and shared uncertain pump proportions. Camera principal point fixed at(300,300); focal range400..5000px is an explicit hypothesis, not EXIF calibration. Inherited hole pattern may scale independently inY/Z by0.6..1.3. No engine, neighbor or clearance input is loaded. Visible rim extrema have6px uncertainty because flange thickness/occlusion complicates seating-plane identification; previous22px side minor span is not silently treated as a precision circular face. Holes4px, tube centers8px, inferred side mounting-origin12px.

First four fits exclude the side tube tip. H98.43/Dfree and H98.43/D70 have small training weightedRMS0.191/0.783 yet held-out tip errors120.733/109.087px. InheritedH143/D70 misses388.716px. These are concrete failed predictions, not proof no possible camera can fit.

Complementary fits include all four tube views while withholding the rear fifth opening. H98.43/Dfree reachesD115mm (declared upper bound), weightedRMS0.202 and held-out2.477px. H98.43/D70 givesRMS0.814 and held-out4.639px. Both have positive camera depth for all fitted physical features. The latter still has tube/root errors above individual pixel assumptions; neither is an accepted metric reconstruction. Broadly different proportions fit observed landmarks with incomplete calibration, and the free solution hits its bound. Do not adoptD115, shrink inherited hole pattern from the fit, or call a least-squares minimum production evidence. Finite local solves do not certify global uniqueness or a bounded physical uncertainty interval.

Reviewed visualization `reference/engine/pump-metric-20261002-fit.png` plots actual observed versus predicted pixels without reproducing manufacturer images. All fitting data, camera parameters, source hashes and residuals are retained in numerical report. Frozen four-view study remains unchanged.

## Concrete next correction contract

Datum-only API: `scripts/pump-metric-20261002-contract.py:pump_height_datums(height_mm=98.43, mount_world_x=375, axis_yz=(-32,170), belt_center_world_x=473.56)`. Returns mount-local/world targets and owned subassembly scope; no shape generation. `reference/engine/pump-metric-20261002-contract.json` serializes both catalog representations.

Nominal: new pulley mating faceX473.43, delta−48.57 from old522. Keep mounting faceX375, gasket/blockfaceX373, four mountaxes, existing impellerX369..384, rear shaft endpointX365 and shaftYZ fixed. Translate hub/pilot, bearing, six seal pieces, slinger and frontwall/bearingnose/weep interfaces together by−48.57; these detailed dimensions remain estimates. Rebuild shaft fromX365 to470.43 (105.43mm), preserving rear engagement and new hub station, rather than translating its rear out of the impeller. Rebuild the chamber/taper between protected rear flange and relocated frontwall, without globally scaling holes or walls. Reconsider inlet/heater root attachment against this changed chamber; frozen tube is not automatically reusable.

Keep existing belt centerX473.56 as a **provisional integration anchor**. New hub face→belt center is+0.13mm versus old−48.44mm, so pulley dish requires rebuilding; rigidly moving the complete pulley would break the accessory belt plane. Translate only mounting web/bolt stack and rebuild its connection to the retained rim. Translate fan-clutch/fan subgroup with hub, then check radiator/body space separately (currently NOT RUN). The catalog height justifies a new explicitly qualified joint-height candidate; successful full photo calibration is not a prerequisite to that bounded candidate. It does not authorize installation or assert the retained diameter/bolt circle/internal geometry are correct.

## Delivery, validation and restart

Commands: `python3 scripts/pump-metric-20261002-fit.py`, `.venv-cad/bin/python scripts/pump-metric-20261002-faces.py`, `python3 scripts/pump-metric-20261002-contract.py`, `python3 scripts/pump-metric-20261002-review.py`. Existing Python3.13, NumPy/SciPy/Matplotlib; CAD environment build123d0.10. No installation. Fit sessions69707/73388 completed; successful face session33446 and plot81341 exit0. No live process remains. Model/usage unavailable.

| Gate | Result | Scope/limit |
|---|---|---|
|Application/coverage|PASS replacement identity|Manufacturer catalog page162; not owner's specimen|
|Dimensions/coordinates|PARTIAL; production unverified|Primary height; actual face span; OD and all-view metric calibration unresolved|
|CAD/export|N/A|No geometry created or changed; existing faces inspected|
|Source/visual|PASS research comparison|Actual images and coordinate residual visualization; no fidelity acceptance|
|Installed interfaces|NOT RUN|Next coordinated scope explicitly defined|
|Motion/disassembly|NOT RUN|No geometry or motion changes|
|Learning/diagnostics|PASS new source/atomic note structure|Semantic backlinker deferred to root shared writer|
|Browser|N/A research|No installation|
|Reproduction/review|PASS local, root review pending|Bound sources, scripts, plots, finite solver limits|

Public download succeeded after sandbox DNS failure; localHTML/text ingestion completed. PDF extraction emitted font-weight warnings but applicable row was checked. New two source pages and one atomic note follow source→note pipeline. Do not redistribute manufacturer originals. Root owns semantic backlinks and shared documentation. No commits, canonical edits, shared runtime writes or old report mutations. Issue47 remains open. Exact next step: root review of the height-contract API and resulting pulley/belt conflict, then a separately scoped coordinated pump-height candidate with actual passage/contact, pulley support, fan and neighbor checks.
