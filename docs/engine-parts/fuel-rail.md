# Fuel rails, return tube and retaining hardware

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#40](https://github.com/0xZakk/truck/issues/40).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `bfab1f2596991d27fe5e52e90f02d070eb034f9de8c2cd72d3dd44666d6c8bb9`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Fuel rail retaining bolt · 1/4-20 × .90 inch** — `fuel-rail-mount-bolt`; modeled quantity **3**; provisional.
  - Instances: `fuel-rail-mount-bolt-1`, `fuel-rail-mount-bolt-2`, `fuel-rail-mount-bolt-3`
  - Source IDs: system-12bc4a9dabbf. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Architecture and component identities follow factory service illustrations. All modeled envelopes, internal profiles, fits, rail bends and installed positions are provisional, not measured production dimensions.
  - Open: Coils and filters are simplified material envelopes; winding count, mesh, calibrated orifices, spring rates and injector flow calibration are not established. No fuel-pressure or atomization simulation is claimed.
- [ ] **Fuel rail retaining washer** — `fuel-rail-mount-washer`; modeled quantity **3**; provisional.
  - Instances: `fuel-rail-mount-washer-1`, `fuel-rail-mount-washer-2`, `fuel-rail-mount-washer-3`
  - Source IDs: system-bd3903b7892e, system-57b3dbc66361, system-750bd1047639, system-73d3dd2d32e7, system-12bc4a9dabbf. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Architecture and component identities follow factory service illustrations. All modeled envelopes, internal profiles, fits, rail bends and installed positions are provisional, not measured production dimensions.
  - Open: Coils and filters are simplified material envelopes; winding count, mesh, calibrated orifices, spring rates and injector flow calibration are not established. No fuel-pressure or atomization simulation is claimed.
- [ ] **Fuel supply rail** — `fuel-supply-rail`; modeled quantity **1**; provisional.
  - Instances: `fuel-supply-rail`
  - Source IDs: system-bd3903b7892e, system-57b3dbc66361, system-750bd1047639, system-73d3dd2d32e7, system-12bc4a9dabbf. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Architecture and component identities follow factory service illustrations. All modeled envelopes, internal profiles, fits, rail bends and installed positions are provisional, not measured production dimensions.
  - Open: Coils and filters are simplified material envelopes; winding count, mesh, calibrated orifices, spring rates and injector flow calibration are not established. No fuel-pressure or atomization simulation is claimed.
- [ ] **Fuel return tube** — `fuel-return-tube`; modeled quantity **1**; provisional.
  - Instances: `fuel-return-tube`
  - Source IDs: system-bd3903b7892e, system-57b3dbc66361, system-750bd1047639, system-73d3dd2d32e7, system-12bc4a9dabbf. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Architecture and component identities follow factory service illustrations. All modeled envelopes, internal profiles, fits, rail bends and installed positions are provisional, not measured production dimensions.
  - Open: Coils and filters are simplified material envelopes; winding count, mesh, calibrated orifices, spring rates and injector flow calibration are not established. No fuel-pressure or atomization simulation is claimed.

## Additional known scope and reconciliation

- [ ] Verify mounting stations, joints and flow passages

## Cross-system boundaries

Coordinate with [#7](https://github.com/0xZakk/truck/issues/7). Keep the current engine-mounted component here; agree ownership before adding its vehicle-side continuation.

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
