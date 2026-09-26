# Illustrative single throttle return spring candidate

## Contract

Component issue #43, parent engine #1. Contributor: bracket/linkage worker; integration owner: root. Baseline commit `5567d751abcf6a9bfac84bdf87ce0d7f0d4dac5c`; manifest and all actual candidate inputs are hashed in `inventory/engine/throttle-return-spring-candidate-validation.json`.

**The integration lead explicitly authorized one illustrative torsion spring. This is not a claim that Ford used one spring, this winding arrangement, these anchors, or these dimensions.** Actual production spring count, construction, free position and retention remain unresolved. The separate cable-end compression spring established by factory Test C is excluded.

Owned files: this handoff, `cad/engine/throttle_return_spring_candidate.py`, `scripts/check-throttle-return-spring-candidate.py`, and `inventory/engine/throttle-return-spring-candidate-validation.json`. No shared assembly, atlas, manifest or source ledger changes. A later bounded instruction also authorized new `viewer/throttle-return-spring-paths.json`, `viewer/throttle-return-spring-mesh.js`, `scripts/check-throttle-return-spring-paths.mjs`, and `inventory/engine/throttle-return-spring-path-validation.json` for independent animation preparation. Candidate-only isolated bracket and lever seat changes are returned by the new module.

World CAD units are millimeters. Shaft axis is world X394,Z490, rotation positive Y; moving parent origin is (394,25,490). The spring spans stationary and moving parents and cannot be represented by a rigid child of either. No service/engineering number is claimed for the illustrative wire. Explode/disassembly sequencing is not implemented.

Dependencies verified locally: final linkage and shield candidate modules, original unchanged shaft STEP, manifest neighbor STEP files, existing CAD environment and spring research ledger. Original source images remain in the ignored authorized manual archive and are not copied into Git.

## Evidence ledger

| Feature | Class | Evidence and limitation |
|---|---|---|
| Cable-side external coil bank | Factory topology | Figures690090240/690365451; exact source paths and hashes in `reference/engine/throttle-return-spring-review.json`. |
| Actual shaft spring count and separate wire paths | Unknown | Perspective factory views and F2TE-FA comparison specimen do not expose every wire and anchor. |
| Separate cable-end spring | Applicable factory procedure | Cable/linkage Test C, documented in research handoff; not represented here. |
| One spring, three turns, radius8.8 mm closed, wire radius0.45 mm | Explicit illustration | Integration-lead scope decision; no Ford dimension or physical rating. |
| Fixed/moving tang seats and hooks | Model-derived estimates | Available material in final revised bracket and lever; exact CAD checks below. |
| Positive return direction | Kinematic illustration | Opening increases winding angle and decreases coil radius at conserved analytical centerline length. Restoring direction is toward the closed reference for positive elastic stiffness; magnitude, preload and reliable friction return are unverified. |

## Geometry and interfaces

The fixed tang passes through a proposed radius0.5 mm Y-axis hole at world(389,104,503) in the bracket web Y103–105. Its return end lies at Y107, and the radial leg lies at Y100. The hook extends2 mm radially beyond the hole center. These two sides prevent straight axial withdrawal across the bracket material; insertion/flexure is unmodeled.

The moving tang passes through a proposed radius0.5 mm Y-axis hole at lever local(0,65,18), closed world(394,90,508). The return end is world Y87.5 and the radial leg Y94, capturing the lever sheet Y89–91. Its return also extends2 mm radially. Both proposed holes are the only seat changes; original mounting, key, ball stud, cable hole and shield pin datums remain unchanged. Holes and wire radius imply0.05 mm nominal radial clearance. They are illustrative geometry, not manufacturing tolerances.

The coil centerline runs between Y100 and Y94, starting at angle atan2(−5,13) from +Z and ending at 6π+lever angle. A scalar bisection solves radius at each pose to conserve the complete CAD centerline length, including all curved transitions. The straight tang anchors remain fixed in their respective frames. Coil pitch changes with winding; the whole coil does not rigidly spin.

