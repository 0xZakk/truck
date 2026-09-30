# Water pump, impeller, shaft, seal, bearing and pulley

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#47](https://github.com/0xZakk/truck/issues/47).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `ab99fff2f63ad5dfc21fde8d12a32fc2a3d65832e6c8664baefd99d94403f7bf`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

Current-state correction: the cast inlet neck is present in this manifest. Older unresolved strings below saying it is missing are superseded; its production geometry and flow fidelity remain unverified.

- [ ] **Water pump slinger** — `water-pump-slinger`; modeled quantity **1**; provisional.
  - Instances: `water-pump-slinger`
  - Source IDs: system-7b01cf423275, system-628ac5b60213, gates-water-pumps-2011. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: F6TZ8501KB / Gates 44009 application is sourced; no pump dimensions or installed datums are established.
  - Open: Casting outline, ports, mounting pattern, vane count/profile and all internal dimensions are illustrative. Bearing is represented as a sealed cartridge, not individual races/rolling elements.
  - Open: Hose connections, block coolant interface, attaching hardware, pulley and fan clutch remain outstanding. No belt ratio or coolant-flow simulation is implemented.
- [ ] **Water pump sealed bearing · cartridge** — `water-pump-bearing`; modeled quantity **1**; provisional.
  - Instances: `water-pump-bearing`
  - Source IDs: system-7b01cf423275, system-628ac5b60213, gates-water-pumps-2011. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: F6TZ8501KB / Gates 44009 application is sourced; no pump dimensions or installed datums are established.
  - Open: Casting outline, ports, mounting pattern, vane count/profile and all internal dimensions are illustrative. Bearing is represented as a sealed cartridge, not individual races/rolling elements.
  - Open: Hose connections, block coolant interface, attaching hardware, pulley and fan clutch remain outstanding. No belt ratio or coolant-flow simulation is implemented.
- [ ] **Water pump drive hub** — `water-pump-drive-hub`; modeled quantity **1**; provisional.
  - Instances: `water-pump-drive-hub`
  - Source IDs: system-7b01cf423275, system-628ac5b60213, gates-water-pumps-2011, imperial-fan-clutch-215161, hayden-fan-clutch-operation, dorman-620-151. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Imperial lists both 215161 (36 mm hex, M30x1.5 RH) and 215155 (40 mm hex, M33x1.5 RH) for 1994 F-Series 4.9L. This is the 215161 comparison branch; installed nut size is unknown.
  - Open: Catalog dimensions constrain clutch OD, overall height, fan mount height, fan pilot and four-hole bolt circle. Housing sections, bearing, seals, shear lands, reservoir, valve and spring are educational assumptions, not a production teardown.
  - Open: Dorman 620-151 supplies a seven-blade, 18.9 inch black stamped-steel comparison and F2UZ8600A cross-reference. Exact 4.9L vehicle fit is not independently established by the saved primary application table; installed fan identity remains unverified.
  - Open: Blade chord, pitch, twist, angular spacing, root shape, spider, fourteen rivets and all sheet thicknesses are provisional interpretations of the manufacturer photo. No airflow, stress, balance or fan-speed simulation.
  - Open: Pump nose extension, pulley bore and axial seating at X530 are provisional interface reconciliation. Thread nominal size and right-hand direction are sourced; the model uses smooth clearance envelopes rather than thread helices.
  - Open: Fan bolts use sourced 5/16-18 nominal diameter and four-hole count; length, head dimensions, thread engagement and hole angular index are provisional. Radiator/shroud clearance is not established.
  - Open: Silicone fluid and its dynamic fill fraction are described rather than represented as rigid solids. The sealed clutch is not a user-serviceable exploded repair procedure.
