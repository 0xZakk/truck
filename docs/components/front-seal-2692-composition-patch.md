# Component contract and handoff: 2692 seal composition patch

Root integration owner; issue #32 under Engine #1; baseline PR104. Propose replacement of the legacy one-piece front seal by three separately selectable physical parts and a stationary assembly. Preserve the old deep link via an explicit assembly alias. Replace the damper-hub asset; retain the newer coordinated cover, whose seal interface must match the qualified 2692 cover. Do not add the free-case comparison as a fourth installed physical part.

Owned: dedicated patch/check script, report and this handoff. Frozen source lessons, sources and localized seal assets remain read-only. Current combined manifest/adapter are frozen for another worker's static audit and will not be rewritten by this task.

All units/frames derive from the existing localized stage and current canonical occurrence parents. Original replacement-envelope dimensions and inferred internal construction remain explicit. Acceptance requires hash guards, serialized placement, actual cover-interface preservation and separate source/lesson links. Proposed deletion and link alias must be handled by the future composer/viewer, not hidden by keeping duplicate seals.

Bounded proposal passes: four local STEP/mesh world bounds (hub plus three seal parts), maximum0.01710mm. Actual full-cover delta contains ten pieces all outside X405..436/R43 seal region, with zero mask intersection. An earlier clipped-first coplanar Boolean returned the entire clipped volume in both directions; retained as FAIL in `front-seal-coordinated-cover-region-diagnostic.json`, not treated as real removed material. Full-shape-first report and each delta piece's bounding-box exclusion establish the separate interface-preservation result.

Reproduce `scripts/check-front-seal-cover-region.py` then `scripts/prepare-front-seal-2692-patch.py` with repository CADPython. Exact hash bindings and limits are in `front-seal-2692-composition-validation.json`. No canonical edits or installation/browser claim. Missing complete engine motion, source fidelity and other completion-plan work remain independent.

## Separate v2 composition

`python3 scripts/compose-corrected-engine-sealing-stage.py` combines this proposal and the worker's main-gasket/two-terminal-sealant proposal into `corrected-engine-stage-v2.json`, preserving the v1 manifest under audit. V2 has747 definitions /1,361 occurrences,13 new lessons and7 source records. Legacy one-piece seal is removed; `front-seal` alias points to new stationary assembly. Free-case comparison is not duplicated as an installed part. Hash-verified external lesson/source records are loaded explicitly. Shared cover-screw source enrichment is applied after comparing its staged definition against the worker's before value.

All IDs/parents/source references resolve. New runtime resolves all1,361 frames and the three seal parts at their qualified X414 assembly origin. This smoke check is not a collision test. The v1 audit's actual compressor, water-pump and ignition connection conflicts remain explicit in v2; it is not accepted installation. See `corrected-engine-stage-v2-composition.json` and `corrected-engine-stage-v2-frame-smoke.json` for exact inputs.
