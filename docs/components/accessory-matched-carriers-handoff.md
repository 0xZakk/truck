# Component contract and handoff: matched ALT/AP common carrier

## Contract

- Issues #32/#34, engine system; pan_access_resume contributor, root integration/review owner. Baseline6b1608257e8c2eaa12512ac0c256d882854f3996; branch engine/timing-drive-fit. Shared branch advanced independently during study. Private v3 SHA f512d6024ed4d3d0d86c45c39492b4ab525e039a9c50fb71b67940633b8a2055.
- Conditional support CAD only, approved exact frozen coupled centers. Pre-build and each revised analytic route recorded in `accessory-matched-carriers-contract.md`. Own only new prefixed source/scripts/reports/docs/generated assets. No shared inventory, pose, PS/AC support or frozen solve changes.
- Proposed replacement occurrence remains `alternator-thermactor-common-carrier`, parent accessory-drive. World-mm STEP, identity local candidate frame; existing occurrence integration requires root's guarded frame patch. Render GLB uses existing axis mapping(X,Z,−Y)/1000. No new installed/explode metadata.
- Four fixed engine feet, two ALT ears and two AP ears, actual hardware and complete v3 q0 neighbors. Separate pump inlet nominal/low/high WORLD hypotheses remain uninstalled. Source topology comparison F4TE-10239-AC supports single ribbed open cradles; exact bore correspondence, contour and material/strength unknown.
- Required source/CAD available in authorized checkout. Report hashes bind actual local inputs; private photographs/manual remain access dependencies, not redistributed. All new dimensions and routes are estimates. No actual neighbor solid used to subtract carrier geometry.

## Evidence ledger

| Feature | Datum / value | Class / source | Limitation |
|---|---|---|---|
| Common casting | joined open ALT/AP cradles and ribs | F4TE-10239-AC photographic comparison, frozen source investigation | installed casting identity and exact correspondence unknown |
| ALT center | Y−262.0120390117497,Z243.56984668932756 | frozen constrained numerical proposal | explicitly inferred, not measured production |
| AP center | Y−201.83251148777921,Z124.39372811097425 | same | no center/shaft movement in this task |
| Accessory faces | ALT X438.56, AP X449.06 | inherited illustrative mating geometry | full R5.5..11 named annular seats preserved |
| Engine faces | X373; ALT(−100,220/310), AP(−100,90)/(−125,140) | current actual block/head and fixed bolt geometry | named mating annulusR5.5..12; outer R16 flange overhang is not claimed fully supported |
| Ribs/cradle | trial6 rectangular ribs14mm, declared dogleg nodes and plane/hub guards | explicitly inferred source-model interface construction | no factory contour, casting process or strength claim |
| AP plate/hub/case bolt | R58 plate, R20 front hub, R53 bolt pattern | thermactor_pump.py illustrative source | analytic nonmating pockets retain1mm clearance; no neighbor-carved surfaces |
| Tool envelope | R11,40mm forward from bolt head front | explicit estimate | no sourced socket identity or demonstrated service sequence |

## Delivery

**Trial6 is a conditional geometry candidate, with a retained new-pump service-access failure.** It is not installation-ready. API: `cad/engine/accessory_matched_carriers_trial6.py:carrier()` returns world-mm BRep. Imports frozen original trial helpers only; delivery binds their hashes. Geometry valid, one solid, volume210756.150696mm³. Bounds X373..461.296885,Y−350.012039..−84,Z42.493354..331.569847.

Selected assets under `cad/engine/generated/accessory-matched-carriers/`:

- `trial6-carrier.step` SHA f824e8ed427e595ba29305c9a683d244038c00a3ce3f78d0cb1e17696ea84680.
- `trial6-carrier.glb` SHA34a337afaf281fdb6b6285ae5f6d6b4b4378e2f8981e519c003cc54862a77e11.
- `trial6-review.png`, `tool-access-review.png`; prior trial0/trial4 visuals retained.
- Exact lower-engine-bolt tool and nominal/low/high overlap STEP witnesses.

Reports: `inventory/engine/accessory-matched-carriers-trial6-check.json`, `accessory-matched-carriers-trial6-final-check.json`, `accessory-matched-carriers-fasteners.json`, `accessory-matched-carriers-tool-witness.json`. Final package hashes: `accessory-matched-carriers-delivery.json`. Root owns artifact publication; no release URL yet.

Reproduce from repository root in macOS Python3.13/build123d0.10 locked CAD environment:

