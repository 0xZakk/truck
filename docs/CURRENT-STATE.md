# Current engine integration — 2026-09-26

Repository root is authoritative. Preview: http://127.0.0.1:8081/viewer/engine.html. Branch: `engine/intake-exterior-iac-detail`. Saved main checkpoint: PR #91 (`3e53f11`), both CI runs passed. **Engine unfinished.**

## Current local integration

**725 definitions / 1,333 occurrences.** Manifest SHA-256: `4f98bbdad7fb1996487d17c4a651de588cef39254efe24e96384375dbdce0c07`.

The current increment adds rounded upper-intake exterior shoulders, border ribs and source-visible wording; an illustrative captured IAC end closure; and two separate electrical terminals with an insulating carrier. The IAC has14 selectable parts. Exact-year electrical topology is supported; terminal construction, closure method, dimensions and font outlines remain estimates.

- Exterior stage:246 exact static neighbor pairs and552 throttle motion pairs across46 positions, no new collisions. Protected interfaces and cap-removal envelope remain intact.
- IAC closure/electrical: final neighbors and attachment coexistence pass. Electrical stage and installed checks bind12 related components, test translated/rotated parent frames and reject a shifted connector datum. No force, pressure or electrical performance is simulated.
- Ordered coordination→attachment→plate-retention→exterior→closure→electrical replay reproduces active changed geometry and frames in isolated output. This is **not** a clean whole-engine rebuild.
- Replay found a nested STEP compound whose container volume reports zero despite one valid solid. `cad_metrics.solid_volume` now measures enclosed solids. The original thresholds remain; nested round-trip and deliberately removed-material controls pass.
- Combined STEP export:1,333 uniquely named occurrences and world-bounds roundtrip pass.
- Navigation:1,333 parts reachable once /1,532 links. All189 source records pass capture registration/integrity checks; applicability is a separate question.
- Browser review covers intake assembled/exploded views,14-part IAC transparency/explosion and the individual control-terminal page. Extension-origin errors and one matching unlocated console error remain recorded; no clean-console claim.
- Whole-static audit passes5,204 exact broad-phase-selected comparisons, with no overlaps above0.1mm³; artifact/scale/hierarchy and1,333-solid combined checks pass. This is one static pose, not continuous whole-engine motion or production validation.

Reports: `inventory/engine/intake-detail-replay-validation.json`, `iac-closure-installed-validation.json`, `iac-electrical-installed-validation.json`, `intake-iac-detail-browser-review.json`, `combined-step-export.json` and `source-record-validation.json`.

## Parallel work and remaining gaps

1. Throttle cable/socket/compression spring candidate: proportions compared with Pioneer replacement photographs; bracket exit revision preserves reviewed anchors. Full motion sweep and final-current neighbor addendum remain in progress. Not installed.
2. Distributor center-contact study: Ford rotor photographs support a raised leaf and molded collar, replacing the old flat-contact approximation. Cap center construction still being reconciled. Not installed.
3. PCV connections: exact-year instructions distinguish fresh-air breather from valve-to-manifold vacuum return. Port/routing evidence is being reconciled before geometry. Not installed.

Upper-intake support research establishes a below-throttle mounting pad and strap but not the lower anchor. The current casting/cover datums may need coordination; no arbitrary brace is installed. See `reference/engine/intake-support-review.json`.

The broader remaining work is in `inventory/engine/completion-plan.json`. All active geometry remains provisional. A collision pass is not proof of production fit, completeness, sealing or strength.

## GitHub and restoration

PR #91 and its private [CAD checkpoint](https://github.com/0xZakk/truck/releases/tag/checkpoint-2026-09-26-intake-attachments) preserve722 definitions /1,330 occurrences. GitHub asset checksum matches the recorded local archive. The725-definition archive is prepared for publication; see `docs/CAD-ARTIFACTS.md` and its checkpoint record.

CLI issue checklists #36, #43 and #44 reflect the current inventory; #1 records the saved milestone. Project column writes still lack token authorization. `inventory/engine/project-status-pending.json` contains desired transitions, **not observed board status**. No engine component is newly marked Done.

Preserve worker files and frozen candidate evidence. Shared assembly changes belong to the integration owner. Never upload purchased manuals, owner photographs or local third-party photo comparisons.
