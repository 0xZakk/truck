# Fuel rail coordinated candidate handoff

## Contract

- Issue #82, engine parent #1; integration owner/root handles issue/Git/shared files. Worker `resume_fuel_fit` owns fuel-rail-candidate-20261003 prefixes and existing layout delivery only.
- Resume baseline5584306a595f87b60b29eca9ea82b527ade5ae98, branch engine/resume-integrations-20261003. Canonical manifest SHA25691950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6.
- Candidate scope: both root-approved transverse signs under frozen `fuel-rail-candidate-20261003-amendment.md` and `-groove-repair.md`. No sign selection, installation, shared manifest or canonical export writes.
- Evidence/detail: Ford1994 rail topology; physical1987 comparison only. Exact numerical geometry remains educational estimate. Six injector cups/axes and three rail seats/hardware remain fixed existing-model interfaces. Preserve source intake ear and nine apertures.
- Millimeter engine XYZ; local regulator and coupling transforms exactly as builder `parts(sign)` and frozen amendment. Existing exporter axis convention GLB meters(X,Z,−Y). Explode convention unchanged, new staged removal not yet accepted.
- Neighbors: frozen unequal-port intake candidate plus every canonical occurrence; regulator, coupling, vacuum and diagnostic interfaces coordinated. No source-driven datum revisions authorized by this resume.
- Required local STEP baseline and r2 artifacts available. GitHub issue read attempted, network unavailable; issue context supplied by root/committed contracts.
- Planned gates: actual STEP seated/open and drilled-bypass connectivity, eight inlet probes/blocked control; protected interfaces, STEP/GLB integrity; all changed occurrences versus all authoritative CAD bounds/exact overlapping pairs; actual source/context renders. Historical overlap threshold0.1mm³ remains numerical convention. Critical browser/removal/unknown tooling gaps stay open.

## Evidence ledger

| Claim | Class | Source and limits |
|---|---|---|
| Front regulator, adjacent return and upturned paired rear connectors | Verified application topology | Ford1994 V5855-F; `intake-return-interface-20261003-evidence.json` |
| Physical rail morphology | Replacement/earlier comparison | 1987 specimen; same source ledger; not exact1994 geometry |
| q=.75 and protected spacing, diameters, bends, flange passages | Inferred | `fuel-rail-layout-20261003-contract.md`, approved amendment and r2 parameters; no manufacturer dimensions |
| Groove minor radius.30 | Inferred geometric repair | r2 opens tangent cutter by.05mm; retained seal unchanged; no manufacturing seal specification |
| Valve, diaphragm and screen internals | Illustrative | Existing definitions plus eight perforations; no calibration or production internal claim |

## Delivery

Readiness **candidate**, not integration-ready. `cad/engine/fuel-rail-candidate-20261003.py:parts(sign)` returns definitions, world shapes, poses and metadata. `sign` is +1 or−1. Both variants remain separate under `cad/engine/generated/fuel-rail-candidate-20261003/{plus,minus}`. No selected side.

Commands from repository root, using existing Python3.13/build123d0.10/OCP7.8.1.1 `.venv-cad`:

```sh
.venv-cad/bin/python scripts/fuel-rail-candidate-20261003-build.py
.venv-cad/bin/python scripts/fuel-rail-candidate-20261003-check.py
.venv-cad/bin/python scripts/fuel-rail-candidate-20261003-flow.py
.venv-cad/bin/python scripts/fuel-rail-candidate-20261003-mesh-diagnostic.py
.venv-cad/bin/python scripts/fuel-rail-candidate-20261003-mesh-repair.py
.venv-cad/bin/python scripts/fuel-rail-candidate-20261003-context.py
```

All paths are repository-relative. Large generated artifact release remains root-owned/pending. No source originals redistributed. Exact step inputs/checker hashes live in flow/context reports. Frozen failed builds and flow-attempt logs preserved; `flow-stale-before-resume.json` preserves the untrustworthy prior result (negative volumes), not acceptance. Model/effort/usage unavailable.

## Validation and review

