# Component contract and handoff: timing-waterpump-cover-datum-audit

## Contract

Issue32 timing integration, with water-pump issue47 as interface dependency. Worker pump_foot_resume; root sole integration owner. Baseline8c2d2d9a1400acf784e04581a61e6a6ede38d3ba, branch engine/timing-drive-fit. Scope is source/datum/ownership diagnosis only of the actual water-pump housing/gasket versus the staged timing cover. Do not carve neighboring solids, change source registration, alter frozen geometry or private/canonical manifests. The PS/AC bracket collision is outside this audit.

Owned files: this handoff, scripts/check-timing-waterpump-cover-datums.py, inventory/engine/timing-waterpump-cover-datum-audit.json, generated/timing-waterpump-cover-datum-audit/. Compare canonical and chronological frozen cover candidates using identical pump transforms; bind all inputs. Separate first collision onset from later modifications. Exact overlap>0.1mm³ is a failure, not an allowable production interference. Export diagnostic intersections and cross-sections; record source dimensional uncertainty. No repaired candidate authorized.

## Evidence and interfaces

Pump replacement sources establish four mounting holes, distinct fifth aperture, rear impeller and direct block mounting. They do not establish pumpY−32/Z170, chamber83mm depth or production casting envelope. Cover manufacturer/gasket images establish silhouette/holes/topology; metric scale and registration have unbounded projective/parallax uncertainty. See reference/engine/water-pump-mounting-topology-reviewed.json and timing-cover-registration-review.json. These two estimated registrations require a coordinated interface, not ownership transfer of colliding material.

Delivery pending measured chronology and actual sections. Unitsmm, unchanged world axes. Canonical and private staged manifests are read-only. No factory/pressure/strength claim.

## Frozen findings

**FAIL: independently estimated registrations are incompatible.** Actual pump definitions and complete world transforms are identical in canonical and private stage. Canonical cover has zero overlap with both pump parts. Source-shaped shell already introduces the defect; this is not a pan21,2692 or serialization error.

|Cover revision|Housing overlap mm³, adaptive|Pump gasket overlap mm³|
|---|---:|---:|
|Canonical|0|0|
|Earliest saved source shell|3062.986684|14.987075|
|Registered front joint|3709.283500|61.130672|
|Attachmentv2|3709.283500|61.130672|
|2692 seal cover|3709.283500|61.130672|
|Seven recessed main seats|2550.395221|61.130672|
|Pan21 relocation and serialized stage|2550.395221|61.130672|

Whole signed-delta intersections establish that all front-joint overlap is in added cover material relative to canonical. Attachmentv2,2692 andpan21 added/removed deltas have zero overlap with either pump part. Seven access pockets remove approximately1158.872263mm³ of the colliding housing region, and add no pump-intersecting stock. This removal reduces an inherited defect; it is not an accepted pump-clearance solution.

Two physically different conflicts require separate treatment:

- Rear pump flange/gasket versus source-shaped rear timing flange, X373.8..385.8416. The gasket witness has60.480473mm³ atY2.589..18.821/Z114.967..129.476 plus0.650199mm³ nearY−15.6/Z100. The housing has674.697840mm³ atY−5.123..20.830/Z109.721..130.439 and72.052143mm³ nearY−15.949..−12.8/Z95.593..105.390. These are actual solid ring/boss conflicts, not empty coolant space. A blind neighbor cut would remove sealing/bolt-support material and cannot establish joint ownership.
- Forward lateral inlet arm versus upper cover wall/boss, approximatelyX404.726..415/Y54.779..113/Z174.378..209.139. Intersecting the witness with the declared analytic inlet construction accounts for1803.645131mm³. The construction itself declares positive-Y orientation, localX−10/Z25, R24 neck and R20 bore to be estimates. The cover's extruded wall/frontX415 and bosses are also estimated.

The source photograph `reference/engine/atk-dff8-block-front.jpg` was re-viewed: it supports a distinct pump opening/bolt group beside the cam gear and a common machined block face. It does not provide an orthographic dimension or authorize overlap between two physical parts. The Gates/Fel-Pro source ledgers identify pump/gasket topology; their coordinates are estimates. The Dorman/Fel-Pro cover registration explicitly records unbounded parallax between aperture and flange planes. The present comparison therefore establishes contradictory modeled datums, not that either OEM part was incorrectly designed.

## Proposed decision order — no repair performed

1. Establish a common front-face registration using the actual crank/cam axes, pump aperture and both mounting patterns in the same automotive block reference. Keep source uncertainty explicit; a new estimated candidate must preserve all named sealing and bolt interfaces together.
2. Resolve rear flange footprints before changing the forward inlet. Moving the entire pump affects its four screws, impeller, shaft, belt/fan and coolant interfaces; it is not a free clearance adjustment. Resizing or moving the cover likewise affects seven seats, gasket/land and gears. Neither choice is presently source-dimensioned.
3. Separately revise the inferred forward inlet trajectory or cover depth/wall contour only after an explicit analytical interface contract. Preserve an open passage with real walls and source-supported lateral-neck topology. Do not subtract the actual cover/pump from its neighbor.

## Delivery, checks and limitations

- Report: `inventory/engine/timing-waterpump-cover-datum-audit.json`, SHA256 `01b016d9180ea72ec4096d97f42e48407cfb8c62601836ca3d6f8e45987b7190`.
- Private stage hash bound: `c09eca9a670b9d6241f04b8e082929cdf864e5c8498bed9b65bc0211d530f342`.
- Localized bodies: `inventory/engine/timing-waterpump-cover-localization.json`.
- Actual CAD sections: `cad/engine/generated/timing-waterpump-cover-datum-audit/sections-review.png`; image hash and data binding in `inventory/engine/timing-waterpump-cover-render.json`. Sections atX374/376 reveal rear gasket/flange overlap; X390 shows tapered chamber clearance; X414 shows inlet-arm conflict. Actual curves were reviewed.
- Exact intersection STEP witnesses and section data reside in the same generated folder. Original source photographs are not copied or redistributed.

```sh
.venv-cad/bin/python scripts/check-timing-waterpump-cover-datums.py
.venv-cad/bin/python scripts/localize-timing-waterpump-cover-datums.py
MPLCONFIGDIR=/tmp/truck-gear-mpl python3 scripts/render-timing-waterpump-cover-datums.py
python3 -m py_compile scripts/check-timing-waterpump-cover-datums.py scripts/localize-timing-waterpump-cover-datums.py scripts/render-timing-waterpump-cover-datums.py
```

Environment macOS/Python3.13.12/build123d0.10.0. Temporary Matplotlib cache is disposable. Readiness: completed diagnostic candidate, no repaired geometry. Application/source review PASS within dimensional uncertainty; coordinates/input hashes PASS; CAD diagnostic export/visual review PASS; actual fit FAIL; motion/strength/flow NOT RUN; new learning N/A research-only; browser NOT RUN; root review pending. All immutable input hashes rechecked after completion. No running processes, canonical edits or stage changes. Issue32/47 interfaces remain open. Next action is root's coordinated datum decision, not automatic cutting. Usage/model billing unavailable.
