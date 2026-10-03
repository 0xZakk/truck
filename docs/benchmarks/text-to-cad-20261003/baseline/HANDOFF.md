# Component contract and handoff: block-core-cup-mps59a (baseline arm)

## Contract (recorded before modeling)

- Assignment: root-dispatched paired benchmark; Engine #1 / historical closure coverage #32 (not issue completion). Dispatch 2026-10-03T18:21:27Z; worker began reading at dispatch.
- Contributor: baseline worker; system lead/integration owner: root.
- Baseline commit: 4ddb52af029062268e55d4585076a8700e7e8650; branch engine/coordinated-host-candidates-20261003. Existing manifest is excluded from this isolated scope.
- Scope/readiness: isolated replacement-envelope candidate only. No installed host, branding, coating, microtexture or alloy claim.
- Owned files: docs/benchmarks/text-to-cad-20261003/baseline/ and cad/engine/generated/text-to-cad-20261003/baseline/. Shared changes and Git controlled by root.
- Identity: Melling MPS-59-A replacement shallow cup; exact truck location/fit unknown. Stable candidate ID block-core-cup-mps59a.
- Datum: CAD millimeters, axis x=y=0, bottom z=0, opening +Z. GLB meters (X,Z,-Y). Parent/transform/explode and neighbors unknown, no installed occurrence.
- Geometry: OD52.578, height8.7122; estimated uniform wall/floor1.0, outer bottom R1.5 and inner floor R0.5, flat lip.
- Input: frozen BRIEF.md and catalog at reference/engine/research-2026-09-23/melling-expansion-plug-guide.pdf; root inspected actual page8/printed6. Public catalog URL in brief. No photograph available; source contour remains unknown.
- Checks: saved STEP valid one connected positive solid, bounds and mesh deviations <=.025mm; mesh watertight/consistent/one component. Finite floor, cavity and radial wall probes, missing-floor and blocked-opening controls. Actual CAD tessellation and saved mesh renders including section. Installed interfaces, disassembly and browser integration NOT RUN.

## Evidence ledger

| Feature | Value | Class | Source | Limits |
|---|---|---|---|---|
| OD | 2.070in =52.578mm; catalog min2.065/max2.075in | replacement comparison | Melling PDF page8/printed6 | metric52.48 conflicts, unresolved; inch basis frozen |
| Height | .343in =8.7122mm | replacement comparison | same | not original truck measurement |
| Trade size | 2-1/16in | replacement comparison | same | not free OD |
| Wall/floor and radii | 1mm; R1.5/R.5 | inferred | frozen study | not measured factory section |
| Fit/position/material alloy | unknown | unknown | no applicable evidence | plain steel appearance only |

## Delivery

- Tracking correction: block/plugs/dowels issue **#24**, parent **#1**; #32 is historical mislabel only. No issue completion claimed.
- Readiness: **candidate**. Parametric cup with estimated concentric bottom bends, flat lip and no application transform.
- Entry point: `build_check.py`; API `build(od=52.578, height=8.7122, thickness=1., outer_radius=1.5, inner_radius=.5)` returns one build123d part, millimeters.
- Generated prefix: `cad/engine/generated/text-to-cad-20261003/baseline/`; STEP/GLB basename `block-core-cup-mps59a`; two deliberately defective control STEPs and `render-data.npz` also present.
- Source/report/render prefix: `docs/benchmarks/text-to-cad-20261003/baseline/`. `report.json` records source/catalog/exporter/artifact hashes and checks, `actual-renders.png` shows actual STEP and GLB. Full build/render logs are alongside them.
- Asset release: root to preserve/package; no external release claimed. `sha256.json` inventories delivered files other than itself.
- Reproduce from repository root using `.venv-cad` created per `cad/requirements-engine-lock.txt`. Exact current environment in `environment-freeze.txt`; renderer separately requires Python3 with NumPy2.4.4 and Matplotlib3.10.9 (see `render-environment.json`). No credentials or temporary input artifacts needed. Obtain the cited public catalog and place it at its documented reference path to reproduce its evidence hash; geometry itself is parameterized directly.

```sh
.venv-cad/bin/python docs/benchmarks/text-to-cad-20261003/baseline/build_check.py > docs/benchmarks/text-to-cad-20261003/baseline/build.log 2>&1
MPLCONFIGDIR=/private/tmp/truck-baseline-mpl python3 docs/benchmarks/text-to-cad-20261003/baseline/render.py > docs/benchmarks/text-to-cad-20261003/baseline/render.log 2>&1
```

