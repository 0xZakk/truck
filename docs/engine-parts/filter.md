# Oil filter, mounting insert and gallery interface

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#75](https://github.com/0xZakk/truck/issues/75).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `f1dc26ba64eb0ba1e8fede4ef42e23a5ae3e288dbeae3cc4b2558cf4148a4a70`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Oil filter steel case** — `oil-filter-case`; modeled quantity **1**; provisional.
  - Instances: `oil-filter-case`
  - Source IDs: system-8b605c7dd171, fsm-d975f341ee63, fsm-6f023139b5f8, wix-51515-envelope, motorcraft-filter-construction, ford-industrial-csg649, enginequest-oil-filter-adapter. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: This is a construction study, not a verified FL-1A or WIX51515 internal replica. The 93mm diameter/132mm overall envelope and72/63/5mm gasket use WIX published metric comparison dimensions; the truck factory specifies FL-1A.
  - Open: Pleat count, wall thicknesses, internal seats, valve parts and spring geometry are illustrative. No oil flow, filtering efficiency, bypass pressure or seal compression is simulated.
  - Open: The insert is a hollow stepped comparison envelope, not a reconstructed E4TZ-6890-A anti-drainback service insert. No unsourced valve mechanism is added.
  - Open: Filter position, inclined boss, gallery routing, insert lengths, block-end thread diameter and sealing lands are provisional. Filter-side 3/4-16 uses coincident nominal male/female envelopes, not helical thread contact.
  - Open: Two deliberately open side interfaces bound this gallery study. They are not production external ports and remain disconnected from the pump and main oil gallery. The engine lubrication circuit is incomplete.
  - Open: No separate adapter gasket or additional bypass valve is inferred. The existing filter gasket, internal flap and illustrative bypass remain separate components; seal compression and anti-drainback performance are not simulated.
- [ ] **Oil filter baseplate** — `oil-filter-baseplate`; modeled quantity **1**; provisional.
  - Instances: `oil-filter-baseplate`
  - Source IDs: system-8b605c7dd171, fsm-d975f341ee63, fsm-6f023139b5f8, wix-51515-envelope, motorcraft-filter-construction, ford-industrial-csg649, enginequest-oil-filter-adapter. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: This is a construction study, not a verified FL-1A or WIX51515 internal replica. The 93mm diameter/132mm overall envelope and72/63/5mm gasket use WIX published metric comparison dimensions; the truck factory specifies FL-1A.
  - Open: Pleat count, wall thicknesses, internal seats, valve parts and spring geometry are illustrative. No oil flow, filtering efficiency, bypass pressure or seal compression is simulated.
  - Open: The insert is a hollow stepped comparison envelope, not a reconstructed E4TZ-6890-A anti-drainback service insert. No unsourced valve mechanism is added.
  - Open: Filter position, inclined boss, gallery routing, insert lengths, block-end thread diameter and sealing lands are provisional. Filter-side 3/4-16 uses coincident nominal male/female envelopes, not helical thread contact.
  - Open: Two deliberately open side interfaces bound this gallery study. They are not production external ports and remain disconnected from the pump and main oil gallery. The engine lubrication circuit is incomplete.
  - Open: No separate adapter gasket or additional bypass valve is inferred. The existing filter gasket, internal flap and illustrative bypass remain separate components; seal compression and anti-drainback performance are not simulated.
- [ ] **Oil filter mounting gasket** — `oil-filter-gasket`; modeled quantity **1**; provisional.
  - Instances: `oil-filter-gasket`
  - Source IDs: system-8b605c7dd171, fsm-d975f341ee63, fsm-6f023139b5f8, wix-51515-envelope, motorcraft-filter-construction, ford-industrial-csg649, enginequest-oil-filter-adapter. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: This is a construction study, not a verified FL-1A or WIX51515 internal replica. The 93mm diameter/132mm overall envelope and72/63/5mm gasket use WIX published metric comparison dimensions; the truck factory specifies FL-1A.
  - Open: Pleat count, wall thicknesses, internal seats, valve parts and spring geometry are illustrative. No oil flow, filtering efficiency, bypass pressure or seal compression is simulated.
  - Open: The insert is a hollow stepped comparison envelope, not a reconstructed E4TZ-6890-A anti-drainback service insert. No unsourced valve mechanism is added.
  - Open: Filter position, inclined boss, gallery routing, insert lengths, block-end thread diameter and sealing lands are provisional. Filter-side 3/4-16 uses coincident nominal male/female envelopes, not helical thread contact.
  - Open: Two deliberately open side interfaces bound this gallery study. They are not production external ports and remain disconnected from the pump and main oil gallery. The engine lubrication circuit is incomplete.
  - Open: No separate adapter gasket or additional bypass valve is inferred. The existing filter gasket, internal flap and illustrative bypass remain separate components; seal compression and anti-drainback performance are not simulated.
