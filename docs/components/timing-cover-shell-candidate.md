# Component contract: isolated timing-cover shell and joint proposal

Issue #32 under Engine #1. Worker: air_cleaner_candidate; integration owner: root. Branch `engine/runner-stops-and-evr`; baseline `796b621244d8e341fe2f3c4de7af99488af01548`. No canonical changes. This new candidate supersedes no installed component.

Owned: `cad/engine/timing_cover_shell_candidate.py`, `scripts/check-timing-cover-shell-candidate.py`, `reference/engine/timing-cover-shell-review.json`, `inventory/engine/timing-cover-shell-validation.json`, this handoff and `cad/engine/generated/timing-cover-shell-candidate/`.

Scope: source-compared seven-hole cover shell/flange, main gasket and proposed isolated block mating land. All dimensions and registration are explicitly estimated. Existing dimensionless gasket outline remains primary data; photo topology and replacement applicability are in `reference/engine/timing-cover-joint-review.json`. Do not include the unidentified five-hole strip. No installed completion or pan-terminal sealing claim.

Parameter contract: current model axial seat X = 373 mm, gasket thickness 0.8 mm, cover face X = 415 mm, crank-seal center X = 414 mm. Scale and in-plane rotation are estimates exposed as parameters. Crank stays YZ = (0,0); compare current cam YZ = (90,72) and gear-worker proposal (95.109821,76.087857). Neither is a verified factory axis. Source envelopes use crank/cam tip radii 43.18/83.947 mm; tooth/helix evidence remains gear-worker owned. No cam axis is inferred from the cover's decorative circular casting mark.

A seven-hole homography between two actual product images yields a source-view crank-aperture center near (595,955) in the 1600-pixel gasket display. Its small residual is photo correspondence only, not a measured scale or casting datum. Candidate uses exposed scale 0.23 mm/reference pixel initially. If cavity tests reject that estimate, report the failure and revised proposal rather than hiding it.

Proposed block land is separate isolated material behind the model seat. It is not a detached installed part and does not replace the canonical block. Verify remaining wall around seven blind sockets, annular seat area and full gasket support; missing/shifted gasket and plugged-bore fault controls. Test both gear-axis envelopes and fixed crank-seal interface. STEP roundtrip volume tolerance 0.01 mm³, GLB bounds tolerance 0.2 mm, collision audit tolerance 0.1 mm³. Pan land X = 365–381 remains untouched and its terminal interface is unresolved.

Affected neighbors for any future installation: block front casting/lands, cam bearings and thrust plate if axis changes, camshaft/lifters/distributor/oil drive and valve train if axis changes, crank gear and crankshaft snout, front crankshaft seal, damper/pulley, water pump and front accessory brackets, oil-pan front gasket/bolts/bridge and timing pointer. Each requires its relevant renewed checks; no existing clearance report certifies this proposal.

## Evidence ledger

| Feature | Evidence class and source | Limit |
|---|---|---|
| Seven bosses, cavity, crank aperture, lower bridge | Dorman 635-109 actual specimen photos; direct cross E5TZ 6019-H | Replacement topology, not measured casting |
| Truck application | Pioneer 500300 catalog printed page 15: 1965–96 F-series L6 4.9; illustration page 31 gives E5TE-6019-H | Preserve E5TE versus E5TZ distinction |
| Main gasket open arch and seven holes | Fel-Pro TCS 45829 and TCS 45830 manufacturer images; primary normalized coordinates in prior outline module | Pixel uncertainty and strip identity retained in review JSON |
| Seal and gear stations | Current model and gear-worker estimate | No factory axial or center-distance measurement |
| Registration and scale | Seven-hole photo correspondence, estimated crank pixel (595,955), zero rotation, scale 0.24 mm/reference pixel | Selected for feasible envelope; never a manufacturer dimension |

Source URLs, exact capture hashes and application limits are copied into `reference/engine/timing-cover-shell-review.json`. Re-fetch those public manufacturer assets if ignored local captures are unavailable. No source originals belong in Git or asset releases. The previous dimensionless outline remains the primary evidence; this scaled instance is only a model proposal.

## Delivery

Uncommitted candidate on the contract branch; no PR or release created by this worker. API: `build(p=Parameters())` returns three world-coordinate mm solids: `timing-cover-shell-candidate`, `timing-cover-main-gasket-candidate`, `timing-cover-block-land-proposal`. Parent is an isolated study, with identity transform; display explosion is X +25/+10/−10 mm only. No canonical part IDs change. Proposed block land is future casting material, not a separately installed part.

