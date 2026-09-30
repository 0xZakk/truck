# Front/rear exhaust manifolds, mounting and outlet joints

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#46](https://github.com/0xZakk/truck/issues/46).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `ab99fff2f63ad5dfc21fde8d12a32fc2a3d65832e6c8664baefd99d94403f7bf`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Front Manifold Lifting Eye** — `front-manifold-lifting-eye`; modeled quantity **1**; provisional.
  - Instances: `front-manifold-lifting-eye`
  - Source IDs: ford-manifold-fastener-topology, ford-1996-manifold-comparison, ford-1996-manifold-fastener-table. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Ford 1994 identifies front stud13 and bolt14 before intake installation; the recovered 1996 factory figure shows a two-foot spanning eye.
  - Open: All station coordinates, lug sections, eye outline, socket depths and clearances are provisional adaptations to current castings, not production dimensions.
  - Open: Stud total axial length90.678 mm and bolt underhead length33.274 mm compare the 1996 labels3/8-16x3.57 and3/8-16x1.31; 1994 identity is not established.
  - Open: Smooth nominal thread envelopes do not simulate thread engagement, preload, lifting strength or fatigue. The projecting stud end has no invented downstream retaining nut.
  - Open: Remaining fourteen manifold fastener stations and shared clamping details are not completed by this subset.
  - Open: The provisional bolt axes are above the intake gasket strip. The casting webs lie outside its sealing plane instead of cutting the gasket into disconnected pieces.
  - Open: Bolt14 and its eye foot use assumed X49 mm, revised from X45 after the whole-engine audit found1.7265 mm3 overlap with injector3 connector. This clearance-driven adaptation is not a recovered Ford station.
  - Open: The simplified head needs explicit8 mm radius internal mounting bosses ending at worldY-109 to surround the provisional blind sockets. These assumed bosses are not traced production castings or verified against recovered coolant-gallery geometry.
- [ ] **Front Manifold Stud13** — `front-manifold-stud13`; modeled quantity **1**; provisional.
  - Instances: `front-manifold-stud13`
  - Source IDs: ford-manifold-fastener-topology, ford-1996-manifold-comparison, ford-1996-manifold-fastener-table. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Ford 1994 identifies front stud13 and bolt14 before intake installation; the recovered 1996 factory figure shows a two-foot spanning eye.
  - Open: All station coordinates, lug sections, eye outline, socket depths and clearances are provisional adaptations to current castings, not production dimensions.
  - Open: Stud total axial length90.678 mm and bolt underhead length33.274 mm compare the 1996 labels3/8-16x3.57 and3/8-16x1.31; 1994 identity is not established.
  - Open: Smooth nominal thread envelopes do not simulate thread engagement, preload, lifting strength or fatigue. The projecting stud end has no invented downstream retaining nut.
  - Open: Remaining fourteen manifold fastener stations and shared clamping details are not completed by this subset.
  - Open: The provisional bolt axes are above the intake gasket strip. The casting webs lie outside its sealing plane instead of cutting the gasket into disconnected pieces.
  - Open: Bolt14 and its eye foot use assumed X49 mm, revised from X45 after the whole-engine audit found1.7265 mm3 overlap with injector3 connector. This clearance-driven adaptation is not a recovered Ford station.
  - Open: The simplified head needs explicit8 mm radius internal mounting bosses ending at worldY-109 to surround the provisional blind sockets. These assumed bosses are not traced production castings or verified against recovered coolant-gallery geometry.
- [ ] **Front Manifold Bolt14** — `front-manifold-bolt14`; modeled quantity **1**; provisional.
  - Instances: `front-manifold-bolt14`
  - Source IDs: ford-manifold-fastener-topology, ford-1996-manifold-comparison, ford-1996-manifold-fastener-table. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Ford 1994 identifies front stud13 and bolt14 before intake installation; the recovered 1996 factory figure shows a two-foot spanning eye.
  - Open: All station coordinates, lug sections, eye outline, socket depths and clearances are provisional adaptations to current castings, not production dimensions.
  - Open: Stud total axial length90.678 mm and bolt underhead length33.274 mm compare the 1996 labels3/8-16x3.57 and3/8-16x1.31; 1994 identity is not established.
  - Open: Smooth nominal thread envelopes do not simulate thread engagement, preload, lifting strength or fatigue. The projecting stud end has no invented downstream retaining nut.
  - Open: Remaining fourteen manifold fastener stations and shared clamping details are not completed by this subset.
  - Open: The provisional bolt axes are above the intake gasket strip. The casting webs lie outside its sealing plane instead of cutting the gasket into disconnected pieces.
  - Open: Bolt14 and its eye foot use assumed X49 mm, revised from X45 after the whole-engine audit found1.7265 mm3 overlap with injector3 connector. This clearance-driven adaptation is not a recovered Ford station.
  - Open: The simplified head needs explicit8 mm radius internal mounting bosses ending at worldY-109 to surround the provisional blind sockets. These assumed bosses are not traced production castings or verified against recovered coolant-gallery geometry.
