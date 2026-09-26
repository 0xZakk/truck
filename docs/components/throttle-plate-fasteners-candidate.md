# Illustrative throttle plate fastener candidate

## Contract

Issue #43 under engine #1. Baseline commit `5567d751abcf6a9bfac84bdf87ce0d7f0d4dac5c`. Contributor: component worker; integration owner: root. Scope is isolated educational retention, not Ford-verified count or dimensions. Owned files are this handoff, the new plate-fastener module/checker/report and `reference/engine/throttle-plate-fasteners-review.json`. Shared shaft, plates, manifest and atlas are untouched.

Preserve millimeter units, current shaft/key geometry, local plate centersY±27 and parent originworld(394,25,490). Actual source count remains unknown; task explicitly permits a bounded educational choice: two screws per plate. Inferred screw heads must seat on plate faces, mating helical surfaces must engage shaft, and proposed pockets/pads must connect to existing material. Test export, local all-occurrence broad phase, swept exact neighbors, physical clamp and negative disengagement controls. No thread strength, locking, torque, manufacture or factory fidelity claim.

Source and assumption ledger: `reference/engine/throttle-plate-fasteners-review.json`. Applicable factory images and procedure were reread before modeling; the four body mounting nuts and external stop screw do not establish plate screw count. Comparison photo supports screw-like features, not an exact production total.

Candidate checks pass within the explicitly limited scope below. Installed acceptance and production fidelity remain unresolved.

## Evidence and bounded educational choice

The exact1994 factory procedure removes the throttle body as an assembly. Figure690365451 identifies four body mounting nuts; figure689805816 labels an external plate set screw/stop. Neither reveals butterfly screw count or internal shaft cross-section. The applicable throttle-valve inspection calls for checking smooth movement and loose, bent or damaged plates, without specifying their internal screws. URLs, local archive paths and hashes are in the review ledger. Manual originals remain ignored and are not redistributed.

The reinspected F2TE-MA comparison photo is a manifold-flange view with two screw-like heads visible on one plate and one clear on the other. The other region is dark; the seller's broad application is not proof for this truck. **Four total is an explicitly inferred symmetric educational choice, not an observed factory count.** Heads are placed on the model's negative-X/manifold side to follow the visible comparison orientation, while retaining that application uncertainty. The illustrated cross drive, dimensions and complete internal architecture are estimates.

## Candidate geometry and interfaces

Existing shaft, keyed lever end, bore axes and plate poses are preserved. The shaft is received from the actual current `throttle-shaft` STEP definition, not reconstructed from an older cylinder. Each plate remains centered at localY−27 or+27 under `throttle-moving`; that parent's inherited origin is world(394,25,490). Four screw axes run along X at localY−35,−19,+19,+35, Z0.

Each head has radius1.8 mm, thickness1 mm and an underside at X−0.5, directly seated on the existing1 mm plate's manifold face. Its shallow cross recess is illustrative. The plate receives two radius1.15 mm clearance holes at its ownY±8. Each negative-X shaft rail receives a radius1.9 mm head pocket fromX−4 to−0.5, allowing direct plate seating. Each positive-X shaft rail receives a radius2 mm pad fromX+0.5 to+0.7, bridging the inherited0.2 mm slot gap and supporting the plate's opposite face. These pads overlap existing rail material; no free-floating support is added.

Each screw has an inferred0.85 mm core radius and1.1 mm thread major radius. The2.7 mm threaded region spansX+0.5 to+3.2; the nominal pitch is0.5 mm with an explicitly modeled triangular helical ridge. **This is not an ISO/SAE or Ford thread specification.** The shaft is cut with a phase-matched helical tap extending1.5 mm beyond each end of the male threaded region. This avoids an artificial female runout left by cutting only with the finite screw. The tap profile adds an inferred0.02 mm radial and axial clearance; measured minimum nominal screw/shaft gap is0.010533 mm on the sloped flanks. Nominal thread contact area is therefore zero; preload or bearing contact is not falsely claimed. Interlocking is demonstrated by axial withdrawal interference and clear coupled rotation/withdrawal. The paired smooth-clearance-bore negative control removes those flanks and must fail axial retention despite unchanged screw coordinates.

The head–plate–rear pad–shaft thread path supplies geometric capture/retention. Clamp force and preload are not modeled. This is a teaching mechanism, not a strength or assembly-process validation. Actual torque, thread class, insertion tolerances, locking/staking, screw replacement policy and anti-loosening construction are unknown. Plate bevels, airflow and actual stop calibration remain inherited gaps.

## Delivery and reproduction

Owned files:

- `cad/engine/throttle_plate_fasteners_candidate.py`
- `scripts/check-throttle-plate-fasteners-candidate.py`
- `inventory/engine/throttle-plate-fasteners-candidate-validation.json`
- `docs/components/throttle-plate-fasteners-candidate.md`
- `reference/engine/throttle-plate-fasteners-review.json`

API: `screw()` returns one screw centered on localY0,Z0 with its head on negative X. `parts(current_shaft,current_plate,finite_thread_cutter=False)` returns proposed shaft/plate definitions and four positioned screw solids. The optional `finite_thread_cutter=True` is a diagnostic baseline that reproduces the rejected finite-thread termination for conservative sweep proof; it must not be integrated. Definitions are local to `throttle-moving`. For later integration, preserve `throttle-shaft`, `throttle-plate-1` and `throttle-plate-2` occurrence IDs; replace their definitions coherently, retaining plate positions. Add four screw occurrences at localY−35,−19,+19,+35 and identity rotation, using the shared screw definition. The new module contains no assembly or viewer writes.

