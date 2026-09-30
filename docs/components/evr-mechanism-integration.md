# EVR integration preparation and discrete motion handoff

## Contract

Issue58, engine parent1/cross-system7. Worker pump_seal_finish; root owns shared exporter/viewer wiring, installation and browser acceptance. Current preparation starts from733definitions/1341occurrences; exact manifest and scoped dependencies are in the isolated stage record. Frozen mechanism candidate/report/source evidence are unchanged. No canonical files are written by this preparation task.

Owned new integration files: `cad/engine/evr_mechanism_integration.py`, `scripts/install-evr-mechanism.py`, `scripts/check-evr-mechanism-installed.py`, `scripts/prepare-evr-motion.py`, `viewer/evr-discrete-motion.js`, `scripts/test-evr-discrete-motion.mjs` and this handoff. Frozen learning: `inventory/engine/evr-mechanism-learning.json`.

The adapter replaces four original EVR definitions and adds seven illustrative internals, preserving original occurrence IDs/positions/rotations/explode values. New occurrences inherit the original body occurrence's frame. Expected total740definitions/1348occurrences. Every original EVR part must have the same relative frame; a changed cap pose is rejected. Assembly parents and unrelated definitions/occurrences are preserved.

## Evidence and source refresh

The frozen candidate establishes illustrative local geometry, not installed identity, factory dimensions or calibrated pressure/electrical/elastic response. Candidate report/source hashes and every referenced evidence image/text are verified. Installed source registry key: `evr-detail-mechanism-comparison`, returned by `adapter.sources()`, with hash/path of `reference/engine/evr-detail-mechanism-review.json`.

Stage records capture relevant definitions, occurrences, ancestors and neighborSTEP/GLB hashes, plus exporter/metrics/adapter/checker/learning/helper hashes. A fresh spatial scan catches newly approaching parts. Unrelated manifest changes are allowed only after scoped validation or restaging; original EVR geometry is copied into the isolated baseline folder for explicit review. Already-installed refresh requires matching candidate evidence, scoped state and artifacts. No blind whole-manifest-hash waiver.

## Commands and assets

```sh
.venv-cad/bin/python scripts/install-evr-mechanism.py
.venv-cad/bin/python scripts/install-evr-mechanism.py --stage
.venv-cad/bin/python scripts/check-evr-mechanism-installed.py
node scripts/test-evr-discrete-motion.mjs
```

Default installer invocation is read-only. `--stage` writes only `cad/engine/generated/evr-mechanism-integration-stage/`. Root alone runs explicit `--apply`, which freshly stages, checks bindings/neighbors/replay/motion, validates guards, then transactionally copies canonical assets and manifest with rollback on exceptions. Root then runs `check-evr-mechanism-installed.py --installed` and browser review. No apply was executed by this worker.

The stage contains11STEP/GLB definitions, five actualCAD springSTEP/GLB poses, pose data, original baselineSTEPs, before/after manifest and installation/validation records. Motion canonical paths on installation are `/models/engine/evr-motion/poses.json`, `spring-0.glb` through `spring-4.glb`; corresponding STEP files live under `cad/engine/generated/evr-motion/`. Include the JSON and all five GLBs in release/archive artifacts even though they are not separate assembly definitions.

## Viewer contract

`createEvrDiscreteMotion(data,{loadSpring,applyPose})` returns `setIndex(index)`, `cancel()` and read-only `index`. Only integer indices0…4 are accepted, corresponding exactly to travel0,0.2,0.4,0.6,0.8mm. No interpolation or duty-cycle/pressure mapping. Root's control belongs on EGR/EVR views; entering/resetting/navigation calls `setIndex(0)` for the seated pose.

- Moving IDs: `evr-disc-illustrative`, `evr-disc-spring-illustrative`.
- Each springGLB is one unplaced local mesh, in standard viewer axes/meters: CAD[x,y,z]mm → viewer[x,z,−y]/1000.
- Frozen canonical geometry is the open0.8mm pose. Absolute disc delta in CAD-local coordinates is[0,0,0.8−travel]mm; equivalent mesh-local viewer delta is[0,(0.8−travel)/1000,0]m.
- Preserve occurrence/ancestor transforms and material. Apply the offset once relative to a captured base; never accumulate it or bake the existing occurrence translation/rotation into spring geometry.
- `loadSpring(url,sha256)` is root's verified loader. `applyPose({spring,discOffsetCadMm,discOffsetViewerM,travelMm,index,label})` atomically swaps spring geometry and updates disc offset only after successful load. Stale/cancelled requests never replace a newer complete frame. Failed fetch leaves the last frame unchanged and can be retried.

The helper validates exact pose count/travel, finite offsets and axis mapping. Tests cover reverse completion, cancellation/reset, same-index cache, failure/retry, bad count/travel/axis/NaN and last-complete-frame preservation.

## Learning registration and limits

Root registers `inventory/engine/evr-mechanism-learning.json` with `viewer/engine-learning-modules.js`, merges `adapter.sources()`, and calls the adapter once after the existing EVR build chain. The shared exporter must preserve the adapter's support-bound dimensions for its changed IDs and cached fine tessellation (body0.02mm/0.06rad, otherparts0.025mm/0.1rad).

Lessons explain exact1994 topology versus comparative construction, the real continuous illustrative conductor, filtering and discrete disc poses. They must retain unknown actual identity, dimensions, calibration, cap compliance and manufacturing method. Original mounting bracket/source-vacuum plumbing and hose-retention limitations remain unresolved; preserving a provisional hose connection does not certify a vacuum seal.

## Validation and restart

