# Timing gears, cam retention and front cover

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#32](https://github.com/0xZakk/truck/issues/32).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `4f98bbdad7fb1996487d17c4a651de588cef39254efe24e96384375dbdce0c07`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Camshaft thrust plate** — `cam-thrust-plate`; modeled quantity **1**; provisional.
  - Instances: `cam-thrust-plate`
  - Source IDs: ford-industrial-parts, fsm-33bfe47109d5, fsm-2e5473b2bf99. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Plate bore/thickness and spacer bore/OD follow an industrial comparison, not verified installed identities.
  - Open: Plate outline, bolt stations, washer section, key size, nose/hub profile and axial stations remain assumed. Female threads and press fits are not represented.
  - Open: The spacer provides an illustrative0.1mm axial allowance; no wear or thrust-load simulation is performed.
- [ ] **Cam timing-gear spacer** — `cam-gear-spacer`; modeled quantity **1**; provisional.
  - Instances: `cam-gear-spacer`
  - Source IDs: ford-industrial-parts, fsm-33bfe47109d5, fsm-2e5473b2bf99. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Plate bore/thickness and spacer bore/OD follow an industrial comparison, not verified installed identities.
  - Open: Plate outline, bolt stations, washer section, key size, nose/hub profile and axial stations remain assumed. Female threads and press fits are not represented.
  - Open: The spacer provides an illustrative0.1mm axial allowance; no wear or thrust-load simulation is performed.
- [ ] **Cam thrust-plate bolt** — `cam-thrust-bolt`; modeled quantity **2**; provisional.
  - Instances: `cam-thrust-bolt-1`, `cam-thrust-bolt-2`
  - Source IDs: ford-industrial-parts, fsm-33bfe47109d5, fsm-2e5473b2bf99. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Plate bore/thickness and spacer bore/OD follow an industrial comparison, not verified installed identities.
  - Open: Plate outline, bolt stations, washer section, key size, nose/hub profile and axial stations remain assumed. Female threads and press fits are not represented.
  - Open: The spacer provides an illustrative0.1mm axial allowance; no wear or thrust-load simulation is performed.
- [ ] **Cam thrust-plate washer** — `cam-thrust-washer`; modeled quantity **2**; provisional.
  - Instances: `cam-thrust-washer-1`, `cam-thrust-washer-2`
  - Source IDs: ford-industrial-parts, fsm-33bfe47109d5, fsm-2e5473b2bf99. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Plate bore/thickness and spacer bore/OD follow an industrial comparison, not verified installed identities.
  - Open: Plate outline, bolt stations, washer section, key size, nose/hub profile and axial stations remain assumed. Female threads and press fits are not represented.
  - Open: The spacer provides an illustrative0.1mm axial allowance; no wear or thrust-load simulation is performed.
- [ ] **Camshaft timing-gear key** — `cam-timing-key`; modeled quantity **1**; provisional.
  - Instances: `cam-timing-key`
  - Source IDs: ford-industrial-parts, fsm-33bfe47109d5, fsm-2e5473b2bf99. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Plate bore/thickness and spacer bore/OD follow an industrial comparison, not verified installed identities.
  - Open: Plate outline, bolt stations, washer section, key size, nose/hub profile and axial stations remain assumed. Female threads and press fits are not represented.
  - Open: The spacer provides an illustrative0.1mm axial allowance; no wear or thrust-load simulation is performed.
- [ ] **Crank Timing Gear** — `crank-timing-gear`; modeled quantity **1**; provisional.
  - Instances: `crank-timing-gear`
  - Source IDs: fsm-33bfe47109d5. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact tooth count, pressure angle, material and timing-mark stations are unverified.
- [ ] **Cam Timing Gear** — `cam-timing-gear`; modeled quantity **1**; provisional.
  - Instances: `cam-timing-gear`
  - Source IDs: fsm-33bfe47109d5. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact tooth count, pressure angle, material and timing-mark stations are unverified.
- [ ] **Front crankshaft seal** — `front-seal`; modeled quantity **1**; provisional.
  - Instances: `front-seal`
  - Source IDs: not recorded. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact production contours, dimensions and tolerances need applicable drawings or measurements.
- [ ] **Timing cover** — `timing-cover`; modeled quantity **1**; provisional.
  - Instances: `timing-cover`
  - Source IDs: ford-industrial-parts, ford-engine-side-layout. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Outer radii52/88mm, inner radii48/84mm and24mmdepth are assumed clearance-study dimensions, not a production casting trace. Block flange, bolt pattern and pump interfaces remain unfinished.

## Additional known scope and reconciliation

- [ ] Timing-cover gasket and attachment hardware: reconcile separate parts
- [ ] Timing pointer/marks and attachment: verify configuration
- [ ] Gear teeth, helix, keys, thrust clearance and production retention

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
