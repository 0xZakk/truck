# Component handoff: coordinated pump/cover candidate

## Contract

- Issue engine#47, coordinated#32, parent#1. Contributor `resume_pump_fit`; integration owner root. Root alone owns Git/shared manifest/builder/viewer changes.
- Resume baseline `5584306a595f87b60b29eca9ea82b527ade5ae98`, branch `engine/resume-integrations-20261003`. Canonical manifest SHA256 `91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6`; actualv4 manifest `9da33ca507e31cf6d906d4ee2c92b87a64ba01db7abea8f14b72f244631f9fe9`.
- Scope candidate repair, diagnosis and source-registration amendment. Not installed. Own `pump-cover-candidate-20261003*` scripts/reports/docs and `cad/engine/pump_cover_candidate_20261003*.py`; root additionally assigned new KB prefix `pump-deck-height-20261003`. Preserve all failed trials and frozen spring.
- Exact original numerical contract remains `pump-cover-candidate-20261003-contract.md`. Worldmm,+Xenginefront; optionBpumpYZ(−22.156967,193.467476),clock−5.641351deg; blockface373,pumpgasket373..375,casting375,seats389,hub473.43. Hardware/internals rigid, not scaled. Source gasket footprint1.061626 relative to old estimate.
- Inputs, neighboring IDs and acceptance scope are unchanged from that contract. New held-out deck evidence invalidates installed-pose acceptance. Root approved numeric source review only, not coupled scale/pose CAD.

## Evidence ledger

| Claim | Value and datum | Class | Evidence | Limits |
|---|---|---|---|---|
| Ford300 nominal deck | 10.000in=254mm above crank axis | Manufacturer nominal family reference | Ford PDFpage1, `kb/sources/pump-deck-height-20261003-ford-nominal.md`, hash recorded |1965–96 family; no production tolerance or owner measurement |
| Candidate fourth pump screw | Z260.259199758mm | Inferred source registration | Original datum report/contract |Above fixed deck; installed conflict |
| New block positive feature reach | Z279.711101mm | Constructed candidate dimension | Current exported block/difference reports |Crosses head joint; must not be carved to neighbors |
| ATK head/block seam | Pixel picks and mapped meanZ289.84487 | Inferred, held-out photo comparison | `*-deck-registration.json` |Coplanarity/depth/camera systematic unknown; not measured deck height |
| Conditional footprint scale |0.88602454relativeoptionB,Zshift−2.809667 | Sensitivity hypothesis only | Same report; root explicitly disallowed automatic adoption |Inheritedpan−24.5 unverified;−7.2126mm sampled cam envelope margin |
| Carter pump height |98.43mm casting face to hub seat | Replacement comparison | Frozen functional/registration ledgers |Does not calibrate transverse photo |

## Delivery

- Readiness: **candidate FAIL; not integration-ready**. No new coupled CAD, installed transforms, shared geometry or spring changed during resume.
- Parametric API: `pump_cover_candidate_20261003.pump_parts()` returns part/region mappings; `block_parts()` returns block/feature mappings. Existing build uses `scripts/pump-cover-candidate-20261003-build.py`, followed by the dedicated check/export scripts. Do not rebuild the entire engine.
- Generated assets: `cad/engine/generated/pump-cover-candidate-20261003/`; current59parts/58non-spring meshes. Release publication and whitelist belong to root. Candidate raw source overlay `deck-source-overlay.png` **must be excluded** from any archive.
- Actual visuals: `reference/engine/pump-cover-candidate-20261003-review.png`, `*-source-compare.png`, and new `*-deck-registration.png`. Inspected actual source and actual STEP-derived surfaces. Source originals excluded; optional local overlay regenerates only when the hash-matched ATK image exists.
- New commands: `python3 scripts/pump-cover-candidate-20261003-deck-registration.py`; `python3 scripts/pump-cover-candidate-20261003-resume-audit.py`; `.venv-cad/bin/python scripts/pump-cover-candidate-20261003-inlet-repair-study.py`; `.venv-cad/bin/python scripts/pump-cover-candidate-20261003-inlet-analytic-study.py`.
- Environment: existing macOSCADvenv Python3.13/build123d0.10/OCP7.8.1.1; systemNumPy/Matplotlib for source plot. Ford PDF ingestion required bundled artifact Python because system pypdf absent. No dependency pins changed. Model/effort/usage unavailable.

## Validation and review

`*-resume-audit.json` hashes the current build, source reports and generated inputs. All nine checked report groups match current inputs; hashing is not a rerun of CAD. The unchanged failures are current, not historical-only.

| Gate | Status | Evidence and coverage | Limits |
|---|---|---|---|
| Application/coverage | FAIL/open | Ford nominal family reference and Carter/ATK replacement ledgers |Exactinstalled pump, fifth-aperture function and full water jacket unknown |
| Dimensions/coordinates | FAIL | New deck registration report; screw4 above nominal deck |No accepted new source frame |
| CAD/export integrity | PASS scoped |58/58non-spring meshes watertight and winding consistent; maximumCADbounds error0.001030mm<0.025 |Analytic spring is separately qualified illustration; shape integrity does not prove flow or fidelity |
| Source/visual comparison | FAIL | Actual source comparison and new actualmesh/landmark figure |Arm too narrow/short; casting tower/ribs incomplete |
| Installed interfaces | FAIL |788fresh nominal pairs,14conflicts,0errors;48tooltests,4conflicts; independent face/boss/seat checks current |Head/gasket/outlet/carrier conflicts; inlet probe16.243315mm³ obstruction |
| Motion/disassembly | FAIL/NOT RUN |Actualimpeller outside exact envelope0; guard checks0; bad double-transform control detected25.448mm error; fourtoolcorridors fail |Full continuous coupled motion, belt/fan and hose interactions NOT RUN |
| Learning/diagnostics | PASS scoped evidence update |New source→atomic deck note; existing candidate limits retained |No new installed learning claims; root owns shared semantic index |
| Browser integration | NOT RUN |Candidate intentionally absent from canonical viewer |Required before installed acceptance |
| Reproduction/review | PASS scoped research |Scripts, hashes, reports, source URLs and visuals preserved; root independently reviewed seam and manufacturer reference |Full candidate export environment/artifact publication still root-owned; local CAD failures remain |

