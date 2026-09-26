# Oil pump, gerotor, relief valve and mounting

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#73](https://github.com/0xZakk/truck/issues/73).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `bfab1f2596991d27fe5e52e90f02d070eb034f9de8c2cd72d3dd44666d6c8bb9`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Oil pump housing** — `oil-pump-housing`; modeled quantity **1**; provisional.
  - Instances: `oil-pump-housing`
  - Source IDs: fsm-6f023139b5f8, fsm-59c6d1fb5ae3, fsm-76412d392bb7, fsm-3ceaca21ab73, ford-industrial-parts, ford-industrial-csg649, fsm-a3698a10af15, melling-intermediate-shaft-dimensions. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: All housing, rotor, shaft and hardware dimensions and installed transforms are provisional. The manual establishes component identities and inspection procedures, not these CAD dimensions.
  - Open: Four cover bolts and relief plunger/spring envelope dimensions follow the industrial book listing for the same C5AZ-6600-A service assembly. Truck applicability of internal revisions, ports, mounting geometry and relief-valve retention still needs verification.
  - Open: 20 degree lean, X227.584 station, gear-axis spacing, distributor lower extension, mounting bosses and pickup bends are constrained fit-study assumptions, not surveyed Ford geometry.
  - Open: Melling IS-74 length 114.808 mm and hex across flats 7.9248 mm remain unchanged. Ten mm upper and nine mm lower engagement are assumed.
  - Open: Cam-to-distributor crossed-helical tooth geometry, working backlash and angular phase remain unverified; this is a connected spatial study, not validated power transmission.
  - Open: Oil galleries and pump mounting architecture require a production reference. Proposed block cuts and supports must not be used as machining instructions.
- [ ] **Inner pump rotor** — `oil-pump-inner-rotor`; modeled quantity **1**; provisional.
  - Instances: `oil-pump-inner-rotor`
  - Source IDs: fsm-6f023139b5f8, fsm-59c6d1fb5ae3, fsm-76412d392bb7, fsm-3ceaca21ab73, ford-industrial-parts, ford-industrial-csg649, fsm-a3698a10af15, melling-intermediate-shaft-dimensions, gerotor-conjugate-profile-liu-2015. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: All housing, rotor, shaft and hardware dimensions and installed transforms are provisional. The manual establishes component identities and inspection procedures, not these CAD dimensions.
  - Open: Four cover bolts and relief plunger/spring envelope dimensions follow the industrial book listing for the same C5AZ-6600-A service assembly. Truck applicability of internal revisions, ports, mounting geometry and relief-valve retention still needs verification.
  - Open: 20 degree lean, X227.584 station, gear-axis spacing, distributor lower extension, mounting bosses and pickup bends are constrained fit-study assumptions, not surveyed Ford geometry.
  - Open: Melling IS-74 length 114.808 mm and hex across flats 7.9248 mm remain unchanged. Ten mm upper and nine mm lower engagement are assumed.
  - Open: Cam-to-distributor crossed-helical tooth geometry, working backlash and angular phase remain unverified; this is a connected spatial study, not validated power transmission.
  - Open: Oil galleries and pump mounting architecture require a production reference. Proposed block cuts and supports must not be used as machining instructions.
  - Open: The four/five tooth interpretation, all rotor dimensions, 3.5 mm eccentricity, D-flat coupling and running clearances remain provisional, not production measurements.
  - Open: The inner profile is the inward normal offset of the circular-cutter center trochoid; its periodic spline is a numerical approximation of the analytic conjugate envelope.
  - Open: Coordinated rigid-body kinematics do not simulate oil pressure, leakage, elastic tooth contact, friction or hydrodynamic lubrication.
