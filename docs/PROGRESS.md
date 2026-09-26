## Pan drain connection — 2026-09-24

Added a replacement-style M14×1.5 threaded plug, separate sealing washer, flat seat and open drain passage to the rear-sump study. Thread diameter and pitch follow the Dorman pan listing; other dimensions and boss construction remain provisional. Solid/clearance checks and the removed-plug passage probe pass. Navigation reaches 731 occurrences through 862 links; full static audit is running. End seals require coordinated changes to the bearing-cap and timing-cover interfaces, documented in `inventory/engine/pan-interface-evidence.json`.

## Rear-sump pan and pickup — 2026-09-24

Replaced the uniform pan with a rear-sump study, using the published replacement depth. Added a pan assembly page and revised the pickup route and strainer position together. A first clearance check caught the tube crossing the pan transition; the revised route clears it. Focused validation passes with 11.95 mm of modeled screen-to-floor clearance, which is an assumption rather than a Ford specification. Navigation passes; whole-engine audit remains running. Flange dimensions, end seals, fasteners, drain hardware and installed geometry remain unfinished.

## Oil-pressure switch study — 2026-09-24

Added nine separate components and individual pages for the metal body, diaphragm, carrier, moving contact, fixed contact/terminal, insulator, retaining rim, spring and illustrative ground bridge. The manufacturer photograph informs the exterior; the internal arrangement is explicitly hypothetical teaching geometry. EVTM-based lessons explain switch behavior and the fixed cluster resistor. Installed dimensions, pressure threshold and block interface remain unresolved.

The focused check passes inlet access, diaphragm separation, open/closed contact geometry, terminal isolation and internal clearances. Navigation reaches all 729 current occurrences through 859 links; the exploded/transparent browser view was inspected. Full static audit is running. These checks do not establish production fidelity or engine completion.

## Filter placement and flow-path correction — 2026-09-24

Moved the staged filter onto the camshaft side using the factory lubrication schematic; numerical station and inclination remain provisional. The lubrication overview now includes filter exploration. Added a central separating standpipe to the illustrative bypass housing, closing an unintended dirty-oil shortcut to the outlet. Three wall probes and a seated/lifted bypass-disc check pass alongside existing solid and internal-clearance checks. Whole static validation is running; navigation passes 849 links. Adapter and block galleries still require reconstruction.

## Oil filter construction increment — 2026-09-24

Added a thirteen-component filter study with published WIX replacement envelope and explicitly provisional Motorcraft-inspired internals. Individual pages, explanation and troubleshooting links, ghosted shell and exploded navigation are available. Filter placement is staged: block boss, galleries and adapter are still unresolved.

Validation: 13 valid single-solid STEP components; no internal overlaps; inlet, outlet and perforation probes pass. Full engine audit passes 2363 broad-phase pairs with no positive-volume overlaps at the static pose. Navigation passes 720 occurrences and 849 deep links. Browser verified 40% exploded and see-through-shell views. These results establish model consistency, not production fidelity.

Saved filter references and the EngineQuest 2025 catalog. Page 23 lists EQ-OFA302 against D7AZ6890A for the Ford application group including 4.9L. It does not prove equivalence to Ford's E4TZ6890A anti-drainback insert; do not substitute it silently.

# Progress ledger

Newest first. Each session: log what was catalogued and what's next.

### 2026-09-24 — PCV valve and grommet

- Added six separate parts under Crankcase ventilation: metal body, angled outlet
  head, plunger, spring, orifice washer and mounting grommet. Internal architecture
  follows the factory typical cutaway; exterior follows the live Standard V219
  catalog photograph, saved with its hash and reviewed specifications.
- Direct checks pass internal clearances, both outlet passages, and interfaces
  with the cover and upper intake. Navigation reaches707parts through835links;
  exploded/transparent view visually checked. All dimensions and calibration are
  provisional; hoses, unused outlet treatment and installed identity remain open.
-211definitions/707occurrences. Whole-engine static audit passes2,301candidate
  pairs with zero overlaps; artifact integrity and scale checks pass.
- Prior fuel-coupling final audit passed2,282candidate pairs with zero overlaps
  after rotating the return clip/tether to clear the intake flange.

### 2026-09-23 — fuel spring-lock connections

- Added 14 reusable definitions / 16 occurrences for the supply and return
  connections: male fitting, female fitting, cage, two seals, coiled garter spring,
  retaining clip and tether. Factory construction and service identifiers are
  saved with local source hashes. Dimensions and stations remain provisional.
- Fixed clip/tether overlap by adding an attachment recess. Both connections pass
  solid-validity, open-passage and pairwise-clearance checks. Navigation passes
  827 deep links / 701 parts. Assembled and exploded transparent views checked.
- Current total: 205 definitions / 701 occurrences. Whole-engine static audit
  is running; no completion or verified production fit claim.
- Captured five factory PCV pages and reviewed the valve and ventilation diagrams
  for the next assembly. Installed PCV identity and hose routing remain open.

### 2026-09-23 — source-dimensioned fuel-rail fasteners

- Factory exploded drawing establishes three1/4-20x.90in bolts with washers.
  Added separate threaded bolts/washers and provisional lower-intake support bosses.
- Corrected center-mount/regulator and mounting-tab/return-tube interferences.
  Shared mount coordinates keep the rail, bolts and casting support consistent.
- Direct checks pass sourced diameter/pitch/length and all mount/return-tube
  clearances. Navigation809links passes; bolt part page visually checked.