Build from repository root: `.venv-cad/bin/python scripts/check-timing-cover-shell-candidate.py`. Then render without repeating CAD checks: `python3 scripts/check-timing-cover-shell-candidate.py --render`. Dependencies are the prior dimensionless outline module, existing CAD metric helper and available build123d/trimesh environment. The render uses system Python's NumPy/Matplotlib. Tested on macOS 15.6.1 arm64, Python 3.13.12, build123d 0.10.0, trimesh 4.7.4. Matplotlib uses a writable temporary cache if the home cache is unavailable; geometry is unaffected. Model/effort and billing usage unavailable.

Artifacts are under `cad/engine/generated/timing-cover-shell-candidate/`: three STEP/GLB files, combined `candidate.glb`, `preview.npz` and actual mesh `candidate-review.png`. Hashes are recorded in the review; no release URL yet. Existing canonical manifest was not an input and installed manifest validation is NOT RUN.

## Validation and review

| Gate | Result | Evidence and limits |
|---|---|---|
| Application/coverage | Partial | Manufacturer replacement comparison supports topology. Strip and pan terminals unresolved. |
| Dimensions/coordinates | Estimated | Model plane X373 and seal X414 preserved; both cam layouts tested, no factory dimensions claimed. |
| CAD/export | PASS | Three valid single solids, watertight meshes, STEP volume and GLB bounds within contract thresholds. |
| Seat and proposed land | PASS | Full 9843.2046 mm² gasket seating probe supported on both sides. Seven clear blind sockets retain radial material and bottom floors. Applies to proposed land only. |
| Fault controls | PASS | Shifted gasket loses support; removed gasket leaves 0.8 mm gap; plugged socket obstructs bore. |
| Gear cavity | PASS | Both source OD envelopes have zero overlap, crank minimum clearance 3.0322 mm and cam 0.25 mm. Two mm exterior support witness passes both layouts. Conservative envelope check, not tooth-motion simulation. |
| Fixed crank seal | PASS | Existing annulus has zero overlap and full outer seat support. Seal interference/material specification unknown. |
| Source/visual comparison | Partial | Actual exported exploded and section views inspected against manufacturer pixels. Source topology visible, but estimated constant depth, relief and bridge are not finished casting fidelity. |
| Pan joint | FAIL | Unchanged current front gasket annulus intersects proposed bridge by 1421.2092 mm³. Full gasket and both open terminals remain unresolved. |
| Installed interfaces | NOT RUN | No canonical installation; proposed block land does not prove block oil/coolant-wall integrity. |
| Motion/disassembly | NOT RUN | No installed gear, fastener removal or accessory movement study. Static envelope and exploded display only. |
| Learning/diagnostics | NOT RUN | Failed CAD review notes are developer evidence, not user-facing component function or diagnostic content. |
| Browser integration | NOT RUN | No browser acceptance inferred from offline render. |
| Reproduction/review | Worker reviewed | Deterministic checker and input hashes saved; root review of this shell pending. |

The initial cavity intersected the cam envelope. Internal relief removed this interference but the initial 0.23 scale failed the unchanged 2 mm exterior-support requirement. A cheap outer-profile comparison found scales 0.24, 0.25 and 0.26 feasible. The lowest tested estimate, 0.24, was selected and the full checks rerun. Failed source/report snapshots remain in `rejected-initial-cavity/` and `rejected-thin-wall/`; parameter results are `registration-comparison.json`. An early spline Boolean produced invalid fused geometry and was discarded in favor of planar corner subdivision. The contour is smoother than the prior angular trace but remains approximate. No tolerances were relaxed.

Worker inspection confirms the seven-boss asymmetric shell, lower crank opening, rear land and recessed cavity. Section Y = 40 mm exposes the seat stack and seal boss; source casting has more varied sections than this model. Root's earlier outline review accepted topology only and requested smoother contours and fewer axial ticks; both are addressed here without claiming finished fidelity. This candidate can be reviewed as bounded code, but cannot be installed. No shared geometry or checks were changed.

## Tracking and restart

Issue #32 remains open. Root should review the actual shell render and proposed model datum before coordinated geometry changes. Next evidence needed: applicable pan junction/strip installation detail, actual cover axial dimensions, scale and bolt sizes. Then resolve the lower bridge against OS34601R and validate the proposed land against the full block, oil/coolant paths, thrust plate and seven fastener engagement stacks. If the cam moves, coordinate all neighbors listed in the contract; the independent gear worker found interference with unchanged camshaft and current cover. Do not install either isolated candidate independently.

No running process. Latest log: `cad/engine/generated/timing-cover-shell-check.log`. Exact next action is source/joint review, not an unchanged checker rerun. All failed experiments and source capture hashes remain reproducible from committed code/review and named public sources; ignored generated artifacts can be rebuilt.

Root review: accepted bounded source topology and feasibility only; installation remains blocked. Follow-up baseline is `124aa7c345af352459a800343ffc50f1e931367c` on `engine/exhaust-timing-joints` after PR #94.
