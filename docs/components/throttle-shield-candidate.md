# Contract: throttle linkage splash shield and pushpin candidate

- Issue #43 / engine #1, contributor shield worker, integration owner root. Baseline commit5567d751abcf6a9bfac84bdf87ce0d7f0d4dac5c. Frozen dependency is final `throttle_linkage_candidate.py` and its proposed bracket, rather than whichever shared manifest revision is currently being installed.
- Own only new shield module, shield checker, shield report and this handoff. No shared source/manifest edits.
- Scope: estimated educational hood9E766 and pushpinN804527-S, supported by applicable1994 factory viewY image692036165 and legend692057936. Source visually inspected again; originals remain ignored. All dimensions, hole location and barb design are inferred.
- Frame: world CAD mm; stationary `throttle-assembly` children, identity occurrence transforms. Source shows shield covers linkage and attaches at bracket; it does not provide a measured mounting coordinate.
- Proposed interface: one new2.4 mm-radius Y-axis mounting hole at(X389,Z514) through proposed bracket webY103–105; shield ear seats on outboard faceY105. Ear thickness1.5 mm, pin head seatY106.5; inferred flexible barb shoulder bears on web backsideY103. Expanded barb2.9 mm radius, hole2.4, shank2.2. Two thin bridges join ear to hood rather than placing an unattached tab in space.
- Hood: estimated67 mm X span382–449, roofZ524.5–526 and outer sideY113.5–115 down toZ480, with chamfered roof transition. Open X ends and inner side allow cable/shaft access. This is an angular approximation to factory hood, not exact contour.
- Inputs: existing shaft STEP, current local throttle/intake STEP, final linkage module/bracket and source ledger. Export STEP/GLB and actual renders under ignored `cad/engine/generated/throttle-shield-candidate/`.
- Gates: valid single solids, STEP/GLB bounds<=0.2 mm; rigid overlap<=0.1 mm³; pin/ear/bracket seat area>1 mm²; detached-pin negative control; linkage and1 mm direct cable envelope sampled every2° over0–90, cable overlap<=1e-6 mm³. Whole-engine/browser independent review remains required.
- Exclusions: spring count/tangs/preload, production pin material/locking geometry, insertion flexure, strength and factory dimensions. No C6 hardware.

## Evidence ledger

| Feature | Class / source | Limits |
|---|---|---|
| Hood over external linkage, bracket attachment | Applicable1994 factory viewY, V6832-F / image692036165 | Perspective contour only; no production dimensions |
| Shield9E766 and pushpinN804527-S identities | Applicable legend image692057936 | One pin illustrated; hidden attachment details cannot be counted from this view |
| Hole atX389,Z514, roof extent, ear bridges | Inferred CAD coordination | Chosen on solid bracket web away from mounting/cable holes; not measured from diagram |
| Split compliant barb construction | Inferred educational pushpin | Actual Ford pin profile/material and installation deformation unknown |

Image URLs/local archive paths and hashes are preserved in `reference/engine/throttle-linkage-review.json`. Original images were inspected in place under ignored `manuals/factory-service-manual/`; none were copied into Git.

## Delivery and reproduction

`throttle_shield_candidate.parts()` returns three world-coordinate solids: `throttle-linkage-shield-estimated`, `throttle-shield-pushpin-estimated`, and the coordinated replacement `accelerator-bracket-shield-hole-estimated`. Both new occurrences belong to stationary `throttle-assembly`, with zero position/rotation. Preserve the existing bracket occurrence ID when replacing its definition/geometry; do not add a second overlapping bracket. Root owns shared installation and source registration.

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-throttle-shield-candidate.py
XDG_CACHE_HOME=/tmp/truck-cache MPLCONFIGDIR=/tmp/truck-shield-mpl python3 scripts/check-throttle-shield-candidate.py --render
python3 -m py_compile cad/engine/throttle_shield_candidate.py scripts/check-throttle-shield-candidate.py
```

Outputs: ignored `cad/engine/generated/throttle-shield-candidate/*.step`, `*.glb`, `preview.npz` and `candidate-context.png`. The checker saves source, neighbor and export hashes in `inventory/engine/throttle-shield-candidate-validation.json`. CAD uses macOS Python3.13/build123d0.10/trimesh4.7.4; rendering uses system Python numpy/matplotlib. Reproduce baseline inputs via `docs/CAD-ARTIFACTS.md`. Temporary paths are caches only. No commit/PR or shared installation performed by this worker; model/effort and usage unavailable.

## Validation and review

Local result **PASS**, snapshot manifest `f725260d8f1497a1b6f2aed9d41d01155bf2a82e7391d24ce866f352bb50cd5b` unchanged during this run.190 exact static/moving candidate pairs and46 linkage/cable poses; zero collisions. Minimum linkage clearance to hood/pin3.63668 mm; direct cable envelope has zero overlap with hood, pin and revised bracket. Three valid single-solid/watertight STEP/GLB exports; maximum mesh-bounds discrepancy0.0000229 mm.

Shield/bracket seating125.302 mm²; pin head/shield32.170 mm²; expanded barb/bracket7.123 mm². A pin displaced8 mm loses both required contacts. Attempted0.25 mm withdrawal intersects bracket by1.781 mm³, demonstrating the modeled barb retention shoulder rather than a pin floating in an oversized hole. Actual barb flexure/insertion is NOT RUN. Existing casting and nut seating remain369.731 mm² and36.643 mm² per nut.

| Gate | Result / limitation |
|---|---|
| Application/coverage | PASS applicable shield/pin identities; exact contour/hidden attachments unresolved |
| Dimensions/coordinates | PASS explicitly inferred dimensions and world frame; no production dimensional claims |
| CAD/export | PASS three solids, STEP volume roundtrip, mesh closure/bounds |
| Source/visual comparison | PASS limited topology: actual two-view render inspected; roof/outer wall and connected lug approximate factory hood; faceted bends substitute curves |
| Installed interfaces | PASS candidate seat/barb geometry and negative controls; real retention forces/material durability unverified |
| Motion/disassembly | PASS sampled linkage/direct cable clearance; physical pushpin insertion/removal deformation and complete engine-bay envelope NOT RUN |
| Learning/diagnostics | Hood protects moving controls from incidental contact; inspect missing pin/loose shield and interference. No production repair or adjustment specification inferred |
| Browser integration | NOT RUN; integration owner must review installed selection/isolation/explosion and linkage visibility |
| Reproduction/review | PASS local reproduction/hashes; independent root review pending |

Readiness remains candidate, issue #43 remains open. Next action: root reviews the factory/actual render comparison and exact proposed mounting-hole delta, then coordinates installation and affected combined checks if accepted. Spring count/tangs/preload are still unknown and were not modeled. No worker process remains running.