| Gate | Status | Evidence and remaining limits |
|---|---|---|
| Application/coverage | PASS topology; incomplete coverage | Source contracts; all internal construction remains illustrative |
| Dimensions/coordinates | PASS frozen estimated contract | Both signs retained; protected interface comparisons zero symmetric difference in six cups/three lower seat bands. Whole seat/stack acceptance pending |
| CAD/export | In progress | r2 STEP6definitions/sign valid single solids; original supply GLB four collinear open edges. Diagnostic and isolated tessellation repair retain failed mesh |
| Source/visual comparison | NOT RUN fresh exported review | Prior numeric source registration retained, actual context render next |
| Installed interfaces | In progress | Fresh flow and context scripts; no installation approval |
| Motion/disassembly | NOT RUN | No validated removal/tool envelopes; do not invent tool specifications |
| Learning/diagnostics | NOT RUN | Existing learning not updated for new candidate |
| Browser integration | NOT RUN | Candidate not installed; root-owned browser review |
| Reproduction/review | In progress | Repro scripts, retained failures; root review/release pending |

Fresh flow checker avoids invalid OCC union at ideal tangent valve seat: positive-volume graph edges between individually valid seated cavity solids and actual drilled cylinder establish bypass connectivity. It reports the graph explicitly; does not claim exported union geometry valid. Seated/open states use actual STEP subtraction. Eight inlet probes and one blocked-inlet control are separate from overall connectivity. Not a leak/hydraulic/calibration test.

## Tracking and restart

Issue remains open. Do not install/select a sign by clearance. Current context process/log: `scripts/fuel-rail-candidate-20261003-context.py`, `cad/engine/generated/fuel-rail-candidate-20261003/context-resume.log`; live status must be checked, not inferred from this note. Next actions: finish context audit; inspect actual exports/source/context; reconcile collisions and tooling/removal gaps with root before any source-rooted geometry revision. No coupled CAD path changes permitted solely to cure a clash.

## Resume review / approved successor

Fresh r2 context completed42,640pairs per sign with unchanged input guards. Plus5 overlaps, minus18, zero checker errors. The actual exported review `actual-export-context.png` was inspected against Ford1994 V5855-F and physical1987 view1. Front regulator/loop and rear connectors now match topology; broad two-sided rectangular mount tabs visibly disagree with one-sided rounded source ears. No calibrated3D image metric claim. Exact conflict lists remain in each context.json. Tiny0.222mm³ tube/flange interference is elbow surface outside a straight radius4.55 socket atZ377.5…378.085; distinct physical solids, no modeled welded-contact justification, remains FAIL.

Root reviewed `reference/engine/fuel-rail-candidate-20261003-tab-proposal.{json,png}` and approved an isolated r4 candidate: Xhalfwidth9,Y−186…−163,Z364…370,R2 lower corners; preserve16×12 seat, radius7 washer contact, bore and bolt axes. These are inherited/estimated dimensions, not source measurements. No sign selection or path change. `-r2.py` and `-r3.py` preserve earlier builders.

Root also approved r3/r4 vacuum socket: exact straight20mm from(0,−75,460) to(0,−55,460), OD12/ID8.2, upstream+Y tangent and original regulator socket. Fitting/upper port unchanged. Existing end tangent alone caused real material intrusion: center of fitting bore(0,−65,460) lies within r2 hose material. See vacuum-junction-diagnostic.json; neither retention exemption nor modeled hose compression applies. Entire upstream curve remains estimate and its upper-intake clashes may persist.

Current component issues clarified by root: #40rail, #41vacuum, #42regulator, #36intake; #82 is electrical/research cross-reference, parent#1. Rebuild successor only with `scripts/fuel-rail-candidate-20261003-build-r4.py`; dedicated `-check-r4.py`, `-flow-r4.py`, `-context-r4.py` write isolated `generated/fuel-rail-candidate-20261003/r4`. Do not rerun the old generic build into frozen r2 output.

## Final r4 validation checkpoint

**Candidate only; FAIL installation and external pressure enclosure.** Neither sign selected. No process remains running from this worker. Both42,640-pair context audits completed (85,280total), hash guards PASS, no Boolean errors. Plus4overlaps; minus17. Actual r4 render `r4/actual-export-context.png` reviewed: one-sided tabs now match source topology better, fixed vacuum lead visible; educational geometry and context clashes remain obvious. This is actual exported geometry, not a generated concept image. Complete numeric list in each `r4/{plus,minus}/context.json`.

