# Timing-axis migration dependency audit

## Contract

- Assignment: #32, Timing gears, cam retention and front cover, under engine #1. Root is integration owner; stops/timing worker owns this research audit, coordinated with the cover worker. Issue read on 2026-09-30; acceptance remains open.
- Baseline: `124aa7c345af352459a800343ffc50f1e931367c`, branch `engine/exhaust-timing-joints`. Exact manifest and source hashes are in `inventory/engine/timing-axis-dependencies.json`. Root is independently integrating rear exhaust; the report is a captured timing snapshot, not a claim that a later whole-manifest hash matches.
- Owned files: this document, the dependency report, and `scripts/check-timing-axis-dependencies.py`. No geometry, canonical inventory, shared builder, viewer or frozen gear proof edits.
- Scope: identify current modeled datums and coherent future changes. No actual migration, CAD sweep or factory datum recovery. All dimensions below describe the model unless separately classified.
- Units/frame: millimeters; crank origin Y/Z=0/0, cam parallel to X at Y90/Z72. Local occurrence positions must be composed with parent transforms; e.g. cam gear local Y/Z=0/0 inherits `cam-motion`. Stable IDs and existing explode conventions must survive future installation.
- Inputs: local canonical manifest and named CAD/motion sources; available. Public replacement and forum evidence remains separately classified in the existing gear evidence handoff/lead ledger. No new proprietary sources required.
- Check: `python3 scripts/check-timing-axis-dependencies.py`; standard-library, read-only extraction to stdout. It asserts current axis, four bearings, twelve lifter bodies and one source-sized-v2 motion revision. This is not a geometric acceptance checker; physical negative controls are specified below for future work.

## Evidence and competing hypotheses

| Datum | Value | Class and limit |
|---|---|---|
| Current cam Y/Z | 90/72; radial center 115.256236 mm | Provisional model; `full_engine.py`, `cam-motion` |
| Independent gear study | 121.8 mm radial center; estimated transverse module 2.8, helix 25° | Candidate hypothesis, not source datum |
| Same-ray candidate Y/Z | 95.109821/76.087857; delta +5.109821/+4.087857 | Conditional arithmetic retaining the old, unverified direction |
| Alternative lead | 4.804 in = 122.0216 mm; only 0.2216 mm above candidate | Unverified Inliners assertion; repeat is the same author, not corroboration; see `reference/engine/timing-axis-datum-leads.json` |
| Published gear diameters | Cam167.894/crank86.36 mm | Elgin replacement comparison; diameter meaning/profile assumptions do not uniquely recover shaft spacing |

A center-distance scalar does not establish Y and Z independently. Neither alternative licenses same-ray placement, a simple vertical lift, or a new block datum. To distinguish 121.8 from 122.0216, seek an applicable Ford machined-block drawing with axis coordinates/tolerances, or identified matched-gear manufacturer drawing with working center and tooth/profile details. An identified block measurement needs crank/cam bore center fitting, datum setup, casting/year, repeated measurements and uncertainty materially below their 0.2216-mm difference (a research target of <=0.05 mm combined uncertainty would be useful, not a Ford tolerance). Perspective photos and rounded catalog ODs cannot settle this. Matching shafts/mandrels or coordinate metrology must account for bore wear, shell thickness, alignment and temperature. Do not infer the value from the forum's decimal precision.

## Actual dependency map

