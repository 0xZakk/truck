# Engine oil dipstick

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#17](https://github.com/0xZakk/truck/issues/17).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Engine oil dipstick blade · flexed study** — `engine-oil-dipstick-blade`; modeled quantity **1**; provisional.
  - Instances: `engine-oil-dipstick-blade`
  - Source IDs: dipstick-specimen-e9te, dipstick-service-catalog, dipstick-tube-1995-adjacent-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Educational interface estimates, not production dimensions or machining instructions. Exact1994 tube/indicator identity and upper support station remain unverified.
  - Open: Lower and upper mating threads are clearance envelopes. Thread engagement, sealing construction, bracket manufacturing joint, clamp load and retention strength are unvalidated.
  - Open: The pilot692.15mm approximate axial route comprises558.476126mm guide and133.673874mm free extension. Estimated waves add6.572804mm of material centerline; the material length is698.722804mm.
  - Open: Blade sections, waves, handle and stamp placement are inherited estimates. E9TE-6750-DA is specimen evidence, not owner identification; no ADD/FULL mark or oil calibration is reconstructed.
  - Open: The inserted blade is a rigid flexed display pose. Elastic insertion/withdrawal, twist, wave compression, handle retention force and service removal are not simulated.
- [ ] **Engine oil dipstick handle and stop · study** — `engine-oil-dipstick-handle`; modeled quantity **1**; provisional.
  - Instances: `engine-oil-dipstick-handle`
  - Source IDs: dipstick-specimen-e9te, dipstick-service-catalog, dipstick-tube-1995-adjacent-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Educational interface estimates, not production dimensions or machining instructions. Exact1994 tube/indicator identity and upper support station remain unverified.
  - Open: Lower and upper mating threads are clearance envelopes. Thread engagement, sealing construction, bracket manufacturing joint, clamp load and retention strength are unvalidated.
  - Open: The pilot692.15mm approximate axial route comprises558.476126mm guide and133.673874mm free extension. Estimated waves add6.572804mm of material centerline; the material length is698.722804mm.
  - Open: Blade sections, waves, handle and stamp placement are inherited estimates. E9TE-6750-DA is specimen evidence, not owner identification; no ADD/FULL mark or oil calibration is reconstructed.
  - Open: The inserted blade is a rigid flexed display pose. Elastic insertion/withdrawal, twist, wave compression, handle retention force and service removal are not simulated.

## Additional known scope and reconciliation

- [ ] Exact1994 indicator identity, section/waves and dimensions; current inserted specimen-informed study is installed
- [ ] Oil-level markings and calibration with the matched sump/guide; no ADD/FULL marks claimed
- [ ] Elastic insertion, withdrawal and handle retention force; inserted pose is a rigid geometry study

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
