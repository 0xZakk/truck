# Oil filler cap and seal

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#15](https://github.com/0xZakk/truck/issues/15).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `bfab1f2596991d27fe5e52e90f02d070eb034f9de8c2cd72d3dd44666d6c8bb9`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Oil filler cap** — `oil-filler-cap`; modeled quantity **1**; provisional.
  - Instances: `oil-filler-cap`
  - Source IDs: not recorded. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact production contours, dimensions and tolerances need applicable drawings or measurements.

## Separate candidate parts (not installed)

- [ ] **Replacement cap body** — `oil-filler-cap`; Candidate only; fit/identity not accepted. Source: `cad/engine/pilot/oil-cap/oil_cap.py`.
- [ ] **Separate filler-cap seal** — `oil-filler-cap-seal`; Candidate only; fit/identity not accepted. Source: `cad/engine/pilot/oil-cap/oil_cap.py`.

## Additional known scope and reconciliation

- [ ] Candidate male thread and separate seal exist
- [ ] Matching female neck retention is missing
- [ ] Dynamic rocker clearance and production cap dimensions unverified

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
