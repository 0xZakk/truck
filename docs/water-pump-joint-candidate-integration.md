# Pump-to-block candidate: integration contract

This candidate corrects the floating pump rear flange using source photographs. It is not a dimensionally verified Gates44009 replica or a complete cooling system.

## Evidence and boundaries

Register sourceID `water-pump-mounting-topology` with `reference/engine/water-pump-mounting-topology-reviewed.json`. It records exact Gates44009 and Fel-Pro13816 product photos, existing manufacturer application evidence, and the ATKDFF8 automotive block-front photo. Photos support four pump fasteners, the gasket's separate larger fifth aperture, an impeller behind the flange, and a flange directly on the block front. They do not establish millimeter dimensions or the fifth opening's function.

The candidate places the gasket at modeled blockfrontX373–375 and the casting flange atX375. Its provisional pump axis isY−32/Z170, opposite the cam as the block photo suggests. The housing tapers from the rear flange toward the existing bearing nose. HubX, bearing/seal/slinger axial locations and heater tube shape are retained; the shaft length and impeller axial position change. The83mm chamber depth remains an assumption. The deeper block coolant jacket, fifth-aperture routing and radiator inlet neck remain incomplete. No pressure/flow or production fit is claimed.

## Builder hooks

1. Import `water_pump_joint_candidate as p` and `water_pump_thermactor_foot_candidate as t`.
2. After existing block adapters, apply `p.block_interface(t.block_interface(block))`. The support adapter closes the former Thermactor upper socket and creates a new dry blind socket. The pump adapter opens only the demonstrated front receiver and four assumed blind mounting sockets; it preserves the front cylinder wall.
3. Wrap the existing eight-component pump builder API with `p.adapt_api`. This replaces only housing, gasket, impeller and shaft definitions. Keep existing IDs; do not add a second gasket. Add `p.build_hardware((define,add,group))` once, yielding one new definition and four occurrences.
4. Set water-pump-assembly position to `(440,-32,170)` and fan-clutch-assembly to `(530,-32,170)`. The pulley inherits the pump shift. Translate only occurrence `heater-pump-return-elbow` byY−32; its world-coordinate definition remains unchanged. `p.shifted_manifest` documents the exact transformation from the unchanged old manifest, but must not be applied twice or after equivalent builder changes.
5. Replace definition `thermactor-support-bracket` with `t.support()` and `thermactor-engine-bolt-2` with `t.upper_bolt()`. Both remain world-frame definitions under their original assembly. Upper foot moves fromY−100/Z180 toY−125/Z140; lowerfoot and pump ears remain. All dimensions/load-path details are provisional. This avoids the old arbitrary support anchor occupying the source-derived pump bolt location.
6. Merge the new source IDs and `p.GAPS`/`t.GAPS` into affected definitions. Replace stale text claiming the pump gasket is a plain ring or its block joint is entirely absent. Preserve unresolved internal bearing/seal/radiator/jacket limitations. Merge `inventory/engine/water-pump-joint-learning.json`.
7. Update the belt's WPcenterY to−32 and re-audit tangent spans and accessory envelopes. The CAD neighbor audit does not include the separately generated belt planning path. Do not claim catalog belt length or a measured axis position.

## Candidate verification

`check-water-pump-joint-candidate.py`:56changed solid occurrences,154exact checks, zero collisions on the frozen90807873baseline. It includes displaced pump pulley, fan/clutch and heater return plus relocated Thermactor support. Both original and new bracket/block interfaces are geometry studies, not factory castings.

`check-water-pump-joint-interfaces.py`: front cylinder region unchanged; the full gasket backed on both sides; main and fifth front apertures open; four pump sockets and relocated accessory socket blind with retained floors. These controls do not establish the deeper coolant circuit or actual fifth-port function.

`export-check-water-pump-joint.py`: eight modified/new definitions pass valid single-solid STEP roundtrips with adaptive-volume tolerance0.02mm³. It exports actual assembled and sectioned mesh artifacts for visual inspection.

Before integration, rerun these on an unchanged isolated pre-joint snapshot containing the newest root changes. Preserve its manifest, STEP files and accepted candidate report. After integration run `check-water-pump-joint-installed.py --baseline-root <that snapshot>` to compare eight definitions and all affected rigid poses. That installed checker is syntax-checked but has not yet been run against a published build.

`check-water-pump-impeller-sweep.py` also passed a conservative annular envelope containing every rotation of the modeled impeller, with zero neighbor collisions. It proves geometric rotation clearance, not vane identity, direction, speed or hydraulic performance. Actual assembled/sectioned mesh visually reviewed at `reference/engine/qc/water-pump-joint-candidate.png`.

Fullengine motion, separate belt planning, browser navigation/explode behavior and source-side dimensions remain root integration checks. The candidate is not published by these scripts.
