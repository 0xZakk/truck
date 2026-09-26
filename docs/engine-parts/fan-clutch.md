# Fan clutch and cooling fan

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#70](https://github.com/0xZakk/truck/issues/70).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `4f98bbdad7fb1996487d17c4a651de588cef39254efe24e96384375dbdce0c07`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Fan clutch input shaft and nut** — `fan-clutch-input-shaft`; modeled quantity **1**; provisional.
  - Instances: `fan-clutch-input-shaft`
  - Source IDs: system-7b01cf423275, imperial-fan-clutch-215161, hayden-fan-clutch-operation, dorman-620-151. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Imperial lists both 215161 (36 mm hex, M30x1.5 RH) and 215155 (40 mm hex, M33x1.5 RH) for 1994 F-Series 4.9L. This is the 215161 comparison branch; installed nut size is unknown.
  - Open: Catalog dimensions constrain clutch OD, overall height, fan mount height, fan pilot and four-hole bolt circle. Housing sections, bearing, seals, shear lands, reservoir, valve and spring are educational assumptions, not a production teardown.
  - Open: Dorman 620-151 supplies a seven-blade, 18.9 inch black stamped-steel comparison and F2UZ8600A cross-reference. Exact 4.9L vehicle fit is not independently established by the saved primary application table; installed fan identity remains unverified.
  - Open: Blade chord, pitch, twist, angular spacing, root shape, spider, fourteen rivets and all sheet thicknesses are provisional interpretations of the manufacturer photo. No airflow, stress, balance or fan-speed simulation.
  - Open: Pump nose extension, pulley bore and axial seating at X530 are provisional interface reconciliation. Thread nominal size and right-hand direction are sourced; the model uses smooth clearance envelopes rather than thread helices.
  - Open: Fan bolts use sourced 5/16-18 nominal diameter and four-hole count; length, head dimensions, thread engagement and hole angular index are provisional. Radiator/shroud clearance is not established.
  - Open: Silicone fluid and its dynamic fill fraction are described rather than represented as rigid solids. The sealed clutch is not a user-serviceable exploded repair procedure.
- [ ] **Fan clutch output housing** — `fan-clutch-housing`; modeled quantity **1**; provisional.
  - Instances: `fan-clutch-housing`
  - Source IDs: system-7b01cf423275, imperial-fan-clutch-215161, hayden-fan-clutch-operation, dorman-620-151. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Imperial lists both 215161 (36 mm hex, M30x1.5 RH) and 215155 (40 mm hex, M33x1.5 RH) for 1994 F-Series 4.9L. This is the 215161 comparison branch; installed nut size is unknown.
  - Open: Catalog dimensions constrain clutch OD, overall height, fan mount height, fan pilot and four-hole bolt circle. Housing sections, bearing, seals, shear lands, reservoir, valve and spring are educational assumptions, not a production teardown.
  - Open: Dorman 620-151 supplies a seven-blade, 18.9 inch black stamped-steel comparison and F2UZ8600A cross-reference. Exact 4.9L vehicle fit is not independently established by the saved primary application table; installed fan identity remains unverified.
  - Open: Blade chord, pitch, twist, angular spacing, root shape, spider, fourteen rivets and all sheet thicknesses are provisional interpretations of the manufacturer photo. No airflow, stress, balance or fan-speed simulation.
  - Open: Pump nose extension, pulley bore and axial seating at X530 are provisional interface reconciliation. Thread nominal size and right-hand direction are sourced; the model uses smooth clearance envelopes rather than thread helices.
  - Open: Fan bolts use sourced 5/16-18 nominal diameter and four-hole count; length, head dimensions, thread engagement and hole angular index are provisional. Radiator/shroud clearance is not established.
  - Open: Silicone fluid and its dynamic fill fraction are described rather than represented as rigid solids. The sealed clutch is not a user-serviceable exploded repair procedure.