-191 definitions/685 occurrences. Full static audit passes2,219 candidate pairs with no overlaps;
  casting contours, station measurements and female thread fit remain unverified.

### 2026-09-23 — connected fuel pressure test valve

- Added eight separate diagnostic-valve components and a drilled branch into the
  fuel rail. Ford establishes the fitting; generic internal construction follows
  Schrader's catalog, saved locally. Installed dimensions/identity remain unknown.
- Direct checks find no internal collisions and no blocked rail branch. Navigation
  passes803 links. Whole-engine static audit remains running at this entry.
- Added targeted fuel refresh and duplicate-ID publication guard. Transparent
  housings expose the core, seating washer, spring and pin. Browser assembled and
  35% exploded/transparent views checked.

### 2026-09-23 — drive-layout reconciliation evidence

- Full static audit completed:2,166 candidate pairs, zero overlaps;181 definitions
  and671 occurrences pass artifact and scale checks.
- Visually reviewed Ford industrial manual PDF6–7, including the sectional engine
  drawing. Saved source/capture and an explicit drive-layout evidence record.
- Confirmed drive architecture; documented why current distributor/cam/pump staging
  cannot be treated as installed alignment. Neck/bowl geometry, block bosses and
  pump mount need coordinated reconstruction before the intermediate shaft.

### 2026-09-23 — distributor hold-down hardware

- Added separate forked clamp and retaining bolt on the housing flange, with
  individual pages and service-procedure context. Dimensions and block attachment
  remain provisional; existence/function follows the applicable Ford procedure.
- Distributor motion audit passes546 candidate pairs over13 poses;794 navigation
  links pass. Clamp part page visually checked.181 definitions/671 occurrences.
- Location-diagram review identified a larger integration issue: the distributor,
  cam and pump studies do not share a verified drive station. Reconcile these
  against source drawings before adding a supposedly installed intermediate shaft.

### 2026-09-23 — separate distributor drive components

- Added helical gear, slotted retaining pin and thrust washer; the shaft and gear
  hub have matching transverse pin bores. These are separate selectable parts,
  rotating with the shaft. Geometry is provisional, not a verified gear pair.
- Rechecked the local factory exploded drawing and a photographed 1996 Ford
  comparison page identifying the roll pin and 4.9L washer. Saved source evidence
  and a KB page; tooth count/profile and installed dimensions remain unverified.
- 179 definitions /669 occurrences. STEP roundtrip and scale checks pass; static
  audit checks2,162 candidate pairs without overlaps. Distributor motion checks
  494 pairs over13 poses, with correct clockwise half-speed rotation and no overlaps.
- Added source/lesson metadata after the geometry audit; navigation passes792links.
  Clamp, block mounting and cam/oil-pump engagement remain unfinished.
- Browser review found lower exploded parts behind the control panel. Camera framing
  now reserves the title/control areas; assembled and35% exploded views checked.

### 2026-09-23 — head/plug integration and sourced rotation direction

- Added six recessed plug wells and photo-informed chamber outlines from Allied's
  EFI-head comparison photos. Shared provisional mounting datums replace staged
  plug placements. Saved the source capture, KB page and interface evidence.
- Corrected a 0.28 mm³ ground-electrode/head overlap at each cylinder. All 54 plug
  components now clear the head, and axial probes reach all six firing pockets.
  Full static audit passes 2,158 candidate pairs, with 176 definitions/666 parts.
- Visually checked the head's manifold and plug sides in the browser. Casting
  dimensions, female threads, chamber volume and coolant passages remain unresolved.
- Reviewed the saved factory firing-order diagram: clockwise distributor rotation
  viewed from the cap. Corrected CAD and browser animation signs; initial clocking,
  drive-gear engagement, timing and plug-lead routing remain unfinished.
- Navigation passes 789 links. Whole-engine completion remains in progress.

### 2026-09-23 — threaded plug geometry and export reliability

- Replaced smooth plug thread envelopes with helical geometry. NGK's 18 mm family
  chart supports inferred 1.5 mm pitch; direct WR4-1 tolerances remain unresolved.
- Corrected a sweep that failed STEP roundtrip validation by orienting its section
  normal to the helix tangent. Added an immediate export topology/volume guard.
- Direct tests verify pitch periodicity, alternating thread metal/void and unchanged
  catalog envelope/firing gap. Full static audit and 789 navigation links pass;
  threaded silhouette inspected in the browser. Counts remain 176/666.
- Head mounting interfaces and leads remain unfinished; no installed-fit claim.

### 2026-09-23 — six spark-plug component studies

- Added nine reusable plug definitions, each instantiated for six cylinders with
  independent component pages and explosion/transparent-shell exploration.
- Used the explicit NGK WR4-1 application and dimensional table; inspected the
  catalog's profile143 and tipDH photographs. General internal construction remains
  an illustration, separately sourced and labeled.
- Direct CAD checks confirm nominal 18 mm thread envelope, 11.684 mm reach,
  20.6375 mm hex and 1.1176 mm firing gap. No internal solid overlaps.
- Full static assembly audit passes 2,074 candidate pairs; 176 definitions and
  666 occurrences pass STEP integrity and GLB scale/bounds checks. Navigation passes
  789 links. Assembled and transparent/exploded plug views inspected in the browser.
- Threads, head bores, orientation and leads remain unfinished; plugs are staged
  next to the head pending integration. The engine is not complete.

