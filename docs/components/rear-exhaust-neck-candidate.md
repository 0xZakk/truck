# Component contract and handoff: rear exhaust neck exterior

## Contract

- Issue #46 under #1; researcher `evr_install_resume`, integration owner root coordinator. Assigned issue read using CLI.
- Baseline commit `411b8363f2fbdcab28f81255578a3d4a07f4772e`; manifest `ab99fff2f63ad5dfc21fde8d12a32fc2a3d65832e6c8664baefd99d94403f7bf`; installed rear STEP `680cf58c458970dfacd5d15f8da3533fe12fc47058de2d68f3709b35aa47bc48` copied to isolated generated directory before modeling.
- Own NEW `cad/engine/rear_exhaust_neck_candidate.py`, `scripts/check-rear-exhaust-neck-candidate.py`, `scripts/render-rear-exhaust-neck-candidate.py`, `inventory/engine/rear-exhaust-neck-candidate-validation.json`, this handoff and ignored `cad/engine/generated/rear-exhaust-neck-candidate/`. Existing collector/proof, canonical, shared exporter and inventory remain frozen.
- Scope: estimated exterior blend of installed rear outlet neck only. Preserve flange/seat/outlet axis and endpoint, exact existing internal gas space, head entries/bolts and full provisional EGR functional patch. No new AIR/HO2S labels or ports; no count changes.
- Evidence: retained Dorman 674-186 front/back/three-quarter replacement images, applicability and unresolved topology in `rear-exhaust-port-topology.md`. Broad blended neck appearance is replacement evidence; all new section dimensions are estimates, not image measurements. Owner casting identity and true neck length/axis remain unknown.
- Units/frame: CAD millimeters; retain installed rear frame. Current axis X=-145.688, Y=-180; Z increases toward collector. Do not move flange to manufacture a shorter silhouette.
- Acceptance sequence: first actual exported mesh side/bottom/oblique views beside actual source pixels, identical baseline/candidate cameras and scales; root shape review BEFORE expensive exact checks. Then protected-region symmetric difference <0.001 mm³, original gas-space obstruction <0.001 mm³, meaningful wall samples and fault controls, one valid solid, STEP roundtrip, watertight clean mesh, bounds error <=0.1 mm, current affected-neighbor overlap <=0.1 mm³. Never relax prior physical scopes to pass.
- Available inputs: frozen installed STEP/GLB/manifest; existing candidate inner geometry helpers read-only; current neighbor STEP files; local source images. Part remains `exhaust-rear`, count delta zero.

## Delivery / review status

V2 isolated candidate passes scoped exact gates after coordinator shape review. It is not installed and no canonical promotion is proposed by this worker. Source originals/composites remain ignored. No manufacturer dimensions claimed. Model/effort and billing unavailable.

## Trial history

The first loft produced a flat visible patch where it crossed the inherited head protection boundary and ended near the collector. It was rejected on visual review before expensive checks. Original module, STEP, GLB, preview report and comparison are retained in `cad/engine/generated/rear-exhaust-neck-candidate/rejected-v1/`.

The second trial limits transverse growth to avoid that boundary and ends its upper sections inside the existing collector. Both trials keep the flange at the original station; apparent neck shortening comes only from the broader exterior transition. Unknown auxiliary bosses and unsupported head lands remain plainly visible rather than being hidden by a camera change.

## Reproduction

From repository root:

```sh
.venv-cad/bin/python scripts/check-rear-exhaust-neck-candidate.py
PYTHONPATH=.venv-cad/lib/python3.13/site-packages MPLCONFIGDIR=cad/engine/generated/rear-exhaust-neck-candidate/mpl python3 scripts/render-rear-exhaust-neck-candidate.py
```

The first command independently reconstructs the candidate and checks the saved reviewed exports. It requires the frozen `baseline.step`, `baseline.glb` and `baseline-manifest.json` in the isolated directory. Restore the installed rear baseline from the coordinator's CAD checkpoint and verify the hashes above; do not substitute a later canonical shape silently. Source photos are the authorized local captures named in the port-topology evidence ledger and are excluded from distribution. Python 3.13/build123d 0.10.0 and trimesh 4.7.4 use the repository CAD environment; rendering uses local Python/matplotlib with that environment's trimesh on PYTHONPATH.

Latest exact status and target hashes are in `inventory/engine/rear-exhaust-neck-candidate-validation.json`; the generated render record binds the actual displayed meshes. Exact gates now pass as detailed below; those gates do not establish factory dimensions or production casting fidelity. Browser and learning edits are N/A for this uninstalled geometry study. Issue #46 remains open.

## Coordinator shape review

Root directly viewed V2 `source-comparison.png` and accepted its broader transition for exact gates. This is explicitly not full casting fidelity. Thin head lands, long bolt arms and end EGR discrepancy remain unresolved. A larger head-land/bolt-arm correction needs a coordinated head receiver, manifold fastener/clamp and intake/exhaust stack contract. A changed outlet flange or seat would require a separate mating pipe/joint contract; it cannot be hidden inside this exterior-only study.