- [ ] **Fan clutch bearing · cartridge** — `fan-clutch-bearing`; modeled quantity **1**; provisional.
  - Instances: `fan-clutch-bearing`
  - Source IDs: system-7b01cf423275, imperial-fan-clutch-215161, hayden-fan-clutch-operation, dorman-620-151. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Imperial lists both 215161 (36 mm hex, M30x1.5 RH) and 215155 (40 mm hex, M33x1.5 RH) for 1994 F-Series 4.9L. This is the 215161 comparison branch; installed nut size is unknown.
  - Open: Catalog dimensions constrain clutch OD, overall height, fan mount height, fan pilot and four-hole bolt circle. Housing sections, bearing, seals, shear lands, reservoir, valve and spring are educational assumptions, not a production teardown.
  - Open: Dorman 620-151 supplies a seven-blade, 18.9 inch black stamped-steel comparison and F2UZ8600A cross-reference. Exact 4.9L vehicle fit is not independently established by the saved primary application table; installed fan identity remains unverified.
  - Open: Blade chord, pitch, twist, angular spacing, root shape, spider, fourteen rivets and all sheet thicknesses are provisional interpretations of the manufacturer photo. No airflow, stress, balance or fan-speed simulation.
  - Open: Pump nose extension, pulley bore and axial seating at X530 are provisional interface reconciliation. Thread nominal size and right-hand direction are sourced; the model uses smooth clearance envelopes rather than thread helices.
  - Open: Fan bolts use sourced 5/16-18 nominal diameter and four-hole count; length, head dimensions, thread engagement and hole angular index are provisional. Radiator/shroud clearance is not established.
  - Open: Silicone fluid and its dynamic fill fraction are described rather than represented as rigid solids. The sealed clutch is not a user-serviceable exploded repair procedure.
- [ ] **Fan clutch shaft seal · envelope** — `fan-clutch-shaft-seal`; modeled quantity **1**; provisional.
  - Instances: `fan-clutch-shaft-seal`
  - Source IDs: system-7b01cf423275, imperial-fan-clutch-215161, hayden-fan-clutch-operation, dorman-620-151. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Imperial lists both 215161 (36 mm hex, M30x1.5 RH) and 215155 (40 mm hex, M33x1.5 RH) for 1994 F-Series 4.9L. This is the 215161 comparison branch; installed nut size is unknown.
  - Open: Catalog dimensions constrain clutch OD, overall height, fan mount height, fan pilot and four-hole bolt circle. Housing sections, bearing, seals, shear lands, reservoir, valve and spring are educational assumptions, not a production teardown.
  - Open: Dorman 620-151 supplies a seven-blade, 18.9 inch black stamped-steel comparison and F2UZ8600A cross-reference. Exact 4.9L vehicle fit is not independently established by the saved primary application table; installed fan identity remains unverified.
  - Open: Blade chord, pitch, twist, angular spacing, root shape, spider, fourteen rivets and all sheet thicknesses are provisional interpretations of the manufacturer photo. No airflow, stress, balance or fan-speed simulation.
  - Open: Pump nose extension, pulley bore and axial seating at X530 are provisional interface reconciliation. Thread nominal size and right-hand direction are sourced; the model uses smooth clearance envelopes rather than thread helices.
  - Open: Fan bolts use sourced 5/16-18 nominal diameter and four-hole count; length, head dimensions, thread engagement and hole angular index are provisional. Radiator/shroud clearance is not established.
  - Open: Silicone fluid and its dynamic fill fraction are described rather than represented as rigid solids. The sealed clutch is not a user-serviceable exploded repair procedure.
