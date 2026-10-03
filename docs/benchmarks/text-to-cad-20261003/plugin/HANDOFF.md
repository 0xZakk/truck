# Component contract and handoff: block-core-cup-mps59a — plugin arm

## Contract

- Bounded paired benchmark under Engine #1 / block/plugs/dowels #24; old coverage handoff used #32 timing, corrected by integration owner; no issue completion claimed. Root owns coordination and Git.
- Worker: cad_pilot_plugin; integration owner: root. Dispatch 2026-10-03T18:21:32Z; first recorded clock 2026-10-03T18:22:09Z.
- Baseline `4ddb52af029062268e55d4585076a8700e7e8650`, branch `engine/coordinated-host-candidates-20261003`. Assembly manifest unchanged; isolated component has no assembly dependency.
- Scope: isolated replacement-envelope candidate. No host bore, position, original fit, installation, or factory-section claim. One manufactured cup, estimated homogeneous steel appearance.
- Ownership: `docs/benchmarks/text-to-cad-20261003/plugin/` and `cad/engine/generated/text-to-cad-20261003/plugin/` only.
- Identity: Melling MPS-59-A comparison, stable candidate ID `block-core-cup-mps59a`. MPE-107R identifies one kit block cup, not location or original dimensions.
- CAD mm, bottom z=0, open +Z, axis x=y=0; parent transform unknown. GLB must be meters (X,Z,-Y). No installed occurrence/explode transform.
- Frozen dimensions: OD52.578, height8.7122, wall/floor1, outer bottom fillet1.5, inner floor fillet0.5 mm; flat lip. Inch nominal source conversion takes precedence within experiment only.
- Inputs: common BRIEF.md and local Melling catalog; no acquired part geometry. Root reported exact step.parts query returned zero. No inspection of baseline arm.
- Checks: saved STEP valid one positive solid; envelope/roundtrip and converted mesh bounds ±0.025mm; mesh one watertight consistently wound component; finite probes floor/cavity/wall; reject missing-floor and blocked-opening controls. Native saved-artifact snapshots and read-back inspection.

## Evidence ledger

| Feature | Value | Class | Source | Limits |
|---|---|---|---|---|
| OD |2.070in =52.578mm; min2.065/max2.075in|replacement comparison|Melling 2026 plug catalog PDF page8 / printed6; https://melling.com/wp-content/uploads/2025/05/2026-plug-catalog.pdf|Listed52.48mm conflicts; unresolved|
| Height |.343in =8.7122mm|replacement comparison|same|No exact original truck verification|
| Wall/floor; outer/inner radii |1;1.5/.5mm|inferred, frozen experiment|BRIEF.md|Not manufacturer section data|
| Host bore, location, retention |unknown|unknown|none|No installed interfaces checked|

## Delivery

In progress. Candidate only. Build entry point `block_core_cup_mps59a.py`; plain parametric factory with parameterless decorated configuration. Full environment, command logs, hashes and reviewed snapshots follow.

### Completed isolated delivery

- Readiness: **candidate**; local frozen experiment gates PASS. Worker source remained unchanged through all retries. Root controls submitted branch/commit/PR and artifact publication; no worker commit.
- Parametric factory: `make_cup(od=52.578, height=8.7122, thickness=1.0, outer_radius=1.5, inner_radius=0.5)`; configuration `block_core_cup_mps59a()` stacks native `@step` and `@glb`.
- Source/checker/environment/report/logs/renders reside in this directory. STEP, GLB and saved STEP roundtrip reside under `cad/engine/generated/text-to-cad-20261003/plugin/`.
- Native GLB uses meters and (X,Z,-Y) already; no conversion or modified mesh was exported. CAD mm bounds ±26.289 XY / z0–8.7122. STEP import/export bounds error0; GLB inverse bounds error0.00000085543mm, threshold0.025mm. Valid single solid3350.599607mm³.
- Declared mesh chord tolerance0.0001 of bounding diagonal (approximately0.0075mm), angular0.10rad. Native GLB134,864 triangles; dense tessellation is a size/time tradeoff, not a factory-fidelity claim. Raw GLB68,262 vertices split at face normals; checker merges coincident positions at8 decimal places in meters (0.00001mm), ignoring normal/texture seams, obtaining67,434 vertices, one watertight consistently wound component. This in-memory inspection does not alter exported bytes or fill holes.
- Saved STEP probes:36floor/108cavity/72wall PASS. Missing-floor control rejects all36floor probes; blocked-opening control rejects36cavity probes. These are finite samples, not continuous manufacturing-fit proof.
- macOS15.6.1 arm64, Python3.13.12, cadgen0.7.10, build123d0.11.1, cadquery-ocp-novtk/proxy7.9.3.1.1, trimesh4.12.2, Playwright1.63.0. Full transitive pins in `requirements-lock.txt`; Python/platform in `environment.json`. CAD versions may differ from baseline and are a confound. Actual model/effort not reliably exposed to this worker; usage measured separately by root.
- Inputs SHA256 in `input-hashes.json`; saved geometry/checker hashes in `report.json`; package hashes in `SHA256SUMS.json`. Public catalog itself is not copied into this delivery. No owner photograph or purchased manual used.

### Reproduce from a clean checkout

From repository root, on compatible macOS arm64/Python3.13:

