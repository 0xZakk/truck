# Belt tensioner, pulley and internals

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#65](https://github.com/0xZakk/truck/issues/65).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `ab99fff2f63ad5dfc21fde8d12a32fc2a3d65832e6c8664baefd99d94403f7bf`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Tensioner pulley wheel** — `tensioner-pulley-wheel`; modeled quantity **1**; provisional.
  - Instances: `tensioner-pulley-wheel`
  - Source IDs: gates-38022, gates-1994-drive, ford-accessory-routing. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: 90 mm outside diameter, 37.5 mm width and 17 mm bearing bore are Gates replacement specifications; installed identity is unverified.
  - Open: Rim thickness 3 mm, web thickness 3 mm, bearing outer diameter 40 mm and bearing width 17 mm are illustrative assumptions.
  - Open: The bearing is an unresolved cartridge envelope, not a reconstruction of races, balls, cage or seals.
  - Open: Pulley center and belt plane are provisional. The axial center follows the illustrative damper groove center, not a measured production datum. A support study is modeled separately; the belt, engine bracket and operating motion remain unfinished.
- [ ] **Tensioner pulley bearing · unresolved cartridge** — `tensioner-pulley-bearing`; modeled quantity **1**; provisional.
  - Instances: `tensioner-pulley-bearing`
  - Source IDs: gates-38022, gates-1994-drive, ford-accessory-routing. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: 90 mm outside diameter, 37.5 mm width and 17 mm bearing bore are Gates replacement specifications; installed identity is unverified.
  - Open: Rim thickness 3 mm, web thickness 3 mm, bearing outer diameter 40 mm and bearing width 17 mm are illustrative assumptions.
  - Open: The bearing is an unresolved cartridge envelope, not a reconstruction of races, balls, cage or seals.
  - Open: Pulley center and belt plane are provisional. The axial center follows the illustrative damper groove center, not a measured production datum. A support study is modeled separately; the belt, engine bracket and operating motion remain unfinished.
- [ ] **Tensioner spring/pivot cartridge · unresolved interior** — `tensioner-spring-cartridge`; modeled quantity **1**; provisional.
  - Instances: `tensioner-spring-cartridge`
  - Source IDs: gates-1994-drive, gates-38131-instructions, ford-accessory-routing. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Gates 38131 instructions establish an enclosed preloaded spring, moving arm, mounting bolt, locating pin and optional locating-pin bushing. They do not establish internal spring geometry.
  - Open: The sealed spring/pivot cartridge is an unresolved envelope: spring, damping element, seals, stops and internal retainers are not separately reconstructed.
  - Open: 75 mm arm length, 64 mm cartridge diameter, axial stack, arm contour, fastener dimensions and pivot sleeve are illustrative construction assumptions, not measured Gates or Ford geometry.
  - Open: Pulley station (473.56,0,435), pivot station (433.56,-75,435) and arm angle are provisional; top-center placement follows labeled Ford routing while the axial datum matches the illustrative pump/damper belt plane. These are not measured installation coordinates. Engine mounting bracket, load path and operating travel remain unresolved.
  - Open: The removable bushing depicts the large-hole bracket option. Gates specifies 1/2 inch and 5/16 inch bracket holes, not the modeled pin/bushing clearances or installed bracket choice.
  - Open: Smooth fastener shanks omit threads, grades and tightening specifications. Collision-free geometry does not verify production fit or spring behavior.