- [ ] **Outer pump rotor** — `oil-pump-outer-rotor`; modeled quantity **1**; provisional.
  - Instances: `oil-pump-outer-rotor`
  - Source IDs: fsm-6f023139b5f8, fsm-59c6d1fb5ae3, fsm-76412d392bb7, fsm-3ceaca21ab73, ford-industrial-parts, ford-industrial-csg649, fsm-a3698a10af15, melling-intermediate-shaft-dimensions, gerotor-conjugate-profile-liu-2015. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: All housing, rotor, shaft and hardware dimensions and installed transforms are provisional. The manual establishes component identities and inspection procedures, not these CAD dimensions.
  - Open: Four cover bolts and relief plunger/spring envelope dimensions follow the industrial book listing for the same C5AZ-6600-A service assembly. Truck applicability of internal revisions, ports, mounting geometry and relief-valve retention still needs verification.
  - Open: 20 degree lean, X227.584 station, gear-axis spacing, distributor lower extension, mounting bosses and pickup bends are constrained fit-study assumptions, not surveyed Ford geometry.
  - Open: Melling IS-74 length 114.808 mm and hex across flats 7.9248 mm remain unchanged. Ten mm upper and nine mm lower engagement are assumed.
  - Open: Cam-to-distributor crossed-helical tooth geometry, working backlash and angular phase remain unverified; this is a connected spatial study, not validated power transmission.
  - Open: Oil galleries and pump mounting architecture require a production reference. Proposed block cuts and supports must not be used as machining instructions.
  - Open: The four/five tooth interpretation, all rotor dimensions, 3.5 mm eccentricity, D-flat coupling and running clearances remain provisional, not production measurements.
  - Open: The inner profile is the inward normal offset of the circular-cutter center trochoid; its periodic spline is a numerical approximation of the analytic conjugate envelope.
  - Open: Coordinated rigid-body kinematics do not simulate oil pressure, leakage, elastic tooth contact, friction or hydrodynamic lubrication.
- [ ] **Pump rotor shaft** — `oil-pump-rotor-shaft`; modeled quantity **1**; provisional.
  - Instances: `oil-pump-rotor-shaft`
  - Source IDs: fsm-6f023139b5f8, fsm-59c6d1fb5ae3, fsm-76412d392bb7, fsm-3ceaca21ab73, ford-industrial-parts, ford-industrial-csg649, fsm-a3698a10af15, melling-intermediate-shaft-dimensions, gerotor-conjugate-profile-liu-2015. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: All housing, rotor, shaft and hardware dimensions and installed transforms are provisional. The manual establishes component identities and inspection procedures, not these CAD dimensions.
  - Open: Four cover bolts and relief plunger/spring envelope dimensions follow the industrial book listing for the same C5AZ-6600-A service assembly. Truck applicability of internal revisions, ports, mounting geometry and relief-valve retention still needs verification.
  - Open: 20 degree lean, X227.584 station, gear-axis spacing, distributor lower extension, mounting bosses and pickup bends are constrained fit-study assumptions, not surveyed Ford geometry.
  - Open: Melling IS-74 length 114.808 mm and hex across flats 7.9248 mm remain unchanged. Ten mm upper and nine mm lower engagement are assumed.
  - Open: Cam-to-distributor crossed-helical tooth geometry, working backlash and angular phase remain unverified; this is a connected spatial study, not validated power transmission.
  - Open: Oil galleries and pump mounting architecture require a production reference. Proposed block cuts and supports must not be used as machining instructions.
  - Open: The four/five tooth interpretation, all rotor dimensions, 3.5 mm eccentricity, D-flat coupling and running clearances remain provisional, not production measurements.
  - Open: The inner profile is the inward normal offset of the circular-cutter center trochoid; its periodic spline is a numerical approximation of the analytic conjugate envelope.
  - Open: Coordinated rigid-body kinematics do not simulate oil pressure, leakage, elastic tooth contact, friction or hydrodynamic lubrication.