- [ ] **Water pump pulley** — `water-pump-pulley`; modeled quantity **1**; provisional.
  - Instances: `water-pump-pulley`
  - Source IDs: system-7b01cf423275, gates-1994-drive. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Ford service procedure establishes a separate pulley and threaded fan-clutch assembly, but supplies no pulley dimensions.
  - Open: Gates S7004 shows backside contact at the central upper wheel; identifying that wheel as the water pump is an interpretation. Smooth rim is provisional pending an identified production-pulley photograph.
  - Open: 150 mm diameter, 28 mm rim width, dish section, four-hole 50 mm bolt circle and all fastener dimensions are illustrative. Four bolts follow the existing provisional hub holes, not a sourced production bolt count.
  - Open: Pulley sits on the existing pump hub front at global X522. Its assumed dish depth aligns the smooth rim with the current illustrative damper belt center X473.56; neither datum establishes factory belt alignment.
  - Open: Fan-clutch threaded nose, thread dimensions, belt routing, working belt ratio and rotational animation remain unresolved. Smooth fastener shanks do not model threads or production clamping fit.
- [ ] **Water pump pulley bolt · provisional** — `water-pump-pulley-bolt`; modeled quantity **4**; provisional.
  - Instances: `water-pump-pulley-bolt-1`, `water-pump-pulley-bolt-2`, `water-pump-pulley-bolt-3`, `water-pump-pulley-bolt-4`
  - Source IDs: system-7b01cf423275, gates-1994-drive. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Ford service procedure establishes a separate pulley and threaded fan-clutch assembly, but supplies no pulley dimensions.
  - Open: Gates S7004 shows backside contact at the central upper wheel; identifying that wheel as the water pump is an interpretation. Smooth rim is provisional pending an identified production-pulley photograph.
  - Open: 150 mm diameter, 28 mm rim width, dish section, four-hole 50 mm bolt circle and all fastener dimensions are illustrative. Four bolts follow the existing provisional hub holes, not a sourced production bolt count.
  - Open: Pulley sits on the existing pump hub front at global X522. Its assumed dish depth aligns the smooth rim with the current illustrative damper belt center X473.56; neither datum establishes factory belt alignment.
  - Open: Fan-clutch threaded nose, thread dimensions, belt routing, working belt ratio and rotational animation remain unresolved. Smooth fastener shanks do not model threads or production clamping fit.
- [ ] **Water pump mounting gasket** — `water-pump-gasket`; modeled quantity **1**; provisional.
  - Instances: `water-pump-gasket`
  - Source IDs: system-7b01cf423275, system-628ac5b60213, gates-water-pumps-2011, water-pump-mounting-topology, fel-pro-vin-y-gaskets. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: F6TZ8501KB / Gates 44009 application is sourced; no pump dimensions or installed datums are established.
  - Open: Casting outline, ports, mounting pattern, vane count/profile and all internal dimensions are illustrative. Bearing is represented as a sealed cartridge, not individual races/rolling elements.
  - Open: Hose connections, block coolant interface, attaching hardware, pulley and fan clutch remain outstanding. No belt ratio or coolant-flow simulation is implemented.
  - Open: ATK DFF8 automotive block-front photo supports pump flange directly on block face, four mounting holes and a larger fifth opening; exact hole coordinates and installed lateral axis offset remain unmeasured.
  - Open: The casting now reaches modeled blockfrontX373 through its rear flange and2mmgasket; tapered chamber depth83mm is assumed to preserve the existing provisional hub/bearing/heater-return datums. This is not a verified Gates44009 dimension.
  - Open: All four fasteners are unthreaded8mm×31.75mm illustrative envelopes with13mmhex heads. Production bolt thread, length, head, washer construction and socket depth are unverified; these are not replacement specifications.
  - Open: The receiver cuts only the demonstrated front opening into the existing modeled cavity while retaining the front cylinder wall. Deeper coolant jacket, fifth-opening function, circulation and hydraulic performance remain unresolved.
  - Open: The larger gasket opening is retained as an unidentified passage with a provisional short pump-chamber connection; its actual cast routing is unverified. Radiator inlet neck remains a separate missing reconstruction.
  - Open: Impeller, mechanical seal, bearing cartridge and internal shaft geometry remain simplified. Existing belt plane and pumpY−32/Z170 coordinates are not factory dimensions.
  - Open: The provisional Thermactor upper support foot and blind socket move together to Y-125/Z140; casting, load capacity and production coordinates remain unverified.
