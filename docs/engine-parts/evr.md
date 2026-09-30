# EGR vacuum regulator and internals

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#58](https://github.com/0xZakk/truck/issues/58).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `73de806af847c528e766151590d7b8235620893414c280711aa6ff382ca8a7e1`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **EVR winding insulator · illustrative** — `evr-bobbin-illustrative`; modeled quantity **1**; provisional.
  - Instances: `evr-bobbin-illustrative`
  - Source IDs: ford-evr-factory, standard-vs52, truck-egr-evtm, evr-detail-mechanism-comparison. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact1994 supports filtered vent and electromagnetic disc/orifice operation. Complete hidden arrangement is an explicitly illustrative positive-gain comparison, not a factory internal replica.
  - Open: All new dimensions, fifteen winding turns, wire size, spring rate/preload, filter permeability pattern and cap bead/groove are uncalibrated estimates. Actual installed identity remains unknown.
  - Open: Five discrete disc/spring poses illustrate vent opening only; no PCM duty-cycle, pressure, resistance, force, flow or elastic simulation. Mounting bracket, fasteners and vehicle hose routing remain unfinished.
- [ ] **EVR chamber and ports** — `evr-body`; modeled quantity **1**; provisional.
  - Instances: `evr-body`
  - Source IDs: ford-evr-factory, standard-vs52, truck-egr-evtm, evr-detail-mechanism-comparison. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exterior dimensions, mounting ears, hose diameters and installed datum are provisional. Factory EVTM locates the unit below EVP at the left rear of the engine.
  - Open: Port routing is source-supported. No calibrated vacuum response or electrical simulation is claimed. Mounting bracket and fasteners remain unfinished.
  - Open: Exact1994 supports filtered vent and electromagnetic disc/orifice operation. Complete hidden arrangement is an explicitly illustrative positive-gain comparison, not a factory internal replica.
  - Open: All new dimensions, fifteen winding turns, wire size, spring rate/preload, filter permeability pattern and cap bead/groove are uncalibrated estimates. Actual installed identity remains unknown.
  - Open: Five discrete disc/spring poses illustrate vent opening only; no PCM duty-cycle, pressure, resistance, force, flow or elastic simulation. Mounting bracket, fasteners and vehicle hose routing remain unfinished.
- [ ] **EVR vent cap and illustrative capture** — `evr-cap`; modeled quantity **1**; provisional.
  - Instances: `evr-cap`
  - Source IDs: ford-evr-factory, standard-vs52, truck-egr-evtm, evr-detail-mechanism-comparison. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exterior dimensions, mounting ears, hose diameters and installed datum are provisional. Factory EVTM locates the unit below EVP at the left rear of the engine.
  - Open: Port routing is source-supported. No calibrated vacuum response or electrical simulation is claimed. Mounting bracket and fasteners remain unfinished.
  - Open: Exact1994 supports filtered vent and electromagnetic disc/orifice operation. Complete hidden arrangement is an explicitly illustrative positive-gain comparison, not a factory internal replica.
  - Open: All new dimensions, fifteen winding turns, wire size, spring rate/preload, filter permeability pattern and cap bead/groove are uncalibrated estimates. Actual installed identity remains unknown.
  - Open: Five discrete disc/spring poses illustrate vent opening only; no PCM duty-cycle, pressure, resistance, force, flow or elastic simulation. Mounting bracket, fasteners and vehicle hose routing remain unfinished.
- [ ] **EVR hollow core · illustrative** — `evr-core-illustrative`; modeled quantity **1**; provisional.
  - Instances: `evr-core-illustrative`
  - Source IDs: ford-evr-factory, standard-vs52, truck-egr-evtm, evr-detail-mechanism-comparison. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact1994 supports filtered vent and electromagnetic disc/orifice operation. Complete hidden arrangement is an explicitly illustrative positive-gain comparison, not a factory internal replica.
  - Open: All new dimensions, fifteen winding turns, wire size, spring rate/preload, filter permeability pattern and cap bead/groove are uncalibrated estimates. Actual installed identity remains unknown.
  - Open: Five discrete disc/spring poses illustrate vent opening only; no PCM duty-cycle, pressure, resistance, force, flow or elastic simulation. Mounting bracket, fasteners and vehicle hose routing remain unfinished.
- [ ] **EVR vent disc · illustrative** — `evr-disc-illustrative`; modeled quantity **1**; provisional.
  - Instances: `evr-disc-illustrative`
  - Source IDs: ford-evr-factory, standard-vs52, truck-egr-evtm, evr-detail-mechanism-comparison. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact1994 supports filtered vent and electromagnetic disc/orifice operation. Complete hidden arrangement is an explicitly illustrative positive-gain comparison, not a factory internal replica.
  - Open: All new dimensions, fifteen winding turns, wire size, spring rate/preload, filter permeability pattern and cap bead/groove are uncalibrated estimates. Actual installed identity remains unknown.
  - Open: Five discrete disc/spring poses illustrate vent opening only; no PCM duty-cycle, pressure, resistance, force, flow or elastic simulation. Mounting bracket, fasteners and vehicle hose routing remain unfinished.
- [ ] **EVR disc spring · illustrative** — `evr-disc-spring-illustrative`; modeled quantity **1**; provisional.
  - Instances: `evr-disc-spring-illustrative`
  - Source IDs: ford-evr-factory, standard-vs52, truck-egr-evtm, evr-detail-mechanism-comparison. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact1994 supports filtered vent and electromagnetic disc/orifice operation. Complete hidden arrangement is an explicitly illustrative positive-gain comparison, not a factory internal replica.
  - Open: All new dimensions, fifteen winding turns, wire size, spring rate/preload, filter permeability pattern and cap bead/groove are uncalibrated estimates. Actual installed identity remains unknown.
  - Open: Five discrete disc/spring poses illustrate vent opening only; no PCM duty-cycle, pressure, resistance, force, flow or elastic simulation. Mounting bracket, fasteners and vehicle hose routing remain unfinished.