- [ ] **Oil pump cover** — `oil-pump-cover`; modeled quantity **1**; provisional.
  - Instances: `oil-pump-cover`
  - Source IDs: fsm-6f023139b5f8, fsm-59c6d1fb5ae3, fsm-76412d392bb7, fsm-3ceaca21ab73, ford-industrial-parts, ford-industrial-csg649, fsm-a3698a10af15, melling-intermediate-shaft-dimensions. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: All housing, rotor, shaft and hardware dimensions and installed transforms are provisional. The manual establishes component identities and inspection procedures, not these CAD dimensions.
  - Open: Four cover bolts and relief plunger/spring envelope dimensions follow the industrial book listing for the same C5AZ-6600-A service assembly. Truck applicability of internal revisions, ports, mounting geometry and relief-valve retention still needs verification.
  - Open: 20 degree lean, X227.584 station, gear-axis spacing, distributor lower extension, mounting bosses and pickup bends are constrained fit-study assumptions, not surveyed Ford geometry.
  - Open: Melling IS-74 length 114.808 mm and hex across flats 7.9248 mm remain unchanged. Ten mm upper and nine mm lower engagement are assumed.
  - Open: Cam-to-distributor crossed-helical tooth geometry, working backlash and angular phase remain unverified; this is a connected spatial study, not validated power transmission.
  - Open: Oil galleries and pump mounting architecture require a production reference. Proposed block cuts and supports must not be used as machining instructions.
- [ ] **Pump cover bolt** — `oil-pump-cover-bolt`; modeled quantity **4**; provisional.
  - Instances: `oil-pump-cover-bolt-1`, `oil-pump-cover-bolt-2`, `oil-pump-cover-bolt-3`, `oil-pump-cover-bolt-4`
  - Source IDs: fsm-6f023139b5f8, fsm-59c6d1fb5ae3, fsm-76412d392bb7, fsm-3ceaca21ab73, ford-industrial-parts, ford-industrial-csg649, fsm-a3698a10af15, melling-intermediate-shaft-dimensions. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: All housing, rotor, shaft and hardware dimensions and installed transforms are provisional. The manual establishes component identities and inspection procedures, not these CAD dimensions.
  - Open: Four cover bolts and relief plunger/spring envelope dimensions follow the industrial book listing for the same C5AZ-6600-A service assembly. Truck applicability of internal revisions, ports, mounting geometry and relief-valve retention still needs verification.
  - Open: 20 degree lean, X227.584 station, gear-axis spacing, distributor lower extension, mounting bosses and pickup bends are constrained fit-study assumptions, not surveyed Ford geometry.
  - Open: Melling IS-74 length 114.808 mm and hex across flats 7.9248 mm remain unchanged. Ten mm upper and nine mm lower engagement are assumed.
  - Open: Cam-to-distributor crossed-helical tooth geometry, working backlash and angular phase remain unverified; this is a connected spatial study, not validated power transmission.
  - Open: Oil galleries and pump mounting architecture require a production reference. Proposed block cuts and supports must not be used as machining instructions.
- [ ] **Pressure relief plunger** — `oil-pump-relief-plunger`; modeled quantity **1**; provisional.
  - Instances: `oil-pump-relief-plunger`
  - Source IDs: fsm-6f023139b5f8, fsm-59c6d1fb5ae3, fsm-76412d392bb7, fsm-3ceaca21ab73, ford-industrial-parts, ford-industrial-csg649, fsm-a3698a10af15, melling-intermediate-shaft-dimensions. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: All housing, rotor, shaft and hardware dimensions and installed transforms are provisional. The manual establishes component identities and inspection procedures, not these CAD dimensions.
  - Open: Four cover bolts and relief plunger/spring envelope dimensions follow the industrial book listing for the same C5AZ-6600-A service assembly. Truck applicability of internal revisions, ports, mounting geometry and relief-valve retention still needs verification.
  - Open: 20 degree lean, X227.584 station, gear-axis spacing, distributor lower extension, mounting bosses and pickup bends are constrained fit-study assumptions, not surveyed Ford geometry.
  - Open: Melling IS-74 length 114.808 mm and hex across flats 7.9248 mm remain unchanged. Ten mm upper and nine mm lower engagement are assumed.
  - Open: Cam-to-distributor crossed-helical tooth geometry, working backlash and angular phase remain unverified; this is a connected spatial study, not validated power transmission.
  - Open: Oil galleries and pump mounting architecture require a production reference. Proposed block cuts and supports must not be used as machining instructions.
