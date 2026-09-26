# Current engine integration — 2026-09-26

Repository root is authoritative. Preview: http://127.0.0.1:8081/viewer/engine.html. Branch: `engine/intake-and-attachment-coordination`. Main checkpoint: merged PR #90 (`fb2a1e7`), with passing GitHub checks. **Engine unfinished.**

## Saved main milestone and verification

Manifest SHA-256: `bfab1f2596991d27fe5e52e90f02d070eb034f9de8c2cd72d3dd44666d6c8bb9`. **718 definitions / 1,322 occurrences.** New installed content: coordinated throttle lever/keyed shaft/ball/pin/bracket/shield/pushpin, one illustrative deforming return spring with captured hooks, and the dipstick blade/handle/guide/receiver/support hardware. Earlier pump-seal and bracket work remains integrated.

- Whole static QC: 5,062 exact broad-phase-selected pairs; no overlap above0.1mm³. All definition exports, mesh bounds and1,322-solid combined STEP checked. This is one static pose, not continuous motion or factory verification.
- Combined STEP: all1,322 occurrence labels unique; world-bounds roundtrip verified. Independent topology copies correct the old duplicate-name export defect. Report: `combined-step-export.json`.
- Throttle linkage46-pose and spring11-pose CAD studies passed. Installed reports form a sequence through intermediate manifest hashes, not independent claims against the final718 manifest. Spring viewer data includes91 exact-CAD-derived integer poses, conserved geometric wire length and fixed/moving hook checks; no return force or production spring-count claim.
- Dipstick: installed8-definition artifact/frame binding passes at current manifest; adapter replay and rejected pilot-pose reset pass. Candidate evidence covers64 static comparisons and797 exact crank/rod/piston checks at73 poses, continuous conservative motion envelopes, seated contacts and fault controls. The692.15mm axial datum and additional6.572804mm wave material length are distinguished. Oil calibration and elastic insertion remain unknown.
- Navigation:1,322 parts /1,521 links. Viewer learning resolves definition defaults to actual occurrence pages, including the shared cover/dipstick retainer. Transparency reveals the guide internals. Browser review remains scoped; extension-origin console noise is not called a clean console.
- The historical718 audit had three missing capture registrations. Those are resolved in the current batch described below; this does not retroactively change that historical result.

No check above completes the engine or certifies production dimensions, strength, sealing or operating behavior. All active CAD models remain explicitly provisional. Historical reports retain their original hashes; do not relabel the previous four-angle rotating-core report as a new whole-engine motion audit.

## Current unmerged integration

Compact intake/oil-fill/EGR coordination is installed (719 definitions /1,323 occurrences), followed by IAC attachments and plate retention (722 /1,330). Intake installation bound8 definitions and67 moved frames; IAC installed checks bind6 definitions, recheck25 nearby parts, motion/withdrawal and replay, and preserve the rigid throttle relocation. Plate retention has a47-pose staged sweep with940 exact neighbor pairs and a matching installed binding/three-pose smoke check. Navigation passes1,330 parts /1,529 links. Scoped browser review sees the new seal, compact manifold and11-part IAC through its housing. See `intake-iac-browser-review.json` and `throttle-plate-fasteners-browser-review.json`. Their exact reviewed snapshots are retained.

Current manifest SHA-256: `f1dc26ba64eb0ba1e8fede4ef42e23a5ae3e288dbeae3cc4b2558cf4148a4a70`. Three existing citations now bind saved captures; registration changed only source records, preserving geometry, poses and learning. All186 source records pass capture integrity/registration checks. This does not certify applicability or factory accuracy.

The current batch passed5,191 exact static pairs with no overlap above0.1mm³ and all artifact/scale/hierarchy checks; combined STEP contains1,330 uniquely named occurrences. The geometry audit/export retain their62dcb37f manifest hash. A subsequent source-summary registration changed only source metadata; `intake-batch-geometry-binding.json` verifies the transition to the current manifest and all722 unchanged part STEPs plus combined STEP. No old numerical check is relabeled as a fresh run. This is still one static pose, not whole-engine dynamic or production verification.

Three workers continue bounded isolated work while root owns promotion and shared viewer:

1. Intake exterior ribs, rounding and source-visible lettering, preserving the accepted runner/flange/port and cap-removal geometry.
2. Engine-end accelerator cable/socket and a separate cable-end compression spring. Manual evidence supports the spring, but seats, socket retention and routing remain inferred; feasibility work is isolated.
3. IAC end-closure retention and sealing contact. Factory closure construction remains unidentified; candidate will identify assumptions explicitly.

Purchased manuals and owner photos remain local/ignored. Candidate ledgers and reports are under `reference/engine/`, `docs/components/`, and `inventory/engine/`. Candidate status never implies installed acceptance.

## GitHub and next actions

CLI issue checklists #15/#36/#44/#59/#43 were refreshed and verified for the1,330-part snapshot, preserving pilot history. Earlier#16/#17/#78 updates remain saved. All issues remain open. Work inventory now has62 In-review import assessments and8 Backlog packages; those are tracking assessments, not completion counts or verified board writes.

**No Project status write has succeeded:** CLI lacks Projects scope and earlier device authorization expired. Desired changes remain queued in `inventory/engine/project-status-pending.json`. Use guarded `scripts/set-engine-project-status.py` after owner authorization, then verify writes. Do not claim board synchronization meanwhile.

The718/1,322 milestone is committed and merged. Private release `checkpoint-2026-09-26-linkage-dipstick` contains the matching CAD archive; GitHub digest matches SHA-256 `c594cdb730ad306974612de4b89a9eda6b763bc12843e4adef699d5106854f5b`. Previous release `checkpoint-2026-09-26-interfaces` covers the old705/1,310 geometry. Continue integrating passing candidates, refreshing learning/tracking and checking affected interfaces/motion. Run combined/export/static/browser checks at coherent milestones. Whole-engine goal stays active; no review request or completion claim yet.
