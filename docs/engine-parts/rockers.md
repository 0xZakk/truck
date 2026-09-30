# Rocker arms, fulcrums, guides and bolts

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#28](https://github.com/0xZakk/truck/issues/28).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `73de806af847c528e766151590d7b8235620893414c280711aa6ff382ca8a7e1`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Rocker attachment bolt** — `rocker-bolt`; modeled quantity **12**; provisional.
  - Instances: `c1-intake-rocker-bolt`, `c1-exhaust-rocker-bolt`, `c2-intake-rocker-bolt`, `c2-exhaust-rocker-bolt`, `c3-intake-rocker-bolt`, `c3-exhaust-rocker-bolt`, `c4-intake-rocker-bolt`, `c4-exhaust-rocker-bolt`, `c5-intake-rocker-bolt`, `c5-exhaust-rocker-bolt`, `c6-intake-rocker-bolt`, `c6-exhaust-rocker-bolt`
  - Source IDs: fsm-c69f7255fa10. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact production contours, dimensions and tolerances need applicable drawings or measurements.
- [ ] **Fulcrum guide** — `rocker-guide`; modeled quantity **12**; provisional.
  - Instances: `c1-intake-guide`, `c1-exhaust-guide`, `c2-intake-guide`, `c2-exhaust-guide`, `c3-intake-guide`, `c3-exhaust-guide`, `c4-intake-guide`, `c4-exhaust-guide`, `c5-intake-guide`, `c5-exhaust-guide`, `c6-intake-guide`, `c6-exhaust-guide`
  - Source IDs: fsm-c69f7255fa10. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact production contours, dimensions and tolerances need applicable drawings or measurements.
- [ ] **Rocker fulcrum** — `rocker-fulcrum`; modeled quantity **12**; provisional.
  - Instances: `c1-intake-fulcrum`, `c1-exhaust-fulcrum`, `c2-intake-fulcrum`, `c2-exhaust-fulcrum`, `c3-intake-fulcrum`, `c3-exhaust-fulcrum`, `c4-intake-fulcrum`, `c4-exhaust-fulcrum`, `c5-intake-fulcrum`, `c5-exhaust-fulcrum`, `c6-intake-fulcrum`, `c6-exhaust-fulcrum`
  - Source IDs: fsm-c69f7255fa10, melling-camshaft-specifications, melling-stock-valve-specifications, melling-pushrod-specifications. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact production contours, dimensions and tolerances need applicable drawings or measurements.
  - Open: Coordinated motion is a teaching construction. The smooth lobe law fits selected Melling SYB-38 scalars; the installed cam, full lift law, advertised checking height and production timing remain unverified.
  - Open: Rigid linkage and constant-wire spring deformation explain motion; hydraulic lash adjustment, spring dynamics, lubrication, fatigue and running-engine performance are not simulated.
- [ ] **Rocker arm** — `rocker-arm`; modeled quantity **12**; provisional.
  - Instances: `c1-intake-rocker`, `c1-exhaust-rocker`, `c2-intake-rocker`, `c2-exhaust-rocker`, `c3-intake-rocker`, `c3-exhaust-rocker`, `c4-intake-rocker`, `c4-exhaust-rocker`, `c5-intake-rocker`, `c5-exhaust-rocker`, `c6-intake-rocker`, `c6-exhaust-rocker`
  - Source IDs: fsm-c69f7255fa10, melling-camshaft-specifications, melling-stock-valve-specifications, melling-pushrod-specifications. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact production contours, dimensions and tolerances need applicable drawings or measurements.
  - Open: Coordinated motion is a teaching construction. The smooth lobe law fits selected Melling SYB-38 scalars; the installed cam, full lift law, advertised checking height and production timing remain unverified.
  - Open: Rigid linkage and constant-wire spring deformation explain motion; hydraulic lash adjustment, spring dynamics, lubrication, fatigue and running-engine performance are not simulated.
  - Open: Source-sized replacement envelopes are not installed-part identification. Absolute cam/deck/station datums, lifter socket/internal offsets and rocker geometry remain assumptions.
  - Open: Guide bore and separate spring load-test heights are service-reference constraints; spring wire/turns, keeper/groove construction and casting contours remain illustrative.

## Additional known scope and reconciliation

- [ ] Verify production contact contours, ratio, mounting and oil path

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
