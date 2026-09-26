# Idle-air control valve and internals

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#44](https://github.com/0xZakk/truck/issues/44).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `0656841ba587a3f05d193aa75fb711f320ddf732cc0343c68504836c9ea7537d`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **IAC solenoid casing** — `iac-solenoid-can`; modeled quantity **1**; provisional.
  - Instances: `iac-solenoid-can`
  - Source IDs: system-1cf529afa81d, truck-throttle-operation. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory chapter illustrates both unvented and vent/filter IAC valves. This study uses the unvented architecture; the installed truck variant is not established.
  - Open: All dimensions, bypass routing, mounting pattern, valve travel and spring/magnetic details are provisional. The model does not simulate idle speed, duty cycle, vacuum or flow.
- [ ] **IAC stem and reverse-seated pintle** — `iac-pintle`; modeled quantity **1**; provisional.
  - Instances: `iac-pintle`
  - Source IDs: system-1cf529afa81d, truck-throttle-operation. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory chapter illustrates both unvented and vent/filter IAC valves. This study uses the unvented architecture; the installed truck variant is not established.
  - Open: All dimensions, bypass routing, mounting pattern, valve travel and spring/magnetic details are provisional. The model does not simulate idle speed, duty cycle, vacuum or flow.
- [ ] **IAC armature and contact sleeve · study** — `iac-armature`; modeled quantity **1**; provisional.
  - Instances: `iac-armature`
  - Source IDs: system-1cf529afa81d, truck-throttle-operation, iac-attachment-factory-1994, iac-attachment-estimated-study, iac-closure-illustrative-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory chapter illustrates both unvented and vent/filter IAC valves. This study uses the unvented architecture; the installed truck variant is not established.
  - Open: All dimensions, bypass routing, mounting pattern, valve travel and spring/magnetic details are provisional. The model does not simulate idle speed, duty cycle, vacuum or flow.
  - Open: Two diagonal mounting fasteners follow exact1994 factory topology; dimensions, threads, strength and installed valve identity remain unverified.
  - Open: The return spring, idealized annular ends and armature contact sleeve are educational construction choices, not verified production internals. No force, preload, rate, duty cycle or valve calibration is simulated.
  - Open: The previous0.1mm end-plug geometric gap is superseded by an illustrative captured metal closure. Factory retention, material/fit, forming process, contact pressure and leak-rate performance remain unknown.
  - Open: The recessed plug flange and integral formed lip are educational choices; exact1994 images do not distinguish pressed, crimped/staked or threaded closure. No separate elastomer, production interference or service procedure is inferred.
- [ ] **IAC mounting gasket · estimated** — `iac-gasket`; modeled quantity **1**; provisional.
  - Instances: `iac-gasket`
  - Source IDs: system-1cf529afa81d, truck-throttle-operation, iac-attachment-factory-1994, iac-attachment-estimated-study, iac-closure-illustrative-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory chapter illustrates both unvented and vent/filter IAC valves. This study uses the unvented architecture; the installed truck variant is not established.
  - Open: All dimensions, bypass routing, mounting pattern, valve travel and spring/magnetic details are provisional. The model does not simulate idle speed, duty cycle, vacuum or flow.
  - Open: Two diagonal mounting fasteners follow exact1994 factory topology; dimensions, threads, strength and installed valve identity remain unverified.
  - Open: The return spring, idealized annular ends and armature contact sleeve are educational construction choices, not verified production internals. No force, preload, rate, duty cycle or valve calibration is simulated.
  - Open: The previous0.1mm end-plug geometric gap is superseded by an illustrative captured metal closure. Factory retention, material/fit, forming process, contact pressure and leak-rate performance remain unknown.
  - Open: The recessed plug flange and integral formed lip are educational choices; exact1994 images do not distinguish pressed, crimped/staked or threaded closure. No separate elastomer, production interference or service procedure is inferred.
