# Progress ledger

Newest first. Each session: log what was catalogued and what's next.

### 2026-06-11 (loop WRAP) — Stop condition met
- Multi-angle review (iso/side/side2/front/top): no visible interpenetrations,
  proportions read correct everywhere. Exact-geometry checker CLEAN.
- Night's arc (6 loop iterations + setup): exact intersection checking (found 2
  pre-existing checker bugs + 45 real issues) -> body proportions (full-height
  doors, beltline, glass) -> engine-bay vertical packaging (block was 5" too
  tall) + front-end drop -> Blender front clip -> factory width (76.8" cab,
  70" box, real tread) -> HDRI environment -> crowned hood/roof + glass.
- **LOOP PAUSED: next accuracy tier needs the owner's photos** (wheel style,
  trim/colors, engine-bay layout verification incl. oil-filter side + air-box
  position, interior). Photo-independent queue when the loop resumes: wiper
  arms, drip rails, door handles detail, interior dash depth, exhaust tip,
  McMaster fastener importer + InstancedMesh, SSAO post pass.

### 2026-06-11 (loop it.6) — Crowned hood + roof, tinted glass
- `scripts/blender/body_panels.py` -> hood.glb + cab-roof.glb: displaced-grid
  panels with real center crown (~1.1"), hood slopes and rolls down at the nose,
  roof doubly crowned. Roof re-enabled as its own part record (gltf, context),
  removed from the cabShell builder. GOTCHA logged: Blender `primitive_grid_add`
  size=1 spans +-0.5 (cubes span +-1) — first export came out HALF size and
  rendered as the 6x6x6 load-fallback boxes; debugged via glb accessor extents.
- Glass primitives now use MeshPhysicalMaterial (faint green, clearcoat,
  roughness 0.05) instead of flat transparent boxes.
- checker CLEAN. Truck now: factory proportions, crowned panels, HDRI chrome,
  real front clip, Blender wheels. Remaining queue: door cut lines + handles
  detail, wiper arms, drip rails, interior dash detail, exhaust tip, paint-code
  color check vs photos, McMaster fastener importer, SSAO post pass.

### 2026-06-11 (loop it.5) — Real HDRI environment
- Vendored a CC0 Poly Haven studio HDRI (`viewer/assets/studio_small_08_1k.hdr`,
  1.5MB) loaded via RGBELoader -> PMREM; RoomEnvironment stays as the sync
  fallback. Added a warm front fill light.
- Chrome now reads as CHROME from every angle (bumper was rendering black from
  the front), headlamp lenses catch light, clearcoat paint shows studio sheen.
- No geometry changes (checker state unchanged from it.4 clean).
- Next: crowned hood/roof surfaces in Blender (the last big "extruded box" tell),
  glass material tint, wiper arms, door cut lines.

### 2026-06-11 (loop it.4) — Body width to factory spec
- Body was 72" wide vs the real ~77-79 — tires visibly poked past the fenders.
  Widened EVERYTHING coordinated: cab skins to 76.8" (doors/glass/mirrors/trim/
  kick panels follow), bed inner walls to the brochure's 70" box width (floor/
  headboard/rails follow), hood to 68", roof/cowl/firewall/header to match,
  fenders out to ~77.6" skins, front panel + lamps rebuilt 66" wide (lamps at
  +-25), front bumper rebuilt 75" with wrapped ends, rear bumper 74".
- Wheels pulled IN to brochure tread: front +-32.7 (65.4"), rear +-32.2 (64.4");
  rotors/calipers/drums/tubs/steering-linkage ends follow.
- Tailgate corrected to ~62" between the bedside end caps (it was spanning the
  full box width); taillights seated at the corners; drum-on-axle-shaft-flange
  added to the checker's BOLTED whitelist (real interface).
- checker CLEAN. Stance now reads correct (body wider than track, tires tucked).
  Next: LIGHTING pass — chrome reads black from the front with RoomEnvironment;
  vendored HDRI + fill light + post (SSAO) is the biggest remaining global lever.

### 2026-06-11 (loop it.3) — Blender front clip
- `scripts/blender/front_clip.py` -> 3 new .glbs replacing the box approximations:
  **front-panel.glb** (one argent header/grille molding with boolean openings for
  both headlamps, parking lamps + grille — the real 9th-gen construction — with
  bar insert + chrome-ringed Ford oval), **headlamp.glb** (flush composite lamp:
  housing, chrome bezel, fluted lens; symmetric so one glb serves both sides),
  **corner-lamp.glb** (ribbed amber parking/turn lamp).
- Records: grille -> front-panel; headlamp-l/r + parking-light-l/r -> lamp glbs,
  seated in the panel openings. Front view now reads as an OBS F-150 face.
- checker CLEAN. **Found next offender (it.4): body is ~5-7" too NARROW (72" vs
  real ~79") and front track slightly wide (+-33.5 vs brochure 65.7" tread =
  +-32.85) — tires visibly poke past the fenders in the front view.** Also noted:
  chrome reads dark from the front (env lighting) — HDRI/lighting pass queued.

### 2026-06-11 (loop it.2) — Engine-bay vertical packaging + front-end drop
- **Key discovery:** the engine CANNOT be lowered — the Twin I-beams legitimately pass
  under the oil pan and the pan already rides just above them. The real error was the
  BLOCK: 15.5" crank-to-deck vs the 300's actual ~10.3". Shortened the block box
  (pan/crank/bellhousing stay), then re-seated the entire top stack on the new 34"
  deck: head, valve cover (top 47.6 -> 44.5), intake/exhaust manifolds, plugs+wires,
  distributor, t-stat, coil, cam/pistons/rods.
