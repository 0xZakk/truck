# Idle-air control valve and internals

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#44](https://github.com/0xZakk/truck/issues/44).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `821f7d3bb47d49a00ffb2975fa5faffcd306fe90bea48ce7c0d6308cd636653f`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **IAC valve body** — `iac-valve-body`; modeled quantity **1**; provisional.
  - Instances: `iac-valve-body`
  - Source IDs: system-1cf529afa81d, truck-throttle-operation. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory chapter illustrates both unvented and vent/filter IAC valves. This study uses the unvented architecture; the installed truck variant is not established.
  - Open: All dimensions, bypass routing, mounting pattern, valve travel and spring/magnetic details are provisional. The model does not simulate idle speed, duty cycle, vacuum or flow.
- [ ] **IAC mounting gasket** — `iac-gasket`; modeled quantity **1**; provisional.
  - Instances: `iac-gasket`
  - Source IDs: system-1cf529afa81d, truck-throttle-operation. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory chapter illustrates both unvented and vent/filter IAC valves. This study uses the unvented architecture; the installed truck variant is not established.
  - Open: All dimensions, bypass routing, mounting pattern, valve travel and spring/magnetic details are provisional. The model does not simulate idle speed, duty cycle, vacuum or flow.
- [ ] **IAC chamber end closure** — `iac-end-plug`; modeled quantity **1**; provisional.
  - Instances: `iac-end-plug`
  - Source IDs: system-1cf529afa81d, truck-throttle-operation. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory chapter illustrates both unvented and vent/filter IAC valves. This study uses the unvented architecture; the installed truck variant is not established.
  - Open: All dimensions, bypass routing, mounting pattern, valve travel and spring/magnetic details are provisional. The model does not simulate idle speed, duty cycle, vacuum or flow.
- [ ] **IAC solenoid casing** — `iac-solenoid-can`; modeled quantity **1**; provisional.
  - Instances: `iac-solenoid-can`
  - Source IDs: system-1cf529afa81d, truck-throttle-operation. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory chapter illustrates both unvented and vent/filter IAC valves. This study uses the unvented architecture; the installed truck variant is not established.
  - Open: All dimensions, bypass routing, mounting pattern, valve travel and spring/magnetic details are provisional. The model does not simulate idle speed, duty cycle, vacuum or flow.
- [ ] **IAC solenoid coil** — `iac-coil`; modeled quantity **1**; provisional.
  - Instances: `iac-coil`
  - Source IDs: system-1cf529afa81d, truck-throttle-operation. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory chapter illustrates both unvented and vent/filter IAC valves. This study uses the unvented architecture; the installed truck variant is not established.
  - Open: All dimensions, bypass routing, mounting pattern, valve travel and spring/magnetic details are provisional. The model does not simulate idle speed, duty cycle, vacuum or flow.
- [ ] **IAC armature** — `iac-armature`; modeled quantity **1**; provisional.
  - Instances: `iac-armature`
  - Source IDs: system-1cf529afa81d, truck-throttle-operation. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory chapter illustrates both unvented and vent/filter IAC valves. This study uses the unvented architecture; the installed truck variant is not established.
  - Open: All dimensions, bypass routing, mounting pattern, valve travel and spring/magnetic details are provisional. The model does not simulate idle speed, duty cycle, vacuum or flow.
- [ ] **IAC stem and reverse-seated pintle** — `iac-pintle`; modeled quantity **1**; provisional.
  - Instances: `iac-pintle`
  - Source IDs: system-1cf529afa81d, truck-throttle-operation. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory chapter illustrates both unvented and vent/filter IAC valves. This study uses the unvented architecture; the installed truck variant is not established.
  - Open: All dimensions, bypass routing, mounting pattern, valve travel and spring/magnetic details are provisional. The model does not simulate idle speed, duty cycle, vacuum or flow.
- [ ] **IAC electrical connector cap** — `iac-connector-cap`; modeled quantity **1**; provisional.
  - Instances: `iac-connector-cap`
  - Source IDs: system-1cf529afa81d, truck-throttle-operation. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory chapter illustrates both unvented and vent/filter IAC valves. This study uses the unvented architecture; the installed truck variant is not established.
  - Open: All dimensions, bypass routing, mounting pattern, valve travel and spring/magnetic details are provisional. The model does not simulate idle speed, duty cycle, vacuum or flow.

## Additional known scope and reconciliation

- [ ] Mounting bolts and terminals: verify complete inventory
- [ ] Verify restoring mechanism, installed valve identity and internal passages

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
