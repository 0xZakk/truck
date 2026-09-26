# Local coolant-outlet/head interface candidate

The original outlet assembly was located atX415 with a gap to the head front. This candidate seats its gasket at the provisional head frontX373, places the thermostat's1.27mm flange in a shallow head recess, and adds two blind bolt receivers. An automotive ATKDFF8 front-face photograph supports direct head-front mounting with adjacent main/smaller fluid openings and diagonal fasteners. A manufacturer photograph of Dorman902-1002 supports the two-aperture gasket and separate hose-neck/secondary-boss construction. Neither photograph establishes millimeter coordinates.

## Integration API

Use `cad/engine/coolant_outlet_head_candidate.py` as a composable adapter:

1. Apply `head_interface(current_head_definition)` after the other accepted head adapters, including the valve changes. The input is head-local geometry, not the installed global head. The adapter adds/cuts only the forward local receiver region; do not replace the entire head with the preview baseline.
2. Replace definitions returned by `parts()`: coolant outlet housing, gasket, bolt, thermostat piston and heater-supply/ECT elbow. The elbow is world-coordinate geometry, as in the existing definition; the other four definitions remain local to their assemblies.
3. Set `coolant-outlet-assembly.position_cad_mm` to the absolute `POSITION=(373,0,295)`.
4. Set `thermostat-assembly.position_cad_mm` to absolute `THERMOSTAT_POSITION=(-.635,0,0)`, retaining its parent coolant-outlet-assembly. All nine thermostat definitions/occurrences otherwise retain their placements, apart from the corrected piston definition.
5. Set coolant-outlet-bolt-1 local position to `(0,-27,29)` and bolt-2 to `(0,32,-25)`. Retain their rotations.
6. Set all five `engine-coolant-temperature-assembly` occurrence positions using `ect_position(identifier)`: body/insulator/thermistor at `(423,-36,315)`, terminal1 at `(421.5,-36,315)`, terminal2 at `(424.5,-36,315)`. Keep current rotations. The supply elbow occurrence remains at the origin because its geometry is already world-coordinate.
7. Register/reuse sources `dorman-902-1002`, `motorad-244-192`, `water-pump-mounting-topology`, and the existing cooling-connection source IDs supplied by the module. Include its uncertainty notes. No new parts or occurrence counts are required.

Absolute group placement and the head adapter are idempotent. The piston front shortens0.01mm to meet the existing bridge plane rather than penetrate it; its rear endpoint is unchanged. That corrects an inherited illustrative geometry interference, not a manufacturer dimensional specification.

## Functional and source limits

The two local coolant pockets have explicitly modeled rear and upper walls. They do not reconstruct a complete head water jacket. The smaller branch remains separate from the thermostat-controlled radiator chamber; no invented bypass channel joins them. Its attached heater-supply elbow and ECT follow the established cooling-connection topology. Exact thread form and deeper head-jacket connections remain unresolved.

The attached supply elbow inserts into the relocated secondary outlet at `(400,-42,295)`. An illustrative shoulder contacts the boss front atX410.2. Its new route retains the old vehicle-interface endpoint `(488,-57,335)`. The five sensor components move coherently onto the new straight section. The pump return remains independent and unchanged by this module.

Bolt coordinates, gasket outline/thickness, wall thickness, receiver depth, neck curvature and axial projection are approximate. The front-face topology and contact model are the supported improvement. No belt length or pulley position was optimized here.

Source observations and exclusions are in `reference/engine/coolant-outlet-head-interface-reviewed.json`. Original manufacturer photograph: `reference/engine/dorman-902-1002-manufacturer-photo.jpg`. The ATKDFF8 front view is registered by the water-pump research packet.

## Verification workflow

Run `scripts/check-coolant-outlet-head-candidate.py --assembly-root PATH` against a coherent, frozen full assembly. It loads the assembly's own valve-aware transforms and deformed spring definitions, checks every changed part against the complete engine, round-trips the20 changed solids, and verifies sealing/fastener/thermostat/supply/sensor contacts. Void/material probes check both local receivers, the rear floor and separation from the rocker space. Additional flow probes check the secondary-outlet-to-supply bore, the entire supply tube and clearance around the wet sensor tip. Reapplying the head adapter must not change its shape. Deliberate gasket withdrawal/penetration must be detected.

The first audit rejected an inherited0.070686mm³ thermostat piston/bridge overlap; the0.01mm piston correction addresses it without changing the0.01mm³ interference threshold. Preserve `inventory/engine/coolant-outlet-head-rejected-piston-validation.json` as the rejected history. The final candidate and actual-installed reports determine acceptance; this document itself is not evidence of passing checks.

The local-joint-only candidate passed14STEProundtrips,255exact intersection checks, all6joint contacts,5material/void probes and both negative controls on post-valve manifest4b847d7b3d3de16ceeb3a209277cd909fc953fe729a17128efe317d2a832f059. Its report is preserved as `inventory/engine/coolant-outlet-head-local-only-validation.json`; it did not yet relocate the dependent supply elbow/sensor and must not be promoted as a complete attached assembly. The expanded candidate's report supersedes it only after those dependencies pass their own checks.

The final expanded candidate passed on manifest `6b11c0f874bb53638b0e7fd0f477f6b7d5fca4df928bcbc918b37c98cb01d94f`: 20 STEP round trips, 265 exact intersections, zero failures, all 8 joint contacts, 5 receiver/rocker-space probes and 3 flow probes. Gasket withdrawal/penetration and a deliberately blocked flow path were detected. The 20-part assembled/exploded preview was visually reviewed at `reference/engine/coolant-outlet-head-preview.png`; the cropped head is a preview-only representation.

The expanded trial's sleeve/boss interference is preserved in `inventory/engine/coolant-outlet-head-rejected-sleeve-validation.json`. Extending the existing secondary bore through the intersecting taper wall and moving the provisional ECT boss/sensor 1mm forward removed the interference. No collision tolerance was relaxed. Final module SHA256: `9aeaa1fd3d3693a64643a120808aa74820d8f58695daf62c79ef7c4bf1a95fc7`.

After integration, run the same checker with `--installed`. It compares all20actual saved placed solids to the expected geometry/placement (for the head, reapplying the local adapter must change nothing), then uses the actual saved solids for all contact, collision and receiver checks. Its installed report is written within the requested assembly root.
