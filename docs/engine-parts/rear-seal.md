# Rear crankshaft seal and sealing interface

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#33](https://github.com/0xZakk/truck/issues/33).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `73de806af847c528e766151590d7b8235620893414c280711aa6ff382ca8a7e1`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Rear crankshaft seal** — `rear-seal`; modeled quantity **1**; provisional.
  - Instances: `rear-seal`
  - Source IDs: not recorded. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact production contours, dimensions and tolerances need applicable drawings or measurements.

## Additional known scope and reconciliation

- [ ] Verify seal construction, lip orientation and mating crank/block surfaces

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
