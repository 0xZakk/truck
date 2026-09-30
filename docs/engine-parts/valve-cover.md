# Valve cover, gasket and attachment hardware

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#35](https://github.com/0xZakk/truck/issues/35).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `73de806af847c528e766151590d7b8235620893414c280711aa6ff382ca8a7e1`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Valve cover gasket** — `valve-cover-gasket`; modeled quantity **1**; provisional.
  - Instances: `valve-cover-gasket`
  - Source IDs: not recorded. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact production contours, dimensions and tolerances need applicable drawings or measurements.
- [ ] **Valve cover** — `valve-cover`; modeled quantity **1**; provisional.
  - Instances: `valve-cover`
  - Source IDs: engine-exploded-drawing, ford-engine-side-layout, upper-intake-topology-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Profile lofts are visual approximations. Upper profiles lean22mm toward the cam side to clear the corrected rocker placement; this is a fit-study assumption. The base envelope and fill/ventilation locations require measurements of the installed truck cover.
  - Open: Educational source-compared interface study, not factory dimensions. Plenum size and cap/throttle/EGR stations are inferred.
  - Open: Cap and matching neck use assumed4.5mm pitch; production thread dimensions and formed-versus-insert neck construction remain unknown.
  - Open: Nominal seal and hose contact do not establish compression, leak tightness, retention strength or production tolerance.
  - Open: Casting ribs, bosses and detailed wall distribution remain incomplete.

## Additional known scope and reconciliation

- [ ] Cover bolts, load spreaders and grommets if applicable: identify and separate
- [ ] Oil baffle/breather interfaces and filler-neck thread
- [ ] Verify production cover and gasket geometry

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
