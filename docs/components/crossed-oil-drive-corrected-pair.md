# Component handoff: estimated corrected crossed oil-drive pair

## Contract

- Issues #32/#34; root is system lead, integration owner and sole owner of shared transforms. Contributor: pan_access_resume.
- Contract recorded before CAD in `crossed-oil-drive-corrected-pair-contract.md`. Creation baseline `dafb8175e4e7b328d2a16bdc47914307f044b0c8`; delivery branch `engine/timing-drive-fit`, merged checkpoint `26d0fdc4e7cdd3de0c621309499d1535d8c5131e`. Canonical manifest SHA-256 `91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6`, unchanged.
- Candidate pair only; no full camshaft, occurrence, builder, inventory or installed transform edits. Owned paths are `crossed_oil_drive_corrected_pair.py`, scripts/reports beginning `crossed-oil-drive`, this contract/handoff and corresponding generated folders.
- Millimeters. Cam local axis +X, distributor local axis +Z, gear face centered at local zero. World cam frame is `Pos(227.584,95.1098209901611,76.08785679212888)`; distributor frame is `Pos(0,5.1098209901611,4.08785679212888)*oil_drive_layout.GEAR_FRAME`. Existing parent/IDs/explode remain unchanged because nothing is installed.
- Preserve 16 teeth, pitch radius18, face width12, original profile, cam phase2.5°, distributor phase11.25°, centerlines and connection surfaces. Change both generated tooth twists from negative to positive. No phase tuning was needed.
- Analytic tangent derivation and original bad-pose witnesses are in `crossed-oil-drive-direction-study.md`: positive lead requires opposite signed rates. These are physical local-axis signs, not a whole-mechanism time reversal.

## Evidence ledger

| Feature | Value/datum | Class | Evidence and limits |
|---|---|---|---|
| Physical rotation direction | cam +q/2 about +X; distributor −q/2 about local +Z | sourced direction, inferred transfer to candidate frames | `engine-rotation-convention-research.md`; root owns frame implementation |
| Gear geometry | 16 teeth, R18 pitch, width12, original involute approximation and tooth thinning | estimate | `oil_drive_layout.py`; no factory tooth-count, hand, lead or backlash identification |
| Corrected lead | +1/18 rad/mm both local axial coordinates | inferred functional correction | pitch tangent derivation, actual STEP edge fits and sampled pair fit |
| Connections | distributor R6.05 bore, R9 collar, R1.55 crosspin; cam R15 shaft core | retained model geometry | exact actual-old/new material guards; not factory measurements |
| Backlash | contact onset between .75° and1° each direction at rest | modeled clearance bracket | actual CAD separated at ±.75°, overlapping at ±1°; not production specification |

## Delivery

Readiness: **candidate, not installed**. Parametric API: `crossed_oil_drive_corrected_pair.pair()` returns `(cam_local, distributor_local)`; `tooth_blank(phase=0)` generates the positive-lead blank. Actual exported files are in `cad/engine/generated/crossed-oil-drive-corrected-pair/`:

- `cam-drive-gear-local.step`: `a8c0288344579f739983e3b7a29858c4806f364351917be11b3cf82bf5b23b29`
- `distributor-drive-gear-local.step`: `b875ee0a6669664c9d3246c175e188c3db561334e42ffc5d9aee937bc60b08f8`
- Matching GLBs and actual exported-mesh `corrected-pair-review.png`. Render hash `a8899732c7f1037148c9f287c71c6196861b8162ae1ec8c7484d9fa137b7774f`.

Environment: macOS, Python3.13/build123d0.10 in `.venv-cad`, numpy/trimesh; system Python supplies matplotlib for rendering. No installs. Model/effort and billing unavailable. Artifact publication belongs to root; release URL pending. All required evidence is repository-relative, no temporary or personal data dependency.

Commands from repository root:

```
.venv-cad/bin/python scripts/check-crossed-oil-drive-corrected-pair.py
.venv-cad/bin/python scripts/check-crossed-oil-drive-backlash.py
.venv-cad/bin/python scripts/check-crossed-oil-drive-connection-lead.py
python3 scripts/render-crossed-oil-drive-corrected-pair.py
```

