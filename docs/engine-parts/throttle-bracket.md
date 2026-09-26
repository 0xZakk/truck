# Throttle cable bracket

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#16](https://github.com/0xZakk/truck/issues/16).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `4f98bbdad7fb1996487d17c4a651de588cef39254efe24e96384375dbdce0c07`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Throttle bracket mounting stud · estimated envelope** — `throttle-bracket-stud-estimated`; modeled quantity **2**; provisional.
  - Instances: `throttle-stud-3`, `throttle-stud-4`
  - Source IDs: pilot-throttle-bracket-factory, pilot-throttle-bracket-photo. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Photo-informed teaching candidate only; every bracket dimension and installed handedness is assumed. Exact 1994 manual-transmission variant is unconfirmed.
  - Open: Preserves accepted stud axes. Educational stack requires positive-Y nuts shifted +2 mm X and explicitly inferred 34 mm stud envelopes centered X373. Threads, material and installed anchorage remain unverified.
  - Open: Sharp bend intersections replace production bend radii; cable clips, linkage, load strength and motion sweep are not validated.
- [ ] **Accelerator cable bracket · estimated** — `accelerator-cable-bracket`; modeled quantity **1**; provisional.
  - Instances: `accelerator-cable-bracket`
  - Source IDs: pilot-throttle-bracket-factory, pilot-throttle-bracket-photo, throttle-1994-linkage-study, throttle-return-spring-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: One illustrative torsion spring explains fixed/moving anchors; actual Ford spring count, tang construction, dimensions and stops remain unverified.
  - Open: Wire motion preserves geometric length; no preload, spring rate, stress, fatigue, friction or guaranteed return force is simulated.
  - Open: Cable-end compression spring is a separate factory-documented component and is not represented by this torsion spring.
  - Open: Bracket and lever anchor holes, wire diameter and retention hooks are inferred; attachment strength and installation flexure are unverified.

## Additional known scope and reconciliation

- [ ] Bracket and two longer smooth stud envelopes are provisionally installed with seated nuts; factory bracket variant, shape and stud dimensions remain unverified
- [ ] Resolve actual threads, engagement strength and intake anchorage; nominal nut coverage is not thread verification
- [ ] Cable retainers/attachment fit, cable routing, return spring and complete linkage motion require reconstruction

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