- [ ] **Oil filter anti-drainback valve** — `oil-filter-anti-drainback`; modeled quantity **1**; provisional.
  - Instances: `oil-filter-anti-drainback`
  - Source IDs: system-8b605c7dd171, fsm-d975f341ee63, fsm-6f023139b5f8, wix-51515-envelope, motorcraft-filter-construction, ford-industrial-csg649, enginequest-oil-filter-adapter. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: This is a construction study, not a verified FL-1A or WIX51515 internal replica. The 93mm diameter/132mm overall envelope and72/63/5mm gasket use WIX published metric comparison dimensions; the truck factory specifies FL-1A.
  - Open: Pleat count, wall thicknesses, internal seats, valve parts and spring geometry are illustrative. No oil flow, filtering efficiency, bypass pressure or seal compression is simulated.
  - Open: The insert is a hollow stepped comparison envelope, not a reconstructed E4TZ-6890-A anti-drainback service insert. No unsourced valve mechanism is added.
  - Open: Filter position, inclined boss, gallery routing, insert lengths, block-end thread diameter and sealing lands are provisional. Filter-side 3/4-16 uses coincident nominal male/female envelopes, not helical thread contact.
  - Open: Two deliberately open side interfaces bound this gallery study. They are not production external ports and remain disconnected from the pump and main oil gallery. The engine lubrication circuit is incomplete.
  - Open: No separate adapter gasket or additional bypass valve is inferred. The existing filter gasket, internal flap and illustrative bypass remain separate components; seal compression and anti-drainback performance are not simulated.
- [ ] **Pleated oil filter media** — `oil-filter-media`; modeled quantity **1**; provisional.
  - Instances: `oil-filter-media`
  - Source IDs: system-8b605c7dd171, fsm-d975f341ee63, fsm-6f023139b5f8, wix-51515-envelope, motorcraft-filter-construction, ford-industrial-csg649, enginequest-oil-filter-adapter. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: This is a construction study, not a verified FL-1A or WIX51515 internal replica. The 93mm diameter/132mm overall envelope and72/63/5mm gasket use WIX published metric comparison dimensions; the truck factory specifies FL-1A.
  - Open: Pleat count, wall thicknesses, internal seats, valve parts and spring geometry are illustrative. No oil flow, filtering efficiency, bypass pressure or seal compression is simulated.
  - Open: The insert is a hollow stepped comparison envelope, not a reconstructed E4TZ-6890-A anti-drainback service insert. No unsourced valve mechanism is added.
  - Open: Filter position, inclined boss, gallery routing, insert lengths, block-end thread diameter and sealing lands are provisional. Filter-side 3/4-16 uses coincident nominal male/female envelopes, not helical thread contact.
  - Open: Two deliberately open side interfaces bound this gallery study. They are not production external ports and remain disconnected from the pump and main oil gallery. The engine lubrication circuit is incomplete.
  - Open: No separate adapter gasket or additional bypass valve is inferred. The existing filter gasket, internal flap and illustrative bypass remain separate components; seal compression and anti-drainback performance are not simulated.
