# Isolated timing-block feature migration contract

## Assignment and baseline

Issue32 under engine1. Root is integration owner; timing worker owns new block discovery/candidate files, cover worker owns front land/pan registration. Root directly reviewed and accepted the bounded thrust-land/axial candidate for further integration preparation, **not installation or production fidelity**. Earlier core/land proofs remain frozen.

Branch `engine/timing-core-pan-joint`, base commit `705c4683c199d8c5e28addba018bc8d1bdd399b1` (merged rear-only PR95). Current canonical manifest is `ab99fff2f63ad5dfc21fde8d12a32fc2a3d65832e6c8664baefd99d94403f7bf`. Owned first-stage files: `cad/engine/timing_block_migration_candidate.py`, `scripts/check-timing-block-baseline.py`, `inventory/engine/timing-block-baseline-validation.json`, this handoff and `generated/timing-block-migration-candidate/`. No shared builder, canonical geometry or inventory edits.

Units are millimeters, X longitudinal. The proposed cam-axis hypothesis remains Y95.109820990/Z76.087856792 (same-ray121.8 mm), deltaYZ+5.109820990/+4.087856792. These are estimates, not selected production coordinates; the4.804-inch forum claim remains an unused lead. No migrated block has been built at this checkpoint.

## Baseline regeneration proved

`baseline(stage=None)` imports the current builder, redirects its output constants defensively, substitutes a shape-capture callback for `define`, then calls **`full_engine.define_block_casting()`**. The shared exporter and `main()` never run. Necessary post-definition block adapters are applied in their original order:

1. Base casting plus direct pushrod-cover, retention, rear-plug, oil-drive, accessory, Thermactor and filter interfaces already called by `define_block_casting`.
2. `oil_pan_joint_v9_candidate.block_interface`.
3. `accessory_carrier_1994.block_interface` (the preceding carrier replacement adapter is identity for block).
4. `water_pump_joint_integration_desktop.replacement('block', shape)`, including its ordered support/pump block hooks.
5. The original three dipstick block-feature statements, extracted unchanged from `dipstick_tube_candidate.candidate` through `modified_block`; tube/blade geometry is not regenerated unnecessarily.

The six manifold adapter registries and source-sized definition adapter are asserted not to own block. Later integration adapters do not alter block except dipstick. This ordering is supported by current source and confirmed geometrically, not assumed from stale component documentation.

Report `inventory/engine/timing-block-baseline-validation.json`, SHA256 `18fa33f43332512b5d3c6445ac05f3ba2071f1352129af67c1a842dcbe24efc5`: **PASS exact baseline regeneration**. Symmetric-difference extra0 / missing0 mm³ against the actual canonical STEP; all five saved stages are valid single solids. Elapsed31.25 seconds. Canonical input hashes remained unchanged during the run. Seventy-three imported CAD source modules, dimensions and checker are recorded; not every imported module affects this block.

The source module used by this baseline is now a frozen prerequisite. A future feature-migration implementation should use a new revision/module rather than silently modifying its hash and claiming this proof remains current. No old bore was filled, and no canonical file was regenerated.

## Exact proposed changed-feature contract — for root review

| Original feature | Proposed change | What remains fixed / why |
|---|---|---|
| Cam-side stock: `Pos(0,90,84)*Box(LENGTH,55,110)` | Center becomes(0,95.109820990,88.087856792); stock dimensions retained | Main casting/crankcase, cylinders and main saddles are rebuilt with their original expressions, not translated |
| Twelve lifter guide cutters: cylinderX±25,Y90,Z150, radius`LIFTER_BORE_R`, length235 | Y95.109820990/Z154.087856792; X, radius and length retained | Shifts complete guide axis with proposed lifter stack; no new arbitrary guide sizing |
| Continuous cam tunnel: center(0,90,72), radius`CAM_BORE_R`, length`LENGTH+2` | Center(0,95.109820990,76.087856792); radius/length unchanged | No filling of the old bore; regenerate the uncut source stock and make only the new cut |
| Four journal-support interfaces | Evaluate bearing stationsX-334,-110,110,360.5 at new tunnel center; retain their widths/radii | Existing model has continuous stock and tunnel, not four separately modeled cast bosses. Do not invent discrete production supports; verify material support/contact at each station |
| `machine_block_bolts` | Conjugate this cam-retention-only cut by delta | Plate axialX373 and relative two-socket pattern stay unchanged |
| `machine_block_seat` | Conjugate this rear cam boss/tunnel/seat-only function by delta | Rear faceX-373, seat depth/radii and replacement plug comparison retained |
| `oil_drive_block_interface` | Conjugate the complete connected distributor/pump block feature by delta, including gear pocket, neck/lower/intermediate bores, clamp pad/socket and pump feet | Whole branch follows the numeric fixed-length drive solution. Feet endpoints embedded in this feature also shift; none are left attached to stale datums |

