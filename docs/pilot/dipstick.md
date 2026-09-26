---
title: "The engine oil dipstick indicates sump oil level relative to a seated reference"
status: "Specimen-informed candidate; installed fit and calibration unaccepted"
---

## Result

One engine-oil dipstick study is delivered as parametric CAD, STEP and GLB. It includes a yellow open-loop handle, seating stop, narrow metal blade with waves near the handle, widened reading end and the specimen's legible engineering stamp. It is distinct from the existing power-steering cap/dipstick. No tube, oil pump or additional lubrication component is included.

The [seller's photographed specimen](https://www.tbscshop.com/90s-ford-f150-f250-truck-4-9l-300-inline-6-oil-dip-stick-dipstick-e9te-6750-da/) is marked E9TE-6750-DA and described as a 1990s 4.9L F-series oil indicator with an approximately 27.25-inch metal blade. This is firsthand specimen evidence, not a Ford engineering drawing. A [1994 service-parts catalog](https://www.fordpartsgiant.com/oem-1994-ford-f_150-dipstick.html) lists E9TZ-6750-E and replacement F4TZ-6750-D for 4.9L among several engines; its broad compatibility and package-style dimensions do not establish the specimen's exact installed identity. Exact VIN-specific service/engineering-number equivalence remains unresolved.

## Dimensions and markings

692.15 mm is the conversion of the seller's approximate 27.25-inch blade measurement. The photograph does not precisely establish its seating-stop datum; it is used as an axial study length, not a calibrated insertion length. All section dimensions, loop proportions, stop geometry, wave amplitude, tip transition and stamp position/depth are estimates. The near-stop waves are represented in the broad blade plane; the actual formed/twisted three-dimensional section requires measurement.

The engineering stamp is legible in the close-up. The oil-level lettering and boundary marks are not sufficiently legible to reconstruct. No ADD, FULL, NORMAL range or quart increment has been invented. The stamp is a specimen comparison, not proof that this owner's truck carries that marking. Oil volume cannot be calculated from this blade or from the provisional sump geometry.

## Placement and interface review

Both owner's engine-bay side views were inspected. They show the engine, intake and several service handles, but do not securely isolate this engine-oil handle, its stop, or its tube entry. No pixels were treated as a measured coordinate datum. The model's reference pose is therefore explicitly **unaccepted**.

The trial stop is at CAD (-120,170,445) mm, rotated -8.5 degrees about X. The tip reaches (-120,67.694,-239.547) mm, in the rear-sump envelope. Against the accepted baseline, the trial blade intersects the block by 163.67 mm³. This indicates an unresolved routing/passage interface, not permission to drill a hole or hide interference. The other five checked neighboring solids do not intersect in this pose; minimum pan-surface distance is 7.10 mm. Neither result establishes physical installation. Block entry, guide-tube bore/centerline, tube-end seating contact, bottom clearance in the real pan and crankshaft clearance remain unverified.

The guide tube is an interface requirement only, with no authored tube solid. Blade withdrawal is flexible and follows the tube; rigid upward translation would not validate removal. No motion path is claimed or installed. Whole-engine moving clearance and browser integration remain the integration owner's work after a measured route exists.

## Learning and inspection

The seated stop provides a repeatable reference between the tube and the blade. Oil wets the blade near its reading end; the relationship of that wet line to the original markings is useful only with the correct indicator, tube, seating condition and engine configuration. An unseated stop, bent blade or mismatched indicator/tube can alter the reading. A missing or illegible mark cannot be replaced using this model's proportions.

Inspect the handle/blade attachment, bends, seating stop and marking readability when readings are inconsistent. This study supplies no calibration, refill quantity or repair dimensions. Use the truck's verified service information and the original matched parts for those decisions.

## Integration API

Import `cad/engine/pilot/dipstick/dipstick.py` by path. `Parameters` exposes the dimensions; `parts(p)` returns blade and handle/stop solids; `shape(p)` returns their compound as one service component; `installed(shape)` applies only the rejected trial pose. Local origin is the assumed stop plane, +Z toward handle, blade along -Z. STEP uses millimetres; GLB uses metres and maps CAD (x,y,z) to (x,z,-y).

For an individual component page use `engine-oil-dipstick` as the service component ID, `learning.json` for content and `evidence.json` for provenance. Keep it in candidate/withdrawn presentation. Do not add the trial pose as an accepted assembly occurrence. Reproduce with `XDG_CACHE_HOME=/private/tmp/truck-cache .venv-cad/bin/python scripts/pilot/dipstick/build_check.py`; render with system Python and `scripts/pilot/dipstick/render.py` (Matplotlib).

Outputs and complete deterministic logs are under the owned pilot directories. Validation hashes bind the source images, CAD module, accepted baseline and exports. `cad-review.png` was visually inspected for handle opening, blade continuity, reading-end widening, and the relationship of the rejected pose to the engine. The embossed/recessed stamp is small and requires a close view. A two-solid compound represents bonded handle and blade materials, not two separately serviced parts.
