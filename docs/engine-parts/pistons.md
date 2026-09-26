# Pistons, wrist pins and ring packs

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#21](https://github.com/0xZakk/truck/issues/21).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `0656841ba587a3f05d193aa75fb711f320ddf732cc0343c68504836c9ea7537d`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Piston** — `piston`; modeled quantity **6**; provisional.
  - Instances: `c1-piston-1`, `c2-piston-1`, `c3-piston-1`, `c4-piston-1`, `c5-piston-1`, `c6-piston-1`
  - Source IDs: fsm-2e5473b2bf99, silvolite-1186, hastings-592. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Inherited piston-study assumptions; exact forging, ring profiles, pin offset and fastener threads remain unresolved.
- [ ] **Wrist pin** — `pin`; modeled quantity **6**; provisional.
  - Instances: `c1-wrist-pin-1`, `c2-wrist-pin-1`, `c3-wrist-pin-1`, `c4-wrist-pin-1`, `c5-wrist-pin-1`, `c6-wrist-pin-1`
  - Source IDs: fsm-2e5473b2bf99, silvolite-1186, hastings-592. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Inherited piston-study assumptions; exact forging, ring profiles, pin offset and fastener threads remain unresolved.
- [ ] **Top compression ring** — `compression-ring`; modeled quantity **12**; provisional.
  - Instances: `c1-top-ring-1`, `c1-second-ring-1`, `c2-top-ring-1`, `c2-second-ring-1`, `c3-top-ring-1`, `c3-second-ring-1`, `c4-top-ring-1`, `c4-second-ring-1`, `c5-top-ring-1`, `c5-second-ring-1`, `c6-top-ring-1`, `c6-second-ring-1`
  - Source IDs: fsm-2e5473b2bf99, silvolite-1186, hastings-592. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Inherited piston-study assumptions; exact forging, ring profiles, pin offset and fastener threads remain unresolved.
- [ ] **Oil-control rail 1** — `oil-rail`; modeled quantity **12**; provisional.
  - Instances: `c1-oil-rail-1`, `c1-oil-rail-2`, `c2-oil-rail-1`, `c2-oil-rail-2`, `c3-oil-rail-1`, `c3-oil-rail-2`, `c4-oil-rail-1`, `c4-oil-rail-2`, `c5-oil-rail-1`, `c5-oil-rail-2`, `c6-oil-rail-1`, `c6-oil-rail-2`
  - Source IDs: fsm-2e5473b2bf99, silvolite-1186, hastings-592. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Inherited piston-study assumptions; exact forging, ring profiles, pin offset and fastener threads remain unresolved.
- [ ] **Oil-ring expander** — `oil-expander`; modeled quantity **6**; provisional.
  - Instances: `c1-oil-expander-1`, `c2-oil-expander-1`, `c3-oil-expander-1`, `c4-oil-expander-1`, `c5-oil-expander-1`, `c6-oil-expander-1`
  - Source IDs: fsm-2e5473b2bf99, silvolite-1186, hastings-592. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Inherited piston-study assumptions; exact forging, ring profiles, pin offset and fastener threads remain unresolved.

## Additional known scope and reconciliation

- [ ] Verify second compression-ring section and identity
- [ ] Verify pin retention construction and offset
- [ ] Verify piston skirt, dish and ring profiles

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
