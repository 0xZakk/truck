# Oil pan, gasket, drain plug and fasteners

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#34](https://github.com/0xZakk/truck/issues/34).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `0656841ba587a3f05d193aa75fb711f320ddf732cc0343c68504836c9ea7537d`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Pan drain plug · M14×1.5 comparison** — `oil-pan-drain-plug`; modeled quantity **1**; provisional.
  - Instances: `oil-pan-drain-plug`
  - Source IDs: truck-oil-pan-hardware, dorman-264011-pan, fel-pro-vin-y-gaskets. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Rear-sump architecture and maximum depth follow the Dorman264-011 comparison. The retained flange, overall length/width, transition station and contours are provisional and do not yet reproduce the published replacement envelope.
  - Open: The pan gasket/block flange, mounting-hole stations and pickup depth need coordinated reconstruction. The side strips are incomplete placeholders: the VIN-Y replacement catalog specifies molded rubber, and the older separate-piece illustration does not establish installed construction. No capacity or production-fit claim is made. Replacement drain uses M14x1.5, which must not be mixed with the older1/2-20 comparison plug.
- [ ] **Pan drain sealing washer** — `oil-pan-drain-gasket`; modeled quantity **1**; provisional.
  - Instances: `oil-pan-drain-gasket`
  - Source IDs: truck-oil-pan-hardware, dorman-264011-pan, fel-pro-vin-y-gaskets. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Rear-sump architecture and maximum depth follow the Dorman264-011 comparison. The retained flange, overall length/width, transition station and contours are provisional and do not yet reproduce the published replacement envelope.
  - Open: The pan gasket/block flange, mounting-hole stations and pickup depth need coordinated reconstruction. The side strips are incomplete placeholders: the VIN-Y replacement catalog specifies molded rubber, and the older separate-piece illustration does not establish installed construction. No capacity or production-fit claim is made. Replacement drain uses M14x1.5, which must not be mixed with the older1/2-20 comparison plug.
- [ ] **Oil pan** — `oil-pan`; modeled quantity **1**; provisional.
  - Instances: `oil-pan`
  - Source IDs: truck-oil-pan-hardware, dorman-264011-pan, fel-pro-vin-y-gaskets, felpro-os34601r-topology. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact OS34601R product photo supports a continuous gasket and10holes per long rail plus3and2at its ends. Hole coordinates, central rail offset and photo-end orientation remain unmeasured.
  - Open: All gasket thicknesses, radii, pads, compression, washers, head geometry, clearances and blind sockets are provisional. This is a matched geometric study, not a production gasket or dimensional drawing.
  - Open: V9 narrows the complete shallow shell to726mm length with720mm inner cavity; the original rear sump profile, floor depth and drain datum remain. This keeps the continuous front end wall behind the bolt extraction corridor; overall stamping remains unmeasured.
  - Open: The continuous inset pan neck uses assumed726x242-to726x232mm envelopes between Z-90and-76, with its center shifted5mm toward+Y and a wider flat flange; it reconciles bolt clearance with the existing provisional starter and does not establish production stamping or capacity. Front and rear end lands are illustrative dry block extensions. The actual timing-cover/block/pan junction and local sealant remain unresolved.
  - Open: Sump stamping, capacity, installed pan identity and production dimensions remain provisional.
- [ ] **Pan mounting screw · 5/16-18 × .87** — `oil-pan-mounting-screw`; modeled quantity **25**; provisional.
  - Instances: `oil-pan-mounting-screw-1`, `oil-pan-mounting-screw-2`, `oil-pan-mounting-screw-3`, `oil-pan-mounting-screw-4`, `oil-pan-mounting-screw-5`, `oil-pan-mounting-screw-6`, `oil-pan-mounting-screw-7`, `oil-pan-mounting-screw-8`, `oil-pan-mounting-screw-9`, `oil-pan-mounting-screw-10`, `oil-pan-mounting-screw-11`, `oil-pan-mounting-screw-12`, `oil-pan-mounting-screw-13`, `oil-pan-mounting-screw-14`, `oil-pan-mounting-screw-15`, `oil-pan-mounting-screw-16`, `oil-pan-mounting-screw-17`, `oil-pan-mounting-screw-18`, `oil-pan-mounting-screw-19`, `oil-pan-mounting-screw-20`, `oil-pan-mounting-screw-21`, `oil-pan-mounting-screw-22`, `oil-pan-mounting-screw-23`, `oil-pan-mounting-screw-24`, `oil-pan-mounting-screw-25`
  - Source IDs: truck-oil-pan-hardware, fel-pro-vin-y-gaskets, felpro-os34601r-topology. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact OS34601R product photo supports a continuous gasket and10holes per long rail plus3and2at its ends. Hole coordinates, central rail offset and photo-end orientation remain unmeasured.
  - Open: All gasket thicknesses, radii, pads, compression, washers, head geometry, clearances and blind sockets are provisional. This is a matched geometric study, not a production gasket or dimensional drawing.
  - Open: V9 narrows the complete shallow shell to726mm length with720mm inner cavity; the original rear sump profile, floor depth and drain datum remain. This keeps the continuous front end wall behind the bolt extraction corridor; overall stamping remains unmeasured.
  - Open: The continuous inset pan neck uses assumed726x242-to726x232mm envelopes between Z-90and-76, with its center shifted5mm toward+Y and a wider flat flange; it reconciles bolt clearance with the existing provisional starter and does not establish production stamping or capacity. Front and rear end lands are illustrative dry block extensions. The actual timing-cover/block/pan junction and local sealant remain unresolved.
