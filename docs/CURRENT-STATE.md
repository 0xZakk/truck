# Current engine integration — 2026-09-26

Repository root is authoritative. Preview: http://127.0.0.1:8081/viewer/engine.html. Branch: `engine/cable-and-distributor-contact`. Saved main checkpoint: PR #92 (`74ca528`), push and PR CI runs passed. **Engine unfinished.**

## Working733-definition integration

Branch `engine/cable-and-distributor-contact` now has **733 definitions /1,341 occurrences**, manifest `0656841ba587a3f05d193aa75fb711f320ddf732cc0343c68504836c9ea7537d`. Curved rotor center leaf and seven-part cable/socket/spring mechanism are installed; canonical scope checks and browser motion/explosion/reset review pass. Direct individual-part entry was repaired by synchronizing its controls with the engine page. Navigation reaches1,341 parts/1,540 links;191 source records pass capture-integrity checks.

Combined STEP export passes1,341 unique occurrence names and bounds. Whole-static audit passes5,249 exact overlapping-bound comparisons with zero overlaps above0.1mm³; artifact, scale and hierarchy checks pass. This is one static pose, not continuous whole-engine motion or production fit. The private restoration archive is uploading as a draft; see `docs/cad-cable-distributor-checkpoint.json`. CLI checklists #43, #16 and #71 have been refreshed; board columns remain authorization-blocked.

## Saved725-definition integration (PR #92)

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

1. Throttle cable/socket/compression spring candidate: proportions compared with Pioneer replacement photographs; bracket exit revision preserves reviewed anchors. Installed with47-pose proof/current-neighbor binding and91-pose viewer mesh checks. Browser acceptance passes; throttle stop candidate is next.
2. Distributor center-contact study: curved leaf and molded collar installed locally; current inventory726 definitions /1,334 occurrences. Exact shape/interface checks pass and browser verifies assembled/exploded distributor plus direct leaf page. Hidden cap construction remains unresolved. Not yet committed.
3. PCV connections: evidence gap documented; no manifold receiver inferred. Worker moved to an isolated EVR filter/vent candidate. Intake runner exterior refinement is also isolated pending Boolean robustness checks.

Upper-intake support research establishes a below-throttle mounting pad and strap but not the lower anchor. The current casting/cover datums may need coordination; no arbitrary brace is installed. See `reference/engine/intake-support-review.json`.

The broader remaining work is in `inventory/engine/completion-plan.json`. All active geometry remains provisional. A collision pass is not proof of production fit, completeness, sealing or strength.

## GitHub and restoration

PR #92 and its private [CAD checkpoint](https://github.com/0xZakk/truck/releases/tag/checkpoint-2026-09-26-iac-detail) preserve725 definitions /1,333 occurrences. The archive includes3,642 files and its224,076,800-byte upload is recorded in the checkpoint manifest; see `docs/CAD-ARTIFACTS.md` and its checkpoint record.

CLI issue checklists #36, #43 and #44 reflect the current inventory; #1 records the saved milestone. Project column writes still lack token authorization. `inventory/engine/project-status-pending.json` contains desired transitions, **not observed board status**. No engine component is newly marked Done.

Preserve worker files and frozen candidate evidence. Shared assembly changes belong to the integration owner. Never upload purchased manuals, owner photographs or local third-party photo comparisons.