- [ ] **Oil filter perforated center tube** — `oil-filter-center-tube`; modeled quantity **1**; provisional.
  - Instances: `oil-filter-center-tube`
  - Source IDs: system-8b605c7dd171, fsm-d975f341ee63, fsm-6f023139b5f8, wix-51515-envelope, motorcraft-filter-construction, ford-industrial-csg649, enginequest-oil-filter-adapter. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: This is a construction study, not a verified FL-1A or WIX51515 internal replica. The 93mm diameter/132mm overall envelope and72/63/5mm gasket use WIX published metric comparison dimensions; the truck factory specifies FL-1A.
  - Open: Pleat count, wall thicknesses, internal seats, valve parts and spring geometry are illustrative. No oil flow, filtering efficiency, bypass pressure or seal compression is simulated.
  - Open: The insert is a hollow stepped comparison envelope, not a reconstructed E4TZ-6890-A anti-drainback service insert. No unsourced valve mechanism is added.
  - Open: Filter position, inclined boss, gallery routing, insert lengths, block-end thread diameter and sealing lands are provisional. Filter-side 3/4-16 uses coincident nominal male/female envelopes, not helical thread contact.
  - Open: Two deliberately open side interfaces bound this gallery study. They are not production external ports and remain disconnected from the pump and main oil gallery. The engine lubrication circuit is incomplete.
  - Open: No separate adapter gasket or additional bypass valve is inferred. The existing filter gasket, internal flap and illustrative bypass remain separate components; seal compression and anti-drainback performance are not simulated.
- [ ] **Oil filter inlet-side end cap** — `oil-filter-lower-endcap`; modeled quantity **1**; provisional.
  - Instances: `oil-filter-lower-endcap`
  - Source IDs: system-8b605c7dd171, fsm-d975f341ee63, fsm-6f023139b5f8, wix-51515-envelope, motorcraft-filter-construction, ford-industrial-csg649, enginequest-oil-filter-adapter. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: This is a construction study, not a verified FL-1A or WIX51515 internal replica. The 93mm diameter/132mm overall envelope and72/63/5mm gasket use WIX published metric comparison dimensions; the truck factory specifies FL-1A.
  - Open: Pleat count, wall thicknesses, internal seats, valve parts and spring geometry are illustrative. No oil flow, filtering efficiency, bypass pressure or seal compression is simulated.
  - Open: The insert is a hollow stepped comparison envelope, not a reconstructed E4TZ-6890-A anti-drainback service insert. No unsourced valve mechanism is added.
  - Open: Filter position, inclined boss, gallery routing, insert lengths, block-end thread diameter and sealing lands are provisional. Filter-side 3/4-16 uses coincident nominal male/female envelopes, not helical thread contact.
  - Open: Two deliberately open side interfaces bound this gallery study. They are not production external ports and remain disconnected from the pump and main oil gallery. The engine lubrication circuit is incomplete.
  - Open: No separate adapter gasket or additional bypass valve is inferred. The existing filter gasket, internal flap and illustrative bypass remain separate components; seal compression and anti-drainback performance are not simulated.
- [ ] **Oil filter closed-end end cap** — `oil-filter-upper-endcap`; modeled quantity **1**; provisional.
  - Instances: `oil-filter-upper-endcap`
  - Source IDs: system-8b605c7dd171, fsm-d975f341ee63, fsm-6f023139b5f8, wix-51515-envelope, motorcraft-filter-construction, ford-industrial-csg649, enginequest-oil-filter-adapter. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: This is a construction study, not a verified FL-1A or WIX51515 internal replica. The 93mm diameter/132mm overall envelope and72/63/5mm gasket use WIX published metric comparison dimensions; the truck factory specifies FL-1A.
  - Open: Pleat count, wall thicknesses, internal seats, valve parts and spring geometry are illustrative. No oil flow, filtering efficiency, bypass pressure or seal compression is simulated.
  - Open: The insert is a hollow stepped comparison envelope, not a reconstructed E4TZ-6890-A anti-drainback service insert. No unsourced valve mechanism is added.
  - Open: Filter position, inclined boss, gallery routing, insert lengths, block-end thread diameter and sealing lands are provisional. Filter-side 3/4-16 uses coincident nominal male/female envelopes, not helical thread contact.
  - Open: Two deliberately open side interfaces bound this gallery study. They are not production external ports and remain disconnected from the pump and main oil gallery. The engine lubrication circuit is incomplete.
  - Open: No separate adapter gasket or additional bypass valve is inferred. The existing filter gasket, internal flap and illustrative bypass remain separate components; seal compression and anti-drainback performance are not simulated.
