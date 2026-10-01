# Component handoff: clockwise engine pose candidate

## Contract before implementation

Issue #32; integration owner root. Baseline `9ab3c575`, branch `engine/timing-pan-seal-joints`. Own only this new handoff, `cad/engine/engine_clockwise_pose_candidate.py`, `scripts/check-engine-clockwise-pose-candidate.py`, and `inventory/engine/engine-clockwise-pose-candidate-validation.json`. No shared viewer, assembly helper, frozen studies or geometry changes. Candidate helper and read-only actual STEP diagnostics, not installation.

Use CAD millimeters, +X front, +Z up; preserve positive event time and source-supported firing order 1-5-3-6-2-4. The frozen rotation-convention proposal supplies direction evidence. Preserve current 58/29 exported gear profiles, estimated shaft centers (121.8 mm separation), axial datum, helical sign and existing backlash contract. Test clockwise crank (-q about +X) and counterclockwise cam (+q/2 plus unchanged axial helix correction). Existing crank export has legacy rest throw phases; it cannot silently become the rephased crank required by the proposed firing order. Detect and report that incompatibility with actual geometric witnesses rather than reflecting or rebuilding it.

Inputs: current manifest, exported crankshaft/rod/piston geometry, backlash candidate gears and frozen validation report, existing coupled-core constants and rotation proposal. Planned command: `.venv-cad/bin/python scripts/check-engine-clockwise-pose-candidate.py`. Gear check initially samples 13 poses across one negative crank tooth period at two axial endpoints; preserve overlap <1e-5 mm³ and gap >1e-6 mm from frozen checker. Critical controls: wrong cam sign, wrong axial compensation, duplicated gear phase; actual crank-journal location and rod/piston bore center extraction, linkage closure, legacy-versus-required rest phase, double phase. Expand only if unresolved evidence requires it. Continuous claims limited to exact signed-pose equivalence and frozen helical axial construction; finite gear samples do not prove continuous angular engagement. Crossed distributor/oil drive handedness, revised crank/cam exports, neighbors and browser remain open.

## Evidence and acceptance scope

The gear pair remains a replacement-comparison teaching candidate with estimated profile, helix, axis and phase; no dimensional refinement is authorized. Pose helper must distinguish already-phased geometry from event/rest phases. Separate APIs expose old-geometry diagnostic poses and required rephased geometry poses, with explicit phase contract. All input bytes will be bound in the report. No new mesh/export is planned: CAD/export integrity is read-only input validation, not new shape acceptance. Browser, removal and installed neighbors NOT RUN. Learning and source comparison inherit the frozen rotation handoff by hash; no new factory or lip-pumping claims.

## Narrow geometry and manifest migration for integration owner

Do not globally replace `full_engine.PHASES`: the same list currently feeds piston/rod event groups, crude legacy cam lobes and manifest event metadata. In `full_engine.rotating()`, keep the first occurrence/group loop at event phases `[0,240,120,120,240,0]`. Introduce a separate `CRANK_REST_PHASES = [(-p)%360 for p in PHASES]` and use it **only** in the second loop that constructs six journal pins and their two cheeks/counterweights. The existing expressions `y=-R*sin(t)`, `z=R*cos(t)` and `Rot(phase,0,0)` then produce physical rest phases `[0,120,240,240,120,0]` without reflecting any solid or changing dimensions. Keep main journals, front nose, rear flange, flywheel interface, pilot-bearing interface and damper key-cut calls unchanged. A future candidate must prove bounded differences around the four changed throws and unchanged end/key surfaces; this helper does not claim that rebuild has happened.

Definition replacement: replace only `crankshaft` with verified rephased geometry at its existing local origin; keep stable occurrence `crankshaft` under `crank-motion` with identity local transform. Change that group's motion to physical `-q`; keep flywheel, damper and crank gear rigid children as appropriate. Their existing local registration is applied once, not mirrored or shifted. `crank-timing-gear` needs the separately selected 29-tooth candidate definition, with local placement `(GEAR_X,0,0)` and no extra phase beyond the exported teeth. The old 24-tooth canonical definition is not validated here.

For each `rod-group-i` and `piston-group-i`, retain station X, stable child IDs and all child local placements. Retain `phase_deg` as event phase only if the integration helper explicitly calls `corrected_slider_frames(q,event_phase,...)`; otherwise migrate to an unambiguous new physical-rest-phase field and compute `-q+rest_phase`. Do not combine a negated phase field with a solver that negates it again. Pass measured new CAD phase to the helper guard; cylinders 2–5 in the preserved old export deliberately fail this guard. Rod caps, both bearing shells, bolts/nuts follow the rod parent; wrist pin/rings follow the piston parent, preserving their existing offsets.

