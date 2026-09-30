# Component contract and handoff: timing gear backlash candidate

## Contract

- Issue #32 under #1; assigned issue and root diagnostic/ledger/report read. Worker owns isolated study; root is integration owner.
- Baseline commit `705c4683c199d8c5e28addba018bc8d1bdd399b1`, branch `engine/timing-core-pan-joint`. Root may install the unrelated rear neck concurrently; this task binds its actual timing inputs rather than rewriting canonical state.
- Own NEW `cad/engine/timing_gear_backlash_candidate.py`, `scripts/check-timing-gear-backlash-candidate.py`, `scripts/render-timing-gear-backlash-candidate.py`, `scripts/rebind-timing-gear-backlash-ledger.py`, `inventory/engine/timing-gear-backlash-candidate-validation.json`, this handoff and ignored `cad/engine/generated/timing-gear-backlash-candidate/`. No old modules/reports, shared files or canonical writes.
- Scope: change each gear's circumferential tooth thinning from 0.12 mm to **0.0381 mm**, nominal pair midpoint clearance **0.0762 mm**. Preserve 58/29 teeth, source-comparison tip diameters, 14 mm width, estimated axes/phase, hubs, bores, keys, marks and accepted estimated cam thrust land.
- Generator reuse: isolated function-global dictionary with copied parameters; never mutate imported base module globals. Apply frozen refinement and thrust-land functions. Bind original sources, refined/core/thrust proofs and baseline assets by SHA-256.
- CAD frame: X axial; local gears centered X=0, crank YZ=(0,0), cam YZ=(95.1098209901611,76.08785679212888); engine gear station X=385.259375. Preserve existing registration.
- Exact-year source service range 0.0508–0.1016 mm; dial-indicator radius/direction are unspecified. Pitch-circle interpretation is an explicit assumption, not a calibrated factory acceptance.
- Acceptance: prove changed material confined to tooth rings and existing interior geometry equal; valid single-solid STEP roundtrip and clean watertight mesh, bounds <=0.15 mm; two-sided free/contact CAD brackets with overlap threshold 1e-5 mm³, positive free gap >1e-6 mm; 25 rotations over one tooth period. Retain failed fixed-phase axial witness. Verify actual generator helix sign and coupled cam phase theta=k*delta, k=-tan(25°)/81.2 rad/mm, both axial endpoints; only claim interpolation bounds if analytically justified by geometry. No whole continuous rotation, loaded dynamics or service calibration claim.
- Critical negative controls: contact on both flanks, fixed-phase axial shift -0.1 mm, opposite helical compensation sign, changed hub/mark or core region sensitivity. No threshold reduction to pass.
- Current neighbors: frozen paired gears and accepted timing-core/thrust interfaces. Unchanged cores may inherit explicitly hash-bound proofs; altered gear engagement cannot inherit old sweep. Coupled rotation also changes core pose and must not be claimed as a whole-core dynamic proof.

## Delivery status

Contract recorded before construction. Candidate/export, two-sided play, full finite coupled sweep and actual render pass within the stated scope. Fixed-phase axial motion fails and is retained. Final input stability caught an additive ledger change; the explicit metadata rebind below preserves that failure and validates the completed witnesses. Learning/browser N/A for an isolated uninstalled study; no accepted engine installation claim. Source originals/composites remain ignored. Usage/effort and billing unavailable. Exact commands, hashes and findings will be appended.

## Axial coupling and integration boundary

The fixed-phase cam shift of -0.1 mm is a rejected hypothesis: the new tooth clearance permits interference. The opposite compensation sign is also intentionally retained as a failed witness. The actual generator's correct correction is +0.0329032768° for that shift, with k=-0.00574270515 rad/mm.

This phase compensation requires the **keyed camshaft, key, spacer and gear/retaining bolt assembly to rotate together**. It must never be implemented as the gear slipping on its key. Existing thrust-land/core proofs at fixed phase do not certify rotated non-axisymmetric neighbors or valve linkage coupling. Future integration must account for the cam/gear/key/retention phase relationship, lobe-to-follower/valve linkage effects, distributor/pump drive coupling and any non-axisymmetric nearby features. This isolated tooth study does not expand into those whole-engine checks.

