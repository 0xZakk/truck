# Upper/lower intake manifolds, gaskets and locating hardware

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#36](https://github.com/0xZakk/truck/issues/36).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `bfab1f2596991d27fe5e52e90f02d070eb034f9de8c2cd72d3dd44666d6c8bb9`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Upper-to-lower intake gasket** — `efi-upper-intake-gasket`; modeled quantity **1**; provisional.
  - Instances: `efi-upper-intake-gasket`
  - Source IDs: fsm-212bf152ff88, fsm-9e1b0b719d0e, efi-intake-drawing. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Upper/lower split and seven retaining studs are supported by the truck manual. Runner curves, plenum volume, port profiles, wall thickness and installed stations remain provisional.
  - Open: Fuel rail, injectors and throttle controls are provisional studies. EGR, vacuum fittings, heat shield, support bracket and head-mounting hardware remain to be reconstructed. No airflow simulation is claimed.
- [ ] **Upper intake retaining stud** — `efi-upper-stud`; modeled quantity **7**; provisional.
  - Instances: `efi-upper-stud-1`, `efi-upper-stud-2`, `efi-upper-stud-3`, `efi-upper-stud-4`, `efi-upper-stud-5`, `efi-upper-stud-6`, `efi-upper-stud-7`
  - Source IDs: fsm-212bf152ff88, fsm-9e1b0b719d0e, efi-intake-drawing. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Upper/lower split and seven retaining studs are supported by the truck manual. Runner curves, plenum volume, port profiles, wall thickness and installed stations remain provisional.
  - Open: Fuel rail, injectors and throttle controls are provisional studies. EGR, vacuum fittings, heat shield, support bracket and head-mounting hardware remain to be reconstructed. No airflow simulation is claimed.
- [ ] **Upper EFI intake manifold** — `efi-upper-intake`; modeled quantity **1**; provisional.
  - Instances: `efi-upper-intake`
  - Source IDs: fsm-212bf152ff88, fsm-9e1b0b719d0e, efi-intake-drawing, system-750bd1047639, system-73d3dd2d32e7. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Upper/lower split and seven retaining studs are supported by the truck manual. Runner curves, plenum volume, port profiles, wall thickness and installed stations remain provisional.
  - Open: Fuel rail, injectors and throttle controls are provisional studies. EGR, vacuum fittings, heat shield, support bracket and head-mounting hardware remain to be reconstructed. No airflow simulation is claimed.
  - Open: Ford establishes an intake-manifold vacuum connection to the regulator spring chamber. It does not dimension the hose or identify this modeled dedicated fitting.
  - Open: Hose routing, 12 mm outside diameter, 8.2 mm main bore, 8.3 mm straight regulator socket, fitting dimensions and plenum port station are provisional; production routing may use a shared vacuum harness.
  - Open: The fitting uses an unthreaded seat with clearance; thread sealing, hose compression, clamps and actual installed variant remain unresolved. No pressure response is simulated.
- [ ] **Intake manifold locating dowel** — `intake-head-locating-dowel`; modeled quantity **1**; provisional.
  - Instances: `intake-head-locating-dowel`
  - Source IDs: ford-intake-manifold-dowel, ford-1996-manifold-fastener-table. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Ford1994 specifies one locating dowel through the intake gasket into the lower intake. The1996 factory comparison table gives5/16 inch diameter by1 inch length; identity and dimensions on the1994 truck remain unverified.
  - Open: The7.9375 by25.4 mm comparison pin replaces the earlier arbitrary6 by23.5 mm candidate. WorldX0/Z298 and axial centerY-132.7 are dry-interface assumptions, not measured Ford datums.
  - Open: Head and intake sockets use0.05 mm radial clearance for geometric checking. They do not establish the real press/sliding fits or retention.
  - Open: The dowel locates the joint but does not clamp it. The front lifting-eye stud/bolt study is separate; fourteen other manifold attachment stations and shared clamping details remain unresolved.
- [ ] **Lower EFI intake manifold** — `efi-lower-intake`; modeled quantity **1**; provisional.
  - Instances: `efi-lower-intake`
  - Source IDs: fsm-212bf152ff88, fsm-9e1b0b719d0e, efi-intake-drawing, ford-manifold-fastener-topology, ford-1996-manifold-comparison, ford-1996-manifold-fastener-table, ford-intake-manifold-dowel. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Upper/lower split and seven retaining studs are supported by the truck manual. Runner curves, plenum volume, port profiles, wall thickness and installed stations remain provisional.
  - Open: Fuel rail, injectors and throttle controls are provisional studies. EGR, vacuum fittings, heat shield, support bracket and head-mounting hardware remain to be reconstructed. No airflow simulation is claimed.
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
  - Open: Ford1994 explicitly installs rear bolts15/16 before the intake; these two fasteners do not complete the remaining shared manifold clamps.
  - Open: Nominal3/8-16 diameter and1.31in underhead length are1996 comparison dimensions, not established1994 installed identity.
  - Open: All mounting stations, casting webs, head bosses, clearance holes, socket depths and hex-head dimensions are provisional adaptations to the existing reconstruction.
  - Open: Smooth envelopes do not model female threads, preload, thermal expansion or retention. Added head bosses are not verified against production coolant jackets.
- [ ] **Intake-to-head gasket** — `efi-head-intake-gasket`; modeled quantity **1**; provisional.
  - Instances: `efi-head-intake-gasket`
  - Source IDs: fsm-212bf152ff88, fsm-9e1b0b719d0e, efi-intake-drawing, fsm-4069bc7976d8, ford-manifold-fastener-topology, ford-1996-manifold-comparison, ford-1996-manifold-fastener-table, ford-intake-manifold-dowel. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Upper/lower split and seven retaining studs are supported by the truck manual. Runner curves, plenum volume, port profiles, wall thickness and installed stations remain provisional.
  - Open: Fuel rail, injectors and throttle controls are provisional studies. EGR, vacuum fittings, heat shield, support bracket and head-mounting hardware remain to be reconstructed. No airflow simulation is claimed.
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
  - Open: Ford1994 explicitly installs rear bolts15/16 before the intake; these two fasteners do not complete the remaining shared manifold clamps.
  - Open: Nominal3/8-16 diameter and1.31in underhead length are1996 comparison dimensions, not established1994 installed identity.
  - Open: All mounting stations, casting webs, head bosses, clearance holes, socket depths and hex-head dimensions are provisional adaptations to the existing reconstruction.
  - Open: Smooth envelopes do not model female threads, preload, thermal expansion or retention. Added head bosses are not verified against production coolant jackets.

## Additional known scope and reconciliation

- [ ] Verify all upper/lower manifold fasteners and support brackets
- [ ] Verify casting contours, runner geometry, bosses and gasket seats

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
