# Idle-air control valve and internals

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#44](https://github.com/0xZakk/truck/issues/44).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `f1dc26ba64eb0ba1e8fede4ef42e23a5ae3e288dbeae3cc4b2558cf4148a4a70`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

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
- [ ] **IAC armature and contact sleeve · study** — `iac-armature`; modeled quantity **1**; provisional.
  - Instances: `iac-armature`
  - Source IDs: system-1cf529afa81d, truck-throttle-operation, iac-attachment-factory-1994, iac-attachment-estimated-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory chapter illustrates both unvented and vent/filter IAC valves. This study uses the unvented architecture; the installed truck variant is not established.
  - Open: All dimensions, bypass routing, mounting pattern, valve travel and spring/magnetic details are provisional. The model does not simulate idle speed, duty cycle, vacuum or flow.
  - Open: Two diagonal mounting fasteners follow exact1994 factory topology; dimensions, threads, strength and installed valve identity remain unverified.
  - Open: The return spring, idealized annular ends and armature contact sleeve are educational construction choices, not verified production internals. No force, preload, rate, duty cycle or valve calibration is simulated.
  - Open: The existing end plug retains0.1mm radial clearance with unresolved retention/sealing construction; this study is not a leak-tight valve certification.
- [ ] **IAC mounting gasket · estimated** — `iac-gasket`; modeled quantity **1**; provisional.
  - Instances: `iac-gasket`
  - Source IDs: system-1cf529afa81d, truck-throttle-operation, iac-attachment-factory-1994, iac-attachment-estimated-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory chapter illustrates both unvented and vent/filter IAC valves. This study uses the unvented architecture; the installed truck variant is not established.
  - Open: All dimensions, bypass routing, mounting pattern, valve travel and spring/magnetic details are provisional. The model does not simulate idle speed, duty cycle, vacuum or flow.
  - Open: Two diagonal mounting fasteners follow exact1994 factory topology; dimensions, threads, strength and installed valve identity remain unverified.
  - Open: The return spring, idealized annular ends and armature contact sleeve are educational construction choices, not verified production internals. No force, preload, rate, duty cycle or valve calibration is simulated.
  - Open: The existing end plug retains0.1mm radial clearance with unresolved retention/sealing construction; this study is not a leak-tight valve certification.
- [ ] **IAC retaining screw · estimated** — `iac-mount-screw-estimated`; modeled quantity **2**; provisional.
  - Instances: `iac-mount-screw-1-estimated`, `iac-mount-screw-2-estimated`
  - Source IDs: iac-attachment-factory-1994, iac-attachment-estimated-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Two diagonal mounting fasteners follow exact1994 factory topology; dimensions, threads, strength and installed valve identity remain unverified.
  - Open: The return spring, idealized annular ends and armature contact sleeve are educational construction choices, not verified production internals. No force, preload, rate, duty cycle or valve calibration is simulated.
  - Open: The existing end plug retains0.1mm radial clearance with unresolved retention/sealing construction; this study is not a leak-tight valve certification.
- [ ] **IAC restoring spring · illustrative** — `iac-return-spring-estimated`; modeled quantity **1**; provisional.
  - Instances: `iac-return-spring-estimated`
  - Source IDs: iac-attachment-factory-1994, iac-attachment-estimated-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Two diagonal mounting fasteners follow exact1994 factory topology; dimensions, threads, strength and installed valve identity remain unverified.
  - Open: The return spring, idealized annular ends and armature contact sleeve are educational construction choices, not verified production internals. No force, preload, rate, duty cycle or valve calibration is simulated.
  - Open: The existing end plug retains0.1mm radial clearance with unresolved retention/sealing construction; this study is not a leak-tight valve certification.
- [ ] **IAC valve body · attachment study** — `iac-valve-body`; modeled quantity **1**; provisional.
  - Instances: `iac-valve-body`
  - Source IDs: system-1cf529afa81d, truck-throttle-operation, iac-attachment-factory-1994, iac-attachment-estimated-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory chapter illustrates both unvented and vent/filter IAC valves. This study uses the unvented architecture; the installed truck variant is not established.
  - Open: All dimensions, bypass routing, mounting pattern, valve travel and spring/magnetic details are provisional. The model does not simulate idle speed, duty cycle, vacuum or flow.
  - Open: Two diagonal mounting fasteners follow exact1994 factory topology; dimensions, threads, strength and installed valve identity remain unverified.
  - Open: The return spring, idealized annular ends and armature contact sleeve are educational construction choices, not verified production internals. No force, preload, rate, duty cycle or valve calibration is simulated.
  - Open: The existing end plug retains0.1mm radial clearance with unresolved retention/sealing construction; this study is not a leak-tight valve certification.

## Additional known scope and reconciliation

- [ ] Two modeled mounting screws and an illustrative restoring spring are installed; actual screw dimensions and restoring mechanism remain unverified
- [ ] End closure retention/sealing and electrical terminals remain unfinished; verify installed valve variant and internal passages

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
