# Full-perimeter pan/gasket contact study

## Contract before checking

Issues #32/#34, Engine #1; root requested a bounded read-only study. Baseline `a66b33cdbb33c77fb74167bbe814b8e646660e47`, branch `engine/timing-pan-seal-joints`. Pan worker owns separately named checker, report, render and generated folder; frozen pan/gasket CAD and shared files stay unchanged.

Physical question: does the actual lower gasket/pan contact contain a continuous positive-width band surrounding the wet opening, including the revised front and retained rear? The prior unsupported25.5356mm² rear patches remain recorded. This study is not a fluid-volume containment or gasket-compression proof.

Inputs: frozen expanded-seat v2 STEP pan/gasket, existing source contracts and rear contact review. World millimeters, original transforms. All source contours/thicknesses remain estimates. Plan: extract actual shared mating faces; inspect their continuity and boundaries; derive a projected positive-width corridor only where actual contact exists, then independently check its lifted actual surface continuity. A projected footprint alone is insufficient. Use deliberate transverse contact loss to demonstrate sensitivity. Stop on a real gap or ambiguous topology with localized evidence instead of building an unbounded checker.

Owned paths use `timing-pan-perimeter-contact` prefix in scripts/inventory/generated. No source dimension or solid will change. Existing CAD Python3.13/build123d0.10 and installed numerical packages only. New geometry is a test fixture/contact witness, never a pan repair. Final gates and commands follow after findings.

## Evidence and results

Extraction uses the exact common surfaces of actual gasket faces with downward/vertical normals and all actual pan faces, sewed at1e−6mm, then tessellated at0.025mm. It does not infer contact from solid validity or a plan-view silhouette. The124 contact faces total35005.0999607431mm² and form one connected manifold mesh with27 free boundary loops and Euler characteristic−25: outer edge, wet edge and25 mounting holes. This includes vertical step contacts; its area is therefore not interchangeable with the earlier downward-face area test.

A triangle-adjacent route follows the actual3D contact, crossing each shared triangle edge explicitly. The final route winds once about every one of the1024 wet-boundary vertices and zero times about all25 mounting axes. Minimum demonstrated corridor width is **1.2813348908mm**, after subtracting0.20mm from each side's boundary-distance estimate (0.125mm path sample interval bound,0.05mm boundary sampling allowance,0.025mm CAD tessellation allowance). This is a conservative geometric witness, not the maximum available width or a specified gasket sealing-bead width. Distances are3D Euclidean, so folds do not inflate the boundary-clearance claim. Seven hundred sampled route nodes/midpoints differ from actual STEP solids by at most0.00837536mm for pan and0.00086484mm for gasket, below the stated tessellation allowance.

Two independent virtual pan faults remove support across the entire band: left rail box centered(0,−135,−35), size4×40×12mm; front box centered(390,0,−62), size100×4×20mm. Each destroys the enclosing free-boundary topology and prevents a closed route. These are checker fixtures, not edited/exported production parts. The actual pan/gasket hashes remain unchanged.

Rejected/limited trials are preserved: the initial wider2.066mm route enclosed13 mounting holes and is insufficient for dry-fastener sealing; the first inboard route still enclosed rear station24. The accepted route selects the inboard crossing atY−85 rather than changing any geometry. All25 winding checks independently verify the result. The first partial front fault did not cross the full band: route search failed at its chosen anchor while a remaining inner strip still existed, so that trial is **not** accepted as a topology fault control. Its files remain in `fault-front-partial/`. Failure to find a route is not generally proof that no route exists; the accepted full-width faults additionally remove the enclosing boundary topology.

## Remaining geometry defects and limits

The exact inherited rear unbacked surfaces remain **25.5355846545mm²** atX−370..−365, Y±40.787..42.375, Z−34..−32. They are not silently reclassified as full-face PASS. The demonstrated corridor goes around their inboard edge and remains supported. This study finds no additional interruption of the complete lower pan/gasket contact band; no geometry repair is proposed.

No whole-fluid containment, gasket compression/contact pressure, production width, material strength, block-side gasket contact or vehicle installation claim. The paired front-block v3 report is separate evidence. Source dimensions remain estimates and originalR11 access failures remain preserved. A positive geometric contact route does not prove a leak-free assembled engine.

## Delivery and reproduction

- Research-only, uninstalled, no stable part IDs/transforms changed. Pan worker owns the separate `timing-pan-perimeter-*` scripts/reports and generated folder. No shared files or frozen CAD edited.
- Environment: existing macOS CAD Python3.13/build123d0.10/trimesh/scipy/numpy, system matplotlib. No package installs. Font cache falls back to a temporary folder. Model/effort/usage unavailable; no release asset published by worker.
- Primary report: `inventory/engine/timing-pan-perimeter-inboard-review.json`. Exact contact extraction: `cad/engine/generated/timing-pan-perimeter-contact/extraction.json` and `actual-contact.step`. Fault reports live below `fault-left/` and `fault-front/`.
- Review image: `cad/engine/generated/timing-pan-perimeter-contact/inboard-contact-review.png`, hash-bound by `inventory/engine/timing-pan-perimeter-inboard-render-review.json`. Worker inspected plan,3D contact route and both fault close-ups; root review pending.3D Z scale is explicitly expanded.

Run from repository root, in order:

```sh
.venv-cad/bin/python scripts/check-timing-pan-perimeter-contact.py
.venv-cad/bin/python scripts/analyze-timing-pan-perimeter-contact.py
.venv-cad/bin/python scripts/analyze-timing-pan-perimeter-contact.py fault-left
.venv-cad/bin/python scripts/analyze-timing-pan-perimeter-contact.py fault-front
.venv-cad/bin/python scripts/analyze-timing-pan-perimeter-inboard.py
.venv-cad/bin/python scripts/check-timing-pan-perimeter-inboard-deviation.py
python3 scripts/render-timing-pan-perimeter-inboard.py
```

| Quality gate | Result and exact scope |
|---|---|
| Application/coverage | Research only; modeled mating surface, no factory dimensional fidelity |
| Dimensions/coordinates | PASS bounded, original world-mm exports and explicit mesh/contact tolerances |
| CAD/export integrity | Existing frozen solids unchanged; actual-contact surface extraction and manifold mesh checked |
| Source/visual | Actual CAD-derived surface render inspected; source contours remain estimates, no new photo fidelity claim |
| Installed interfaces | PASS finite-width lower contact corridor only; full-face rear failure retained |
| Motion/disassembly | N/A read-only contact study, no new motion or removal claim |
| Learning/diagnostics | NOT RUN user-facing lesson; engineering evidence only |
| Browser integration | NOT RUN, uninstalled candidate |
| Reproduction/review | Bound scripts/STEP/mesh/route/report/render hashes, root review pending |

## Tracking and stop point

Bounded study complete. No pan process remains running. Next action is root review and preservation of this separate evidence beside the original full-face failure. No further geometry or checker expansion is needed for this question. #32/#34 remain open for their other acceptance gates; no component Done or installed claim.