- [ ] **IAC retaining screw · estimated** — `iac-mount-screw-estimated`; modeled quantity **2**; provisional.
  - Instances: `iac-mount-screw-1-estimated`, `iac-mount-screw-2-estimated`
  - Source IDs: iac-attachment-factory-1994, iac-attachment-estimated-study, iac-closure-illustrative-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Two diagonal mounting fasteners follow exact1994 factory topology; dimensions, threads, strength and installed valve identity remain unverified.
  - Open: The return spring, idealized annular ends and armature contact sleeve are educational construction choices, not verified production internals. No force, preload, rate, duty cycle or valve calibration is simulated.
  - Open: The previous0.1mm end-plug geometric gap is superseded by an illustrative captured metal closure. Factory retention, material/fit, forming process, contact pressure and leak-rate performance remain unknown.
  - Open: The recessed plug flange and integral formed lip are educational choices; exact1994 images do not distinguish pressed, crimped/staked or threaded closure. No separate elastomer, production interference or service procedure is inferred.
- [ ] **IAC restoring spring · illustrative** — `iac-return-spring-estimated`; modeled quantity **1**; provisional.
  - Instances: `iac-return-spring-estimated`
  - Source IDs: iac-attachment-factory-1994, iac-attachment-estimated-study, iac-closure-illustrative-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Two diagonal mounting fasteners follow exact1994 factory topology; dimensions, threads, strength and installed valve identity remain unverified.
  - Open: The return spring, idealized annular ends and armature contact sleeve are educational construction choices, not verified production internals. No force, preload, rate, duty cycle or valve calibration is simulated.
  - Open: The previous0.1mm end-plug geometric gap is superseded by an illustrative captured metal closure. Factory retention, material/fit, forming process, contact pressure and leak-rate performance remain unknown.
  - Open: The recessed plug flange and integral formed lip are educational choices; exact1994 images do not distinguish pressed, crimped/staked or threaded closure. No separate elastomer, production interference or service procedure is inferred.
- [ ] **IAC captured end plug · illustrative** — `iac-end-plug`; modeled quantity **1**; provisional.
  - Instances: `iac-end-plug`
  - Source IDs: system-1cf529afa81d, truck-throttle-operation, iac-closure-illustrative-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory chapter illustrates both unvented and vent/filter IAC valves. This study uses the unvented architecture; the installed truck variant is not established.
  - Open: All dimensions, bypass routing, mounting pattern, valve travel and spring/magnetic details are provisional. The model does not simulate idle speed, duty cycle, vacuum or flow.
  - Open: The previous0.1mm end-plug geometric gap is superseded by an illustrative captured metal closure. Factory retention, material/fit, forming process, contact pressure and leak-rate performance remain unknown.
  - Open: The recessed plug flange and integral formed lip are educational choices; exact1994 images do not distinguish pressed, crimped/staked or threaded closure. No separate elastomer, production interference or service procedure is inferred.
- [ ] **IAC valve body · attachment study** — `iac-valve-body`; modeled quantity **1**; provisional.
  - Instances: `iac-valve-body`
  - Source IDs: system-1cf529afa81d, truck-throttle-operation, iac-attachment-factory-1994, iac-attachment-estimated-study, iac-closure-illustrative-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory chapter illustrates both unvented and vent/filter IAC valves. This study uses the unvented architecture; the installed truck variant is not established.
  - Open: All dimensions, bypass routing, mounting pattern, valve travel and spring/magnetic details are provisional. The model does not simulate idle speed, duty cycle, vacuum or flow.
  - Open: Two diagonal mounting fasteners follow exact1994 factory topology; dimensions, threads, strength and installed valve identity remain unverified.
  - Open: The return spring, idealized annular ends and armature contact sleeve are educational construction choices, not verified production internals. No force, preload, rate, duty cycle or valve calibration is simulated.
  - Open: The previous0.1mm end-plug geometric gap is superseded by an illustrative captured metal closure. Factory retention, material/fit, forming process, contact pressure and leak-rate performance remain unknown.
  - Open: The recessed plug flange and integral formed lip are educational choices; exact1994 images do not distinguish pressed, crimped/staked or threaded closure. No separate elastomer, production interference or service procedure is inferred.
