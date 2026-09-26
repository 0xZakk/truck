# Engine oil dipstick

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#17](https://github.com/0xZakk/truck/issues/17).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `f725260d8f1497a1b6f2aed9d41d01155bf2a82e7391d24ce866f352bb50cd5b`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- No accepted installed definitions are mapped to this package; candidate artifacts may exist as noted below.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.


## Separate candidate parts (not installed)

- [ ] **Dipstick blade and handle/stop** — `engine-oil-dipstick`; Candidate only; fit/identity not accepted. Source: `cad/engine/pilot/dipstick/dipstick.py`.

## Additional known scope and reconciliation

- [ ] Candidate blade/handle exists
- [ ] Trial installed routing intersects block
- [ ] Oil-level markings/calibration and matched tube remain unresolved

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
