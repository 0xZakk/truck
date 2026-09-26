# Throttle cable bracket

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#16](https://github.com/0xZakk/truck/issues/16).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `f725260d8f1497a1b6f2aed9d41d01155bf2a82e7391d24ce866f352bb50cd5b`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Accelerator cable mounting bracket** — `accelerator-cable-bracket`; modeled quantity **1**; provisional.
  - Instances: `accelerator-cable-bracket`
  - Source IDs: pilot-throttle-bracket-factory, pilot-throttle-bracket-photo. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Photo-informed teaching candidate only; every bracket dimension and installed handedness is assumed. Exact 1994 manual-transmission variant is unconfirmed.
  - Open: Preserves accepted stud axes. Educational stack requires positive-Y nuts shifted +2 mm X and explicitly inferred 34 mm stud envelopes centered X373. Threads, material and installed anchorage remain unverified.
  - Open: Sharp bend intersections replace production bend radii; cable clips, linkage, load strength and motion sweep are not validated.
- [ ] **Throttle bracket mounting stud · estimated envelope** — `throttle-bracket-stud-estimated`; modeled quantity **2**; provisional.
  - Instances: `throttle-stud-3`, `throttle-stud-4`
  - Source IDs: pilot-throttle-bracket-factory, pilot-throttle-bracket-photo. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Photo-informed teaching candidate only; every bracket dimension and installed handedness is assumed. Exact 1994 manual-transmission variant is unconfirmed.
  - Open: Preserves accepted stud axes. Educational stack requires positive-Y nuts shifted +2 mm X and explicitly inferred 34 mm stud envelopes centered X373. Threads, material and installed anchorage remain unverified.
  - Open: Sharp bend intersections replace production bend radii; cable clips, linkage, load strength and motion sweep are not validated.

## Additional known scope and reconciliation

- [ ] Bracket and two longer smooth stud envelopes are provisionally installed with seated nuts; factory bracket variant, shape and stud dimensions remain unverified
- [ ] Resolve actual threads, engagement strength and intake anchorage; nominal nut coverage is not thread verification
- [ ] Cable retainers/attachment fit, cable routing, return spring and complete linkage motion require reconstruction

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
