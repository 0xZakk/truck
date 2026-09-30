# EGR exhaust tube and connections

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#59](https://github.com/0xZakk/truck/issues/59).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `73de806af847c528e766151590d7b8235620893414c280711aa6ff382ca8a7e1`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **EGR tube manifold fitting** — `egr-tube-manifold-fitting`; modeled quantity **1**; provisional.
  - Instances: `egr-tube-manifold-fitting`
  - Source IDs: dorman-598-105, efi-intake-drawing, dorman-674186-profile-specification, dorman-674186-head-facing-photo, dorman-674186-opposite-photo, dorman-674186-overview-photo, dorman-674186-catalog-application. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Tube OD is from the applicable replacement catalog; wall thickness, bend coordinates and fitting dimensions are provisional.
  - Open: The published 17.9 inch length has no measurement definition and is not treated as a verified developed centerline length.
  - Open: Protective sleeve construction, thread forms and sealing seats remain unverified. Route is a candidate, not installed factory routing.
  - Open: Manufacturer674-186 photos and catalog application support three rounded-rectangular rear entries, not their dimensions or installed casting identity.
  - Open: Entry28x28mm, corner3mm, outer36x36mm and transition stations reuse provisional front study dimensions; no pixel scaling is used.
  - Open: This incremental entry correction retains the old collector and EGR end connection. Both remain unsupported form/routing studies pending joint reconstruction; this is not a completed rear manifold.
  - Open: The provisional EGR fitting insertion envelope is shortened from19mm to12.5mm so its tip ends0.5mm before the collector inner wall rather than intruding into the collector and rear runner. This is a geometric clearance assumption, not a verified thread engagement or retention specification.
  - Open: Production flange lands, head attachment, outlet flange, auxiliary ports, wall thickness and thermal/flow performance remain unverified.
- [ ] **EGR exhaust tube** — `egr-exhaust-tube`; modeled quantity **1**; provisional.
  - Instances: `egr-exhaust-tube`
  - Source IDs: dorman-598-105, efi-intake-drawing, upper-intake-topology-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Tube OD is from the applicable replacement catalog; wall thickness, bend coordinates and fitting dimensions are provisional.
  - Open: The published 17.9 inch length has no measurement definition and is not treated as a verified developed centerline length.
  - Open: Protective sleeve construction, thread forms and sealing seats remain unverified. Route is a candidate, not installed factory routing.
  - Open: Educational source-compared interface study, not factory dimensions. Plenum size and cap/throttle/EGR stations are inferred.
  - Open: Cap and matching neck use assumed4.5mm pitch; production thread dimensions and formed-versus-insert neck construction remain unknown.
  - Open: Nominal seal and hose contact do not establish compression, leak tightness, retention strength or production tolerance.
  - Open: Casting ribs, bosses and detailed wall distribution remain incomplete.
- [ ] **EGR tube protective sleeve** — `egr-tube-heat-sleeve`; modeled quantity **1**; provisional.
  - Instances: `egr-tube-heat-sleeve`
  - Source IDs: dorman-598-105, efi-intake-drawing, upper-intake-topology-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Tube OD is from the applicable replacement catalog; wall thickness, bend coordinates and fitting dimensions are provisional.
  - Open: The published 17.9 inch length has no measurement definition and is not treated as a verified developed centerline length.
  - Open: Protective sleeve construction, thread forms and sealing seats remain unverified. Route is a candidate, not installed factory routing.
  - Open: Educational source-compared interface study, not factory dimensions. Plenum size and cap/throttle/EGR stations are inferred.
  - Open: Cap and matching neck use assumed4.5mm pitch; production thread dimensions and formed-versus-insert neck construction remain unknown.
  - Open: Nominal seal and hose contact do not establish compression, leak tightness, retention strength or production tolerance.
  - Open: Casting ribs, bosses and detailed wall distribution remain incomplete.
- [ ] **EGR tube valve union nut** — `egr-tube-valve-nut`; modeled quantity **1**; provisional.
  - Instances: `egr-tube-valve-nut`
  - Source IDs: dorman-598-105, efi-intake-drawing, upper-intake-topology-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Tube OD is from the applicable replacement catalog; wall thickness, bend coordinates and fitting dimensions are provisional.
  - Open: The published 17.9 inch length has no measurement definition and is not treated as a verified developed centerline length.
  - Open: Protective sleeve construction, thread forms and sealing seats remain unverified. Route is a candidate, not installed factory routing.
  - Open: Educational source-compared interface study, not factory dimensions. Plenum size and cap/throttle/EGR stations are inferred.
  - Open: Cap and matching neck use assumed4.5mm pitch; production thread dimensions and formed-versus-insert neck construction remain unknown.
  - Open: Nominal seal and hose contact do not establish compression, leak tightness, retention strength or production tolerance.
  - Open: Casting ribs, bosses and detailed wall distribution remain incomplete.

## Additional known scope and reconciliation

- [ ] Fixed exhaust fitting and moved valve now have a connected estimated tube and sleeve route; verify production bends, fitting threads and catalog length convention
- [ ] Nominal contact checks are geometric only; hot behavior, sealing and assembly procedure remain unverified

## Cross-system boundaries

Coordinate with [#7](https://github.com/0xZakk/truck/issues/7), [#9](https://github.com/0xZakk/truck/issues/9). Keep the current engine-mounted component here; agree ownership before adding its vehicle-side continuation.

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
