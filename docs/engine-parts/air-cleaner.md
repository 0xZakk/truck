# Air cleaner, filter and intake ducts

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#80](https://github.com/0xZakk/truck/issues/80).

**Backlog** — Known scope not delivered as a complete modeled/installed package; applicability and quantity may need research.

Baseline manifest: `91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- No accepted installed definitions are mapped to this package; candidate artifacts may exist as noted below.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.


## Separate candidate parts (not installed)

- [ ] **Lower dirty-air tray** — `air-cleaner-lower-tray-candidate`; Isolated candidate; not installed. Local CAD/flow/seal checks pass; retention/body placement and browser acceptance remain open.. Source: `docs/components/air-cleaner-candidate.md`.
- [ ] **Twin-outlet clean-air cover** — `air-cleaner-twin-outlet-cover-candidate`; Isolated candidate; not installed. Local CAD/flow/seal checks pass; retention/body placement and browser acceptance remain open.. Source: `docs/components/air-cleaner-candidate.md`.
- [ ] **Pleated paper element** — `air-cleaner-paper-element-candidate`; Isolated candidate; not installed. Local CAD/flow/seal checks pass; retention/body placement and browser acceptance remain open.. Source: `docs/components/air-cleaner-candidate.md`.
- [ ] **Filter perimeter seal** — `air-cleaner-perimeter-seal-candidate`; Isolated candidate; not installed. Local CAD/flow/seal checks pass; retention/body placement and browser acceptance remain open.. Source: `docs/components/air-cleaner-candidate.md`.

## Additional known scope and reconciliation

- [ ] Four-part housing/lid/filter/seal candidate remains isolated; cover screws are source-supported but their count, pattern and retention are unknown.
- [ ] Twin intake ducts/bellows, clamps and throttle connections visible in owner photos
- [ ] Inlet snorkel and body mounts: verify routing and variant

## Cross-system boundaries

Coordinate with [#7](https://github.com/0xZakk/truck/issues/7), [#12](https://github.com/0xZakk/truck/issues/12). Keep the current engine-mounted component here; agree ownership before adding its vehicle-side continuation.

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