- [ ] **Pressure relief spring** — `oil-pump-relief-spring`; modeled quantity **1**; provisional.
  - Instances: `oil-pump-relief-spring`
  - Source IDs: fsm-6f023139b5f8, fsm-59c6d1fb5ae3, fsm-76412d392bb7, fsm-3ceaca21ab73, ford-industrial-parts, ford-industrial-csg649, fsm-a3698a10af15, melling-intermediate-shaft-dimensions. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: All housing, rotor, shaft and hardware dimensions and installed transforms are provisional. The manual establishes component identities and inspection procedures, not these CAD dimensions.
  - Open: Four cover bolts and relief plunger/spring envelope dimensions follow the industrial book listing for the same C5AZ-6600-A service assembly. Truck applicability of internal revisions, ports, mounting geometry and relief-valve retention still needs verification.
  - Open: 20 degree lean, X227.584 station, gear-axis spacing, distributor lower extension, mounting bosses and pickup bends are constrained fit-study assumptions, not surveyed Ford geometry.
  - Open: Melling IS-74 length 114.808 mm and hex across flats 7.9248 mm remain unchanged. Ten mm upper and nine mm lower engagement are assumed.
  - Open: Cam-to-distributor crossed-helical tooth geometry, working backlash and angular phase remain unverified; this is a connected spatial study, not validated power transmission.
  - Open: Oil galleries and pump mounting architecture require a production reference. Proposed block cuts and supports must not be used as machining instructions.
- [ ] **Relief chamber closure** — `oil-pump-relief-cap`; modeled quantity **1**; provisional.
  - Instances: `oil-pump-relief-cap`
  - Source IDs: fsm-6f023139b5f8, fsm-59c6d1fb5ae3, fsm-76412d392bb7, fsm-3ceaca21ab73, ford-industrial-parts, ford-industrial-csg649, fsm-a3698a10af15, melling-intermediate-shaft-dimensions. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: All housing, rotor, shaft and hardware dimensions and installed transforms are provisional. The manual establishes component identities and inspection procedures, not these CAD dimensions.
  - Open: Four cover bolts and relief plunger/spring envelope dimensions follow the industrial book listing for the same C5AZ-6600-A service assembly. Truck applicability of internal revisions, ports, mounting geometry and relief-valve retention still needs verification.
  - Open: 20 degree lean, X227.584 station, gear-axis spacing, distributor lower extension, mounting bosses and pickup bends are constrained fit-study assumptions, not surveyed Ford geometry.
  - Open: Melling IS-74 length 114.808 mm and hex across flats 7.9248 mm remain unchanged. Ten mm upper and nine mm lower engagement are assumed.
  - Open: Cam-to-distributor crossed-helical tooth geometry, working backlash and angular phase remain unverified; this is a connected spatial study, not validated power transmission.
  - Open: Oil galleries and pump mounting architecture require a production reference. Proposed block cuts and supports must not be used as machining instructions.
- [ ] **Oil pump mounting bolt · provisional** — `oil-pump-mount-bolt`; modeled quantity **2**; provisional.
  - Instances: `oil-pump-mount-bolt-1`, `oil-pump-mount-bolt-2`
  - Source IDs: ford-industrial-csg649, fsm-a3698a10af15, melling-intermediate-shaft-dimensions. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: 20 degree lean, X227.584 station, gear-axis spacing, distributor lower extension, mounting bosses and pickup bends are constrained fit-study assumptions, not surveyed Ford geometry.
  - Open: Melling IS-74 length 114.808 mm and hex across flats 7.9248 mm remain unchanged. Ten mm upper and nine mm lower engagement are assumed.
  - Open: Cam-to-distributor crossed-helical tooth geometry, working backlash and angular phase remain unverified; this is a connected spatial study, not validated power transmission.
  - Open: Oil galleries and pump mounting architecture require a production reference. Proposed block cuts and supports must not be used as machining instructions.

## Additional known scope and reconciliation

- [ ] Verify actual rotor profile/count, clearances and pump-to-block outlet gallery
- [ ] Pressure relief operation and production mounting

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
