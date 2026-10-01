# Component handoff: corrected-direction cam lobe candidate

## Contract before modeling

Issue #32, integration owner root. Baseline `dafb817`, current branch `engine/timing-motion-integration`. Own NEW `cad/engine/cam_clockwise_candidate.py`, `scripts/check-cam-clockwise-candidate.py`, `inventory/engine/cam-clockwise-candidate-{build,contact}-validation.json`, this handoff and `cad/engine/generated/cam-clockwise-candidate/`. Frozen studies and canonical files remain unchanged.

The actual coupled-core cam comes from translated canonical source-sized cam geometry; thrust/backlash revisions did not modify its lobes. Source lobe law lives in `valve_motion_candidate.lobe_shape`, with sampled profile `cad/engine/candidates/valve-motion/profile.json`; `valve_layout_candidate.cam_adapter` replaces each 15 mm station at physical phase +(event center)/2. Replay the exact positive-phase generator on the preserved cam and require geometric identity before the candidate. Then rebuild the same lobe source at negative placed phase only. Do not reflect the shaft or profile, change lift samples, scale geometry or alter event scheduling.

Local frame: millimeters, X shaft, Y/Z about cam axis; world axis `(95.1098209901611,76.08785679212888)`. Explicit change masks: each existing lobe station X±7.5 mm and radius≤26 mm. Protect shaft core R≤17.9 mm within these stations and all geometry outside the masks: journals, ends, nose/key/retention and existing crossed-drive gear. Retaining the latter geometry does not establish corrected handedness. Rest physical lobe phases change +(468/246+firing)/2 to their negatives, with positive q and physical cam rotation +q/2+degrees(K*axial). The profile is symmetric; no mirrored shape is necessary. Effective event angle becomes q+2degrees(K*axial).

Acceptance stages: source replay and locality (<1e-5 mm³ symmetric difference), valid one-solid STEP and roundtrip (<0.001 mm³), watertight winding-consistent positive-volume GLB with bounds error <0.15 mm. Then actual exported lobe/lifter contacts at 12 stations × five event-relative offsets (-150,-96,0,96,150) × axial endpoints (0,-0.1 mm), matching the prior <0.002 mm surface witness criterion. Independent moved-normal witness, wrong cam sign and omitted lobe rephase must fail. Contact coverage is sampled; analytic profile reflection is continuous only for the declared lift law, not a whole-engine interference proof. Render actual STEP section and exported mesh overview. Bounded differences and matching source imply a phase revision, not new production fidelity. Source spring nominal residual remains unchanged. No crossed-drive, loaded-contact, whole-engine axial or browser acceptance.

## Delivery status

Validated bounded candidate; build, contact, independent-section and practical-linkage stages PASS. Root integration and browser acceptance remain pending. Reproduce with `XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-cam-clockwise-candidate.py --build` then `--contact`. Canonical integration is root-owned. Source originals remain unredistributed; generated profile/source/helper/artifact hashes will be bound. Units/stable camshaft identity preserved; no automatic installation.

## Probe correction retained as evidence

`inventory/engine/cam-clockwise-coplanar-probe-diagnostic.json` retains two rejected probe trials. Source replay produced zero difference, but symmetric differences of clipped lobes were unstable at shared/interpolated boundaries: a changed station returned zero, another only 0.0237 mm³, and others implausibly large. Such values are labeled `boolean_changed_mm3_untrusted` and are not acceptance measurements. The core gate now tests missing material from an inset R17.9×14.9 mm cylinder, preserving the original 1e-5 mm³ threshold; independent strict points cover X offsets ±7.49 and 0. Exterior exclusion masks use 0.0001 mm numerical padding in radius and at each axial face, explicitly separated from the source generator's exact ±7.5 mm extent. Construction itself only replaces the original 15 mm lobe.

New owned `scripts/check-cam-clockwise-sections.py` and `inventory/engine/cam-clockwise-candidate-section-validation.json` independently read actual BRep cross-sections. They compare replay to original and revised lobes to rigidly rotated original outlines at 4096 boundary points with <0.002 mm Hausdorff error and <0.02 mm² area error. These are finite polygon approximations, not lowered solid-difference thresholds. A wrong-phase boundary must fail. The script also renders the exported GLB and actual section into `cam-clockwise-mesh-section.png`. This independent gate is mandatory before acceptance; a completed build report alone is insufficient.

Run section/render check using the documented host plotting environment: `PYTHONPATH=.venv-cad/lib/python3.13/site-packages MPLCONFIGDIR=/tmp/truck-mpl XDG_CACHE_HOME=/tmp/truck-cache python3 scripts/check-cam-clockwise-sections.py`. The cache directories are optional runtime locations, not report inputs. No source image is republished.

## Completed local gates

Build passes: source replay0 mm³, inset protected-core missing material0 at all12 stations, exterior protected-region difference0 with explicit0.0001 mm mask padding, and injected protected shaft notch0.5235988 mm³ detected. STEP roundtrip volume residual4.65e-7 mm³; exported mesh37,432 triangles, watertight, winding-consistent and positive volume, maximum bounds error0.007965 mm. Per-lobe Boolean changed-volume diagnostics remain untrusted and excluded.

