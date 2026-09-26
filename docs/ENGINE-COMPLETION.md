# Engine reconstruction status

The owner's target remains **every physical component**, each with its own page,
assembled in the correct location at a common scale. The engine is **not finished**.
The live counts in `inventory/engine/full-assembly.json` describe modeled content, not a
verified complete bill of materials. Repeated parts share geometry and retain
independent identities. Passing CAD checks does not verify Ford manufacturing geometry.

## Available now

The saved assembly now contains 688 definitions and 1,244 occurrences. Added
studies include accessory supports, alternator, CII steering pump, FS10 compressor,
Thermactor exterior, fan/clutch, secondary ignition leads, filter mounting insert
and a 132-component manual PMGR starter study. The starter remains retracted and
stationary, with no claimed bellhousing support or complete solenoid/overrun action.
Separate pull/hold winding envelopes, S/B/M terminals and an insulated contact bridge
are represented. A provisional slotted-clevis/fork linkage now passes17 sampled
saved-STEP poses and945 neighbor checks; production joint geometry and loaded
engagement remain unverified. Four coil-end conductors and four insulating sleeves
are published. Their initial interpenetrating junctions failed whole-assembly QC;
a separately checked nonpenetrating correction now passes installed contact,
clearance and whole-static checks. Motor feed, its frame grommet, four brush
pigtails and a ground bridge are now represented and checked. Commutator/armature
interconnections, vehicle cables and loaded electrical operation remain unresolved.
The67-part FS10 study now includes a sourced30×55×23mm clutch-bearing
envelope, rear manifold/two seals/bolt and two separately identified radial shaft
support cartridges. Bearing internals, gland compression and production fit remain
unresolved; the radial cartridge dimensions are assumptions, not catalog dimensions.
The manifold-boss passage obstruction is corrected: complete suction/discharge
probe networks and the blind bolt socket pass installed verification, not a
pressure-tightness or operating-performance certification.
Accessory stations and many internal dimensions remain provisional. The current
belt-layout study does not match the catalog effective length; a longer comparison
loop is not an accepted installed belt. Tensioner internals remain incomplete.

A three-part front manifold lifting-eye study now represents the spanning eye,
shoulder stud13 and bolt14. Its four adapted interfaces include provisional
casting pads and head socket bosses. Applicable1994 installation text and a
later1996 factory comparison support the arrangement, not its dimensions or
lifting capacity. Candidate interfaces pass contact, socket-wall/floor and
neighbor checks. Installed verification passes seven shape matches,335 neighbor
checks and20 interface measurements; whole-static verification passes4,539 checks
with no overlaps above0.1mm³. Corrected exploded spacing and offline renders also
pass their limited checks. Fourteen other
manifold attachment stations and production coolant-gallery compatibility remain
unresolved. Do not use the modeled bracket as lifting-equipment guidance.

A separate intake locating-dowel comparison is integrated with three revised
joint interfaces. Its7.9375×25.4mm size comes from a1996 table, not verified1994
hardware. Candidate socket-wall/floor, clearance and repeat-build checks pass;
installed checks pass four saved-shape matches, socket probes and three exact
joint/neighbor checks. Exploded display and actual-STEP cutaway inspection pass;
the new whole-static audit passes4,542 checks with no overlaps above0.1mm³.
Station, fits, pad sections and production
gallery compatibility remain assumptions. The dowel locates, not clamps, the joint.

The front-exhaust form correction is published: manufacturer-supported
rounded-rectangular entries and a blended collector replace the circular-mouth,
box-collector abstraction. Matching head entries preserve open transitions;
candidate neighbor, passage, corner-control and positive rim checks pass.
At the front-profile checkpoint, installed audits pass, including4,542 static intersection checks
with zero overlaps above0.1mm³. The capsule collector, dimensions,
flange contours and outlet remain provisional, not a traced production casting.

Rear rounded-rectangular entries, matching head transitions and a shortened
provisional EGR fitting insertion are now published. The candidate passes three
STEP roundtrips,212 neighbor checks,36 passage checks,24 corner controls and six
rim bands; isolated entry and fitting cutaways were inspected. Installed rear
verification passes the same checks and three actual STEP matches on manifest
90807873; actual saved-STEP fitting and published exhaust renders were inspected.
Whole-static passes4,542 exact checks with zero overlaps above0.1mm³; front,
eye, dowel and exploded-view regressions also pass. The retained rear box collector and
collector-end EGR routing remain unsupported by the reviewed replacement's
auxiliary bosses near its discharge neck. Correcting entry shape and fitting
intrusion does not complete the rear casting, threads, route or production fit.