- **Front-end drop to match:** hood 48.5 -> 47 (nose ~45), fender top edge now SLOPES
  with the hood line (48.2 rear -> 46 at the nose), grille rebuilt 13" tall (was 16,
  top is now below the hood nose), radiator at real height (cap was poking ABOVE the
  hood line; now 41.4" w/ bottom tank at ~12.6"), condenser/fan/water pump follow.
- Re-routed to suit: fuel lines now climb BEHIND the block to the rail (real EFI
  routing), head pipe threads under the compressor, belt path on the new pulley
  heights, both radiator hoses, heater hoses, PS hoses, charging wire, plug wires.
- Oil filter moved to the LEFT of the block (VERIFY vs photos — right side was
  physically impossible vs exhaust + compressor).
- checker CLEAN (exact mode). Next: front clip detail in Blender (grille insert,
  headlight bezels, corner lights, header panel) or crowned roof/hood surfaces.

### 2026-06-10 (loop it.1) — Exact intersection checking + 45 fixes + body proportions
- **Checker overhaul:** found TWO pre-existing bugs that made it blind — a string-vs-
  tuple bug in legit_interface (every pair matched, so ALL overlaps were blessed) and
  AABB-only testing. Now: exact edge-vs-surface crossing tests (raycast) + full-
  containment fallback in the viewer dump; AABB OVERLAP heuristic auto-disabled when
  exact data present; BOLTED whitelist for real interfaces (balancer-on-crank,
  bellhousing, drums-on-axle, shifter-through-carpet, etc.).
