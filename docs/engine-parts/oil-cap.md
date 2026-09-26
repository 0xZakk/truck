# Oil filler cap and seal

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#15](https://github.com/0xZakk/truck/issues/15).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `f1dc26ba64eb0ba1e8fede4ef42e23a5ae3e288dbeae3cc4b2558cf4148a4a70`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Oil filler cap** — `oil-filler-cap`; modeled quantity **1**; provisional.
  - Instances: `oil-filler-cap`
  - Source IDs: upper-intake-topology-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact production contours, dimensions and tolerances need applicable drawings or measurements.
  - Open: Educational source-compared interface study, not factory dimensions. Plenum size and cap/throttle/EGR stations are inferred.
  - Open: Cap and matching neck use assumed4.5mm pitch; production thread dimensions and formed-versus-insert neck construction remain unknown.
  - Open: Nominal seal and hose contact do not establish compression, leak tightness, retention strength or production tolerance.
  - Open: Casting ribs, bosses and detailed wall distribution remain incomplete.
- [ ] **Oil filler cap seal · estimated** — `oil-filler-cap-seal`; modeled quantity **1**; provisional.
  - Instances: `oil-filler-cap-seal`
  - Source IDs: upper-intake-topology-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Educational source-compared interface study, not factory dimensions. Plenum size and cap/throttle/EGR stations are inferred.
  - Open: Cap and matching neck use assumed4.5mm pitch; production thread dimensions and formed-versus-insert neck construction remain unknown.
  - Open: Nominal seal and hose contact do not establish compression, leak tightness, retention strength or production tolerance.
  - Open: Casting ribs, bosses and detailed wall distribution remain incomplete.

## Additional known scope and reconciliation

- [ ] Cap, separate seal and continuous matching threaded neck are installed as an educational study; production identity, pitch, dimensions and neck construction remain unverified
- [ ] Installed cap removal and12-rocker interference studies pass at their recorded hashes; actual material deformation, seal compression and leak tightness remain unknown

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