The exact checker verifies the already reviewed `candidate.step`/`candidate.glb` and independently rebuilds the shape for equality; it does not overwrite reviewed exports. Frozen preview-builder source remains in the ignored directory as trial evidence. The checked-in module's `build(baseline)` is the parametric API; export reproduction is below.

To reproduce exports in a fresh isolated folder after restoring the baseline (this replaces the preview stage only; rerun exact gates and visual review afterward):

```sh
PYTHONPATH=cad/engine .venv-cad/bin/python - <<'PY'
from pathlib import Path
import build123d as b
import numpy as np
import trimesh
from OCP.BRepTools import BRepTools
from rear_exhaust_neck_candidate import build
out = Path('cad/engine/generated/rear-exhaust-neck-candidate')
s = build(b.import_step(out / 'baseline.step'))
b.export_step(s, out / 'candidate.step')
BRepTools.Clean_s(s.wrapped)
v, f = s.tessellate(.05, .1)
m = trimesh.Trimesh(np.array([tuple(p) for p in v])[:, [0,2,1]] * [1,1,-1] / 1000,
                    np.array(f), process=False)
m.merge_vertices()
m.update_faces(m.nondegenerate_faces())
m.update_faces(m.unique_faces())
m.remove_unreferenced_vertices()
m.export(out / 'candidate.glb')
PY
.venv-cad/bin/python scripts/check-rear-exhaust-neck-candidate.py
```

No mesh hole filling or CAD repair is part of this export. If outputs differ, preserve the previous review and repeat source comparison rather than inheriting its acceptance silently.

## Final scoped validation

Exact checker exited 0. Report SHA-256: `2ca5e93bc5e34b05a06c13b39ecf3a9c59bd8da19dfc3a50cd92822de3c73953`. Target STEP: `e62eb15b98718387b76357a96458dfc73c6cee13440882bc5686b6cbce0879e9`; target GLB: `e91a7ce204811713565f7893601ebdbe1a3c4815405d6eeea9c949f57a37f556`. Source-comparison image: `96ded1670ce3d1d6f253ceeb61c67bcb3d9ee6f3e9db3be3d98bfa1471bc0dca`. A final read-only hash check confirmed the checked mesh equals the rendered/reviewed mesh and all bound sources remained unchanged. Canonical manifest remains `ab99fff2f63ad5dfc21fde8d12a32fc2a3d65832e6c8664baefd99d94403f7bf`.

| Gate | Result | Actual coverage and limits |
|---|---|---|
| Application/coverage | Bounded PASS | Replacement-photo-informed exterior only; owner casting and port identity unresolved |
| Dimensions/coordinates | Bounded PASS | Fixed original datums, estimated loft section dimensions; no production dimensions |
| CAD/export | PASS | One valid solid; reviewed STEP and rebuilt CAD symmetric difference 0 mm³; no baseline material removed; watertight 65,656-triangle GLB with zero duplicate/degenerate faces; maximum mesh/CAD bounds error 0.002314 mm |
| Source/visual comparison | PASS for bounded scope | Coordinator reviewed V2 side/bottom/oblique comparison; thin lands, bolt arms, end EGR and true neck length remain unsupported |
| Protected interfaces | PASS | Head entries/bolt lands, full flange/seat/end station, EGR protective region each 0 mm³ difference; independently derived full EGR end wall/seat difference and bore obstruction also 0 |
| Flow/walls | PASS, scoped | Connected flow witness and full original generated gas-volume obstruction 0 mm³; all three runner void probes clear; 24 spherical wall probes fully contained. Not a global minimum-thickness or CFD proof |
| Fault sensitivity | PASS | Added blocker detected at 87.9645 mm³; removed wall sphere detected at 0.523599 mm³; shifted interface detected at 57,735.37 mm³ |
| Current neighbors | PASS | Full current occurrence bounds scan then 27 exact STEP comparisons, all 0 mm³ overlap. Includes current EGR fitting/tube/sleeve; scoped transforms and artifact hashes preserved in report |
| Motion/disassembly | N/A | Exterior study has no moving joint; no new removal-path claim |
| Learning/browser | NOT RUN / N/A | No integration or learning edits; browser acceptance requires later installation |
| Reproduction/review | PASS for isolated candidate | Parameter API, export/check/render commands, input hashes and rejected trial preserved; final integration review remains coordinator-owned |

Next action: coordinator review of exact evidence; no apply command or shared hook has been prepared. Any future adapter must recheck current canonical/neighbor state rather than treating this static report as installation acceptance. No process remains running. #46 remains open.

### Integration-base transition

After PR #95 merged, coordinator moved the shared checkout to `engine/timing-core-pan-joint`, HEAD `705c4683c199d8c5e28addba018bc8d1bdd399b1`. This is the next integration base, not a replacement for the original study baseline. Rear STEP/GLB, manifest `ab99fff2…`, all report-bound inputs and reviewed candidate exports were checked unchanged. Frozen prior collector and neck proof records were not rewritten for the branch transition.