| Dependency | Current authority and modeled datum | Smallest coherent future scope |
|---|---|---|
| Cam, lobes and timing gear | `full_engine.py` cam-motion Y90/Z72; `valve_layout_integration.py` replaces twelve lobes; `rear_cam_clearance_desktop.py` changes rear journal X-330 to-334 | Move shaft and its inherited rotating gear/spacer/key consistently only after datum choice; preserve axial lobe stations unless independently revised. Revalidate 2:1 phase, lobe-to-follower contact and removal. |
| Four journals, bearings and block tunnel | `full_engine.py` cam stations; installed bearing X=-334,-110,110,360.5, all Y90/Z72. Continuous block tunnel is cut at Y90/Z72; shell radial thickness1.5 mm and widths22 mm are estimates | Rebuild block tunnel/support structure at new axis, place all bearings, preserve sourced radial ranges. Do not translate the entire block or leave the old open tunnel behind. Oil-feed drillings/indexing remain missing, so no lubrication acceptance claim. |
| Rear bore plug and seat | `expansion_plugs.py`: rear face X-373; cup envelope2.194in OD/.343in height; boss/tunnel/seat centered90/72 | Update rear boss, seat cutter and stationary `rear-cam-plug` together; validate sealing contact and shaft axial clearance. Envelope is replacement comparison, seat/press fit unresolved. |
| Front retention | `cam_retention.py`: faceX373, plate5.159375 mm, assumed endplay.1, gear centerX385.259375; stationary plate/bolts centered90/72 while spacer/key inherit cam-motion | Move stationary plate/bolt sockets/washer stack and rotating nose/spacer/key together; maintain documented axial stack and prove contact/clearance. Changing only parent misses stationary parts. |
| Twelve lifters and block guides | `full_engine.py` vertical bores at cylinder X±25/Y90; `valve_source_integration.py` active body datumZ114.8; `valve_source_layout.py` footZ90=CAM_Z72+baseR18 | Choose follower track relation explicitly. To retain current centered track geometry under same-ray migration, lifter axes and their complete nine-part internal stacks follow deltaY and deltaZ; block guide cutters, support walls and side-cover cavity must follow. Alternatively fixed guides require newly solved off-center contact and cannot inherit current lobe proof. |
| Pushrod chain and head passages | Active source-sized-v2 `valve_source_layout.py`, `valve_dimensions_candidate.py`: lower ballY90/Z139.7, overall257.556 mm, ball centers250.003354 mm, diameter7.9248 mm. Head passageY90; `rear_cam_clearance_desktop.py` gasket holeY90/r6 | Preserve replacement length rather than shorten it to force closure. Re-solve rocker cup geometry and pushrod orientation against retained valve/head datums; recut head/gasket passages with sealing-land checks. A rigid lifter shift while keeping old rods/pivots breaks closure. |
| Rocker and valve chain | Intake current pivotY51.071840/Z395.1246, valveY-12/Z261; exhaust has its own rest solution. `valve_source_layout.py` calibrates pivot using catalog lift, and shapes head pedestals/rocker cups | Recalculate full linkage with explicit unknowns before changing solid pedestals. Rocker/fulcrum/bolt/guide, cups and head pedestal sockets form one interface set; valve stems/seats and springs should remain reference constraints unless evidence requires changes. Recheck valve cover clearance. Historical builder prose about226.6-mm rods is superseded by active source-sized-v2 authority. |
| Cam-to-distributor drive | `oil_drive_layout.py`: driveX227.584, provisional20° tilt,36-mm spacing; gear frameY123.828934/Z59.687275; cam gear fused into camshaft atX227.584 | Holding current relative drive relation requires translating distributor/drive frame by the same deltaY/Z. Fixed distributor instead requires new crossed-helical geometry/spacing study, not the old unchecked mesh. Production tooth geometry/backlash already unresolved. |
| Distributor/pump/intermediate shaft | Current distributor origin[227.584,152.900647,139.561148], pump[224.084,60.620876,-113.975439], both -20°X rotation. `oil_drive_layout.py` derives these and block tunnel/supports from gear frame; Melling shaft length114.808/across-flats7.9248 preserved | Translate the whole connected drive branch to preserve socket engagement, then rebuild block boss/bore/clamp, pump mounting feet/holes and pickup tube start. Or retain pump and re-solve drive axis/engagement with evidence. Do not stretch the sourced intermediate shaft. Pickup endpoint/sump position, pump outlet joint, distributor cap/lead routing and nearby peripherals need fresh checks. |
| Cover/seal/pan | Independent cover worker owns source-compared shell and flange; crank seal remains on crank axis | Recheck full rotating envelope against coordinated cover and block seat, retaining fixed crank/seal. Resolve lower bridge/pan gasket collision separately; a gear-clear cavity is insufficient for installation. |
| Motion and refresh | `assembly_math.py` and `valvetrain_dispatch.py` dispatch source-sized-v2 to `valve_source_integration.py`; browser equivalent `viewer/engine-valve-source.js`, `atlas.js` | Update CAD and browser datum/kinematic authorities together. Partial refresh must not reapply old90/72 hardcodes, old head passages or old shaft frame. Preserve IDs; bind actual neighboring shapes/transforms, not only module names. |