```sh
python3.13 -m venv .venv-cad-plugin
.venv-cad-plugin/bin/python -m pip install -r docs/benchmarks/text-to-cad-20261003/plugin/requirements-lock.txt
.venv-cad-plugin/bin/python -m playwright install chromium
bash docs/benchmarks/text-to-cad-20261003/plugin/reproduce.sh .venv-cad-plugin/bin/python
```

The installed skill pin is `cadgen[snapshot]==0.7.10`; lock includes those snapshot dependencies plus trimesh. No original-machine temporary file is an input. A fresh writable cache can be regenerated; `reproduce.sh` defaults it to an ignored folder under this arm's generated directory. Playwright browser installation is required. Environments that restrict local sockets/browser launch need those operations authorized; setting daemon off alone still creates a private local broker. The actual measured run used a temporary isolated interpreter/cache/browser path, with commands and failures preserved in logs. Authorized run set `CADGEN_DAEMON=0`, a writable `CADGEN_CACHE_DIR` and `PLAYWRIGHT_BROWSERS_PATH` pointing to the installed isolated browser. Global plugin configuration was not changed.

### Function and limits

A cup core plug closes a casting core opening in the engine block. Its continuous floor separates the cavity from the outside, while its rim and cylindrical wall form the closure body. This candidate depicts the replacement envelope only. Host bore, installed interference, sealant, orientation, corrosion condition and exact location are unknown. Leakage/corrosion are relevant inspection concerns, but this study provides no installation torque, repair procedure, pressure rating or claim that a plug protects an engine from freezing.

## Validation and review

| Gate | Result | Evidence | Limits |
|---|---|---|---|
| Application/coverage |PASS for replacement-candidate identity|BRIEF.md, evidence ledger, input hashes|Exact original truck fit unknown; #24 remains open|
| Dimensions/coordinates |PASS|`report.json`, `check.py`|Parent pose/bore unknown; metric catalog conflict retained|
| CAD/export |PASS|`logs/check-final.log`, `report.json`|One native solid and one welded mesh component; finite checks|
| Source/visual comparison |NOT RUN for exact source contour; PASS frozen geometry visual inspection|`cad-opening.png`, `cad-section.png`, `mesh-opening.png`|No actual source photograph; catalog dimensions bound envelope only|
| Installed interfaces |NOT RUN|No host geometry or installation attempted|Cannot claim installation acceptance|
| Motion/disassembly |NOT RUN|Isolated static study|No host removal path or explosion evaluated|
| Learning/diagnostics |PASS bounded content|Function/limits above|No service specifications invented|
| Browser integration |NOT RUN engine integration|Root separately opened native CAD viewer and reported actual cup screenshot success|CAD viewer is not engine integration|
| Reproduction/review |PASS local checks and actual snapshot review; independent root review reported|Pinned lock, reproducible script, full logs/hashes|Clean-environment rebuild not repeated; root records final accepted revision|

Worker visually read all three saved PNGs. CAD and mesh views show a thin flat lip, open cavity and uninterrupted floor; XZ section exposes a uniform straight wall/floor and both bottom radii. No visible geometry repair was needed. Root independently reported the same visual findings and passing640 analytic probes in its own checker. This handoff does not substitute those reported root results for local report evidence.

No shared assembly, viewer, inventory or neighboring geometry changed. Candidate code can be preserved; installed acceptance remains open. Next action: root reviews package hashes, records benchmark acceptance timestamp/usage, and preserves outputs under artifact policy.

## Failure and rework ledger

- Three build failures before success: default cache unwritable (`build.log`); writable-cache run could not reach geometry service (`build-retry.log`); daemon-disabled private broker socket still sandbox-blocked (`build-direct.log`). Authorized local-socket run succeeded (`build-authorized.log`). No geometry/source redesign.
- Three snapshot failures before success: geometry service (`cad-snapshot.log`); missing Chromium for CAD and section (`cad-snapshot-authorized.log`, `section-snapshot.log`). Installed browser to isolated directory (`install-browser.log`); three final snapshot logs confirm saved files.
- One dependency network attempt failed (`install-check-dependency.log`), authorized retry installed trimesh (`install-check-dependency-retry.log`). Initial `python -m pip freeze` was unavailable because this uv-created runtime has no pip; pins collected using Python package metadata. Preliminary trimesh import also confirmed the missing package. These setup/discovery costs belong to this arm.
- Two checker failures: mesh split attempted optional networkx repair (`check.log`), replaced by direct face-adjacency component count; initial normal-preserving topology load reported three components (`check-retry.log`), corrected to positional seam welding for topology inspection. Final checker passes; native exported bytes unchanged. No holes filled and no tolerance gate reduced.
- One documentation read attempted nonexistent `docs/COMPONENT-CONTRACT.md`; actual quality-linked contract is `docs/templates/COMPONENT-HANDOFF.md`, read and followed. This is a discovery error, not a CAD failure.

## Tracking and restart

- Engine #1 / block-plug scope #24 remain open; no board status changed by worker.
- No build, check or snapshot process remains running at submission. No background work promised.
- Available token/cache/effort metrics: root owns measurement. No billing estimate.

Worker submission UTC: 2026-10-03T18:31:15.893033+00:00. Root acceptance/end timestamp is recorded separately.
