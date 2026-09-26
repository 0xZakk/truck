# Oil pickup, strainer and support

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#74](https://github.com/0xZakk/truck/issues/74).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `4f98bbdad7fb1996487d17c4a651de588cef39254efe24e96384375dbdce0c07`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Oil pickup tube** — `oil-pickup-tube`; modeled quantity **1**; provisional.
  - Instances: `oil-pickup-tube`
  - Source IDs: fsm-00314a45e241, fsm-6f023139b5f8, ford-industrial-csg649, fsm-a3698a10af15, melling-intermediate-shaft-dimensions. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: All housing, rotor, shaft and hardware dimensions and installed transforms are provisional. The manual establishes component identities and inspection procedures, not these CAD dimensions.
  - Open: Four cover bolts and relief plunger/spring envelope dimensions follow the industrial book listing for the same C5AZ-6600-A service assembly. Truck applicability of internal revisions, ports, mounting geometry and relief-valve retention still needs verification.
  - Open: 20 degree lean, X227.584 station, gear-axis spacing, distributor lower extension, mounting bosses and pickup bends are constrained fit-study assumptions, not surveyed Ford geometry.
  - Open: Melling IS-74 length 114.808 mm and hex across flats 7.9248 mm remain unchanged. Ten mm upper and nine mm lower engagement are assumed.
  - Open: Cam-to-distributor crossed-helical tooth geometry, working backlash and angular phase remain unverified; this is a connected spatial study, not validated power transmission.
  - Open: Oil galleries and pump mounting architecture require a production reference. Proposed block cuts and supports must not be used as machining instructions.
- [ ] **Pickup strainer shell** — `oil-pickup-bell`; modeled quantity **1**; provisional.
  - Instances: `oil-pickup-bell`
  - Source IDs: fsm-00314a45e241, fsm-6f023139b5f8, ford-industrial-csg649, fsm-a3698a10af15, melling-intermediate-shaft-dimensions. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: All housing, rotor, shaft and hardware dimensions and installed transforms are provisional. The manual establishes component identities and inspection procedures, not these CAD dimensions.
  - Open: Four cover bolts and relief plunger/spring envelope dimensions follow the industrial book listing for the same C5AZ-6600-A service assembly. Truck applicability of internal revisions, ports, mounting geometry and relief-valve retention still needs verification.
  - Open: 20 degree lean, X227.584 station, gear-axis spacing, distributor lower extension, mounting bosses and pickup bends are constrained fit-study assumptions, not surveyed Ford geometry.
  - Open: Melling IS-74 length 114.808 mm and hex across flats 7.9248 mm remain unchanged. Ten mm upper and nine mm lower engagement are assumed.
  - Open: Cam-to-distributor crossed-helical tooth geometry, working backlash and angular phase remain unverified; this is a connected spatial study, not validated power transmission.
  - Open: Oil galleries and pump mounting architecture require a production reference. Proposed block cuts and supports must not be used as machining instructions.
- [ ] **Pickup inlet screen** — `oil-pickup-screen`; modeled quantity **1**; provisional.
  - Instances: `oil-pickup-screen`
  - Source IDs: fsm-00314a45e241, fsm-6f023139b5f8, ford-industrial-csg649, fsm-a3698a10af15, melling-intermediate-shaft-dimensions. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: All housing, rotor, shaft and hardware dimensions and installed transforms are provisional. The manual establishes component identities and inspection procedures, not these CAD dimensions.
  - Open: Four cover bolts and relief plunger/spring envelope dimensions follow the industrial book listing for the same C5AZ-6600-A service assembly. Truck applicability of internal revisions, ports, mounting geometry and relief-valve retention still needs verification.
  - Open: 20 degree lean, X227.584 station, gear-axis spacing, distributor lower extension, mounting bosses and pickup bends are constrained fit-study assumptions, not surveyed Ford geometry.
  - Open: Melling IS-74 length 114.808 mm and hex across flats 7.9248 mm remain unchanged. Ten mm upper and nine mm lower engagement are assumed.
  - Open: Cam-to-distributor crossed-helical tooth geometry, working backlash and angular phase remain unverified; this is a connected spatial study, not validated power transmission.
  - Open: Oil galleries and pump mounting architecture require a production reference. Proposed block cuts and supports must not be used as machining instructions.

## Additional known scope and reconciliation

- [ ] Pickup support bracket and fasteners
- [ ] Verify tube route, inlet clearance and seals

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