Actual-contact gate passes120 sampled poses: maximum cam surface witness gap8.55e-10 mm, lifter gap0, overlap0, and moved-normal gap at least0.099999999 mm. Wrong spin controls separate surfaces by up to3.6176 mm; omitted-rephase controls also separate by up to3.6176 mm. A few omitted-rephase vertices lie inside the wrong solid and return zero distance, so no claim is based on every such vertex being diagnostic. The accepted poses additionally use actual overlap checks and exterior normal controls. Independent section/render gate subsequently passed, as recorded below.

## Integration API and protected scope

`cam_clockwise_candidate.revise_local(local_cam,manifest,phase_sign=-1)` performs the bounded source construction; `phase_sign=+1` is replay only. Its input/output origin is the shaft center at Y=Z=0. Adopt `camshaft-local.step` and `camshaft-local.glb` as definition-local assets only after review, preserving stable `camshaft` occurrence ID under the corrected cam group. Existing world candidate `camshaft.step` is placed at `(0,*AXIS)` and is intended for diagnostics; do not apply that translation twice. Use `engine_clockwise_pose_candidate.cam_frame(q,axial)` only on the world-placed candidate, or local parent translation/rotation equivalent on local assets.

`effective_event(q,axial)=q+2degrees(K*axial)` and `state(q,cylinder,kind,axial)` retain the exact inclined source-length linkage solver and all nominal lift residuals. `tangent(...)` shifts to the opposite side of the centered flat lifter. `linkage_frames(manifest,q,axial)` returns only lifter, valve/retainer/keeper, rocker, pushrod and stationary pedestal hardware frames. It intentionally omits inherited crank/cam general frames and spring geometry: use the corrected rigid-group helper and separately checked compressed-spring geometry. No copied old general poses may leak into the integration. All keyed cam members must share one corrected rigid parent; keeping an old cam group and adding this transform would double rotation.

The source's existing shaft-end, journal, retention and crossed-drive features remain physically unchanged outside the lobe masks. This is preservation, not proof of the crossed-drive's new operating hand. Distributor remains clockwise from its cap and requires a separate compatible drive solution. Root's separately regenerated crank is needed for the preserved firing order; this candidate does not replace the earlier old-crank failure report or establish whole-engine combined motion.

Environment: macOS15.6.1 arm64, Python3.13.12, build123d0.10.0, cadquery-ocp7.8.1.1.post1. The plotting host has NumPy/SciPy/Matplotlib/Trimesh; no Shapely installation is required. The independent boundary metric uses nearest-vertex-adjacent segment distances as a conservative upper bound for each sampled point's nearest-boundary distance, in both directions; it is explicitly a4096-point check rather than a continuous Hausdorff certificate. Model/effort/usage unavailable.

The separate practical API checker `scripts/check-cam-clockwise-linkage.py` binds `cam-clockwise-candidate-linkage-validation.json`. Eight angle/axial combinations return216 intended linkage frames each; comparison with the frozen inclined law at the analytically equivalent event angle differs by at most3.5e-18 in transformation matrix entries. Legacy crank/cam frames and valve-spring shape placements are absent. Internal lifter springs remain rigid lifter members, as before; this does not model their internal dynamics.

## Quality gates and review

| Gate | Scoped result |
|---|---|
| Application / evidence | Inherits qualified replacement profile and rotation evidence; no factory cam calibration claim. |
| Dimensions / coordinates | PASS explicit local/world frames, original width/profile/stations retained. |
| CAD / export | PASS valid one-solid STEP, roundtrip and watertight positive mesh. |
| Source / visual comparison | Actual source-replay and phase-only BRep sections plus native exported mesh image; root review pending. |
| Interfaces | PASS declared shaft/core preservation and sampled lifter contact; crossed drive compatibility OPEN. |
| Motion / disassembly | PASS120 sampled contacts and practical linkage API replay; continuous all-neighbor motion/removal NOT RUN. |
| Learning / diagnostics | Rejected Boolean probes retained; sign/rephase/normal/shaft-notch controls documented. |
| Browser | NOT RUN, uninstalled. |
| Reproduction / review | Four reports and transitive sources bound by `scripts/check-cam-clockwise-delivery.py`; independent root acceptance pending. |

Root owns adoption of definition/occurrence files and combined motion. No canonical file or frozen failure was overwritten. Issue #32 remains open. New source and reports may be preserved as a bounded candidate; they do not authorize production or whole-engine acceptance. After final image inspection, run `python3 scripts/check-cam-clockwise-delivery.py` to verify exact report/artifact hashes and unchanged transitive dependencies from baseline `dafb817`. This includes explicitly checking dependencies omitted from the original build watch against that baseline. Final export distribution follows the project's candidate-artifact policy; no release was published by this worker.

## Final review evidence

All12 independent actual BRep sections pass. Maximum sampled replay boundary error4.46e-6 mm; maximum revised-versus-rigidly-rotated-original error4.65e-6 mm; area difference2.27e-6 mm². All1,728 strict core material points pass; wrong-phase boundary control differs6.2738 mm. These independent results establish the intended local phase revision without relying on the rejected per-lobe Boolean volume figures.

Actual render inspected: `cad/engine/generated/cam-clockwise-candidate/cam-clockwise-review.png` from owned `scripts/render-cam-clockwise-candidate.py` shows the exported mesh and source/revised BRep section. Corrected and prior correctly driven lobes touch the same lifter plane on opposite sides; the unrephased wrong-spin outline misses that contact. The original combined render is also retained. All local gates are complete; parent/root source/render review and full integration remain open. No process remains after final render/check completion.
