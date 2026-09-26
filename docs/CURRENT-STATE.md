# Current engine integration — 2026-09-26

Repository root is authoritative. Preview: http://127.0.0.1:8081/viewer/engine.html. Branch: `engine/next-interface-contracts`. Previous main checkpoint: PR #89 (`2cc2000`); current checked milestone is being committed. **Engine unfinished.**

## Installed state and verification

Manifest SHA-256: `bfab1f2596991d27fe5e52e90f02d070eb034f9de8c2cd72d3dd44666d6c8bb9`. **718 definitions / 1,322 occurrences.** New installed content: coordinated throttle lever/keyed shaft/ball/pin/bracket/shield/pushpin, one illustrative deforming return spring with captured hooks, and the dipstick blade/handle/guide/receiver/support hardware. Earlier pump-seal and bracket work remains integrated.

- Whole static QC: 5,062 exact broad-phase-selected pairs; no overlap above0.1mm³. All definition exports, mesh bounds and1,322-solid combined STEP checked. This is one static pose, not continuous motion or factory verification.
- Combined STEP: all1,322 occurrence labels unique; world-bounds roundtrip verified. Independent topology copies correct the old duplicate-name export defect. Report: `combined-step-export.json`.
- Throttle linkage46-pose and spring11-pose CAD studies passed. Installed reports form a sequence through intermediate manifest hashes, not independent claims against the final718 manifest. Spring viewer data includes91 exact-CAD-derived integer poses, conserved geometric wire length and fixed/moving hook checks; no return force or production spring-count claim.
- Dipstick: installed8-definition artifact/frame binding passes at current manifest; adapter replay and rejected pilot-pose reset pass. Candidate evidence covers64 static comparisons and797 exact crank/rod/piston checks at73 poses, continuous conservative motion envelopes, seated contacts and fault controls. The692.15mm axial datum and additional6.572804mm wave material length are distinguished. Oil calibration and elastic insertion remain unknown.
- Navigation:1,322 parts /1,521 links. Viewer learning resolves definition defaults to actual occurrence pages, including the shared cover/dipstick retainer. Transparency reveals the guide internals. Browser review remains scoped; extension-origin console noise is not called a clean console.
- Local source-record audit verifies179 captures. Three older bracket source records remain URL-only without local capture hashes; see `source-record-validation.json`. This is an outstanding provenance-registration gap, not hidden as a pass.

No check above completes the engine or certifies production dimensions, strength, sealing or operating behavior. All active CAD models remain explicitly provisional. Historical reports retain their original hashes; do not relabel the previous four-angle rotating-core report as a new whole-engine motion audit.

## Active isolated work

Three workers own bounded candidates; root owns canonical integration and QC.

1. Compact balanced intake, forward oil-fill cap/neck, coordinated throttle/EGR frames and fixed-end EGR exhaust/vacuum routes. Original neck failed cap removal under the long plenum. Revised removal, all12rockers and affected-neighbor checks are being finalized. Nested-placement Boolean anomalies require STEP-roundtripped world solids plus negative controls. The route now measures440.931mm but remains inferred; catalog length convention is unknown. Hose contact is nominal geometry, not sealing proof. Isolated adapter/staging work is underway; nothing from this set is installed yet.
2. Throttle plate retention: source-limited four-screw educational candidate, explicitly not a verified1994 count. Heads, plate seats, shaft engagement and motion checks are isolated; no canonical changes.
3. IAC attachments: exact1994 images establish two flange fasteners. Candidate body/gasket/pad mounting interfaces and fasteners are being developed; return-mechanism variant remains unresolved.

Purchased manuals and owner photos remain local/ignored. Candidate ledgers and reports are under `reference/engine/`, `docs/components/`, and `inventory/engine/`. Candidate status never implies installed acceptance.

## GitHub and next actions

CLI issue checklists #43/#16/#17/#78 were refreshed and verified against previously generated bodies, preserving pilot history. All issues remain open. Work inventory now has62 In-review import assessments and8 Backlog packages; those are tracking assessments, not completion counts or verified board writes.

**No Project status write has succeeded:** CLI lacks Projects scope and earlier device authorization expired. Desired changes remain queued in `inventory/engine/project-status-pending.json`. Use guarded `scripts/set-engine-project-status.py` after owner authorization, then verify writes. Do not claim board synchronization meanwhile.

Save/push this milestone and its matching private CAD archive; previous release `checkpoint-2026-09-26-interfaces` covers the old705/1,310 geometry. Continue integrating passing candidates, refreshing learning/tracking and checking affected interfaces/motion. Run combined/export/static/browser checks at coherent milestones. Whole-engine goal stays active; no review request or completion claim yet.
