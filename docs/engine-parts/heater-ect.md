# Heater fittings and two-wire ECT sensor

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#49](https://github.com/0xZakk/truck/issues/49).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `ab99fff2f63ad5dfc21fde8d12a32fc2a3d65832e6c8664baefd99d94403f7bf`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Heater return tube at water pump** — `heater-pump-return-elbow`; modeled quantity **1**; provisional.
  - Instances: `heater-pump-return-elbow`
  - Source IDs: ford-cooling-connections, ford-ect-construction, ford-cooling-sensor-circuits, gates-1994-drive, truck-cooling-hose-photos. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Ford identifies the two-lead ECT at the thermostat housing/heater elbow and specifies 3/8-18 NPTF-SPL dry-seal thread. All sensor dimensions, internal thermistor shape and connector detail are provisional.
  - Open: A separate single-wire gauge sender C150 on the RH engine side feeds circuit 39 R/W and grounds through its body. It is not the ECT C183. Gauge sender mounting and the head coolant jacket remain unresolved; no false dry pocket is presented as a coolant connection.
  - Open: Both heater connections use Gates 18767 in the five-speed manual application. Exact hose end assignment, bore, installed cut length and routing are not established here; metal tubes, radii, beads and clearances are illustrative.
  - Open: Owner photos show paired red-orange heater hoses crossing from the firewall toward the front engine. Only attached engine-side metal takeoffs are modeled; full heater/radiator hoses need located vehicle endpoints.
  - Open: The thermostat-side elbow opens into the existing secondary outlet passage; the pump return opens into its existing coolant chamber. Pump/block and outlet/head jacket connections remain incomplete.
  - Open: Ford TSB 94-9-13 describes an E4OD-only radiator bleed tee. That automatic-transmission arrangement is not applied to this manual truck.
  - Open: Thread helices, tapered sealing fits, hose deformation, clamps, harness connectors and coolant/temperature simulation are absent. Sensor resistor and leads are a construction study, not a rebuild procedure.
- [ ] **ECT sensor metal body** — `engine-coolant-temperature-body`; modeled quantity **1**; provisional.
  - Instances: `engine-coolant-temperature-body`
  - Source IDs: ford-cooling-connections, ford-ect-construction, ford-cooling-sensor-circuits, gates-1994-drive, truck-cooling-hose-photos. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Ford identifies the two-lead ECT at the thermostat housing/heater elbow and specifies 3/8-18 NPTF-SPL dry-seal thread. All sensor dimensions, internal thermistor shape and connector detail are provisional.
  - Open: A separate single-wire gauge sender C150 on the RH engine side feeds circuit 39 R/W and grounds through its body. It is not the ECT C183. Gauge sender mounting and the head coolant jacket remain unresolved; no false dry pocket is presented as a coolant connection.
  - Open: Both heater connections use Gates 18767 in the five-speed manual application. Exact hose end assignment, bore, installed cut length and routing are not established here; metal tubes, radii, beads and clearances are illustrative.
  - Open: Owner photos show paired red-orange heater hoses crossing from the firewall toward the front engine. Only attached engine-side metal takeoffs are modeled; full heater/radiator hoses need located vehicle endpoints.
  - Open: The thermostat-side elbow opens into the existing secondary outlet passage; the pump return opens into its existing coolant chamber. Pump/block and outlet/head jacket connections remain incomplete.
  - Open: Ford TSB 94-9-13 describes an E4OD-only radiator bleed tee. That automatic-transmission arrangement is not applied to this manual truck.
  - Open: Thread helices, tapered sealing fits, hose deformation, clamps, harness connectors and coolant/temperature simulation are absent. Sensor resistor and leads are a construction study, not a rebuild procedure.