For cam integration use the source-informed candidate lobe generator, not the crude legacy `full_engine` cam loop. Reverse local event-center phases only after a separate candidate proves its lobe/support geometry; preserve source event scheduling and lift-driven upper linkage transforms. Keep `cam-motion` centered on the selected candidate axis and put the keyed gear/shaft/spacer in one rigid frame. The gear helper accepts **local** `crank.step` / `cam.step` exports, so applying it to already-world-placed coupled-core STEP parts would double their translation; use `crank_frame` / `cam_frame` directly for those world-placed parts instead. Distributor remains clockwise from its cap, but its crossed-drive handedness is explicitly unsupported pending a separate geometry correction.

## Delivery and reproduction

Helper APIs: `crank_frame(q)`, `cam_frame(q,axial_mm=0)` transform already world-placed geometry; `gear_frames(q,axial_mm=0)` supplies local exported gear placements; `slider_frames(q,physical_rest_phase,R,L,x)` is an explicit measured-geometry diagnostic; `corrected_slider_frames(q,event_phase,R,L,x,measured_cad_rest_phase_degrees=...)` requires corrected physical CAD phase; `distributor_frame(q)` retains clockwise local shaft motion without certifying its drive mesh. No global state mutation or shape generation occurs.

Environment: macOS 15.6.1 arm64, Python 3.13.12, build123d 0.10.0, cadquery-ocp 7.8.1.1.post1. Reproduce from repository root with `XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-engine-clockwise-pose-candidate.py`; cache directory is optional and not a deliverable dependency. New source passes `py_compile`. Model/usage metrics unavailable. No asset archive is needed because existing byte-bound STEP artifacts are reused; restore them under the frozen studies' artifact instructions. No new mesh or source imagery is distributed.

| Gate | Outcome / scope |
|---|---|
| Application / coverage | PASS bounded candidate direction and phase contract; prior source evidence remains qualified. |
| Dimensions / coordinates | PASS unchanged dimensions and explicit frames; actual cylinder axes read from STEP. |
| CAD / export | Read-only valid STEP inputs; no new geometry/export; mesh checks N/A for unchanged artifacts. |
| Source / visual comparison | Inherited frozen rotation source review; no newly shaped parts. Corrected whole-engine visual NOT RUN. |
| Installed interfaces | FAIL preserved legacy crank under corrected event phases; deliberate guard rejects it. Gear results are scoped below. |
| Motion / disassembly | Sampled gear engagement and actual-axis linkage diagnostic; no loaded dynamics, removal or whole-engine proof. |
| Learning / diagnostics | Explicit wrong-sign, axial and duplicated-phase controls; prior direction lesson unchanged. |
| Browser integration | NOT RUN; isolated helper is uninstalled. |
| Reproduction / review | Inputs bound in new report; parent/root owns independent review and adoption. |

Actual crank axes establish rest phases from geometry, not copied metadata. Old geometry can close under its measured phases but fails the proposed firing registration; these are deliberately separate verdicts. Future rephased crank must receive a new check/report binding, never overwrite this historical failure. The root-owned crank candidate is outside this worker's ownership. Issue remains open pending regenerated crank/cam and drive mesh integration.

## Final bounded result

Gear samples PASS: 26 fresh exact checks (13 event angles, two axial endpoints), zero overlap and minimum gap 0.03282866112968426 mm. All three injected faults produce positive overlap: wrong_cam_sign 592.535352 mm³, wrong_axial_compensation 1.33394056 mm³, duplicated_phase 590.46233 mm³. These remain finite angular samples; unloaded clearance is not loaded contact. Backlash scope is inherited from the byte-identical exported pair and reversed traversal of the same relative phases.

Actual geometry-based linkage checks at 145 poses per cylinder close measured legacy geometry below 7.2e-12 mm, with rod-small-end/piston-pin error below 5.9e-14 mm. Required corrected-firing poses miss preserved journals by up to 87.54824012 mm; duplicated rest phase is detected at the same scale. Cylinders 2–5 are correctly rejected by the corrected-pose guard. The old crank therefore remains FAIL for corrected-firing compatibility, while the bounded helper/gear diagnostic passes. No running process remains. Reviewer: root pending.