- [ ] **Rear Manifold Bolt15** — `rear-manifold-bolt15`; modeled quantity **1**; provisional.
  - Instances: `rear-manifold-bolt15`
  - Source IDs: ford-manifold-fastener-topology, ford-1996-manifold-comparison, ford-1996-manifold-fastener-table. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Ford1994 explicitly installs rear bolts15/16 before the intake; these two fasteners do not complete the remaining shared manifold clamps.
  - Open: Nominal3/8-16 diameter and1.31in underhead length are1996 comparison dimensions, not established1994 installed identity.
  - Open: All mounting stations, casting webs, head bosses, clearance holes, socket depths and hex-head dimensions are provisional adaptations to the existing reconstruction.
  - Open: Smooth envelopes do not model female threads, preload, thermal expansion or retention. Added head bosses are not verified against production coolant jackets.
- [ ] **Rear Manifold Bolt16** — `rear-manifold-bolt16`; modeled quantity **1**; provisional.
  - Instances: `rear-manifold-bolt16`
  - Source IDs: ford-manifold-fastener-topology, ford-1996-manifold-comparison, ford-1996-manifold-fastener-table. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Ford1994 explicitly installs rear bolts15/16 before the intake; these two fasteners do not complete the remaining shared manifold clamps.
  - Open: Nominal3/8-16 diameter and1.31in underhead length are1996 comparison dimensions, not established1994 installed identity.
  - Open: All mounting stations, casting webs, head bosses, clearance holes, socket depths and hex-head dimensions are provisional adaptations to the existing reconstruction.
  - Open: Smooth envelopes do not model female threads, preload, thermal expansion or retention. Added head bosses are not verified against production coolant jackets.
- [ ] **Front exhaust manifold** — `exhaust-front`; modeled quantity **1**; provisional.
  - Instances: `exhaust-front`
  - Source IDs: system-9d57ed6d21b9, system-b9d2a4ac71cc, ford-manifold-fastener-topology, ford-1996-manifold-comparison, ford-1996-manifold-fastener-table, dorman-674185-profile-specification, dorman-674185-head-facing-photo, dorman-674185-opposite-photo, dorman-674185-application, dorman-674186-opposite-photo, dorman-674186-catalog-application. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory procedure establishes separate front/rear castings and head attachment. Runner bends, common chamber, flange contours, outlet dimensions and installed stations remain provisional.
  - Open: EGR takeoff, air-injection connections, lifting eye, dowel, head fasteners and exhaust-pipe joints remain unresolved. No production gasket is inferred from the model.
  - Open: Ford 1994 identifies front stud13 and bolt14 before intake installation; the recovered 1996 factory figure shows a two-foot spanning eye.
  - Open: All station coordinates, lug sections, eye outline, socket depths and clearances are provisional adaptations to current castings, not production dimensions.
  - Open: Stud total axial length90.678 mm and bolt underhead length33.274 mm compare the 1996 labels3/8-16x3.57 and3/8-16x1.31; 1994 identity is not established.
  - Open: Smooth nominal thread envelopes do not simulate thread engagement, preload, lifting strength or fatigue. The projecting stud end has no invented downstream retaining nut.
  - Open: Remaining fourteen manifold fastener stations and shared clamping details are not completed by this subset.
  - Open: The provisional bolt axes are above the intake gasket strip. The casting webs lie outside its sealing plane instead of cutting the gasket into disconnected pieces.
  - Open: Bolt14 and its eye foot use assumed X49 mm, revised from X45 after the whole-engine audit found1.7265 mm3 overlap with injector3 connector. This clearance-driven adaptation is not a recovered Ford station.
  - Open: The simplified head needs explicit8 mm radius internal mounting bosses ending at worldY-109 to surround the provisional blind sockets. These assumed bosses are not traced production castings or verified against recovered coolant-gallery geometry.
  - Open: Dorman674-185 manufacturer photos/specifications establish rectangular entries and a blended collector for its1994F1504.9L front application, not the installed truck casting identity.
  - Open: Entry28x28mm with3mm corners, outer pad36x36mm with6mm corners, runner radii15/18mm and collector radii18/24mm are dimensional study assumptions.
  - Open: The three port stations, rectangular-to-round transitions, collector centerline and outlet station retain provisional engine datums. Wall thickness, thermal stress, flow and casting manufacturability are unverified.
  - Open: Existing provisional lifting-eye lugs are retained. Other manifold clamping stations, production flange outline and downstream pipe joint remain incomplete.
  - Open: Rear manifold and intake port shape are not inferred from the front replacement photograph.
  - Open: Manufacturer replacement photographs show an integral outlet flange with two opposed mounting holes on each manifold. Installed casting identity remains unknown.
  - Open: The40mm outlet opening,10mm flange thickness,32mm central outer radius,12mm ear radii and77.67mm diagonal hole spacing are explicit geometric assumptions, not measurements from the photos.
  - Open: Outlet axes and elevations retain the provisional model. Production sealing seat, mating pipe flange, fastener identity, thread engagement, gasket applicability and thermal performance remain unresolved.