- [ ] **IAC winding envelope · illustrative** — `iac-coil`; modeled quantity **1**; provisional.
  - Instances: `iac-coil`
  - Source IDs: system-1cf529afa81d, truck-throttle-operation, iac-electrical-factory-topology-illustrative-construction. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory chapter illustrates both unvented and vent/filter IAC valves. This study uses the unvented architecture; the installed truck variant is not established.
  - Open: All dimensions, bypass routing, mounting pattern, valve travel and spring/magnetic details are provisional. The model does not simulate idle speed, duty cycle, vacuum or flow.
  - Open: Exact1994 diagrams support two IAC terminals and a suppression diode in parallel with the winding; no physical diode package or location is modeled.
  - Open: Connector dimensions, key and mounting clocking, carrier, terminal alloy/plating, embedded shoulders and tail terminations are illustrative. No production molded retention or joint method is identified.
  - Open: The coil is a winding envelope, not a homogeneous conductor, resolved turns or electrical resistance simulation. No wire-color-to-metal-material inference is made.
- [ ] **IAC coil insulator · illustrative** — `iac-coil-carrier-estimated`; modeled quantity **1**; provisional.
  - Instances: `iac-coil-carrier-estimated`
  - Source IDs: iac-electrical-factory-topology-illustrative-construction. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact1994 diagrams support two IAC terminals and a suppression diode in parallel with the winding; no physical diode package or location is modeled.
  - Open: Connector dimensions, key and mounting clocking, carrier, terminal alloy/plating, embedded shoulders and tail terminations are illustrative. No production molded retention or joint method is identified.
  - Open: The coil is a winding envelope, not a homogeneous conductor, resolved turns or electrical resistance simulation. No wire-color-to-metal-material inference is made.
- [ ] **IAC keyed connector cap · illustrative** — `iac-connector-cap`; modeled quantity **1**; provisional.
  - Instances: `iac-connector-cap`
  - Source IDs: system-1cf529afa81d, truck-throttle-operation, iac-electrical-factory-topology-illustrative-construction. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory chapter illustrates both unvented and vent/filter IAC valves. This study uses the unvented architecture; the installed truck variant is not established.
  - Open: All dimensions, bypass routing, mounting pattern, valve travel and spring/magnetic details are provisional. The model does not simulate idle speed, duty cycle, vacuum or flow.
  - Open: Exact1994 diagrams support two IAC terminals and a suppression diode in parallel with the winding; no physical diode package or location is modeled.
  - Open: Connector dimensions, key and mounting clocking, carrier, terminal alloy/plating, embedded shoulders and tail terminations are illustrative. No production molded retention or joint method is identified.
  - Open: The coil is a winding envelope, not a homogeneous conductor, resolved turns or electrical resistance simulation. No wire-color-to-metal-material inference is made.
- [ ] **IAC control terminal and tail · illustrative** — `iac-terminal-control-estimated`; modeled quantity **1**; provisional.
  - Instances: `iac-terminal-control-estimated`
  - Source IDs: iac-electrical-factory-topology-illustrative-construction. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact1994 diagrams support two IAC terminals and a suppression diode in parallel with the winding; no physical diode package or location is modeled.
  - Open: Connector dimensions, key and mounting clocking, carrier, terminal alloy/plating, embedded shoulders and tail terminations are illustrative. No production molded retention or joint method is identified.
  - Open: The coil is a winding envelope, not a homogeneous conductor, resolved turns or electrical resistance simulation. No wire-color-to-metal-material inference is made.
- [ ] **IAC VPWR terminal and tail · illustrative** — `iac-terminal-vpwr-estimated`; modeled quantity **1**; provisional.
  - Instances: `iac-terminal-vpwr-estimated`
  - Source IDs: iac-electrical-factory-topology-illustrative-construction. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact1994 diagrams support two IAC terminals and a suppression diode in parallel with the winding; no physical diode package or location is modeled.
  - Open: Connector dimensions, key and mounting clocking, carrier, terminal alloy/plating, embedded shoulders and tail terminations are illustrative. No production molded retention or joint method is identified.
  - Open: The coil is a winding envelope, not a homogeneous conductor, resolved turns or electrical resistance simulation. No wire-color-to-metal-material inference is made.

## Additional known scope and reconciliation

- [ ] Two modeled mounting screws and an illustrative restoring spring are installed; actual screw dimensions and restoring mechanism remain unverified
- [ ] End closure retention/sealing and electrical terminals remain unfinished; verify installed valve variant and internal passages

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
