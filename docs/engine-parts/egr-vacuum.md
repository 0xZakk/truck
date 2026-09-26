# EGR vacuum hoses and supports

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#60](https://github.com/0xZakk/truck/issues/60).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `bfab1f2596991d27fe5e52e90f02d070eb034f9de8c2cd72d3dd44666d6c8bb9`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **EGR controlled-vacuum hose** — `egr-control-vacuum-hose`; modeled quantity **1**; provisional.
  - Instances: `egr-control-vacuum-hose`
  - Source IDs: ford-evr-factory, truck-egr-evtm. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Routing, hose material, wall thickness and diameters are provisional; this smooth reducing envelope connects the current provisional nipples.
  - Open: No production hose identity, molded end geometry, hose compression or vacuum-flow simulation is established. Source-vacuum plumbing and retainers remain unfinished.

## Additional known scope and reconciliation

- [ ] Complete manifold supply/regulator/actuator vacuum route
- [ ] Hose ends, clips and routing supports

## Cross-system boundaries

Coordinate with [#7](https://github.com/0xZakk/truck/issues/7). Keep the current engine-mounted component here; agree ownership before adding its vehicle-side continuation.

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
