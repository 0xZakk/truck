# Component contract and handoff: inclined linkage lower passage scope

## Contract

- Assigned engine issue #32; integration owner: root agent. Issue fetch attempted with `gh issue view 32 --json title,body,state` but GitHub was unreachable. Assignment and parent scope are inherited from the integration owner; current issue state is not freshly verified.
- Baseline `8547c589d3c086bad91baf879219612bcd9a162f`, focused branch `engine/timing-support-joints`; manifest SHA-256 `91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6`.
- Research-only scope: complete numeric Y90 upper-socket hypothesis and propose a bounded lower passage/deck transition. This document is a proposal requiring integration-owner scope selection before neighbor CAD edits; it does not authorize installation.
- Own `scripts/check-timing-valvetrain-inclined-scope.py`, `inventory/engine/timing-valvetrain-inclined-scope-validation.json`, this handoff, and delivery results in `timing-valvetrain-inclined-hypothesis.md`. Frozen vertical contract, adapter candidate, shared builders/inventory, existing block and canonical geometry remain unchanged.
- Model millimeters and world XYZ; retain all station X values, source-sized rods/valves, valve axes, compensated keyed-cam phase and all current fluid interfaces. All component transforms remain inherited until a separate isolated inclined adapter exists.
- Inputs verified locally: full assembly manifest, nine actual lifter STEP definitions, inclined numerical hypothesis and authoritative previous linkage source. Inputs are hashed in the new report. Block/head/gasket exact CAD examination for proposed changes remains a next-stage check.
- Check: `.venv-cad/bin/python scripts/check-timing-valvetrain-inclined-scope.py`. Rod clearance is a sufficient circular containment bound at integer crank0–720 and axial0/-0.1, all twelve branches. Affine centerline difference bounds the full Z interval using its endpoints. Actual lifter STEP Z bounds plus the analytic maximum cam lift bound lifter height across the profile. Negative controls shrink the proposed aperture toR3 and lower backing toZ150; both must fail their numeric bounds.

## Evidence ledger

| Feature | Value and datum | Evidence class | Source and limitation |
|---|---|---|---|
| Rod/valve lengths | Frozen comparison-sized geometry, unchanged | Replacement comparison | `valve_dimensions_candidate.py`; exact owner hardware identity remains unknown |
| Upper socket | Y90 nominal; common pivotY50.894736784, cup-localZ-1.385614069 | Inferred hypothesis | `timing_valvetrain_inclined_hypothesis.py`; not factory rocker geometry |
| Highest actual lifter component | WorldZ151.161656792 at maximum modeled cam lift | Derived model bound | Actual nine lifter STEP bounds and analytic profile maximum; does not validate assumed lift law |
| Proposed transition/backing | WorldZ244–254 | Inferred study choice | Local10 mm deck backing starts92.838343208 mm above maximum lifter top; no manufacturing thickness claim |
| Proposed added aperture | InclinedR5, following intake rest rod axis | Inferred study choice | Y93.061156059@Z244,92.856723256@254,92.826058335@255.5,91.834559242@304 |
| Existing passages/cover | R6/Y90 passage; cover inner boundaryY98 | Current model constraint | Existing adapter/passage reports; source dimensions unknown |
| Production oil/coolant passages and sealing requirements | Unknown | Unknown | Current simplified casting is not a traced fluid network |

## Proposed bounded CAD scope — not yet constructed