- [ ] **Fan clutch drive rotor** — `fan-clutch-drive-rotor`; modeled quantity **1**; provisional.
  - Instances: `fan-clutch-drive-rotor`
  - Source IDs: system-7b01cf423275, imperial-fan-clutch-215161, hayden-fan-clutch-operation, dorman-620-151. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Imperial lists both 215161 (36 mm hex, M30x1.5 RH) and 215155 (40 mm hex, M33x1.5 RH) for 1994 F-Series 4.9L. This is the 215161 comparison branch; installed nut size is unknown.
  - Open: Catalog dimensions constrain clutch OD, overall height, fan mount height, fan pilot and four-hole bolt circle. Housing sections, bearing, seals, shear lands, reservoir, valve and spring are educational assumptions, not a production teardown.
  - Open: Dorman 620-151 supplies a seven-blade, 18.9 inch black stamped-steel comparison and F2UZ8600A cross-reference. Exact 4.9L vehicle fit is not independently established by the saved primary application table; installed fan identity remains unverified.
  - Open: Blade chord, pitch, twist, angular spacing, root shape, spider, fourteen rivets and all sheet thicknesses are provisional interpretations of the manufacturer photo. No airflow, stress, balance or fan-speed simulation.
  - Open: Pump nose extension, pulley bore and axial seating at X530 are provisional interface reconciliation. Thread nominal size and right-hand direction are sourced; the model uses smooth clearance envelopes rather than thread helices.
  - Open: Fan bolts use sourced 5/16-18 nominal diameter and four-hole count; length, head dimensions, thread engagement and hole angular index are provisional. Radiator/shroud clearance is not established.
  - Open: Silicone fluid and its dynamic fill fraction are described rather than represented as rigid solids. The sealed clutch is not a user-serviceable exploded repair procedure.
- [ ] **Fan clutch reservoir partition** — `fan-clutch-reservoir-partition`; modeled quantity **1**; provisional.
  - Instances: `fan-clutch-reservoir-partition`
  - Source IDs: system-7b01cf423275, imperial-fan-clutch-215161, hayden-fan-clutch-operation, dorman-620-151. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Imperial lists both 215161 (36 mm hex, M30x1.5 RH) and 215155 (40 mm hex, M33x1.5 RH) for 1994 F-Series 4.9L. This is the 215161 comparison branch; installed nut size is unknown.
  - Open: Catalog dimensions constrain clutch OD, overall height, fan mount height, fan pilot and four-hole bolt circle. Housing sections, bearing, seals, shear lands, reservoir, valve and spring are educational assumptions, not a production teardown.
  - Open: Dorman 620-151 supplies a seven-blade, 18.9 inch black stamped-steel comparison and F2UZ8600A cross-reference. Exact 4.9L vehicle fit is not independently established by the saved primary application table; installed fan identity remains unverified.
  - Open: Blade chord, pitch, twist, angular spacing, root shape, spider, fourteen rivets and all sheet thicknesses are provisional interpretations of the manufacturer photo. No airflow, stress, balance or fan-speed simulation.
  - Open: Pump nose extension, pulley bore and axial seating at X530 are provisional interface reconciliation. Thread nominal size and right-hand direction are sourced; the model uses smooth clearance envelopes rather than thread helices.
  - Open: Fan bolts use sourced 5/16-18 nominal diameter and four-hole count; length, head dimensions, thread engagement and hole angular index are provisional. Radiator/shroud clearance is not established.
  - Open: Silicone fluid and its dynamic fill fraction are described rather than represented as rigid solids. The sealed clutch is not a user-serviceable exploded repair procedure.
- [ ] **Fan clutch finned front cover** — `fan-clutch-front-cover`; modeled quantity **1**; provisional.
  - Instances: `fan-clutch-front-cover`
  - Source IDs: system-7b01cf423275, imperial-fan-clutch-215161, hayden-fan-clutch-operation, dorman-620-151. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Imperial lists both 215161 (36 mm hex, M30x1.5 RH) and 215155 (40 mm hex, M33x1.5 RH) for 1994 F-Series 4.9L. This is the 215161 comparison branch; installed nut size is unknown.
  - Open: Catalog dimensions constrain clutch OD, overall height, fan mount height, fan pilot and four-hole bolt circle. Housing sections, bearing, seals, shear lands, reservoir, valve and spring are educational assumptions, not a production teardown.
  - Open: Dorman 620-151 supplies a seven-blade, 18.9 inch black stamped-steel comparison and F2UZ8600A cross-reference. Exact 4.9L vehicle fit is not independently established by the saved primary application table; installed fan identity remains unverified.
  - Open: Blade chord, pitch, twist, angular spacing, root shape, spider, fourteen rivets and all sheet thicknesses are provisional interpretations of the manufacturer photo. No airflow, stress, balance or fan-speed simulation.
  - Open: Pump nose extension, pulley bore and axial seating at X530 are provisional interface reconciliation. Thread nominal size and right-hand direction are sourced; the model uses smooth clearance envelopes rather than thread helices.
  - Open: Fan bolts use sourced 5/16-18 nominal diameter and four-hole count; length, head dimensions, thread engagement and hole angular index are provisional. Radiator/shroud clearance is not established.
  - Open: Silicone fluid and its dynamic fill fraction are described rather than represented as rigid solids. The sealed clutch is not a user-serviceable exploded repair procedure.
