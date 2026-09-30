# Component contract and handoff: rear exhaust neck integration

## Contract

- Issue #46 under #1. Worker owns preparation; root coordinator alone owns shared builder/viewer edits and canonical apply.
- Integration base: `705c4683c199d8c5e28addba018bc8d1bdd399b1`, branch `engine/timing-core-pan-joint`. Original neck-study baseline and proof remain frozen. Current manifest `ab99fff2f63ad5dfc21fde8d12a32fc2a3d65832e6c8664baefd99d94403f7bf`, 741 definitions / 1,349 occurrences at preparation.
- Owned NEW files: `cad/engine/rear_exhaust_neck_integration.py`, `scripts/install-rear-exhaust-neck.py`, `scripts/check-rear-exhaust-neck-installed.py`, `scripts/check-rear-exhaust-neck-promotion-controls.py`, `inventory/engine/rear-exhaust-neck-learning.json`, this handoff, and ignored `cad/engine/generated/rear-exhaust-neck-integration-stage/`.
- Stable ID `exhaust-rear`; no added/deleted parts or occurrences. Plain name: **Rear exhaust manifold**. CAD millimeters, existing local/ancestor transforms and explode metadata remain unchanged.
- Scope: accepted estimated neck exterior only. Preserve head/bolt interfaces, flange/seat/outlet endpoint, existing EGR functional patch and original gas path. Production casting identity, auxiliary-port assignments, head lands, bolt arms and EGR location remain unresolved.
- Inputs: source-bound isolated neck proof `inventory/engine/rear-exhaust-neck-candidate-validation.json` SHA `2ca5e93bc5e34b05a06c13b39ecf3a9c59bd8da19dfc3a50cd92822de3c73953`; baseline STEP `680cf58c458970dfacd5d15f8da3533fe12fc47058de2d68f3709b35aa47bc48`; target STEP `e62eb15b98718387b76357a96458dfc73c6cee13440882bc5686b6cbce0879e9`.
- Preparation acceptance: baseline/target recognition, idempotence, frame rejection, canonical artifact-byte bindings, extension metadata preservation, exact bounds, source/target/checker/exporter bindings, fresh current-neighbor scan, rollback and disposable promotion controls. No worker whole-engine rebuild or canonical apply.

## Evidence and limits

The coordinator reviewed the actual V2 source-comparison mesh and accepted only the broader outlet exterior. Exact candidate proof records zero removed baseline material, unchanged protected regions, unobstructed original generated gas volumes, 24 wall probes, 27 exact neighbor comparisons and watertight export. These are scoped historical inputs; staging independently verifies target STEP equality and the actual current shared exporter, plus fresh neighbors. Nothing here certifies production dimensions or browser behavior.

Source originals and composites remain excluded from Git/releases. Preserve target/baseline STEP, candidate proof and stage artifacts according to the CAD artifact policy. The previous collector installer, sources and reports are unchanged; do not rewrite historical proof to conceal dependency changes.

## Full-build consistency review

Root must add, immediately after the existing collector hook:

```python
import rear_exhaust_neck_integration as rear_neck
rear_neck.install(define,add,defs,occurrences,assemblies,shapes)
```

Then add `sources.update(rear_neck.source())`; load `rear-exhaust-neck-learning.json` after `exhaust-rear-collector-learning.json`; append `rear-exhaust-neck` after `exhaust-rear-collector` in `viewer/engine-learning-modules.js`.

The old collector hook creates precisely the new adapter's recognized baseline on a from-source build. The new hook then recognizes that baseline or its own target and replaces only `exhaust-rear`. It preserves extension metadata and exact supported bounds. Its occurrence update changes name/function only. Subsequent full-builder function propagation uses the updated definition. Source ordering includes both historical collector and new neck evidence.

The final bounds loop already uses `support_bounds` for `rear_collector.CHANGED_IDS`, containing the same `exhaust-rear` ID. Therefore the new shape receives exact final bounds without another bounds-condition change. Existing rear-only exporter mesh cleanup remains applicable; the new adapter clears/prepares the fine tessellation cache. A static wiring audit checks hook/learning/source order and ID coverage before stage. This review is not a whole-engine rebuild claim.

The installer requires `--rebind-exporter` because the candidate was exported with the documented isolated fine-tessellation profile, not `full_engine.define`. The stage preserves that distinction: historical shared exporter hash is null, isolated profile retained, current shared function hash recorded, and actual current STEP/GLB/metadata checked. No silent historical exporter waiver.

## Guard and rollback design

- Canonical manifest plus canonical rear STEP/GLB byte hashes are captured before stage and rechecked before promotion. Installed validation requires canonical target bytes to equal staged bytes.
- Exact local and ancestor frames are protected; geometry must match reviewed baseline or target within 0.001 mm³ symmetric difference.
- Candidate source/checker and target hashes are checked from the frozen proof. Stage also binds adapter, installer, installed checker, controls, learning, port research, viewer registry, shared builder and transaction helper.
- Preserve all unknown definition extension fields. Recompute `model_bounds_mm`; remove only the exact superseded long-neck gap and obsolete pre-collector sentence, retaining other substantive gaps.
- Fresh current broadphase scans every occurrence; overlapping bounds receive exact STEP checks at unchanged 0.1 mm³ threshold. Current artifact and frame bindings prevent stale neighbor reuse.
- Reuse the existing transaction helper from `install-intake-cap-coordination.py`. Disposable rollback tests inject first-write, second-write and postcheck failure; original bytes must return and new paths disappear.
- Disposable promotion controls cover proof/dependency/export/neighbor corruption, actual canonical STEP/GLB byte mutations in a mirror, dropped bounds, stale collector/neck limitations, changed extension metadata, shifted frame despite updated manifest hash, and isolated-export promotion rejection. The real canonical tree is never mutated by these controls.