The wire is swept along a continuous, tangent-matched path comprising an analytic helix, straight tang sections and quadratic/cubic Bézier bends. The tang-to-coil transitions span0.18 radians of the nominal helix at each end. The final candidate has no spherical joint unions or allowance enlargement. Full curved centerline length is conserved; finite CAD integration error is recorded. This is a continuous single-solid geometric approximation; forming, bending strain and local stress are not simulated. No shaft guide, spring material model, load, friction, coil buckling or fatigue claim is made.

## Delivery and reproduction

API: `spring(angle)` returns world-coordinate wire CAD; `radius_at(angle)` and `analytical_length(angle,radius)` expose the deformation rule (the latter measures the complete CAD curve, despite its short API name); `path_points(angle,radius)` exposes the animation centerline; `seats(existing_shaft)` returns stationary and moving dictionaries derived from the final shield/linkage candidates. Supply the original `cad/engine/generated/throttle-shaft.step`, not the installed extended shaft, to avoid adding the keyed extension twice.

From repository root:

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-throttle-return-spring-candidate.py --quick
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-throttle-return-spring-candidate.py
XDG_CACHE_HOME=/tmp/truck-cache MPLCONFIGDIR=/tmp/truck-spring-mpl python3 scripts/check-throttle-return-spring-candidate.py --render
```

Environment: macOS; CAD Python3.13.12/build123d0.10.0/trimesh4.7.4; rendering system Python with matplotlib3.10.9. Cache paths are optional writable runtime locations, not handoff dependencies. No commits or external posts from the worker.

Ignored outputs under `cad/engine/generated/throttle-return-spring-candidate/`: spring0/45/90 STEP+GLB, bracket/lever seat STEP files, `preview.npz`, and `candidate-context.png`. Exported meshes use browser axes [X,Z,−Y] in meters; exact CAD remains millimeters. Outputs are reproducible and not copied into tracked files. Release publishing and installed browser checks are NOT RUN.

## Validation and review

Check report is authoritative for the current candidate hashes. Initial cheap neutral/mid/open testing exposed a STEP inconsistency in rounded boolean joints. Those joints were replaced by a tangent-continuous sweep; the final geometry passes strict adaptive STEP volume comparison without loosening tolerances.

The full isolated study samples0–90° every10° plus45°, while the quick command uses0/45/90°. It tests spring against the final proposed bracket/lever, shaft/pin/ball, shield/pushpin, straight cable envelope and actual manifest throttle/TPS/IAC neighbors. Exact collision threshold is1e−5 mm³; no generic collision exclusions. Nominal clearance seats are intentional; they need not have artificial bonded contact. Positive axial hook-withdrawal intersections prove geometric capture at the closed pose. An intentionally rigidly rotated fixed anchor at45° must fail the0.05 mm anchor tolerance. Anchor errors, length range and minimum clearance are recorded per pose.

| Gate | Status and scope |
|---|---|
| Application/coverage | Explicit illustrative scope only; actual Ford spring count unresolved. |
| Dimensions/coordinates | Estimated, model-grounded seat locations; report checks both endpoint frames and analytical length. |
| CAD/export | Report checks valid one-solid wire, STEP volume, watertight GLB and bounds at0/45/90°. |
| Source/visual comparison | Coil-bank concept supported; exact one-spring geometry deliberately not claimed as factory matching. Candidate render review recorded below. |
| Installed interfaces | NOT RUN; isolated final linkage/shield baseline only. |
| Motion/disassembly | Sampled deformation and collision checks; not a continuous collision proof. Insertion and disassembly NOT RUN. |
| Learning/diagnostics | Candidate clearly distinguishes winding/return direction from calibrated force and separate cable-end spring. |
| Browser integration | NOT RUN; atlas installation is not included. |
| Reproduction/review | Commands, hashes, report and outputs provided; integration-owner review pending. |

## Animation preparation and proposed integration

Use a stationary descriptor with `axisOrigin:[394,25,490]`, `axis:[0,1,0]`, `wireRadius:0.45`, `turns:3`, `fixedAngle:atan2(-5,13)`, `fixedY:100`, `movingY:94`, fixed radial anchor √194, moving radial anchor18, and closed radius8.8. Fixed return end Y107 and moving return end Y87.5 are joined through1 mm Bézier corner offsets; coil transitions use0.18 rad trim and0.7 mm tangent control distances. Use the module as the geometry specification; the simpler sharp-corner helix equation is insufficient to match these bends. At each opening angle, construct the matching straight/Bézier/helix centerline segments and solve the same constant-full-curve-length scalar equation, then regenerate tube vertices around the centerline. The fixed hook coordinates stay constant; only the moving hook rotates with the lever. Do not put the entire spring GLB under `throttle-moving`. STEP/GLBs remain reference poses. The following exact-path table and pure mesh module now implement the geometry preparation; atlas wiring is still owned by root. Preserve labels that this is one illustrative spring and not verified Ford construction.

`viewer/throttle-return-spring-paths.json` contains91 integer poses0–90, each with1601 equally spaced arc-length samples from the exact CAD centerline/radius solver, rounded to0.00001 mm. Size is4,434,992 bytes. The file includes source hashes, per-frame curve/polygon lengths, anchor errors and coil-spacing checks. It does not recompute independently invented viewer geometry.

`buildThrottleSpringMesh(frame, wireRadiusMm=0.45, sides=12)` in `viewer/throttle-return-spring-mesh.js` returns `Float32Array` positions/normals and `Uint32Array` indices. Coordinates are already browser meters [X,Z,−Y]. Build a Three BufferGeometry using these arrays; use identity placement under the stationary assembly, not the rotating lever parent. Normals use parallel transport, endpoint caps close the mesh, and the helper imports no Three dependency. Each reference mesh has19,214 vertices and38,424 triangles. This module deliberately has no atlas-side loading, disposal or slider wiring.

Reproduce animation preparation/checks:

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-throttle-return-spring-candidate.py --paths
node scripts/check-throttle-return-spring-paths.mjs
```

