# Component contract and handoff: shifted ignition-lead endpoints

Engine #32; root integration owner; inclined-linkage worker. Baseline `8c2d2d9a1400acf784e04581a61e6a6ede38d3ba`, current branch `engine/timing-drive-fit`. Own new `cad/engine/shifted_ignition_lead_candidate.py`, dedicated checker/reports and `cad/engine/generated/shifted-ignition-lead-candidate/`. No shared manifest, canonical assets, frozen drive/pickup or original ignition helper edits.

Cause: distributor branch moves by worldDELTA `[0,5.109820990161097,4.087856792128875]` while seven cap-end cable joints stay fixed. Peer audit reports56 overlaps. Preserve firing order and exact tower map, all stableIDs, all plug/coil frame datums, cable diameters and source limitations. Cap-end boots/contacts are rigid connector constituents and followDELTA. Jackets/cores are flexible routes: adjust only the cap-adjacent firstBezier plus straight segment for cylinder leads, or lastBezier plus straight segment for coil lead. Preserve lane point/tangent and every downstream Bezier/straight segment exactly. No whole-lead translation.

Control-point contract: cylinder firstBezier first two controls translateDELTA, final two remain fixed; coil lastBezier final two controls translateDELTA, first two remain fixed. This is a declared layout bend estimate, not modeled material strain or production cable length. The unchanged side is preserved by exact source curve and separately verified section/control geometry. Envelope for change is convex hull of old/new changedBezier controls and straight endpoints expanded3.5mm jacket radius; include rigid connector extents separately. No threshold reduction or clearance-driven clipping.

Predeclared checks: source replay of exported definitions; actual shifted cap/terminal versus new jacket/core/boot/contact; positive terminal-to-contact and core-to-contact mating evidence; deliberately stale endpoint controls; fixed opposite boot/contact identities and exact downstream curve/support preservation; candidate/candidate and bounded affected neighboring static comparisons; valid solids, STEP roundtrip, GLB bounds/watertightness; actual CAD/mesh rendered. Continuous distributor motion does not move cap wires; flexible lead motion/thermal behavior and browser are NOT RUN. Existing electrical/factory-dimension gaps remain.


## Evidence ledger

| Feature | Evidence | Limit |
|---|---|---|
| Seven cap-end joints | Existing `ignition_leads.py` cap/plug/coil frames and frozen conditional distributor DELTA | Absolute tower clocking and factory connector contours remain provisional |
| Jacket/core radii | Original 3.5/1.05 mm jacket and 1 mm aggregate core | Illustrative material envelope, not measured production dimensions |
| Route revision | Two Bezier controls moved by DELTA, opposite two and remaining curves identical | Layout estimate; length/strain conservation not claimed |

## Delivery

Readiness: separate candidate ready for root review; no installed acceptance. Shared branch now contains root checkpoint `3dcbd364ac24396e671d5d16b930571713b7be0a`; original contract baseline remains above. API `shifted_ignition_lead_candidate.build(cylinder=None)` returns four shapes and path contract; cylinders 1..6, None for coil. All 28 assets in `cad/engine/generated/shifted-ignition-lead-candidate/` retain world-aligned original definition frames. Existing occurrence parents and identity transforms stay unchanged. In particular, the 14 cap boot/contact translations are baked into the new assets; translating their occurrences again would be wrong. No learning content changes.

Reproduce from repository root with `XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-shifted-ignition-lead-candidate.py`, then `scripts/mesh-shifted-ignition-leads.py` and `scripts/check-shifted-ignition-lead-neighbors.py` using that same interpreter. Render with `PYTHONPATH=.venv-cad/lib/python3.13/site-packages MPLCONFIGDIR=/tmp/truck-mpl XDG_CACHE_HOME=/tmp/truck-cache python3 scripts/render-shifted-ignition-leads.py`; bind using `python3 scripts/bind-shifted-ignition-leads.py`. macOS 15.6.1 arm64, Python 3.13.12, build123d 0.10.0/OCP 7.8.1.1.post1; host NumPy/Trimesh/Matplotlib. Usage/model billing unavailable.

## Validation and review

| Gate | Result | Scope and evidence |
|---|---|---|
| Application/source | LIMITED | Existing source constraints retained; estimated routes and connector dimensions, no new factory claim |
| Coordinates | PASS scoped | Exact shared downstream curve construction/radii, unchanged opposite end frames; source replay edge/circular boundary samples and fixed-wall interior probes |
| CAD/export | PASS | 28 valid single-solid STEP files, roundtrip volume checks; 28 GLBs watertight, winding consistent, positive volumes; bounds within 0.15 mm |
| Mating joints | PASS | All 56 new cap/terminal pair overlaps zero; each terminal/contact 122.52211349 mm² and core/contact π mm²; stale boot positive overlap controls retained |
| Affected static neighbors | PASS | Frozen v2 hash 9b8253b318e800e18b999a0a74caa749d9525978f2c19bc7286c07bb79a7c100; 365 actual intersection pairs zero, 37,337 bounds-separated pairs; q0/axial0 only |
| Visual | Actual exported mesh | `ignition-lead-review.png`: world X/Y route projection and lead1 cap-local Z108 transverse boot/contact rings |
| Motion/disassembly | NOT RUN | Cap wiring is stationary; full moving-neighbor, flexible cable, thermal and disassembly coverage absent |
| Learning/browser | NOT RUN | No canonical or viewer changes; root integration/replay required |
| Reproduction | Bound | Final delivery JSON hashes reports, assets, proposal, checker and render sources |

The original full-source coplanar symmetric-difference gate failed and is preserved in `shifted-ignition-lead-initial-replay-failure.json`. Subsequent exact full-solid subtraction stalled and was interrupted, preserved in `shifted-ignition-lead-source-replay-diagnostic.json`. Fixed-tail probe subtractions also returned contradictory positive volumes (including whole-probe volumes) and remain explicitly untrusted. None is relabeled PASS. Separate evidence consists of identical source parameter/curve laws, tiny replay volume/bounds differences, bidirectional actual boundary samples, fixed-path shell probes and strict interior points, with a 0.2 mm radial negative control. This is not an exact whole-solid symmetric-difference proof. The first coil probe used a mismatched Frenet flag; the final checker matches the original non-Frenet coil sweep, with earlier log and six-family resume provenance retained.

The guarded integration proposal replaces 28 definitions and includes unchanged before/after occurrence guards. It preserves stable IDs, parents, electrical order and opposite-end assets. Root must replay the original 56 faults before superseding their classification. Full engine acceptance, exact cable lengths, clip elasticity, sealing compression, dielectric behavior and physical bend limits remain unresolved.

## Tracking and restart

Engine #32 stays open. Next action is root visual review and guarded v3 composition/replay; frozen v1/v2 are unchanged. No running CAD processes at delivery. No canonical files were modified by this worker.