- [ ] **Tensioner moving arm** — `tensioner-moving-arm`; modeled quantity **1**; provisional.
  - Instances: `tensioner-moving-arm`
  - Source IDs: gates-1994-drive, gates-38131-instructions, ford-accessory-routing. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Gates 38131 instructions establish an enclosed preloaded spring, moving arm, mounting bolt, locating pin and optional locating-pin bushing. They do not establish internal spring geometry.
  - Open: The sealed spring/pivot cartridge is an unresolved envelope: spring, damping element, seals, stops and internal retainers are not separately reconstructed.
  - Open: 75 mm arm length, 64 mm cartridge diameter, axial stack, arm contour, fastener dimensions and pivot sleeve are illustrative construction assumptions, not measured Gates or Ford geometry.
  - Open: Pulley station (473.56,0,435), pivot station (433.56,-75,435) and arm angle are provisional; top-center placement follows labeled Ford routing while the axial datum matches the illustrative pump/damper belt plane. These are not measured installation coordinates. Engine mounting bracket, load path and operating travel remain unresolved.
  - Open: The removable bushing depicts the large-hole bracket option. Gates specifies 1/2 inch and 5/16 inch bracket holes, not the modeled pin/bushing clearances or installed bracket choice.
  - Open: Smooth fastener shanks omit threads, grades and tightening specifications. Collision-free geometry does not verify production fit or spring behavior.
- [ ] **Tensioner pivot sleeve · illustrative** — `tensioner-pivot-sleeve`; modeled quantity **1**; provisional.
  - Instances: `tensioner-pivot-sleeve`
  - Source IDs: gates-1994-drive, gates-38131-instructions, ford-accessory-routing. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Gates 38131 instructions establish an enclosed preloaded spring, moving arm, mounting bolt, locating pin and optional locating-pin bushing. They do not establish internal spring geometry.
  - Open: The sealed spring/pivot cartridge is an unresolved envelope: spring, damping element, seals, stops and internal retainers are not separately reconstructed.
  - Open: 75 mm arm length, 64 mm cartridge diameter, axial stack, arm contour, fastener dimensions and pivot sleeve are illustrative construction assumptions, not measured Gates or Ford geometry.
  - Open: Pulley station (473.56,0,435), pivot station (433.56,-75,435) and arm angle are provisional; top-center placement follows labeled Ford routing while the axial datum matches the illustrative pump/damper belt plane. These are not measured installation coordinates. Engine mounting bracket, load path and operating travel remain unresolved.
  - Open: The removable bushing depicts the large-hole bracket option. Gates specifies 1/2 inch and 5/16 inch bracket holes, not the modeled pin/bushing clearances or installed bracket choice.
  - Open: Smooth fastener shanks omit threads, grades and tightening specifications. Collision-free geometry does not verify production fit or spring behavior.
- [ ] **Tensioner pulley retaining bolt · illustrative** — `tensioner-pulley-bolt`; modeled quantity **1**; provisional.
  - Instances: `tensioner-pulley-bolt`
  - Source IDs: gates-1994-drive, gates-38131-instructions, ford-accessory-routing. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Gates 38131 instructions establish an enclosed preloaded spring, moving arm, mounting bolt, locating pin and optional locating-pin bushing. They do not establish internal spring geometry.
  - Open: The sealed spring/pivot cartridge is an unresolved envelope: spring, damping element, seals, stops and internal retainers are not separately reconstructed.
  - Open: 75 mm arm length, 64 mm cartridge diameter, axial stack, arm contour, fastener dimensions and pivot sleeve are illustrative construction assumptions, not measured Gates or Ford geometry.
  - Open: Pulley station (473.56,0,435), pivot station (433.56,-75,435) and arm angle are provisional; top-center placement follows labeled Ford routing while the axial datum matches the illustrative pump/damper belt plane. These are not measured installation coordinates. Engine mounting bracket, load path and operating travel remain unresolved.
  - Open: The removable bushing depicts the large-hole bracket option. Gates specifies 1/2 inch and 5/16 inch bracket holes, not the modeled pin/bushing clearances or installed bracket choice.
  - Open: Smooth fastener shanks omit threads, grades and tightening specifications. Collision-free geometry does not verify production fit or spring behavior.
