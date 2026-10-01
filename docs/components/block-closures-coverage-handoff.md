# Component contract and handoff: block closures coverage

Engine #32; root integration owner. Baseline3dcbd364ac24396e671d5d16b930571713b7be0a, branch engine/timing-drive-fit. Own block-closures-coverage files only. Canonical manifest hash is bound in the delivery. Scope: reconcile identifiable closures/dowels against current inventory and completion plan, plus one isolated replacement-envelope candidate. No canonical inventory, block bores, placements or installed acceptance.

## Actionable physical-parts coverage

| Piece / evidence | Quantity boundary | Canonical coverage / reserved candidate ID | Next datum |
|---|---|---|---|
| Melling MPS-126 shallow block cup | Five in applicable MPE-107R replacement kit | Absent; definition `block-core-cup-mps126`, future occurrences1..5 only after location survey | Five bore axes, diameters, shoulder/depth and free-to-installed fit |
| Melling MPS-59A block cup | One in same kit | Absent; `block-core-cup-mps59a` | Resolve catalog inch/metric discrepancy, location and wall/seat |
| Melling MPP-554 pipe plug | Two in kit; locations unspecified | Absent; `block-pipe-plug-mpp554` | Actual thread form/taper/OD, gallery identity and port axes; nominal3/8in is not OD |
| Rear camshaft closure MPC-147 | One in same kit | Already modeled `rear-cam-plug`, provisional seat/section; do not duplicate | Existing fit and source limits remain |
| Ford C9AZ-6026-A distributor oil-access plug | One in industrial comparison | Absent; `block-distributor-oil-access-plug` | Confirm1994 application, bore/location and actual closure construction |
| Ford C2OZ-6A008-A head-to-block dowel | Two, diameter1/2in in industrial comparison | Absent; `head-block-locating-dowel`, proposed occurrences1..2 | Applicable length, solid/hollow construction, head/block sockets and fit |
| Ford87837-S pipe closures | As required;1/4-18 industrial water-jacket/compressor/main-gallery uses | Absent; role-specific IDs after topology survey | Do not convert “as required” into guessed quantity; separate active accessory ports from closures |
| Ford87710-S pipe closures | Three industrial comparison,3/8-18 | Absent; source-family row only | May overlap replacement MPP-554 inventory; do not add quantities together |
| Ford371485-S top-of-head core-hole plug | Four industrial comparison,3/4-14 | Absent; `head-core-pipe-plug` pending applicability | Head casting/EFI variant and locations |
| Oil-pump mounting dowel378644-S | Industrial comparison; quantity not established in this audit | Absent; `oil-pump-block-locating-dowel` pending pump architecture | Correct flange, orientation, fit and whether solid/hollow; do not assume oil passage |

Ford C5AZ-6026-E five1.625in cleanout plugs and C5AZ-6026-G2.078in head/block plugs are comparison families, **not additional confirmed parts** to add on top of the Melling kit. Nominal descriptions cannot establish interchange or host diameter. Kit contents are not an entire engine closure BOM. Industrial quantities must not become a verified1994 inventory.

Other covered mounting interfaces are not absent merely because unfinished: current pushrod side cover/gasket and six bolt/grommet pairs, head bolts, cam retention and pump mounting-bolt studies exist with provisional geometry. Intake manifold locating dowel is already modeled and is distinct from absent head/block dowels. Engine mounting bosses/brackets remain an explicit completion-plan gap, but this audit has no applicable exploded quantity or fastener survey for them; no invented BOM count is supplied. Bellhousing locating hardware likewise needs transmission-interface scope/evidence before reservation.

## Evidence and candidate

Existing Ford reviewed ledger `reference/engine/ford-block-plugs-reviewed.json` binds industrial PDF8–9/printed5–6 comparison findings. The applicable Melling kit application is recorded in `inventory/engine/research-2026-09-23.json`; this audit freshly inspected actual manufacturer PDF7/printed5 andPDF10/printed8. Source [Melling expansion plug guide](https://melling.com/wp-content/uploads/2025/05/2026-plug-catalog.pdf), local `reference/engine/research-2026-09-23/melling-expansion-plug-guide.pdf`. Restricted originals are not newly redistributed.

MPS-126: nominal1.625in differs from listed free OD1.640–1.642in; height.365in. Candidate uses free OD41.656mm (catalog low end), height9.271mm and explicit estimated uniform1mm wall/floor with square corners. Published metric OD41.66 is rounded; inch values are used consistently. **No installed OD, bore size, interference or seating depth is inferred.** Root authorized this isolated envelope only. `build(wall_mm=1.0)` independently parameterizes the unknown wall while preserving source OD/height. No material deformation or manufacturing contour is modeled.

Owned API `cad/engine/block_closures_coverage_candidate.py`; stable reserved definition `block-core-cup-mps126`. Local+Z opens the cup, floorZ0; no parent/occurrence/engine transform. STEP mm and GLB `[x,z,-y]/1000`. Files `cad/engine/generated/block-closures-coverage-candidate/block-core-cup-mps126.{step,glb}`. Actual exported mesh section `cup-section.png` inspected; cup remains open, floor present and source envelope matches. A separate full individual lesson is in `inventory/engine/block-closures-coverage-learning-candidate.json`, not loaded.

Reproduce: `PYTHONPATH=.venv-cad/lib/python3.13/site-packages MPLCONFIGDIR=/tmp/truck-mpl XDG_CACHE_HOME=/tmp/truck-cache python3 scripts/check-block-closures-coverage-candidate.py`. macOS15.6.1/Python3.13.12/build123d0.10.0/OCP7.8.1.1.post1. Checker verifies valid one-solid STEP, dimensional bounds, STEP roundtrip, positive closed/wound mesh and bounds within.05mm. A changed-wall floor-point control detects removal of the selected floor stock. It tests geometry, not sealing.

## Gates and tracking

Source/application PASS as replacement comparison; complete OEM BOM UNKNOWN. Coordinates/export PASS isolated; wall/stamp radii estimated. Actual mesh visual reviewed; manufacturer dimensional-table comparison only, no production contour photograph. Host interfaces, installed clearance/motion/disassembly, browser and leakage NOT RUN. Learning supplied but not installed. No source-supported block location means there is no candidate integration proposal. Root review required; #32 stays open. Next action: verify actual bore family locations/diameters and cup section before any five-occurrence placement. No running processes; usage unavailable.
