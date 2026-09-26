# Pushrod side cover, gasket and hardware

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#26](https://github.com/0xZakk/truck/issues/26).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `821f7d3bb47d49a00ffb2975fa5faffcd306fe90bea48ce7c0d6308cd636653f`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Pushrod side cover** — `pushrod-cover`; modeled quantity **1**; provisional.
  - Instances: `pushrod-cover`
  - Source IDs: enginequest-fsp300n, fel-pro-vin-y-gaskets, ford-industrial-parts, fel-pro-10740-retailer. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Cover envelope, hole stations, stamped ribs, gasket section and casting interface are provisional.
  - Open: Grommet dimensions are a retailer replacement envelope; hidden section and compression are unverified.
  - Open: 5/16-18 x1-inch bolt is an industrial comparison. The present uncompressed stack gives only3.908mm engagement; installed bolt identity and adequacy remain unverified.
- [ ] **Pushrod cover perimeter gasket** — `pushrod-cover-gasket`; modeled quantity **1**; provisional.
  - Instances: `pushrod-cover-gasket`
  - Source IDs: enginequest-fsp300n, fel-pro-vin-y-gaskets, ford-industrial-parts, fel-pro-10740-retailer. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Cover envelope, hole stations, stamped ribs, gasket section and casting interface are provisional.
  - Open: Grommet dimensions are a retailer replacement envelope; hidden section and compression are unverified.
  - Open: 5/16-18 x1-inch bolt is an industrial comparison. The present uncompressed stack gives only3.908mm engagement; installed bolt identity and adequacy remain unverified.
- [ ] **Pushrod cover bolt grommet** — `pushrod-cover-grommet`; modeled quantity **6**; provisional.
  - Instances: `pushrod-cover-grommet-1`, `pushrod-cover-grommet-2`, `pushrod-cover-grommet-3`, `pushrod-cover-grommet-4`, `pushrod-cover-grommet-5`, `pushrod-cover-grommet-6`
  - Source IDs: enginequest-fsp300n, fel-pro-vin-y-gaskets, ford-industrial-parts, fel-pro-10740-retailer. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Cover envelope, hole stations, stamped ribs, gasket section and casting interface are provisional.
  - Open: Grommet dimensions are a retailer replacement envelope; hidden section and compression are unverified.
  - Open: 5/16-18 x1-inch bolt is an industrial comparison. The present uncompressed stack gives only3.908mm engagement; installed bolt identity and adequacy remain unverified.
- [ ] **Pushrod cover bolt · industrial comparison** — `pushrod-cover-bolt`; modeled quantity **6**; provisional.
  - Instances: `pushrod-cover-bolt-1`, `pushrod-cover-bolt-2`, `pushrod-cover-bolt-3`, `pushrod-cover-bolt-4`, `pushrod-cover-bolt-5`, `pushrod-cover-bolt-6`
  - Source IDs: enginequest-fsp300n, fel-pro-vin-y-gaskets, ford-industrial-parts, fel-pro-10740-retailer. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Cover envelope, hole stations, stamped ribs, gasket section and casting interface are provisional.
  - Open: Grommet dimensions are a retailer replacement envelope; hidden section and compression are unverified.
  - Open: 5/16-18 x1-inch bolt is an industrial comparison. The present uncompressed stack gives only3.908mm engagement; installed bolt identity and adequacy remain unverified.

## Additional known scope and reconciliation

- [ ] Production contour, sealing compression and bolt engagement

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
