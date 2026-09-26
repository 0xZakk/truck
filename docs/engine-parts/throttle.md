# Throttle body, shaft, plates and mounting hardware

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#43](https://github.com/0xZakk/truck/issues/43).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `bfab1f2596991d27fe5e52e90f02d070eb034f9de8c2cd72d3dd44666d6c8bb9`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Twin-bore throttle housing** — `throttle-housing`; modeled quantity **1**; provisional.
  - Instances: `throttle-housing`
  - Source IDs: truck-throttle-operation, truck-throttle-service, truck-throttle-catalog. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory manual supports dual bores, a separate gasket and four mounting studs/nuts. Bore diameter, shaft/plate construction, casting contour and fastener dimensions are assumed.
  - Open: IAC/TPS studies and bypass passages are present; their exact variants and internal details remain unresolved. Purge ports, linkage, return spring, accelerator bracket and plate screws remain unmodeled. Idealized 0–90 degree motion is not the production stop calibration.
- [ ] **Throttle body gasket** — `throttle-gasket`; modeled quantity **1**; provisional.
  - Instances: `throttle-gasket`
  - Source IDs: truck-throttle-operation, truck-throttle-service, truck-throttle-catalog. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory manual supports dual bores, a separate gasket and four mounting studs/nuts. Bore diameter, shaft/plate construction, casting contour and fastener dimensions are assumed.
  - Open: IAC/TPS studies and bypass passages are present; their exact variants and internal details remain unresolved. Purge ports, linkage, return spring, accelerator bracket and plate screws remain unmodeled. Idealized 0–90 degree motion is not the production stop calibration.
- [ ] **Throttle butterfly plate** — `throttle-plate`; modeled quantity **2**; provisional.
  - Instances: `throttle-plate-1`, `throttle-plate-2`
  - Source IDs: truck-throttle-operation, truck-throttle-service, truck-throttle-catalog. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory manual supports dual bores, a separate gasket and four mounting studs/nuts. Bore diameter, shaft/plate construction, casting contour and fastener dimensions are assumed.
  - Open: IAC/TPS studies and bypass passages are present; their exact variants and internal details remain unresolved. Purge ports, linkage, return spring, accelerator bracket and plate screws remain unmodeled. Idealized 0–90 degree motion is not the production stop calibration.
- [ ] **Throttle mounting stud** — `throttle-mount-stud`; modeled quantity **2**; provisional.
  - Instances: `throttle-stud-1`, `throttle-stud-2`
  - Source IDs: truck-throttle-operation, truck-throttle-service, truck-throttle-catalog. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory manual supports dual bores, a separate gasket and four mounting studs/nuts. Bore diameter, shaft/plate construction, casting contour and fastener dimensions are assumed.
  - Open: IAC/TPS studies and bypass passages are present; their exact variants and internal details remain unresolved. Purge ports, linkage, return spring, accelerator bracket and plate screws remain unmodeled. Idealized 0–90 degree motion is not the production stop calibration.
- [ ] **Throttle retaining nut** — `throttle-mount-nut`; modeled quantity **4**; provisional.
  - Instances: `throttle-nut-1`, `throttle-nut-2`, `throttle-nut-3`, `throttle-nut-4`
  - Source IDs: truck-throttle-operation, truck-throttle-service, truck-throttle-catalog. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory manual supports dual bores, a separate gasket and four mounting studs/nuts. Bore diameter, shaft/plate construction, casting contour and fastener dimensions are assumed.
  - Open: IAC/TPS studies and bypass passages are present; their exact variants and internal details remain unresolved. Purge ports, linkage, return spring, accelerator bracket and plate screws remain unmodeled. Idealized 0–90 degree motion is not the production stop calibration.
- [ ] **Throttle cable ball stud · estimated** — `throttle-cable-ball-stud-estimated`; modeled quantity **1**; provisional.
  - Instances: `throttle-cable-ball-stud-estimated`
  - Source IDs: throttle-1994-linkage-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: All new dimensions, D-section shaft coupling and retention pin inferred; production retention unverified.
  - Open: Bracket web offset11 mm and ear extensions are a coordinated educational revision, not a Ford dimension.
  - Open: Spring, shield, cable/socket, plate screws and preset stops absent;0–90 degrees is inherited educational travel.
  - Open: Pin locking, load capacity, spring return, shield, actual cable/socket, plate hardware and production stops remain unresolved.
