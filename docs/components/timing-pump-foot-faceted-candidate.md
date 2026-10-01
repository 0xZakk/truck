# Component contract: isolated faceted timing pump feet

Issue #32 under engine #1; root integration owner. Baseline8547c589d3c086bad91baf879219612bcd9a162f, branch engine/timing-support-joints. New isolated candidate, all analytic ellipse failure files frozen. Owned files: timing_pump_foot_faceted_candidate.py, matching checker/render, report, generated directory and this handoff.

Root authorized replacing only the ellipse profile with an inscribed128-segment polygon of ellipse14/5.5mm, with maximum chord sag bound14*(1-cos(pi/128))≈0.004217mm. This is a declared estimated representation change, not an exact topology-equivalence or factory dimension claim. Pump frame, thickness localZ16..24, cutters, screw axes and column endpoints fixed. No canonical/shared edits.

Acceptance: native valid single block/supports; exact STEP readback1e-5mm³; direct complete watertight mesh and bounds0.15mm; wholepan clearance, actualpump/boltcontact; oldstrictwitnesscontrols; onlyoldfootmaterialremoved; columnsunchanged. Facet margins conservative using5.5*cos(pi/128): borewall>2.29mm and headcircumscribedmargin>0.29mm. These are comparison limits, not strength specifications. Inheritedcrankgear/frontlandfailure and browserNOTRUN retained.

## Delivery — 2026-10-01

Readiness: **candidate; local gates PASS, integration review pending**. This is a separate representation study from the frozen failed analytic ellipse. No installed or factory acceptance. API `timing_pump_foot_faceted_candidate.build()` returns `(block, data)`; `revised_supports()` replaces only the original ellipse expression with the declared polygon. World frame and translated source `PUMP_FRAME` match the analytic contract in `timing-pump-foot-candidate.md`; stable installed IDs/transforms are not edited.

Evidence remains inherited model estimates: the polygon dimensions and 0.004216538 mm maximum chord-sag bound do not establish manufacturer contour or strength. The unchanged pump, two actual bolt occurrences and pan are the geometric neighbors. Formula `5.5*cos(pi/128)` conservatively bounds the polygon inradius, giving a 2.298343503 mm bore wall and 0.298343503 mm clearance beyond the radius5.2 head envelope. These replace the analytic ellipse's nominal margins only for this separately declared representation, without changing any contact/collision tolerance.

Outputs: `cad/engine/generated/timing-pump-foot-faceted-candidate/` contains `block.step`, directly tessellated `block.glb`, both support STEPs, actual placed pump/bolt/pan STEPs, `pump-foot-render.png`, `block-glb-render.png` and logs. Report: `inventory/engine/timing-pump-foot-faceted-validation.json`. Required frozen baselines, native sources and dependency restoration are described in `docs/CAD-ARTIFACTS.md`; its current support supplement supplies the prior candidate/witnesses. No temporary file is an input. New artifact publication and PR remain root-owned; no new release URL yet.

