# Isolated airbox body-bracket screw specimen

## Contract before CAD

Issue #80, engine air induction. Worker inclined_linkage_resume; integration owner root. Baseline `4f1fe9da2ec177e1ff61668df66ca422e37b0b7c`. Research-sized candidate, no shared files, installed occurrences or host changes. Owned `cad/engine/airbox_screw_online_20261002.py`, same hyphenated prefix scripts/reports/docs and generated folder. No manifest input. Existing airbox-host research remains frozen.

Manufacturer-authored Auveco catalog printed102/PDF2 (product13019, cross-reference N610959-S2) was inspected as pixels before modeling. It shows an external hex with circular washer head, coarse external helical thread and pointed end; no separate washer joint, slot, drilled point or captive clip is established. Exact1994 service figure190226466 calls for four N610959-S2 body screws; these are different from two N611062-S2 isolated box mounting screws. Source locators and original hashes are in `reference/engine/airbox-host-online-20261002.json`.

Supported replacement dimensions: nominal major diameter6.3mm, pitch1.81mm, under-head length19mm, washer-head OD11.5mm and hex across flats8mm. Under-head length convention is adopted for the catalog nominal screw length; no dimensioned OEM drawing is claimed. Estimated independently: root diameter4.5mm, flange thickness0.7mm, hex height3.4mm, head-top bevel0.3mm, point length4mm terminating at radius0.08mm, crest flat0.16mm and profile axial halfwidth0.65mm. Those are explicit free parameters, not measurements or ACT-derived geometry. Photo supports topology only, not these estimates. Thread is right-handed as a declared conventional estimate; no manufacturer handedness specification was found. Point retains the helical ridge clipped by a taper, rather than an unthreaded decorative cone.

Frame: mm, bearing planeZ0, +Z toward tipZ19, hex extends−Z. Stable proposed definition `air-cleaner-body-bracket-screw`; one isolated artifact, four eventual body occurrences unspecified. No parent/world transform or hole placement. Head underside and shank are future host contact interfaces; receiving pilot/clip, sheet stack, engagement, load and tool access unknown. No installation claim.

Construction reuses isolated pan-thread helper `solid`/`cz` and its one-turn loft pattern, with independent parameters. Export uses established STEP roundtrip and CAD-mm/Z-up to GLB-meter/Y-up convention. Checks: valid connected solid, positive/watertight/winding-consistent mesh, absolute bounds agreement<0.05mm; actual helical crest/root material alternation, pitch repeat and removed volume against a smooth blank; identical predicate must reject smooth blank. Tip and head sections checked independently. Actual exported render compares source-observed hex/flange/thread/point topology; originals excluded. Manufacturing gauge, mating host, installation, motion, browser: NOT RUN.

## Delivery

Pending build and review; report and separate handoff will bind final source/assets. Contract parameters remain estimates even if geometric checks pass. No model is placed to fit another estimated component.