- [ ] **Water pump shaft** — `water-pump-shaft`; modeled quantity **1**; provisional.
  - Instances: `water-pump-shaft`
  - Source IDs: system-7b01cf423275, system-628ac5b60213, gates-water-pumps-2011, water-pump-mounting-topology, fel-pro-vin-y-gaskets. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: F6TZ8501KB / Gates 44009 application is sourced; no pump dimensions or installed datums are established.
  - Open: Casting outline, ports, mounting pattern, vane count/profile and all internal dimensions are illustrative. Bearing is represented as a sealed cartridge, not individual races/rolling elements.
  - Open: Hose connections, block coolant interface, attaching hardware, pulley and fan clutch remain outstanding. No belt ratio or coolant-flow simulation is implemented.
  - Open: ATK DFF8 automotive block-front photo supports pump flange directly on block face, four mounting holes and a larger fifth opening; exact hole coordinates and installed lateral axis offset remain unmeasured.
  - Open: The casting now reaches modeled blockfrontX373 through its rear flange and2mmgasket; tapered chamber depth83mm is assumed to preserve the existing provisional hub/bearing/heater-return datums. This is not a verified Gates44009 dimension.
  - Open: All four fasteners are unthreaded8mm×31.75mm illustrative envelopes with13mmhex heads. Production bolt thread, length, head, washer construction and socket depth are unverified; these are not replacement specifications.
  - Open: The receiver cuts only the demonstrated front opening into the existing modeled cavity while retaining the front cylinder wall. Deeper coolant jacket, fifth-opening function, circulation and hydraulic performance remain unresolved.
  - Open: The larger gasket opening is retained as an unidentified passage with a provisional short pump-chamber connection; its actual cast routing is unverified. Radiator inlet neck remains a separate missing reconstruction.
  - Open: Impeller, mechanical seal, bearing cartridge and internal shaft geometry remain simplified. Existing belt plane and pumpY−32/Z170 coordinates are not factory dimensions.
  - Open: The provisional Thermactor upper support foot and blind socket move together to Y-125/Z140; casting, load capacity and production coordinates remain unverified.
- [ ] **Water pump impeller** — `water-pump-impeller`; modeled quantity **1**; provisional.
  - Instances: `water-pump-impeller`
  - Source IDs: system-7b01cf423275, system-628ac5b60213, gates-water-pumps-2011, water-pump-mounting-topology, fel-pro-vin-y-gaskets. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: F6TZ8501KB / Gates 44009 application is sourced; no pump dimensions or installed datums are established.
  - Open: Casting outline, ports, mounting pattern, vane count/profile and all internal dimensions are illustrative. Bearing is represented as a sealed cartridge, not individual races/rolling elements.
  - Open: Hose connections, block coolant interface, attaching hardware, pulley and fan clutch remain outstanding. No belt ratio or coolant-flow simulation is implemented.
  - Open: ATK DFF8 automotive block-front photo supports pump flange directly on block face, four mounting holes and a larger fifth opening; exact hole coordinates and installed lateral axis offset remain unmeasured.
  - Open: The casting now reaches modeled blockfrontX373 through its rear flange and2mmgasket; tapered chamber depth83mm is assumed to preserve the existing provisional hub/bearing/heater-return datums. This is not a verified Gates44009 dimension.
  - Open: All four fasteners are unthreaded8mm×31.75mm illustrative envelopes with13mmhex heads. Production bolt thread, length, head, washer construction and socket depth are unverified; these are not replacement specifications.
  - Open: The receiver cuts only the demonstrated front opening into the existing modeled cavity while retaining the front cylinder wall. Deeper coolant jacket, fifth-opening function, circulation and hydraulic performance remain unresolved.
  - Open: The larger gasket opening is retained as an unidentified passage with a provisional short pump-chamber connection; its actual cast routing is unverified. Radiator inlet neck remains a separate missing reconstruction.
  - Open: Impeller, mechanical seal, bearing cartridge and internal shaft geometry remain simplified. Existing belt plane and pumpY−32/Z170 coordinates are not factory dimensions.
  - Open: The provisional Thermactor upper support foot and blind socket move together to Y-125/Z140; casting, load capacity and production coordinates remain unverified.
