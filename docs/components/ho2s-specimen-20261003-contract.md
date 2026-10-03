# HO2S isolated exterior specimen — pre-CAD contract

## Contract

Issue #82 / engine #1. Worker `airbox_screw_finish`; root owns integration, Git and shared files. Baseline `4f2760612a18e597da5e6df15e27b6b9ae69ac6c`. Assembly manifest is not a geometry input; no installed transform. Scope authorized by root: isolated source-compared Bosch15718/0258005718 replacement exterior, **candidate only**, with separate visible regions and explicit educational estimates. Own `ho2s-specimen-20261003*` docs/reference/scripts/generated folder and matching underscore CAD module. No edits to the frozen prior research, shared builders, inventory or viewer.

Inputs: frozen `ho2s-online-20261003` identity/source delivery and `ho2s-dimensions-20261003` dimension delivery; three publicly linked Bosch product views identified there. Originals are available for pixel review but excluded from delivery. No generated predecessor. CAD mm, local sensor Z0 estimated ring bearing plane, +Z towards exhaust nose; connector in its own independent local frame with rear Z0/mouth Z44. Any side-by-side display offset is a presentation transform only. No host pipe, bung, harness mate or cable route exists in scope. Leads terminate in short cut stubs; do not interpret these as full catalog length or a connected harness.

## Evidence and working estimates frozen before CAD

Only **22 mm hex AF** is a primary dimensional value. All other numbers, handedness, fillets, hidden sections and region breaks below are estimates. The prior dimension contract's22-row table, photo picks and conditional sensitivity apply unchanged. M18×1.5 is a declared visual choice; neither photo nor interchange proves thread fit or manufacturing class. No pitch/diameter gauge acceptance.

| Region/detail | Working geometry in mm | Evidence/limit |
|---|---|---|
| Main shell | OD20, Z−38.5..−8.5, wall1 | Exterior photo estimate; hidden wall educational |
| Mounting region | hex AF22 at−7.8..−2.6; neck OD19 bridges−8.5..0; rootOD16.2, thread crestOD18/pitch1.5 at0..7.5 | AF primary; all other details estimated; right-handed trapezoidal ridge root halfwidth.65/crest halfwidth.08 |
| Central empty shell/mount | main ID18; mount bore9.9 | Educational void to avoid a fictitious solid cartridge; no target internals or gas/signal architecture implied |
| Ring | OD21.5, ID18, Z−2..0 | Visible separate metal annulus; not compressed gasket/seal proof |
| Protective cap | OD11.5, open atZ7.5, hemisphere radius5.75 centeredZ19.25 endsZ25; wall.8 | Rounded/slotted appearance supported; wall and exact end shape estimated |
| Cap slots | four equally spaced, width.7, overall length13 fromZ8.5..21.5 | Visible long slots supported; count/hidden angles/width/length estimated, not factory drawing |
| Rear closure | collarOD20.5 at−45..−38.5; reducerOD16.5 at−55..−45; exitOD12.5 at−65..−55; .5-mm conical shoulders within these envelopes | Stepped metal appearance supported; joins/stations/wall1 educational; no generic rubber boot |
| Exit insert | OD10.5, Z−66..−64; four holesOD1.3 on3.6-mm square | Pale insulation and four exits visible; spacing/depth/shape estimated |
| Exit collars | four red-brown annuliOD2.4/ID1.3, Z−66.2..−66 | Visible colored collars; material/compression unspecified |
| Sensor leads | OD1.3, square3.6, Z−78..−64, colors white/white/black/gray | Four visible leads supported; stubs only, no wire-to-pin electrical mapping or conductor gauge |
| Connector outer | front circularOD17 atZ23..44; rear rounded rectangle17×14 atZ0..25; corners3 | Exterior topology supported; all dimensions estimated |
| Connector void | circularID14 atZ26..44; rear cavity14×11 atZ−.1..31; corners2; back open | Hidden wall/web/mate depths educational estimates |
| Connector support face | diskOD14, Z32..35; four holesOD1.6 on6-mm square | Four contacts/photo face supported; dimensions educational |
| Connector seal | red annulusOD14/ID12.5 Z35..36 | Visible colored ring; dimensions/material/compression unknown |
| Connector contacts | four round pinsOD1.6, Z34..41, end fillet.2 | Four male round ends supported; no assigned cavity mapping/mating proof; hidden metal continuation omitted |
| Connector central divider | red strip width.9, Y−6..6, Z35..40 | Visible central red feature supported; dimensions and function unconfirmed |
| Connector latch | two railswidth1.2, Y7..11, Z22..39; spacing6; bridges Z22..23.2 and37.8..39 | Open latch form visible; flexure/hidden retention/spring force not modeled |
| Connector rear lead stubs | four OD1.3, on6-mm square, Z−10..2 | Separate cut stubs only; no correspondence to sensor leads asserted |

Exterior regions are separately selectable modeled regions, not a claim that each is separately serviceable or a verified production BOM. Exclude ceramic thimble, heater, electrodes, potting, crimp barrels, hidden seals and cable jacket/bundle wrap. These remain unknown or family illustration; do not fill the hollow body with invented internals.

## Checks fixed before CAD

Use existing `pan_fastener_thread_candidate.solid/cz` and prior exporter convention `(X,Y,Z)→(X,Z,−Y)/1000`. Each intended region must be one valid positive-volume STEP solid after roundtrip; each GLB must be watertight, winding-consistent and positive, with actual CAD/GLB bounds error <0.05 mm. Tessellation .012mm/.08rad and vertex merge6digits, inherited unchanged from body screw. Thread crest/root probes at eight angles and three interior turns, plus smooth cylinder negative control. Cap slots: radial passage probes through every declared slot at three axial stations; closed-cap negative control. Connector mouth must remain open ahead of pin ends; blocked-mouth control. Wire holes, annular ring and hollow shell have material/void probes. Pairwise overlap audit numeric threshold0.1mm³ (not manufacturing clearance); all deliberate overlaps must be declared or repaired. Actual exported front/side/rear/connector closeups compared to three source views; retain failures. No installation, flow-rate, thermal, motion/service or browser acceptance inferred.

Planned commands: `.venv-cad/bin/python scripts/check-ho2s-specimen-20261003.py`; systemPython render and package scripts. Reports bind exact source/checker/export hashes, local environment and previous source ledgers. Final handoff uses common quality gates. Freeze this contract hash in `reference/engine/ho2s-specimen-20261003-pre-cad.json` before modeling. Root review is required for delivery, not another owner approval.