- [ ] **Pan mounting washer** — `oil-pan-mounting-washer`; modeled quantity **25**; provisional.
  - Instances: `oil-pan-mounting-washer-1`, `oil-pan-mounting-washer-2`, `oil-pan-mounting-washer-3`, `oil-pan-mounting-washer-4`, `oil-pan-mounting-washer-5`, `oil-pan-mounting-washer-6`, `oil-pan-mounting-washer-7`, `oil-pan-mounting-washer-8`, `oil-pan-mounting-washer-9`, `oil-pan-mounting-washer-10`, `oil-pan-mounting-washer-11`, `oil-pan-mounting-washer-12`, `oil-pan-mounting-washer-13`, `oil-pan-mounting-washer-14`, `oil-pan-mounting-washer-15`, `oil-pan-mounting-washer-16`, `oil-pan-mounting-washer-17`, `oil-pan-mounting-washer-18`, `oil-pan-mounting-washer-19`, `oil-pan-mounting-washer-20`, `oil-pan-mounting-washer-21`, `oil-pan-mounting-washer-22`, `oil-pan-mounting-washer-23`, `oil-pan-mounting-washer-24`, `oil-pan-mounting-washer-25`
  - Source IDs: truck-oil-pan-hardware, fel-pro-vin-y-gaskets, felpro-os34601r-topology. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact OS34601R product photo supports a continuous gasket and10holes per long rail plus3and2at its ends. Hole coordinates, central rail offset and photo-end orientation remain unmeasured.
  - Open: All gasket thicknesses, radii, pads, compression, washers, head geometry, clearances and blind sockets are provisional. This is a matched geometric study, not a production gasket or dimensional drawing.
  - Open: V9 narrows the complete shallow shell to726mm length with720mm inner cavity; the original rear sump profile, floor depth and drain datum remain. This keeps the continuous front end wall behind the bolt extraction corridor; overall stamping remains unmeasured.
  - Open: The continuous inset pan neck uses assumed726x242-to726x232mm envelopes between Z-90and-76, with its center shifted5mm toward+Y and a wider flat flange; it reconciles bolt clearance with the existing provisional starter and does not establish production stamping or capacity. Front and rear end lands are illustrative dry block extensions. The actual timing-cover/block/pan junction and local sealant remain unresolved.
- [ ] **Continuous molded pan gasket study** — `oil-pan-molded-gasket`; modeled quantity **1**; provisional.
  - Instances: `oil-pan-molded-gasket`
  - Source IDs: truck-oil-pan-hardware, fel-pro-vin-y-gaskets, felpro-os34601r-topology. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact OS34601R product photo supports a continuous gasket and10holes per long rail plus3and2at its ends. Hole coordinates, central rail offset and photo-end orientation remain unmeasured.
  - Open: All gasket thicknesses, radii, pads, compression, washers, head geometry, clearances and blind sockets are provisional. This is a matched geometric study, not a production gasket or dimensional drawing.
  - Open: V9 narrows the complete shallow shell to726mm length with720mm inner cavity; the original rear sump profile, floor depth and drain datum remain. This keeps the continuous front end wall behind the bolt extraction corridor; overall stamping remains unmeasured.
  - Open: The continuous inset pan neck uses assumed726x242-to726x232mm envelopes between Z-90and-76, with its center shifted5mm toward+Y and a wider flat flange; it reconciles bolt clearance with the existing provisional starter and does not establish production stamping or capacity. Front and rear end lands are illustrative dry block extensions. The actual timing-cover/block/pan junction and local sealant remain unresolved.

## Historical artifacts (not current installed inventory)

- `pan-gasket` — Historical/superseded or demonstration artifact absent from current manifest; retain as history, not an additional verified truck part.
- `pan-side-gasket-1` — Historical/superseded or demonstration artifact absent from current manifest; retain as history, not an additional verified truck part.
- `pan-side-gasket-2` — Historical/superseded or demonstration artifact absent from current manifest; retain as history, not an additional verified truck part.

## Additional known scope and reconciliation

- [ ] Verify stamped contours, capacity, hole pattern and end orientation
- [ ] Verify seal compression and timing-cover junction

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