- [ ] **EVR magnetic shell · illustrative** — `evr-magnetic-shell-illustrative`; modeled quantity **1**; provisional.
  - Instances: `evr-magnetic-shell-illustrative`
  - Source IDs: ford-evr-factory, standard-vs52, truck-egr-evtm, evr-detail-mechanism-comparison. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact1994 supports filtered vent and electromagnetic disc/orifice operation. Complete hidden arrangement is an explicitly illustrative positive-gain comparison, not a factory internal replica.
  - Open: All new dimensions, fifteen winding turns, wire size, spring rate/preload, filter permeability pattern and cap bead/groove are uncalibrated estimates. Actual installed identity remains unknown.
  - Open: Five discrete disc/spring poses illustrate vent opening only; no PCM duty-cycle, pressure, resistance, force, flow or elastic simulation. Mounting bracket, fasteners and vehicle hose routing remain unfinished.
- [ ] **EVR control terminal** — `evr-terminal-control`; modeled quantity **1**; provisional.
  - Instances: `evr-terminal-control`
  - Source IDs: ford-evr-factory, standard-vs52, truck-egr-evtm, evr-detail-mechanism-comparison. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exterior dimensions, mounting ears, hose diameters and installed datum are provisional. Factory EVTM locates the unit below EVP at the left rear of the engine.
  - Open: Port routing is source-supported. No calibrated vacuum response or electrical simulation is claimed. Mounting bracket and fasteners remain unfinished.
  - Open: Exact1994 supports filtered vent and electromagnetic disc/orifice operation. Complete hidden arrangement is an explicitly illustrative positive-gain comparison, not a factory internal replica.
  - Open: All new dimensions, fifteen winding turns, wire size, spring rate/preload, filter permeability pattern and cap bead/groove are uncalibrated estimates. Actual installed identity remains unknown.
  - Open: Five discrete disc/spring poses illustrate vent opening only; no PCM duty-cycle, pressure, resistance, force, flow or elastic simulation. Mounting bracket, fasteners and vehicle hose routing remain unfinished.
- [ ] **EVR supply terminal** — `evr-terminal-supply`; modeled quantity **1**; provisional.
  - Instances: `evr-terminal-supply`
  - Source IDs: ford-evr-factory, standard-vs52, truck-egr-evtm, evr-detail-mechanism-comparison. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exterior dimensions, mounting ears, hose diameters and installed datum are provisional. Factory EVTM locates the unit below EVP at the left rear of the engine.
  - Open: Port routing is source-supported. No calibrated vacuum response or electrical simulation is claimed. Mounting bracket and fasteners remain unfinished.
  - Open: Exact1994 supports filtered vent and electromagnetic disc/orifice operation. Complete hidden arrangement is an explicitly illustrative positive-gain comparison, not a factory internal replica.
  - Open: All new dimensions, fifteen winding turns, wire size, spring rate/preload, filter permeability pattern and cap bead/groove are uncalibrated estimates. Actual installed identity remains unknown.
  - Open: Five discrete disc/spring poses illustrate vent opening only; no PCM duty-cycle, pressure, resistance, force, flow or elastic simulation. Mounting bracket, fasteners and vehicle hose routing remain unfinished.
- [ ] **EVR filter · illustrative** — `evr-vent-filter-illustrative`; modeled quantity **1**; provisional.
  - Instances: `evr-vent-filter-illustrative`
  - Source IDs: ford-evr-factory, standard-vs52, truck-egr-evtm, evr-detail-mechanism-comparison. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact1994 supports filtered vent and electromagnetic disc/orifice operation. Complete hidden arrangement is an explicitly illustrative positive-gain comparison, not a factory internal replica.
  - Open: All new dimensions, fifteen winding turns, wire size, spring rate/preload, filter permeability pattern and cap bead/groove are uncalibrated estimates. Actual installed identity remains unknown.
  - Open: Five discrete disc/spring poses illustrate vent opening only; no PCM duty-cycle, pressure, resistance, force, flow or elastic simulation. Mounting bracket, fasteners and vehicle hose routing remain unfinished.
- [ ] **EVR continuous winding · illustrative** — `evr-winding-illustrative`; modeled quantity **1**; provisional.
  - Instances: `evr-winding-illustrative`
  - Source IDs: ford-evr-factory, standard-vs52, truck-egr-evtm, evr-detail-mechanism-comparison. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact1994 supports filtered vent and electromagnetic disc/orifice operation. Complete hidden arrangement is an explicitly illustrative positive-gain comparison, not a factory internal replica.
  - Open: All new dimensions, fifteen winding turns, wire size, spring rate/preload, filter permeability pattern and cap bead/groove are uncalibrated estimates. Actual installed identity remains unknown.
  - Open: Five discrete disc/spring poses illustrate vent opening only; no PCM duty-cycle, pressure, resistance, force, flow or elastic simulation. Mounting bracket, fasteners and vehicle hose routing remain unfinished.

## Additional known scope and reconciliation

- [ ] Eleven comparative component models include coil, disc/seat, spring, filter/vent and electrical connections. Verify installed identity, production internals, dimensions and calibration; browser acceptance remains pending.
- [ ] Mounting bracket, hardware, vacuum and electrical connectors

## Cross-system boundaries

Coordinate with [#7](https://github.com/0xZakk/truck/issues/7). Keep the current engine-mounted component here; agree ownership before adding its vehicle-side continuation.

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