The blockdelta reports show old overlaps0 and new overlaps10,904.370mm³(head),1,034.479mm³(headgasket),26.943765mm³(thermostatframe). Source-datum conflict, rather than a local meshing error, causes those failures. Root reviewed seam identity as plausible and refused using inherited pan height as sole additional scale anchor. See `pump-cover-candidate-20261003-deck-amendment.md` for the exact research remedy and rejected sources.

Inlet diagnostics are separate: reconstructing the declared firstspan and applying a1e−6mm fuzzycut leave16.243315mm³ probe intersection while broad housing/lumen intersection reports0. This inconsistency remains explicit. No new shape is accepted from a successful export or smaller residual. The independent analytical-axis report records the follow-up experiment; any candidate repair requires source-module implementation, full protected-region, mesh, flow and affected-neighbor reruns.

## Tracking and restart

Issue#47 stays open; no Done or installed promotion. No shared writes. Root owns publication, issue update and semantic/backlink index integration. A direct issue read was initially blocked by sandbox network; assignment scope came from root.

Next: independently establish coplanar crank/seal datum or dimensioned mounting pattern, then propose a coordinated numeric frame with Ford254mmdeck. Do not use the forward gear hubs or the conditional0.886scale as accepted calibration. Continue the isolated analytical inlet diagnosis if its result justifies a native lumen correction; preserve failed reports. Run `python3 scripts/pump-cover-candidate-20261003-resume-audit.py` before resuming from any later checkout. Exact study results are retained in their JSON/logs; final process state is confirmed below.


## Isolated local inlet successor

The independent analytical-axis experiment confirms a real obstruction: R1cylinder on the declared first-span centerline intersects15.686388mm³ of original housing. An R5cylinder on exactly the same span, derived only from the original inlet profile centers, removes378.591311mm³ and adds0. It leaves one valid solid. It is an illustrative local channel, not a newly measured production passage or change to inlet exterior proportions.

All original protected-region checks on this separate successor pass: complete seal face/backing, four full drybosses/bores/seats, actual screw seats, rotor/guard, heater/fifth passages and axial bore remain intact. Both original loft flowprobe and independent analyticR1probe are clear. `*-inlet-analytic-check.json` preserves exact inputs. The mesh is one finite watertight component with consistent winding and maximumCADbounds error0.000027722mm under the unchanged0.025mm gate (`*-inlet-analytic-mesh.json`).

The broad original housing/declared-lumen Boolean still reports0 despite the analytical-axis obstruction. Measuring analyticaltube minus declared loft fails adaptive volume convergence at0.00400937; this is explicitly INCONCLUSIVE, not accepted by loosening the threshold. Therefore the broad loft containment claim is not promoted. The separate actual meshsection visual shows the local opening; `*-inlet-analytic-review.png` and `*-inlet-analytic-render.json` record it.

The original59part build remains frozen. The local successor is `cad/engine/generated/pump-cover-candidate-20261003/housing-inlet-analytic-diagnostic.step` and itsGLB, with reproducible script `scripts/pump-cover-candidate-20261003-inlet-analytic-study.py`. It is suitable for review as a scoped flow remedy, never as installed acceptance. No new full788pair neighbor claim is made. The pure subtractive delta and unchanged exterior pose do not resolve the14existing clashes, the wrong jointframe, broad source-shape mismatch or coupled motion/browser gaps.

To reproduce the mesh visual, run `.venv-cad/bin/python scripts/pump-cover-candidate-20261003-inlet-analytic-render.py --prepare`, then `python3 scripts/pump-cover-candidate-20261003-inlet-analytic-render.py`. Preparation uses pinned CAD/trimesh environment; rendering uses systemNumPy/Matplotlib. This keeps the environment lock unchanged.


## Independent integration-owner review

Root separately inspected the actual inlet review image, analytic study source and study/check/mesh reports on2026-10-03. Root accepts this **separate local flow successor as candidate progress**:0addedstock,378.591311mm³removed, clear sampled flow paths, preserved named regions and0.000027722mm meshbounds error. This does not accept full passage hydraulic crosssection, factory R5dimension, coupled sourceframe or installed component. The tube-minus-loft adaptive-volume result stays INCONCLUSIVE.

Root integrated the Ford deck source/note into shared KB map/crosslinks and regenerated embeddings391notes; worker did not edit the shared index. Focused Python syntax and prefixedKBlinks checks pass. All local successor check/mesh/render input hashes were independently re-read and match. The diagnosticSTEP is open in CADViewer; the worker reviewed its actualGLB render and section. No modeling/check processes remain at final checkpoint.

`reference/engine/pump-cover-candidate-20261003-resume-package.json` is the release-ready file/hash ledger. It identifies authored files, generated artifacts, external existing dependencies and the exact source-overlay exclusion. Independent root38inputhash auditPASS is `reference/engine/pump-cover-candidate-20261003-root-inlet-review.json` and is included. Root handles the archive, release and GitHub issue update. The manifest is regenerated with `python3 scripts/pump-cover-candidate-20261003-resume-package.py` after any final authored edits.