- [ ] **Rear exhaust manifold · rounded collector study** — `exhaust-rear`; modeled quantity **1**; provisional.
  - Instances: `exhaust-rear`
  - Source IDs: system-9d57ed6d21b9, system-b9d2a4ac71cc, dorman-598-105, dorman-674186-profile-specification, dorman-674186-head-facing-photo, dorman-674186-opposite-photo, dorman-674186-overview-photo, dorman-674186-catalog-application, ford-manifold-fastener-topology, ford-1996-manifold-comparison, ford-1996-manifold-fastener-table, dorman-674185-opposite-photo, dorman-674185-application, rear-collector-rounded-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory procedure establishes separate front/rear castings and head attachment. Runner bends, common chamber, flange contours, outlet dimensions and installed stations remain provisional.
  - Open: EGR takeoff, air-injection connections, lifting eye, dowel, head fasteners and exhaust-pipe joints remain unresolved. No production gasket is inferred from the model.
  - Open: Manufacturer674-186 photos and catalog application support three rounded-rectangular rear entries, not their dimensions or installed casting identity.
  - Open: Entry28x28mm, corner3mm, outer36x36mm and transition stations reuse provisional front study dimensions; no pixel scaling is used.
  - Open: The provisional EGR fitting insertion envelope is shortened from19mm to12.5mm so its tip ends0.5mm before the collector inner wall rather than intruding into the collector and rear runner. This is a geometric clearance assumption, not a verified thread engagement or retention specification.
  - Open: Production flange lands, head attachment, outlet flange, auxiliary ports, wall thickness and thermal/flow performance remain unverified.
  - Open: Ford1994 explicitly installs rear bolts15/16 before the intake; these two fasteners do not complete the remaining shared manifold clamps.
  - Open: Nominal3/8-16 diameter and1.31in underhead length are1996 comparison dimensions, not established1994 installed identity.
  - Open: All mounting stations, casting webs, head bosses, clearance holes, socket depths and hex-head dimensions are provisional adaptations to the existing reconstruction.
  - Open: Smooth envelopes do not model female threads, preload, thermal expansion or retention. Added head bosses are not verified against production coolant jackets.
  - Open: Manufacturer replacement photographs show an integral outlet flange with two opposed mounting holes on each manifold. Installed casting identity remains unknown.
  - Open: The40mm outlet opening,10mm flange thickness,32mm central outer radius,12mm ear radii and77.67mm diagonal hole spacing are explicit geometric assumptions, not measurements from the photos.
  - Open: Outlet axes and elevations retain the provisional model. Production sealing seat, mating pipe flange, fastener identity, thread engagement, gasket applicability and thermal performance remain unresolved.
  - Open: Rounded collector and repaired runner exterior are a replacement-photo-informed dimensional study, not production geometry.
  - Open: Retained long outlet neck, thin head lands/bolt arms and end EGR connection still differ visibly from Dorman674-186; dimensions, casting identity, auxiliary ports, threads, sealing and thermal behavior remain unresolved.

## Additional known scope and reconciliation

- [ ] Reconcile every manifold attachment/clamp station and shared intake/exhaust hardware
- [ ] Outlet flanges/seals/springs/studs/nuts: candidate artifacts exist, reconcile installed publication
- [ ] Verify rear collector contour, auxiliary bosses and EGR takeoff location

## Cross-system boundaries

Coordinate with [#9](https://github.com/0xZakk/truck/issues/9). Keep the current engine-mounted component here; agree ownership before adding its vehicle-side continuation.

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
