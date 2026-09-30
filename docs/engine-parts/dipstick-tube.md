# Dipstick guide tube, seat and retaining hardware

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#78](https://github.com/0xZakk/truck/issues/78).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `ab99fff2f63ad5dfc21fde8d12a32fc2a3d65832e6c8664baefd99d94403f7bf`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Engine oil dipstick guide · estimated** — `engine-oil-dipstick-tube`; modeled quantity **1**; provisional.
  - Instances: `engine-oil-dipstick-tube`
  - Source IDs: dipstick-specimen-e9te, dipstick-service-catalog, dipstick-tube-1995-adjacent-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Educational interface estimates, not production dimensions or machining instructions. Exact1994 tube/indicator identity and upper support station remain unverified.
  - Open: Lower and upper mating threads are clearance envelopes. Thread engagement, sealing construction, bracket manufacturing joint, clamp load and retention strength are unvalidated.
  - Open: The pilot692.15mm approximate axial route comprises558.476126mm guide and133.673874mm free extension. Estimated waves add6.572804mm of material centerline; the material length is698.722804mm.
  - Open: Blade sections, waves, handle and stamp placement are inherited estimates. E9TE-6750-DA is specimen evidence, not owner identification; no ADD/FULL mark or oil calibration is reconstructed.
  - Open: The inserted blade is a rigid flexed display pose. Elastic insertion/withdrawal, twist, wave compression, handle retention force and service removal are not simulated.
- [ ] **Dipstick lower retaining nut · estimated** — `engine-oil-dipstick-tube-retaining-nut`; modeled quantity **1**; provisional.
  - Instances: `engine-oil-dipstick-tube-retaining-nut`
  - Source IDs: dipstick-specimen-e9te, dipstick-service-catalog, dipstick-tube-1995-adjacent-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Educational interface estimates, not production dimensions or machining instructions. Exact1994 tube/indicator identity and upper support station remain unverified.
  - Open: Lower and upper mating threads are clearance envelopes. Thread engagement, sealing construction, bracket manufacturing joint, clamp load and retention strength are unvalidated.
  - Open: The pilot692.15mm approximate axial route comprises558.476126mm guide and133.673874mm free extension. Estimated waves add6.572804mm of material centerline; the material length is698.722804mm.
  - Open: Blade sections, waves, handle and stamp placement are inherited estimates. E9TE-6750-DA is specimen evidence, not owner identification; no ADD/FULL mark or oil calibration is reconstructed.
  - Open: The inserted blade is a rigid flexed display pose. Elastic insertion/withdrawal, twist, wave compression, handle retention force and service removal are not simulated.
- [ ] **Dipstick tube support bracket · estimated** — `engine-oil-dipstick-tube-bracket`; modeled quantity **1**; provisional.
  - Instances: `engine-oil-dipstick-tube-bracket`
  - Source IDs: dipstick-specimen-e9te, dipstick-service-catalog, dipstick-tube-1995-adjacent-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Educational interface estimates, not production dimensions or machining instructions. Exact1994 tube/indicator identity and upper support station remain unverified.
  - Open: Lower and upper mating threads are clearance envelopes. Thread engagement, sealing construction, bracket manufacturing joint, clamp load and retention strength are unvalidated.
  - Open: The pilot692.15mm approximate axial route comprises558.476126mm guide and133.673874mm free extension. Estimated waves add6.572804mm of material centerline; the material length is698.722804mm.
  - Open: Blade sections, waves, handle and stamp placement are inherited estimates. E9TE-6750-DA is specimen evidence, not owner identification; no ADD/FULL mark or oil calibration is reconstructed.
  - Open: The inserted blade is a rigid flexed display pose. Elastic insertion/withdrawal, twist, wave compression, handle retention force and service removal are not simulated.
- [ ] **Dipstick support nut · estimated** — `engine-oil-dipstick-tube-support-nut`; modeled quantity **1**; provisional.
  - Instances: `engine-oil-dipstick-tube-support-nut`
  - Source IDs: dipstick-specimen-e9te, dipstick-service-catalog, dipstick-tube-1995-adjacent-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Educational interface estimates, not production dimensions or machining instructions. Exact1994 tube/indicator identity and upper support station remain unverified.
  - Open: Lower and upper mating threads are clearance envelopes. Thread engagement, sealing construction, bracket manufacturing joint, clamp load and retention strength are unvalidated.
  - Open: The pilot692.15mm approximate axial route comprises558.476126mm guide and133.673874mm free extension. Estimated waves add6.572804mm of material centerline; the material length is698.722804mm.
  - Open: Blade sections, waves, handle and stamp placement are inherited estimates. E9TE-6750-DA is specimen evidence, not owner identification; no ADD/FULL mark or oil calibration is reconstructed.
  - Open: The inserted blade is a rigid flexed display pose. Elastic insertion/withdrawal, twist, wave compression, handle retention force and service removal are not simulated.
- [ ] **Dipstick support / cover retainer · estimated** — `pushrod-cover-dipstick-retainer-estimated`; modeled quantity **1**; provisional.
  - Instances: `pushrod-cover-bolt-1`
  - Source IDs: dipstick-specimen-e9te, dipstick-service-catalog, dipstick-tube-1995-adjacent-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Educational interface estimates, not production dimensions or machining instructions. Exact1994 tube/indicator identity and upper support station remain unverified.
  - Open: Lower and upper mating threads are clearance envelopes. Thread engagement, sealing construction, bracket manufacturing joint, clamp load and retention strength are unvalidated.
  - Open: The pilot692.15mm approximate axial route comprises558.476126mm guide and133.673874mm free extension. Estimated waves add6.572804mm of material centerline; the material length is698.722804mm.
  - Open: Blade sections, waves, handle and stamp placement are inherited estimates. E9TE-6750-DA is specimen evidence, not owner identification; no ADD/FULL mark or oil calibration is reconstructed.
  - Open: The inserted blade is a rigid flexed display pose. Elastic insertion/withdrawal, twist, wave compression, handle retention force and service removal are not simulated.

## Additional known scope and reconciliation

- [ ] Exact1994 guide/indicator identity and routing; current estimated guide, receiver, bracket and hardware are installed
- [ ] Production threads, seals, clamp load and attachment strength; modeled nut/receiver threads are clearance envelopes
- [ ] Support bracket manufacturing joint and actual upper mounting station; adjacent1995 architecture remains applicability-limited

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
