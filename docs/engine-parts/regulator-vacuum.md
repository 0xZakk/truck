# Fuel regulator vacuum hose and fitting

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#41](https://github.com/0xZakk/truck/issues/41).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `821f7d3bb47d49a00ffb2975fa5faffcd306fe90bea48ce7c0d6308cd636653f`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Fuel regulator vacuum hose** — `regulator-vacuum-hose`; modeled quantity **1**; provisional.
  - Instances: `regulator-vacuum-hose`
  - Source IDs: system-750bd1047639, system-73d3dd2d32e7. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Ford establishes an intake-manifold vacuum connection to the regulator spring chamber. It does not dimension the hose or identify this modeled dedicated fitting.
  - Open: Hose routing, 12 mm outside diameter, 8.2 mm main bore, 8.3 mm straight regulator socket, fitting dimensions and plenum port station are provisional; production routing may use a shared vacuum harness.
  - Open: The fitting uses an unthreaded seat with clearance; thread sealing, hose compression, clamps and actual installed variant remain unresolved. No pressure response is simulated.
- [ ] **Regulator manifold vacuum fitting · provisional** — `regulator-vacuum-fitting`; modeled quantity **1**; provisional.
  - Instances: `regulator-vacuum-fitting`
  - Source IDs: system-750bd1047639, system-73d3dd2d32e7. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Ford establishes an intake-manifold vacuum connection to the regulator spring chamber. It does not dimension the hose or identify this modeled dedicated fitting.
  - Open: Hose routing, 12 mm outside diameter, 8.2 mm main bore, 8.3 mm straight regulator socket, fitting dimensions and plenum port station are provisional; production routing may use a shared vacuum harness.
  - Open: The fitting uses an unthreaded seat with clearance; thread sealing, hose compression, clamps and actual installed variant remain unresolved. No pressure response is simulated.

## Additional known scope and reconciliation

- [ ] Verify hose routing, end connections and manifold vacuum passage

## Cross-system boundaries

Coordinate with [#7](https://github.com/0xZakk/truck/issues/7). Keep the current engine-mounted component here; agree ownership before adding its vehicle-side continuation.

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
