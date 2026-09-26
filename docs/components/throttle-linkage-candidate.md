# Component contract and handoff: estimated throttle linkage

## Contract

- Issue #43, engine parent #1. Baseline commit `2cc2000f876901d76a12fbe251f03103a0e516de`; manifest SHA recorded by checker. Worker: linkage agent; reviewer/integration owner: coordinating agent.
- Scope: candidate lever, ball stud and retention pin, plus coordinated **proposed** shaft and bracket replacements. Shared sources/manifest unchanged. No factory dimensional certification.
- Owned files: `cad/engine/throttle_linkage_candidate.py`, `scripts/check-throttle-linkage-candidate.py`, `inventory/engine/throttle-linkage-candidate-validation.json` and this handoff. Generated outputs under ignored `cad/engine/generated/throttle-linkage-candidate/`.
- Evidence/detail: factory topology from `reference/engine/throttle-linkage-review.json`; all candidate dimensions and D-shaft/pin construction inferred. Factory retention architecture remains unknown.
- Units/frame: CAD mm. Moving parts use current `throttle-moving` local origin, world (394,25,490), Y-axis rotation, identity occurrence transforms. Proposed bracket remains in world coordinates under `throttle-assembly` with identity transform.
- Neighbor scope: current throttle housing, gasket/hardware, twin plates, IAC/TPS components and intake; current shaft replaced only inside this candidate study. Revised bracket checked against the same local neighbors. Whole-engine installation/browser acceptance remains separate.
- Tolerances: exact overlap maximum0.1 mm³; contact area>1 mm²; GLB bounds error<=0.2 mm; motion sampled every2° from0–90°. Negative controls must disconnect the anchor and show relative rotation/axial displacement physically blocked.

## Evidence and geometric decisions

The applicable1994 factory figures690090240 and690365451 show the external lever and spring bank;690370320 establishes the opposite TPS side. Factory procedure explicitly names a cable ball stud. No dimensions, key, pin or spring specification are transferred from these images. Public specimen/factory image references and hashes live in the research ledger; restricted manual originals are not redistributed.

The original bonded hub/inward ball concept was rejected for installed retention and orientation. Final candidate uses a **model-derived D-section coupling and transverse pin**, with a shoulder on the replacement shaft. These establish a physical rotational and axial constraint without claiming that Ford used this construction. Pin material, tolerance, strength and its own production locking method remain unverified; the model represents a fitted pin, not a service specification.

The lever's24 mm arm initially points in local+Z. Opening rotation carries it toward+X, with an outward-facing ball on the positive-Y side (ball center worldY95). This produces positive opening torque from pull toward the inherited round cable-hole datum (465,110,467) throughout the sampled range. Starting the arm along+X would go over-center and was rejected. A1 mm-radius straight cable envelope from ball center to the fixed exit is checked against the revised bracket. The physical cable/socket remain absent; this validates only a direct clearance path and force direction, not sheath flexibility or articulation.

The original bracket web occupies worldY92–94, conflicting with the outward ball sweep. The proposed bracket calls the existing pilot generator with **web_y104 instead of93**: +11 mmY. Mounting datums,2 mm sheet thickness, casting/nut seats, mounting openings, tipX465, outerY124 and cable-hole centers remain fixed. Mounting ears extend to the revised web; cable-end flange becomes correspondingly narrower. The original central opening is additionally enlarged by a capsule in the web, centersX431/449,Z484 and radius12 mm, to clear the direct cable envelope throughout travel. Mounting/cable holes and tip stay fixed. These are coordinated corrections to an already estimated bracket, not extracted factory dimensions.

Shaft proposal retains original plate slots and the entire original shaft, adds a2 mm cylindrical shoulder beyond localY62, then a4 mm D-section key (radius2.5 mm, flat at2 mm before orientation). Hub spans localY64–66 and matches that key. A1.5 mm-diameter transverse pin passes through a matching shaft bore at localY66.75 and8 mm total length; its lower tangent contacts the lever outer face. The shoulder contacts the opposite hub face. All figures are estimates. No C6 kickdown parts are added.

## Delivery and reproduction

