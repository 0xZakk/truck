# Current engine integration — 2026-09-30

Repository root is authoritative. Preview: http://127.0.0.1:8081/viewer/engine.html. Checkpoint branch: `engine/runner-stops-and-evr`, [PR #94](https://github.com/0xZakk/truck/pull/94). **Engine unfinished.** Browser acceptance for this batch remains NOT RUN.

## Current checkpoint

**741 definitions / 1,349 occurrences.** Manifest SHA-256: `73de806af847c528e766151590d7b8235620893414c280711aa6ff382ca8a7e1`.

The upper intake has broader source-compared runner faces with unchanged bores, flange, plenum and cap envelope. An eleven-part illustrative EGR vacuum regulator has five matched disc/spring poses and viewer controls. The throttle has a threaded illustrative idle-stop screw/pad and a separate WOT contact lug, preserving the existing cable and spring mechanisms. A four-part air-cleaner housing/filter/seal candidate remains separate and uninstalled.

- Runner installation: zero geometry/replay differences; watertight fine mesh. Its historical report retains the runner-only manifest scope.
- EVR: eleven zero-difference STEP bindings, five spring poses, nearby-component checks and replay/frame guards pass after the final exporter refresh. Five promotion fault controls pass in a separate fresh stage. The earlier attempt to test a pre-install stage after installation correctly rejected its stale STEP hashes; that failed setup is retained in the logs.
- Stops: three zero-difference STEP bindings, watertight exports, four replay cases, frame/geometry rejection and transactional rollback controls pass. The frozen 47-pose/843-pair candidate proof is supplemented by 141 current-context exact comparisons. The subsequent EVR refresh changed only manifest array order; `throttle-stop-checkpoint-binding.json` verifies unchanged metadata, source dependencies and all recorded context/artifact hashes.
- Whole-engine static audit: **5,287 exact overlapping-bound comparisons, zero overlaps above 0.1 mm³**. Artifact, scale and hierarchy checks pass. This is one static pose, not continuous whole-engine motion or factory validation.
- Combined STEP: 1,349 unique occurrence names, valid solids and matching world bounds (maximum roundtrip difference 0.000351 mm). Navigation reaches all 1,349 parts / 1,548 links; discrete-motion, reset/request/failure and committed motion-asset tests pass. All 194 registered source captures pass integrity checks; applicability is separate.
- Browser automation rejected the localhost preview under its security policy. No alternate-surface bypass was attempted. Node tests and CAD renders do not replace selection, explosion/reset and installed-motion browser review. No Done transition or accepted-factory-replica claim.

Root review: `inventory/engine/runner-evr-stops-review.json`. Detailed component handoffs and installed reports retain their own hashes and scopes. Full clean-clone CAD rebuild remains unproven. Production dimensions, calibration, mounting/routing and the remaining physical BOM are tracked in `inventory/engine/completion-plan.json`; part count is not a completion percentage.

## Next batch in progress

Three workers own isolated files; root alone integrates shared assembly/viewer changes:

- Rear exhaust collector (#46): source-compared blended casting and bounded runner-seam repair. Original outer sweep exported open despite valid CAD; the repaired candidate uses a separate fine export. Root review and installation remain pending.
- Timing gears (#32): manufacturer comparisons support 58/29 teeth for an applicable replacement, rather than the current 48/24. Published diameters conflict with current shaft spacing. Independent helical-pair study uses explicitly estimated profile/centers; no installed cam translation. See `docs/components/timing-gear-evidence-review.md`.
- Timing cover/gasket (#32): manufacturer images establish seven holes, an open-bottom gasket, recessed cover cavity and lower pan bridge. The independent outline is unregistered; shell/flange and block-land proposals are being coordinated with the gear envelope. Scale, axial registration, strip identity and pan junction remain unresolved. See `docs/components/timing-cover-joint.md` and `timing-cover-shell-candidate.md`.

Do not mix these candidates into the checkpoint or overwrite their files. Preserve failed trials and critical interfaces. Worker completion does not authorize automatic installation.

## Restoration and tracking

Private CAD archive: [runner/EVR/stops checkpoint](https://github.com/0xZakk/truck/releases/tag/checkpoint-2026-09-30-runner-evr-stops). Verify `docs/cad-runner-evr-stops-checkpoint.json` and follow `docs/CAD-ARTIFACTS.md`. It contains active STEP geometry, combined assembly, required older fixtures and this batch's studies/proofs. Reference originals/composites, purchased manuals, owner photographs and the next batch are excluded. Browser meshes, including all five EVR spring poses, are committed.

CLI checklists #36, #43, #58 and #80 were refreshed and each write verified. Issue #1 records ongoing work. Project-column writes still lack Projects authorization. `inventory/engine/project-status-pending.json` records desired changes, **not observed board statuses**. No component was newly marked Done.
