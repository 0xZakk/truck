# Crankshaft damper, pulley, key and retaining hardware

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#64](https://github.com/0xZakk/truck/issues/64).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `821f7d3bb47d49a00ffb2975fa5faffcd306fe90bea48ce7c0d6308cd636653f`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Damper hub** — `damper-hub`; modeled quantity **1**; provisional.
  - Instances: `damper-hub`
  - Source IDs: dorman-2006-oes-catalog, dorman-594-152. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Only the 6.42-inch overall diameter and 2.8-inch overall width are catalog dimensions for Dorman 594-152. Internal diameters, section widths, keyway and grooves are not dimensioned.
  - Open: Axial placement follows the provisional crank snout. It is not an established engine datum or verified installed OE part.
  - Open: Bonded internal decomposition is an educational interpretation, not a service disassembly. Key and retaining hardware are represented by a provisional joint study. Integrated pulley grooves are now represented; their production profile and belt plane remain unverified.
  - Open: Front web recess and six integrated pulley grooves follow replacement appearance, but groove count, pitch, depth, root radius and web thickness remain provisional.
- [ ] **Damper elastomer** — `damper-elastomer`; modeled quantity **1**; provisional.
  - Instances: `damper-elastomer`
  - Source IDs: dorman-2006-oes-catalog, dorman-594-152. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Only the 6.42-inch overall diameter and 2.8-inch overall width are catalog dimensions for Dorman 594-152. Internal diameters, section widths, keyway and grooves are not dimensioned.
  - Open: Axial placement follows the provisional crank snout. It is not an established engine datum or verified installed OE part.
  - Open: Bonded internal decomposition is an educational interpretation, not a service disassembly. Key and retaining hardware are represented by a provisional joint study. Integrated pulley grooves are now represented; their production profile and belt plane remain unverified.
  - Open: Front web recess and six integrated pulley grooves follow replacement appearance, but groove count, pitch, depth, root radius and web thickness remain provisional.
- [ ] **Damper inertia ring** — `damper-inertia-ring`; modeled quantity **1**; provisional.
  - Instances: `damper-inertia-ring`
  - Source IDs: dorman-2006-oes-catalog, dorman-594-152. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Only the 6.42-inch overall diameter and 2.8-inch overall width are catalog dimensions for Dorman 594-152. Internal diameters, section widths, keyway and grooves are not dimensioned.
  - Open: Axial placement follows the provisional crank snout. It is not an established engine datum or verified installed OE part.
  - Open: Bonded internal decomposition is an educational interpretation, not a service disassembly. Key and retaining hardware are represented by a provisional joint study. Integrated pulley grooves are now represented; their production profile and belt plane remain unverified.
  - Open: Front web recess and six integrated pulley grooves follow replacement appearance, but groove count, pitch, depth, root radius and web thickness remain provisional.
- [ ] **Crankshaft damper key** — `damper-key`; modeled quantity **1**; provisional.
  - Instances: `damper-key`
  - Source IDs: dorman-594-152. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Key, washer, bolt, thread bore and extended crank nose dimensions are assumed fit-study geometry, not factory dimensions. Key shape/index and production thread/grade are unverified.
- [ ] **Damper retaining washer** — `damper-washer`; modeled quantity **1**; provisional.
  - Instances: `damper-washer`
  - Source IDs: dorman-594-152. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Key, washer, bolt, thread bore and extended crank nose dimensions are assumed fit-study geometry, not factory dimensions. Key shape/index and production thread/grade are unverified.
- [ ] **Damper retaining bolt** — `damper-bolt`; modeled quantity **1**; provisional.
  - Instances: `damper-bolt`
  - Source IDs: dorman-594-152. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Key, washer, bolt, thread bore and extended crank nose dimensions are assumed fit-study geometry, not factory dimensions. Key shape/index and production thread/grade are unverified.

## Additional known scope and reconciliation

- [ ] Verify integrated pulley construction and belt plane
- [ ] Separate bolt-on pulley not established

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