## Ordered migration and gate plan

1. **Resolve or explicitly bound axis evidence.** Select Y/Z coordinates, center uncertainty, source/application limits and profile hypothesis as a coordinated contract. A full-engine translation is not authorized by this audit. Freeze crank, axial station convention and sourced radial/length dimensions.
2. **Solve mechanisms numerically before CAD.** Timing pair at selected center/profile; all twelve cam/follower/pushrod/rocker closures; crossed-helical distributor drive and fixed-length pump shaft/socket chain. Use retained head/valve datums as constraints; reject an inconsistent system rather than distort catalog dimensions. Existing candidate proof is only reusable if geometry and transforms remain equivalent within its stated scope.
3. **Regenerate coherent interface sets in an isolated stage.** Cam/bearings/tunnel/rear plug/front retention first; lifter guides, head/gasket passages and rocker pedestals next; distributor/pump supports, drive tunnel and pickup/outlet paths next; coordinated cover/block flange/pan junction last. Preserve unrelated block/head features using bound baselines, not a broad destructive rebuild.
4. **Check each interface and exports.** Exact shaft/bearing and spacer/thrust contact/clearance, key engagement, bore coaxiality, guide walls/oil-route limits, flange/socket contact, passage continuity and sealing lands. Valid intended solids, STEP roundtrip, watertight GLBs and mesh/CAD bounds at established project tolerances. Do not invent press fits or source tolerances.
5. **Motion and fault sensitivity.** 720° engine cycle with all twelve followers/rockers and connected drive; adaptive worst-case samples around peak lift/contact transitions, gear engagement phase and closest neighbors. Report sampled coverage separately from continuous claims. Negative controls: retain one bearing at old center; omit one guide/passage update; freeze distributor while moving cam; misphase gear; restore old browser datum. Each must fail its named check.
6. **Replay, render and integration review.** Full and relevant partial-refresh replay, transform/geometry/hash guards, unaffected-component comparison, source/actual CAD views and complete staged explosion/reassembly. Root reviews stage before installation; run affected static/motion/export checks, then browser selection/isolation/scale/reset/motion. Existing browser restriction means NOT RUN, never automatic accepted-installed status.

## Delivery, validation and restart

Readiness: **research audit**, not integration-ready. No STEP/GLB, physical learning content or new render is produced: N/A because no component geometry is authored. Existing gear render remains an independent hypothesis.

| Gate | Audit result | Limit |
|---|---|---|
| Application/coverage | PASS for identifying modeled dependencies | Production axes and variant remain unknown |
| Dimensions/coordinates | PASS extraction and conditional arithmetic | No factory datum or world-shape clearance claim |
| CAD/export, source/visual | N/A to this read-only audit | Prior gear/cover candidates retain their separate gates |
| Installed interfaces; motion/disassembly | NOT RUN | Ordered future checks above; no migration performed |
| Learning/diagnostics | N/A: developer dependency audit | Not service instructions |
| Browser | NOT RUN | Root reported security restriction; no alternate surface attempted |
| Reproduction/review | PASS local extraction; root review pending | Hash-bound snapshot, not timeless validation |

Reproduce from repo root with system Python3 (standard library only):

```sh
python3 scripts/check-timing-axis-dependencies.py > inventory/engine/timing-axis-dependencies.json
```

Regenerating the report intentionally replaces its snapshot; retain historical version in Git before rebinding a later manifest. Root should review this audit and coordinate the datum contract with cover ownership before any CAD mutation. Issue #32 stays open. No background processes running; model/effort/usage unavailable. No shared or canonical files changed by this audit.