1. Build a separate inclined rocker/pedestal candidate using the Y90 numeric layout, with the same spherical contact neighborhoods and mounting checks as the frozen vertical adapter. Recompute rather than reuse its pedestal acceptance. No changes to source rod/valve solids or their physical lengths.
2. Lower head: add only the obliqueR5 passage swept along the specified rest axis, clipped to worldZ255.5–304 at each of the twelve existing rod stations. Preserve the existingR6/Y90 passage by union; remove material only within the new cut mask. No upper-head passage change above304. Preserve combustion chambers, valve seats/guides, bolt bores/lands, port and coolant-outlet interfaces. Existing upper passage sampled clearance remains only0.145257 mm atZ304; do not confuse it with a1 mm design margin.
3. Head gasket: add the matching oblique passage clippedZ254–255.5, retaining the old aperture. Preserve all material outside the union mask, every combustion/bolt aperture, and the outer perimeter. Do not substitute a relocated circular hole that fills an existing open passage. Compute actual minimum remaining lands and their continuous support on both faces; production sealing adequacy remains unknown.
4. Block: retain its migratedR11.124565 guide belowZ244 and all actual lifter travel. Add estimated local backing only within each guide neighborhood atZ244–254, then clear the same union of legacyR6/Y90 and obliqueR5 apertures through the backing. Suggested maximum allowed addition mask isR13.124565 centeredY95.109820990, clippedZ244–254; this is the existing guide plus a2 mm connection allowance, not permission for general casting infill. Geometry may only add material here; any proposed removal outside the passage/guide void requires review. Verify connected material and support to existing deck, not twelve detached plugs.
5. Block/head/gasket aperture matching must be checked as an assembled stack. A minimum2 mm model support band around the final union aperture is an estimated educational target, subject to actual topology and source limits. Both faces must have continuous backing. Contact-area and missing-support checks must use the final union outline, not an annulus around only one overlapping hole. If that target conflicts with protected interfaces, preserve failure and return for scope review; do not silently widen masks.
6. Preserve cylinders and bore sleeves, head bolts, the entire valve-cover gasket/support/cover, and all current external fluid seats/bores. Preserve head material outside declared cut/pedestal regions and block material outside declared backing masks by exact symmetric difference at1e-5 mm³. Existing named fluid interfaces must be enumerated and independently probed before any preservation claim. No assertion about absent/unmodeled production passages.

This proposal modifies only the top10 mm of the oversized guide opening. It intentionally leaves the lower guide untouched because no modeled lifter reaches this upper deck region. A longer transition or an inferred casting rib is outside this proposal.

## Delivery and validation

- Readiness: research proposal, uninstalled. No new STEP/GLB, release asset or render; CAD/export and visual gates remain NOT RUN because no CAD candidate was constructed.
- Branch baseline as above; no worker commit/PR or shared integration edits. Parent owns preservation/issue updates.
- Commands: first `.venv-cad/bin/python scripts/check-timing-valvetrain-inclined-hypothesis.py`, then `.venv-cad/bin/python scripts/check-timing-valvetrain-inclined-scope.py`.
- Environment: existing macOS Python3.13/build123d0.10.0 environment; no new installations. Model/effort and usage unavailable.
- Numeric outcomes: maximum linkage closure8.53e-14 mm; intake peak10.033 mm; exhaust nominal peak residual+0.000202687 mm. New lower passage sufficient sampled clearance0.977621039 mm; unchanged upper passage atZ3040.145257029 mm. R3 negative control gives-1.022378961 mm; backing atZ150 gives-1.161656792 mm lifter separation.

| Quality gate | Status | Scope and remaining work |
|---|---|---|
| Application/coverage | Research only | Source constraints inherited; production passage geometry unknown |
| Dimensions/coordinates | PASS numeric scope | Report binds imported STEP and numeric sources; no new placement CAD |
| CAD/export integrity | NOT RUN | No revised solids or exports |
| Source/visual comparison | NOT RUN | No revised geometry; source passage dimensions absent |
| Installed interfaces | NOT RUN | Proposal requires exact protected differences, support and connected-material probes |
| Motion/disassembly | PASS sampled numeric only / broader NOT RUN | Numeric rod and continuous lifter-height bound; contact, spring/rocker/cover/piston and removal checks remain |
| Learning/diagnostics | N/A | Research scope; no installed learning-content changes |
| Browser integration | NOT RUN | Prior security rejection; no alternate surface attempted |
| Reproduction/review | Numeric report reproducible; review pending | All new inputs hashed; integration owner must select neighbor scope |

The previous OCC false negative remains relevant: future exact clearance checks must include independent section/interior probes, plus a deliberately undersized/blocked passage negative control. A zero Boolean common alone cannot establish clearance. Fresh CAD contact, mounting, support, affected fluid-interface preservation, export bounds, actual renders and spring/cover/piston sweeps are required after construction. No old adapter acceptance transfers automatically to the inclined candidate.

## Tracking and restart

