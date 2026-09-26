# Component contract and handoff: throttle plate retention integration

## Contract

- Issue: [#43](https://github.com/0xZakk/truck/issues/43), engine parent #1. Integration owner: root; bounded plate-retention worker owns only the new adapter, installer, installed checker, learning record and this handoff.
- Baseline: `fb2a1e756cf5e0d6ed925975312231406fce18ed`; stage-time manifest SHA `af0f6b5da21483ac6a71bba33ba20cf8e54130383a5f530d92374cb8f7307f07`, 721 definitions / 1,326 occurrences, including the compact intake, −167 mm throttle ancestor X shift and new IAC attachment.
- Scope: stage an explicitly educational four-screw hypothesis. Preserve shaft/plate IDs, keyed shaft end, plate/bore locations and local moving frame. Excludes production count, dimensions, fit, torque, locking, strength, preload, airflow and idle calibration.
- Owned: `cad/engine/throttle_plate_fasteners_integration.py`, `scripts/install-throttle-plate-fasteners.py`, `scripts/check-throttle-plate-fasteners-installed.py`, `inventory/engine/throttle-plate-fasteners-learning.json`, this file. Parent owns shared builder/viewer integration and canonical installation. No shared writes by this worker.
- Units and interface: millimeters; original shaft and plates remain local to `throttle-moving`. Plate centers Y ±27; screw centers Y −35, −19, 19, 35; X=Z=0. Screw head seats on negative-X plate face. Shaft pads seat on positive-X plate face. All inherit moving-parent rotation. Explode screw −80 X. Ancestor rigid movement is permitted without weakening local part bindings.
- Inputs: existing shaft/plate STEP and current full assembly STEP/GLB artifacts, exact candidate/review/report hashes. Tested local CAD environment is required; see artifact restoration policy. Stage rechecks whichever canonical exists when invoked.
- Required checks: staged current-neighbor sweep, local contacts, modeled thread capture, export bounds, preserved key geometry, local-frame negative control and displaced-head negative control. Full check is 47 poses (every 2° plus 45°); quick check is 0/45/90 only and cannot authorize apply.

## Evidence ledger

| Feature | Evidence class | Source | Limit |
|---|---|---|---|
| Four plate screws | Explicit educational hypothesis | `reference/engine/throttle-plate-fasteners-review.json` | Factory mounting-nut count is unrelated; exact butterfly screw count unknown. |
| Negative-X heads, two per plate | Inferred from comparison specimen topology | Same ledger and candidate handoff | Comparison specimen is not verified exact 1994 application. |
| Threads, seats and holes | Estimated local construction | `cad/engine/throttle_plate_fasteners_candidate.py` | Physical educational retention, no production fit or locking claim. |

## Delivery

- Branch: `engine/intake-and-attachment-coordination`; no worker commit. Readiness: full 47-pose stage PASS; installation/browser acceptance remains with root.
- API: `install(define, add, definitions, occurrences, assemblies, shapes)` in `throttle_plate_fasteners_integration.py`; call after throttle keyed linkage and return-spring adapters. Merge `source()` into manifest sources. Reuses `throttle-shaft` and `throttle-plate`; adds `throttle-plate-screw-illustrative` plus four occurrences. Predicted result: **722 definitions / 1,330 occurrences**, +1/+4.
- Stage directory: `cad/engine/generated/throttle-plate-fasteners-integration-stage/` (ignored). Contains original manifest and local STEP snapshots, exported changed STEP/GLB, staged manifest, installation record and validation report. Existing candidate reports remain unchanged.
- Learning: `inventory/engine/throttle-plate-fasteners-learning.json`. Prior actual geometry renders: `cad/engine/generated/throttle-plate-fasteners-candidate/candidate-context.png` and `candidate-screw-detail.png`; root reviewed context before staging.
- Environment: macOS, Python 3.13.12, build123d 0.10.0, trimesh 4.7.4. Model/effort and usage unavailable. No asset release for this stage; ignored outputs are reproducible from source and baseline CAD assets.

Commands from repository root:

```sh
# Plan only, no output writes.
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/install-throttle-plate-fasteners.py
# Current canonical becomes stage baseline; canonical is unchanged.
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/install-throttle-plate-fasteners.py --stage
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-throttle-plate-fasteners-installed.py --stage-dir cad/engine/generated/throttle-plate-fasteners-integration-stage --quick
# Root installation: restages current inputs, runs full 47-pose gate, then guarded writes.
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/install-throttle-plate-fasteners.py --apply
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-throttle-plate-fasteners-installed.py
```

Apply checks fresh canonical bytes after preflight and rolls back partial writes on a write failure. Installation records bind the local artifacts/occurrences, while a future ancestor shift triggers fresh spatial checks rather than a false local-frame rejection. The installed checker retains the stage baseline for preservation proofs; reproduce stage snapshots before deleting generated artifacts.

## Validation and review

| Gate | Status | Method / output | Limit |
|---|---|---|---|
| Application/coverage | Limited | Factory/replacement ledger reviewed | Four screws remain a hypothesis. |
| Dimensions/coordinates | PASS | Local binding and preserved shaft material outside seats | Estimates, not factory dimensions. |
| CAD/export | PASS | Actual STEP validity/solids, GLB watertightness and bounds ≤0.2 mm | No strength claim. |
| Source/visual comparison | Reviewed candidate | Actual context/detail renders; parent context review | Staged browser not reviewed. |
| Installed interfaces | PASS | Head/plate contact, rear support and axial thread capture; displaced head and local-frame controls | No preload or locking claim. |
| Motion/disassembly | PASS | All current occurrences broad-phase; exact selected neighbors at 0/45/90, then full 47 poses for apply | Sampled sweep, not continuous proof. |
| Learning/diagnostics | Authored | Scoped learning JSON separates mounting nuts, stop screw and plate screws | Viewer hook belongs to root. |
| Browser integration | NOT RUN | Root after install | Not accepted installed. |
| Reproduction/review | PASS (staged) | Hashed stage inputs, metadata scope and geometric idempotence | Requires baseline CAD restoration. |

No generic collision exclusions: changed-part internal pairs are checked at neutral because they share one rigid moving frame; external neighbors use their actual per-angle transforms, including a deforming spring shifted with its current parent. A clean sweep proves only sampled geometric clearance.

## Tracking and restart

Issue #43 remains open. Root reviews staged report, runs guarded apply, hooks adapter into shared builder, wires learning and performs browser verification. No production completion claim. The plan-only command and all three new Python modules pass syntax validation. Full stage validation passed all 47 poses and 940 exact external pairs with zero collisions; all 1,330 occurrences entered broad phase. Stable local shaft/plate regeneration has zero symmetric difference, as does shaft material outside the four seat regions. Head contact is 6.0240039 mm² per screw, rear support is 16.8232287 mm² per plate, axial-withdrawal thread interference is 0.5619439 mm³, and displaced-head contact is zero. All three exports are valid one-solid and watertight after explicit 1e-8 m position welding; maximum bounds discrepancy is 0.0060924798250212575 mm. Durable report: `inventory/engine/throttle-plate-fasteners-staged-validation.json`; stage manifest SHA `967fad5db68ca51f5e3556845120e4e55dcb97f4ad15b476a1fc7e7080cfc229`. See stage `validation.json` for exact tested angles and current hashes; a quick pass is not a full-motion pass.