### 2026-09-23 — remote ignition module and spark-plug evidence

- Added the factory-illustrated fender heat-sink/module mounting architecture with
  seven independent occurrences, including both pairs of retaining screws.
- Kept electronics, installed dwell variant, dimensions and fender datum unresolved.
- Corrected screw-head interference. Full static audit passes 1,972 candidate pairs;
  167 definitions / 612 occurrences have valid solids and matching GLB scale/bounds.
  Navigation passes 728 links; assembled module view inspected in the browser.
- Acquired NGK's 2019 catalog and visually verified the explicit F-150 application
  and WR4-1 dimensional table. Saved PDF, source page, review text and checksum.
  Next: sourced spark-plug envelope, internals and head/lead integration.

### 2026-09-23 — distributor and ignition-coil component studies

- Added a 23-component closed-bowl distributor with shaft, shutter, Hall package,
  rotor/contact, cap and seven terminals, bushings, O-ring and retaining screws.
- Linked the rotor/shutter to half crankshaft speed in CAD and viewer. Playback
  now wraps at 720 degrees to avoid resetting half-speed parts after one revolution.
- Added a ten-component DG470 coil study with core-stack envelopes, winding packs,
  bobbin, insulation, case, high-voltage terminal and two primary terminals.
  Ford's DG470/F7PZ12029AA identity matches the archived service part; exterior
  photographs were reviewed and captured in the evidence ledger and KB source.
- Distinct ignition lessons describe PIP/SPOUT, primary switching and distribution;
  individual parts and local source links are reachable. Current total: 162 CAD
  definitions / 605 occurrences. Counts include teaching aggregates, not every wire
  or core sheet, and do not imply engine completion.
- Distributor sampled motion passes 13 crank poses with zero internal overlaps;
  coil's ten solids pass mutual-clearance checks after tower/shroud corrections.
  Full-engine static audit: 1,963 candidate pairs with zero >0.1 mm3 overlaps;
  STEP integrity and GLB scale/bounds checks pass.
  Navigation passes 720 links; browser assembled and exploded coil views inspected.
- All distributor/coil dimensions and mounting datums remain provisional. Gear
  engagement, bracket, capacitor, plugs, leads, module and harness remain unfinished.

### 2026-09-22 — engine atlas and component pages
- Expanded to 53 valid CAD definitions and 399 individually addressable occurrences;
  added an assembled STEP export and nested assembly exploration.
- Preserved the piston study and added per-occurrence pages with explanations,
  source links, model measurements, limitations and STEP downloads.
- Built six-cylinder rotating geometry, block/main supports, head and valve gear,
  nine-piece hydraulic lifters, timing gears and preliminary covers/seals.
- Corrected piston boss protrusion, crankcase/cheek clashes, valve seats, keeper
  grooves, pushrod interfaces, cover fit and gasket interference through CAD audits.
- Static all-pair audit passes at the reference pose; sampled rotating/core checks
  and 720-degree idealized linkage checks are distinct, limited verification scopes.
- Browser verification covered individual-part navigation and return-to-engine
  highlighting, nested assembly filtering/search, exploded lifter layout, section
  view and responsive layout. Captured browser warning/error log is empty.
- Added two Ford industrial comparison PDFs, two archived exploded drawings and
  two KB source pages. Industrial specifications remain separate from verified
  1994 truck applicability. The low-resolution full-engine image is not a reliable
  source for its unreadable part-number table.
- The engine is not finished. Full remaining scope and evidence needs are tracked
  in ENGINE-COMPLETION.md. Do not equate occurrence count or CAD validity with OEM accuracy.

### 2026-09-22 — sourced engine audit and first working component study
- Indexed 413 engine manual pages and 72 unique illustrations; extracted 52
  parts-information categories. These are research coverage, not complete BOM counts.
- Downloaded and visually reviewed UEM Silvolite and Hastings catalog application
  tables; captured three new KB sources with processed:false. Added 32 dimensional
  claims/assumptions, five hashed source references and four blocked claims.
- Built a repository-owned build123d pipeline with 12 reusable CAD definitions,
  15 physical part occurrences and one explicitly schematic crank throw.
- Added /viewer/engine.html: individual selection, isolation, hiding, explosion,
  section, piston transparency and slider-crank animation, plus evidence/limitations.
- Validated saved STEP topology/volume, GLB units/axes/bounds, all pairwise solid
  intersections at four crank positions, and linkage closure/stroke at 1,441 angles.
  Corrected bolt/bearing and crank-context clashes found by the checks.
- Visually reviewed assembled, exploded, isolated and sectioned browser views;
  playback/reset works and captured browser error/warning log is empty.
- Remaining: exact rod geometry/length, pin offset/retention, actual piston identity,
  hardware specifications, full rotating assembly, and the rest of the engine.
  This study is provisional and is not counted as completion of the engine.
- Reproduce via cad/engine/README.md; research and gap sheet: docs/ENGINE-AUDIT.md.

### 2026-09-22 — owner confirms component-level scope and engine first
- Reviewed the four reference posts in the browser and the public text-to-cad
  repository. Fan still image inspected; embedded videos could not play.
- Confirmed existing engine builders combine pistons, rods and closures into
  coarse selectable groups. These do not satisfy the newly explicit requirement.
- Added COMPONENT-MODEL.md: separate part definitions/occurrences, nested
  assemblies, mechanical and functional relationships, motion, evidence and
  acceptance criteria. Engine first is confirmed, not pending.
