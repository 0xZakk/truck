# Remote ignition module, heat sink and connector

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#53](https://github.com/0xZakk/truck/issues/53).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `f1dc26ba64eb0ba1e8fede4ef42e23a5ae3e288dbeae3cc4b2558cf4148a4a70`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Ignition module heat sink** — `ignition-heat-sink`; modeled quantity **1**; provisional.
  - Instances: `ignition-heat-sink`
  - Source IDs: system-0538e7de7e9d, system-75dcdb21ac74, system-6d43f4508d79. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Factory illustration establishes a fender-mounted module/heat-sink assembly, two module screws and two assembly screws, not these dimensions.
  - Open: All mounting coordinates, fin spacing/count, casting profile, screw dimensions and connector outline are provisional. The fender and harness are not yet modeled.
  - Open: Module is an unresolved electronic package, not a complete internal reconstruction. Installed push-start/CCD identity and pinout remain unverified. Neutral display color does not identify its calibration.
- [ ] **Ignition control module · unresolved package** — `ignition-module-package`; modeled quantity **1**; provisional.
  - Instances: `ignition-module-package`
  - Source IDs: system-0538e7de7e9d, system-75dcdb21ac74, system-6d43f4508d79. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Factory illustration establishes a fender-mounted module/heat-sink assembly, two module screws and two assembly screws, not these dimensions.
  - Open: All mounting coordinates, fin spacing/count, casting profile, screw dimensions and connector outline are provisional. The fender and harness are not yet modeled.
  - Open: Module is an unresolved electronic package, not a complete internal reconstruction. Installed push-start/CCD identity and pinout remain unverified. Neutral display color does not identify its calibration.
- [ ] **Ignition module connector shell** — `ignition-module-connector`; modeled quantity **1**; provisional.
  - Instances: `ignition-module-connector`
  - Source IDs: system-0538e7de7e9d, system-75dcdb21ac74, system-6d43f4508d79. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Factory illustration establishes a fender-mounted module/heat-sink assembly, two module screws and two assembly screws, not these dimensions.
  - Open: All mounting coordinates, fin spacing/count, casting profile, screw dimensions and connector outline are provisional. The fender and harness are not yet modeled.
  - Open: Module is an unresolved electronic package, not a complete internal reconstruction. Installed push-start/CCD identity and pinout remain unverified. Neutral display color does not identify its calibration.
- [ ] **Module retaining screw** — `ignition-module-screw`; modeled quantity **2**; provisional.
  - Instances: `ignition-module-screw-1`, `ignition-module-screw-2`
  - Source IDs: system-0538e7de7e9d, system-75dcdb21ac74, system-6d43f4508d79. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Factory illustration establishes a fender-mounted module/heat-sink assembly, two module screws and two assembly screws, not these dimensions.
  - Open: All mounting coordinates, fin spacing/count, casting profile, screw dimensions and connector outline are provisional. The fender and harness are not yet modeled.
  - Open: Module is an unresolved electronic package, not a complete internal reconstruction. Installed push-start/CCD identity and pinout remain unverified. Neutral display color does not identify its calibration.
- [ ] **Heat-sink assembly retaining screw** — `ignition-heat-sink-screw`; modeled quantity **2**; provisional.
  - Instances: `ignition-heat-sink-screw-1`, `ignition-heat-sink-screw-2`
  - Source IDs: system-0538e7de7e9d, system-75dcdb21ac74, system-6d43f4508d79. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Factory illustration establishes a fender-mounted module/heat-sink assembly, two module screws and two assembly screws, not these dimensions.
  - Open: All mounting coordinates, fin spacing/count, casting profile, screw dimensions and connector outline are provisional. The fender and harness are not yet modeled.
  - Open: Module is an unresolved electronic package, not a complete internal reconstruction. Installed push-start/CCD identity and pinout remain unverified. Neutral display color does not identify its calibration.

## Additional known scope and reconciliation

- [ ] Verify installed module variant and circuit detail appropriate to scope
- [ ] Harness contacts, fender mounting and thermal interface

## Cross-system boundaries

Coordinate with [#11](https://github.com/0xZakk/truck/issues/11). Keep the current engine-mounted component here; agree ownership before adding its vehicle-side continuation.

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
