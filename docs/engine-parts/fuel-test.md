# Fuel pressure test valve and cap

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#38](https://github.com/0xZakk/truck/issues/38).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `821f7d3bb47d49a00ffb2975fa5faffcd306fe90bea48ce7c0d6308cd636653f`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Pressure-test fitting body** — `fuel-test-body`; modeled quantity **1**; provisional.
  - Instances: `fuel-test-body`
  - Source IDs: fsm-4840fb38c793, schrader-core-construction. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Ford establishes a fuel-rail Schrader fitting. Exact installed fitting/core identity, dimensions, thread forms and location are unverified.
  - Open: Internal construction is a generic spring-actuated valve study, not a production Ford section. No pressure rating, leakage, material compatibility or spring calibration is established.
- [ ] **Pressure-test valve core housing** — `fuel-test-core`; modeled quantity **1**; provisional.
  - Instances: `fuel-test-core`
  - Source IDs: fsm-4840fb38c793, schrader-core-construction. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Ford establishes a fuel-rail Schrader fitting. Exact installed fitting/core identity, dimensions, thread forms and location are unverified.
  - Open: Internal construction is a generic spring-actuated valve study, not a production Ford section. No pressure rating, leakage, material compatibility or spring calibration is established.
- [ ] **Valve-core static seal** — `fuel-test-static-seal`; modeled quantity **1**; provisional.
  - Instances: `fuel-test-static-seal`
  - Source IDs: fsm-4840fb38c793, schrader-core-construction. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Ford establishes a fuel-rail Schrader fitting. Exact installed fitting/core identity, dimensions, thread forms and location are unverified.
  - Open: Internal construction is a generic spring-actuated valve study, not a production Ford section. No pressure rating, leakage, material compatibility or spring calibration is established.
- [ ] **Valve-core actuating pin and poppet** — `fuel-test-pin`; modeled quantity **1**; provisional.
  - Instances: `fuel-test-pin`
  - Source IDs: fsm-4840fb38c793, schrader-core-construction. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Ford establishes a fuel-rail Schrader fitting. Exact installed fitting/core identity, dimensions, thread forms and location are unverified.
  - Open: Internal construction is a generic spring-actuated valve study, not a production Ford section. No pressure rating, leakage, material compatibility or spring calibration is established.
- [ ] **Valve-core seating washer** — `fuel-test-seat-seal`; modeled quantity **1**; provisional.
  - Instances: `fuel-test-seat-seal`
  - Source IDs: fsm-4840fb38c793, schrader-core-construction. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Ford establishes a fuel-rail Schrader fitting. Exact installed fitting/core identity, dimensions, thread forms and location are unverified.
  - Open: Internal construction is a generic spring-actuated valve study, not a production Ford section. No pressure rating, leakage, material compatibility or spring calibration is established.
- [ ] **Valve-core return spring** — `fuel-test-spring`; modeled quantity **1**; provisional.
  - Instances: `fuel-test-spring`
  - Source IDs: fsm-4840fb38c793, schrader-core-construction. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Ford establishes a fuel-rail Schrader fitting. Exact installed fitting/core identity, dimensions, thread forms and location are unverified.
  - Open: Internal construction is a generic spring-actuated valve study, not a production Ford section. No pressure rating, leakage, material compatibility or spring calibration is established.
- [ ] **Fuel pressure test-port cap** — `fuel-test-cap`; modeled quantity **1**; provisional.
  - Instances: `fuel-test-cap`
  - Source IDs: fsm-4840fb38c793, schrader-core-construction. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Ford establishes a fuel-rail Schrader fitting. Exact installed fitting/core identity, dimensions, thread forms and location are unverified.
  - Open: Internal construction is a generic spring-actuated valve study, not a production Ford section. No pressure rating, leakage, material compatibility or spring calibration is established.
- [ ] **Pressure test-port cap seal** — `fuel-test-cap-seal`; modeled quantity **1**; provisional.
  - Instances: `fuel-test-cap-seal`
  - Source IDs: fsm-4840fb38c793, schrader-core-construction. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Ford establishes a fuel-rail Schrader fitting. Exact installed fitting/core identity, dimensions, thread forms and location are unverified.
  - Open: Internal construction is a generic spring-actuated valve study, not a production Ford section. No pressure rating, leakage, material compatibility or spring calibration is established.

## Additional known scope and reconciliation

- [ ] Verify core identity, sealing and actuation

## Cross-system boundaries

Coordinate with [#7](https://github.com/0xZakk/truck/issues/7). Keep the current engine-mounted component here; agree ownership before adding its vehicle-side continuation.

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
