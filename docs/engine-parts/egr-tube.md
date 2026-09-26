# EGR exhaust tube and connections

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#59](https://github.com/0xZakk/truck/issues/59).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `bfab1f2596991d27fe5e52e90f02d070eb034f9de8c2cd72d3dd44666d6c8bb9`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **EGR exhaust tube** — `egr-exhaust-tube`; modeled quantity **1**; provisional.
  - Instances: `egr-exhaust-tube`
  - Source IDs: dorman-598-105, efi-intake-drawing. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Tube OD is from the applicable replacement catalog; wall thickness, bend coordinates and fitting dimensions are provisional.
  - Open: The published 17.9 inch length has no measurement definition and is not treated as a verified developed centerline length.
  - Open: Protective sleeve construction, thread forms and sealing seats remain unverified. Route is a candidate, not installed factory routing.
- [ ] **EGR tube protective sleeve** — `egr-tube-heat-sleeve`; modeled quantity **1**; provisional.
  - Instances: `egr-tube-heat-sleeve`
  - Source IDs: dorman-598-105, efi-intake-drawing. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Tube OD is from the applicable replacement catalog; wall thickness, bend coordinates and fitting dimensions are provisional.
  - Open: The published 17.9 inch length has no measurement definition and is not treated as a verified developed centerline length.
  - Open: Protective sleeve construction, thread forms and sealing seats remain unverified. Route is a candidate, not installed factory routing.
- [ ] **EGR tube valve union nut** — `egr-tube-valve-nut`; modeled quantity **1**; provisional.
  - Instances: `egr-tube-valve-nut`
  - Source IDs: dorman-598-105, efi-intake-drawing. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Tube OD is from the applicable replacement catalog; wall thickness, bend coordinates and fitting dimensions are provisional.
  - Open: The published 17.9 inch length has no measurement definition and is not treated as a verified developed centerline length.
  - Open: Protective sleeve construction, thread forms and sealing seats remain unverified. Route is a candidate, not installed factory routing.
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

## Additional known scope and reconciliation

- [ ] Verify takeoff location, seats/threads, hot routing and heat sleeve

## Cross-system boundaries

Coordinate with [#7](https://github.com/0xZakk/truck/issues/7), [#9](https://github.com/0xZakk/truck/issues/9). Keep the current engine-mounted component here; agree ownership before adding its vehicle-side continuation.

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