Environment: macOS, Python3.13/build123d0.10.0 in `.venv-cad`; system Python NumPy/Matplotlib renders. No packages installed. Model/effort and usage unavailable.

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-timing-pump-foot-faceted-candidate.py > cad/engine/generated/timing-pump-foot-faceted-candidate/validation.log 2>&1
XDG_CACHE_HOME=/tmp/truck-cache MPLCONFIGDIR=/tmp/truck-gear-mpl python3 scripts/render-timing-pump-foot-faceted-candidate.py
python3 -m py_compile cad/engine/timing_pump_foot_faceted_candidate.py scripts/check-timing-pump-foot-faceted-candidate.py scripts/render-timing-pump-foot-faceted-candidate.py
```

The renderer binds its final output/source hashes into the report after rendering. Restore inputs and run the fresh checker before rendering; `--from-export` is diagnostic only.

| Quality gate | Outcome |
|---|---|
| Application/coverage | NOT RUN factory verification; explicit inherited and estimated geometry. |
| Dimensions/coordinates | PASS scoped contract; 128-segment profile only, fixed frame, cutters, pad thickness and column endpoints. |
| CAD/export | PASS: valid original single block and single supports; valid STEP with zero symmetric difference. Direct native GLB watertight, bounds error0.006842375 mm against0.15 mm limit. |
| Local material preservation | PASS: no added material,2412.727940 mm³ removed; zero removal outside original supports and zero missing original column material. |
| Installed interfaces | Local PASS: whole block and feet clear pan by0.581117073 mm, zero overlap; actual pump and bolts clear pan. Both actual pump seats167.812279634 mm² and bolt seats38.082071982 mm² positive. Zero pump/bolt overlap and no support missing from connected block. Overall installation remains FAIL due inherited crankgear/front-land conflict. |
| Critical negative controls | PASS: old0.008 mm³ witness cubes still fully contained by original support and pan; both excluded by new support. |
| Source/visual comparison | Actual shaded local STEP meshes, exact CAD section and actual exported whole-block GLB rendered and inspected. No source photograph/production-contour acceptance. |
| Motion/disassembly | NOT RUN: static support revision; no new whole-engine motion or removal study. |
| Learning/diagnostics | N/A: isolated support estimate only; installed learning unchanged. |
| Browser integration | NOT RUN: isolated candidate and previous root security rejection; no bypass attempted. |
| Reproduction/review | PASS local inputs, report, assets and syntax; root independent review and release pending. |

Source vs render: the inspected section shows both new feet inside the fixed pan wall and excludes the old witness locations. The local view shows retained columns, feet and bolt seats. Polygon facets are the declared approximation. No source comparison image was available for factory fidelity; appearance remains unverified for the truck.

Inherited `61.012932 mm³` refined crankgear/front-land interference remains open in the frozen source report; neither this foot revision nor passing export resolves it. Frozen analytic ellipse candidate and all failed mesh diagnostics remain unchanged. No canonical writes, shared assembly mutation or automatic promotion.

## Tracking and restart

Issue #32 stays open under engine #1. Local work complete; no processes running. Next action: root reviews the hash-bound candidate/contact proof and actual renders, then coordinates any later integration with the front-land and other timing dependencies. Publication should preserve both failed analytic and passing faceted studies. Browser/installed acceptance and production source gaps remain explicit. No worker or coordinator billing values are available.

Final shaded review: `block-glb-review.png` uses actual GLB face normals and a +Y side view. Original flat overview retained as `block-glb-render.png`.

Final SHA-256 bindings (all report input/artifact hashes rechecked):

- `inventory/engine/timing-pump-foot-faceted-validation.json`: `c9ce2474a7c65a73b872fb83b7f1cac2218354e0309d45b8eeed4e8c4c9af256`
- `cad/engine/generated/timing-pump-foot-faceted-candidate/block.step`: `7c7e9e0c5c6db1233fca045d20312dda2ad9bcaca9654965346d85edd0bc9a2e`
- `cad/engine/generated/timing-pump-foot-faceted-candidate/block.glb`: `2f59cd8d79c60844d84e5f5d1efb34f312fc0a53adf5133ef9d2007662ea4f9e`
- `cad/engine/generated/timing-pump-foot-faceted-candidate/pump-foot-render.png`: `d5bfb8df3e18b104d4a1482251dd33782ea602bce35e7428ae3dfae1a3c55fde`
- `cad/engine/generated/timing-pump-foot-faceted-candidate/block-glb-render.png`: `a264ab3d6c44636a7bfc6d9a7c219e749aa86e9498c88c385cb5856316dc7344`
- `cad/engine/generated/timing-pump-foot-faceted-candidate/block-glb-review.png`: `6f606ceff64486c4254c25b612baa2c9e3fab944fe7e71568255c44b7569b438`
