# Component contract and handoff: isolated timing pump feet

## Contract

- Issue #32; root integration owner; baseline8547c589d3c086bad91baf879219612bcd9a162f, branch engine/timing-support-joints.
- New isolated candidate only; no canonical, pan, pump, shared source or frozen proof edits.
- Owned new timing_pump_foot_candidate.py, check/render scripts, corresponding inventory report, generated directory and this handoff.
- Millimeters, original oil_drive_layout PUMP_FRAME plus previously proposed delta(0,5.1098209901611,4.08785679212888). Pump/screw axes, padZ16..24, cutters and column endpoints remain fixed.
- One declared source change: pad ellipse semiaxes14/9 to14/5.5. Estimated minimum bore wall2.3mm and hex circumscribed-head margin0.3mm are comparison criteria, not source dimensions or strength approval.
- Required actual neighbors: oil-pump-housing, both mount bolts and unchanged oil-pan; all locally available. Positive seat contact at localZ16 and24; whole support/pan checks, column identity and strict old0.008mm³ witnesses required.
- CAD/readback symmetric difference tolerance1e-5mm³; no adaptive integration relaxation. Direct mesh valid/watertight and bounds checked; actual render required.

## Evidence ledger

| Feature | Value | Class | Source | Limits |
|---|---|---|---|---|
| Foot ellipse |14/5.5mm | estimated | root-approved local proposal | not manufacturer geometry |
| Frame/column/cutters | unchanged | inherited model | oil_drive_layout.py | factory fidelity unresolved |
| Old pan interference | two strict0.008mm³ witnesses | geometric proof | timing-pump-foot-pan-witnesses.json | volume integral nonconvergent; not waived |

## Delivery

Build and validation in progress. Inherited crankgear/front-land collision remains FAIL. Browser NOT RUN; no installation acceptance. Frozen prior support/machining candidate preserved.

## Delivery checkpoint — 2026-10-01

Readiness: **candidate, export blocked**. The geometric revision was built from source; it is not integration-ready. Only the ellipse change was applied. No canonical or frozen support candidate file was changed. Issue #32 under engine #1 remains open. Branch and baseline are those in Contract; root owns publication/review. Assembly manifest SHA-256 is `91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6`.

Entry point `timing_pump_foot_candidate.build()` returns `(block, data)` with new and old support witnesses; `revised_supports()` preserves the inherited source function except its single ellipse argument. Outputs are under `cad/engine/generated/timing-pump-foot-candidate/`; the machine report is `inventory/engine/timing-pump-foot-validation.json`. The report verifies inherited input hashes and binds actual pump, bolt, pan and strict witness STEP inputs. Prerequisites restore through `docs/CAD-ARTIFACTS.md`, including the frozen support candidate and its witness STEPs. No personal temporary file is an input. Artifact publication remains with root; no new release URL exists yet.

Environment: macOS, repository `.venv-cad`, Python 3.13, build123d 0.10.0; NumPy/Matplotlib in system Python for render. Model/effort/billing are unavailable. Cache paths below are disposable outputs only.

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-timing-pump-foot-candidate.py > cad/engine/generated/timing-pump-foot-candidate/validation.log 2>&1
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/diagnose-timing-pump-foot-mesh.py > cad/engine/generated/timing-pump-foot-candidate/mesh-diagnostic.log 2>&1
XDG_CACHE_HOME=/tmp/truck-cache MPLCONFIGDIR=/tmp/truck-gear-mpl python3 scripts/render-timing-pump-foot-candidate.py
python3 -m py_compile cad/engine/timing_pump_foot_candidate.py scripts/check-timing-pump-foot-candidate.py scripts/diagnose-timing-pump-foot-mesh.py scripts/render-timing-pump-foot-candidate.py
```

The checker intentionally exits nonzero after preserving the full report because mesh acceptance fails. `--from-export` is a debugging convenience and does not replace a fresh native CAD roundtrip check.

| Gate | Result and limits |
|---|---|
| Application/coverage | NOT RUN: source/factory foot geometry and strength remain unknown. This is an estimated educational revision to inherited geometry. |
| Dimensions/coordinates | PASS scoped contract: only ellipse semiminor 9→5.5 mm changes; frames, cutters, thickness and endpoints fixed. Nominal bore wall 2.3 mm and head-envelope margin 0.3 mm are estimates, not strength certification. |
| CAD/export | Native and STEP PASS: valid single solid, zero symmetric difference. **Mesh FAIL**: two faces cannot be triangulated; no accepted GLB exists. |
| Local material | PASS: zero material added, 2411.327163 mm³ removed; zero removal outside original supports. Original column material has zero missing volume on both sides. |
| Installed interfaces | Local CAD PASS: entire block and actual pump/bolts have zero pan overlap; block/foot minimum pan distance 0.581117073 mm. Each foot has 167.870691642 mm² actual pump contact at local Z16 and 38.082071982 mm² bolt contact at Z24. No pump/bolt overlap, no support missing from block; supports and block are connected single solids. Overall installed acceptance FAIL from inherited crankgear/front-land conflict and export failure. |
| Negative controls | PASS: both exact 0.008 mm³ old witness cubes remain fully inside old supports and actual pan, and have zero overlap with new supports. |
| Source/visual comparison | Actual STEP edge context and CAD section rendered and inspected in `pump-foot-render.png`; section confirms witnesses lie outside new feet. No source photo comparison or shaded mesh acceptance claimed. |
| Motion/disassembly | NOT RUN: static local attachment scope only; no pump relocation or moving internal geometry changed. |
| Learning/diagnostics | N/A: candidate only, installed learning unchanged. |
| Browser integration | NOT RUN: isolated candidate; prior root security rejection remains. No bypass attempted. |
| Reproduction/review | Source/report/STEP inputs and outputs bound by hashes; syntax PASS. Root independent review and artifact publication pending. |

### Export failure and rejected trials

Native tessellation and STEP readback tessellation raise `AttributeError: 'NoneType' object has no attribute 'NbNodes'`. Diagnostics identify missing triangulation on two faces near `(264.371933,96.037966,-100.564480)` and `(183.796068,101.727018,-100.776108)` mm, each approximately 1.4325 mm². Relative tolerances 0.12 and 0.03 mm, absolute 0.03 mm meshing, and same-domain clean do not resolve it. An exact NURBS representation conversion was also tested; it became invalid and still did not mesh, so it is rejected. No face was omitted and no repaired mesh was substituted for complete CAD. Logs retain these outcomes.

The render deliberately uses actual STEP edges and an exact CAD section rather than suppressing the two failed faces. The earlier direct-tessellation failure log is preserved separately. Inherited crankgear/front-land collision remains 61.012932 mm³ in its frozen source report; this scoped local revision does not claim to repair it.

### Tracking and restart

Next action: root review of the local interface proof, followed by a bounded topology-only repair of the two unmeshable foot faces. Preserve ellipse dimensions, fixed axes/cutters/endpoints, all old witnesses and exact material-equivalence criteria. Re-run the fresh checker, then require a complete watertight GLB and actual shaded render before any integration proposal. Do not declare the component Done or promote it from the successful CAD contact checks.

Frozen analytic candidate: no processes running. Final report SHA-256: `3ca8ad60cf3f48025fc772f2d04bd1d34507ccc02fc48b179389b4f6ae9cdf70`.
