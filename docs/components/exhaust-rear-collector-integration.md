# Rear collector guarded integration

Issue46; root reviewed and accepted the bounded collector/runner-seam study for integration, not full casting fidelity. Integration preparation begins on `engine/exhaust-timing-joints`, baseline merge `124aa7c345af352459a800343ffc50f1e931367c`; canonical741 definitions remain root-owned. Candidate evidence and unresolved source differences are in `exhaust-rear-collector.md` and its bound review/validation JSON.

Worker ownership: `cad/engine/exhaust_rear_collector_integration.py`, `scripts/install-exhaust-rear-collector.py`, `scripts/check-exhaust-rear-collector-installed.py`, `scripts/check-exhaust-rear-collector-promotion-controls.py`, `inventory/engine/exhaust-rear-collector-learning.json`, this handoff, and ignored `cad/engine/generated/exhaust-rear-collector-integration-stage/`. No canonical apply or shared exporter/assembly edit is authorized for this worker.

Contract: retain definition/occurrence `exhaust-rear`, local/ancestor transforms, head entries and mounts, outlet and EGR interfaces. Replace only reviewed rear geometry and associated name/function/source/gap metadata; definition/occurrence counts stay fixed. Adapter recognizes reviewed baseline or target and rejects unknown geometry, shifted local frame and shifted ancestor frame. Replays must be idempotent. Stage binds current full builder/helper/adapter/learning/source proof and exports; fresh all-occurrence broadphase and exact overlapping STEP checks bind current neighbors. Promotion uses transactional rollback on write or postcheck failures. Source originals/composites remain ignored, not release assets.

Status: final real-exporter stage and ten promotion controls PASS after audit fixes; root apply and browser acceptance pending. An explicit isolated export shim allows pre-hook tests, but its stage is hard-blocked from promotion. Root must add the reviewed rear-only exporter behavior and installation/source/learning hooks, then run a fresh real-exporter stage. Historical candidate export proof is never silently rebound: `--rebind-exporter` records old/new exporter function hashes and verifies fresh actual outputs, while leaving the original candidate report intact.

## Prepared result

The pre-hook isolated stage passes: target STEP difference0 mm³, watertight mesh64,868 triangles, no degenerate/duplicate faces, bounds error0.002314 mm; target and baseline replays idempotent; shifted local frame, shifted ancestor frame and unrecognized geometry rejected. All27 current exact neighbor checks pass. Rollback controls restore both an existing and new file for failures after writes1,2 and postcheck. Learning part/source references pass. Six promotion controls reject changed candidate proof, builder dependency, staged mesh, neighbor artifact, a shifted frame even with updated manifest hash, and any isolated-shim promotion attempt. Canonical manifest stayed unchanged. This stage is explicitly nonpromotable; its triangle count need not match the earlier candidate tessellation, but exact target geometry and actual mesh metadata are checked independently.

Historical pre-hook stage record SHA256 `83d04393e89c8f06f3c26540f1bdd02e5ec3d3f3eec2a314990305feba556265`. Reports are `validation.json` and `promotion-controls.json` in the ignored integration stage. Preserve that directory under a historical name before the root's real-exporter stage overwrites it. Python syntax checks pass. No installed or browser claim.

## Exact shared hook proposal (root owns edits)

In `full_engine.build`, immediately after the current throttle-stop install:

```python
import exhaust_rear_collector_integration as rear_collector
rear_collector.install(define, add, defs, occurrences, assemblies, shapes)
```

The adapter clears the target's triangulation cache and precaches .05 mm/.1 rad tessellation before calling `define(..., prepared=True)`. In `full_engine.define`, add **only** `'exhaust-rear'` to the existing mesh-cleanup ID tuple before the `smooth_casting` branch. That existing branch merges vertices, removes degenerate and duplicate faces and removes unreferenced vertices. Keep the existing smooth-casting and final `triangle_count=len(mesh.faces)` logic. A source-preserving isolated probe of the current function with fine precache produced64,898 faces/4 degenerates, then64,894 watertight faces after those exact cleanup operations. No generic threshold or all-component export change is proposed.

After the existing throttle-stop learning update:

```python
learning.update(json.loads((ROOT/'inventory/engine/exhaust-rear-collector-learning.json').read_text()))
```

After the existing throttle-stop sources update:

```python
sources.update(rear_collector.source())
```

The later occurrence-function synchronization already includes `exhaust-rear` and will read the updated definition. No definition/occurrence IDs, count or transforms change. Root should still review the final shared diff and run its static/full-build metadata checks.

## Fast explicit exporter rebind and root acceptance

After root changes the shared hooks/exporter, preserve the old isolated stage and run:

```sh
.venv-cad/bin/python scripts/install-exhaust-rear-collector.py --stage --rebind-exporter
.venv-cad/bin/python scripts/check-exhaust-rear-collector-promotion-controls.py
```

Do **not** pass `--isolated-export` to that final stage. Without explicit `--rebind-exporter`, a changed exporter function is rejected. The new record retains the historical candidate exporter hash and records the current function hash; fresh actual exports must pass exact target STEP difference, watertight/nondegenerate/unique mesh, triangle metadata, millimeter bounds, frame/replay and current-neighbor tests. All source/CAD/flow/wall evidence remains bound to the untouched original candidate report; no full candidate rebuild is necessary when only the shared integration/export hook changes. The whole current builder is hash-bound by the new stage and cannot change before apply.

After root reviews the real-exporter stage, root may run:

