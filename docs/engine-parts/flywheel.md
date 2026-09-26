# Flywheel, ring gear and crankshaft bolts

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#62](https://github.com/0xZakk/truck/issues/62).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `f1dc26ba64eb0ba1e8fede4ef42e23a5ae3e288dbeae3cc4b2558cf4148a4a70`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Flywheel body** — `flywheel-body`; modeled quantity **1**; provisional.
  - Instances: `flywheel-body`
  - Source IDs: luk-flywheel, hicengine-ffm68. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: HICENGINE FFM68 is a replacement cross-reference to LFW132, not an inspected OEM flywheel or proof of installed identity.
  - Open: Catalog constrains 362 mm OD, 44.5 mm bore, 25 mm thickness, six 11 mm crank holes on 76 mm PCD, 295 mm cover PCD and 164 teeth. Axial datums, recesses, cover hole count/threads and angular indexing remain provisional.
  - Open: Ring width, shrink fit, tooth pressure angle/profile, balance drilling, dowels and fastener thread/grade are unverified. Clutch diameter remains unresolved between catalog options; pilot bearing and clutch internals remain unfinished.
- [ ] **Starter ring gear** — `flywheel-ring-gear`; modeled quantity **1**; provisional.
  - Instances: `flywheel-ring-gear`
  - Source IDs: luk-flywheel, hicengine-ffm68. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: HICENGINE FFM68 is a replacement cross-reference to LFW132, not an inspected OEM flywheel or proof of installed identity.
  - Open: Catalog constrains 362 mm OD, 44.5 mm bore, 25 mm thickness, six 11 mm crank holes on 76 mm PCD, 295 mm cover PCD and 164 teeth. Axial datums, recesses, cover hole count/threads and angular indexing remain provisional.
  - Open: Ring width, shrink fit, tooth pressure angle/profile, balance drilling, dowels and fastener thread/grade are unverified. Clutch diameter remains unresolved between catalog options; pilot bearing and clutch internals remain unfinished.
- [ ] **Flywheel crankshaft bolt** — `flywheel-crank-bolt`; modeled quantity **6**; provisional.
  - Instances: `flywheel-crank-bolt-1`, `flywheel-crank-bolt-2`, `flywheel-crank-bolt-3`, `flywheel-crank-bolt-4`, `flywheel-crank-bolt-5`, `flywheel-crank-bolt-6`
  - Source IDs: luk-flywheel, hicengine-ffm68. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: HICENGINE FFM68 is a replacement cross-reference to LFW132, not an inspected OEM flywheel or proof of installed identity.
  - Open: Catalog constrains 362 mm OD, 44.5 mm bore, 25 mm thickness, six 11 mm crank holes on 76 mm PCD, 295 mm cover PCD and 164 teeth. Axial datums, recesses, cover hole count/threads and angular indexing remain provisional.
  - Open: Ring width, shrink fit, tooth pressure angle/profile, balance drilling, dowels and fastener thread/grade are unverified. Clutch diameter remains unresolved between catalog options; pilot bearing and clutch internals remain unfinished.

## Additional known scope and reconciliation

- [ ] Verify production profile, indexing, ring fit and threads
- [ ] Clutch disc/pressure plate belong to Transmission and clutch

## Cross-system boundaries

Coordinate with [#2](https://github.com/0xZakk/truck/issues/2). Keep the current engine-mounted component here; agree ownership before adding its vehicle-side continuation.

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
