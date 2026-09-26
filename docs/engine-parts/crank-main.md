# Crankshaft, main bearings and caps

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#23](https://github.com/0xZakk/truck/issues/23).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `f725260d8f1497a1b6f2aed9d41d01155bf2a82e7391d24ce866f352bb50cd5b`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Main bearing cap** — `main-cap`; modeled quantity **7**; provisional.
  - Instances: `main-cap-1`, `main-cap-2`, `main-cap-3`, `main-cap-4`, `main-cap-5`, `main-cap-6`, `main-cap-7`
  - Source IDs: not recorded. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact production contours, dimensions and tolerances need applicable drawings or measurements.
- [ ] **Upper main bearing shell** — `main-bearing-upper`; modeled quantity **7**; provisional.
  - Instances: `main-bearing-upper-1`, `main-bearing-upper-2`, `main-bearing-upper-3`, `main-bearing-upper-4`, `main-bearing-upper-5`, `main-bearing-upper-6`, `main-bearing-upper-7`
  - Source IDs: not recorded. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact production contours, dimensions and tolerances need applicable drawings or measurements.
- [ ] **Lower main bearing shell** — `main-bearing-lower`; modeled quantity **7**; provisional.
  - Instances: `main-bearing-lower-1`, `main-bearing-lower-2`, `main-bearing-lower-3`, `main-bearing-lower-4`, `main-bearing-lower-5`, `main-bearing-lower-6`, `main-bearing-lower-7`
  - Source IDs: not recorded. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact production contours, dimensions and tolerances need applicable drawings or measurements.
- [ ] **Main cap bolt** — `main-cap-bolt`; modeled quantity **14**; provisional.
  - Instances: `main-cap-bolt-1-1`, `main-cap-bolt-1-2`, `main-cap-bolt-2-1`, `main-cap-bolt-2-2`, `main-cap-bolt-3-1`, `main-cap-bolt-3-2`, `main-cap-bolt-4-1`, `main-cap-bolt-4-2`, `main-cap-bolt-5-1`, `main-cap-bolt-5-2`, `main-cap-bolt-6-1`, `main-cap-bolt-6-2`, `main-cap-bolt-7-1`, `main-cap-bolt-7-2`
  - Source IDs: not recorded. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact production contours, dimensions and tolerances need applicable drawings or measurements.
- [ ] **Crankshaft** — `crankshaft`; modeled quantity **1**; provisional.
  - Instances: `crankshaft`
  - Source IDs: fsm-2e5473b2bf99, fsm-2f144bda5e08, hicengine-ffm68, timken-pilot-dimensions. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Journal widths, axial stations, counterweight contours, fillets, oil drillings and flange holes remain provisional.
  - Open: Front crank nose length and damper key/retaining bore are provisional attachment-study geometry.
  - Open: Front crank nose length and damper key/retaining bore are provisional attachment-study geometry.

## Historical artifacts (not current installed inventory)

- `crank-throw-demo` — Historical/superseded or demonstration artifact absent from current manifest; retain as history, not an additional verified truck part.

## Additional known scope and reconciliation

- [ ] Resolve thrust-bearing construction and thrust faces
- [ ] Verify counterweights, fillets, oil drillings and journal interfaces

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