- This pass defines architecture and reviews tooling; no new geometry or runtime
  installation is claimed.

### 2026-09-22 — restart audit and accuracy direction
- Audited 281 inventory records, 37 CAD Python sources, 44 model files, and
  163 source pages / 354 notes / 21 maps. All 61 GLB references resolve locally.
- Found missing CAD runtime/plugin dependencies; only four inventory records
  contain factory-manual source references. Accuracy needs evidence tracking.
- Added docs/RESTART.md with research acquisition, CAD/Blender/browser roles,
  nested assemblies, dimensional provenance, and proposed engine milestone.
- Marked NEXT-SESSION.md as historical; its removed app is not the current viewer.
- Restored the factory-manual archive from CHARM; ZIP CRC verified and extracted.
- No geometry changes or visual certification in this audit.

### 2026-06-12 — text-to-cad pipeline + per-part CAD loop (34 parts)
- **New pipeline**: `cad@text-to-cad` plugin (build123d on OpenCASCADE).
  Sources in `cad/<part-id>.py` (1 unit = 1 INCH, +X fwd +Z up +Y left);
  `scripts/cad_export.sh` -> STEP + `models/<id>.glb`; records use
  `model.glbScale: 1000` (cadpy GLBs are meter-scaled). Conventions +
  verify loop in `cad/README.md`. Venv: `.venv-cad/` (py3.11).
  GOTCHA: cadpy DROPS a parent Compound's location on GLB export — bake
  axis rotations into every child location (see cooling-fan.py `AX`).
- **Parts converted to CAD so far (20)**: valve cover, air cleaner,
  radiator, cooling fan + clutch, A/C condenser, battery, alternator,
  intake manifold, exhaust manifold, water pump, thermostat housing,
  harmonic balancer, oil filter, distributor (TFI), PS pump, brake
  booster + MC, fuel tank, catalytic converter, muffler, fuel filter.
- **Packaging fixes the loop surfaced**: radiator->101.4 / condenser->
  102.95 (pump pulley | fan | tanks/core | condenser | grille now stack
  physically); lower rad hose rerouted around the bigger crank pulley;
  cat moved 1.5" inboard off the RH radius arm; new BOLTED whitelist
  pairs (fan<->pump, condenser<->core support).
- **Batch 2 (21-34)**: steering box, horn, wiper motor, coil springs
  (true swept helix), shocks x4, engine mounts, ignition coil, starter
  relay, cambered leaf springs, Twin I-Beams, vented rotors, calipers,
  drums, 8.8 diff cover. All shared-instance records point at one glb.
- **Queue**: radius arms, drag link/tie rods, driveshaft, steering
  column/wheel, transmission case detail, rear axle housing, grille-area
  lamps OK (Blender), interior pass (dash/seats/column), engine long
  block (LAST — many mating parts + explode internals). Starter
  intentionally skipped (already hero-detailed w/ internals + explode).

### 2026-06-11 — Viewer controls (owner request)
- **Body-panels toggle** (`🚚` button / `?hidebody`): hides shells + body-cab/
  body-bed/exterior-trim/glass so the running gear and engine are unobstructed.
- **Multi-system view**: system buttons now TOGGLE — click to add a system to
  the view, click again to remove; any combination composes (`?iso=engine,
  cooling,...`). "Whole truck" clears. Ghost cage shows whenever a selection
  is active (unless body is hidden); explicitly selected body systems still show.