- [ ] **Filter bypass housing and seat** — `oil-filter-bypass-housing`; modeled quantity **1**; provisional.
  - Instances: `oil-filter-bypass-housing`
  - Source IDs: system-8b605c7dd171, fsm-d975f341ee63, fsm-6f023139b5f8, wix-51515-envelope, motorcraft-filter-construction, ford-industrial-csg649, enginequest-oil-filter-adapter. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: This is a construction study, not a verified FL-1A or WIX51515 internal replica. The 93mm diameter/132mm overall envelope and72/63/5mm gasket use WIX published metric comparison dimensions; the truck factory specifies FL-1A.
  - Open: Pleat count, wall thicknesses, internal seats, valve parts and spring geometry are illustrative. No oil flow, filtering efficiency, bypass pressure or seal compression is simulated.
  - Open: The insert is a hollow stepped comparison envelope, not a reconstructed E4TZ-6890-A anti-drainback service insert. No unsourced valve mechanism is added.
  - Open: Filter position, inclined boss, gallery routing, insert lengths, block-end thread diameter and sealing lands are provisional. Filter-side 3/4-16 uses coincident nominal male/female envelopes, not helical thread contact.
  - Open: Two deliberately open side interfaces bound this gallery study. They are not production external ports and remain disconnected from the pump and main oil gallery. The engine lubrication circuit is incomplete.
  - Open: No separate adapter gasket or additional bypass valve is inferred. The existing filter gasket, internal flap and illustrative bypass remain separate components; seal compression and anti-drainback performance are not simulated.
- [ ] **Filter bypass valve disc** — `oil-filter-bypass-poppet`; modeled quantity **1**; provisional.
  - Instances: `oil-filter-bypass-poppet`
  - Source IDs: system-8b605c7dd171, fsm-d975f341ee63, fsm-6f023139b5f8, wix-51515-envelope, motorcraft-filter-construction, ford-industrial-csg649, enginequest-oil-filter-adapter. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: This is a construction study, not a verified FL-1A or WIX51515 internal replica. The 93mm diameter/132mm overall envelope and72/63/5mm gasket use WIX published metric comparison dimensions; the truck factory specifies FL-1A.
  - Open: Pleat count, wall thicknesses, internal seats, valve parts and spring geometry are illustrative. No oil flow, filtering efficiency, bypass pressure or seal compression is simulated.
  - Open: The insert is a hollow stepped comparison envelope, not a reconstructed E4TZ-6890-A anti-drainback service insert. No unsourced valve mechanism is added.
  - Open: Filter position, inclined boss, gallery routing, insert lengths, block-end thread diameter and sealing lands are provisional. Filter-side 3/4-16 uses coincident nominal male/female envelopes, not helical thread contact.
  - Open: Two deliberately open side interfaces bound this gallery study. They are not production external ports and remain disconnected from the pump and main oil gallery. The engine lubrication circuit is incomplete.
  - Open: No separate adapter gasket or additional bypass valve is inferred. The existing filter gasket, internal flap and illustrative bypass remain separate components; seal compression and anti-drainback performance are not simulated.
- [ ] **Filter bypass valve spring** — `oil-filter-bypass-spring`; modeled quantity **1**; provisional.
  - Instances: `oil-filter-bypass-spring`
  - Source IDs: system-8b605c7dd171, fsm-d975f341ee63, fsm-6f023139b5f8, wix-51515-envelope, motorcraft-filter-construction, ford-industrial-csg649, enginequest-oil-filter-adapter. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: This is a construction study, not a verified FL-1A or WIX51515 internal replica. The 93mm diameter/132mm overall envelope and72/63/5mm gasket use WIX published metric comparison dimensions; the truck factory specifies FL-1A.
  - Open: Pleat count, wall thicknesses, internal seats, valve parts and spring geometry are illustrative. No oil flow, filtering efficiency, bypass pressure or seal compression is simulated.
  - Open: The insert is a hollow stepped comparison envelope, not a reconstructed E4TZ-6890-A anti-drainback service insert. No unsourced valve mechanism is added.
  - Open: Filter position, inclined boss, gallery routing, insert lengths, block-end thread diameter and sealing lands are provisional. Filter-side 3/4-16 uses coincident nominal male/female envelopes, not helical thread contact.
  - Open: Two deliberately open side interfaces bound this gallery study. They are not production external ports and remain disconnected from the pump and main oil gallery. The engine lubrication circuit is incomplete.
  - Open: No separate adapter gasket or additional bypass valve is inferred. The existing filter gasket, internal flap and illustrative bypass remain separate components; seal compression and anti-drainback performance are not simulated.
