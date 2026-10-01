# Component contract and handoff: 2692 front-seal datums

## Contract before geometry

Issue #32; root integration owner. Research started from the prior assigned baseline `4e480f8e40458384986b9e1792597e87e56daad7`; current root checkpoint is `70542fad9de467a5c03ad54a6f54def8550956eb`, branch `engine/timing-interface-integration`. Canonical manifest remains91950c89. Own only this new handoff, `scripts/research-front-seal-2692-datums.py` and its new report. No seal construction or cover/hub changes before root selects the cross-part contract. All earlier timing candidates and source studies remain frozen.

Scope: replacement2692 component architecture and quantitative cross-part datum alternatives. Millimeters, crank axis+X forward, Y=Z=0. Preserve rotating crank/hub/key/bolt/washer/belt planes; seal is stationary in cover. Read actual source cross-section, do not derive measured thicknesses from its drawing.

## Source review

The earlier factual ledger `reference/engine/front-crank-seal-envelope-review.json` remains authoritative: exact-year OEM E6DZ6700A cross-references National2692; catalog dimensions are shaft47.625, housing65.0494, free case65.151, overall width13.4112 and flange80.264 mm. These are replacement comparisons, not identification of the owner's installed seal.

The National manufacturer-authored2013 catalog PDF page244/printed230 was rendered and visually inspected, including the complete page and type76 detail. It shows a stepped/flanged metal case returning toward an elastomer element and a circular spring section. It is representative, undimensioned topology. Separate case, elastomer and garter-spring occurrences are supported; their wall/lip/spring dimensions and joint details are unknown. Restricted/source artwork will not be included in a candidate release.