## Commands and delivery status

After root hooks are frozen:

```sh
.venv-cad/bin/python scripts/install-rear-exhaust-neck.py --stage --rebind-exporter
.venv-cad/bin/python scripts/check-rear-exhaust-neck-promotion-controls.py
```

Optional staged replay: `.venv-cad/bin/python scripts/check-rear-exhaust-neck-installed.py`. Root alone may later use `scripts/install-rear-exhaust-neck.py --apply`; worker has not applied. Installed checker supports `--installed` and writes its replay to the isolated stage directory. A subsequent shared-builder edit invalidates stage source bindings: preserve that stage as history and repeat explicit scoped stage/rebind; do not repeat the frozen expensive candidate geometry checks unless their own inputs changed.

| Gate | Preparation status |
|---|---|
| Source/candidate geometry | Historical scoped PASS; sources revalidated at stage |
| Python syntax | PASS |
| Full-build consistency | PASS static wiring audit; root hooks frozen and staged |
| Actual shared exporter/metadata/neighbor stage | PASS; exact target, fresh metadata and 27 neighbors |
| Promotion/rollback controls | PASS; 12 promotion controls and three rollback cases |
| Learning | PASS source/part linkage; source-grounded diagnosis retained, limits revised |
| Browser/integration | NOT RUN; no acceptance claim |

Environment: existing locked CAD Python 3.13/build123d 0.10.0/trimesh 4.7.4. No dependency updates. No process running. #46 remains open. Usage/effort and billing unavailable. Next action: root review of the real stage evidence and guarded apply when ready; no worker apply.

## Real shared-exporter stage — 2026-09-30

The root-owned hooks were frozen before staging. `--stage --rebind-exporter` exited 0, followed by promotion controls exiting 0. No isolated exporter shim was used. Stage directory: `cad/engine/generated/rear-exhaust-neck-integration-stage/`; build log: `cad/engine/generated/rear-exhaust-neck-candidate/integration-stage.log`.

- Exact staged STEP / accepted target difference: **0 mm³**. Baseline and target adapter replay both pass. Local-frame, ancestor-frame and unknown-geometry rejection pass.
- Actual shared-export mesh: **65,670 triangles**, watertight, no duplicate or degenerate faces, bounds error **0.002313370641 mm**. Its count differs from the isolated candidate's 65,656; fresh staged checks passed rather than inheriting that earlier export claim.
- All **27** fresh exact neighbor comparisons: **0 mm³ overlap**. All-current occurrence broadphase and artifact hashes are recorded in `validation.json` and `installation.json`.
- Extension metadata, exact supported bounds, plain name `Rear exhaust manifold`, source links and diagnostic lesson references pass. Counts stay **741 definitions / 1,349 occurrences**.
- All **12** disposable promotion controls pass. Transaction rollback at first write, second write and postcheck restores original bytes/removes new paths.
- Actual staged mesh rendered and viewed in side/bottom/oblique comparison and remains consistent with accepted V2. The source-comparison composite and render script are ignored local evidence, excluded from Git/releases. No browser acceptance claimed.
- Final read-only check confirms watched sources and canonical rear STEP/GLB bytes still match the stage's baseline bindings. Canonical manifest remains `ab99fff2f63ad5dfc21fde8d12a32fc2a3d65832e6c8664baefd99d94403f7bf`.

| Staged artifact | SHA-256 |
|---|---|
| `installation.json` | `6c5855e56832b29e088db8435f2ef6916779355d93179032cf9074cde7e1250c` |
| `validation.json` | `619f275b09f99ff4528a4101b7ffdf1ab0e974d9ef8d42aeca9d50eca3bf3416` |
| `promotion-controls.json` | `8f3c8ca2dbdaed7e7f729b6bcb62bc2fc13431f4a013d30c6ae047bacd2e8300` |
| `full-assembly.json` | `91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6` |
| `step/exhaust-rear.step` | `f711fa4e23d617921a83972585d8eaecd8fdf196682a0474d0f8796278ab0a07` |
| `models/exhaust-rear.glb` | `0425c0273a75800ceaae7e76fe9888a179d7bfe485774f8f70bfbac5f941dd75` |
| Local `source-comparison.png` | `acdb7d5aa943d15361096f487c10fe5634720bec27cddbade00cac3a6a3ab1af` |

Root-only guarded next command: `.venv-cad/bin/python scripts/install-rear-exhaust-neck.py --apply`. No process remains running. No shared or canonical file was edited by this worker. If root changes bound sources or canonical data before apply, preserve this stage and repeat the scoped stage/controls; do not bypass its guard.