- [ ] **Water-pump mounting screw · provisional envelope** — `water-pump-mounting-screw`; modeled quantity **4**; provisional.
  - Instances: `water-pump-mounting-screw-1`, `water-pump-mounting-screw-2`, `water-pump-mounting-screw-3`, `water-pump-mounting-screw-4`
  - Source IDs: water-pump-mounting-topology, gates-water-pumps-2011, fel-pro-vin-y-gaskets. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: ATK DFF8 automotive block-front photo supports pump flange directly on block face, four mounting holes and a larger fifth opening; exact hole coordinates and installed lateral axis offset remain unmeasured.
  - Open: The casting now reaches modeled blockfrontX373 through its rear flange and2mmgasket; tapered chamber depth83mm is assumed to preserve the existing provisional hub/bearing/heater-return datums. This is not a verified Gates44009 dimension.
  - Open: All four fasteners are unthreaded8mm×31.75mm illustrative envelopes with13mmhex heads. Production bolt thread, length, head, washer construction and socket depth are unverified; these are not replacement specifications.
  - Open: The receiver cuts only the demonstrated front opening into the existing modeled cavity while retaining the front cylinder wall. Deeper coolant jacket, fifth-opening function, circulation and hydraulic performance remain unresolved.
  - Open: The larger gasket opening is retained as an unidentified passage with a provisional short pump-chamber connection; its actual cast routing is unverified. Radiator inlet neck remains a separate missing reconstruction.
  - Open: Impeller, mechanical seal, bearing cartridge and internal shaft geometry remain simplified. Existing belt plane and pumpY−32/Z170 coordinates are not factory dimensions.
- [ ] **Water pump housing** — `water-pump-housing`; modeled quantity **1**; provisional.
  - Instances: `water-pump-housing`
  - Source IDs: system-7b01cf423275, system-628ac5b60213, gates-water-pumps-2011, ford-cooling-connections, ford-ect-construction, ford-cooling-sensor-circuits, gates-1994-drive, truck-cooling-hose-photos, water-pump-mounting-topology, fel-pro-vin-y-gaskets, water-pump-inlet-v3-topology. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: F6TZ8501KB / Gates 44009 application is sourced; no pump dimensions or installed datums are established.
  - Open: Casting outline, ports, mounting pattern, vane count/profile and all internal dimensions are illustrative. Bearing is represented as a sealed cartridge, not individual races/rolling elements.
  - Open: Hose connections, block coolant interface, attaching hardware, pulley and fan clutch remain outstanding. No belt ratio or coolant-flow simulation is implemented.
  - Open: Ford identifies the two-lead ECT at the thermostat housing/heater elbow and specifies 3/8-18 NPTF-SPL dry-seal thread. All sensor dimensions, internal thermistor shape and connector detail are provisional.
  - Open: A separate single-wire gauge sender C150 on the RH engine side feeds circuit 39 R/W and grounds through its body. It is not the ECT C183. Gauge sender mounting and the head coolant jacket remain unresolved; no false dry pocket is presented as a coolant connection.
  - Open: Both heater connections use Gates 18767 in the five-speed manual application. Exact hose end assignment, bore, installed cut length and routing are not established here; metal tubes, radii, beads and clearances are illustrative.
  - Open: Owner photos show paired red-orange heater hoses crossing from the firewall toward the front engine. Only attached engine-side metal takeoffs are modeled; full heater/radiator hoses need located vehicle endpoints.
  - Open: The thermostat-side elbow opens into the existing secondary outlet passage; the pump return opens into its existing coolant chamber. Pump/block and outlet/head jacket connections remain incomplete.
  - Open: Ford TSB 94-9-13 describes an E4OD-only radiator bleed tee. That automatic-transmission arrangement is not applied to this manual truck.
  - Open: Thread helices, tapered sealing fits, hose deformation, clamps, harness connectors and coolant/temperature simulation are absent. Sensor resistor and leads are a construction study, not a rebuild procedure.
  - Open: ATK DFF8 automotive block-front photo supports pump flange directly on block face, four mounting holes and a larger fifth opening; exact hole coordinates and installed lateral axis offset remain unmeasured.
  - Open: The casting now reaches modeled blockfrontX373 through its rear flange and2mmgasket; tapered chamber depth83mm is assumed to preserve the existing provisional hub/bearing/heater-return datums. This is not a verified Gates44009 dimension.
  - Open: All four fasteners are unthreaded8mm×31.75mm illustrative envelopes with13mmhex heads. Production bolt thread, length, head, washer construction and socket depth are unverified; these are not replacement specifications.
  - Open: The receiver cuts only the demonstrated front opening into the existing modeled cavity while retaining the front cylinder wall. Deeper coolant jacket, fifth-opening function, circulation and hydraulic performance remain unresolved.
  - Open: The larger gasket opening is retained as an unidentified passage with a provisional short pump-chamber connection; its actual cast routing is unverified. Radiator inlet neck remains a separate missing reconstruction.
  - Open: Impeller, mechanical seal, bearing cartridge and internal shaft geometry remain simplified. Existing belt plane and pumpY−32/Z170 coordinates are not factory dimensions.
  - Open: The provisional Thermactor upper support foot and blind socket move together to Y-125/Z140; casting, load capacity and production coordinates remain unverified.
  - Open: Gates44009 front/rear/side photos show large lateral cast inlet arm with hose neck and retaining bead. Positive-Y assignment opposite retained heater tube is inferred; no physical pump measurement exists.
  - Open: Inlet neck localX−10/Z25, endY145, outer radius24 and bore20mm are provisional. Cast arm curves to rear chamber at localX−20/Y19; no internal photograph fixes this path. They are not hose purchasing dimensions.
  - Open: Smooth tapered open passage demonstrates topology only: the actual volute, impeller-eye feed, casting wall sections, hydraulic capacity and flow simulation remain unverified.
