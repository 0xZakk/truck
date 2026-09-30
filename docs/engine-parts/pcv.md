# PCV valve, grommet and crankcase ventilation

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#55](https://github.com/0xZakk/truck/issues/55).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **PCV metal valve body** — `pcv-body`; modeled quantity **1**; provisional.
  - Instances: `pcv-body`
  - Source IDs: truck-pcv-valve-operation, truck-pcv-service, truck-pcv-parts, standard-v219-pcv. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory diagram is a typical mechanism, and the exterior follows a Standard V219 replacement photograph. Installed identity, external dimensions and internal calibration remain unverified.
  - Open: All model dimensions and clocking are provisional. The catalog inlet-diameter field is not assigned to a geometric feature without a dimensioned drawing. Hose routing, unused-outlet closure and valve-cover baffle remain unresolved. No airflow, spring-rate or backfire simulation is claimed.
- [ ] **PCV angled outlet head** — `pcv-outlet-head`; modeled quantity **1**; provisional.
  - Instances: `pcv-outlet-head`
  - Source IDs: truck-pcv-valve-operation, truck-pcv-service, truck-pcv-parts, standard-v219-pcv. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory diagram is a typical mechanism, and the exterior follows a Standard V219 replacement photograph. Installed identity, external dimensions and internal calibration remain unverified.
  - Open: All model dimensions and clocking are provisional. The catalog inlet-diameter field is not assigned to a geometric feature without a dimensioned drawing. Hose routing, unused-outlet closure and valve-cover baffle remain unresolved. No airflow, spring-rate or backfire simulation is claimed.
- [ ] **PCV metering plunger** — `pcv-plunger`; modeled quantity **1**; provisional.
  - Instances: `pcv-plunger`
  - Source IDs: truck-pcv-valve-operation, truck-pcv-service, truck-pcv-parts, standard-v219-pcv. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory diagram is a typical mechanism, and the exterior follows a Standard V219 replacement photograph. Installed identity, external dimensions and internal calibration remain unverified.
  - Open: All model dimensions and clocking are provisional. The catalog inlet-diameter field is not assigned to a geometric feature without a dimensioned drawing. Hose routing, unused-outlet closure and valve-cover baffle remain unresolved. No airflow, spring-rate or backfire simulation is claimed.
- [ ] **PCV orifice washer** — `pcv-orifice-washer`; modeled quantity **1**; provisional.
  - Instances: `pcv-orifice-washer`
  - Source IDs: truck-pcv-valve-operation, truck-pcv-service, truck-pcv-parts, standard-v219-pcv. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory diagram is a typical mechanism, and the exterior follows a Standard V219 replacement photograph. Installed identity, external dimensions and internal calibration remain unverified.
  - Open: All model dimensions and clocking are provisional. The catalog inlet-diameter field is not assigned to a geometric feature without a dimensioned drawing. Hose routing, unused-outlet closure and valve-cover baffle remain unresolved. No airflow, spring-rate or backfire simulation is claimed.
- [ ] **PCV metering spring** — `pcv-spring`; modeled quantity **1**; provisional.
  - Instances: `pcv-spring`
  - Source IDs: truck-pcv-valve-operation, truck-pcv-service, truck-pcv-parts, standard-v219-pcv. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory diagram is a typical mechanism, and the exterior follows a Standard V219 replacement photograph. Installed identity, external dimensions and internal calibration remain unverified.
  - Open: All model dimensions and clocking are provisional. The catalog inlet-diameter field is not assigned to a geometric feature without a dimensioned drawing. Hose routing, unused-outlet closure and valve-cover baffle remain unresolved. No airflow, spring-rate or backfire simulation is claimed.
- [ ] **PCV mounting grommet** — `pcv-grommet`; modeled quantity **1**; provisional.
  - Instances: `pcv-grommet`
  - Source IDs: truck-pcv-valve-operation, truck-pcv-service, truck-pcv-parts, standard-v219-pcv. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory diagram is a typical mechanism, and the exterior follows a Standard V219 replacement photograph. Installed identity, external dimensions and internal calibration remain unverified.
  - Open: All model dimensions and clocking are provisional. The catalog inlet-diameter field is not assigned to a geometric feature without a dimensioned drawing. Hose routing, unused-outlet closure and valve-cover baffle remain unresolved. No airflow, spring-rate or backfire simulation is claimed.

## Additional known scope and reconciliation

- [ ] PCV hose and intake connector
- [ ] Fresh-air breather hose, fittings and clips
- [ ] Cover baffle and unused outlet closure if applicable
- [ ] Verify valve identity, flow behavior and plumbing

## Cross-system boundaries

Coordinate with [#7](https://github.com/0xZakk/truck/issues/7). Keep the current engine-mounted component here; agree ownership before adding its vehicle-side continuation.

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