- [ ] **Fan clutch fluid-control valve** — `fan-clutch-control-valve`; modeled quantity **1**; provisional.
  - Instances: `fan-clutch-control-valve`
  - Source IDs: system-7b01cf423275, imperial-fan-clutch-215161, hayden-fan-clutch-operation, dorman-620-151. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Imperial lists both 215161 (36 mm hex, M30x1.5 RH) and 215155 (40 mm hex, M33x1.5 RH) for 1994 F-Series 4.9L. This is the 215161 comparison branch; installed nut size is unknown.
  - Open: Catalog dimensions constrain clutch OD, overall height, fan mount height, fan pilot and four-hole bolt circle. Housing sections, bearing, seals, shear lands, reservoir, valve and spring are educational assumptions, not a production teardown.
  - Open: Dorman 620-151 supplies a seven-blade, 18.9 inch black stamped-steel comparison and F2UZ8600A cross-reference. Exact 4.9L vehicle fit is not independently established by the saved primary application table; installed fan identity remains unverified.
  - Open: Blade chord, pitch, twist, angular spacing, root shape, spider, fourteen rivets and all sheet thicknesses are provisional interpretations of the manufacturer photo. No airflow, stress, balance or fan-speed simulation.
  - Open: Pump nose extension, pulley bore and axial seating at X530 are provisional interface reconciliation. Thread nominal size and right-hand direction are sourced; the model uses smooth clearance envelopes rather than thread helices.
  - Open: Fan bolts use sourced 5/16-18 nominal diameter and four-hole count; length, head dimensions, thread engagement and hole angular index are provisional. Radiator/shroud clearance is not established.
  - Open: Silicone fluid and its dynamic fill fraction are described rather than represented as rigid solids. The sealed clutch is not a user-serviceable exploded repair procedure.
- [ ] **Fan clutch bimetal spring** — `fan-clutch-thermal-spring`; modeled quantity **1**; provisional.
  - Instances: `fan-clutch-thermal-spring`
  - Source IDs: system-7b01cf423275, imperial-fan-clutch-215161, hayden-fan-clutch-operation, dorman-620-151. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Imperial lists both 215161 (36 mm hex, M30x1.5 RH) and 215155 (40 mm hex, M33x1.5 RH) for 1994 F-Series 4.9L. This is the 215161 comparison branch; installed nut size is unknown.
  - Open: Catalog dimensions constrain clutch OD, overall height, fan mount height, fan pilot and four-hole bolt circle. Housing sections, bearing, seals, shear lands, reservoir, valve and spring are educational assumptions, not a production teardown.
  - Open: Dorman 620-151 supplies a seven-blade, 18.9 inch black stamped-steel comparison and F2UZ8600A cross-reference. Exact 4.9L vehicle fit is not independently established by the saved primary application table; installed fan identity remains unverified.
  - Open: Blade chord, pitch, twist, angular spacing, root shape, spider, fourteen rivets and all sheet thicknesses are provisional interpretations of the manufacturer photo. No airflow, stress, balance or fan-speed simulation.
  - Open: Pump nose extension, pulley bore and axial seating at X530 are provisional interface reconciliation. Thread nominal size and right-hand direction are sourced; the model uses smooth clearance envelopes rather than thread helices.
  - Open: Fan bolts use sourced 5/16-18 nominal diameter and four-hole count; length, head dimensions, thread engagement and hole angular index are provisional. Radiator/shroud clearance is not established.
  - Open: Silicone fluid and its dynamic fill fraction are described rather than represented as rigid solids. The sealed clutch is not a user-serviceable exploded repair procedure.