| Gate | Final status | Evidence / limit |
|---|---|---|
| Application/coverage | PASS bounded source topology, incomplete internals | Exact-year Ford image and physical1987 view1 inspected; no exact production dimensions/internal architecture |
| Dimensions/coordinates | PASS approved estimated r4 contract | Full16×12×6 seat volumes and full radius7 washer-contact bands have zero old/new symmetric difference at all three mounts. Bores empty; single fused rail; root material140.654mm³ each; shifted1mm frame detected81.305mm³. `r4/tab-check.json` |
| CAD/export | PARTIAL PASS / FAIL hose mesh | Six changed STEP definitions per sign valid/single solids; rail now natively watertight. Hose STEP valid but wire-sweep GLB has nonmanifold seam at curve/lead. Separate-sweep study and finer.02mm/.05rad tessellation also FAIL; no arbitrary repair/cap accepted. `r4/checks.json`, `r4/vacuum-mesh-refine.json`, `vacuum-seam-study/report.json` |
| Source/visual comparison | PASS review, not factory fidelity | r2/r4 actual export/context renders and source observations; all numeric tab radii/widths/thickness estimates. Source originals excluded |
| Installed interfaces | FAIL | r4 plus4/minus17clashes, including upper intake/hose, lifting eye(+), screws, tube/flange and protected mounts(−). Fixed vacuum fitting overlap eliminated; fresh section probes show open axis. No clash exemptions |
| Regulator local valve topology | PASS bounded control, FAIL enclosure | `r4/flow.json`: seated2positive fluid solids/open1; all8inlets open; blocked-inlet and drilled-bypass controls detected. FiniteR17 test envelope alone does not prove sealing |
| External pressure boundary | FAIL | `r4/pressure-boundary.json`: radius.15mm continuous radial cylinder from pressure regionr8→ambientr21 atZ388.5 intersects zero actual solids, both signs. Lower wall top388/diaphragm underside389.1 leaves open gap; no inferred extension made |
| Motion/disassembly | NOT RUN | Tool sizes, extraction/retention directions and coupling sweep controls remain unresolved; no production tool dimensions invented |
| Learning/diagnostics | NOT RUN new content | Existing regulator description still acknowledges illustrative internals; no new calibration/leak claim |
| Browser integration | NOT RUN | Candidate not installed; integration-owner review required. No alternate-surface workaround for historical browser restriction |
| Reproduction/review | PASS local inputs/commands; external release/root review pending | Authored and generated SHA256 ledger `reference/engine/fuel-rail-candidate-20261003-delivery.json`; report inputs guarded. No shared canonical assets changed. Root owns issue/PR/release |

Additional commands:

```sh
.venv-cad/bin/python scripts/fuel-rail-candidate-20261003-tab-check.py
.venv-cad/bin/python scripts/fuel-rail-candidate-20261003-junction-diagnostic-r4.py
.venv-cad/bin/python scripts/fuel-rail-candidate-20261003-pressure-boundary.py
MPLCONFIGDIR=/private/tmp/fuel-rail-resume-mpl python3 scripts/fuel-rail-candidate-20261003-render-r4.py
```

The render uses system Python NumPy/Matplotlib (CAD runtime has no Matplotlib). Its optional cache directory is disposable, never an input/artifact dependency. Geometry scripts use `.venv-cad`; no environment installations or dependency pin changes. Parsed30owned Python files successfully before final additions; final ledger reruns syntax across all owned Python. Actual model/effort/usage unavailable.

Residual r4 plus overlaps in mm³: hose/upper intake2349.524; rail/front lifting eye542.817; return elbow/flange0.222037; rail/regulator screw3 3.052. Minus retains226.270rail/return intersection at protected mounting side, plus two13.127return/washer overlaps, intake/regulator and hose conflicts. Counts do not select a transverse sign.

Exact next action: root review the r4 reports/actual render and coordinate a source-supported regulator pressure-boundary contract before changing housing/diaphragm geometry; resolve return elbow/socket contact as distinct physical solids, hose native tessellation representation, and remaining source/installed routing. No implicit permission to reroute around the intake, move fixed interfaces, remove source ear, or promote this candidate. A bounded valve-connectivity PASS must never be presented as a sealed regulator PASS.


## r5–r6 preservation checkpoint, 2026-10-03