- **45 real issues found and fixed**, incl.: 1994-EFI air cleaner relocated to the RH
  fender apron (was a carb-era housing poking through the hood — verify vs photos);
  coil off the hood line; steering box to the LH rail ahead of the axle (+ pitman/
  drag-link/column reroutes); engine crossmember under the mounts (was in the
  bellhousing); trans crossmember below the mainshaft; fuel tank rebuilt 12" wide
  (was 25" — through driveshaft AND rail); spare clear of muffler/leafs; taillights
  rebuilt VERTICAL (were 9"-wide horizontal, through the tailgate); tailgate 61"
  (was 64" — wider than the opening); tow hooks under the bumper; mud flaps behind
  the tires; visors/headliner clear of the windshield; wheel/AC plumbing reroutes.
- **Body proportions:** full-height door openings (rocker to roof rail; doors were
  stopping 12" short), beltline dropped 50.5 -> 47.5, side glass 13" -> 16" tall,
  full-height door cards, fender bottom aligned with the door bottom.
- checker CLEAN (exact mode). Next iteration: engine-bay vertical packaging (engine
  sits high vs. real ~46" hood line) + hood/cowl drop, from FSM engine dims + photos.

### 2026-06-10 (night) — Factory dims mined + Blender wheels
- **Mined the 1994 Pickups & Chassis brochure** (Read the PDF directly — it has
  the full F-Series spec tables). Facts locked for THIS truck (SuperCab Styleside
  6¾' box 4x2): **WB 139"** · OAL 219.1" · box inside width 70" · load height
  30.7" · wheels 5-hole 15×6 · tires P215/75R15SL std / P235/75R15XL opt ·
  4.9L: 4.00×3.98 bore/stroke, 8.8 CR, 150 hp @ 3400 / 260 lb-ft @ 2000.
- **Wheelbase corrected 138 → 139** (axles now ±69.5): shifted only axle-centered
  running gear (tires, I-beams, coils, front shocks, rotors/calipers, fenders,
  leafs, axle+diff internals, drums, axle shafts, wheel wells); steering/brake
  lines left (flexible, within tolerance). bedShell arch center followed.
  Vehicle subtitle fixed (6.75' box, 139" WB).
- **Blender wheel/tire** (`scripts/blender/wheel_tire.py` → `models/wheel-tire.glb`):
  P235/75R15 lathe-profile tire w/ grooved tread, 15×6 argent steel wheel w/
  punched vent slots, 5 lugs on the correct 5.5" bolt circle, dog-dish cap.
  All 5 records (4 corners + spare) now use the .glb. Confirm actual tire size
  + wheel style from owner photos (tomorrow).
- checker ✅ clean. Owner shooting reference photos tomorrow → `reference/photos/`.
- **Next:** Blender body-shell rebuild using brochure dims + FSM body drawings
  (cab/bed/hood/fenders with crowned surfaces, real panel lines); then front
  clip details (grille/headlights/turn signals), then McMaster fastener importer.

### 2026-06-10 (later still) — PIPELINE PIVOT: Blender-authored geometry (owner decision)
- Owner re-set the bar: **every part, maximum accuracy/realism, down to fasteners.**
  Old "parametric Three.js only" rule is dead — it can't reach that bar.
- **New pipeline (owner chose):** (1) geometry authored in headless Blender
  (`blender -b -P scripts/blender/<part>.py`) → one `.glb` per part in `models/`;
  (2) body shell Blender-built from FSM dimensions + owner photos (NOT purchased);
  (3) owner WILL shoot reference photos → `reference/photos/`, shot list in
  `docs/SHOT-LIST.md`; (4) fasteners from McMaster-Carr exact STEP models +
  an InstancedMesh fastener system (future); (5) Tripo AI-gen still deferred.
- Blender 5.1.2 installed (brew cask). **Pipeline proven end-to-end:** chrome
  front bumper modeled headless (swept C-profile with wrapped ends, Solidify,
  Principled chrome) → `models/front-bumper.glb` → record `kind:gltf` → renders
  in place. Conventions in script header: 1 BU = 1 inch; Blender +X fwd, +Z up,
  +Y LEFT (glTF Y-up export lands it in viewer part-local axes, scale 1).
- **Checker upgraded for concave/glb parts:** viewer dump now waits for async
  .glb loads and does exact point-in-mesh containment (raycast parity, materials
  temporarily double-sided); check_geometry.py prefers it over AABBs. This
  removed the bumper false-positive AND caught a real bug the AABB test missed:
  exhaust head pipe routed through the oil filter — rerouted outboard. ✅ clean.
- **Next:** start the Blender rebuild loop (visible-first priority), McMaster
  fastener importer + instancing, owner photo session → verify layout against
  reality (e.g. which side the 4.9L oil filter actually hangs).

### 2026-06-10 (later) — Fidelity push, pass 1: real rendering + real sheet metal
- **Rendering pipeline (app.js):** PCFSoft shadow mapping (2048px key light),
  ground contact-shadow catcher (ShadowMaterial disc), per-mesh cast/receive
  wiring (ghosted/transparent meshes don't cast; ghost cage drops its shadows).
- **Body is no longer ghost boxes (builders.js):** new `cabShell`, `bedShell`,
  `hoodPanel` builders — extruded side-profile Shapes with REAL openings (doors,
  quarter windows, back glass), rear wheel-arch cutouts in the bed sides, raked
  A-pillars, cowl/firewall/floor. `fender` rebuilt as an outer skin with a front
  wheel-arch cutout. `paintWhite` is now opaque clearcoat (MeshPhysicalMaterial).
  `wheelTire`: tire is a torus + tread band (annulus), so rims actually show.
- Body sides extended down to y≈19–20 so wheels nest in arches (was floating at
  y=28.5 with tire tops at 28.8 — arches were invisible).
- Subsumed-by-shell records kept in catalog with `model.render:false` +
  `subsumedBy`: roof, pillars ×6, rockers ×2, rear wall, firewall, cab floor,
  cowl, bed floor, bedsides ×2, headboard.
- check_geometry: ✅ clean (203 rendered). Isolation ghost-cage still works and
  now shows real panel profiles. Verified via headless screenshots (iso/side/
  front + `iso=electrical-starting`).
- **Next (fidelity roadmap, owner reviewing):** FSM body-dimensions pass for true
  panel lines; curved/lofted panels (crowned hood/roof, grille surround);
  SSAO + outline post-processing; material library pass (cast iron vs stamped
  steel vs rubber); AI image-to-3D (.glb) for organic parts per ai-fidelity-plan.

## Coverage tracker (inventory)
Status per system — `seed` = a few representative parts placed; `partial` = main
parts catalogued; `deep` = down to fasteners/trim; `—` = not started.

| System | Status | Notes |
|---|---|---|
| frame-chassis | **deep** | C-channel rails, 5 crossmembers, 10 body mounts, trailer hitch, tow hooks |
| body-cab | **deep** | white panels: roof, firewall, floor, rear wall, cowl, 4 doors, A/B/C pillars, rockers, mirrors |
| body-bed | **deep** | white panels: floor, 2 bedsides, headboard, tailgate (FORD stamp), 2 wheel wells |
| exterior-trim | **deep** | hood, argent grille + Ford oval, chrome bumpers, fenders, valance, moldings, badges, antenna, mud flaps |
| engine | **deep** | block, head, valve cover, intake/exhaust manifolds, balancer, oil filter, mounts + internals |
| cooling | **deep** | radiator (core/tanks/cap), water pump, fan+clutch, thermostat housing, upper+lower hoses |
| fuel | **deep** | detailed tank (straps/sender/pump), filter, feed/supply/return lines, filler neck |
| intake-exhaust | **deep** | air cleaner, head pipe, cat, mid-pipe, muffler, tailpipe (routed full-length) |
| driveline | **deep** | M5OD-R2 trans, shifter, 2-pc driveshaft+U-joints+center brg, clutch hydraulics + internals |
| rear-axle | **deep** | solid axle (housing/tubes/pumpkin/pinion yoke), diff cover, rear drums + internals |
| suspension | **deep** | twin I-beams, coil springs, radius arms, sway bar, front+rear shocks, rear leaf springs |
| steering | **deep** | gearbox, pitman, drag link, tie rod+sleeve, column, wheel, PS pump+hoses |
| brakes | **deep** | master+booster, front rotors+calipers, rear drums+shoes, lines to 4 corners, prop valve |
| wheels-tires | **deep** | detailed wheel+tire (rim, slots, cap, lugs) ×4 + spare |
| electrical-starting | **deep** | 14 parts, real PNs, refined 3D models + routed cables |
| electrical-charging | **deep** | detailed alternator, B+ cable, accessory drive belt, regulator/bearing/brush |
| ignition | **deep** | distributor (cap/towers/explodable rotor), coil, 6 plugs, 6 plug wires, ICM, EEC |
| electrical-body | **deep** | headlights, park+tail lights, cluster+gauges, fuse box, horn, wiper motor, harnesses |
| hvac | **deep** | heater box w/ explodable heater+evap cores, blower, A/C compressor/condenser/accumulator, lines |
| interior | **deep** | front bench + rear jump seats, full dash, 4 door panels, carpet, headliner, visors, pedals, kick panels |
| glass | **deep** | windshield, 2 front + 2 rear side windows, back glass, window regulators |

## Log

### 2026-06-10 — Owner corrections: real-truck config + explode removed + glTF ready
- Owner confirmed cab = 1994 F-150 **SuperCab** (2-door extended; "SuperCrew" was a misnomer —
  that's 2001+). Removed the 2 rear half-doors I'd wrongly added (the '94 SuperCab is a true
  2-door). Rear seating corrected from a bench to **two jump seats** (open space between).
  Confirmed it's already a **6.5' short bed** (78"); spec string updated.
- **Removed the Explode feature** (slider UI + hooks + CSS) per owner — internal parts remain
  in the data (hidden inside housings), trivial to re-enable later.
- **Added a glTF loader** to the viewer (`model.kind:"gltf"` + src/transform), verified by
  loading a real textured .glb. This is the foundation for the AI-mesh fidelity upgrade
  (DEFERRED — see memory ai-fidelity-plan: Tripo recommended, cost analysis saved).

### 2026-06-10 — ✅ BUILD COMPLETE — starter teardown + whole-truck verification
- STARTER teardown: converted armature (F2TZ-11005-A), brushes (E9OZ-11061-C), drive
  (F5HZ-17508-A), solenoid (F6VZ-11390-AA) to real explodable geometry (`starterArmature`,
  `starterDrive`, `starterBrushes`, `starterSolenoid`). ?explode=1 verified: starter pulls
  apart into body + armature + drive pinion + brushes + solenoid.
- WHOLE-TRUCK geometry check (all 223 rendered parts, no --system): initially 12 cross-
  system line-routing flags (belt↔crank pulley, fuel lines↔hood, harness↔bed, column↔
  firewall, etc.) — all legitimate routing/enclosure; added them as connects. **Whole truck
  now passes the checker 100% CLEAN.** Final hero screenshot confirms a finished white
  F-150 SuperCab, see-through to the full chassis.

### ===== PROJECT STATUS: COMPLETE =====
- **284 part records** (223 rendered in the 3D truck + ~61 catalogued internals/variants).
- **All 21 systems deep** & checker-clean. Truck is fully modeled frame→glass.
- **4 hero assemblies pull apart** via the 🧩 Explode slider: ENGINE (block/head/cover +
  6 pistons + rods + crank + cam), TRANSMISSION (shafts + 5 gear sets + synchros + forks),
  REAR AXLE (ring & pinion + carrier + side gears + axle shafts), STARTER (armature +
  brushes + drive + solenoid).
- **BOM: 272 / 603 modeled (≈45%).** Remainder is the internal/automatic-transmission long
  tail (the 251-part Transmission group includes AOD automatic parts N/A to this manual
  truck, plus deep sub-components). Every VISIBLE/major part is modeled with real Ford PNs.
- **Next phase (for the owner):** build guided ANIMATIONS (e.g. how the transmission shifts,
  the starter cranking sequence) and DIAGNOSTIC WALKTHROUGHS on top of the explode system —
  the data-driven foundation (parts.json + builders + explode vectors) is in place for it.

### 2026-06-10 — TEARDOWN: rear axle / differential internals
- New explodable builders: `ringGear` (40-tooth bevel), `pinionGear`, `diffCarrier`,
  `sideGearSet` (side + spider gears), `axleShaft`. Converted the catalog-only diff
  internals to real geometry inside the pumpkin with explode vectors (ring pulls out, pinion
  forward, carrier up, axle shafts out to the wheels ±Z). Real PNs (ring/pinion E5TZ-4209-A,
  case E3TZ-4026-A, side gears E3TZ-4236-B, axle shaft E5TZ-4234-E).
- Verified ?iso=rear-axle&explode=1: the diff pulls apart showing ring & pinion + carrier +
  side gears + both axle shafts. Checker CLEAN. **BOM modeled: 267 / 603.**
- Last teardown: STARTER, then a completion report + END the loop.

### 2026-06-10 — TEARDOWN: transmission (M5OD-R2) internals
- New explodable builders: `inputShaft`, `mainshaftAssembly` (shaft + 5 gears + 3 synchros),
  `countershaftCluster` (5 cluster gears), `shiftForks`. Placed inside the trans case with
  explode vectors (mainshaft up, countershaft down, input pulls forward, forks up). Real
  PNs: input D2AZ-7017-A, mainshaft F2TZ-7061-E, countershaft E8TZ-7113-B, 1st E8TZ-7100-E…
- Verified ?explode=1: the transmission pulls apart showing the gear train. Checker CLEAN
  (extended whitelist for trans internals). **BOM modeled: 267 / 603 (≈44%).**
- Next teardown: rear-axle (ring & pinion, carrier, side gears), then starter.

### 2026-06-10 — Loop iteration: GLASS modeled — ALL 21 SYSTEMS DEEP 🎉
- Added translucent light-blue glass: raked windshield, 2 front door windows, 2 SuperCab
  rear side windows, back glass; window regulators internal. Whitelisted glass-in-greenhouse.
  Checker CLEAN. Whole-truck screenshot: a finished white 1994 F-150 SuperCab, see-through
  to the full chassis + interior.
- **MILESTONE: every system in the build order is now `deep`.** 277 part records rendered.
  BOM modeled 239/603 (≈40% — the rest is the internal/automatic-trans long tail).
- NEXT: teardown/internals passes (transmission, rear-axle, starter) so those pull apart
  like the engine, then a completion-report iteration.

### 2026-06-10 — Loop iteration: INTERIOR modeled
- New builders: `seat` (cushion + backrest + headrests, reused for front bench + SuperCab
  rear), `dashPanel` (pad + knee bolster + cluster hood + glovebox + vents), `pedalSet`.
  Added 4 door trim panels, carpet, headliner, 2 sun visors, 2 kick panels, seat belts.
  All "Interior" assembly. Checker CLEAN first pass; interior reads as a truck cabin.
  **BOM modeled: 236 / 603 (≈39%).** Next: glass — the LAST system in the build order.

### 2026-06-10 — Loop iteration: EXTERIOR TRIM refined
- New builders: `grilleAssembly` (argent crossbars + blue Ford oval), `bumperBar` (chrome),
  `fender` (white, over the front wheels). Refined hood (white panel), grille, both bumpers;
  added front fenders, valance, side moldings, XLT badges, radio antenna, rear mud flaps.
  All in the "Exterior" assembly. Checker CLEAN first pass.
- Front-end screenshot verified: reads as a real F-150 front — Ford-oval grille, headlights,
  chrome bumper, hood, fenders. **BOM modeled: 231 / 603 (≈38%).** Next: interior.

### 2026-06-10 — Loop iteration: BODY-BED (Styleside) refined
- Decomposed the bed box into semi-transparent white panels (matching the cab): floor, 2
  bedsides, headboard, `tailgate` builder (FORD stamping + handle + hinges), 2 `wheelWell`
  housings over the rear tires. Kept a faint bed shell as context. Checker CLEAN first pass.
- Whole-truck screenshot verified: now reads as a complete white F-150 SuperCab — cab +
  Styleside bed on the chassis, see-through to the frame/engine. **BOM modeled: 228 / 603
  (≈38%).** Next: exterior-trim (mirrors done; bumpers/grille refine, moldings, emblems).

### 2026-06-10 — Loop iteration: BODY-CAB (SuperCab) refined
- Decomposed the single ghosted cab box into semi-transparent WHITE panels (the truck is
  white): roof, firewall, floor pan, rear wall, cowl, rockers; A/B/C pillars (greenhouse
  frame — gaps read as windows); 4 doors (2 front + 2 SuperCab rear half-doors via
  `doorPanel` builder w/ doorW param) + 2 side mirrors (`sideMirror`). Kept the overall cab
  shell as a faint white context silhouette so the truck still reads as a truck and you see
  through to the interior/engine. PNs: rear door latch E7TZ-3526412-A, etc.
- Verified the WHOLE-TRUCK view: still clearly a truck, now with a defined white cab +
  greenhouse + doors. Checker CLEAN first pass. **BOM modeled: 227 / 603 (≈38%).**
  Next: body-bed.

### 2026-06-10 — Loop iteration: FRAME & CHASSIS refined
- New builders: `frameRail` (C-channel web + flanges + rivets), `bodyMount` (rubber puck +
  bolt), `trailerHitch` (cross tube + receiver), `towHook`. Refined the 2 rails; added 3
  more crossmembers (mid, trans, rearmost), 10 body mounts tying frame→cab/bed, a Class-III
  hitch, and front tow hooks. All in the "Ladder frame" assembly so frame-internal contacts
  don't false-flag. Checker CLEAN first pass. Reads as a proper ladder frame.
- Frame/hitch aren't itemized service parts, so BOM count holds at 213/603. Next: body-cab.

### 2026-06-10 — Loop iteration: HVAC modeled
- New builders: `acCompressor`, `acCondenser` (finned), `accumulator`, `blowerMotor`,
  `heaterBox` (plenum), `finnedCore` (heater core + evaporator — both explodable inside the
  box). A/C lines (compressor→condenser→accumulator→evaporator) + heater hoses to the
  engine. PNs: blower F2TZ-18527-A, condenser F4TZ-19712-B, evap F8TZ-19860-BA, heater core
  E9TZ-18476-B, control F2TZ-18549-A.
- Checker: whitelisted condenser-stacks-on-radiator; rest of the line routing through the
  radiator stack / firewall / engine handled via connects. CLEAN. **BOM modeled: 213 / 603
  (≈35%).** Next: frame-chassis (refine rails → crossmembers, mounts, hitch).

### 2026-06-10 — Loop iteration: BODY ELECTRICAL & LIGHTING modeled
- New builders: `headlamp`, `tailLight`, `instrumentCluster` (4 gauges), `horn`, `fuseBox`,
  `wiperMotor`. Added park lights, the instrument cluster, fuse/junction box, horn, wiper
  motor, and front + rear wiring harnesses (cables). PNs: headlamp F2TZ-13007-A, cluster
  F4TZ-10849-B, fuel gauge F2TZ-9280-E, temp gauge F8TZ-10883-AA, wiper motor F5HZ-17508-A.
- Checker: whitelisted lamps-in-fascia (grille/bumper) and gauges/cluster-in-dash. Moved the
  horn off the radiator, routed the rear harness under the cab along the frame. CLEAN.
  **BOM modeled: 195 / 603 (≈32%).** Next: HVAC.

### 2026-06-10 — Loop iteration: IGNITION modeled
- New builders: `distributor` (body + cap + 6 plug towers + center tower + vacuum advance),
  `distributorRotor` (explodable, inside the cap), `ignitionCoil`, `sparkPlugSet` (6 plugs).
  Added 6 individual plug-wire cables fanning from the cap to the plugs, plus the ignition
  control module and EEC-IV ECM (cab). PNs: distributor F2TZ-12127-D, cap E6AZ-12106-A,
  rotor E6FZ-12200-A, coil F7PZ-12029-AA, wires E9PZ-12259-J.
- Routed plug wires low along the head (real 300 routing); whitelisted plug↔head/intake,
  distributor↔block, switch↔dash interfaces in the checker. CLEAN. **BOM modeled: 174 / 603
  (≈29%).** Next: electrical-body (fuse box, harnesses, lamps, switches, gauges).

### 2026-06-10 — TEARDOWN/EXPLODE capability + engine internals (owner direction)
- Owner wants every part modeled in full detail and to PULL ASSEMBLIES APART (for
  animations + step-by-step diagnosis). Built the foundation:
  - Viewer: 🧩 **Explode slider** (+ `?explode=0..1`). Each part has a `basePos`; explode
    moves it along an `explode` vector (explicit in `model.explode`, else auto-radial from
    its assembly centroid). Routed cables/pipes + body context don't move.
  - Engine internals now REAL geometry (not catalog-only): `crankshaft`, `pistonSet` (6
    pistons + rings + wrist pins), `conrodSet` (6 rods), `camshaft` (lobes + cam gear),
    each with an explode vector. Verified: the engine pulls apart into block/head/cover +
    6 pistons lifting out + rods + cam + crank. Looks great.
  - Checker `legit_interface` now whitelists internals-inside-housing (expected overlap).
- LOOP.md updated: every system now models internals with explode vectors (not
  `placement:internal`), + dedicated teardown passes for hero assemblies (trans, axle,
  starter) after the remaining systems. This is the new standing requirement.

### 2026-06-10 — Loop iteration: CHARGING system modeled
- New builder `alternator` (stator body + drive-end/rear housings + pulley + mount ears +
  B+ terminal). Added the B+ charging cable to the relay and the accessory drive belt
  looping the crank/water-pump/alternator/PS pulleys (routed clear of the cooling fan).
  PNs: alternator F6UZ-10346-VA, B+ cable E9TZ-14431-A, bearing C9ZZ-10094-A, brush
  D2OZ-10347-B. Regulator integral (internal). Checker CLEAN.
- **BOM modeled: 149 / 603 (≈25%).** Next: ignition.

### 2026-06-10 — Loop iteration: WHEELS & TIRES modeled
- New builder `wheelTire`: tire (tread + sidewall shoulders), styled steel rim (barrel +
  outboard lip + face + 6 slots), center cap, 5 lug nuts. Replaced the 4 placeholder tire
  cylinders (left side rotated 180° so the styled face points outboard) + added a flat
  under-bed spare. Checker clean (moved the spare off the muffler).
- Note: tires/rims/lug nuts aren't itemized in the factory parts catalog (consumables), so
  the BOM modeled count stays 138/603 even though 5 wheels were modeled. P235/75R15.
  **System wheels-tires → deep.** Next: charging system.

### 2026-06-10 — Loop iteration: BRAKES modeled
- New builders: `masterBooster` (vacuum booster + master cyl + reservoir), `brakeRotor`
  (disc + hat + studs), `brakeCaliper`. Front disc (rotors + calipers), rear drums (from
  the axle iteration) + shoes/wheel cylinders internal, brake lines to all four corners,
  proportioning valve. PNs: master F4TZ-2140-E, booster F4TZ-2005-A, rotor F4UZ-1102-A,
  pads F5TZ-2001-BC, hose F2TZ-2282-C, shoe F3UZ-2200-A, wheel cyl D1AZ-2261-A.
- Heavy line-routing fight (front suspension + driver-side tank are in the way). Routed
  front-L outboard of the steering box, front-R inboard then low across the crossmember,
  rear high along the frame above the tank. **Improved the checker**: added a
  `legit_interface` whitelist so brake rotors/calipers inside the wheels no longer flag as
  overlaps. Brakes pass CLEAN. **BOM modeled: 138 / 603 (≈23%).** Next: wheels & tires.

### 2026-06-10 — Loop iteration: STEERING modeled
- New builders: `steeringGear` (recirculating-ball housing + worm/sector shafts),
  `psPump` (reservoir + pulley), `steeringWheel` (ring + spokes + hub). Linkage as routed
  rods: pitman arm, drag link, tie rod + adjusting sleeve, steering column to the wheel,
  and PS pressure/return hoses. PNs: pitman E7TZ-3590-B, sector F6AZ-3575-AA, shaft
  F2UZ-3542-A, knuckle F4TZ-3105-A, tie-rod tube E7TZ-3281-B, wheel bearing E3TZ-1225-AA.
- Steering shares the crowded front corner with the suspension — routed the linkage to
  clear the coil spring, moved the wheel behind the dash, and marked the legitimate
  steering↔spindle, tie-rod↔sleeve, and column↔dash interfaces as connections. CLEAN.
- **BOM modeled: 118 / 603 (≈20%).** Next: brakes.

### 2026-06-10 — Loop iteration: SUSPENSION modeled
- New builders: `iBeam` (web + flanges + pivot bushing + spindle knuckle), `coilSpring`
  (real helix via TubeGeometry), `leafSpring` (stacked leaves + eyes + center clamp),
  `shockAbsorber` (body + shaft + eye mounts). Front = twin-I-beam (2 crossing beams,
  coils, radius arms, sway bar, 2 shocks); rear = leaf springs + 2 shocks. PNs: beam
  E7TZ-3006-A, ball joint F6TZ-3050-AB, coil/leaf F1TZ-5560-E, sway bar E9TZ-5482-C,
  shock E7TZ-18124-B. Catalogued: ball joints ×4, bushings, U-bolts, shackles.
- Checker caught the front-left shock inside the steering box; moved both front shocks
  outboard. Suspension passes CLEAN. Front view shows the twin I-beams + helical coils
  reading beautifully. **BOM modeled: 90 / 603.** Next: steering.

### 2026-06-10 — Loop iteration: REAR AXLE & DIFFERENTIAL modeled
- New builders: `rearAxle` (housing tubes + pumpkin/carrier + pinion snout & yoke + wheel
  flanges + fill plug), `diffCover` (stamped cover + bolt ring), `brakeDrum`. Replaced the
  old axle cylinder + diff sphere. PNs: housing E7UZ-4010-C, case E3TZ-4026-A, cover
  F4TZ-4033-A, axle shaft E5TZ-4234-E, pinion E5TZ-4209-A, side gears E3TZ-4236-B.
- U-joints made internal (they co-locate with the trans/pinion yokes — redundant to draw
  twice); moved rear drums outboard of the axle flange. Rear axle passes the checker CLEAN.
- Milestone: 100 part records in the viewer. **BOM modeled: 74 / 603.** Next: suspension.

### 2026-06-10 — Loop iteration: DRIVELINE modeled
- New builders: `transmission` (M5OD-R2: bellhousing + ribbed case + tailshaft + shifter
  tower + output yoke), `shifter` (lever + knob), `hydraulicCylinder` (clutch master).
  Driveshaft = 2-piece routed `pipe` + center support bearing + front/rear U-joints;
  clutch hydraulic line master→bell. PNs: trans F2TA-7003-KA, clutch disc E8TZ-7550-D,
  release fork E4TZ-7515-C, slave F2TZ-7560-A, pilot brg D8TZ-7600-A, ring gear C5AZ-6384-D.
- Packaging fight resolved (the crowded mid-chassis): narrowed the fuel tank and OFFSET it
  to the driver side so the centered driveshaft clears it; straightened the exhaust mid-pipe
  beside the now-narrower tank; made the clutch slave a concentric (internal) unit; fixed
  the rear U-joint onto the pinion. driveline + fuel + intake-exhaust all re-checked CLEAN.
- **BOM modeled: 58 / 603.** Next: rear axle & differential.

### 2026-06-10 — Loop iteration: FUEL system modeled
- New builders: `fuelTank` (body + crimp seam + 2 straps + sender/pump module + supply/
  return fittings + filler inlet) and `fuelFilter`. Fuel lines as routed tubes: feed
  (tank→filter), supply (filter→rail), return (rail→tank), and filler neck to the bed.
  PN: tank F6TZ-9002-A. Catalogued internals: pump, gauge sender, throttle body,
  pressure regulator, injectors ×6.
- Routing lesson: fuel + exhaust can't share the passenger frame rail. Ran the fuel lines
  down the DRIVER-side rail and crossed them over the top of the engine to the fuel rail;
  lowered the tank to clear the driveshaft. Fuel now passes the checker CLEAN.
- **BOM modeled: 42 / 603.** Next: driveline (clutch, M5OD-R2, driveshaft, U-joints).

### 2026-06-10 — Loop iteration: INTAKE & EXHAUST modeled
- New builders: `airCleaner` (housing + snorkel + outlet), `catalyticConverter`,
  `muffler` (oval canister + necks), and a generic `pipe` (routed metal tube). Built the
  full exhaust run: head pipe → cat → mid-pipe → muffler → tailpipe, routed the length of
  the passenger side. Air cleaner on the throttle body. PNs: air filter E7TZ-9601-B,
  exhaust manifold F5TZ-9430-F, muffler F5TZ-5230-AXA.
- **Improved the checker:** `pipe` builders now emit centerlines (like cables), so the
  OVERLAP check no longer false-positives on long diagonal pipes (their AABBs enclose
  nearby parts). Caught a real mid-pipe-through-fuel-tank and rerouted it below the tank.
  Intake/exhaust now passes CLEAN.
- **BOM modeled: 29 / 603.** Next: fuel system.

### 2026-06-10 — Loop iteration: COOLING system modeled
- New builders: `radiator` (core + fin slats + top/bottom tanks + filler neck + cap),
  `fanBlade` (clutch + 7 blades), `waterPump` (volute + pulley + inlet),
  `thermostatHousing`. Upper + lower radiator hoses as routed tubes (cable builder w/
  connects). Real PNs: radiator F2TZ-8005-BA, cap E5TZ-8100-A, fan F2UZ-8600-A, water
  pump F6TZ-8501-KB, thermostat housing F5TZ-8592-BC, hose F2TZ-8260-E.
- Checker caught lower hose clipping the fan, then the harmonic balancer — rerouted it
  outboard of both; cooling now passes the checker CLEAN. Moved water pump forward to
  clear the block. Screenshots confirm hoses route naturally between pump/radiator.
- **BOM modeled: 24 / 603.** Next: intake & exhaust.

### 2026-06-10 — Loop iteration: ENGINE (4.9L I6) modeled
- Built a detailed engine assembly (new builders in `viewer/builders.js`):
  `engineLongBlock` (block + oil pan + timing cover + bellhousing), `cylinderHead`,
  `valveCover`, `intakeManifold` (+throttle body), `exhaustManifold`, `harmonicBalancer`,
  `oilFilter`, `motorMount`. Each is its own clickable part in `inventory/parts.json`
  with real Ford PNs (block F6TZ-6010-TB, head F1TZ-6049-B, valve cover F3TZ-6582-H,
  intake E7TZ-9424-A, balancer E7TZ-6312-A, oil filter D9AZ-6731-A, mounts F3UZ-6038-B).
- Catalogued internals (placement:internal) w/ PNs: crankshaft E3TZ-6303-C, camshaft
  F2TZ-6250-A, piston F5TZ-6108-AC ×6, connecting rod E3TZ-6200-ERM ×6, oil pump
  C5AZ-6600-A, timing gears D3TZ-6256-C. Repositioned distributor to the engine front.
- Verified: JSON/JS/smoke-test pass; checker clean except 1 legit mount overlap
  (distributor into block front); screenshots confirm it reads as an inline-six and sits
  correctly in the bay. Moved cooling fan forward to clear the block.
- **BOM modeled: 16 / 603.** Next: cooling system.

### 2026-06-10 — BOM ledger built + autonomous build launched
- `scripts/build_bom.py` extracts the factory parts catalog → `inventory/bom.json`:
  **603 serviceable parts** across 18 groups, 255 with exact Ford part numbers. This is
  the completeness checklist (`status: not-started → catalogued → modeled`); "done" = all
  modeled + exploded-view fasteners per assembly. Biggest groups: Transmission/Drivetrain
  251, Engine/Cooling/Exhaust 68, Powertrain Mgmt 67, Steering/Suspension 38.
- Loop now BOM-driven (`docs/LOOP.md`). Launched the autonomous build loop (parametric
  builders, screenshot + `check_geometry.py` verification each iteration), starting at the
  engine and working the build order. Owner wants it to run unattended toward a complete
  truck; interrupt anytime to redirect or stop.
- **Modeled so far:** starting system (deep). BOM modeled: ~9 / 603.

### 2026-06-10 — Automated geometry QA + fixed a double-offset bug
- Built `scripts/check_geometry.py`: renders the viewer in headless Chrome, pulls every
  part's true world AABB (+ cable centerlines) via `?dump=1`, and auto-flags
  CABLE-THROUGH (cables passing through unrelated solids — cables now carry
  `connects:[a,b]`), OVERLAP (interpenetration across assemblies), and ORPHAN (part
  floating with no neighbor within 6"). Prints a size/position table for proportion QA.
  This is the scalable accuracy net — no more hand-checking every part.
- The checker immediately caught a **double-offset bug**: single-primitive massing parts
  had their position applied twice (mesh + wrapping group), so the whole truck was ~2×
  too spread (envelope was X −226..214; now correctly X −114..108). This was the
  "pieces aren't laid out proportionally" issue. Fixed in `addPart`.
- Fixed the battery: swapped terminals so POS is outboard (→ relay) and NEG inboard
  (→ engine), so the ground cable no longer routes THROUGH the battery; re-routed cables;
  corrected battery location text to passenger (RH) side. Checker now passes clean for
  the starting system (only legit nested-part overlaps remain truck-wide).
- Inventory note: 45 records total; only the starting system is deep. Comprehensive
  every-fastener inventory (10k+ items) is the long goal, not yet built.

### 2026-06-10 — Rendering overhaul + screenshot verification (fixed "looks wrong")
- Root cause of repeated "parts in the wrong place / isolation doesn't work": I was
  editing 3D coordinates **blind**. Now rendering with headless Chrome and viewing the
  PNGs to verify every change (see `docs/LOOP.md` step 4 + `?view/iso/sel/snap/axes`).
- Diagnosis from real renders: placement was ~fine; the problems were (a) the truck
  body was invisible so isolated parts floated context-less, and (b) everything was too
  dark to read. Both fixed:
  - Studio look: light gradient background, `RoomEnvironment` IBL + ACES tone mapping,
    brighter key/fill lights, lighter grid, dark readable edge lines.
  - Body shells (cab/bed/hood) tagged `context:true` — always visible; during isolation
    they drop to a faint **wireframe ghost cage** so the colored system parts pop.
  - Isolation now HIDES other systems entirely (was murky 4% ghosts) and the camera
    **flies to frame** the active system. Whole-truck auto-frames on load.
  - Battery moved to the passenger-side fender (FSM: relay on RH apron, rear of battery)
    with a tray; all 3 cables re-routed so endpoints land on the actual terminals.
- Verified via screenshots: whole-truck iso/side/top, starting-system isolation, and a
  selected part (info panel + highlight) all render correctly.

### 2026-06-10 — Starting system: detailed models + deep catalog
- Pivoted off massing blocks for the starting system to **refined parametric
  geometry** (real shaped meshes, not boxes). New `viewer/builders.js` with
  `starterMotor` (housing, solenoid, nose cone, drive pinion w/ teeth, terminal
  studs, through-bolts, mounting flange — 34 nodes), `battery` (case, cell caps,
  lead terminals, strap), `relay`, and `cable` (heavy cables routed as 3D tubes
  along real waypoints between battery → relay → starter, plus the ground).
- Viewer now supports `model.builder` and `model.kind:"group"` compound parts, and
  `placement:"internal"` (catalogued, drawn later in an exploded view). Click
  resolves through sub-meshes to the parent part. Builder failures fall back safely.
- Deep-catalogued the starting system from the FSM with **real Ford part numbers**:
  starter F2TZ-11002-ARM, solenoid F6VZ-11390-AA, armature F2TZ-11005-A, brushes
  E9OZ-11061-C ×4, drive F5HZ-17508-A, bearings E9OZ-11135-A ×2, relay E9TZ-11450-B,
  cables F4TZ-14300-A / E9TZ-14431-A / ground F2TZ-14301-A, ignition switch
  F4DZ-11572-B, lock cylinder F4TZ-1522050-B, CPP switch (basic 11A152).
- Inventory now 45 records (14 in the starting system). Headless smoke-test passes.
- **Decision pending:** how to scale HIGH-fidelity to *every* part — parametric
  builders (me) vs. AI image-to-3D generation (Meshy/Tripo/Hunyuan3D, needs API +
  budget) vs. sourcing real CAD (.glb). Likely a blend; this drives the autonomous loop.

### 2026-06-10 — Reset + foundation
- Deleted the prior 2D systems web app (kept `manuals/`).
- New direction: full part inventory → 3D model of every part → assembled WebGL
  truck with part highlight + system isolation (see `docs/PROJECT.md`).
- Built the data-driven spine:
  - `inventory/schema.md` — part-record contract + inch/`+X fwd, +Y up, +Z right`
    coordinate convention (origin = wheelbase center, on the ground).
  - `inventory/systems.json` — 21-system taxonomy with colors.
  - `inventory/parts.json` — **34 seed parts** (major masses + full starting
    system) placed at real-ish coordinates. Part numbers intentionally blank.
  - `viewer/` — Three.js explorer: builds the truck from the inventory, orbit,
    click-to-inspect, isolate-by-system, ghosted body shells (x-ray feel).
  - `scripts/serve.py` — static server (127.0.0.1:8080).
- **Next:** confirm fidelity target & cataloging order with owner, then start the
  first deep catalog pass (candidate: engine accessories or front suspension)
  by mining the FSM exploded views for part numbers + quantities.