```sh
.venv-cad/bin/python scripts/accessory-matched-carriers-trial6-check.py
.venv-cad/bin/python scripts/accessory-matched-carriers-fasteners.py
.venv-cad/bin/python scripts/accessory-matched-carriers-trial6-final-check.py
.venv-cad/bin/python scripts/accessory-matched-carriers-tool-witness.py
.venv-cad/bin/python scripts/accessory-matched-carriers-render.py trial6 --extract
.venv-cad/bin/python scripts/accessory-matched-carriers-render.py tool-access --extract
python3 scripts/accessory-matched-carriers-render.py trial6
python3 scripts/accessory-matched-carriers-render.py tool-access
```

Fastener report originally tests trial4 carrier and exact neighbors; final checker hash-verifies unchanged neighbors/tool poses, recomputes all eight holes and carrier tool intersections on trial6. It does not reuse old carrier fit. Final candidate rerun needs preserved trial4 STEP for that historical check; all files are packaged. Matplotlib/system Python for rendering, NumPy/trimesh for mesh. Cache warnings only; no packages installed. Model/effort/usage unavailable.

## Validation and review

| Gate | Result | Evidence / limits |
|---|---|---|
| Application/coverage | PARTIAL | common casting topology compared; detailed production identity unknown |
| Dimensions/coordinates | PASS conditional | exact selected centers and fixed engine feet; no pose edits; estimates explicitly retained |
| CAD/export | PASS | valid one solid; GLB watertight, consistent winding, one mesh component; bound error0.010964mm at0.08mm tessellation |
| Source/visual comparison | PARTIAL | actual STEP render; no factory contour match claimed |
| Installed interfaces | PASS bounded static/seat; not installed |47 actual q0 neighbors, zero overlap; nonmating gap≥1mm; eight full named annuli backed on both sides |
| Motion/disassembly | FAIL separate pump tool scope | seven approaches clear; lower engine approach blocked by all3 new inlet hypotheses; moving/load envelopes NOT RUN |
| Learning/diagnostics | NOT RUN | no lesson/user-facing content; independent bad-seat checker control only |
| Browser integration | NOT RUN | canonical unchanged; isolated candidate |
| Reproduction/review | hash-bound, root scoped review completed | sources, reports, exact witnesses, actual visuals preserved |

Minimum nonmating v3 gaps: AP housing1.832511mm, WP housing2.403791mm, AP pulley2.5mm. Named contact and bolt-bearing fits intentionally exempt from nonmating spacing. Actual overlap threshold remains0.1mm³. All eight R5.4 hole probes and carrier-only tool approaches have zero intersection. Engine named seat area357.356164mm² each; accessory area285.099533mm² each. A1mm deliberately separated engine seat makes the entire0.02mm witness miss7.147123mm³, detecting failed contact. Exact engine owner is block for engine0/2/3, head for engine1; AP mate is front plate, not housing.

Modeled smooth insertion: engine14mm, ALT19.8mm, AP7.8mm. These are **not verified threaded engagement or complete retention**: source hardware has unverified threads/nuts/grades/preload. Strength, fatigue, belt loads and thermal/engine-motion margins remain open.

The separate new-pump inlet shapes have zero carrier overlap and minimum2.403791mm spacing. However fixed lower engine bolt at(Y−100,Z90), toolX391..431, overlaps nominal1689.846952, low1576.070148, high2316.756726mm³. Current v3 pump tool clears. No service-removal sequence is established that would waive this failed installed approach. Carrier routing cannot remove a fixed bolt/pump access conflict; root must coordinate source-supported service architecture with pump work.

Rejected studies preserved: trial0 sloping-seat/head and pump collisions; trial1 invalid rounded-rib Boolean; trial2 lost stock despite valid one-solid result (rejected by full extent/seat evidence); trial3 AP-body/cartridge and unbounded seat guard; trial4 AP plate/hub; trial5 AP case bolt. Trial0 AP contact checker wrongly used housing; trial3 onward corrects to actual front plate. Do not interpret trial1/2 numerical neighbor results as valid geometry acceptance. Runtime/initial build errors and source snapshots retained. No failed threshold relaxed.

## Tracking and restart

Component issues remain open. Root inspected trial6 STEP context and recognized scoped seat/clearance progress. The box-section spine and dogleg are explicitly an estimated load-path prototype, not a factory casting reconstruction. Source silhouette comparison remains a required later gate. Root must resolve the fixed-bolt/new-pump access dependency and retention gaps before any integration. PS/AC support, catalog/effective belt uncertainty, wiring/plumbing and broader assembly acceptance remain outside this delivery. No running process at freeze. No canonical/shared writes, installed change or browser claim. Usage unavailable.
