# Engine parts and work breakdown

[Engine ticket](https://github.com/0xZakk/truck/issues/1) · [Engine parts project view](https://github.com/users/0xZakk/projects/2/views/6)

Authoritative tracking snapshot of every current modeled definition and occurrence, plus known missing work. This is not a verified Ford production BOM: unknown variants, quantities and undiscovered internals remain an explicit reconciliation task.

Manifest SHA-256: `821f7d3bb47d49a00ffb2975fa5faffcd306fe90bea48ce7c0d6308cd636653f`. **698 definitions / 1304 modeled occurrences / 70 work packages.** Repeated physical instances share a checklist entry with their modeled quantity; occurrence IDs remain in the JSON inventory.

Existing geometry is credited separately from acceptance. Integrated/candidate packages enter In review for acceptance triage; identified unbuilt work enters Backlog. In review does not assert that known fit/evidence failures have passed. Rejected parts remain open. No worker is implied to be running. Done requires a recorded acceptance decision, not geometry presence.

Engine owns these current engine-mounted models; linked truck-system issues own their vehicle-side continuations. Do not duplicate the same physical part in another system backlog. Boundaries and unknown applicability are called out in each package.

Each package lists every modeled part and its unresolved claims, then the additional known scope. Checklist boxes mean **accepted completion**, not mere geometry existence. The explicit geometry-delivered checkbox credits the existing model without closing unfinished parts.

| Package | Modeled definitions | Modeled quantity | Board status | Ticket |
|---|---:|---:|---|---|
| [Pistons, wrist pins and ring packs](pistons.md) | 5 | 42 | In review | [#21](https://github.com/0xZakk/truck/issues/21) |
| [Connecting rods, caps, bearings and hardware](rods.md) | 6 | 48 | In review | [#22](https://github.com/0xZakk/truck/issues/22) |
| [Crankshaft, main bearings and caps](crank-main.md) | 5 | 36 | In review | [#23](https://github.com/0xZakk/truck/issues/23) |
| [Cylinder block, plugs and dowels](block.md) | 2 | 2 | In review | [#24](https://github.com/0xZakk/truck/issues/24) |
| [Cylinder head, gasket and bolts](head.md) | 3 | 16 | In review | [#25](https://github.com/0xZakk/truck/issues/25) |
| [Pushrod side cover, gasket and hardware](side-cover.md) | 4 | 14 | In review | [#26](https://github.com/0xZakk/truck/issues/26) |
| [Intake/exhaust valves, springs, retainers and keepers](valves.md) | 7 | 72 | In review | [#27](https://github.com/0xZakk/truck/issues/27) |
| [Rocker arms, fulcrums, guides and bolts](rockers.md) | 4 | 48 | In review | [#28](https://github.com/0xZakk/truck/issues/28) |
| [Pushrods](pushrods.md) | 1 | 12 | In review | [#29](https://github.com/0xZakk/truck/issues/29) |
| [Hydraulic lifters and internal components](lifters.md) | 9 | 108 | In review | [#30](https://github.com/0xZakk/truck/issues/30) |
| [Camshaft and cam bearings](camshaft.md) | 2 | 5 | In review | [#31](https://github.com/0xZakk/truck/issues/31) |
| [Timing gears, cam retention and front cover](timing.md) | 9 | 11 | In review | [#32](https://github.com/0xZakk/truck/issues/32) |
| [Rear crankshaft seal and sealing interface](rear-seal.md) | 1 | 1 | In review | [#33](https://github.com/0xZakk/truck/issues/33) |
| [Oil pan, gasket, drain plug and fasteners](oil-pan.md) | 6 | 54 | In review | [#34](https://github.com/0xZakk/truck/issues/34) |
| [Valve cover, gasket and attachment hardware](valve-cover.md) | 2 | 2 | In review | [#35](https://github.com/0xZakk/truck/issues/35) |
| [Oil filler cap and seal](oil-cap.md) | 1 | 1 | In review | [#15](https://github.com/0xZakk/truck/issues/15) |
| [Upper/lower intake manifolds, gaskets and locating hardware](intake.md) | 6 | 12 | In review | [#36](https://github.com/0xZakk/truck/issues/36) |
| [Six fuel injectors and their internal components](injectors.md) | 11 | 78 | In review | [#37](https://github.com/0xZakk/truck/issues/37) |
| [Fuel pressure test valve and cap](fuel-test.md) | 8 | 8 | In review | [#38](https://github.com/0xZakk/truck/issues/38) |
| [Fuel supply/return spring-lock couplings](fuel-couplings.md) | 14 | 16 | In review | [#39](https://github.com/0xZakk/truck/issues/39) |
| [Fuel rails, return tube and retaining hardware](fuel-rail.md) | 4 | 8 | In review | [#40](https://github.com/0xZakk/truck/issues/40) |
| [Fuel regulator vacuum hose and fitting](regulator-vacuum.md) | 2 | 2 | In review | [#41](https://github.com/0xZakk/truck/issues/41) |
| [Fuel pressure regulator and internals](fuel-regulator.md) | 11 | 13 | In review | [#42](https://github.com/0xZakk/truck/issues/42) |
| [Throttle body, shaft, plates and mounting hardware](throttle.md) | 6 | 13 | In review | [#43](https://github.com/0xZakk/truck/issues/43) |
| [Throttle cable bracket](throttle-bracket.md) | 0 | 0 | In review | [#16](https://github.com/0xZakk/truck/issues/16) |
| [Idle-air control valve and internals](iac.md) | 8 | 8 | In review | [#44](https://github.com/0xZakk/truck/issues/44) |
| [Throttle-position sensor and internals](tps.md) | 6 | 7 | In review | [#45](https://github.com/0xZakk/truck/issues/45) |
| [Front/rear exhaust manifolds, mounting and outlet joints](exhaust.md) | 7 | 7 | In review | [#46](https://github.com/0xZakk/truck/issues/46) |
| [Water pump, impeller, shaft, seal, bearing and pulley](water-pump.md) | 11 | 17 | In review | [#47](https://github.com/0xZakk/truck/issues/47) |
| [Thermostat, coolant outlet and fasteners](thermostat.md) | 12 | 13 | In review | [#48](https://github.com/0xZakk/truck/issues/48) |
| [Heater fittings and two-wire ECT sensor](heater-ect.md) | 6 | 7 | In review | [#49](https://github.com/0xZakk/truck/issues/49) |
| [Ignition coil mounting bracket and fasteners](coil-bracket.md) | 7 | 7 | In review | [#50](https://github.com/0xZakk/truck/issues/50) |
| [Spark-plug leads and coil-to-distributor lead](ignition-leads.md) | 42 | 42 | In review | [#51](https://github.com/0xZakk/truck/issues/51) |
| [Ignition coil and internals](coil.md) | 9 | 10 | In review | [#52](https://github.com/0xZakk/truck/issues/52) |
| [Remote ignition module, heat sink and connector](ignition-module.md) | 5 | 7 | In review | [#53](https://github.com/0xZakk/truck/issues/53) |
| [Spark plugs and internal construction](spark-plugs.md) | 9 | 54 | In review | [#54](https://github.com/0xZakk/truck/issues/54) |
| [PCV valve, grommet and crankcase ventilation](pcv.md) | 6 | 6 | In review | [#55](https://github.com/0xZakk/truck/issues/55) |
| [Oil-pressure switch and electrical connection](oil-pressure.md) | 9 | 9 | In review | [#56](https://github.com/0xZakk/truck/issues/56) |
| [EGR valve-position sensor and internals](evp.md) | 16 | 16 | In review | [#57](https://github.com/0xZakk/truck/issues/57) |
| [EGR vacuum regulator and internals](evr.md) | 4 | 4 | In review | [#58](https://github.com/0xZakk/truck/issues/58) |
| [EGR exhaust tube and connections](egr-tube.md) | 4 | 4 | In review | [#59](https://github.com/0xZakk/truck/issues/59) |
| [EGR vacuum hoses and supports](egr-vacuum.md) | 1 | 1 | In review | [#60](https://github.com/0xZakk/truck/issues/60) |
| [EGR valve and vacuum actuator](egr-valve.md) | 14 | 15 | In review | [#61](https://github.com/0xZakk/truck/issues/61) |
| [Flywheel, ring gear and crankshaft bolts](flywheel.md) | 3 | 8 | In review | [#62](https://github.com/0xZakk/truck/issues/62) |
| [Clutch pilot bearing and internals](pilot-bearing.md) | 4 | 19 | In review | [#63](https://github.com/0xZakk/truck/issues/63) |
| [Crankshaft damper, pulley, key and retaining hardware](damper.md) | 6 | 6 | In review | [#64](https://github.com/0xZakk/truck/issues/64) |
| [Belt tensioner, pulley and internals](tensioner.md) | 8 | 8 | In review | [#65](https://github.com/0xZakk/truck/issues/65) |
| [Accessory support castings and mounting hardware](carriers.md) | 23 | 23 | In review | [#66](https://github.com/0xZakk/truck/issues/66) |
| [Alternator, pulley and internal components](alternator.md) | 26 | 26 | In review | [#67](https://github.com/0xZakk/truck/issues/67) |
| [Power-steering pump, reservoir, pulley and internals](steering-pump.md) | 46 | 46 | In review | [#68](https://github.com/0xZakk/truck/issues/68) |
| [Thermactor air pump, pulley and internal components](thermactor.md) | 17 | 17 | In review | [#69](https://github.com/0xZakk/truck/issues/69) |
| [Fan clutch and cooling fan](fan-clutch.md) | 13 | 35 | In review | [#70](https://github.com/0xZakk/truck/issues/70) |
| [Distributor, drive, cap and rotor](distributor.md) | 19 | 28 | In review | [#71](https://github.com/0xZakk/truck/issues/71) |
| [Oil-pump intermediate shaft and retainer](oil-drive.md) | 2 | 2 | In review | [#72](https://github.com/0xZakk/truck/issues/72) |
| [Oil pump, gerotor, relief valve and mounting](oil-pump.md) | 10 | 14 | In review | [#73](https://github.com/0xZakk/truck/issues/73) |
| [Oil pickup, strainer and support](pickup.md) | 3 | 3 | In review | [#74](https://github.com/0xZakk/truck/issues/74) |
| [Oil filter, mounting insert and gallery interface](filter.md) | 14 | 14 | In review | [#75](https://github.com/0xZakk/truck/issues/75) |
| [FS10 A/C compressor, clutch and internal components](ac-compressor.md) | 67 | 67 | In review | [#76](https://github.com/0xZakk/truck/issues/76) |
| [Starter motor, reduction, drive and solenoid](starter.md) | 132 | 132 | In review | [#77](https://github.com/0xZakk/truck/issues/77) |
| [Engine oil dipstick](dipstick.md) | 0 | 0 | In review | [#17](https://github.com/0xZakk/truck/issues/17) |
| [Dipstick guide tube, seat and retaining hardware](dipstick-tube.md) | 0 | 0 | Backlog | [#78](https://github.com/0xZakk/truck/issues/78) |
| [Engine mounting brackets, isolators and hardware](engine-mounts.md) | 0 | 0 | Backlog | [#79](https://github.com/0xZakk/truck/issues/79) |
| [Air cleaner, filter and intake ducts](air-cleaner.md) | 0 | 0 | Backlog | [#80](https://github.com/0xZakk/truck/issues/80) |
| [Vacuum tree, hoses, caps and retainers](vacuum-network.md) | 0 | 0 | Backlog | [#81](https://github.com/0xZakk/truck/issues/81) |
| [Engine wiring harness, connectors and grounds](engine-harness.md) | 0 | 0 | Backlog | [#82](https://github.com/0xZakk/truck/issues/82) |
| [Thermactor hoses, valves and manifold plumbing](air-injection.md) | 0 | 0 | Backlog | [#83](https://github.com/0xZakk/truck/issues/83) |
| [Engine coolant hoses, clamps and sender interfaces](coolant-hoses.md) | 0 | 0 | Backlog | [#84](https://github.com/0xZakk/truck/issues/84) |
| [Engine rear plate, lifting and boundary hardware](engine-boundary-hardware.md) | 0 | 0 | Backlog | [#85](https://github.com/0xZakk/truck/issues/85) |
| [Accessory drive belt and installed routing](accessory-belt.md) | 0 | 0 | In review | [#86](https://github.com/0xZakk/truck/issues/86) |
| [Engine physical BOM and variant reconciliation](bom-reconciliation.md) | 0 | 0 | Backlog | [#87](https://github.com/0xZakk/truck/issues/87) |

## Rebuild and audit

`python3 scripts/build-engine-work-breakdown.py` regenerates this index and all package pages from the manifest, curated scope and persisted GitHub issue mapping. It fails on an unmapped definition and checks occurrence coverage. Update the curated scope when new part families appear. Do not infer Done from file existence or close an issue solely because a worker stopped.

To record a later status change in this snapshot, update tracking_status and tracking_reason in the curated scope. Done also requires acceptance_record pointing to the reviewed handoff in the repository. Regenerate and review the change; do not infer acceptance from file existence. The board is the operational status authority after import; this generated snapshot records the import assessment. Review status decisions against current handoffs before future updates; the generator does not overwrite GitHub statuses.