For a cam profile generated with hand=-1, local helical cross-section phase is k*x. Translation by delta changes it to k*(x-delta); rigid rotation by k*delta restores the original cross-section at world X. With crank X span [-7,7] and cam span [-7+delta,7+delta], their overlapping slab is a subset of the neutral slab for delta in [-0.1,0]. Thus the specified screw construction gives an analytic no-intersection argument for every axial position **at each checked rotation**; numerical endpoint checks independently verify sign and geometry. This does not certify continuous rotation, loaded behavior or production manufacturing tolerances.

The cropped engagement region contains the full possible intersection lens: in the centerline coordinate u, any common point of the tip cylinders must satisfy 121.8-83.947=37.853 <= u <= 43.18 mm. Its transverse extent is at most sqrt(43.18²-37.853²) < 22 mm; the box covers u=[33.6,47.6], transverse ±22 and axial ±8.2 mm. Whole gears remain inside their tip cylinders and axial widths by build checks. Unchanged crank core R36.6 and cam core R77.2 are outside the mate's tip cylinder by 1.253 mm and 1.42 mm respectively, so the tooth-pair intersection argument does not omit core material that could meet the mate.

The coupled law describes one feasible unloaded path that keeps the ideal helical tooth sections aligned. It is not a prediction that an operating engine must follow that exact centered-clearance path: flank load, contact, elastic response and axial forcing are outside this model. Geometry preservation of the keyed interfaces does not authorize independent rotation of the gear relative to those interfaces.

## Reproduction