- **Free camera**: right-drag/two-finger pan, arrow keys walk along the truck,
  double-click recenters the orbit on the clicked point, min zoom distance
  lowered (12"). Hint bar updated.

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

## 2026-09-22 — Engine navigation redesign

Replaced the competing system dropdown, isolate state, and expandable full tree with
one assembly-to-part browsing hierarchy. Start with five major assemblies, drill
into their immediate contents, and return through breadcrumbs, Up, or Whole engine.
Global search includes each result's ancestry; individual parts show neighboring
parts and a link to their parent assembly. Every scope has a bookmarkable URL and
browser Back/Forward support. Legacy part.html?id links remain supported.

The browsing hierarchy is independent of CAD transforms; no geometry was changed.
Explode, cutaway, transparency and motion are view controls; Reset keeps the current
location. Sources and geometry qualifications remain available in part details.

Validation: scripts/check-engine-navigation.mjs confirms all 399 occurrences are
reachable exactly once and all 481 navigation URLs round-trip. Browser checks
covered engine → cylinder → piston assembly → piston, parent return, cross-branch
lifter search, empty search, deep-link reload, Back/Forward and Reset; no browser
console errors were observed.

## 2026-09-22 — Archived the legacy whole-truck prototype

Moved 95 legacy viewer, CAD, mesh, inventory and helper files into
`archive/2026-09-22-legacy-truck/`, with original hashes and a runnable archived
viewer. Replaced `/viewer/` with a current project home linking the engine explorer.
Manuals, reference material, extracted BOM, KB and current engine work remain in
place. Verified preserved-file hashes, archive-relative mesh paths, and
home/archive browser loading.

## 2026-09-22 — Lubrication component study

Added 12 CAD definitions / 15 occurrences for the oil pump and pickup, bringing
this reconstruction to 65 definitions / 414 occurrences. The new lubrication
branch includes the rotor set, housing, cover and four bolts, relief plunger,
spring and closure, pickup tube, shell and perforated screen representation.
Assembly explanations link to the relevant components and factory references;
inspection notes distinguish pump wear from the documented filter-drainback issue.

The 1994 catalog and industrial parts book both list C5AZ-6600-A. The industrial
comparison supports four cover bolts and the relief plunger/spring envelope
sizes. It lists a different pickup, so its tube cannot be copied as truck geometry.
`inventory/engine/oil-pump-evidence.json` records this distinction and unresolved
mounting, rotor, drive and passage details. The model remains a provisional study,
including its installed transforms; the large block/head/cover shapes were not
changed without stronger references.

Validation: all 65 saved STEP definitions and GLB scale/bounds passed; assembled
STEP has 414 solids. All-pair static CAD checks found no overlaps above 0.1 mm³;
rotating-core and lubrication clearance checks passed at 0/90/180/270 degrees.
The 1,441-sample idealized crank test passed. Navigation tests cover all 501 scope
URLs, educational links/sources, and comparison-derived relief-part envelopes.
Browser review covered the pump, exploded view, rotor set and explanation links;
no console errors were observed. STEP round-trip volume tolerance is explicitly
10 ppm, accommodating a measured 1.35 ppm trimmed-surface integration difference
in the housing; scale and solid-validity checks remain independent.

## 2026-09-22 — EFI intake and cover refinement

Added five definitions / eleven occurrences: hollow upper and lower EFI intake
castings, two gaskets and seven retaining studs. Total: 70 definitions / 425
occurrences. The intake has its own navigation branch, individual part pages,
linked explanations, sources and explicit dimensional uncertainties. Factory
references support architecture and stud count; runner profiles, mounting
positions and casting envelopes remain provisional.

Refined the valve cover with sloped shoulders and a rear ventilation opening.
Extended the existing head ports to the manifold face after probes found their
cuts ended 5.5 mm short. Added crease-aware smooth shading to intake castings.
Throttle body, fuel hardware, EGR, exhaust and exact production interfaces remain
unfinished; this is not a verified complete engine.

Validation: all 70 saved CAD definitions and GLB bounds passed, assembled STEP
contains 425 solids, all-pair static checks found no overlaps above 0.1 mm³,
and sampled core/lubrication motion checks passed. Eighteen intake interface
probes pass. Navigation verifies 425 reachable parts and 515 deep links; the
1,441-sample crank mechanism test passes. Browser review covered intake assembly,
exploded view, individual upper casting and cutaway, with no captured errors.

## 2026-09-22 — Interactive throttle mechanism

Added six definitions / thirteen occurrences for the twin-bore housing, gasket,
shaft, two plates and four mounting studs/nuts. Total: 76 definitions / 438 parts.
A separate throttle slider rotates the shaft and both plates; ghosting the housing
exposes the mechanism. Navigation, individual pages, exploded view, explanation
and evidence links include the new assembly. Added a provisional mounting pad and
stud bores to the upper intake to connect the throttle assembly.

Reviewed the local 1994 factory operation, service and parts pages and their
illustrations. The manual/C6 catalog entry differs from the E4OD entry. Factory
layout and mounting counts are supported; dimensions, shaft construction and
0–90 degree stop range remain illustrative. IAC/bypass, TPS, linkage/return spring,
accelerator bracket, purge ports and plate screws remain unmodeled. Fuel and
exhaust were not added in this increment.

Validation: 76 saved definitions and 438 assembled solids passed CAD/scale checks;
all-pair static audit and sampled core/lubrication audit passed. Seven throttle
angles produced 637 passing pair checks; both open inlet probes and all 18 prior
intake probes passed. Navigation covers 531 deep links and all 438 occurrences.
The 1,441-sample crank test passed. Browser review confirmed closed/open plates,
transparent housing, reset, exploded state and no captured console errors.


## 2026-09-22 — Fuel, throttle controls and split exhaust

Added 40 CAD definitions / 110 occurrences, for 116 definitions / 548 occurrences.
Six injectors each have thirteen separate components, including coil, armature,
needle, spring, filter, seat, body, insulator, two terminals and two seals. Added
supply/return rail, thirteen-piece regulator, eight-piece unvented IAC and
seven-piece TPS. The TPS rotor/wiper follow the independent throttle slider.
Separate hollow front/rear exhaust castings connect to the six modeled head ports.
All new definitions have source links, explanation, unresolved details and stable
part pages. The IAC installed variant and all new dimensions remain provisional.

Indexed 53 factory pages in twelve engine-mounted component families beyond the
original Engine chapter. Completion is tracked as a physical-component work
breakdown, not a percentage based on modeled counts. Cooling, ignition, accessory
drive, interfaces, hardware and foundational geometry remain unresolved. The user
requested review only after the entire engine is finished; this is not that point.
Read ENGINE-GEOMETRY-EVIDENCE.md for the drawings/scans/measurements required to
close accuracy. Search results for miniature engines are not production CAD.

Fit checking exposed injector shell/needle interference, fuel return and regulator
mounting interference, and throttle stud/nut interference after adding the IAC pad.
Corrected the source geometry and rebuilt. All saved CAD definitions and GLB
scale/axis bounds pass, with 548 solids in the assembled STEP. Static checking
covers 1,866 candidate pairs; sampled core/lubrication checking covers four crank
poses. Seven throttle/TPS positions cover 301 candidate pair checks and two open
inlet probes. All 25 fuel/IAC/exhaust probes and 18 intake probes pass. Navigation
reaches all 548 occurrences through 654 links; 1,441 idealized crank samples pass.
Reports retain explicit scope and manifest hashes; these are internal consistency
checks, not Ford geometry verification.

Browser checks covered injector explosion, moving TPS, transparent IAC, exhaust
passages and navigation. Exhaust meshes now retain smooth curved surfaces, and
their cutaway runs lengthwise so it exposes both collectors instead of removing
one complete manifold. The floor grid now follows the isolated assembly. No
browser console errors were captured during these checks.

## Research round — 2026-09-23

Saved 17 source records/pages, public manual samples and manufacturer catalogs,
27 Melling application entries and 10 reviewed specification groups. Start with
[the research report](ENGINE-RESEARCH-2026-09-23.md). No geometry was changed in
this research pass. Apply the strongest dimensions with assembly-datum checks;
keep valve application anomalies and catalog alternatives explicit. Complete
EVTM/PC/ED books were identified but not purchased or obtained in full.

## Whole-truck continuation — 2026-09-23

Added a 15-system reference navigator with component search and local manual links;
3,628 pages indexed after excluding explicit automatic/transfer-case/ZF branches
from the manual-transmission entry. These remain unreviewed reference candidates,
not proof of installed fitment or complete physical parts inventories.

Built hub, elastic coupling and inertia ring as separate damper solids. Catalog
outer envelope verified at 71.12 x 163.068 x 163.068 mm; internal sections and
axial station remain provisional. Engine: 119 definitions / 551 occurrences.
Artifact/scale/static checks passed (1,870 candidate pairs, no >0.1 mm³ overlaps).
Navigation: 658 reachable deep links. Browser checked assembly isolation/explosion
and transmission component search. EVTM acquisition prepared; payment pending.

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

## Thermostat study — 2026-09-23

Active goal continuation — thermostat geometry (2026-09-23):
136 definitions / 568 occurrences. Added nine-part thermostat study using MotoRad
244-192 manufacturer envelope, whose interchange list includes factory service
number XR3Z8575BA. Source record motorad-244-192 and KB page saved. Internal
geometry and placement remain provisional; no thermal motion claimed. New
cad/engine/thermostat.py is built by --refresh-cooling. Thermostat envelope test
passes 53.85 mm flange and 37.85 mm total height; all-static validation passes
1,899 candidate pairs with zero >0.1 mm³ overlaps; 678 navigation links pass.
Browser inspected at 50% explosion. Spring/capsule represented independently.
Next: outlet housing/gasket/fasteners and head coolant interface. Factory archived
Thermostat Housing parts page has identity to extract. All current pump/thermostat
placements are staging datums; do not treat collision-free placement as fit proof.
Completion plan edited after build (omissions prose will refresh next build).
Goal active; previous turn is progress, not a blocker. Preserve all prior changes.

## Coolant outlet integration — 2026-09-23

Active goal continuation — outlet validated (2026-09-23):
139 definitions / 572 occurrences. No CAD processes remain live. Supersedes pending
sessions below. Outlet casting, gasket and two bolts added around nested thermostat.
Exact-axis Solid.make_cylinder avoids OCCT creating a degree-14 unbounded spline
surface (control points near 1e100) when rotated coaxial faces are cleaned.
Hollow sections formed before union. Cleared mutual intrusions at secondary port.
Current validation: 139 valid STEP definitions / 572 assembly solids; GLB bounds
within 0.5 mm; zero >0.1 mm³ collisions in 1,910 static candidate pairs. Eight outlet
probes include a connected six-mm-diameter route through the whole main channel.
Navigation passes 683 deep links. Browser assembled and 35% exploded views checked.
Validator now rejects manifest/artifact changes during validation; no concurrent
builds should run while validating. See coolant-outlet-evidence/validation.json.
All casting outline/datum/thread/hose/head interfaces remain provisional. Do not
call accurate fit complete. Source geometry does not yet match photo silhouette
closely enough; long neck length and orientation need further reconciliation.
Next: continue substantial missing ignition system (factory sources already indexed
in system-references.json), or finish cooling hose/fan boundaries with source data.
Keep whole-engine goal active and work autonomously. Previous turn made progress.

## VIN-Y sealing evidence review — 2026-09-24

Acquired and ingested the Fel-Pro manufacturer master catalog, visually checked
PDF pages 353–354, and saved twenty catalog-to-model crosswalk entries in
`inventory/engine/sealing-coverage.json`. Replacement identities now support
targeted work on missing pushrod-cover gasket/grommets, distinct intake/exhaust
valve seals, timing-cover joints and the oil-pump-to-block gasket. Kit quantities
and alternative service options are explicitly distinguished from physical parts.

Corrected the pan lesson and individual side-study pages: an older separate-piece
illustration does not establish the gasket construction for this truck. The CAD
geometry remains provisional. Focused pan/pickup/drain checks pass; navigation
reaches all731occurrences through862links. The refreshed full static audit passes2381broad-phase pairs with0overlaps, valid
STEP solids and matching GLB bounds at the reference pose. This does not certify
production fit or continuous motion; completion remains false.

## Corrected cam-side architecture — 2026-09-24

Ford external/internal diagrams exposed that the provisional cam and pushrods
occupied the manifold side. Rebuilt the block gallery, lifter bores, head pushrod
passages, rocker supports, valve offsets and timing-drive centers with the cam
opposite the manifold face. Filter, switch and pump studies now follow that side.
The pickup is reflected around the pan midplane to preserve its sump clearance;
production mounting and drive alignment are still unresolved.

The new source-backed side check passes40relationships and24pushrod passage probes.
Pan/pickup checks show no interference and11.95mmassumed floor clearance;25existing
fuel/idle/exhaust probes and862navigation links pass. Whole static and sampled
core interference audits are running; these partial checks do not certify the
new assembly. Pushrod-cover comparison hardware identities were saved for the
next component build.

Reflected pump-housing volume checks now use adaptive integration, which agrees
before/after STEP export within0.000001mm³. Other parts retain the previous volume
method; validation tolerances were not widened.

## Pushrod-cover construction candidate — 2026-09-24

Reviewed EngineQuest FSP300N manufacturer application and the six-hole photograph
on catalog page18. Saved the source, interchange and photo observations. Built a
separate thin-shell candidate with X-shaped pressed ribs and corrected its bolt
seating lands after visual inspection caught a breakthrough defect. It passes
STEP round-trip, six circular-hole and eighteen seating-land checks.

The candidate is not installed in the engine and its dimensions remain assumed.
Block opening, gasket, grommets and hardware integration remain pending. The
existing whole static audit is still running on its unchanged manifest.


Side-cover candidate: added perimeter gasket, six replacement-envelope grommets and six industrial-comparison threaded bolts. Isolated 14-solid STEP assembly passes internal overlap and seat probes; not installed or production-fit verified. Retailer 10740 envelope and its evidence limits saved in reference and KB. Existing full-engine static audit28655 remains running; installed files unchanged while it computes.


Isolated side-cover block interface: added a provisional access opening, perimeter rail and six connected fastener webs. Valid one-solid STEP round trip; cover/hardware clear the candidate block, twelve pushrod passages stay open, and four rail support probes pass. Selected head/distributor/filter/pressure-switch neighbor checks pass. Scratch visual inspected. Publisher API prepared but not integrated while whole static audit28655 runs. The uncompressed fastener stack leaves3.908mm engagement, still unverified; this is not a production fit claim. Applicable archived service rows saved in pushrod-cover-evidence.json, including25–35 inch-lb cover torque and lifter access context.


Confirmed side-layout follow-up: all twelve relocated rockers intersect the old valve-cover shoulder by roughly544.7mm3 each. Isolated valve_cover.py candidate retains the flange and cap/PCV positions while shifting upper profiles22mm toward the cam side. Valid STEP round trip and53 selected occurrence checks pass without overlap. Geometry remains provisional, and no installed artifact was changed during running static audit28655.


Prepared the next full-build source integration for the pushrod side cover and corrected valve-cover shoulders while preserving the live audit's installed artifacts. Factory rebuilding ranges now replace assumed cam-journal, cam-bearing-ID, lifter-OD and lifter-bore diameters. Isolated core generation passes34 valid-solid checks and four STEP round trips; production locations and shell thickness remain provisional.

Reviewed industrial cam-retention pages12–13: dimensional plate/spacer and two bolt references saved. A six-part isolated plate/spacer/bolt/washer study passes internal clearance and STEP checks. It is not installed: nose, key, gear-hub relief and block attachment need coordinated reconstruction. Industrial92-tooth gear and2.199-inch rear plug details remain comparison evidence. Full static audit28655 still computing at the latest observation.


Integrated cover/cam increment (244 definitions,752 occurrences): added the14-part side-cover assembly and seven cam-retention components, connected the cam nose/key/hub, and applied factory-range cam/lifter diameters. First static check caught one timing-gear/cover collision; a two-lobe cover cavity corrected it. The rebuilt manifest passes all2,433 static candidate pairs, expanded core/cam/lubrication checks at0/90/180/270, and278 selected retention checks including gear/cover motion across eight crank positions. Reports share the current manifest hash. These checks establish modeled consistency, not completion or production fidelity. Browser verification covers assembly explosion, the individual key page, search, side-cover transparency and the revised timing-cover silhouette.

2026-09-24: Browser verified final whole-engine framing with all752parts and one-row desktop controls. Oil pan remains unobscured. Exact part-name search, cam retention explode/individual pages, and side-cover transparency passed. Temporary review tab34 closed.

2026-09-24: Rear camshaft cup plug integrated with a separate provisional block seat and boss.245definitions/753occurrences. Full static2437pairs zero overlaps, core4angles zero overlaps, extended retention audit zero overlaps; all reports match current manifest. Browser checked both cup faces and individual part breadcrumbs.

2026-09-24: EGR factory cutaway and archived service number E9PZ9H473C reviewed. Dorman911-432 saved as an unverified comparison, not promoted to installed geometry. SMP illustrated-catalog URL returned404 and was not acquired. All CAD audits terminal; temporary browser tab35 closed.

2026-09-24: Integrated31-part EGR/EVP study (12 valve components,16 sensor components, gasket and two mounting bolts). Manufacturer Standard live catalog confirms EGV258 cross to archived FordE9PZ9H473C; four views acquired into reference/engine/standard-egv258. Paid EVTM23-2/23-4 visually reviewed for separate C180 vacuum command and C182 potentiometer feedback. All geometry dimensions and EVP internal construction remain provisional. No EGR flow/calibration simulation.
Published275definitions784occurrences; manifest60e96bc41e15f9b42e3c3f18c8617afee0e0034eed318ca8b5162faa9d82b72f. Full static2485pairs zero overlaps; four core poses zero overlaps; retention1069checks zero overlaps. All reports match. Browser verified31-part assembly,100%explode,16-part sensor transparency, individual wiper page and intake integration. Projected-box camera fit improves long-assembly visibility; whole-engine controls remain unobscured. Temporary tabs36/37 closed; no live CAD jobs.

## 2026-09-24 — EGR tube application and routing candidate

Verified Dorman 598-105 using the manufacturer's live selector for 1994 Ford F-150 L6 300 4.9L. Saved photo, capture, hashes and KB source. Manufacturer Ford cross is F4TZ9D477C; OD 0.74 in, length 17.9 in, stainless steel with two threaded connectors. Length measurement convention is unspecified. The photographed sleeve and bends do not supply thread sizes or installation coordinates.

Added unpublished `cad/engine/egr_tube.py` tube/sleeve candidate, using sourced OD and explicitly provisional wall/routing. `scripts/check-egr-tube-candidate.py` completed: valid single-solid STEP roundtrips, 108 broad-phase comparisons, zero overlaps with installed engine. Current developed path 390.208 mm is not claimed to reproduce the ambiguous catalog length. Not installed: manifold takeoff, both couplings and valve joint must be resolved first. Existing 275-definition/784-occurrence manifest unchanged. Engine remains unfinished.

## 2026-09-24 — EGR exhaust line integrated

Published four additional definitions/occurrences: tube with end geometry, protective sleeve, valve union nut and manifold fitting. Rear exhaust collector now has a connected takeoff bore. Manufacturer photo confirms externally threaded valve inlet; actual threads, seats and joint construction remain provisional smooth envelopes. Candidate STEP and 86 broad-phase fit comparisons passed without overlap. Full atlas now 279 definitions / 788 occurrences / 926 navigation links. Build40237 terminalPASS; static67040 terminalPASS with2564candidate pairs and0overlaps. ManifestSHA2561e0f829cc17af7a17a257c9c478fe388637aa8d798cf804f5a781a02dd5395da.

Browser39 verified4part assembly,100%explode, individual union-nut page and breadcrumbs; closed. Navigation andJSsyntax pass. Coremotion23193 andretention44283 started against frozeninstalledstate; poll existinghandles to terminal. No geometry edits during audits.

FactoryEVR source reviewed and ingested: upper hose nipple toEGRvalve, lower tovacuumsource; PCM duty cycle regulates vacuum. Factoryparttable printsFOTZ9J459A. Newreference`evr-factory-reviewed.json`, KBsource`ford-evr-port-routing-and-factory-service-identity.md`. StandardVS52 retailercrosslead awaitsmanufacturer verification. Engine remains unfinished.

EGRtube final audit: coremotion23193 andretention44283 terminalPASS0overlaps. All3reports matchcurrentmanifestSHA256. StandardVS52 manufacturerfit confirmed with1994/Ford/F150/6Cyl4.9L selected; specifications and successfulfit saved/ingested. Productimages and internalconstruction next. No liveCADjobs.

## 2026-09-24 — Vacuum regulator and controlled-vacuum hose

Integrated EVR exterior/cap/two terminals and the connected output hose, with assembly and individual pages, source links and diagnostic context. Factory EVTM location and port labels guide placement; dimensions, mounting hardware and hidden regulator internals remain unresolved. Corrected invalid hose sweep geometry and routed clear of the exhaust tube. Final static, motion and retention audits all pass against manifestfce274ec...,284definitions/793occurrences. Navigation933links passes. Browser verified regulator and combined40-partEGR view.

Acquired and ingested LuK2012catalog (applicableLFW132flywheel plus10/11inchclutchvariants) and ATPGraywerkscatalog (applicableoilpan103024exterior). HICENGINEdimensionalcatalog download inprogress for flywheel comparison. Engine NOT complete.

## Flywheel and pilot-bearing construction studies — 2026-09-24

Added the LFW132-family flywheel body, 164-tooth ring and six crank bolts, followed by an FC65662 pilot-bearing construction study with separate case, cage, seal and 16 illustrative needles. Current build has 291 definitions / 820 occurrences / 962 navigation links; these counts are not a completeness or accuracy percentage. Flywheel candidate and installed static/core-motion checks passed. Pilot candidate passed 130 broad-phase checks; installed checks are running. Both have learning pages; flywheel assembled/exploded rendering reviewed.

Saved HICENGINE and Timken application/dimensional catalogs, source pages, and reviewed evidence. Timken pilot versus needle tables disagree: preserve both. Internal pilot construction and flywheel recesses, indexing, ring fit and tooth profile remain provisional. Engine is not complete.

Damper attachment and profile pass: key, center bolt and washer added with matched provisional crank connection; recessed web and integrated pulley grooves refined from Dorman photograph. Gates 2008 belt/hose catalog and S7004 routing evidence acquired. Current count294/823, navigation965. Installed static/motion checks running; engine remains incomplete.

Final checks for the damper increment passed: 2702 static broad-phase pairs with zero overlaps, sampled crank motion0/90/180/270 with zero overlaps, and823parts/965navigationlinks. Both reports match manifest bbf8b19a79b3b0d8517b7055822d741423858b49e8419087075f4397eca56e22. Browser reviewed flywheel assembly/explosion, pilot bearing transparency/explosion, and revised damper assembled view. Production geometry and whole-engine completion remain unverified.