The Melling IS-74 shaft is now integrated with a reconciled provisional tilted
drive axis, cam engagement, pump socket and mounting interfaces. Conjugate gerotor
motion passes sampled installed checks, but production gear/rotor dimensions and
hydraulic performance remain unverified. Earlier rejected-axis reports are history,
not the current arrangement. The filter boss supports the gasket and separates
its eight inlets from the central return; pump/main-gallery connections and the
E4TZ anti-drainback service insert remain missing. See `docs/NEXT-SESSION.md` for
the current build/checkpoint and pending component work.

- `/viewer/engine.html`: current assembly with assembly-to-part navigation,
  breadcrumbs, global component search, exploded layout, cutaway and transparent
  castings. Six cylinders share a crank mechanism with independent phases.
- `/viewer/part.html?id=<occurrence-id>`: a dedicated view of any modeled component,
  with explanation, evidence, unresolved details, model dimensions, STEP download
  and a link back to its place in the engine.
- `/viewer/piston-study.html`: the original focused mechanism study, preserved.
- `cad/engine/generated/full-assembly.step`: assembled CAD at the reference pose,
  in millimeters. Individual STEP files are regenerated by the build.

The core includes the six piston/ring/pin/rod assemblies; six-throw crankshaft;
block, seven caps and bearing pairs; head, fourteen head bolts and gasket; twelve
valve/spring/keeper assemblies; twelve pushrods, rockers and nine-component
hydraulic lifters; camshaft and four bearings; timing gears and several closures.

## Completion gates still open

| Assembly | Current state | Required before calling it finished |
|---|---|---|
| Piston and rod | Separate CAD components and solved motion | Verify installed piston/rod identity, pin offset/retention, forging contours, ring profiles and oil-expander construction |
| Crank and main bearings | Six throws, seven supports, sampled fit checks | Counterweight contours, fillets, oil passages, thrust bearing, axial dimensions, keys, flange and fastener pattern |
| Block | Bores, factory-range lifter bores and a14-part side-cover study | Applicable casting dimensions/scans, jackets, galleries, plugs, dowels, mounts, cover contours and seal/fastener fit |
| Head | Chambers, ports and pedestals are provisional | Exact chamber and port surfaces, coolant/oil passages, seats/guides, plug bores and fasteners |
| Valvetrain | Separate components; factory-range cam journal, bearing ID and lifter OD; revised rocker-cover clearance | Applicable cam profile, valve timing, axial stations, rocker geometry/ratio, spring dimensions and coordinated operating motion |
| Timing drive | Involute teaching gears, keyed cam nose, seven-part retention study and revised cover cavity | Truck-specific tooth counts/materials, helix, pressure angle, marks, key/hub dimensions, installed hardware identities and casting interfaces |
| Lubrication | Pump/rotor/relief/pickup, filter internals, pressure-switch and rear-sump pan/drain studies | Verify production contours and installed interfaces; intermediate drive, filter adapter, dipstick, galleries/plugs, pan hardware and complete seal geometry remain unfinished |
| Induction and exhaust | Hollow intake castings, throttle/IAC/TPS studies, decomposed injectors, rail/regulator and split exhaust castings | Verify casting contours, ports and placement; finish throttle linkage/IAC hardware, exhaust details and head fasteners, rail supports/couplings, fuel wiring, vacuum and EGR components |
| Cooling | Water-pump, thermostat and coolant-outlet component studies | Production internals/castings, seals, passages, mounting hardware, pulley/fan and hose interfaces |
| Ignition and accessory interfaces | Distributor, six decomposed plugs, coil, module and damper studies | Installed variants, distributor drive, leads/harness, brackets, capacitor, pulley and accessory interfaces |
| Closures and rear interface | Several covers and gaskets modeled | Truck sump/stamping profiles, end seals, full hardware count, flywheel, pilot bearing and clutch boundary |

## Evidence limits

The 1994 factory archive establishes many part identities, procedures and service
dimensions. Silvolite and Hastings provide applicable replacement dimensions.
The industrial Ford manuals are useful comparison sources, but their earlier
parts and dimensions cannot silently become 1994 truck specifications.

The current bore pitch (113.792 mm), deck height (254 mm), casting envelopes,
cam/valve/rocker locations and many small-part dimensions remain modeling
assumptions. They are sufficient to establish a consistent CAD study, not to
measure or manufacture replacement parts. The fixed valvetrain is not an operating
valve-timing simulation; the rotating mechanism, gear ratio and idealized throttle plates animate.

To close geometric accuracy, seek applicable dimensioned drawings, a trustworthy
CAD/scan with provenance, or measurements of matching production components.
Exterior photos can improve casting and attachment detail; internal surfaces and
hidden dimensions need stronger references. No teardown is necessary merely to
use or improve the current viewer.

## Verification and reproduction

