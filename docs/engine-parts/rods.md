# Connecting rods, caps, bearings and hardware

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#22](https://github.com/0xZakk/truck/issues/22).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `f1dc26ba64eb0ba1e8fede4ef42e23a5ae3e288dbeae3cc4b2558cf4148a4a70`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Connecting rod** — `rod`; modeled quantity **6**; provisional.
  - Instances: `c1-connecting-rod-1`, `c2-connecting-rod-1`, `c3-connecting-rod-1`, `c4-connecting-rod-1`, `c5-connecting-rod-1`, `c6-connecting-rod-1`
  - Source IDs: fsm-2e5473b2bf99, silvolite-1186, hastings-592. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Inherited piston-study assumptions; exact forging, ring profiles, pin offset and fastener threads remain unresolved.
- [ ] **Rod cap** — `rod-cap`; modeled quantity **6**; provisional.
  - Instances: `c1-rod-cap-1`, `c2-rod-cap-1`, `c3-rod-cap-1`, `c4-rod-cap-1`, `c5-rod-cap-1`, `c6-rod-cap-1`
  - Source IDs: fsm-2e5473b2bf99, silvolite-1186, hastings-592. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Inherited piston-study assumptions; exact forging, ring profiles, pin offset and fastener threads remain unresolved.
- [ ] **Upper bearing shell** — `upper-bearing`; modeled quantity **6**; provisional.
  - Instances: `c1-rod-bearing-upper-1`, `c2-rod-bearing-upper-1`, `c3-rod-bearing-upper-1`, `c4-rod-bearing-upper-1`, `c5-rod-bearing-upper-1`, `c6-rod-bearing-upper-1`
  - Source IDs: fsm-2e5473b2bf99, silvolite-1186, hastings-592. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Inherited piston-study assumptions; exact forging, ring profiles, pin offset and fastener threads remain unresolved.
- [ ] **Lower bearing shell** — `lower-bearing`; modeled quantity **6**; provisional.
  - Instances: `c1-rod-bearing-lower-1`, `c2-rod-bearing-lower-1`, `c3-rod-bearing-lower-1`, `c4-rod-bearing-lower-1`, `c5-rod-bearing-lower-1`, `c6-rod-bearing-lower-1`
  - Source IDs: fsm-2e5473b2bf99, silvolite-1186, hastings-592. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Inherited piston-study assumptions; exact forging, ring profiles, pin offset and fastener threads remain unresolved.
- [ ] **Rod bolt 1** — `rod-bolt`; modeled quantity **12**; provisional.
  - Instances: `c1-rod-bolt-1`, `c1-rod-bolt-2`, `c2-rod-bolt-1`, `c2-rod-bolt-2`, `c3-rod-bolt-1`, `c3-rod-bolt-2`, `c4-rod-bolt-1`, `c4-rod-bolt-2`, `c5-rod-bolt-1`, `c5-rod-bolt-2`, `c6-rod-bolt-1`, `c6-rod-bolt-2`
  - Source IDs: fsm-2e5473b2bf99, silvolite-1186, hastings-592. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Inherited piston-study assumptions; exact forging, ring profiles, pin offset and fastener threads remain unresolved.
- [ ] **Rod nut 1** — `rod-nut`; modeled quantity **12**; provisional.
  - Instances: `c1-rod-nut-1`, `c1-rod-nut-2`, `c2-rod-nut-1`, `c2-rod-nut-2`, `c3-rod-nut-1`, `c3-rod-nut-2`, `c4-rod-nut-1`, `c4-rod-nut-2`, `c5-rod-nut-1`, `c5-rod-nut-2`, `c6-rod-nut-1`, `c6-rod-nut-2`
  - Source IDs: fsm-2e5473b2bf99, silvolite-1186, hastings-592. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Inherited piston-study assumptions; exact forging, ring profiles, pin offset and fastener threads remain unresolved.

## Additional known scope and reconciliation

- [ ] Verify rod length and production forging
- [ ] Verify bearing tangs, crush, oil clearances and fastener threads

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
