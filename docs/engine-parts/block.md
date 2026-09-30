# Cylinder block, plugs and dowels

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#24](https://github.com/0xZakk/truck/issues/24).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Rear camshaft bore plug** — `rear-cam-plug`; modeled quantity **1**; provisional.
  - Instances: `rear-cam-plug`
  - Source IDs: melling-expansion-plug-guide, ford-industrial-parts. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Melling MPC-147 replacement envelope: OD2.194in and height.343in; kit identifies its camshaft application. Installed identity is not verified.
  - Open: Uniform1mm cup wall, square internal corner, supporting boss, .5mm recess and clearance-fit seat are assumptions. Actual press fit, stamp radii and bore size remain unresolved.
- [ ] **Cylinder block** — `block`; modeled quantity **1**; provisional.
  - Instances: `block`
  - Source IDs: fsm-ed8704e3446e, fsm-2e5473b2bf99, ford-engine-side-layout, ford-industrial-csg649, fsm-a3698a10af15, melling-intermediate-shaft-dimensions, ford-accessory-brackets, ford-accessory-routing, ford-cii-pump-study, ford-alternator-study, ford-thermactor-study, fsm-d975f341ee63, fsm-6f023139b5f8, wix-51515-envelope, enginequest-oil-filter-adapter, ford-tsb-94-10-19-accessory, truck-oil-pan-hardware, fel-pro-vin-y-gaskets, felpro-os34601r-topology, water-pump-mounting-topology, gates-water-pumps-2011, dipstick-specimen-e9te, dipstick-service-catalog, dipstick-tube-1995-adjacent-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Bore pitch 113.792 mm, deck height 254 mm and casting envelope are assumptions. The side-cover opening, perimeter rail and six fastener webs are provisional fit-study geometry. The rear cam plug seat and support boss are provisional. Water jackets, oil drillings, other bosses/plugs and deck passages need reconstruction.
  - Open: 20 degree lean, X227.584 station, gear-axis spacing, distributor lower extension, mounting bosses and pickup bends are constrained fit-study assumptions, not surveyed Ford geometry.
  - Open: Melling IS-74 length 114.808 mm and hex across flats 7.9248 mm remain unchanged. Ten mm upper and nine mm lower engagement are assumed.
  - Open: Cam-to-distributor crossed-helical tooth geometry, working backlash and angular phase remain unverified; this is a connected spatial study, not validated power transmission.
  - Open: Oil galleries and pump mounting architecture require a production reference. Proposed block cuts and supports must not be used as machining instructions.
  - Open: Ford identifies a shared power-steering/A/C bracket attached to block and head and a separate alternator bracket. These castings reconstruct that load-path topology, not a measured production casting.
  - Open: All boss coordinates, bolt counts, web sections, material colors, hole sizes and mounting-face locations are illustrative interfaces to the current component studies. Casting ribs, part numbers, dowels and factory contours remain unknown.
  - Open: Engine feet touch provisional front-face seats. Explicit interface adapters add isolated blind support bosses and 16 mm deep smooth thread-envelope bores; 14 mm bolt engagement is illustrative, not a verified thread specification. These are dry blind attachments, not coolant or oil passages.
  - Open: Accessory bolt shanks use clearance through the candidate mounting ears. Threads, grades, preload, bracket stiffness and belt-load deflection are not simulated.
  - Open: The Thermactor and tensioner engine brackets remain separate unresolved load paths. No unsupported air-pump attachment is added to these castings.
  - Open: Ford identifies a belt-driven positive-displacement vane pump and illustrates its body, inlet, outlet and three-hole pulley hub. This interim model reconstructs the exterior interfaces, not the full internal pumping mechanism.
  - Open: The generic Ford truck description covers 19 and 22 cubic-inch pumps without assigning one to this installed engine. Neither displacement nor vane count is claimed. The pumping cartridge is one explicitly unresolved envelope.
  - Open: All dimensions, rotor-envelope form, bearing cartridges, shaft, pulley diameter/profile, six grooves, case fastener count and mounting-ear positions are illustrative. No aftermarket part identity or published generic comparison dimensions are treated as verified installed geometry.
  - Open: Station (473.56,-280,100) follows the labeled lower-RH A/P topology and provisional belt plane, not measured engine datums. Inlet filter, hoses, bypass/diverter valves and air-injection manifold connections remain unfinished.
  - Open: A separate assumed support connects the current pump ears to dry blind front-block bosses. Bracket casting, two mount bolts, two engine bolts and 14 mm smooth engagement envelopes are not factory dimensional evidence.
  - Open: No threads, bearing rolling elements, dynamic vane contact, pressure/flow, pump speed ratio or thermal/friction simulation. Collision-free geometry does not verify an emissions-system repair or production fit.
  - Open: The insert is a hollow stepped comparison envelope, not a reconstructed E4TZ-6890-A anti-drainback service insert. No unsourced valve mechanism is added.
  - Open: Filter position, inclined boss, gallery routing, insert lengths, block-end thread diameter and sealing lands are provisional. Filter-side 3/4-16 uses coincident nominal male/female envelopes, not helical thread contact.
  - Open: Two deliberately open side interfaces bound this gallery study. They are not production external ports and remain disconnected from the pump and main oil gallery. The engine lubrication circuit is incomplete.
  - Open: No separate adapter gasket or additional bypass valve is inferred. The existing filter gasket, internal flap and illustrative bypass remain separate components; seal compression and anti-drainback performance are not simulated.
  - Open: Ford Fig4 establishes a shared P/S–A/C–tensioner carrier, front-head bolt#1, side-head bolt#2 and two side-block nuts#3. It does not dimension any modeled hole, web, casting, stud or fastening fit.
  - Open: PS and A/C stations stay unchanged. The tensioner wheel is provisionally at(473.56,167,350) with its75mm assumed arm below the pivot; source drawings establish relative arrangement only.
  - Open: Smooth shafts and nut bores represent stud engagement without production thread pitches, grades, preload or load analysis.
  - Open: Adapters add dry external side bosses. Passage proximity, casting wall thickness and original old front block boss cleanup require independent source work.
  - Open: The original separate tensioner engine support must not be installed. This candidate replaces the PS/AC carrier and its two provisional front-axis attachment bolts.
  - Open: Catalog belt fit and moving tensioner travel remain unresolved. This architecture correction does not match centers to a target belt length.
  - Open: Exact OS34601R product photo supports a continuous gasket and10holes per long rail plus3and2at its ends. Hole coordinates, central rail offset and photo-end orientation remain unmeasured.
  - Open: All gasket thicknesses, radii, pads, compression, washers, head geometry, clearances and blind sockets are provisional. This is a matched geometric study, not a production gasket or dimensional drawing.
  - Open: The continuous inset pan neck uses assumed746x242-to726x232mm envelopes between Z-90and-76, with its center shifted5mm toward+Y and a wider flat flange; it reconciles bolt clearance with the existing provisional starter and does not establish production stamping or capacity. Front and rear end lands are illustrative dry block extensions. The actual timing-cover/block/pan junction and local sealant remain unresolved.
  - Open: V9 narrows the complete shallow shell to726mm length with720mm inner cavity; the original rear sump profile, floor depth and drain datum remain. This keeps the continuous front end wall behind the bolt extraction corridor; overall stamping remains unmeasured.
  - Open: The continuous inset pan neck uses assumed726x242-to726x232mm envelopes between Z-90and-76, with its center shifted5mm toward+Y and a wider flat flange; it reconciles bolt clearance with the existing provisional starter and does not establish production stamping or capacity. Front and rear end lands are illustrative dry block extensions. The actual timing-cover/block/pan junction and local sealant remain unresolved.
  - Open: ATK DFF8 automotive block-front photo supports pump flange directly on block face, four mounting holes and a larger fifth opening; exact hole coordinates and installed lateral axis offset remain unmeasured.
  - Open: The casting now reaches modeled blockfrontX373 through its rear flange and2mmgasket; tapered chamber depth83mm is assumed to preserve the existing provisional hub/bearing/heater-return datums. This is not a verified Gates44009 dimension.
  - Open: All four fasteners are unthreaded8mm×31.75mm illustrative envelopes with13mmhex heads. Production bolt thread, length, head, washer construction and socket depth are unverified; these are not replacement specifications.
  - Open: The receiver cuts only the demonstrated front opening into the existing modeled cavity while retaining the front cylinder wall. Deeper coolant jacket, fifth-opening function, circulation and hydraulic performance remain unresolved.
  - Open: The larger gasket opening is retained as an unidentified passage with a provisional short pump-chamber connection; its actual cast routing is unverified. Radiator inlet neck remains a separate missing reconstruction.
  - Open: Impeller, mechanical seal, bearing cartridge and internal shaft geometry remain simplified. Existing belt plane and pumpY−32/Z170 coordinates are not factory dimensions.
  - Open: The provisional Thermactor upper support foot and blind socket move together to Y-125/Z140; casting, load capacity and production coordinates remain unverified.
  - Open: Educational interface estimates, not production dimensions or machining instructions. Exact1994 tube/indicator identity and upper support station remain unverified.
  - Open: Lower and upper mating threads are clearance envelopes. Thread engagement, sealing construction, bracket manufacturing joint, clamp load and retention strength are unvalidated.
  - Open: The pilot692.15mm approximate axial route comprises558.476126mm guide and133.673874mm free extension. Estimated waves add6.572804mm of material centerline; the material length is698.722804mm.
  - Open: Blade sections, waves, handle and stamp placement are inherited estimates. E9TE-6750-DA is specimen evidence, not owner identification; no ADD/FULL mark or oil calibration is reconstructed.
  - Open: The inserted blade is a rigid flexed display pose. Elastic insertion/withdrawal, twist, wave compression, handle retention force and service removal are not simulated.

## Additional known scope and reconciliation

- [ ] Core/freeze plugs and all oil-gallery plugs: identify locations and quantities
- [ ] Head/block and rear engine locating dowels: verify inventory
- [ ] Block coolant jackets and oil galleries
- [ ] Casting identification, dimensions and mounting bosses

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