From repository root:

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-throttle-plate-fasteners-candidate.py --quick
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-throttle-plate-fasteners-candidate.py
XDG_CACHE_HOME=/tmp/truck-cache MPLCONFIGDIR=/tmp/truck-plate-mpl python3 scripts/check-throttle-plate-fasteners-candidate.py --render
```

Environment: macOS, CAD Python3.13.12/build123d0.10.0/trimesh4.7.4; system Python/matplotlib3.10.9 for rendering. Cache paths are optional writable runtime locations, not dependencies. Model usage/billing figures are unavailable.

Ignored output directory: `cad/engine/generated/throttle-plate-fasteners-candidate/`. It contains three proposed definition STEP/GLBs, `preview.npz`, `candidate-context.png` and `candidate-screw-detail.png`. Mesh coordinates use browser meters [X,Z,−Y]; source CAD remains millimeters. Reproduction requires current relevant STEP/GLB definitions and the retained evidence ledger. No temporary image files are required, and no source images are copied into Git. Asset publishing is NOT RUN.

## Validation and review

The current report's hashes define scope. A manifest snapshot identifies the inspected assembly but is deliberately not a whole-manifest mutation guard: root may integrate unrelated work concurrently. All exact selected STEP files and directly used candidate modules are guarded. Every occurrence participates in conservative mesh-AABB broad phase; relevant candidates then receive exact solid intersections. The source shaft's outside-seat geometry must remain unchanged.

The full sweep covers0–90° every2° plus45° (47 poses). Neighbor transforms follow the manifest's throttle motion, and the installed illustrative spring is regenerated from its own exact deformation module for each pose. A rotating shaft is not compared against frozen lever/pin geometry. Candidate-internal contacts are checked separately because all those parts move rigidly together.

Retention checks include actual head/plate contact, nominal thread clearance, rear support contact, plate motion toward and away from its heads, sideways hole/shank interference, direct screw withdrawal, coupled quarter-turn withdrawal, detached-head loss of seating and the smooth-bore negative control. Checks do not infer engagement from a cylinder merely overlapping the shaft's axial range.

| Gate | Result/scope |
|---|---|
| Application/coverage | Explicit four-screw illustration; production count/architecture unknown. |
| Dimensions/coordinates | Inferred values; preserve current shaft/key and plate poses. |
| CAD/export | Checker requires valid one-solid definitions, watertight meshes, STEP volume error<0.001 mm³ and GLB bounds error<0.2 mm. |
| Source/visual comparison | Source images reinspected; new render reviewed before final handoff. No factory-fidelity claim. |
| Installed interfaces | NOT RUN; isolated proposed replacements only. Nominal interfaces and physical retention tested locally. |
| Motion/disassembly |47 sampled poses and retention/unthread controls; no continuous collision or installation-process certification. |
| Learning/diagnostics | Distinguishes plate retention from four body nuts and external stop screw. |
| Browser integration | NOT RUN; root owns shared installation and atlas. |
| Reproduction/review | Commands, hashes, ledger, export and render provided; integration-owner acceptance pending. |

## Final measured result

PASS on manifest snapshot `bfab1f2596991d27fe5e52e90f02d070eb034f9de8c2cd72d3dd44666d6c8bb9`. All1,322 occurrences entered broad phase;15 nearby occurrences were selected. The initial finite-thread shaft underwent47 exact motion poses and658 candidate/neighbor intersections with zero collisions. The corrected female tap only removes shaft material: regenerated baseline comparison finds **zero added material**, and plates/screws are unchanged. The final `--reuse-sweep` run requires the same manifest and relevant dependencies, records previous report/input/output hashes, and proves current geometry is a subset of that previously swept geometry. This preserves collision coverage conservatively; reported prior distances are lower bounds for the corrected candidate, not freshly measured exact distances. Fresh current internal-intersection, interface, retention and export checks pass. The default command independently reruns all47 poses when reproducing from scratch; no cached report is required for that path.

Each head seats over6.02400 mm²; each plate has16.82323 mm² rear support. Straight screw withdrawal by0.125 mm interferes with female flanks by approximately0.56194 mm³. A−90° X rotation combined with the same headward translation clears; reversed rotation interferes by0.83897 mm³. A smooth-clearance-bore substitute has zero axial-retention interference and fails the retention condition. Detached screw heads have zero plate contact. Plate headward, tailward and sideways escape controls each produce positive interference.

All three definitions are valid single solids with watertight GLBs. Maximum STEP volume error is6.604e−7 mm³ and maximum GLB bounds error0.008773 mm. Shaft changes outside the four allowed seat regions are zero, and the original plate positions remain unchanged. The final two-sided assembly context and isolated screw-detail renders were opened for inspection; they expose head-side orientation, four retained positions and the helical thread/drive geometry. These visuals compare the educational geometry to the observed concept only; they do not verify factory dimensions or count.

## Tracking and next actions

Issue #43 remains open. Root should review the candidate and source limits, integrate all three definitions/four screw occurrences coherently if accepted, rerun installed checks and inspect closed/mid/open browser views. Code merge is distinct from installed acceptance. Follow-up evidence needs an exact applicable specimen with each head, shaft slot, threads and staking exposed. The [F2TE-EA manual-transmission listing lead](https://www.ebay.com/itm/257472725875) was searched again; its page still returned a cache miss, so no new specimen image or count was established. No commits or external posts are made by this worker.

No background process remains running at handoff.

Final worker command was `XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-throttle-plate-fasteners-candidate.py --reuse-sweep`; it reran all current export, internal-interface and retention checks and preserved the guarded47-pose collision evidence via the subset proof. `--reuse-sweep` is optional and requires a compatible existing full-sweep report; use the unflagged command for an independent complete reproduction.