Conjugation is `translate(+delta, feature(translate(-delta, input)))`. It is permitted only for a function whose **entire** scope belongs to the shifted interface; the input block's transforms cancel. It must never wrap `define_block_casting`, the pan/carrier/pump/adapters, or unrelated features. The three literal source placements above should be parameterized through a checked function AST or isolated equivalent implementation with an exact zero-delta baseline test and exact expected edit count, not broad text substitution.

Keep fixed: all crank/main bore coordinates; cylinder axes/bore diameters; deck planeZ254; head-bolt axes/holes; block outer base/crankcase expressions; pushrod-cover window, perimeter rail and six fastener webs; accessory/Thermactor/filter interfaces; current pan joint, carrier1994, water-pump joint and dipstick feature. The fixed side-cover/retainer/dipstick datums avoid silently expanding this scope into their attached components. New guide openings may change deck material locally, so “fixed deck” means plane/other sealing regions, not a false claim that the migrated guide holes are unchanged. If the fixed side-cover structure obstructs shifted guides, report the conflict for coordination rather than move it by stealth.

## Protected-region and candidate gate plan

Before expensive candidate construction, root reviews this feature contract. The next isolated implementation must first reproduce the zero-delta baseline. Then:

- Preserve crank/main bore and bearing-interface material in named local radial masks, cylinder bore/wall masks, head-bolt socket masks and deck sealing band outside the union of old/new lifter passages. Bind dimensions and exact masks in the checker before acceptance. Verify plane/axis coordinates independently; do not choose masks retrospectively to hide a changed interface.
- Report complete added/removed material and its containment in declared cam-side/retention/rear-seat/drive-feature regions. Unrelated accessory/filter/pump/dipstick/pan interfaces require zero differences within their protected masks, even where rebuilt after the moved feature.
- Check shifted shaft and all four bearings, rear plug seat, stationary plate/bolt sockets, moving thrust core and shifted lifter guide axes against the new block. Preserve the prior axial-core proofs only for their unchanged inputs; new block/context requires fresh affected checks. Check translated distributor/pump block interfaces against the numeric branch, including fixed shaft length and actual support/socket contact. Do not equate drilled clearance with bearing contact or oil-feed continuity.
- Export valid single-solid STEP/GLB; roundtrip, mesh integrity and bounds checks; actual mesh/sections. Negative controls should retain one old guide/tunnel or stationary socket and detect the mismatch. No full engine motion sweep until this localized feature construction is coherent.

## Front cover/pan ownership boundary

Cover worker's module is `cad/engine/timing_cover_front_joint_candidate.py`; API `build(pan_world)` returns isolated parts/metadata and is still under review. Its proposed future block land is a separate uninstalled shape: main-gasket archX363..373 trimmed atZ>=-24.5, local rail supportX335..365 and screw pads near(X353,Y-133.4/162.2). Main gasketX373..373.8, cover rear373.8/front415, seal410..418. Rear/bodyX<=335 and twenty pan stations are protected in that worker's scope. New front flange/gasket spansX335..399/Y-149..213; bridge projectionX365..373.8 avoids the main land.

**Do not apply or duplicate that standalone land as an installed block patch.** Leave existing front land/pan features untouched in this block candidate; root will coordinate the later union/seat review. Both current and proposed cam tip envelopes plus the-0.1 axial travel are already considered in the cover study; its reported rear cavity startsX378.009375, retaining nominal0.15 mm to the shifted rear gear endpointX378.159375.

## Validation, reproduction and handoff

Readiness: baseline-equivalence research/feature contract, not a migrated or installed component. Application evidence remains mixed comparisons/estimates. Dimensions/coordinates PASS for baseline identity only. CAD baseline valid/single-solid and exact volume comparison PASS. New migrated interfaces, visual review, motion/disassembly and browser NOT RUN. Learning/diagnostics N/A developer feature study. Baseline reproduction PASS; root feature-contract review pending. Existing browser restriction is not bypassed.

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-timing-block-baseline.py
```

Uses pinned Python3.13/build123d0.10.0; no metadata/export writes outside the owned generated directory/report. Restore canonical block STEP and repo source inputs using project artifact policy. Saved stages and log `generated/timing-block-baseline-check.log` make any future mismatch diagnosable. No private sources are redistributed. No process remains running at this checkpoint; model/effort/usage unavailable. Issue32 remains open. Exact next action is root review of the changed-feature/protected-region contract, then a new isolated migration implementation; previous core/land proofs remain frozen.
