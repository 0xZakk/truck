# Fuel rail numeric layout review

## Contract

Issue #82/engine #1. Root owns integration/Git; contributor owns fuel-rail-layout-20261003-prefixed source-comparison script, reference artifacts and this contract only. Baseline aca7a20a98804563f90647c98d2ddfd89dcca184 on engine/fuel-exhaust-hosts-20261003. Research/numeric proposal before CAD; root must review this concrete proposal before coordinated candidate construction. No shared edits or changes to frozen intake/return records.

Evidence is the frozen intake-return-interface-20261003 package: actual Ford1994 V5855-F and actual physical1987 rail views1/6, with URLs/hashes already recorded. No new original redistributed. Numeric files are `reference/engine/fuel-rail-layout-20261003-{measurements,parameters}.json`; authored review figure is matching `-review.png`. Script uses system Python/numpy/scipy/matplotlib; no CAD runtime needed.

## Registration and uncertainty

Identify I1 at the front loop/regulator end and I6 at paired rear connectors, using Ford's front arrow. Manual socket-mouth pixel coordinates and feature picks are preserved. In each view, project onto the I1→I6 image chord and fit a three-coefficient one-dimensional projective mapping for ordered stations q=0..5. This is a longitudinal comparison, **not calibrated 3-D registration**. Off-row regulator/mount/connector features are perspective-biased. Mouth centers and tilt contribute bias; no contour accuracy is claimed.

Physical view1 socket fit RMS6.611px, regulator projected q=.875; Ford drawing RMS2.153px, regulator q=.645. Deterministic1000-sample perturbation gives physical .644–1.098 and Ford .375–.891 for the specified pick/projection perturbations. These are sensitivity scenarios, not statistical confidence or factory tolerance. Wider review range q=.3–1.3 brackets uncertain depth/attachment identification. Nominal q=.75 is an explicit source-compared estimate.

Protected model coordinates are I1X259.48 to I6X−309.48 atY−163, injector groupZ294, each axis+Z. The five intervals113.792mm and endpoint568.96mm are existing-model anchors, not an image ruler or new factory measurement. Three protected lower rail seat centers are X220,−40,−250/Y−178/Z363.95; retain actual existing seat solids and bolt axes, not merely those sampled bands.

The protected mount q values are .347,2.632,4.477. Physical projected holes .624,2.648,4.678 and Ford .355,2.291,4.810 differ by up to about .34 interval. Do not silently move mounts to make a picture fit; transverse/depth projection and schematic drawing are unresolved. Preserve three mounting stems/seats and report the resultant source discrepancy.

Rear mouths project to q4.58/5.08 in the photograph and5.49/5.94 in Ford; their raised height makes these unsuitable as exact longitudinal stations. Proposed5.4/5.2 and front-loop tip−.3 are estimates with broad review ranges4.4–6.1 and−.8–.1. They must not be described as measured endpoints.

## Proposed numeric contract for root review

Full machine-readable values and review ranges are in parameters.json. All following spatial values are **proposed estimates**, not accepted geometry.

| Interface | Proposed value mm | Basis / sensitivity |
|---|---|---|
| Regulator group origin | (174.136,−139,385), no rotation | q=.75; q=.3–1.3 gives X225.3424…111.5504; nominal transverse+24 and height retained385; Y offset16–40/Z377–393 review |
| Supply main run | Y−163/Z369, OD12/ID9 | Existing injector cup interfaces and tube study dimensions retained |
| Adjacent return run | Y−139/Z369, OD8/ID5.6 |24mm separation estimate; side is unresolved |
| Front supply loop tip | X293.618 at nominalZ369 | Ahead of I1; R18 centerline estimate, review12–30; OD12/ID9 inherited |
| Rear supply coupling origin | (−354.997,−163,410) | q5.4, upturned+Z; R18 nominal bend |
| Rear return coupling origin | (−332.238,−139,410) | q5.2, upturned+Z; R12 nominal bend |
| Coupling frames | group rotation(0,90,0)deg | Existing children use(0,−90,0), so combined exit+Z; tilt±20deg review, roll unresolved |
| Return bend radius / seal lead | R12 /15 | Explicit estimates; reviewR8–24, finite tangent geometry required |
| Regulator vacuum start | (174.136,−139,420), tangent+Z | Same existing nipple engagement in moved group |
| Vacuum manifold endpoint | (0,−55,460), tangent+Y | Existing fitting/port preserved; OD12/ID8.2/socketID8.3 retained estimates |
| Diagnostic fitting | (100,−163,378) | Existing estimate/IDs retained initially, not evidence of exact factory station |