The temporary matplotlib directory holds only a disposable font cache; no deliverable depends on it. For another platform, choose any writable cache directory. GLB export directly reuses `cad/engine/intake_runner_exterior_integration.py:export_mesh`; this helper's imports use repository modules, and its target-building functions are never called. Tessellation .07mm linear/.08rad angular; the helper's historical .15mm assertion is supplemented with the frozen **.025mm** independent acceptance check. No thresholds altered. Python3.13.12/build123d0.10.0/OCP7.8.1.1.post1/Trimesh4.7.4/NumPy2.5.3 on macOS15.6.1 arm64. Model/effort unavailable to worker; root measures token usage.

## Validation and review

| Gate | Status | Evidence | Limits |
|---|---|---|---|
| Application/coverage | PASS for bounded replacement comparison | Frozen brief and catalog hash in report | Truck location/fit unknown, not factory fidelity |
| Dimensions/coordinates | PASS | CAD nominal max error .0000001mm; STEP roundtrip0; mesh max .005195773mm | Inch-vs-metric catalog conflict unresolved |
| CAD/export | PASS | One valid positive connected solid; saved mesh watertight, winding consistent, one component; 61 CAD and 61 mesh probes | Finite samples, not entire solid analytic proof |
| Source/visual comparison | NOT RUN source contour; PASS actual-artifact inspection | Worker opened actual-renders.png, compared STEP and GLB opening and half-surface views | No source photo; visible floor, lip and rounded transitions agree between saved artifacts only |
| Installed interfaces | NOT RUN | No host bore/pose contract | No installed fit, seal, press interference or retention conclusion |
| Motion/disassembly | NOT RUN | Isolated stationary cup | No removal/access model or installed neighbors |
| Learning/diagnostics | PASS bounded educational text | Below | No torque, repair specification or diagnostic procedure invented |
| Browser integration | NOT RUN | Root owns UI/integration | Candidate absent from viewer |
| Reproduction/review | PASS local reproduction; root review pending | Source, hashes, full logs, lock/environment, commands | Root independent review required before experiment acceptance |

The cup illustrates a closure used for a block core opening. Its continuous floor closes the opening, while its outer cylindrical wall represents the seating region. The modeled fit is unknown: this isolated shape cannot establish leakage, retention, corrosion condition, installation depth or service suitability. Catalog identity is replacement comparison only. Plain gray steel-like display color is not an alloy specification.

Negative controls are exported and reopened: missing-floor rejects13 floor probes; blocked-opening rejects12 opening entries (these share the central opening coordinate, so they are not12 distinct spatial samples). The61-entry set has50 distinct coordinates; radial wall/floor/cavity/outside checks use12 angular stations. Mesh occupancy uses generalized winding numbers without an optional ray-tree library. Both CAD and mesh candidate checks pass. Controls are CAD checks against saved defective STEP artifacts.

## Failures and rework

- Geometry builds:1, no failed solid/export/check runs. Expected faulty controls are test evidence, not accidental build failures.
- One discovery command used unmatched shell globs; corrected to a repository file search. No files modified by that command.
- First render removed all triangles crossing the cut plane, which hid broad floor triangles. Inspected it, changed the visualization to clip triangles exactly at Y=0, regenerated and inspected the final render. Geometry and artifacts never changed. This is one render rework; the first temporary image was overwritten, so only the final image is preserved. No false floor absence is claimed in the model.
- Harmless logs: ezdxf cache path not writable; STEP Compound color warning. GLB color is explicitly assigned and geometry checks pass. Initial Matplotlib import used a temporary cache; final commands set a disposable writable cache explicitly.

## Tracking and restart

- Root controls Git/PR/issue and board. Candidate preservation only; #24 stays open for installed scope.
- Next action: root independently inspect artifacts/renders and frozen gate results; archive generated artifacts per project policy. No assembly changes or checks invalidated.
- Worker start/dispatch:2026-10-03T18:21:27Z. Submission recorded in `timing.json`; accepted finish recorded separately by root. No running process after delivery.
- Tokens/effort/billing: unavailable locally; root measures worker and coordinator scopes separately.
