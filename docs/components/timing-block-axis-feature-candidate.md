# Isolated timing block axis-feature candidate

## Contract

- Issue #32, timing system; integration owner root. Candidate only, no canonical writes.
- Baseline commit `705c4683c199d8c5e28addba018bc8d1bdd399b1`. Historical block regeneration proof remains frozen in `inventory/engine/timing-block-baseline-validation.json`; current input hashes are captured by the new checker. Rear-neck integration changed the manifest and builder main only. Historical builder bytes are recovered by commit and hash-verified, all AST outside main must match, all other baseline module hashes and canonical block STEP must match, and zero-delta regeneration is rechecked.
- Approved scope: move only cam-side stock, cam tunnel, twelve guide cuts and the complete cam-retention/rear-seat/oil-drive feature functions by the same-ray 121.8 mm hypothesis delta. Preserve X stations and all unrelated expressions/adapters. Never fill an old bore or translate the entire block.
- Owned files: `cad/engine/timing_block_axis_feature_candidate.py`, `scripts/check-timing-block-axis-feature-candidate.py`, `scripts/check-timing-block-core-interfaces.py`, their reports and generated directory, this handoff. Frozen baseline/core/land studies are unchanged.
- Millimeter CAD world frame, crank center Y/Z zero. Cam axis Y/Z becomes 95.1098209901611/76.08785679212888; delta 0/5.1098209901611/4.08785679212888. These are estimates, not measured Ford datums.
- Neighbor interfaces: four cam bearings, shaft, rear plug, retention plate and bolts, translated distributor/pump mounting features, twelve lifter guides; fixed cylinder/main/deck/head-bolt/accessory/pan/filter/dipstick/carrier regions.
- Required inputs are the locally available canonical block STEP and frozen isolated core STEP set. Reproduction requires CAD artifact restoration per repository policy.
- Gates: exact zero-delta symmetric difference <1e-5 mm³; 79 predeclared fixed protected masks with changed volume <1e-5 mm³ each; containment of changes in declared feature operands; valid single-solid STEP/GLB; core intersections, guide-clearance probes, bearing support comparisons and wrong-unshifted-bearing negative control. No threshold waiver.

## Evidence ledger

| Feature | Value / class | Evidence / uncertainty |
|---|---|---|
| Cam center | 121.8 mm, estimated hypothesis | Timing gear evidence review and axis migration plan; not selected production dimension |
| Axis direction | Same ray as current 90/72 datum, estimated | No primary block dimensional drawing available |
| Casting expressions / interfaces | Existing CAD implementation | Frozen baseline exact regeneration proof |
| Source-sized fixed parts | Preserved existing dimensions and X stations | Frozen core and thrust-land handoffs retain source classes |
| Gear service backlash | 0.0508–0.1016 mm, root-reviewed 1994 manual evidence | Separate diagnostic; existing .12 gear-thinning parameter and Euclidean clearance do not establish service compliance |
| Front casting land | Excluded, separate coordinated proposal | Cover worker owns `timing_cover_front_joint_candidate.py`; no union applied here |

## Delivery

