# Cylinder head, gasket and bolts

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#25](https://github.com/0xZakk/truck/issues/25).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `73de806af847c528e766151590d7b8235620893414c280711aa6ff382ca8a7e1`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Cylinder head bolt** — `head-bolt`; modeled quantity **14**; provisional.
  - Instances: `head-bolt-1-1`, `head-bolt-1-2`, `head-bolt-2-1`, `head-bolt-2-2`, `head-bolt-3-1`, `head-bolt-3-2`, `head-bolt-4-1`, `head-bolt-4-2`, `head-bolt-5-1`, `head-bolt-5-2`, `head-bolt-6-1`, `head-bolt-6-2`, `head-bolt-7-1`, `head-bolt-7-2`
  - Source IDs: fsm-1b7a4041a45d. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact production contours, dimensions and tolerances need applicable drawings or measurements.
- [ ] **Head gasket** — `head-gasket`; modeled quantity **1**; provisional.
  - Instances: `head-gasket`
  - Source IDs: melling-camshaft-specifications, melling-stock-valve-specifications, melling-pushrod-specifications. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact production contours, dimensions and tolerances need applicable drawings or measurements.
  - Open: Coordinated motion is a teaching construction. The smooth lobe law fits selected Melling SYB-38 scalars; the installed cam, full lift law, advertised checking height and production timing remain unverified.
  - Open: Rigid linkage and constant-wire spring deformation explain motion; hydraulic lash adjustment, spring dynamics, lubrication, fatigue and running-engine performance are not simulated.
  - Open: Rear cam journal and bearing move from assumedX-330to-334mm to clear the complete cylinder6 intake follower. Journal width23mm, bearing width22mm and axial coordinates remain unverified; source radial dimensions are preserved.
  - Open: The existing continuous cam bore supports the revised bearing location; actual bearing retention, oil-feed indexing and axial production layout remain unresolved.
  - Open: The head gasket pushrod openings retain their old clearance and gain a6mm-radius cut at the revisedY90axis. Hole contours and sealing lands remain provisional; positive passage checks do not establish a production gasket.