Issue #32 stays open. Scope proposal sent to integration owner; no neighbor CAD change has started. Next action is integration-owner selection of this bounded scope, followed by a new isolated module/output directory and preconstruction input hashes. No process remains running. No claim of background continuation or installation readiness.

## Scope approval

The integration owner approved this bounded scope on2026-10-01, including the Y90 hypothesis, matching passage union, localZ244–254 deck backing and protected interfaces. Construction is now authorized only in new isolated `timing_valvetrain_inclined_candidate.py`, its dedicated checker/report and `generated/timing-valvetrain-inclined-candidate/` outputs. No canonical changes or installation are authorized. The proposal-only results above remain a distinct completed research stage.

## Construction findings requiring review

The first clipped oblique-cylinder cutter suffered an OCC false-zero intersection: its inclined portion disappeared, leaving only the oldY90/R6 hole. A strict point witness at(259.48,97,254.75) caught the issue. Rejected artifacts and hashes are recorded in `reference/engine/timing-inclined-rejected-clipped-cylinder.json`. The replacement uses an explicit ruled loft of horizontalR5 circles along the same rest axis. Its section radius is exactly5 mm (rather than the slightly wider elliptical section of a perpendicular-radius cylinder); the numeric sufficient containment bound already uses this conservative5 mm radius. All affected first gates were rerun.

The stack support probe then revealed an inheritedY88/R6 aperture in both actual gasket and lower head, in addition to theY90 passage. `full_engine.py:top_end` creates theY88 aperture; later source-layout additions do not fill it. A support probe around onlyY90 plus the new inclined passage incorrectly counts this intentionally open lobe as missing support. The actual outline must includeY88 as well. Matching that complete opening in the block requires a separately reviewed small crescent cut; it was proposed to root before altering block removal scope. The earlier proposal and passage-map simplification to onlyY90 are not an exhaustive description of the canonical opening.

### Approved three-lobe correction

Root approved retaining the actualY88/R6 +Y90/R6 + inclinedR5 union and clearing that same complete opening in the block only atZ244–254 within the originalR13.124565 mask. Block removal inside this mask is now explicitly authorized; added/removed material outside it must remain below1e-5 mm³. The actualY88 aperture is inherited source-code geometry, not new evidence of production dimensions. `reference/engine/timing-inclined-rejected-two-lobe-support.json` preserves all twelve failed support results, including the measured0.2388842127 mm³ open-lobe contribution on each original head/gasket band. Construction and support probes now both use the actual complete outline.

During this work, root moved the working branch to `engine/timing-clearance-revisions` at `4e480f8e40458384986b9e1792597e87e56daad7`. Original construction baseline and frozen inputs above remain recorded; no worker branch switch or canonical change was performed.

## Delivered candidate — scoped gates complete

This section supersedes the proposal-stage NOT RUN entries only for the gates explicitly completed below. Readiness is **candidate**, not integration-ready or accepted installed. No canonical or browser files changed. Root owns issue/PR/publication and separate review; no worker commit was made.

Parametric module: `cad/engine/timing_valvetrain_inclined_candidate.py`. Entry points: `rocker()`, `head_adapter(old_local_head, manifest)`, `gasket_adapter(old_world_gasket, manifest)`, `block_adapter(old_world_block, manifest)`, `poses(manifest, theta=0, axial=0)` and `passage(station_x, zlo=244, zhi=304, extra=0)`. Head output is local; gasket/block adapters consume and return world coordinates. Export checkers convert through the explicit assembly frames. This distinction is intentional and must be preserved by an integration caller.

Final artifacts: `cad/engine/generated/timing-valvetrain-inclined-candidate/` contains four STEP/GLB pairs (`rocker-arm`, `cylinder-head`, `head-gasket`, `block`), `adapter-comparison.png` and `lower-stack-section.png`. The worker visually inspected the actual exported section: matching aperture edges through the head/gasket/deck, visible positive rod clearance, and the boundedZ244–254 backing. This is a model comparison and section, not a manufacturer-photo comparison. The rejected clipped-cylinder trial remains in its subdirectory. Large artifacts require root's next private checkpoint before a clean-clone reviewer can restore them; final hashes are in the delivery report. Reproduction uses restored canonical inputs and the existing timing-support block STEP identified by hash above; it does not require temporary logs.

Run in this order from the repository root:

```sh
.venv-cad/bin/python scripts/check-timing-valvetrain-inclined-hypothesis.py
.venv-cad/bin/python scripts/check-timing-valvetrain-inclined-scope.py
.venv-cad/bin/python scripts/check-timing-valvetrain-inclined-candidate.py
.venv-cad/bin/python scripts/check-timing-valvetrain-inclined-passages.py
.venv-cad/bin/python scripts/check-timing-valvetrain-inclined-rocker-interfaces.py
.venv-cad/bin/python scripts/check-timing-valvetrain-inclined-piston-envelope.py
.venv-cad/bin/python scripts/check-timing-valvetrain-inclined-export-contacts.py
PYTHONPATH=.venv-cad/lib/python3.13/site-packages MPLCONFIGDIR=/tmp/truck-mpl XDG_CACHE_HOME=/tmp/truck-cache python3 scripts/render-timing-valvetrain-inclined-candidate.py
.venv-cad/bin/python scripts/check-timing-valvetrain-inclined-delivery.py
```

All corresponding `inventory/engine/timing-valvetrain-inclined-*-validation.json` files are listed and hashed in `timing-valvetrain-inclined-delivery-validation.json`. That final checker also verifies all report input hashes and binds the complete transitive local CAD source imports and final artifacts. Re-exporting a STEP can change its file hash even with equal geometry; rerun dependent evidence rather than reusing the old report.

| Final gate | Result and scope |
|---|---|
| Dimensions / closure | PASS numeric hypothesis; source rods/valves unchanged and only rigid poses used |
| CAD / topology | PASS four valid single-solid STEP roundtrips; block connectedness does not certify structural capacity |
| Protected changes | PASS zero head material outside approved pedestal/passage masks; zero added/removed block material outside approved deck masks; zero gasket addition or removal outside declared passage masks |
| Approved block removal | 1,917.139499206 mm³ total inside masks; actualY88 crescent opened through upper10 mm only |
| Geometric mounting | PASS twelve mounting stacks and support annuli; smooth shank insertion still does not establish threaded engagement |
| Exact rocker neighborhoods | PASS zero symmetric difference for aligned fulcrum, ball socket and lower pad patches |
| Exported linkage contacts | PASS120 actual reimported STEP poses, all twelve branches × five event-relative phases × two axial endpoints,0.002 mm contact threshold |
| True-union gasket support | PASS all48 probes: twelve branches × block deck / gasket bottom / gasket top / head; positive2 mm bands approximately1.018–1.019 mm³ each, zero missing volume |
| Actual passages | PASS36 exact full-passage overlap probes and5,400 independent interior point tests, with zero occupied points; numeric sufficient phase envelope remains0.977621039 mm minimum in lower transition |
| Sensitivity | PASS old gasket contains strict rod interior; old block misses0.647628500 mm³ of true-union support band; previous numericR3 aperture and low backing controls fail as intended |
| Piston | PASS sampled whole-CAD separating bound6.744981727 mm; continuous motion not proven |
| Mesh integrity | PASS four watertight GLBs; triangles3,602 rocker /82,746 head /12,428 gasket /73,724 block; largest bounds error0.006842375 mm |
| Visual review | Worker inspected actual CAD/mesh section; independent root review pending; source comparison NOT RUN |
| Fluid interfaces | Spatial preservation PASS outside explicit masks; no production network, fluid-flow or source-validation claim |
| Remaining motion / disassembly | NOT RUN broader spring/cover/neighbors and staged removal; numeric upper-passage clearance is not whole-rocker cover clearance |
| Browser / installation | NOT RUN; prior security rejection respected, no alternate surface or installation attempted |

The block deck lies92.838343208 mm above the actual lifter top at its maximum modeled lift, so the backing does not shorten actual travel. Existing cover lands and protected valve/cylinder/bolt regions remain outside the declared masks. New production casting, coolant or oil-channel dimensions have not been inferred from clearance success.

Root review of the completed isolated package is the next action, followed by any authorized broader neighbor sweep. Issue #32 remains open. All worker processes are finished; no background continuation is claimed. Python syntax checks of all new source/checker/render files pass. Navigation was not rerun because no installed manifest/viewer/navigation content changed. Usage and billing remain unavailable.