- [ ] **ECT sensor connector insulator** — `engine-coolant-temperature-insulator`; modeled quantity **1**; provisional.
  - Instances: `engine-coolant-temperature-insulator`
  - Source IDs: ford-cooling-connections, ford-ect-construction, ford-cooling-sensor-circuits, gates-1994-drive, truck-cooling-hose-photos. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Ford identifies the two-lead ECT at the thermostat housing/heater elbow and specifies 3/8-18 NPTF-SPL dry-seal thread. All sensor dimensions, internal thermistor shape and connector detail are provisional.
  - Open: A separate single-wire gauge sender C150 on the RH engine side feeds circuit 39 R/W and grounds through its body. It is not the ECT C183. Gauge sender mounting and the head coolant jacket remain unresolved; no false dry pocket is presented as a coolant connection.
  - Open: Both heater connections use Gates 18767 in the five-speed manual application. Exact hose end assignment, bore, installed cut length and routing are not established here; metal tubes, radii, beads and clearances are illustrative.
  - Open: Owner photos show paired red-orange heater hoses crossing from the firewall toward the front engine. Only attached engine-side metal takeoffs are modeled; full heater/radiator hoses need located vehicle endpoints.
  - Open: The thermostat-side elbow opens into the existing secondary outlet passage; the pump return opens into its existing coolant chamber. Pump/block and outlet/head jacket connections remain incomplete.
  - Open: Ford TSB 94-9-13 describes an E4OD-only radiator bleed tee. That automatic-transmission arrangement is not applied to this manual truck.
  - Open: Thread helices, tapered sealing fits, hose deformation, clamps, harness connectors and coolant/temperature simulation are absent. Sensor resistor and leads are a construction study, not a rebuild procedure.
- [ ] **ECT sensing thermistor · envelope** — `engine-coolant-temperature-thermistor`; modeled quantity **1**; provisional.
  - Instances: `engine-coolant-temperature-thermistor`
  - Source IDs: ford-cooling-connections, ford-ect-construction, ford-cooling-sensor-circuits, gates-1994-drive, truck-cooling-hose-photos. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Ford identifies the two-lead ECT at the thermostat housing/heater elbow and specifies 3/8-18 NPTF-SPL dry-seal thread. All sensor dimensions, internal thermistor shape and connector detail are provisional.
  - Open: A separate single-wire gauge sender C150 on the RH engine side feeds circuit 39 R/W and grounds through its body. It is not the ECT C183. Gauge sender mounting and the head coolant jacket remain unresolved; no false dry pocket is presented as a coolant connection.
  - Open: Both heater connections use Gates 18767 in the five-speed manual application. Exact hose end assignment, bore, installed cut length and routing are not established here; metal tubes, radii, beads and clearances are illustrative.
  - Open: Owner photos show paired red-orange heater hoses crossing from the firewall toward the front engine. Only attached engine-side metal takeoffs are modeled; full heater/radiator hoses need located vehicle endpoints.
  - Open: The thermostat-side elbow opens into the existing secondary outlet passage; the pump return opens into its existing coolant chamber. Pump/block and outlet/head jacket connections remain incomplete.
  - Open: Ford TSB 94-9-13 describes an E4OD-only radiator bleed tee. That automatic-transmission arrangement is not applied to this manual truck.
  - Open: Thread helices, tapered sealing fits, hose deformation, clamps, harness connectors and coolant/temperature simulation are absent. Sensor resistor and leads are a construction study, not a rebuild procedure.
- [ ] **ECT terminal and internal lead** — `engine-coolant-temperature-terminal`; modeled quantity **2**; provisional.
  - Instances: `engine-coolant-temperature-terminal-1`, `engine-coolant-temperature-terminal-2`
  - Source IDs: ford-cooling-connections, ford-ect-construction, ford-cooling-sensor-circuits, gates-1994-drive, truck-cooling-hose-photos. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Ford identifies the two-lead ECT at the thermostat housing/heater elbow and specifies 3/8-18 NPTF-SPL dry-seal thread. All sensor dimensions, internal thermistor shape and connector detail are provisional.
  - Open: A separate single-wire gauge sender C150 on the RH engine side feeds circuit 39 R/W and grounds through its body. It is not the ECT C183. Gauge sender mounting and the head coolant jacket remain unresolved; no false dry pocket is presented as a coolant connection.
  - Open: Both heater connections use Gates 18767 in the five-speed manual application. Exact hose end assignment, bore, installed cut length and routing are not established here; metal tubes, radii, beads and clearances are illustrative.
  - Open: Owner photos show paired red-orange heater hoses crossing from the firewall toward the front engine. Only attached engine-side metal takeoffs are modeled; full heater/radiator hoses need located vehicle endpoints.
  - Open: The thermostat-side elbow opens into the existing secondary outlet passage; the pump return opens into its existing coolant chamber. Pump/block and outlet/head jacket connections remain incomplete.
  - Open: Ford TSB 94-9-13 describes an E4OD-only radiator bleed tee. That automatic-transmission arrangement is not applied to this manual truck.
  - Open: Thread helices, tapered sealing fits, hose deformation, clamps, harness connectors and coolant/temperature simulation are absent. Sensor resistor and leads are a construction study, not a rebuild procedure.