- [ ] **Filter bypass spring retainer** — `oil-filter-bypass-retainer`; modeled quantity **1**; provisional.
  - Instances: `oil-filter-bypass-retainer`
  - Source IDs: system-8b605c7dd171, fsm-d975f341ee63, fsm-6f023139b5f8, wix-51515-envelope, motorcraft-filter-construction, ford-industrial-csg649, enginequest-oil-filter-adapter. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: This is a construction study, not a verified FL-1A or WIX51515 internal replica. The 93mm diameter/132mm overall envelope and72/63/5mm gasket use WIX published metric comparison dimensions; the truck factory specifies FL-1A.
  - Open: Pleat count, wall thicknesses, internal seats, valve parts and spring geometry are illustrative. No oil flow, filtering efficiency, bypass pressure or seal compression is simulated.
  - Open: The insert is a hollow stepped comparison envelope, not a reconstructed E4TZ-6890-A anti-drainback service insert. No unsourced valve mechanism is added.
  - Open: Filter position, inclined boss, gallery routing, insert lengths, block-end thread diameter and sealing lands are provisional. Filter-side 3/4-16 uses coincident nominal male/female envelopes, not helical thread contact.
  - Open: Two deliberately open side interfaces bound this gallery study. They are not production external ports and remain disconnected from the pump and main oil gallery. The engine lubrication circuit is incomplete.
  - Open: No separate adapter gasket or additional bypass valve is inferred. The existing filter gasket, internal flap and illustrative bypass remain separate components; seal compression and anti-drainback performance are not simulated.
- [ ] **Filter element tension clip** — `oil-filter-tension-clip`; modeled quantity **1**; provisional.
  - Instances: `oil-filter-tension-clip`
  - Source IDs: system-8b605c7dd171, fsm-d975f341ee63, fsm-6f023139b5f8, wix-51515-envelope, motorcraft-filter-construction, ford-industrial-csg649, enginequest-oil-filter-adapter. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: This is a construction study, not a verified FL-1A or WIX51515 internal replica. The 93mm diameter/132mm overall envelope and72/63/5mm gasket use WIX published metric comparison dimensions; the truck factory specifies FL-1A.
  - Open: Pleat count, wall thicknesses, internal seats, valve parts and spring geometry are illustrative. No oil flow, filtering efficiency, bypass pressure or seal compression is simulated.
  - Open: The insert is a hollow stepped comparison envelope, not a reconstructed E4TZ-6890-A anti-drainback service insert. No unsourced valve mechanism is added.
  - Open: Filter position, inclined boss, gallery routing, insert lengths, block-end thread diameter and sealing lands are provisional. Filter-side 3/4-16 uses coincident nominal male/female envelopes, not helical thread contact.
  - Open: Two deliberately open side interfaces bound this gallery study. They are not production external ports and remain disconnected from the pump and main oil gallery. The engine lubrication circuit is incomplete.
  - Open: No separate adapter gasket or additional bypass valve is inferred. The existing filter gasket, internal flap and illustrative bypass remain separate components; seal compression and anti-drainback performance are not simulated.
- [ ] **Hollow oil filter mounting insert · comparison study** — `oil-filter-mounting-insert`; modeled quantity **1**; provisional.
  - Instances: `oil-filter-mounting-insert`
  - Source IDs: fsm-d975f341ee63, fsm-6f023139b5f8, ford-industrial-csg649, wix-51515-envelope, enginequest-oil-filter-adapter. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The insert is a hollow stepped comparison envelope, not a reconstructed E4TZ-6890-A anti-drainback service insert. No unsourced valve mechanism is added.
  - Open: Filter position, inclined boss, gallery routing, insert lengths, block-end thread diameter and sealing lands are provisional. Filter-side 3/4-16 uses coincident nominal male/female envelopes, not helical thread contact.
  - Open: Two deliberately open side interfaces bound this gallery study. They are not production external ports and remain disconnected from the pump and main oil gallery. The engine lubrication circuit is incomplete.
  - Open: No separate adapter gasket or additional bypass valve is inferred. The existing filter gasket, internal flap and illustrative bypass remain separate components; seal compression and anti-drainback performance are not simulated.

## Additional known scope and reconciliation

- [ ] E4TZ anti-drainback service insert: identify construction and applicability
- [ ] Verify separate inlet/return galleries and internal filter construction

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