- [ ] **Mechanical-seal carrier · illustrative** — `water-pump-seal-carrier`; modeled quantity **1**; provisional.
  - Instances: `water-pump-seal-carrier`
  - Source IDs: water-pump-internal-construction. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: This six-component seal is a generic axial-face construction study, not a verified Gates44009 bill of materials. No real replacement seal number is established.
  - Open: All face diameters,10mm stack length, carrier shape, elastomer sections, spring wire/turn count and installed compression are illustrative. Face material pairing is not established for this truck.
  - Open: Carrier contact at localX18..21 uses radius24 to meet the modeled housing throat; it replaces the former radius23.8 floating envelope. Housing, shaft, mounting and drive poses are unchanged.
  - Open: Exact bearing row count/type, rolling-element count, cages and raceway dimensions remain unknown. The existing bearing cartridge is not claimed to be a measured production bearing.
  - Open: Exploded geometry explains interfaces, not a pump rebuild procedure. Ford services the sealed pump as an assembly. No elastic, thermal, pressure, leakage or coolant-film simulation is included.
- [ ] **Stationary sealing face · illustrative** — `water-pump-seal-stationary-face`; modeled quantity **1**; provisional.
  - Instances: `water-pump-seal-stationary-face`
  - Source IDs: water-pump-internal-construction. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: This six-component seal is a generic axial-face construction study, not a verified Gates44009 bill of materials. No real replacement seal number is established.
  - Open: All face diameters,10mm stack length, carrier shape, elastomer sections, spring wire/turn count and installed compression are illustrative. Face material pairing is not established for this truck.
  - Open: Carrier contact at localX18..21 uses radius24 to meet the modeled housing throat; it replaces the former radius23.8 floating envelope. Housing, shaft, mounting and drive poses are unchanged.
  - Open: Exact bearing row count/type, rolling-element count, cages and raceway dimensions remain unknown. The existing bearing cartridge is not claimed to be a measured production bearing.
  - Open: Exploded geometry explains interfaces, not a pump rebuild procedure. Ford services the sealed pump as an assembly. No elastic, thermal, pressure, leakage or coolant-film simulation is included.
- [ ] **Rotating sealing face · illustrative** — `water-pump-seal-rotating-face`; modeled quantity **1**; provisional.
  - Instances: `water-pump-seal-rotating-face`
  - Source IDs: water-pump-internal-construction. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: This six-component seal is a generic axial-face construction study, not a verified Gates44009 bill of materials. No real replacement seal number is established.
  - Open: All face diameters,10mm stack length, carrier shape, elastomer sections, spring wire/turn count and installed compression are illustrative. Face material pairing is not established for this truck.
  - Open: Carrier contact at localX18..21 uses radius24 to meet the modeled housing throat; it replaces the former radius23.8 floating envelope. Housing, shaft, mounting and drive poses are unchanged.
  - Open: Exact bearing row count/type, rolling-element count, cages and raceway dimensions remain unknown. The existing bearing cartridge is not claimed to be a measured production bearing.
  - Open: Exploded geometry explains interfaces, not a pump rebuild procedure. Ford services the sealed pump as an assembly. No elastic, thermal, pressure, leakage or coolant-film simulation is included.