**Y sign remains unresolved.** +Y toward head is only the primary review hypothesis; mirror regulator/return offsets across Y−163 to Y−187 is retained as an explicit alternative. Neither is selected because it clears H9. The present source views alone cannot prove installed transverse sign/depth. Root can authorize both bounded variants for comparative review or require an additional source-side correspondence. No definitive side choice or installed approval is implied.

Supply topology must loop from the front end of the six-cup rail into the regulator inlet. Return outlet remains separate and runs beside the rail toward its rear coupling. A coincident central bore cannot substitute for two communicating input/output paths. During CAD contract amendment, freeze flange inlet/outlet regions and their nonintersection before sweeping tubes; exact front-loop transitions are not defined by the schematic plot. Keep injector cups and three mounts unchanged. Minimum centerline radius greater than OD/2 is only a geometric condition, not a manufacturing bend limit; tube material/flattening/production minimum remain unknown.

The vacuum control polygon in parameters.json is an estimated smooth curve from the moved nipple to the unchanged fitting; it is not owner routing. Recompute socket straight lead and curvature, test continuity and all neighbors. Do not change the upper manifold port to rescue this routing. New regulator location invalidates previous vacuum hose/seat context checks.

## Stable IDs and invalidated checks

Keep fuel-system, fuel-rail-assembly, fuel-regulator, fuel-injector-1…6 and all injector child IDs. Change fuel-supply-rail and fuel-return-tube definitions coherently. Move the entire regulator group, preserving these13 occurrences and relative construction initially: regulator-lower-housing, regulator-upper-housing, regulator-diaphragm, regulator-spring-seat, regulator-spring, regulator-gasket, regulator-valve-seat, regulator-valve, regulator-inlet-screen, regulator-o-ring, regulator-screw-1…3. Do not move only its outside shell. Internal function remains an illustrative study; unchanged relative positions do not prove factory internals.

Preserve both fuel-supply-coupling and fuel-return-coupling group IDs with male/cage/female/two seals/spring/clip/tether children. Reorient whole groups; seal offsets and socket geometry must travel with mating frames. Existing return clip180deg clearance clocking remains an unaccepted estimate, not a reason to suppress new tool/ear conflicts. Keep regulator-vacuum-line, regulator-vacuum-hose/fitting and fuel-test-valve group/children stable. Preserve six injector upper/lower seats, head/injector axes and three mount hardware stacks; no interface relocation hidden in a rail rewrite.

Invalidated: rail/regulator fuel passages; regulator-to-rail gasket/O-ring engagement; all moved regulator versus neighbors; both coupling seating/retention/tool/extraction paths; vacuum nipple engagement/route context; rail diagnostic passage; full intake candidate context versus all changed fuel occurrences; all explosion/disassembly and browser results for affected IDs. Existing broad lower-region Boolean failure remains open and is not healed by fuel work.

## Checks and delivery

Command: `MPLCONFIGDIR=/tmp/fuel-rail-layout-mpl python3 scripts/fuel-rail-layout-20261003-review.py`. Fixed RNG seed20261003. No original image needed for replay of digitized results; verification against originals uses prior source hashes/URLs. Authored plot inspected. Script syntax PASS. Application/topology PASS from exact-year drawing; numeric source comparison bounded as above. Dimensions/coordinates proposed estimates; CAD/export, full installed interfaces, fastener/motion/browser NOT RUN. No CAD acceptance.

After root numeric review, create a new isolated candidate prefix with frozen accepted parameters and amendments. Exact solids/unit/export checks; source-render comparison; retained seats comparison; finite bend/minimum-section/passages; blocked passage/shifted frame/reversed coupling controls; whole-scene exact context with all affected groups; rear H9/fastener/tool and removal sweeps. Preserve source ear and all nine gasket apertures. Do not inherit a previous13-neighbor or4062-pair pass after these moves.

Gasket outer contour and upper exterior restoration remain separate tasks in the return-interface handoff; this proposal does not waive either. No Git/shared edits, no process running. Root review pending; issue open. Model/usage unavailable.
