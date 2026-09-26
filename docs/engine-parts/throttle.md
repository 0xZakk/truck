# Throttle body, shaft, plates and mounting hardware

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#43](https://github.com/0xZakk/truck/issues/43).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `821f7d3bb47d49a00ffb2975fa5faffcd306fe90bea48ce7c0d6308cd636653f`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Twin-bore throttle housing** — `throttle-housing`; modeled quantity **1**; provisional.
  - Instances: `throttle-housing`
  - Source IDs: truck-throttle-operation, truck-throttle-service, truck-throttle-catalog. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory manual supports dual bores, a separate gasket and four mounting studs/nuts. Bore diameter, shaft/plate construction, casting contour and fastener dimensions are assumed.
  - Open: IAC/TPS studies and bypass passages are present; their exact variants and internal details remain unresolved. Purge ports, linkage, return spring, accelerator bracket and plate screws remain unmodeled. Idealized 0–90 degree motion is not the production stop calibration.
- [ ] **Throttle body gasket** — `throttle-gasket`; modeled quantity **1**; provisional.
  - Instances: `throttle-gasket`
  - Source IDs: truck-throttle-operation, truck-throttle-service, truck-throttle-catalog. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory manual supports dual bores, a separate gasket and four mounting studs/nuts. Bore diameter, shaft/plate construction, casting contour and fastener dimensions are assumed.
  - Open: IAC/TPS studies and bypass passages are present; their exact variants and internal details remain unresolved. Purge ports, linkage, return spring, accelerator bracket and plate screws remain unmodeled. Idealized 0–90 degree motion is not the production stop calibration.
- [ ] **Throttle shaft** — `throttle-shaft`; modeled quantity **1**; provisional.
  - Instances: `throttle-shaft`
  - Source IDs: truck-throttle-operation, truck-throttle-service, truck-throttle-catalog. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory manual supports dual bores, a separate gasket and four mounting studs/nuts. Bore diameter, shaft/plate construction, casting contour and fastener dimensions are assumed.
  - Open: IAC/TPS studies and bypass passages are present; their exact variants and internal details remain unresolved. Purge ports, linkage, return spring, accelerator bracket and plate screws remain unmodeled. Idealized 0–90 degree motion is not the production stop calibration.
- [ ] **Throttle butterfly plate** — `throttle-plate`; modeled quantity **2**; provisional.
  - Instances: `throttle-plate-1`, `throttle-plate-2`
  - Source IDs: truck-throttle-operation, truck-throttle-service, truck-throttle-catalog. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory manual supports dual bores, a separate gasket and four mounting studs/nuts. Bore diameter, shaft/plate construction, casting contour and fastener dimensions are assumed.
  - Open: IAC/TPS studies and bypass passages are present; their exact variants and internal details remain unresolved. Purge ports, linkage, return spring, accelerator bracket and plate screws remain unmodeled. Idealized 0–90 degree motion is not the production stop calibration.
- [ ] **Throttle mounting stud** — `throttle-mount-stud`; modeled quantity **4**; provisional.
  - Instances: `throttle-stud-1`, `throttle-stud-2`, `throttle-stud-3`, `throttle-stud-4`
  - Source IDs: truck-throttle-operation, truck-throttle-service, truck-throttle-catalog. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory manual supports dual bores, a separate gasket and four mounting studs/nuts. Bore diameter, shaft/plate construction, casting contour and fastener dimensions are assumed.
  - Open: IAC/TPS studies and bypass passages are present; their exact variants and internal details remain unresolved. Purge ports, linkage, return spring, accelerator bracket and plate screws remain unmodeled. Idealized 0–90 degree motion is not the production stop calibration.
- [ ] **Throttle retaining nut** — `throttle-mount-nut`; modeled quantity **4**; provisional.
  - Instances: `throttle-nut-1`, `throttle-nut-2`, `throttle-nut-3`, `throttle-nut-4`
  - Source IDs: truck-throttle-operation, truck-throttle-service, truck-throttle-catalog. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory manual supports dual bores, a separate gasket and four mounting studs/nuts. Bore diameter, shaft/plate construction, casting contour and fastener dimensions are assumed.
  - Open: IAC/TPS studies and bypass passages are present; their exact variants and internal details remain unresolved. Purge ports, linkage, return spring, accelerator bracket and plate screws remain unmodeled. Idealized 0–90 degree motion is not the production stop calibration.

## Additional known scope and reconciliation

- [ ] Throttle lever/cam and return spring
- [ ] Plate retaining screws and shaft bushings/seals as applicable
- [ ] Speed-control cable attachment and linkage shield if fitted
- [ ] Verify stops, return action and installed geometry

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