- [ ] **Throttle lever retaining pin · estimated** — `throttle-lever-retaining-pin-estimated`; modeled quantity **1**; provisional.
  - Instances: `throttle-lever-retaining-pin-estimated`
  - Source IDs: throttle-1994-linkage-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: All new dimensions, D-section shaft coupling and retention pin inferred; production retention unverified.
  - Open: Bracket web offset11 mm and ear extensions are a coordinated educational revision, not a Ford dimension.
  - Open: Spring, shield, cable/socket, plate screws and preset stops absent;0–90 degrees is inherited educational travel.
  - Open: Pin locking, load capacity, spring return, shield, actual cable/socket, plate hardware and production stops remain unresolved.
- [ ] **Throttle shaft · estimated keyed end** — `throttle-shaft`; modeled quantity **1**; provisional.
  - Instances: `throttle-shaft`
  - Source IDs: truck-throttle-operation, truck-throttle-service, truck-throttle-catalog, throttle-1994-linkage-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: The factory manual supports dual bores, a separate gasket and four mounting studs/nuts. Bore diameter, shaft/plate construction, casting contour and fastener dimensions are assumed.
  - Open: IAC/TPS studies and bypass passages are present; their exact variants and internal details remain unresolved. Purge ports, linkage, return spring, accelerator bracket and plate screws remain unmodeled. Idealized 0–90 degree motion is not the production stop calibration.
  - Open: All new dimensions, D-section shaft coupling and retention pin inferred; production retention unverified.
  - Open: Bracket web offset11 mm and ear extensions are a coordinated educational revision, not a Ford dimension.
  - Open: Spring, shield, cable/socket, plate screws and preset stops absent;0–90 degrees is inherited educational travel.
  - Open: Pin locking, load capacity, spring return, shield, actual cable/socket, plate hardware and production stops remain unresolved.
- [ ] **Throttle linkage splash shield · estimated** — `throttle-linkage-shield-estimated`; modeled quantity **1**; provisional.
  - Instances: `throttle-linkage-shield-estimated`
  - Source IDs: throttle-1994-linkage-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: All dimensions, mounting coordinate, barb and relief slots are inferred educational geometry; Ford production details unverified.
  - Open: Angular hood approximates factory viewY. Pushpin insertion flexure/material/strength and full cable sheath/connector envelopes are unvalidated.
  - Open: Spring and its tangs, stops and production calibration remain unresolved; not invented here.
- [ ] **Throttle shield pushpin · estimated** — `throttle-shield-pushpin-estimated`; modeled quantity **1**; provisional.
  - Instances: `throttle-shield-pushpin-estimated`
  - Source IDs: throttle-1994-linkage-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: All dimensions, mounting coordinate, barb and relief slots are inferred educational geometry; Ford production details unverified.
  - Open: Angular hood approximates factory viewY. Pushpin insertion flexure/material/strength and full cable sheath/connector envelopes are unvalidated.
  - Open: Spring and its tangs, stops and production calibration remain unresolved; not invented here.
- [ ] **Throttle lever · estimated** — `throttle-lever-estimated`; modeled quantity **1**; provisional.
  - Instances: `throttle-lever-estimated`
  - Source IDs: throttle-1994-linkage-study, throttle-return-spring-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: One illustrative torsion spring explains fixed/moving anchors; actual Ford spring count, tang construction, dimensions and stops remain unverified.
  - Open: Wire motion preserves geometric length; no preload, spring rate, stress, fatigue, friction or guaranteed return force is simulated.
  - Open: Cable-end compression spring is a separate factory-documented component and is not represented by this torsion spring.
  - Open: Bracket and lever anchor holes, wire diameter and retention hooks are inferred; attachment strength and installation flexure are unverified.
- [ ] **Throttle return spring · illustrative** — `throttle-return-spring-illustrative`; modeled quantity **1**; provisional.
  - Instances: `throttle-return-spring-illustrative`
  - Source IDs: throttle-return-spring-study. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: One illustrative torsion spring explains fixed/moving anchors; actual Ford spring count, tang construction, dimensions and stops remain unverified.
  - Open: Wire motion preserves geometric length; no preload, spring rate, stress, fatigue, friction or guaranteed return force is simulated.
  - Open: Cable-end compression spring is a separate factory-documented component and is not represented by this torsion spring.
  - Open: Bracket and lever anchor holes, wire diameter and retention hooks are inferred; attachment strength and installation flexure are unverified.

## Additional known scope and reconciliation

- [ ] Actual return spring count/construction, preload and stops; one illustrative deforming spring with captured anchors is installed, separate cable-end spring remains missing
- [ ] Plate retaining screws and shaft bushings/seals as applicable
- [ ] Actual throttle/speed-control cables and sockets, pin locking and production shield construction
- [ ] Verify production stops, shaft retention, dimensions and installed geometry; current lever/key/pin/shield are inferred teaching parts

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