- [ ] **Cooling fan mounting spider** — `cooling-fan-spider`; modeled quantity **1**; provisional.
  - Instances: `cooling-fan-spider`
  - Source IDs: system-7b01cf423275, imperial-fan-clutch-215161, hayden-fan-clutch-operation, dorman-620-151. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Imperial lists both 215161 (36 mm hex, M30x1.5 RH) and 215155 (40 mm hex, M33x1.5 RH) for 1994 F-Series 4.9L. This is the 215161 comparison branch; installed nut size is unknown.
  - Open: Catalog dimensions constrain clutch OD, overall height, fan mount height, fan pilot and four-hole bolt circle. Housing sections, bearing, seals, shear lands, reservoir, valve and spring are educational assumptions, not a production teardown.
  - Open: Dorman 620-151 supplies a seven-blade, 18.9 inch black stamped-steel comparison and F2UZ8600A cross-reference. Exact 4.9L vehicle fit is not independently established by the saved primary application table; installed fan identity remains unverified.
  - Open: Blade chord, pitch, twist, angular spacing, root shape, spider, fourteen rivets and all sheet thicknesses are provisional interpretations of the manufacturer photo. No airflow, stress, balance or fan-speed simulation.
  - Open: Pump nose extension, pulley bore and axial seating at X530 are provisional interface reconciliation. Thread nominal size and right-hand direction are sourced; the model uses smooth clearance envelopes rather than thread helices.
  - Open: Fan bolts use sourced 5/16-18 nominal diameter and four-hole count; length, head dimensions, thread engagement and hole angular index are provisional. Radiator/shroud clearance is not established.
  - Open: Silicone fluid and its dynamic fill fraction are described rather than represented as rigid solids. The sealed clutch is not a user-serviceable exploded repair procedure.
- [ ] **Cooling fan stamped blade** — `cooling-fan-blade`; modeled quantity **7**; provisional.
  - Instances: `cooling-fan-blade-1`, `cooling-fan-blade-2`, `cooling-fan-blade-3`, `cooling-fan-blade-4`, `cooling-fan-blade-5`, `cooling-fan-blade-6`, `cooling-fan-blade-7`
  - Source IDs: system-7b01cf423275, imperial-fan-clutch-215161, hayden-fan-clutch-operation, dorman-620-151. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Imperial lists both 215161 (36 mm hex, M30x1.5 RH) and 215155 (40 mm hex, M33x1.5 RH) for 1994 F-Series 4.9L. This is the 215161 comparison branch; installed nut size is unknown.
  - Open: Catalog dimensions constrain clutch OD, overall height, fan mount height, fan pilot and four-hole bolt circle. Housing sections, bearing, seals, shear lands, reservoir, valve and spring are educational assumptions, not a production teardown.
  - Open: Dorman 620-151 supplies a seven-blade, 18.9 inch black stamped-steel comparison and F2UZ8600A cross-reference. Exact 4.9L vehicle fit is not independently established by the saved primary application table; installed fan identity remains unverified.
  - Open: Blade chord, pitch, twist, angular spacing, root shape, spider, fourteen rivets and all sheet thicknesses are provisional interpretations of the manufacturer photo. No airflow, stress, balance or fan-speed simulation.
  - Open: Pump nose extension, pulley bore and axial seating at X530 are provisional interface reconciliation. Thread nominal size and right-hand direction are sourced; the model uses smooth clearance envelopes rather than thread helices.
  - Open: Fan bolts use sourced 5/16-18 nominal diameter and four-hole count; length, head dimensions, thread engagement and hole angular index are provisional. Radiator/shroud clearance is not established.
  - Open: Silicone fluid and its dynamic fill fraction are described rather than represented as rigid solids. The sealed clutch is not a user-serviceable exploded repair procedure.
