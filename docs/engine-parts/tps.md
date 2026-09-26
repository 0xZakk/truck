# Throttle-position sensor and internals

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#45](https://github.com/0xZakk/truck/issues/45).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `f1dc26ba64eb0ba1e8fede4ef42e23a5ae3e288dbeae3cc4b2558cf4148a4a70`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **TPS housing** — `tps-housing`; modeled quantity **1**; provisional.
  - Instances: `tps-housing`
  - Source IDs: system-5691d2ae0a6c, system-f6b16c0f51f5. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Factory text establishes a curved resistor, moving wiper, direct shaft coupling and two mounting screws. Internal packaging, track sweep, dimensions, connector and installed orientation are illustrative.
  - Open: No voltage calibration or electrical fault simulation is inferred from the throttle slider. Production preload and stop angles are unresolved.
- [ ] **TPS cover** — `tps-cover`; modeled quantity **1**; provisional.
  - Instances: `tps-cover`
  - Source IDs: system-5691d2ae0a6c, system-f6b16c0f51f5. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Factory text establishes a curved resistor, moving wiper, direct shaft coupling and two mounting screws. Internal packaging, track sweep, dimensions, connector and installed orientation are illustrative.
  - Open: No voltage calibration or electrical fault simulation is inferred from the throttle slider. Production preload and stop angles are unresolved.
- [ ] **TPS shaft coupling rotor** — `tps-rotor`; modeled quantity **1**; provisional.
  - Instances: `tps-rotor`
  - Source IDs: system-5691d2ae0a6c, system-f6b16c0f51f5. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Factory text establishes a curved resistor, moving wiper, direct shaft coupling and two mounting screws. Internal packaging, track sweep, dimensions, connector and installed orientation are illustrative.
  - Open: No voltage calibration or electrical fault simulation is inferred from the throttle slider. Production preload and stop angles are unresolved.
- [ ] **TPS resistance track** — `tps-resistance-track`; modeled quantity **1**; provisional.
  - Instances: `tps-resistance-track`
  - Source IDs: system-5691d2ae0a6c, system-f6b16c0f51f5. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Factory text establishes a curved resistor, moving wiper, direct shaft coupling and two mounting screws. Internal packaging, track sweep, dimensions, connector and installed orientation are illustrative.
  - Open: No voltage calibration or electrical fault simulation is inferred from the throttle slider. Production preload and stop angles are unresolved.
- [ ] **TPS moving wiper** — `tps-wiper`; modeled quantity **1**; provisional.
  - Instances: `tps-wiper`
  - Source IDs: system-5691d2ae0a6c, system-f6b16c0f51f5. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Factory text establishes a curved resistor, moving wiper, direct shaft coupling and two mounting screws. Internal packaging, track sweep, dimensions, connector and installed orientation are illustrative.
  - Open: No voltage calibration or electrical fault simulation is inferred from the throttle slider. Production preload and stop angles are unresolved.
- [ ] **TPS retaining screw** — `tps-screw`; modeled quantity **2**; provisional.
  - Instances: `tps-screw-1`, `tps-screw-2`
  - Source IDs: system-5691d2ae0a6c, system-f6b16c0f51f5. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Factory text establishes a curved resistor, moving wiper, direct shaft coupling and two mounting screws. Internal packaging, track sweep, dimensions, connector and installed orientation are illustrative.
  - Open: No voltage calibration or electrical fault simulation is inferred from the throttle slider. Production preload and stop angles are unresolved.

## Additional known scope and reconciliation

- [ ] Connector contacts/seals and calibration
- [ ] Verify coupling, track and wiper construction

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