**Candidate only: installation and complete regulator pressure enclosure still FAIL. Neither transverse sign selected.** Root-approved estimated r5 clamp shell additions retain OD40, all poses and diaphragm. Exact face contacts are lower/diaphragm423.235362mm², upper/diaphragm323.709707mm² and lower/upper25.007078mm², with zero interfering volume. Actual saved section `r5/actual-clamp-section.png` reviewed by worker and root. This is ideal contact, not crimp/preload validation. Full exterior-domain flow preserves vacuum/fuel separation and detects original-shell and pierced-diaphragm negatives; the lower O-ring path remains open to ambient. Valve displacement is topology testing, not an accepted moving mechanism. See `r5/clamp-check.json` and `r5/exterior-flow.json` (actual filenames in package ledger). The inherited central-return seal architecture is now contradicted by service/replacement evidence; r7 research remains a separate unbuilt proposal.

r6 changes only the approved vacuum Bezier control from(80,-90,460) to(0,-115,460), retaining remaining controls, both endpoints, straight socket engagement, OD12/ID8.2 and regulator socket. Maximum corresponding-parameter displacement is28.9665583734mm. This is an illustrative curvature correction, not an OEM route claim. Conservative continuous local radius bounds are7.359403mm plus and6.674681mm minus, greater than outer radius6. Every pair among eight exact Bezier sub-sweeps and the straight lead has zero intersecting volume. The global checker extracts controls from the frozen builder, verifies builder/parameter/STEP hashes and reconstructs the complete outer/bore/socket hose; symmetric difference with the actual saved STEP is0mm³ for each sign. Checker hash is embedded in `r6/hose-global.json`.

Both r6 hose GLBs are watertight; all seven changed definition exports per sign pass saved STEP validity/solid checks. Full context tested42,640pairs/sign with unchanged hash guards and no Boolean errors: plus3 and minus16 residual overlaps. **The hose/intake and hose/fitting overlaps are absent in r6.** Plus failures are rail/lifting eye542.817327mm³, rail/return0.222036mm³ and rail/screw3 3.051836mm³. Minus residual failures concern rail/return, protected mounts and regulator/intake; full list is `r6/minus/context.json`. Counts do not select orientation. Tiny elbow/flange contact remains a distinct-part overlap requiring physical joint classification, not an exemption.

Reproduction uses frozen builders `-r2.py`, `-r4.py`, `-r5.py`, `-r6.py`, whose hashes equal the corresponding historical build reports. Revision build entrypoints now import those exact sources. Original entrypoint text is preserved as `*-historical-entrypoint.py`; historical checker/entrypoint hashes refer to historical inputs, not silently to successor scripts. r3 is preserved as its separate lead study. Runtime is existing `.venv-cad`; source/generated inputs are repository-relative. Temporary Matplotlib cache is optional and not an input. Source photos/manual pixels are excluded. Browser installation, production dimensions, material/seal compatibility, mechanism motion and disassembly remain NOT RUN/unknown. No shared assembly assets were modified.

Commands for latest local checks:

```sh
.venv-cad/bin/python scripts/fuel-rail-candidate-20261003-build-r6.py
.venv-cad/bin/python scripts/fuel-rail-candidate-20261003-check-r6.py
.venv-cad/bin/python scripts/fuel-rail-candidate-20261003-hose-global-r6.py
.venv-cad/bin/python scripts/fuel-rail-candidate-20261003-context-r6.py
MPLCONFIGDIR=/private/tmp/fuel-rail-resume-mpl python3 scripts/fuel-rail-candidate-20261003-render-r6.py
```

The r5 clamp/exterior-flow checks describe r5 geometry; they have not been relabeled as rerun r6 tests. r6 changes only hose geometry, verified by frozen source comparison. Their scoped architectural conclusions remain relevant; they never establish complete enclosure acceptance. Next work is a coordinated r7 offset supply-stem seal, small bare return and two-port gasket numerical proposal based on exact service evidence and DS1125/PR18 replacement views; no r7 geometry authorized or built. Continue independent source orientation investigation without clash-based sign choice.


### CRITICAL r6 actual-render correction — supersedes positive hose conclusions above

The actual exported r6 render exposed that the saved hose is only a socket-region fragment, volume69.186945mm³ plus, boundsZ420..430, not the requested full route through endpoint(0,-55,460). Watertight mesh, exact reconstruction equality and absence of hose/intake collisions describe this defective fragment and are **not functional hose acceptance**. The conservative centerline/sub-sweep proof remains a useful isolated path study but did not validate the final Boolean shell. Full hose geometry/envelope, both endpoint openings and positive physical volume were missing acceptance gates. Both r6 candidates FAIL hose coverage. Preserve all prior reports as failed/superseded evidence; no installation or pressure acceptance follows. Diagnostic and successor pending. Archive must carry this correction.