- [ ] **Cooling fan blade rivet · provisional** — `cooling-fan-rivet`; modeled quantity **14**; provisional.
  - Instances: `cooling-fan-rivet-1-1`, `cooling-fan-rivet-1-2`, `cooling-fan-rivet-2-1`, `cooling-fan-rivet-2-2`, `cooling-fan-rivet-3-1`, `cooling-fan-rivet-3-2`, `cooling-fan-rivet-4-1`, `cooling-fan-rivet-4-2`, `cooling-fan-rivet-5-1`, `cooling-fan-rivet-5-2`, `cooling-fan-rivet-6-1`, `cooling-fan-rivet-6-2`, `cooling-fan-rivet-7-1`, `cooling-fan-rivet-7-2`
  - Source IDs: system-7b01cf423275, imperial-fan-clutch-215161, hayden-fan-clutch-operation, dorman-620-151. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Imperial lists both 215161 (36 mm hex, M30x1.5 RH) and 215155 (40 mm hex, M33x1.5 RH) for 1994 F-Series 4.9L. This is the 215161 comparison branch; installed nut size is unknown.
  - Open: Catalog dimensions constrain clutch OD, overall height, fan mount height, fan pilot and four-hole bolt circle. Housing sections, bearing, seals, shear lands, reservoir, valve and spring are educational assumptions, not a production teardown.
  - Open: Dorman 620-151 supplies a seven-blade, 18.9 inch black stamped-steel comparison and F2UZ8600A cross-reference. Exact 4.9L vehicle fit is not independently established by the saved primary application table; installed fan identity remains unverified.
  - Open: Blade chord, pitch, twist, angular spacing, root shape, spider, fourteen rivets and all sheet thicknesses are provisional interpretations of the manufacturer photo. No airflow, stress, balance or fan-speed simulation.
  - Open: Pump nose extension, pulley bore and axial seating at X530 are provisional interface reconciliation. Thread nominal size and right-hand direction are sourced; the model uses smooth clearance envelopes rather than thread helices.
  - Open: Fan bolts use sourced 5/16-18 nominal diameter and four-hole count; length, head dimensions, thread engagement and hole angular index are provisional. Radiator/shroud clearance is not established.
  - Open: Silicone fluid and its dynamic fill fraction are described rather than represented as rigid solids. The sealed clutch is not a user-serviceable exploded repair procedure.
- [ ] **Fan-to-clutch bolt** — `cooling-fan-bolt`; modeled quantity **4**; provisional.
  - Instances: `cooling-fan-bolt-1`, `cooling-fan-bolt-2`, `cooling-fan-bolt-3`, `cooling-fan-bolt-4`
  - Source IDs: system-7b01cf423275, imperial-fan-clutch-215161, hayden-fan-clutch-operation, dorman-620-151. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Imperial lists both 215161 (36 mm hex, M30x1.5 RH) and 215155 (40 mm hex, M33x1.5 RH) for 1994 F-Series 4.9L. This is the 215161 comparison branch; installed nut size is unknown.
  - Open: Catalog dimensions constrain clutch OD, overall height, fan mount height, fan pilot and four-hole bolt circle. Housing sections, bearing, seals, shear lands, reservoir, valve and spring are educational assumptions, not a production teardown.
  - Open: Dorman 620-151 supplies a seven-blade, 18.9 inch black stamped-steel comparison and F2UZ8600A cross-reference. Exact 4.9L vehicle fit is not independently established by the saved primary application table; installed fan identity remains unverified.
  - Open: Blade chord, pitch, twist, angular spacing, root shape, spider, fourteen rivets and all sheet thicknesses are provisional interpretations of the manufacturer photo. No airflow, stress, balance or fan-speed simulation.
  - Open: Pump nose extension, pulley bore and axial seating at X530 are provisional interface reconciliation. Thread nominal size and right-hand direction are sourced; the model uses smooth clearance envelopes rather than thread helices.
  - Open: Fan bolts use sourced 5/16-18 nominal diameter and four-hole count; length, head dimensions, thread engagement and hole angular index are provisional. Radiator/shroud clearance is not established.
  - Open: Silicone fluid and its dynamic fill fraction are described rather than represented as rigid solids. The sealed clutch is not a user-serviceable exploded repair procedure.

## Additional known scope and reconciliation

- [ ] Verify fan/clutch variant, blade pitch, internal fluid coupling, bearings and seals

## Cross-system boundaries

Coordinate with [#8](https://github.com/0xZakk/truck/issues/8). Keep the current engine-mounted component here; agree ownership before adding its vehicle-side continuation.

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