- [ ] **Cylinder head** — `cylinder-head`; modeled quantity **1**; provisional.
  - Instances: `cylinder-head`
  - Source IDs: fsm-1b7a4041a45d, allied-12952-head-photos, fsm-be886ffa4807, fsm-2f144bda5e08, system-f1571449160a, system-2ea2c28d7cca, ford-accessory-brackets, ford-accessory-routing, ford-cii-pump-study, ford-alternator-study, ford-manifold-fastener-topology, ford-1996-manifold-comparison, ford-1996-manifold-fastener-table, ford-intake-manifold-dowel, dorman-674185-profile-specification, dorman-674185-head-facing-photo, dorman-674185-opposite-photo, dorman-674185-application, dorman-674186-profile-specification, dorman-674186-head-facing-photo, dorman-674186-opposite-photo, dorman-674186-overview-photo, dorman-674186-catalog-application, ford-tsb-94-10-19-accessory, melling-camshaft-specifications, melling-stock-valve-specifications, melling-pushrod-specifications, dorman-902-1002, motorad-244-192, water-pump-mounting-topology, ford-cooling-connections, ford-ect-construction, ford-cooling-sensor-circuits, gates-1994-drive, truck-cooling-hose-photos. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Photograph-informed chamber outline and plug wells remain provisional. Plug datums are shared with the installed study for geometric coherence, not verified production fit. Chamber volume/profile, port routing, coolant passages, casting identity and valve stations remain unverified.
  - Open: Firing sequence and clockwise distributor sweep follow Ford references. Tower 1 at local +X is an explicit model phase; surveyed cap clocking and absolute ignition timing are unverified.
  - Open: Ford describes a carbon-impregnated multifilament synthetic-fiber core and heat-resistant rubber insulation. The 7 mm jacket, 2 mm aggregate core and all boot/contact dimensions are illustrative; individual fibers and electrical resistance are not simulated.
  - Open: Lead lengths, bends, terminal clip construction, seal compression and support arrangement are provisional. These routes are not an installation guide.
  - Open: Coil bracket geometry, two head mounting bosses and fasteners are a fit study. Four coil screws follow existing provisional core holes, not a verified factory screw count.
  - Open: Electrical paths and firing order are represented; ignition voltage, dielectric breakdown, spark timing, flexing and thermal behavior are not simulated.
  - Open: Ford identifies a shared power-steering/A/C bracket attached to block and head and a separate alternator bracket. These castings reconstruct that load-path topology, not a measured production casting.
  - Open: All boss coordinates, bolt counts, web sections, material colors, hole sizes and mounting-face locations are illustrative interfaces to the current component studies. Casting ribs, part numbers, dowels and factory contours remain unknown.
  - Open: Engine feet touch provisional front-face seats. Explicit interface adapters add isolated blind support bosses and 16 mm deep smooth thread-envelope bores; 14 mm bolt engagement is illustrative, not a verified thread specification. These are dry blind attachments, not coolant or oil passages.
  - Open: Accessory bolt shanks use clearance through the candidate mounting ears. Threads, grades, preload, bracket stiffness and belt-load deflection are not simulated.
  - Open: The Thermactor and tensioner engine brackets remain separate unresolved load paths. No unsupported air-pump attachment is added to these castings.
  - Open: Ford 1994 identifies front stud13 and bolt14 before intake installation; the recovered 1996 factory figure shows a two-foot spanning eye.
  - Open: All station coordinates, lug sections, eye outline, socket depths and clearances are provisional adaptations to current castings, not production dimensions.
  - Open: Stud total axial length90.678 mm and bolt underhead length33.274 mm compare the 1996 labels3/8-16x3.57 and3/8-16x1.31; 1994 identity is not established.
  - Open: Smooth nominal thread envelopes do not simulate thread engagement, preload, lifting strength or fatigue. The projecting stud end has no invented downstream retaining nut.
  - Open: Remaining fourteen manifold fastener stations and shared clamping details are not completed by this subset.
  - Open: The provisional bolt axes are above the intake gasket strip. The casting webs lie outside its sealing plane instead of cutting the gasket into disconnected pieces.
  - Open: Bolt14 and its eye foot use assumed X49 mm, revised from X45 after the whole-engine audit found1.7265 mm3 overlap with injector3 connector. This clearance-driven adaptation is not a recovered Ford station.
  - Open: The simplified head needs explicit8 mm radius internal mounting bosses ending at worldY-109 to surround the provisional blind sockets. These assumed bosses are not traced production castings or verified against recovered coolant-gallery geometry.
  - Open: Ford1994 specifies one locating dowel through the intake gasket into the lower intake. The1996 factory comparison table gives5/16 inch diameter by1 inch length; identity and dimensions on the1994 truck remain unverified.
  - Open: The7.9375 by25.4 mm comparison pin replaces the earlier arbitrary6 by23.5 mm candidate. WorldX0/Z298 and axial centerY-132.7 are dry-interface assumptions, not measured Ford datums.
  - Open: Head and intake sockets use0.05 mm radial clearance for geometric checking. They do not establish the real press/sliding fits or retention.
  - Open: The dowel locates the joint but does not clamp it. The front lifting-eye stud/bolt study is separate; fourteen other manifold attachment stations and shared clamping details remain unresolved.
  - Open: Dorman674-185 manufacturer photos/specifications establish rectangular entries and a blended collector for its1994F1504.9L front application, not the installed truck casting identity.
  - Open: Entry28x28mm with3mm corners, outer pad36x36mm with6mm corners, runner radii15/18mm and collector radii18/24mm are dimensional study assumptions.
  - Open: The three port stations, rectangular-to-round transitions, collector centerline and outlet station retain provisional engine datums. Wall thickness, thermal stress, flow and casting manufacturability are unverified.
  - Open: Existing provisional lifting-eye lugs are retained. Other manifold clamping stations, production flange outline and downstream pipe joint remain incomplete.
  - Open: Rear manifold and intake port shape are not inferred from the front replacement photograph.
  - Open: Manufacturer674-186 photos and catalog application support three rounded-rectangular rear entries, not their dimensions or installed casting identity.
  - Open: Entry28x28mm, corner3mm, outer36x36mm and transition stations reuse provisional front study dimensions; no pixel scaling is used.
  - Open: This incremental entry correction retains the old collector and EGR end connection. Both remain unsupported form/routing studies pending joint reconstruction; this is not a completed rear manifold.
  - Open: The provisional EGR fitting insertion envelope is shortened from19mm to12.5mm so its tip ends0.5mm before the collector inner wall rather than intruding into the collector and rear runner. This is a geometric clearance assumption, not a verified thread engagement or retention specification.
  - Open: Production flange lands, head attachment, outlet flange, auxiliary ports, wall thickness and thermal/flow performance remain unverified.
  - Open: Ford1994 explicitly installs rear bolts15/16 before the intake; these two fasteners do not complete the remaining shared manifold clamps.
  - Open: Nominal3/8-16 diameter and1.31in underhead length are1996 comparison dimensions, not established1994 installed identity.
  - Open: All mounting stations, casting webs, head bosses, clearance holes, socket depths and hex-head dimensions are provisional adaptations to the existing reconstruction.
  - Open: Smooth envelopes do not model female threads, preload, thermal expansion or retention. Added head bosses are not verified against production coolant jackets.
  - Open: Ford Fig4 establishes a shared P/S–A/C–tensioner carrier, front-head bolt#1, side-head bolt#2 and two side-block nuts#3. It does not dimension any modeled hole, web, casting, stud or fastening fit.
  - Open: PS and A/C stations stay unchanged. The tensioner wheel is provisionally at(473.56,167,350) with its75mm assumed arm below the pivot; source drawings establish relative arrangement only.
  - Open: Smooth shafts and nut bores represent stud engagement without production thread pitches, grades, preload or load analysis.
  - Open: Adapters add dry external side bosses. Passage proximity, casting wall thickness and original old front block boss cleanup require independent source work.
  - Open: The original separate tensioner engine support must not be installed. This candidate replaces the PS/AC carrier and its two provisional front-axis attachment bolts.
  - Open: Catalog belt fit and moving tensioner travel remain unresolved. This architecture correction does not match centers to a target belt length.
  - Open: Coordinated motion is a teaching construction. The smooth lobe law fits selected Melling SYB-38 scalars; the installed cam, full lift law, advertised checking height and production timing remain unverified.
  - Open: Rigid linkage and constant-wire spring deformation explain motion; hydraulic lash adjustment, spring dynamics, lubrication, fatigue and running-engine performance are not simulated.
  - Open: Automotive front-face photograph establishes the head-front outlet, two diagonal fasteners and adjacent smaller opening, not calibrated positions or dimensions.
  - Open: Dorman902-1002 establishes two .313-inch holes, 1.5-inch catalog outside diameter and separate gasket/main/secondary apertures; neck contours and measurement station remain uncertain.
  - Open: All modeled hole coordinates, gasket contour, neck curvature, bolt engagement and receiver depths are assumptions. Only thermostat flange53.85mmOD/1.27mmthickness are manufacturer dimensions.
  - Open: The head adapter creates bounded local blind coolant receiver pockets with modeled wall material. It does not reconstruct or validate the complete head water jacket.
  - Open: The current longblock front plane X373 and outlet center Y0/Z295 are provisional reference datums. Placement corrects the floating joint without optimizing a belt length.
  - Open: The illustrative thermostat piston front is shortened0.01mm to seat exactly against the existing bridge; this corrects an inherited interference, not a sourced actuator dimension.
  - Open: The adjacent heater-supply passage remains separate from the thermostat-controlled radiator chamber. Its thread and deeper head-jacket connectivity remain unverified.
  - Open: The heater-supply/ECT elbow follows the relocated secondary outlet while retaining the existing engine-side vehicle endpoint(488,-57,335). New bend control points, collar, shoulder and sensor station are provisional; the boss is located1mm farther forward than the rejected trial to clear the outlet casting.
  - Open: Source-sized replacement envelopes are not installed-part identification. Absolute cam/deck/station datums, lifter socket/internal offsets and rocker geometry remain assumptions.
  - Open: Guide bore and separate spring load-test heights are service-reference constraints; spring wire/turns, keeper/groove construction and casting contours remain illustrative.

## Additional known scope and reconciliation

- [ ] Valve guides and seats: establish integral versus replaceable construction
- [ ] Verify ports, water jacket, oil feeds and plug seats
- [ ] Verify head bolt variants and gasket passages

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
