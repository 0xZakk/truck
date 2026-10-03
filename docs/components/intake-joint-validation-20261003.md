# Intake joint validation successor

## Contract

Issue #82/intake under engine #1; root owns integration. Preserve the frozen intake-joint-candidate-20261003 delivery (9 authored/34 generated files) unchanged. Owned prefix only: scripts, this handoff and `cad/engine/generated/intake-joint-validation-20261003`. No geometry, frozen/shared files or installed transforms changed.

First diagnose the protected head/injector comparison with lower-level OCC operation state and topology. An exception or null shape is never a pass. Record IsDone, available error flags, validity, face/solid counts, volume and an identical-input empty control plus shifted nonempty control. Then perform a whole-scene static audit of changed upper/lower/gasket versus every other current occurrence at current shared transforms. Use authoritative STEP bounds for broadphase, exact solids for intersecting bounds, existing0.1mm³ numerical audit convention (not factory tolerance), and explicit operation errors. Bind all input hashes before/after. Seven existing stud IDs use proposed positions as a separate unresolved hypothesis; old and proposed placement evidence must remain distinguishable. No automatic acceptance or motion/retention claim.

Root source review accepts preservation of the center/order correction only. Known visual gap: actual MS93838 has a broader continuous asymmetric web around the middle pair/offset hole; the candidate's circles/straps/discrete central H5 ear do not reproduce that silhouette. A later successor should trace that full outline at the same explicit estimated scale. Upper decorative exterior must also be restored before installation. This validation does not waive those gaps.

## Delivery and findings

Readiness: **validation research; candidate remains unaccepted**. No geometry repair, relocation, installation or frozen-package edit.

The original head/injector error is a genuine Boolean failure. `boolean.json` records successful valid125-face old/new region intersections, followed by **IsDone=false** for both directional cuts. Old-minus-new returns invalid topology with a signed negative mass; new-minus-old returns null. The identical-input control is IsDone=true and returns a valid non-null empty compound with zero faces/solids/volume. A0.5mm translated control succeeds and returns11,684.327mm³. The binding exposes no HasErrors/GetReport-style methods; the available-operation-state list is recorded. Nothing converts the failed operation into a pass.

`seats.json` separately compares the actual six head-face0.1mm bands, six injector socket upper0.1mm annuli and three rail mounting upper0.1mm annuli. All15 masks, both directional cuts and resulting topology succeed; all symmetric differences are0mm³. This establishes those bounded seats only. It does not waive the broad curved-region failure or establish production dimensions, compression or retention.

The whole static audit covers741 definitions/1349 occurrences and **4062 pairs**: three changed parts versus1346 other installed occurrences each (4038), seven proposed stud poses versus three changed parts (21), and three mutual candidate pairs. Authoritative CAD-space STEP bounding boxes with transformed corners exclude3685 pairs;377 pairs receive exact OCC Common operations. There are no invalid neighbor definitions or operation errors. Every input hash is unchanged before/after. The audit uses whole changed parts, not added-material-only inheritance.

Of4038 installed comparisons,3685 have disjoint CAD bounds,337 have no volume above the existing0.1mm³ convention, and16 overlap. Fifteen overlaps are the unchanged installed positions of studs2–6 against allthree changed parts. Their repositioning is required for any coordinated successor. The21 proposed stud comparisons have no volume above0.1mm³; this does not assign paired-hole roles or prove clamping/engagement. The three mutually coordinated candidate pairs also have no volume above0.1mm³.

The remaining new conflict is **efi-upper-intake versus fuel-return-tube:295.5873187mm³**, compared with0mm³ for the installed upper. Both exact operations succeed with valid topology. The intersection occupies X[-343.268,-312.696],Y[-194,-186],Z[366,371.5]mm: the rear H9 ear/flange, **not an upper runner bulge**. `fuel-return-conflict.json`, `fuel-return-intersection.step` and the inspected `fuel-return-conflict.png` record the actual solids. The detail render hides the tube skin and marks its axis so the red intersection remains visible.

`cad/engine/fuel_injection.py` defines the current8mm-OD tube's provisional points as `(0,-163,383.5)→(0,-163,345)→(0,-190,345)→(0,-190,370)→(-345,-190,370)`. Its comment explicitly says this is not a traced production bend. The source-compared H9 rear ear points toward the head; the candidate's estimated absolute anchors place it through that old route. No evidence supports deleting the ear or moving its hole to fit the old line. Next scope is to identify actual return routing and its fixed connections, then coordinate a source-compared tube/ear/fastener stack. Any new line route must be labeled and supported independently of simply eliminating this overlap.

## Reproduction

From repository root:

```sh
.venv-cad/bin/python scripts/intake-joint-validation-20261003-boolean.py
.venv-cad/bin/python scripts/intake-joint-validation-20261003-seats.py
.venv-cad/bin/python scripts/intake-joint-validation-20261003-context.py
.venv-cad/bin/python scripts/intake-joint-validation-20261003-conflict.py
MPLCONFIGDIR=/tmp/intake-joint-validation-mpl python3 scripts/intake-joint-validation-20261003-render.py
```

Generated reports and authored CAD renders live in `cad/engine/generated/intake-joint-validation-20261003/` (about4.6MB). Runtime follows the frozen candidate package: repository CAD Python/build123d/OCC plus separate system numpy/matplotlib plotting. The temporary plotting cache is disposable. No evidence depends on it. No original photographs are redistributed. Root owns artifact preservation/release; no release URL assigned by contributor. Ledger records source/artifact/input hashes and verifies the frozen candidate's9/34 hashes remain unchanged.

## Quality gates and next actions

- Reproduction/input scope: PASS hashes/completeness; root review pending.
- Broad protected-region equality: **FAIL operation**, not empty result; preserve diagnostic and investigate an authoritative retained-solid boundary or robust source-curve comparison before claiming full lower-body preservation.
- Actual bounded head/injector/rail seats: PASS15 comparisons; source dimension certainty unchanged.
- Whole static context: **FAIL**, one additional rear-ear/return-line interference plus old stud placements incompatible with the revised joint. The proposed stud poses are hypotheses only.
- Source visual fidelity: root has reviewed center/order correction; full gasket contour still needs tracing and upper decorative exterior restoration. No source-supported feature is waived.
- Motion/disassembly, fastener roles/engagement/tool access, browser integration: NOT RUN/unresolved. Static audit is not installed approval.
- Learning/diagnostics: N/A for this validation successor; no product learning changed.

Issue remains open. Preserve both frozen packages and use a new prefix for return-interface sourcework or geometry repair. No shared or canonical changes. No process remains running after delivery. Model/usage billing data unavailable.