- [ ] **Rotating seal collar · illustrative** — `water-pump-seal-shaft-collar`; modeled quantity **1**; provisional.
  - Instances: `water-pump-seal-shaft-collar`
  - Source IDs: water-pump-internal-construction. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: This six-component seal is a generic axial-face construction study, not a verified Gates44009 bill of materials. No real replacement seal number is established.
  - Open: All face diameters,10mm stack length, carrier shape, elastomer sections, spring wire/turn count and installed compression are illustrative. Face material pairing is not established for this truck.
  - Open: Carrier contact at localX18..21 uses radius24 to meet the modeled housing throat; it replaces the former radius23.8 floating envelope. Housing, shaft, mounting and drive poses are unchanged.
  - Open: Exact bearing row count/type, rolling-element count, cages and raceway dimensions remain unknown. The existing bearing cartridge is not claimed to be a measured production bearing.
  - Open: Exploded geometry explains interfaces, not a pump rebuild procedure. Ford services the sealed pump as an assembly. No elastic, thermal, pressure, leakage or coolant-film simulation is included.
- [ ] **Stationary seal bellows · illustrative** — `water-pump-seal-bellows`; modeled quantity **1**; provisional.
  - Instances: `water-pump-seal-bellows`
  - Source IDs: water-pump-internal-construction. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: This six-component seal is a generic axial-face construction study, not a verified Gates44009 bill of materials. No real replacement seal number is established.
  - Open: All face diameters,10mm stack length, carrier shape, elastomer sections, spring wire/turn count and installed compression are illustrative. Face material pairing is not established for this truck.
  - Open: Carrier contact at localX18..21 uses radius24 to meet the modeled housing throat; it replaces the former radius23.8 floating envelope. Housing, shaft, mounting and drive poses are unchanged.
  - Open: Exact bearing row count/type, rolling-element count, cages and raceway dimensions remain unknown. The existing bearing cartridge is not claimed to be a measured production bearing.
  - Open: Exploded geometry explains interfaces, not a pump rebuild procedure. Ford services the sealed pump as an assembly. No elastic, thermal, pressure, leakage or coolant-film simulation is included.
- [ ] **Seal face-loading spring · illustrative** — `water-pump-seal-spring`; modeled quantity **1**; provisional.
  - Instances: `water-pump-seal-spring`
  - Source IDs: water-pump-internal-construction. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: This six-component seal is a generic axial-face construction study, not a verified Gates44009 bill of materials. No real replacement seal number is established.
  - Open: All face diameters,10mm stack length, carrier shape, elastomer sections, spring wire/turn count and installed compression are illustrative. Face material pairing is not established for this truck.
  - Open: Carrier contact at localX18..21 uses radius24 to meet the modeled housing throat; it replaces the former radius23.8 floating envelope. Housing, shaft, mounting and drive poses are unchanged.
  - Open: Exact bearing row count/type, rolling-element count, cages and raceway dimensions remain unknown. The existing bearing cartridge is not claimed to be a measured production bearing.
  - Open: Exploded geometry explains interfaces, not a pump rebuild procedure. Ford services the sealed pump as an assembly. No elastic, thermal, pressure, leakage or coolant-film simulation is included.

## Additional known scope and reconciliation

- [ ] Six illustrative mechanical-seal pieces are integrated; identify the actual seal variant, dimensions, materials and production component count before claiming truck-specific completeness
- [ ] Bearing cartridge internals: identify races/rollers/seals/retention from applicable evidence
- [ ] Cast inlet exists: verify production contour and coolant path
- [ ] Verify impeller, hub, pulley, fasteners and gland interfaces

## Cross-system boundaries

Coordinate with [#8](https://github.com/0xZakk/truck/issues/8). Keep the current engine-mounted component here; agree ownership before adding its vehicle-side continuation.

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