Use `cad/engine/README.md` for commands. The reports are
`inventory/engine/atlas-validation.json` (sampled rotating/core interfaces) and
`inventory/engine/atlas-static-validation.json` (all pairs at the reference pose).
The motion test checks 1,441 samples over 720 degrees, including paired piston
positions and TDC at the declared firing events. Neither a static clearance check
nor this idealized mechanism verifies continuous clearance of a completed engine.

The oil pump and pickup now have 15 independent occurrences. See
`inventory/engine/oil-pump-evidence.json` for factory identities, comparison-derived
relief dimensions, modeling assumptions and outstanding interfaces. A same-service-
number industrial comparison supports four cover bolts; the truck pickup has a
different service number, so the modeled tube remains a provisional layout.

The EFI increment adds 11 occurrences across five definitions. The valve cover
now has sloped shoulders and a rear ventilation opening. Head passages were extended
to the manifold face, correcting a 5.5 mm blind end in the earlier model. These are
provisional shapes, not measured production geometry. See
`inventory/engine/intake-evidence.json` for the reference/assumption boundary.
`inventory/engine/intake-validation.json` records 18 open mating-interface probes.

Next accuracy work: verify the block/head envelope and intake/exhaust mounting
dimensions. Pump mounting, outlet and intermediate-drive interfaces also remain
open. Do not replace unresolved castings with visually elaborate but unsupported
detail. The remaining systems and hardware are itemized in the completion plan.

The throttle mechanism adds six definitions / thirteen occurrences. Its independent
slider turns the shaft and paired butterfly plates from 0–90 degrees. Factory
layout and mounting count are sourced; dimensions and actual stop angles remain
assumptions. See `inventory/engine/throttle-evidence.json` and the seven-angle
clearance report `inventory/engine/throttle-validation.json`. The throttle branch
now has 28 occurrences including IAC and TPS studies; remaining linkage, springs,
plate screws and mounting hardware are recorded in the completion plan.


## Completion boundary

The physical-component work breakdown is tracked in
`inventory/engine/completion-plan.json`. Engine geometry requirements and reference
search findings are in [ENGINE-GEOMETRY-EVIDENCE.md](ENGINE-GEOMETRY-EVIDENCE.md).
Neither the occurrence count nor passing clearance checks establishes that the
requested every-part engine replica is finished. The complete engine is not ready
for final acceptance: major systems and foundational dimensions remain unresolved.

The latest fuel/control studies add separate injector internals and seals, supply
and return rails, a diaphragm regulator, an unvented IAC study and a rotary TPS.
The TPS rotor/wiper follow the throttle control. The factory manual describes
multiple IAC variants; the installed truck variant is not established. Coil and
screen envelopes are simplified, and calibration/flow are not simulated.


Historical fuel/control verification covered 116 valid CAD definitions and 548 assembled solids,
1,866 static candidate pairs with no overlaps above 0.1 mm³, and four sampled
core/lubrication poses with no such overlaps. Seven throttle positions cover 301
candidate pair checks; 25 fuel/IAC/exhaust probes and 18 intake probes verify the
modeled mating openings. Navigation reaches all 548 components through 654 scope
links. These checks establish internal consistency of the reconstruction only.

## Water-pump increment — 2026-09-23

Current increment — water pump (2026-09-23): 127 definitions / 559 occurrences.
Added eight-component water-pump internal study, Cooling navigation, individual
part pages, cover transparency, explosion and factory-linked explanations.
Build: .venv-cad/bin/python cad/engine/full_engine.py --refresh-cooling.
All geometry dimensions, production casting/ports and installed datums remain
provisional. Bearing and coolant seal remain cartridge/envelope representations;
pulley, fan clutch, mounting hardware and hose/block connections are outstanding.
Validation: 127 valid STEP definitions, 559 assembled solids, GLB bounds within
0.5 mm, zero >0.1 mm³ overlaps across 1,881 static candidate pairs, 668 navigation
links. Browser checked assembled and 65% exploded views. No pump motion/flow claim.
Owner confirms no more underhood labels; treat VECI as missing, stop requesting
label searches. This does not block mechanical modeling. Next: pump production
outline/connections and pulley/fan boundary, then remaining cooling components.

### EGR valve and position-sensor increment (2026-09-24)

The atlas now contains a31-part EGR/EVP study with individual pages and a connected provisional intake interface. Manufacturer replacement photos and the owner-purchased EVTM constrain architecture and wiring; overall dimensions, calibrated motion, internal sensor construction and actual mounting geometry remain unverified. The exhaust tube, vacuum regulator, hoses and wiring are still missing. Current total275definitions/784occurrences is not a completion percentage. Published static and sampled-motion checks pass; these are geometric checks, not proof of production accuracy.