- [ ] **Heater supply and ECT elbow** — `heater-supply-ect-elbow`; modeled quantity **1**; provisional.
  - Instances: `heater-supply-ect-elbow`
  - Source IDs: ford-cooling-connections, ford-ect-construction, ford-cooling-sensor-circuits, gates-1994-drive, truck-cooling-hose-photos, dorman-902-1002, motorad-244-192, water-pump-mounting-topology. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Ford identifies the two-lead ECT at the thermostat housing/heater elbow and specifies 3/8-18 NPTF-SPL dry-seal thread. All sensor dimensions, internal thermistor shape and connector detail are provisional.
  - Open: A separate single-wire gauge sender C150 on the RH engine side feeds circuit 39 R/W and grounds through its body. It is not the ECT C183. Gauge sender mounting and the head coolant jacket remain unresolved; no false dry pocket is presented as a coolant connection.
  - Open: Both heater connections use Gates 18767 in the five-speed manual application. Exact hose end assignment, bore, installed cut length and routing are not established here; metal tubes, radii, beads and clearances are illustrative.
  - Open: Owner photos show paired red-orange heater hoses crossing from the firewall toward the front engine. Only attached engine-side metal takeoffs are modeled; full heater/radiator hoses need located vehicle endpoints.
  - Open: The thermostat-side elbow opens into the existing secondary outlet passage; the pump return opens into its existing coolant chamber. Pump/block and outlet/head jacket connections remain incomplete.
  - Open: Ford TSB 94-9-13 describes an E4OD-only radiator bleed tee. That automatic-transmission arrangement is not applied to this manual truck.
  - Open: Thread helices, tapered sealing fits, hose deformation, clamps, harness connectors and coolant/temperature simulation are absent. Sensor resistor and leads are a construction study, not a rebuild procedure.
  - Open: Automotive front-face photograph establishes the head-front outlet, two diagonal fasteners and adjacent smaller opening, not calibrated positions or dimensions.
  - Open: Dorman902-1002 establishes two .313-inch holes, 1.5-inch catalog outside diameter and separate gasket/main/secondary apertures; neck contours and measurement station remain uncertain.
  - Open: All modeled hole coordinates, gasket contour, neck curvature, bolt engagement and receiver depths are assumptions. Only thermostat flange53.85mmOD/1.27mmthickness are manufacturer dimensions.
  - Open: The head adapter creates bounded local blind coolant receiver pockets with modeled wall material. It does not reconstruct or validate the complete head water jacket.
  - Open: The current longblock front plane X373 and outlet center Y0/Z295 are provisional reference datums. Placement corrects the floating joint without optimizing a belt length.
  - Open: The illustrative thermostat piston front is shortened0.01mm to seat exactly against the existing bridge; this corrects an inherited interference, not a sourced actuator dimension.
  - Open: The adjacent heater-supply passage remains separate from the thermostat-controlled radiator chamber. Its thread and deeper head-jacket connectivity remain unverified.
  - Open: The heater-supply/ECT elbow follows the relocated secondary outlet while retaining the existing engine-side vehicle endpoint(488,-57,335). New bend control points, collar, shoulder and sensor station are provisional; the boss is located1mm farther forward than the rejected trial to clear the outlet casting.

## Additional known scope and reconciliation

- [ ] Verify wet passages, fittings and sensor construction
- [ ] Harness mating connector belongs to engine harness
- [ ] Vehicle heater hoses/clamps are cross-system interfaces

## Cross-system boundaries

Coordinate with [#8](https://github.com/0xZakk/truck/issues/8), [#11](https://github.com/0xZakk/truck/issues/11). Keep the current engine-mounted component here; agree ownership before adding its vehicle-side continuation.

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