- [ ] **Tensioner locating-pin bushing · optional** — `tensioner-locating-bushing`; modeled quantity **1**; provisional.
  - Instances: `tensioner-locating-bushing`
  - Source IDs: gates-1994-drive, gates-38131-instructions, ford-accessory-routing. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Gates 38131 instructions establish an enclosed preloaded spring, moving arm, mounting bolt, locating pin and optional locating-pin bushing. They do not establish internal spring geometry.
  - Open: The sealed spring/pivot cartridge is an unresolved envelope: spring, damping element, seals, stops and internal retainers are not separately reconstructed.
  - Open: 75 mm arm length, 64 mm cartridge diameter, axial stack, arm contour, fastener dimensions and pivot sleeve are illustrative construction assumptions, not measured Gates or Ford geometry.
  - Open: Pulley station (473.56,0,435), pivot station (433.56,-75,435) and arm angle are provisional; top-center placement follows labeled Ford routing while the axial datum matches the illustrative pump/damper belt plane. These are not measured installation coordinates. Engine mounting bracket, load path and operating travel remain unresolved.
  - Open: The removable bushing depicts the large-hole bracket option. Gates specifies 1/2 inch and 5/16 inch bracket holes, not the modeled pin/bushing clearances or installed bracket choice.
  - Open: Smooth fastener shanks omit threads, grades and tightening specifications. Collision-free geometry does not verify production fit or spring behavior.
- [ ] **Tensioner central mounting bolt · illustrative** — `tensioner-mounting-bolt`; modeled quantity **1**; provisional.
  - Instances: `tensioner-mounting-bolt`
  - Source IDs: gates-1994-drive, gates-38131-instructions, ford-accessory-routing, ford-tsb-94-10-19-accessory. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Gates 38131 instructions establish an enclosed preloaded spring, moving arm, mounting bolt, locating pin and optional locating-pin bushing. They do not establish internal spring geometry.
  - Open: The sealed spring/pivot cartridge is an unresolved envelope: spring, damping element, seals, stops and internal retainers are not separately reconstructed.
  - Open: 75 mm arm length, 64 mm cartridge diameter, axial stack, arm contour, fastener dimensions and pivot sleeve are illustrative construction assumptions, not measured Gates or Ford geometry.
  - Open: Pulley station (473.56,0,435), pivot station (433.56,-75,435) and arm angle are provisional; top-center placement follows labeled Ford routing while the axial datum matches the illustrative pump/damper belt plane. These are not measured installation coordinates. Engine mounting bracket, load path and operating travel remain unresolved.
  - Open: The removable bushing depicts the large-hole bracket option. Gates specifies 1/2 inch and 5/16 inch bracket holes, not the modeled pin/bushing clearances or installed bracket choice.
  - Open: Smooth fastener shanks omit threads, grades and tightening specifications. Collision-free geometry does not verify production fit or spring behavior.
  - Open: Ford Fig4 establishes a shared P/S–A/C–tensioner carrier, front-head bolt#1, side-head bolt#2 and two side-block nuts#3. It does not dimension any modeled hole, web, casting, stud or fastening fit.
  - Open: PS and A/C stations stay unchanged. The tensioner wheel is provisionally at(473.56,167,350) with its75mm assumed arm below the pivot; source drawings establish relative arrangement only.
  - Open: Smooth shafts and nut bores represent stud engagement without production thread pitches, grades, preload or load analysis.
  - Open: Adapters add dry external side bosses. Passage proximity, casting wall thickness and original old front block boss cleanup require independent source work.
  - Open: The original separate tensioner engine support must not be installed. This candidate replaces the PS/AC carrier and its two provisional front-axis attachment bolts.
  - Open: Catalog belt fit and moving tensioner travel remain unresolved. This architecture correction does not match centers to a target belt length.

## Separate candidate parts (not installed)

- [ ] **Tensioner engine bracket** — `tensioner-engine-bracket`; Candidate mounting study; production identity and belt datums unresolved. Source: `cad/engine/tensioner_engine_support.py`.
- [ ] **Tensioner bracket block bolt** — `tensioner-bracket-block-bolt`; Candidate mounting study; production identity and belt datums unresolved. Source: `cad/engine/tensioner_engine_support.py`.
- [ ] **Tensioner bracket head bolt** — `tensioner-bracket-head-bolt`; Candidate mounting study; production identity and belt datums unresolved. Source: `cad/engine/tensioner_engine_support.py`.

## Additional known scope and reconciliation

- [ ] Tensioner spring/damper, pivot and bearing internals require decomposition
- [ ] Verify mount, travel and retention

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