The main checker resumes seven completed, hash-bound build-time BRep poses and reads the frozen STEP for the other ten. Cache source, STEP and interrupted-log hashes are checked. Its old checker hash corresponds exactly to preserved `checker-before-resume.py` (8d78c577…); it intentionally does not match the resumed checker. This is disclosed mixed provenance, not seventeen newly imported STEP calculations. The source and exported files did not change between these runs. A cache-free source-build/full17-pose reproduction entry is `scripts/reproduce-crossed-oil-drive-corrected-pair.py`; it writes a new `crossed-oil-drive-corrected-pair-reproduction` folder, fails if that folder exists, and has passed syntax validation only. It was not run as a redundant second full sweep.

The rejected initial transcription used an incorrect root endpoint. `rejected-profile-preflight/` retains that source, partial exports, console and reason. Final source restores the original exact endpoint before accepted exports. Interrupted slow sweeps and pre-resume checker versions remain in the generated folder. No rejected result was reused as acceptance.

## Validation and review

| Gate | Status | Evidence | Limits |
|---|---|---|---|
| Application/coverage | NOT RUN factory identity | direction research; modeled pair only | actual factory hand/count/lead unknown |
| Dimensions/coordinates | PASS scoped | direction study, unchanged pitch/axes/phases; measured STEP lead | all gear dimensions remain estimates |
| CAD/export | PASS scoped | pair review: valid single solids, watertight GLBs; STEP-based later checks | full-cam union not exported |
| Source/visual comparison | PASS model comparison; NOT RUN factory comparison | actual GLB rest and5.625° views; old/new connection and STEP lead checks | no applicable factory gear image/dimension comparison |
| Installed interfaces | PASS local connections; NOT RUN installed assembly | lead report: old/new distributor guarded material zero change; actual and candidate cam R15 core zero missing volume | fullcam adapter and surrounding block/bearings not checked |
| Motion/disassembly | PASS sampled pair; NOT RUN full motion/disassembly | 17 poses across one22.5° tooth period, ≤1.40625° spacing; zero overlap; gap .167265971754–.170194060635mm | no continuous solid sweep, torque, endplay or loaded contact calculation |
| Learning/diagnostics | NOT RUN | no new lesson | CAD direction witnesses are not educational acceptance |
| Browser integration | NOT RUN | no canonical changes | root integration/browser review required |
| Reproduction/review | PASS bound local evidence; fresh full rebuild NOT RUN | reports bind scripts, source, assets, render and resumed cache; fresh runner syntax checked | publication and root review pending |

Wrong same-sign motion at +5.625° produces114.104962773737mm³ overlap, demonstrating fault sensitivity where tooth-period endpoints alone miss the issue. The frozen original pair under opposite signs produced114.10496281999mm³ at that pose. New ±1° relative-phase perturbations produce .1367832mm³ penetration while ±.75° remain .0124092mm separated. These bracket actual clearance/contact onset; they do not prove a production backlash allowance or force transmission under load.

`inventory/engine/crossed-oil-drive-connection-lead-review.json` measures304 helical edges per exported STEP, each sampled17 times: slopes .05555555101055–.05555555101062rad/mm, within1e−6 of+1/18. Inner distributor material and collar guard added/removed volumes are zero. Existing cam sections immediately outside the gear are R15, and both actual/candidate R15×12 cores have zero missing volume.

Self-review inspected the actual exported-mesh render; root review pending. Code may be preserved as a bounded candidate. Installed acceptance remains open. Existing shaft branch translation, ratios and connected drive fit are documented separately in the direction study; no pump-flow inference.

## Tracking and restart

Issues remain open. Root's next decision is review of the pair render and permission to integrate only gear tooth material into the separately rephased camshaft, preserving R15 core and every out-of-window surface. Face window is X221.584..233.584. Distributor candidate remains gear-centered; original part frame requires translating localZ−85 when serializing into the old definition frame. Root must reconcile that conversion explicitly.

Cam axial travel changes tooth phase relative to a fixed distributor; the existing cam axial-phase function does not by itself prove crossed-drive compatibility. Endplay coupling, surrounding neighbors, full combined motion and production dimensions remain open dependencies. No running process. Usage unavailable.