```sh
.venv-cad/bin/python scripts/install-exhaust-rear-collector.py --apply
.venv-cad/bin/python scripts/check-exhaust-rear-collector-installed.py --installed
```

The apply transaction verifies dependency/source/export/current-neighbor/manifest hashes, writes only the rear STEP/GLB plus canonical manifest/install receipts, and rolls back on postcheck failure. Current-neighbor scanning is fresh; it does not reuse historical neighbor pass claims. Browser/source-fidelity acceptance remains separate and pending. Keep issue46 open for the visibly unsupported neck, lands, auxiliary ports and retained end EGR layout.

## Audit corrections before promotion

A read-only audit found that the initial installer guarded the manifest and neighbors but did not bind the existing rear STEP/GLB bytes. The installer now records both current rear artifact hashes before staging and requires them unchanged before promotion; installed checking requires the target hashes instead. Disposable canonical-path mirrors exercise STEP and GLB byte mutations without touching canonical files.

The original adapter recreated the definition through `define` and dropped `model_bounds_mm`. It now preserves extension/provenance fields absent from the exporter base schema and recomputes target bounds; the checker verifies metadata presence, bounds, solid count and volume. Root aligns the full-builder final bounds pass to `support_bounds` for this ID. Only the exact obsolete gap beginning “This incremental entry correction retains the old collector...” is removed; all other substantive gaps remain. A scope assertion and mutation control reject reintroducing that obsolete claim.

The frozen frame-baseline manifest is now hash-checked directly in the adapter, including full-build use. Original baseline artifacts must remain distinct from the installed target: do not recreate `baseline.step` by copying canonical `exhaust-rear.step` after installation. The next CAD archive must include the candidate's `baseline.step`, `baseline.glb`, `baseline-manifest.json`, reviewed target STEP/GLB and required integration receipts. The previous runner/EVR/stops archive deliberately excludes this next-batch study and cannot alone restore a fresh checkout using the new hook. Root owns archive registration; restricted source originals/composites stay excluded.

The earlier real-exporter stage is preserved at `cad/engine/generated/exhaust-rear-collector-integration-before-audit-fixes/`. An intermediate audit-fix run was deliberately interrupted before root's final bounds edit; its log is `cad/engine/generated/exhaust-rear-collector-candidate/superseded-support-bounds-stage.log`. These are history, not current promotion proof.

Troubleshooting now uses two applicable service-grounded cards: distinguish head, main pipe and EGR joints when investigating a suspected leak (explicitly labeled as an inference from the separate service operations); clean mating surfaces before reassembly and do not infer a combination intake/exhaust gasket on a new exhaust manifold. Both link `system-b9d2a4ac71cc`; its retained exact1994 HTML hash was verified. Learning checks verify source hashes and per-card source references. No leak-test pressure, torque or unsupported repair specification was added. Root registered the new module in the viewer's learning list.

## Final real-exporter stage after audit fixes

The final `--stage --rebind-exporter` run exited0 against the frozen shared builder, without the isolated shim. Exact target STEP difference0 mm³; watertight mesh64810 triangles, no degenerate/duplicate faces, bounds error0.002313370641104484 mm. Baseline/target replay, local/ancestor/unknown-geometry rejection, all27 current-neighbor intersections and rollback controls pass. Definition metadata and source-linked learning checks pass. All10 promotion controls pass, including actual byte mutations in disposable mirrors of both canonical rear files, dropped bounds metadata and the obsolete-gap mutation. Canonical manifest and rear STEP/GLB remain unchanged. No `--apply` was run.

Installation record SHA256 `ecda7877f19b46f85a48018fe3b5128670d31ac622067789df24415dfec33c1c`.

Validation SHA256 `216f3ce7cfd1aec2ca95821a3447bc7923ad0aec1b72589e62da508d5b55b910`.

Promotion controls SHA256 `e347136d17703205af59e27c4da5c7aa4a4defd1ab81ab47ca5bca0d8afd5acc`.

Staged manifest SHA256 `ab99fff2f63ad5dfc21fde8d12a32fc2a3d65832e6c8664baefd99d94403f7bf`; baseline canonical manifest SHA256 `73de806af847c528e766151590d7b8235620893414c280711aa6ff382ca8a7e1`. The explicit root apply/check commands above now refer to this real-exporter stage; any bound source, manifest, rear artifact or neighbor change requires restaging. Next-checkpoint fixture/archive registration and browser acceptance remain root responsibilities.

## Root installation — September 30

Root reviewed the final real-exporter stage and ten promotion controls, then ran `XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/install-exhaust-rear-collector.py --apply`. The transaction and installed postcheck passed: exact target STEP difference zero, watertight 64,810-face export, 0.002313mm bounds error, preserved metadata/frames, baseline and target replays, and 27 fresh neighbor comparisons with no overlaps above the unchanged threshold. Canonical inventory remains 741 definitions / 1,349 occurrences. Manifest SHA256: `ab99fff2f63ad5dfc21fde8d12a32fc2a3d65832e6c8664baefd99d94403f7bf`.

Installed report: `inventory/engine/exhaust-rear-collector-installed-validation.json`; log: `cad/engine/generated/exhaust-rear-install-20260930.log`. Navigation now passes with the new source-linked lesson registered. The earlier navigation attempt before manifest installation rejected the not-yet-registered source ID as expected; this is resolved by the installation. Combined STEP and whole-static checks are running separately. Browser acceptance remains NOT RUN; issue46 stays open for casting fidelity and the remaining gates.
