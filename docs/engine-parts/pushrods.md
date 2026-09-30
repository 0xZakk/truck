# Pushrods

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#29](https://github.com/0xZakk/truck/issues/29).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `ab99fff2f63ad5dfc21fde8d12a32fc2a3d65832e6c8664baefd99d94403f7bf`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Hollow pushrod** — `pushrod`; modeled quantity **12**; provisional.
  - Instances: `c1-intake-pushrod`, `c1-exhaust-pushrod`, `c2-intake-pushrod`, `c2-exhaust-pushrod`, `c3-intake-pushrod`, `c3-exhaust-pushrod`, `c4-intake-pushrod`, `c4-exhaust-pushrod`, `c5-intake-pushrod`, `c5-exhaust-pushrod`, `c6-intake-pushrod`, `c6-exhaust-pushrod`
  - Source IDs: fsm-6f023139b5f8, melling-camshaft-specifications, melling-stock-valve-specifications, melling-pushrod-specifications. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact production contours, dimensions and tolerances need applicable drawings or measurements.
  - Open: Coordinated motion is a teaching construction. The smooth lobe law fits selected Melling SYB-38 scalars; the installed cam, full lift law, advertised checking height and production timing remain unverified.
  - Open: Rigid linkage and constant-wire spring deformation explain motion; hydraulic lash adjustment, spring dynamics, lubrication, fatigue and running-engine performance are not simulated.
  - Open: Source-sized replacement envelopes are not installed-part identification. Absolute cam/deck/station datums, lifter socket/internal offsets and rocker geometry remain assumptions.
  - Open: Guide bore and separate spring load-test heights are service-reference constraints; spring wire/turns, keeper/groove construction and casting contours remain illustrative.

## Additional known scope and reconciliation

- [ ] Verify length, end seats, hollowness and full-travel clearances

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