- Branch `engine/timing-core-pan-joint`; uninstalled research candidate. No assembly inventory, shared builder or production meshes edited.
- API `regenerate(delta=DELTA, stage=None)` returns shape and exact AST edit counts; `protected_masks()` declares immutable-region probes before inspecting candidate changes.
- Outputs under `cad/engine/generated/timing-block-axis-feature-candidate/`; validation under `inventory/engine/timing-block-axis-feature-validation.json` and `inventory/engine/timing-block-core-interface-validation.json`.
- macOS, Python 3.13/build123d 0.10.0 via `.venv-cad`. Model usage/billing unavailable.

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-timing-block-axis-feature-candidate.py
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-timing-block-core-interfaces.py
```

## Validation and review

**FAIL — preserve first migration trial.** Zero-delta regeneration is exactly equal to the current block (0 mm³ symmetric difference), but five of 79 protected regions change. Declared-change containment is exact (0 mm³ outside the feature regions). These failures are retained without changing masks or thresholds.

| Protected region | Added / removed mm³ |
|---|---:|
| Side-cover rail/fastener region | 30985.911099 / 6554.808031 |
| Carrier region X292 | 465.536306 / 419.799752 |
| Carrier region X340 | 465.536306 / 323.003516 |
| Dipstick receiver | 159.549922 / 30.027266 |
| Pan socket 8 | 0.004783591 / 0 |

The original side-cover guard is X −337..337, Y 103..122, Z 129..241 mm. Supplementary comparison confirms the actual original rail and six fastener-web solid regions are unchanged. Nevertheless, moved stock extends beyond the fixed sealing plane: actual canonical gasket overlap becomes 9128.305711 mm³ and cover overlap 6352.186058 mm³, both formerly zero. This is a real interface failure, not merely a broad-mask discrepancy. Actual CAD sections at Z135,140,185 are in `side-cover-sections.png`; they show stock extending to Y122.609821 beside the lower rail. The unchanged rail does not excuse material added outside it.

The translated shaft overlaps the new block by 505.804605 mm³ at nominal axial pose and 511.808355 at −0.1 mm. Bearing 3 overlaps 349.763657 mm³ (X99..109, Y117.4..122.257, Z60.591..91.584), consistent with the later fixed filter-boss feature refilling the tunnel. Bearing 4 overlaps 3.321126 mm³ near X349.5..351.303/Y104..108.477/Z99.717..101.739, in the carrier vicinity. Their corresponding unshifted shapes in the baseline have zero overlap. Exact bounds are in the core report; the named feature attribution is geometric localization, not a separate feature-ablation proof.

All twelve guide probes intrude on later fixed material at Y105..106.233 and Z130..240. Eleven have 152.453871 mm³ intrusion; cylinder 1 guide X309.48 has 183.441368 mm³. Baseline probes are empty. Five translated distributor/oil-drive cutter probes are empty. The wrong-unshifted-bearing control overlaps 2751.109541 mm³, establishing sensitivity. Bearing support shells have positive material at all four stations, but journals 1 and 4 are not full circumferential support and these comparisons do not establish production bearing support.

The fixed refined crank gear overlaps the front lower casting by 61.012931 mm³ in both this candidate and baseline context, X378.259..381/Z−43.18..−32. This is an inherited independent-gear envelope conflict, not caused by the cam shift.

| Quality gate | Result / scope |
|---|---|
| Application and evidence | Estimated migration only; no primary axis datum or production claim |
| Dimensions/coordinates | PASS exact zero-delta baseline and limited AST edits; 5 protected-region failures |
| CAD/export | Valid single solid, watertight GLB, no duplicate/degenerate faces; 68502 triangles, bounds error0.006842375 mm, STEP volume roundtrip error0.000877831 mm³ |
| Source/visual | Actual mesh and actual CAD sections viewed by worker; casting topology remains estimated |
| Interfaces | FAIL cover/gasket, shaft, bearings3/4 and guide probes; fixed refined crank conflict inherited |
| Motion/disassembly | Block intersections sampled at axial endpoints only; failed fit prevents installation. Previous gear proofs remain frozen; service backlash unresolved |
| Learning | N/A isolated failure study; no installed learning changed |
| Browser | NOT RUN, isolated candidate and root-reported browser security block |
| Reproduction | Commands and bound source hashes retained; CAD sources/STEP inputs required per artifact policy |

Additional reproduction commands:

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-timing-block-side-cover-conflict.py
MPLCONFIGDIR=/tmp/truck-gear-mpl python3 scripts/render-timing-block-side-cover-conflict.py
MPLCONFIGDIR=/tmp/truck-gear-mpl python3 scripts/render-timing-block-axis-feature-candidate.py
```

The mesh renderer uses `.venv-cad` for extraction and system Python NumPy/Matplotlib for rendering. Its intermediate mesh file remains inside the repository generated directory. No new dependency installation. Additional preserved failed checker logs identify ShapeList and empty-Compound implementation handling; repaired checks completed without relaxing geometry gates. Source/factory fidelity remains estimated; browser NOT RUN because integration browser access is blocked and this is an isolated candidate. No installed acceptance. Frozen prior source proofs are preserved. The initial stale-input abort is retained as `cad/engine/generated/timing-block-axis-feature-check-stale-input.log`.

## Tracking and restart

Issue #32 remains open. First trial is frozen for root review. Proposed next NEW revision retains original cam-side stock and shifts only tunnel/guide/retention/drive features, then measures exact deficient support stations before any local material addition. That trial alone cannot resolve the observed later fixed rail/filter/carrier refills; their ordering and required interface changes need explicit review. No gasket/cover subtraction, hidden hole fill or automatic scope expansion. Shared integration and future front-land union belong to root. No production installation authorized.

Final artifacts SHA-256:

- `inventory/engine/timing-block-axis-feature-validation.json`: `be6b5f69ac54d45d581ce49f4d854dd8d553ccff8c358dc201dae8ebb32ce7a7`
- `inventory/engine/timing-block-core-interface-validation.json`: `a52cd2db2e373f05d615aeb8d3d1007eaf1a858483e1b686f1a8752f960286e9`
- `inventory/engine/timing-block-side-cover-conflict.json`: `4dac2d6e2d5eb5f9f38c8f5e40ab67464bad25b0616b69eaf5fff23c22238ef6`
- `cad/engine/generated/timing-block-axis-feature-candidate/block-render.png`: `e312546c35b43684f9379385206b2258c9d7165747872ae13bdbe0c90435cf37`
- `cad/engine/generated/timing-block-axis-feature-candidate/side-cover-sections.png`: `3ce7fb5aadb8c457672d26ba06ed79d08e62c4e9177a8425a739663a635ac6e0`

No processes remain. Root review pending for this failed revision. Usage/billing figures unavailable.
