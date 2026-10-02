# Paired intake duct contour refinement — issue 80

## Contract before CAD

Baseline `54c2abf7aae73a8a5818321ee48ad81c8b7346ad`; parent engine #1, paired intake ducts #80. Worker inclined_linkage_resume; root integrates. Own only `airbox-refined-20261002*` records/scripts/generated folder and `cad/engine/airbox_refined_20261002.py`. No frozen sources, manifests or previous candidate assets change. Candidate only: improved local physical shape, not installed placement, measured replacement geometry or completion.

Read inputs: frozen `online-airbox-research.json`, `online-airbox-duct-specimen.md`, prior geometry/checker/delivery, and actual public specimen photographs 4, 6 and 12. Image URL/hash identity is inherited from the research ledger; originals stay out of Git and artifacts. The two later views show the opposite side/oblique projection and confirm that the prior triangular corrugations and box-shaped connecting web omit visible contours.

| Observation | Source view | Proposed geometry and evidence boundary |
|---|---|---|
| Bellows have rounded crests/valleys; throats taper mildly rather than a steep cone | Photos 4, 6, 12 | Smooth lofted periodic profile with rounded axial transitions. Pitch, depth and valley radii remain inferred; no material compliance law. |
| Large cuffs bulge behind the mouth; bellows begin after smooth cuffs | Photos 6, 12 | Preserve explicit straight insertion intervals; smoothly bulged exterior behind them. Source does not establish unloaded insertion diameter. |
| Smooth legs bend gradually through shoulders into straighter small ends | Photos 4, 6, 12 | Smooth centerline interpolation between declared local control values. No claim of exact 3D free-state path or installed reach. |
| Bridge outline blends outward into both tubes and has rounded corners | Photos 4, 6, 12 | Rounded/waisted web clipped only to actual external tube surfaces. Molded region, not proven separate service part. |
| Retainer has a broad open U-shaped channel and flared lips | Photo 6, reverse face in 12 | Curved channel and rounded lips on an external saddle. Retained item's identity and hidden features unknown. |
| Cuff images appear oval in oblique views | Photos 6, 12 | Cannot separate projection from physical ovality. Retain circular insertion sections as explicit estimates rather than inventing a measured elliptical ratio. |

Numeric parameters are fixed before clearance: projected X spans559/533mm and wall3mm inherited as estimates; old straight cuff intervals/frames retained so four clamp assemblies can be reused. Their untouched exact artifacts are verified by hashes. Cuff outer radii42.5/28.5mm are not source dimensions. The new bellows valley radius varies approximately35→32mm,7mm rise,12mm pitch. Smooth paths and shoulder/clip/web contour dimensions are inferred and serialized by the module. These values cannot be adjusted to fit old airbox/throttle geometry. Local X large-to-small cuff, Y branch separation, Z up; no world/parent transform.

Named regions preserved: two separate lumen-bearing tubes, joining web, retainer, four bands/housings and four screws. Web/retainer manufacturing separation remains unknown. Preserve open independent passages, exterior contacts and original cuff/clamp frames. No body support is modeled. Existing engine/airbox/throttle neighbors are not checked because this has no supported installed frame.

## Acceptance planned

- STEP validity, one intended solid per region, watertight/winding-consistent positive-volume GLBs, <=0.05mm CAD/mesh bounds error.
- Fresh tube passage/wall checks at crests, valleys, transitions and curved shoulders; deliberate blocked passage and thin-wall controls. Section sampling does not certify continuous material deformation.
- Fresh local overlap/contact checks with0.1mm³ numerical overlap threshold. Reuse unchanged clamp geometry evidence only under exact hashes; regenerate tube/web/retainer evidence.
- Actual exported mesh views compared with photographs4/6/12; report remaining contour discrepancies and distinguish shape estimates from measured dimensions. No AI concept render.
- No installed motion, sealing, preload, disassembly or browser claim. Root independently reviews before any preservation/integration decision.

## Delivery

Pending. Commands, hashes, actual checks and reviewed render follow in a separate final handoff. No source originals will be redistributed. Environment: existing pinned CAD Python3.13/build123d0.10; source-render inspection uses existing matplotlib/trimesh runtime. Model/usage information unavailable.