First733 isolated stage passed; historical copy is `cad/engine/generated/evr-mechanism-stage-before-runner/`, including its original learning snapshot. ValidationSHA256 `b078e94358c18ab7f1ff1996d2f67bd0d7a6a7cc4345bd843a514666b6b1da62`. All11STEP bindings and5spring bindings have0difference; maximum mesh/CAD bounds difference0.00404074mm. An assembly-level EVR lesson was then added by explicit integration-owner request; the next stage must bind that updated learning and runner-updated manifest. No installed/browser acceptance. Stage checker binds all11definitions to frozen candidate geometry, preserves original placements, checks exact nearby parts, replays adapter idempotently and under a parent transform, rejects a changed relative cap pose, and binds every dynamic spring/disc pose to the validated builder. macOS/Python3.13/build123d0.10/OCP7.8; Node helper tests are separate. Usage/billing unavailable.

Root plans runner installation first, then EVR restaging against the resulting manifest. Do not apply this earlier snapshot after that update without the required rebind. Integration owner supplies next notification; no inferred factory acceptance or issue closure.

## Runner-baseline restage checkpoint

Resumed on branch `engine/runner-stops-and-evr`, baseline commit `796b621244d8e341fe2f3c4de7af99488af01548`, with runner installation already present. Issue58 acceptance scope was re-read; issue remains open. Before manifest SHA256 `2df0e1b64ae048a5f4c57d518bf9104936d7a1bcba8c87dd89850b54921f41c4`. Frozen candidate geometry, report and evidence hashes remain valid; its expensive isolated checks were reused by those hashes, not rerun.

**Integration-ready within the illustrative scope; canonical apply and browser acceptance NOT RUN by this worker.** Fresh isolated stage contains740definitions/1348occurrences. Staged manifest SHA256 `d748bcc9a38a592dc058bcf9c3a792a0dc59821a3bbd442cbcd73705a18569b9`; installation record SHA256 `706ca126c02881440935453d8eeec9fa0e69dc89c4a0e5b677a8b5d431069488`; scoped validation SHA256 `5e51756a70c5d04027d98a983114e7dfc8537f416d21678e02ec73b4f11be115`.

- All11STEP candidate bindings have zero symmetric difference; five spring bindings also zero. Maximum mesh/CAD bounds difference0.004040740430355072mm.
- Fresh spatial-neighbor scan still finds only `egr-control-vacuum-hose`, `egr-exhaust-tube`, `egr-tube-heat-sleeve`; static and five-pose moving-part overlaps remain zero within the scoped checker.
- Adapter replay/idempotence, parent-frame replay and deliberately shifted relative cap rejection PASS. Candidate evidence and relevant stage inputs remain stable through completion.
- Five viewer-pose helper controls PASS, including stale completion, cancellation/reset, load failure/retry and invalid pose metadata.
- New `scripts/check-evr-promotion-controls.py` PASS: disposable stage copies reject changed candidate evidence, checker hash, nearby-geometry hash, mesh hash and cap frame before promotion. Canonical manifest is unchanged. These test hash/input guard sensitivity; geometric sensitivity remains in the scoped and frozen candidate reports.

Reproduction commands:

```sh
.venv-cad/bin/python scripts/install-evr-mechanism.py --stage
.venv-cad/bin/python scripts/check-evr-mechanism-installed.py
.venv-cad/bin/python scripts/check-evr-promotion-controls.py
node scripts/test-evr-discrete-motion.mjs
```

Reports/logs: `cad/engine/generated/evr-mechanism-integration-stage/{installation.json,validation.json,check.log,promotion-controls.log,viewer-helper-controls.log}` and `cad/engine/generated/evr-mechanism-promotion-controls/controls-validation.json`. These generated assets require the normal private CAD archive; no temporary directory is needed. No candidate source/report was edited. Only the added control script and this handoff changed during the resume task. Usage/billing unavailable; no process running at handoff.

Integration owner next commands, serialized with other canonical edits:

```sh
.venv-cad/bin/python scripts/install-evr-mechanism.py --apply
.venv-cad/bin/python scripts/check-evr-mechanism-installed.py --installed
```

Apply freshly stages/checks again; the recorded stage is not a bypass. Then complete browser selection/isolation, five poses, explosion/reset, direct-part entry and error review. Factory identity/dimensions/calibration, bracket/hardware, hose seal/routing and manufacturing uncertainties remain open regardless of this staging PASS.

## Integration-owner checkpoint

Root installed the mechanism and then refreshed `--apply` / `--installed` after the final shared exporter change. Eleven candidate bindings and five spring bindings remain zero; current scoped neighbor, mesh and replay checks PASS. Viewer wiring and required pose assets are committed; Node request/reset/failure and pose-asset hash tests PASS. Browser acceptance remains NOT RUN under the recorded localhost security rejection.

The promotion-control suite expects a pre-install stage. Its first post-install rerun failed at the stale original STEP hash guard, before reaching the intended export fault. Root preserved that failed log, added a `--stage-dir` option to the control harness, and generated/checked a separate fresh stage without modifying the canonical engine. All five fault controls then PASS. Reproduce with:

```sh
.venv-cad/bin/python scripts/install-evr-mechanism.py --stage --stage-dir cad/engine/generated/evr-promotion-control-stage
.venv-cad/bin/python scripts/check-evr-mechanism-installed.py --stage-dir cad/engine/generated/evr-promotion-control-stage
.venv-cad/bin/python scripts/check-evr-promotion-controls.py --stage-dir cad/engine/generated/evr-promotion-control-stage
```

The default installed stage is retained separately so its installed checker remains reproducible. Reports are `inventory/engine/evr-mechanism-installed-validation.json`, `cad/engine/generated/evr-mechanism-promotion-controls/controls-validation.json`, and the integration-owner batch review. The private runner/EVR/stops release preserves these stages and logs. No factory acceptance or issue closure.