From repository root, with restored frozen timing assets:

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-timing-gear-backlash-candidate.py --build
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-timing-gear-backlash-candidate.py --motion
PYTHONPATH=.venv-cad/lib/python3.13/site-packages MPLCONFIGDIR=cad/engine/generated/timing-gear-backlash-candidate/mpl python3 scripts/render-timing-gear-backlash-candidate.py
```

The build verifies the service/review capture hashes and frozen thrust-land gear hashes, then writes isolated local-frame `crank.step`, `cam.step` and corresponding GLBs. The motion stage refuses changed build inputs. The render reads those actual exported meshes, places the cam at the preserved estimated axis, and compares them with the retained Elgin replacement photograph. The local source-comparison composite is not distributable. Use the repository CAD artifact policy for restoring input STEP files; no personal paths or credentials are needed by these commands.

Environment: locked CAD Python 3.13, build123d 0.10.0, cadquery-ocp 7.8.1.1.post1, trimesh 4.7.4; rendering uses local matplotlib with the CAD trimesh package on PYTHONPATH. No dependency updates. Parametric API: `timing_gear_backlash_candidate.parts()` returns local `crank`/`cam` solids; `posed(parts, crank_degrees=0, axial_mm=0, coupled=True)` creates a study pose without modifying inputs.

## Evidence ledger

| Feature | Evidence class | Basis / limitation |
|---|---|---|
| 0.0508–0.1016 mm service backlash | Exact-year service evidence | Retained Ford timing procedure, source hash in `timing-gear-backlash-review.json`; indicator radius/direction omitted |
| 0.0762 mm nominal pair play | Inferred modeling target | Requested arithmetic midpoint, not a manufacturing specification |
| 0.0381 mm thinning per gear | Parameter interpretation | Two contributions add; frozen generator subtracts this total circumferential thickness from each tooth |
| 58/29 teeth and tip envelopes | Replacement comparison | Frozen PBM/Elgin comparison study; no owner-installed identity claim |
| Module, pressure angle, helix, axis registration, shoulders and marks | Estimated | Preserved from the prior isolated study; not made factory-exact by a backlash fit |
| Rear thrust land | Estimated accepted study | Geometry preserved exactly inside cam R77.2; no new backside source claim |

The actual render visibly retains the prior estimated web recesses, holes, keys/marks and rear land. The replacement photograph has different lighting, materials and camera pose, so it is not a dimensional overlay. The contact detail is the true exported mesh with no clearance exaggeration; CAD contact checks, rather than image pixels, establish the free-play brackets.

## Completed checks and explicit ledger rebind

The build completed successfully. The motion run completed all eight two-sided contact measurements, three axial sign/failure witnesses and all 50 sweep rows, then **failed its final stability assertion** because root added `crank_key_followup` to the reference ledger during the run. It did not exit successfully and is not described as having done so.

Removing **only** `crank_key_followup` and serializing with `json.dumps(..., indent=2) + '\n'` exactly reproduces the captured original bytes and SHA-256. The addition concerns a separate unresolved crank key; the original backlash facts, source hashes and interpretation are unchanged. All other bound inputs and target STEP/GLB hashes were verified unchanged. No geometry rerun was needed or claimed.

`scripts/rebind-timing-gear-backlash-ledger.py` implements this single explicit case. It requires the exact original hash, preserves both ledger hashes and the failed-run log, revalidates all numerical witnesses and export/render bindings, and writes the final report. It does not generally waive a changed-source guard.

- Original ledger: `58c9cfbc225a5b576993a94c6ff233a69b33284a8b85ac567b347722cb794419`.
- Additive current ledger: `08116d1484e0832b1882168fb48f8458b57bcb269df7a564af9c3dcb5232f90f`.
- Final report: `inventory/engine/timing-gear-backlash-candidate-validation.json`, SHA-256 `0a4023d5eb2d609fa122c797dcb9af2b3fb0dcec714f013d57eff9789576a5eb`.
- Historical witnesses and original reconstructed ledger are under the ignored candidate directory. Rebind command: `python3 scripts/rebind-timing-gear-backlash-ledger.py`. A fresh clean build/motion run uses the current ledger normally and does not require this historical-case rebind.

| Gate | Result and scope |
|---|---|
| Application | Exact-year range retained; factory indicator setup still unresolved |
| Parameters/coordinates | PASS copied parameters, unchanged imported base globals, 58/29 count, tip envelopes, width and axes preserved |
| Protected core | PASS zero symmetric difference inside crank R36.6 and cam R77.2; no material outside original tip/axial envelope; changed material confined to tooth rings |
| Core fault sensitivity | PASS removed 0.5 mm-radius land sphere detected as 0.523599 mm³ |
| CAD/export | PASS both valid single solids, watertight meshes, no duplicate/degenerate faces; crank bounds error 0.012900 mm, cam 0.000229 mm; STEP volume errors below 0.000001 mm³ |
| Two-sided play | PASS bounded 0.07086037–0.08503244 mm at both sampled phases, within 0.0508–0.1016 mm under the explicit pitch-circle interpretation. Each sign has positive-gap free and positive-overlap contact witnesses |
| Fixed-phase axial shift | **FAIL retained:** -0.1 mm cam shift gives 0.03339618 mm³ overlap at reference phase |
| Wrong sign | **FAIL retained:** -0.03290328° correction gives 1.33394056 mm³ overlap |
| Correct sign | PASS +0.03290328° at -0.1 mm; reference local gap 0.03284101 mm, zero overlap |
| Full sampled period | PASS 25 crank angles across 360/29 degrees, each at axial 0 and -0.1 mm using coupled phase; all 50 overlaps zero, minimum sampled local gap 0.03282866 mm |
| Axial interpolation | Construction-level analytic argument at those 25 rotations, as above; no continuous rotational or loaded dynamics certificate |
| Visual comparison | PASS actual exported front/back/contact render viewed; source comparison remains qualitative and replacement-only |
| Core/valvetrain integration | NOT RUN coupled rotation against non-axisymmetric neighbors and linked mechanisms; prior fixed-phase proofs are not a substitute |
| Learning/browser | N/A isolated uninstalled study; no browser or accepted installation claim |
| Reproduction | PASS scoped evidence plus explicit additive metadata rebind; failed original final guard preserved |

### Assets

| File in isolated candidate directory | SHA-256 |
|---|---|
| `crank.step` | `533208c5f28da3500021a1e8431aba26f1cd8f0b0e886a768a03041263c0e4a4` |
| `cam.step` | `78df586a13fa6d0a18dc10c8628e8a02900468fb33da94b147f9b7abb3b0a0be` |
| `crank.glb` | `f435281f938a9a4c9e299f89c14d1c9ef58688aff76750f0e112911c54eb216c` |
| `cam.glb` | `07fd302629f47b033ff03b02ef19b8ba22299f9a60af8e4d2445814e13e16d90` |
| Local `source-comparison.png` | `8b47b438349a883fa9fb4014615f1073c62ae882345f558cb72166b4a5c2fb6a` |

The crank mesh has 6,864 triangles and cam mesh 10,380. The source composite is excluded from Git/releases. Old timing modules and reports are unchanged. Next action is coordinator review and a separate coupled keyed-core/linkage contract before any installation; #32 remains open. No process remains running. No canonical/shared edits were made by this worker.
