# EGR vacuum regulator and internals

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#58](https://github.com/0xZakk/truck/issues/58).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `821f7d3bb47d49a00ffb2975fa5faffcd306fe90bea48ce7c0d6308cd636653f`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **EVR body and hose ports** — `evr-body`; modeled quantity **1**; provisional.
  - Instances: `evr-body`
  - Source IDs: ford-evr-factory, standard-vs52, truck-egr-evtm. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exterior dimensions, mounting ears, hose diameters and installed datum are provisional. Factory EVTM locates the unit below EVP at the left rear of the engine.
  - Open: Solenoid winding, magnetic circuit, moving valve, atmospheric bleed/filter, terminal straps and seals remain unmodeled; this is an exterior reconstruction, not a complete internal replica.
  - Open: Port routing is source-supported. No calibrated vacuum response or electrical simulation is claimed. Mounting bracket and fasteners remain unfinished.
- [ ] **EVR upper cap** — `evr-cap`; modeled quantity **1**; provisional.
  - Instances: `evr-cap`
  - Source IDs: ford-evr-factory, standard-vs52, truck-egr-evtm. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exterior dimensions, mounting ears, hose diameters and installed datum are provisional. Factory EVTM locates the unit below EVP at the left rear of the engine.
  - Open: Solenoid winding, magnetic circuit, moving valve, atmospheric bleed/filter, terminal straps and seals remain unmodeled; this is an exterior reconstruction, not a complete internal replica.
  - Open: Port routing is source-supported. No calibrated vacuum response or electrical simulation is claimed. Mounting bracket and fasteners remain unfinished.
- [ ] **EVR power terminal** — `evr-terminal-supply`; modeled quantity **1**; provisional.
  - Instances: `evr-terminal-supply`
  - Source IDs: ford-evr-factory, standard-vs52, truck-egr-evtm. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exterior dimensions, mounting ears, hose diameters and installed datum are provisional. Factory EVTM locates the unit below EVP at the left rear of the engine.
  - Open: Solenoid winding, magnetic circuit, moving valve, atmospheric bleed/filter, terminal straps and seals remain unmodeled; this is an exterior reconstruction, not a complete internal replica.
  - Open: Port routing is source-supported. No calibrated vacuum response or electrical simulation is claimed. Mounting bracket and fasteners remain unfinished.
- [ ] **EVR control terminal** — `evr-terminal-control`; modeled quantity **1**; provisional.
  - Instances: `evr-terminal-control`
  - Source IDs: ford-evr-factory, standard-vs52, truck-egr-evtm. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exterior dimensions, mounting ears, hose diameters and installed datum are provisional. Factory EVTM locates the unit below EVP at the left rear of the engine.
  - Open: Solenoid winding, magnetic circuit, moving valve, atmospheric bleed/filter, terminal straps and seals remain unmodeled; this is an exterior reconstruction, not a complete internal replica.
  - Open: Port routing is source-supported. No calibrated vacuum response or electrical simulation is claimed. Mounting bracket and fasteners remain unfinished.

## Additional known scope and reconciliation

- [ ] Coil, valve, seat, filter/vent and internal connections: applicability/decomposition pending
- [ ] Mounting bracket, hardware, vacuum and electrical connectors

## Cross-system boundaries

Coordinate with [#7](https://github.com/0xZakk/truck/issues/7). Keep the current engine-mounted component here; agree ownership before adding its vehicle-side continuation.

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
