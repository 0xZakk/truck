---
title: "The accelerator bracket anchors the cable housing beside the throttle body"
status: provisional-candidate
---

## Function and location

The accelerator cable has an outer housing and a moving inner cable. The bracket holds the outer housing relative to the engine, allowing inner-cable movement to pull the throttle linkage. A loose bracket can consume pedal movement before the throttle opens. This stationary part belongs to the throttle assembly; it should not rotate with the throttle shaft.

The factory 1994 4.9L service procedure places the accelerator bracket onto the throttle body before installing the body onto the upper intake studs. The candidate uses the accepted positive-Y stud pair at Y=74, Z=464/516 mm and the existing casting front face X=378.5 mm. The chosen stud pair and installed handedness remain assumptions; the procedure does not establish those dimensions or orientation.

## Geometry and evidence

A salvaged 4.9L bracket photograph shows a formed tapered web, a large central aperture, round and rectangular openings on one end, and a forked opposite mounting end. These features inform the candidate topology. The model replaces the stamped curves and rolled edges with planar sheet intersections; it is visibly more angular than the photograph. No ruler, orthographic views or verified engineering drawing supplies dimensions. The photo listing spans several years and does not establish a 1994 manual-transmission part number. There is no claim of fabrication accuracy.

The candidate is 2 mm thick, with an assumed 8.8 mm mounting opening, 11 mm round cable opening, and 11×12 mm rectangular cable opening. Overall bounds are X=378.5–465, Y=73–124, Z=456–524 mm. The retained source dimension count is zero. CAD datums inherited from the accepted assembly are not factory dimensions.

## Installation conflict

At the accepted baseline, both positive-Y nuts already bear against the casting at X=378.5 mm. Inserting the bracket without moving those nuts causes about 73.29 mm³ interference per nut. Shifting those two nut centers from X=381.5 to X=383.5 mm gives face contact without volumetric overlap. Body, gasket and stud axes remain unchanged. The 30 mm provisional studs end at X=386, while the shifted 6 mm nuts end at X=386.5; 5.5 mm of nominal overlap remains, but threads and adequate engagement have not been established. Integration must retain this unresolved fastener issue. No shared file or accepted baseline was modified.

## Inspection and troubleshooting

With the engine stopped, inspect the cable housing retainer, the bracket mounting points and the sheet around each opening. A moving outer housing, cracked mounting ear, missing retainer or a bent web can create lost pedal travel or misalignment. Check that the cable moves without snagging and the throttle returns fully when released; a bracket model alone cannot certify return action. The speed-control cable, linkage shield and return mechanism are separate components.

If the throttle does not reach its travel limit, inspect cable routing, housing seating and bracket movement before assuming the throttle body is defective. If it sticks open or fails to return, stop using the vehicle until the binding or return fault is corrected. The CAD's static openings are not an adjustment specification. Use the factory procedure for installation; this pilot does not establish cable adjustment or operating-stop calibration.

## Validation and integration

`cad/engine/pilot/throttle-bracket/candidate.py` exposes `shape(overrides=None)` and the existing five-function `build(api)` interface. Call it after the throttle assembly group exists. The candidate uses world CAD millimeters and zero occurrence transform. The exported GLB preserves millimeter coordinates; integration should regenerate it with the shared exporter if that exporter changes axes or units. Register the source IDs in `inventory/engine/pilot/throttle-bracket/learning.json` when integrating. Do not silently apply the suggested nut shift as a validated production change.

Run `.venv-cad/bin/python scripts/pilot/throttle-bracket/build_check.py` with `XDG_CACHE_HOME=/private/tmp/truck-cache`. It writes STEP, GLB, the validation report and an intermediate preview archive. Run `python scripts/pilot/throttle-bracket/render.py` with writable cache variables to render the actual tessellation. The report covers solid validity, mesh closure, bounds, exact CAD neighbor intersections, stud clearance, mounting contact, and sample butterfly poses. It is a local component study, not a whole-engine interference audit. Cable, shield and linkage sweep remain unavailable; browser integration acceptance belongs to the integration owner.

## Sources

- [1994 Ford 4.9L throttle body factory service procedure, hosted by Operation CHARM](https://charm.li/Ford/1994/F%20150%202WD%20Pickup%20L6-300%204.9L/Repair%20and%20Diagnosis/Powertrain%20Management/Fuel%20Delivery%20and%20Air%20Induction/Throttle%20Body/Service%20and%20Repair/): read through web retrieval on 2026-09-26. Supports assembly order, shared retention, and cable connections. Its linked factory diagram at `https://charm.li/images/DM05Q313/ford10/690090240/` was researched but could not be visually inspected: direct and browser access timed out. This is an explicit evidence gap.
- [Salvage photograph, Ford 1987–97 F-series/Bronco 4.9 bracket, listing 375325588661](https://www.ebay.com/itm/375325588661): physical-part photograph, visually inspected in the browser and saved as `reference/engine/pilot/throttle-bracket/salvage-photo.jpg`. Seller applicability is unverified. [Original image](https://i.ebayimg.com/images/g/YbQAAOSwAqBl~O8i/s-l1200.jpg).