[Timken2692](https://cad.timken.com/item/seals/oil-seals-inch/2692) was reread2026-10-01: table matches these dimensions, polyacrylate material and clockwise-spiral lip description. The page explicitly says internal features/lip position are representative. No vendor CAD or sales drawing was downloaded; original candidate geometry must be independently authored from the permitted factual envelope and identified assumptions. Clockwise description alone does not establish a modeled helix handedness without viewing-direction and operating-rotation conventions.

## Existing model observations

- Current front seal is a54/42×8 mm annulus atX410–418. It does not embody2692 internals or dimensions.
- Frozen cover seal boss isR38 atX406–418, withR27 bore from410 forward andR24 rear passage. The cover main forward plane isX415. These are estimated source-code features.
- Current hub startsX419, outer sealing-regionR27 and boreR21.05. Its overall axial envelope71.12 mm and assembly position454.56 derive from the prior replacement envelope/estimated placement. The27 mm sealing radius and21.05 mm bore are assumptions. Seal shaft47.625 describes the contacted exterior, not the crank nose or hub bore.
- Reducing only the candidate track toR23.8125 leaves nominal modeled hub wall2.7625 mm over the existingR21.05 bore. This is geometric material continuity only; no press-fit/strength/actual bore claim.
- Current key cut startsX444.95. Keep the key, crank nose, washer, bolt and belt rim fixed. A prospective rear track ending beforeX435.5 stays away from that pocket.

## Axial alternatives for root selection

1. Overall seal air faceX415, rear401.5888: matches the old cover plane but has no overlap with the hub beginning419. Reject as an installed contact hypothesis.
2. Overall air faceX420.7056, rear407.2944: preserves the old seal center414 but has only1.7056 mm potential axial hub overlap. It would require assigning the unknown lip into a narrow forward portion merely to make contact. Keep as an unselected sensitivity case.
3. **Proposed robust-envelope hypothesis:** overall rearX420, air faceX433.4112. The complete source-width interval is inside the current hub's axial envelope, with1 mm rear-edge margin. This avoids inventing a specific lip plane just to obtain contact, at the cost of a local extended cover boss. The1 mm margin and absolute axial position are estimates; there is no factory-placement claim.

This is a proposal, not a source-proven installation. Keep cover/gasket perimeter and damper transform fixed rather than translating the whole cover or damper. The supported contact radius requires a local hub track change regardless of the selected axial position.

## Proposed cross-part masks and component contract

- Cover allowed region: X406–434.4112, radial24–43 mm about the crank axis, only near the old seal boss. Preserve all other shell, main gasket, pan terminal, bolt sockets and fluid boundaries. Exact added/removed material outside mask must be below1e-5 mm³. Gear front boundX392.509375 leaves13.490625 mm axial separation from mask; all seven existingR9 mounting lands have at least11.121426 mm radial separation fromR43. These are current-model bounds, not manufacturing clearances.
- Prospective cover rear shoulderX420 and housing radius32.5247. Flange air face433.4112; flange thickness remains an explicit estimated parameter, provisionally0.8 mm for a future study, giving seating plane432.6112. The source overall13.4112 mm includes all modeled material; do not add flange thickness outside that envelope.
- Proposed hub machining mask: onlyX419–435.5 and radial23.8125–27 mm, retaining bore, keyway, crank joint and all forward damper webs/pulley geometry. Establish a cylindrical47.625 mm contact track covering the entire seal envelope plus a bounded forward transition; no overall hub/assembly shift. Exact changes outside mask must be zero. Thickness2.7625 mm is an unresolved structural/application limit.
- Three independently identifiable physical candidate definitions: stationary metal case, bonded illustrative polyacrylate element, separate representative garter spring. Any flange0.8 mm/case-wall/lip-position/spring-wire values must be declared estimates before building and must fit the source envelope. Case and elastomer cannot be arbitrary disconnected rings: require positive bond/support interface and continuous seal path; spring must seat in the elastomer groove.
- Distinguish free caseOD65.151 from installed housing65.0494. The0.1016 mm nominal diametral difference is catalog geometry, not a tolerance specification. If an installed compressed case representation is made, retain separate free geometry and label the idealized fitted state; do not treat intentional press-fit interference as accidental collision or silently reduce source OD.
- Installed lip touches the47.625 rotating track with an explicitly modeled idealized contact band. Free lip interference, oil-side orientation, axial lip station, spring preload, swirl geometry and pressure capability remain unknown. Keep representative internals from being labeled exact2692 anatomy.

## Required checks after approval

Before any geometry: root must select axial registration and masks. Then use new isolated modules/artifacts and bind actual input hashes. Check source envelope, single-solid intended components, STEP/mesh bounds, continuous case seat/support annulus, flange face support, bond/spring contacts, lip-track contact across crank endplay if sourced (otherwise endplay NOT RUN), preserved protected differences and actual candidate/neighbor intersections. Negative controls must detect a shifted lip off the track and opened housing/flange support. Inspect actual assembly/cross-section beside the permitted source observations without redistributing the source image.

Application/dimensions PASS only for replacement evidence; physical construction, installation, motion, source-shape match, learning integration and browser NOT RUN. Source-index/learning candidates prepared by root stay separate. Issue remains open; no candidate installation or Done claim. Usage unavailable.

## Root-selected candidate contract

Root selected the fixed-damper/rearX420 hypothesis before construction. Installed case OD is explicitly65.0494 mm to represent nominal bore contact; retain a separate free-case shape at65.151 mm and the0.1016 nominal diametral press allowance. No unknown manufacturing tolerances are inferred.

Representative internals declared before modeling: metal wall0.8 mm, inner return carrierR27.6–28.4, flange0.8 mm; bonded polyacrylate elementX426.2–429.4, ideal lip bandX427.9–428.2 atR23.8125; garter groove/coil envelope centeredX426.6 at majorR25.6, winding radius0.45, wire radius0.12 and96 illustrative turns. These are independent educational estimates, not traced or downloaded Timken internal geometry. Clockwise micro-spiral lip texture is not modeled because scale/profile/viewing convention are unknown; retain that omission explicitly.

Dorman635-109 manufacturer photos003/007 were inspected from the existing local source collection. They support a raised circular seal boss qualitatively; they do not validate this candidate's approximately18 mm forward extension or its straight cylindrical contour. Preserve that visible discrepancy/uncertainty during review rather than labeling it a matched factory boss.

Own new `cad/engine/front_seal_2692_candidate.py`, dedicated checker/report/render, and `generated/front-seal-2692-candidate/`. Check actual neighbors: attachment-v2 cover baseline, combined future block, future block land, new access-pan and its gasket, crank gear and damper hardware. Cover-mount worker is informed of non-overlapping radial scope and retains all seven mounting lands. Root serializes eventual cover composition.

## Candidate construction and delivery notes

Stable integration IDs reserved by root: `front-seal-case` → `seal-case-installed.step`, `front-seal-elastomer` → `seal-elastomer.step`, `front-seal-garter-spring` → `seal-garter-spring.step`. The separate free-case artifact is a comparison state, not a fourth installed occurrence. Existing canonical `front-seal` stays untouched. All candidate exports are in world millimeters about +X; the hub must be transformed back through its preserved assembly frame before a later local-definition installation. Root owns the old-ID/deep-link migration and learning activation.

The initial long smooth spring sweeps were invalid and rejected; diagnostics are preserved in `inventory/engine/front-seal-2692-spring-construction-diagnostics.json`. The selected closed spring uses 48 circular sections per winding, ruled side surfaces and 96 repeated windings, sewn as one solid. This retains the declared nominal radii/count but approximates curvature between stations. It is not an exact smooth toroidal helix or a source-proven end-joint construction. Every winding has a positive-material seating witness; no preload/force is inferred from nominal contact.

Actual section inspection shows a flange supported on the forward cover face, a returned case carrier, bonded rubber reaching the machined hub track, and a garter groove on the oil side. These are independently authored illustrative internals. Type76 is a qualitative architecture comparison only (PDF244/printed230); the OEM cross-reference page is separately PDF309/printed295. The long straight extended boss remains visibly different from the photographed formed contour. Absolute X420 registration and boss depth/contour still require acceptance as estimates.

Reproduction, from repository root (baseline artifacts must first be restored):

```sh
.venv-cad/bin/python scripts/research-front-seal-2692-datums.py
.venv-cad/bin/python scripts/check-front-seal-2692-candidate.py
.venv-cad/bin/python scripts/check-front-seal-2692-contact-bands.py
PYTHONPATH=.venv-cad/lib/python3.13/site-packages MPLCONFIGDIR=/tmp/truck-mpl XDG_CACHE_HOME=/tmp/truck-cache python3 scripts/render-front-seal-2692-candidate.py
```

Temporary paths here are disposable cache directories; no temporary file is an input. CAD environment is the repository Python3.13/build123d environment; plotting uses the host Python's matplotlib with the CAD site-packages explicitly included. No packages or dependency pins were changed. Render/validation reports bind relevant inputs and artifacts. Candidate API: `cover_adapter(old)`, `hub_adapter(old_world)`, `case(free=False)`, `elastomer()`, `spring()`; helper masks return world solids. The source application/envelope is inherited from the frozen ledger; internal values are estimates and tolerances/preload/endplay are unknown.

Code is a separate uninstalled candidate under #32. Submission/PR/archive publication and final combined review belong to root. Browser interaction, explosion/reset, disassembly, crank endplay, manufacturing/strength, fluid pressure behavior and clockwise micro-spiral texture are NOT RUN. No issue completion or production claim follows from candidate checks. Model/effort and usage accounting are unavailable. Canonical inventory, IDs, assembly transforms, cover fasteners and belt planes were not edited.

## Scoped validation result

The candidate main report passes 45 outside-neighbor pairs: 12 exact intersections and 33 continuous axis-bound separations, zero overlap. This is the declared nominal static assembly, not an endplay/disassembly sweep. Four intended contact pairs have zero volumetric overlap and gap at numerical zero. Complete flange and rear-shoulder probes have zero missing material; separate full annular bond/lip probes and 96 winding-specific groove witness pairs also pass. All six internal non-contact pairs pass; the closest is cover/hub at0.1875 mm. The spring's continuous conservative envelope is used only for its three non-contact neighbors, not as a substitute for the actual groove contact checks.

Cover adds54,639.4397 mm³; the hub removes8,395.6548 mm³. Both added and removed outside-mask differences are zero. The free case intentionally intersects nominal housing by131.0244 mm³, preserving the nominal0.1016 mm press allowance in the record. All six STEP states are valid single solids after export; maximum roundtrip volume error0.000021872 mm³. The five installed-state GLBs are watertight; a separate actual-GLB exploded render checks winding consistency and positive signed volume. Spring mesh uses0.01 mm linear/0.5 rad angular meshing settings; case/rubber/cover/hub use0.035 mm/0.10 rad. These affect display tessellation only, not the STEP winding construction or contact thresholds.

Additional commands in dependency order after the main export:

```sh
.venv-cad/bin/python scripts/check-front-seal-2692-internal-clearance.py
PYTHONPATH=.venv-cad/lib/python3.13/site-packages MPLCONFIGDIR=/tmp/truck-mpl XDG_CACHE_HOME=/tmp/truck-cache python3 scripts/render-front-seal-2692-exploded.py
.venv-cad/bin/python scripts/check-front-seal-2692-delivery.py
```

| Gate | Result and scope |
|---|---|
| Application/coverage | PASS inherited exact-application cross-reference and replacement envelope; installed-owner seal identity unknown. |
| Dimensions/coordinates | PASS declared envelope, world axes, nominal fitted/free distinction and protected change masks; X420 and internals remain estimates. |
| CAD/export | PASS six STEP states, five GLBs, input/artifact bindings and native mesh checks. |
| Source/visual comparison | REVIEWED representative type76 architecture and source boss photos; exact internal contour and extended boss shape remain unsupported estimates. |
| Installed interfaces | PASS bounded uninstalled candidate; final expanded-seat block/pan composition remains root-owned follow-up. |
| Motion/disassembly | Nominal axisymmetric contact permits arbitrary crank rotation; endplay, tolerance, preload, installation/service route NOT RUN. |
| Learning/diagnostics | Root owns separate three-part learning candidate; failure controls for off-track lip, missing flange support, shifted rubber and displaced spring pass. |
| Browser integration | NOT RUN; prior security rejection and no candidate installation. |
| Reproduction/review | Report bindings and commands supplied; root archive/publication and clean-clone replay remain pending. |

Root reviewed the actual section before requesting the additional exploded view. The current branch moved to `engine/timing-pan-seal-joints` at baseline `a66b33c` after PR101 merged; this does not replace the recorded research baseline. This scoped handoff does not certify the still-changing expanded-seat block/pan pair. Root must check their final hashes/locality before composition. No scripts remain intentionally running after delivery. Generated artifacts are excluded from normal Git by existing policy and need the next authorized candidate release archive.