Standalone JS report `inventory/engine/throttle-return-spring-path-validation.json`: PASS for all91 path frames, maximum sampled length loss0.007493 mm, endpoint deviation0.00000640 mm, minimum sampled nonlocal centerline spacing1.81237 mm against0.9 mm wire diameter. Minimum analytical coil-turn surface gap0.913545 mm. Closed oriented topology is checked at0/45/90; a wrongly rotated fixed endpoint is rejected. Sampled self-spacing is a sanity check, not continuous exact-CAD collision certification. Fixed tang anchor-to-polyline gap is below0.00000634 mm. Frame-table SHA-256 is `19ca2d0bbe8e6251656df1fcec294e7dbc9cbf34c23004283541bdd3fa79de8f`.

## Tracking and restart

Final isolated CAD result: PASS on manifest `330b2c5f10534fd1298f350ee94f30cd2b2a3c39f958a4e0a0b68a767f455f8d`. Eleven poses produced62 exact candidate/neighbor intersection checks with zero overlap. Both seats have0.05 mm nominal radial clearance; minimum shield clearance3.00145 mm, pushpin4.97671 mm, cable envelope4.02639 mm. Both hook withdrawal tests intersect their seat by1.00699 mm³. Exact full curve length198.529139 mm varies by less than2e−9 mm; radius changes8.8→8.06159 mm. All three exported reference poses are watertight single solids; STEP volume difference below5e−11 mm³ and GLB bound error below0.000224 mm. Wrong-parent anchor control at45° misses by10.6603 mm. The three-pose context render was opened and visually reviewed: a stationary fixed hook, deforming coil and lever-following moving tang are visible behind the translucent bracket; labels and frame titles are readable.

Issue #43 remains open. Code may be reviewed as a limited educational candidate; it is not accepted installed. Root must review the geometry, add coordinated seat replacements and a deforming animation, rerun installed neighbor/cable checks, and inspect the browser before any installation acceptance. Production follow-up still needs exposed spring ends, count, retention, actual wire dimensions and relevant mechanical data. Usage/model billing figures unavailable. No background process remains running. Neutral spring STEP is world CAD at identity under `throttle-assembly`; proposed bracket seat is also world CAD, and proposed lever seat is local to `throttle-moving`. Preserve existing bracket and lever occurrence IDs when selecting their replacement definitions. Exported `spring-0.step` is the neutral reference; the animated mesh must use the stationary frame and table-selected angle, never an additional lever rotation.
