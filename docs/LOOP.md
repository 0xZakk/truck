# Autonomous modeling loop — operating procedure

The owner approved running this as an **autonomous loop** using **parametric builders**
(hand-authored shaped geometry in `viewer/builders.js`, like the starting system).
Each iteration models ONE assembly/system to the quality bar, then reschedules itself.

## MODEL INTERNALS + EXPLODE (owner's standing requirement, 2026-06-10)
The owner wants every part modeled in full detail and to be able to **pull assemblies
apart** (teardown / exploded view) for animations and step-by-step diagnostics. So:
- Internal parts get **real geometry** (NOT `placement:"internal"`): position them inside
  their housing (they're occluded normally) and give each an **`explode` vector**
  `[dx,dy,dz]` in `model` — the direction/distance it travels when the assembly is
  exploded (e.g. pistons `[0,15,0]` up out the deck, crank `[0,-11,0]` down). The viewer's
  🧩 Explode slider (and `?explode=0..1`) animates them out. Verify the exploded view in a
  screenshot too. The engine is the reference (crankshaft/pistonSet/conrodSet/camshaft).
- After the remaining systems are deep, do **internals/teardown passes** on the hero
  assemblies: transmission (shafts, gearsets, synchros), rear axle (ring & pinion, carrier,
  side gears), starter (armature, brushes, drive), etc. Routed cables/pipes don't explode.
- The checker's `legit_interface` whitelists internals-inside-housing, so those overlaps
  are expected — but still screenshot-verify the exploded layout reads correctly.

## Quality bar (non-negotiable — the starting system is the reference)
- **Real shaped geometry, never bare massing boxes** for a part we're "doing". A part
  should be recognizable: cylinders/cones/gears/tubes/flanges composed in a builder.
- **Real Ford part numbers + specs** mined from the FSM (`manuals/factory-service-manual/...`).
  Don't fabricate part numbers — leave blank or mark "(basic)" if only the basic number is known.
- **Real coordinates & scale** in inches per `inventory/schema.md` (origin = wheelbase
  center on the ground; +X fwd, +Y up, +Z right). Place parts where they actually are.
- Catalog internal/hidden sub-parts with `placement:"internal"` (counted, drawn later).

## Completeness is driven by the BOM ledger
`inventory/bom.json` is the master checklist — **603 serviceable parts** from the factory
catalog (rebuild with `python3 scripts/build_bom.py`). Each part has a `status`
(`not-started → catalogued → modeled`) and a `system`. The truck is "complete" when every
BOM part is `modeled` (plus exploded-view fasteners added per assembly). Work a whole
catalog group/system per iteration; tick its parts off in `bom.json` as you model them.

## Per-iteration checklist
1. Pick the next system from the BOM ledger / `docs/PROGRESS.md` coverage tracker (build
   order below; skip any the owner redirected to). List its `bom.json` parts (the ones to
   build). Re-read `inventory/schema.md` + skim `viewer/builders.js` for the pattern/helpers.
2. Mine the FSM for that system (use an Explore subagent): enumerate every part, Ford
   part number, qty, location, specs, and source page paths. Note exploded-view images.
3. Author detailed builder(s) in `viewer/builders.js` and add/refine records in
   `inventory/parts.json` (builder + real coordinates + part numbers + function +
   issues + fsm_sources). Reuse the shared `M.*` materials and `cyl/box/ball/gear/at`
   helpers. Export new builders in the `BUILDERS` map.
4. **Verify — including SEEING it (mandatory).** Building 3D blind was the root cause
   of repeated misplacement. Every iteration MUST screenshot-check the result:
   - `python3 -c "import json;json.load(open('inventory/parts.json'))"`, `node --check`
     on both viewer files, and the headless builder smoke-test (rewrite `from 'three'`
     → `/tmp/three.mock.mjs`, run every BUILDER, assert each returns a non-empty Group).
   - Render with headless Chrome and LOOK at the PNGs (use the Read tool on them):
     `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
       --use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader \
       --window-size=1400,900 --virtual-time-budget=12000 \
       --screenshot=/tmp/shots/x.png "http://127.0.0.1:8080/viewer/?<params>"`
   - Diagnostic URL params: `iso=<systemId>` isolate · `sel=<partId>` select ·
     `view=iso|side|side2|top|front` fixed camera · `snap` jump instantly · `zoom`
     (with sel) frame one part · `axes` XYZ axes (R=+X fwd, G=+Y up, B=+Z right) ·
     `dump=1` emit geometry JSON. Check a whole-truck view AND an isolated view of the
     system you just added. Fix placement/scale until it looks right.
   - **Run the automated geometry checker** — this is how we stay accurate at scale
     without hand-checking every part: `python3 scripts/check_geometry.py --system <id>`.
     It pulls real world-space bounding boxes from the scene and flags CABLE-THROUGH
     (route cables around obstacles; give each cable a `connects:[a,b]`), OVERLAP
     (interpenetrating parts of different assemblies), and ORPHAN (part floating with no
     neighbor within 6"). Also prints a size/position table — sanity-check proportions
     against `inventory/schema.md` reference dims. Resolve real flags before logging done.
5. Update `inventory/bom.json` (set the modeled parts' `status:"modeled"`, fill any newly
   found `part_numbers`/`system`) AND `docs/PROGRESS.md` (bump the system to `deep`, dated
   log entry, BOM modeled-count so the owner can see % complete).
6. The static server serves files live (no restart needed); the owner can refresh to see
   new parts. Then **reschedule the next iteration** (same loop prompt) unless: every
   system is `deep`, or the owner has asked to pause/redirect.

## Build order (big visible mechanical systems first)
1. engine (4.9L I6 long block + valve cover, manifolds, accessory brackets)
2. cooling (radiator detail, water pump, fan, thermostat housing, hoses)
3. intake-exhaust (air cleaner, intake/exhaust manifolds, pipe, cat, muffler, tailpipe)
4. fuel (tank detail, sending unit, pump, lines, filter, throttle body/injection)
5. driveline (clutch, bellhousing, M5OD-R2 case detail, shifter, driveshaft, U-joints)
6. rear-axle (housing, diff carrier, axle shafts, brakes backing)
7. suspension (twin-I-beams, radius arms, coil/leaf springs, shocks, bushings)
8. steering (box, pitman arm, drag link, tie rods, pump, column)
9. brakes (front discs/calipers, rear drums, master cyl, booster, lines, proportioning)
10. wheels-tires (refine rims + tires + lug nuts + hubs)
11. electrical-charging (alternator detail, regulator, wiring)
12. ignition (distributor detail, coil, plugs, wires, EEC)
13. electrical-body (fuse box, harnesses, lamps, switches, gauges)
14. hvac (heater box, blower, core, A/C compressor/condenser, ducts)
15. frame-chassis (refine rails, crossmembers, mounts, hitch)
16. body-cab (refine into firewall, floor, doors, roof, pillars)
17. body-bed (refine into bedsides, floor, tailgate, wheel wells)
18. exterior-trim (refine bumpers, grille, mirrors, moldings, emblems, lights housings)
19. interior (seats, dash detail, console, panels, pedals, steering wheel)
20. glass (windshield, doors, back glass, regulators)

## Notes for the owner
- Each iteration logs to `docs/PROGRESS.md`. Refresh the viewer anytime to watch the
  truck fill in. Interrupt at any point to redirect (e.g. "do brakes next", "more detail
  on the engine", "stop the loop"). Saying stop ends it; otherwise it keeps going.
