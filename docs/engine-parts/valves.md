# Intake/exhaust valves, springs, retainers and keepers

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#27](https://github.com/0xZakk/truck/issues/27).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `f725260d8f1497a1b6f2aed9d41d01155bf2a82e7391d24ce866f352bb50cd5b`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Valve spring retainer** — `spring-retainer`; modeled quantity **12**; provisional.
  - Instances: `c1-intake-retainer`, `c1-exhaust-retainer`, `c2-intake-retainer`, `c2-exhaust-retainer`, `c3-intake-retainer`, `c3-exhaust-retainer`, `c4-intake-retainer`, `c4-exhaust-retainer`, `c5-intake-retainer`, `c5-exhaust-retainer`, `c6-intake-retainer`, `c6-exhaust-retainer`
  - Source IDs: not recorded. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact production contours, dimensions and tolerances need applicable drawings or measurements.
- [ ] **Valve keeper half** — `valve-keeper`; modeled quantity **24**; provisional.
  - Instances: `c1-intake-keeper-1`, `c1-intake-keeper-2`, `c1-exhaust-keeper-1`, `c1-exhaust-keeper-2`, `c2-intake-keeper-1`, `c2-intake-keeper-2`, `c2-exhaust-keeper-1`, `c2-exhaust-keeper-2`, `c3-intake-keeper-1`, `c3-intake-keeper-2`, `c3-exhaust-keeper-1`, `c3-exhaust-keeper-2`, `c4-intake-keeper-1`, `c4-intake-keeper-2`, `c4-exhaust-keeper-1`, `c4-exhaust-keeper-2`, `c5-intake-keeper-1`, `c5-intake-keeper-2`, `c5-exhaust-keeper-1`, `c5-exhaust-keeper-2`, `c6-intake-keeper-1`, `c6-intake-keeper-2`, `c6-exhaust-keeper-1`, `c6-exhaust-keeper-2`
  - Source IDs: not recorded. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact production contours, dimensions and tolerances need applicable drawings or measurements.
- [ ] **Valve stem seal** — `valve-seal`; modeled quantity **12**; provisional.
  - Instances: `c1-intake-seal`, `c1-exhaust-seal`, `c2-intake-seal`, `c2-exhaust-seal`, `c3-intake-seal`, `c3-exhaust-seal`, `c4-intake-seal`, `c4-exhaust-seal`, `c5-intake-seal`, `c5-exhaust-seal`, `c6-intake-seal`, `c6-exhaust-seal`
  - Source IDs: not recorded. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact production contours, dimensions and tolerances need applicable drawings or measurements.
- [ ] **Intake Valve** — `intake-valve`; modeled quantity **6**; provisional.
  - Instances: `c1-intake-valve`, `c2-intake-valve`, `c3-intake-valve`, `c4-intake-valve`, `c5-intake-valve`, `c6-intake-valve`
  - Source IDs: fsm-ff8bb019d348, melling-camshaft-specifications, melling-stock-valve-specifications, melling-pushrod-specifications, melling-valve-progressive-size-chart-2025. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact production contours, dimensions and tolerances need applicable drawings or measurements.
  - Open: Coordinated motion is a teaching construction. The smooth lobe law fits selected Melling SYB-38 scalars; the installed cam, full lift law, advertised checking height and production timing remain unverified.
  - Open: Rigid linkage and constant-wire spring deformation explain motion; hydraulic lash adjustment, spring dynamics, lubrication, fatigue and running-engine performance are not simulated.
  - Open: Source-sized replacement envelopes are not installed-part identification. Absolute cam/deck/station datums, lifter socket/internal offsets and rocker geometry remain assumptions.
  - Open: Guide bore and separate spring load-test heights are service-reference constraints; spring wire/turns, keeper/groove construction and casting contours remain illustrative.
- [ ] **Exhaust Valve** — `exhaust-valve`; modeled quantity **6**; provisional.
  - Instances: `c1-exhaust-valve`, `c2-exhaust-valve`, `c3-exhaust-valve`, `c4-exhaust-valve`, `c5-exhaust-valve`, `c6-exhaust-valve`
  - Source IDs: fsm-ff8bb019d348, melling-camshaft-specifications, melling-stock-valve-specifications, melling-pushrod-specifications, melling-valve-progressive-size-chart-2025. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact production contours, dimensions and tolerances need applicable drawings or measurements.
  - Open: Coordinated motion is a teaching construction. The smooth lobe law fits selected Melling SYB-38 scalars; the installed cam, full lift law, advertised checking height and production timing remain unverified.
  - Open: Rigid linkage and constant-wire spring deformation explain motion; hydraulic lash adjustment, spring dynamics, lubrication, fatigue and running-engine performance are not simulated.
  - Open: Source-sized replacement envelopes are not installed-part identification. Absolute cam/deck/station datums, lifter socket/internal offsets and rocker geometry remain assumptions.
  - Open: Guide bore and separate spring load-test heights are service-reference constraints; spring wire/turns, keeper/groove construction and casting contours remain illustrative.
- [ ] **Intake valve spring** — `intake-spring`; modeled quantity **6**; provisional.
  - Instances: `c1-intake-spring`, `c2-intake-spring`, `c3-intake-spring`, `c4-intake-spring`, `c5-intake-spring`, `c6-intake-spring`
  - Source IDs: fsm-2e5473b2bf99. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact production contours, dimensions and tolerances need applicable drawings or measurements.
  - Open: Source-sized replacement envelopes are not installed-part identification. Absolute cam/deck/station datums, lifter socket/internal offsets and rocker geometry remain assumptions.
  - Open: Guide bore and separate spring load-test heights are service-reference constraints; spring wire/turns, keeper/groove construction and casting contours remain illustrative.
- [ ] **Exhaust valve spring** — `exhaust-spring`; modeled quantity **6**; provisional.
  - Instances: `c1-exhaust-spring`, `c2-exhaust-spring`, `c3-exhaust-spring`, `c4-exhaust-spring`, `c5-exhaust-spring`, `c6-exhaust-spring`
  - Source IDs: fsm-2e5473b2bf99. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact production contours, dimensions and tolerances need applicable drawings or measurements.
  - Open: Source-sized replacement envelopes are not installed-part identification. Absolute cam/deck/station datums, lifter socket/internal offsets and rocker geometry remain assumptions.
  - Open: Guide bore and separate spring load-test heights are service-reference constraints; spring wire/turns, keeper/groove construction and casting contours remain illustrative.

## Historical artifacts (not current installed inventory)

- `valve-spring` — Historical/superseded or demonstration artifact absent from current manifest; retain as history, not an additional verified truck part.
- `spring-seat` — Historical/superseded or demonstration artifact absent from current manifest; retain as history, not an additional verified truck part.

## Additional known scope and reconciliation

- [ ] Verify seats, keeper grooves and spring interfaces
- [ ] Source-supported envelopes and coordinated motion exist: verify installed variant and production profiles

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