Entry points: `parts(existing_shaft, overrides=None)` returns four local solids; `bracket_proposal()` returns the revised world-coordinate bracket. Import the existing current shaft STEP as `existing_shaft`; do not rotate its plate slots when applying the lever's initial orientation. Proposed IDs are `throttle-lever-estimated`, `throttle-cable-ball-stud-estimated`, `throttle-shaft-keyed-estimated`, `throttle-lever-retaining-pin-estimated`; stable installed shaft occurrence ID must be preserved if integrated. The bracket proposal is a replacement of the existing occurrence, not a second overlapping bracket.

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-throttle-linkage-candidate.py
XDG_CACHE_HOME=/tmp/truck-cache MPLCONFIGDIR=/tmp/truck-linkage-mpl python3 scripts/check-throttle-linkage-candidate.py --render
python3 -m py_compile cad/engine/throttle_linkage_candidate.py scripts/check-throttle-linkage-candidate.py
```

Environment: macOS; CAD Python3.13/build123d0.10/trimesh4.7.4; system Python with numpy/matplotlib renders the saved actual tessellation. STEP and browser-convention GLB (metres,X/Z/−Y) are exported to the ignored output directory. Report contains source/neighbor/output hashes. No required temporary inputs; caches are disposable. Restore baseline STEP through `docs/CAD-ARTIFACTS.md`. Model/effort/usage unavailable.

## Validation and review scope

Report is authoritative for numeric results and input hashes. It checks valid one-solid CAD, STEP volume roundtrip, watertight GLBs after removing zero-area/duplicate triangles at the sphere pole, mesh bounds, D-hub and stud seating contacts, shoulder/pin axial capture, and46 sampled motion poses. A separated hub must lose contact; a5° relative rotation must collide with the D key; ±0.25 mm axial shifts must hit pin/shoulder. The unmodified bracket's collisions are preserved as an explicit rejected baseline.

| Gate | Scope / readiness |
|---|---|
| Application/coverage | Factory lever/ball topology; spring, shield, screws, cables and stops remain excluded |
| Dimensions/coordinates | Explicit model estimates and current local frame; no source-supported production dimensions |
| CAD/export | See report for five exported single-solid definitions and roundtrip checks |
| Visual/source comparison | Actual candidate render generated below; contour/dimensions remain estimates |
| Installed interfaces | Candidate D torque path and shoulder/pin capture checked; actual production construction and load capacity unknown |
| Motion/disassembly | Sampled0–90° local sweep and cable force sign; full spring return, cable routing, stops, pin removal/disassembly NOT RUN |
| Learning/diagnostics | Explains pull-to-rotation and retention; not repair guidance or production calibration |
| Browser integration | NOT RUN; no shared installation performed |
| Reproduction/review | Input/output hashes and commands; independent root review pending |

Readiness remains candidate until integration owner reviews geometry/evidence, resolves scope limitations, applies coordinated replacements and checks installed browser/neighbor behavior. Issue #43 stays open. The pin's axial security, spring/return action, shield, plate hardware and real stops remain necessary follow-up work.

## Recorded local outcome

Final coordinated candidate **PASS** on manifest `f725260d8f1497a1b6f2aed9d41d01155bf2a82e7391d24ce866f352bb50cd5b`:557 exact pairs against28 local neighbors,46 sampled poses, no collisions over the0.1 mm³ static threshold. The1 mm-radius cable envelope has **zero overlap** at all46 poses, tested separately to1e-6 mm³. Opening force projection stays positive (minimum23 mm). The unchanged bracket produces137 recorded candidate/pose conflicts and cannot be retained for this mechanism.

Hub/shaft mating area40.642 mm²; stud seat10.179 mm²; pin/shaft contact23.023 mm². Negative controls detect disconnected hub (zero contact),5° relative twist (0.196 mm³ interference),+0.25 mm axial shift into pin (0.586 mm³), and−0.25 mm shift into shoulder (2.415 mm³). Revised bracket retains casting contact369.731 mm² and both nut seats36.643 mm² each. Five STEP/GLB pairs pass integrity/bounds checks; maximum GLB bounds discrepancy0.00412 mm.

Actual tessellation renders `candidate-context.png` and `candidate-linkage-detail.png` in the ignored output directory were visually inspected. The latter exposes the D bore, outward ball and pin; the context shows the larger bracket aperture and opposite shaft end. The lever remains a simplified flat educational outline, rather than the factory formed profile. Root independent review and installed acceptance are NOT RUN. No process remains running at handoff.
