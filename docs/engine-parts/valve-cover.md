# Valve cover, gasket and attachment hardware

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#35](https://github.com/0xZakk/truck/issues/35).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `f725260d8f1497a1b6f2aed9d41d01155bf2a82e7391d24ce866f352bb50cd5b`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Valve cover gasket** — `valve-cover-gasket`; modeled quantity **1**; provisional.
  - Instances: `valve-cover-gasket`
  - Source IDs: not recorded. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact production contours, dimensions and tolerances need applicable drawings or measurements.
- [ ] **Valve cover** — `valve-cover`; modeled quantity **1**; provisional.
  - Instances: `valve-cover`
  - Source IDs: engine-exploded-drawing, ford-engine-side-layout. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Profile lofts are visual approximations. Upper profiles lean22mm toward the cam side to clear the corrected rocker placement; this is a fit-study assumption. The base envelope and fill/ventilation locations require measurements of the installed truck cover.

## Additional known scope and reconciliation

- [ ] Cover bolts, load spreaders and grommets if applicable: identify and separate
- [ ] Oil baffle/breather interfaces and filler-neck thread
- [ ] Verify production cover and gasket geometry

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
