# Oil-pump intermediate shaft and retainer

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#72](https://github.com/0xZakk/truck/issues/72).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `4f98bbdad7fb1996487d17c4a651de588cef39254efe24e96384375dbdce0c07`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Oil pump intermediate shaft · IS-74 study** — `oil-pump-intermediate-shaft`; modeled quantity **1**; provisional.
  - Instances: `oil-pump-intermediate-shaft`
  - Source IDs: ford-industrial-csg649, fsm-a3698a10af15, melling-intermediate-shaft-dimensions. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: 20 degree lean, X227.584 station, gear-axis spacing, distributor lower extension, mounting bosses and pickup bends are constrained fit-study assumptions, not surveyed Ford geometry.
  - Open: Melling IS-74 length 114.808 mm and hex across flats 7.9248 mm remain unchanged. Ten mm upper and nine mm lower engagement are assumed.
  - Open: Cam-to-distributor crossed-helical tooth geometry, working backlash and angular phase remain unverified; this is a connected spatial study, not validated power transmission.
  - Open: Oil galleries and pump mounting architecture require a production reference. Proposed block cuts and supports must not be used as machining instructions.
- [ ] **Intermediate shaft retaining ring · envelope** — `oil-pump-drive-retainer`; modeled quantity **1**; provisional.
  - Instances: `oil-pump-drive-retainer`
  - Source IDs: ford-industrial-csg649, fsm-a3698a10af15, melling-intermediate-shaft-dimensions. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: 20 degree lean, X227.584 station, gear-axis spacing, distributor lower extension, mounting bosses and pickup bends are constrained fit-study assumptions, not surveyed Ford geometry.
  - Open: Melling IS-74 length 114.808 mm and hex across flats 7.9248 mm remain unchanged. Ten mm upper and nine mm lower engagement are assumed.
  - Open: Cam-to-distributor crossed-helical tooth geometry, working backlash and angular phase remain unverified; this is a connected spatial study, not validated power transmission.
  - Open: Oil galleries and pump mounting architecture require a production reference. Proposed block cuts and supports must not be used as machining instructions.

## Additional known scope and reconciliation

- [ ] Verify shaft/retainer construction, tilted installed axis and drive interfaces

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
