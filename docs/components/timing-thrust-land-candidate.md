# Estimated rear timing-gear thrust land

## Contract and provenance

Issue32 under engine1. Root reviewed the original15-occurrence timing-core render as a coherent isolated presentation and accepted it for preservation, not installation. Its failed thrust arrangement, exports, render and reports remain unchanged. Root then approved this bounded additive annulus: radii20.65–26 mm, cam-gear localX-7..+1.02. This new candidate owns `cad/engine/timing_thrust_land_candidate.py`, dedicated `check-timing-thrust-land-*` and render scripts, new inventory reports and generated directory. No canonical/shared files change.

Baseline shared commit124aa7c345af352459a800343ffc50f1e931367c / branch engine/exhaust-timing-joints; exact imported isolated-core/refined-gear reports and STEP/GLBs are hash-bound in `inventory/engine/timing-thrust-land-candidate-validation.json`. Source images show replacement hub/shoulder topology generally; **production backside geometry and these numeric land dimensions are unknown**. The land is an explicitly estimated mechanism correction. Plate/spacer comparison dimensions, existing axial stations, bore/key and the same-ray121.8-mm hypothesis are retained. Missing crank key, production fits, block/cover migration and factory identity remain outside acceptance.

Module API `revise(local_cam)` returns the original local shape plus an annulus; the0.02-mm extension beyond the relief floor produces a sound fused connection. Gear back remains at worldX378.259375, plate frontX378.159375. The rotating unit for axial travel consists of camshaft, cam gear, spacer and cam key. Bearings/rear plug/plate/bolts/washers and crank gear remain stationary for the axial test. IDs and frames match the prior core; exported parts remain world-frame occurrences, not replacement local definitions.

## Protected geometry and export checks

Exact boolean comparisons find zero difference inside bore guardR16.1 and the enclosing key/spacer guardR20.64. No original material is removed. Added material is6272.566724 mm³, entirely insideR26.000001 and therefore inside the protected tooth-root boundaryR77.65; outer tooth surfaces remain exactly unchanged. This justifies inherited fixed-axial tooth geometry only. It does not, by itself, prove shifted helical engagement.

Fourteen unchanged occurrence STEP/GLBs are copied byte-for-byte from the bound failed-core exports; their previous export checks remain applicable. The revised gear is valid one solid, passes STEP roundtrip, watertight/duplicate/degenerate-face checks and0.15-mm mesh-bounds/0.001-mm³ volume-error limits. Specific values and hashes are in the report. Existing failed-core files are never overwritten.

## All affected core pairs and full axial travel

All50 unordered pairs containing at least one of the four moving parts are explicitly enumerated. Six pairs move rigidly together and retain constant relative geometry. The helical pair is handled by the separate endpoint report; the other49 pairs receive static exact-intersection checks at travel-0.1,-0.075,-0.05,-0.025,0 mm (constant-relative pairs need one pose). All checked solid overlaps are below1e-5 mm³.

Full axial coverage is not inferred from those five samples. Every non-helical pair also receives a continuous certificate using one of:

- Entire swept bounding boxes remain separated.
- Both parts share the same rigid translation.
- The bounded interface gap and excluded-region distance exceed the entire0.1-mm translation. Shaft clipping retains a1-mm axial margin; any omitted shaft cannot enter during0.1-mm travel. Gear clipping is allowed only when counterpart corners stay insideR49, leaving at least1 mm to omitted material beyondR50.
- Each full bearing-source axial interval lies inside a coaxial journal cylinderR25.62225, whose entire volume clears the bearing; the journal's axial support margin covers the travel.
- Shaft material able to enter the plate slab lies either behindX373 or inside the nose cylinderR15.875. Those bounds remain clear of the plate for the entire negative translation.
- The whole revised gear stays at or forward of the stationary plate front plane throughout[-0.1,0].

These are conservative exact-solid/coordinate witnesses for the stated bodies and interval, with the declared numerical boolean tolerance. Stationary-to-stationary pairs are unchanged and outside this affected-pair scope. No continuous rotational or full-engine motion claim is made.

## Actual stops and faults

At travel-0.1 mm, gear-land/plate opposing faces contact over784.070841 mm² with zero overlap. At travel0, shaft-shoulder/plate opposing faces contact over724.430182 mm² with zero overlap. Areas are measured on physically coincident faces with opposite axial normals; they are not projected across a gap.

Moving beyond the interval is detected: travel-0.11 mm produces7.840708 mm³ land/plate penetration; travel+0.11 produces79.687320 mm³ shaft/plate penetration. The negative fault is0.01 mm beyond the-0.1 endpoint; the positive fault is0.11 beyond the0 endpoint. These are deliberate geometric controls, not Ford service tolerances. This establishes provisional axial stops for this candidate; load, wear, press fits and retention under service remain unmodeled.

## Helical axial endpoints

`check-timing-thrust-land-helical-endpoints.py` checks25 crank angles across one tooth period at travel-0.1, with unchanged opposite half-speed cam phase. Travel0 inherits the frozen original25-pose proof through hash-bound subtractive refinement and the new addition's exact containment. AddedR26 material is at least52.62 mm from the crank tip, outside engagement.

At each of those25 rotations, the original engagement-region gap exceeds0.1 mm. Translation inX commutes with the fixedYZ overlap-lens clipping and remains inside itsX±8 bounds. Subtractive refinement cannot reduce the original gap; the added annulus is remote. The distance bound `original gap - 0.1` therefore establishes no intersection for **every axial position[-0.1,0] at those25 sampled rotations**. It does not establish every rotational phase. Endpoint results and minimum bounds are recorded separately in `inventory/engine/timing-thrust-land-helical-validation.json`; that report is required before combined candidate review. Prior finite loaded-contact phase brackets ataxial0 are not transferred toaxial-0.1.

## Reproduction and acceptance scope

From repo root with Python3.13/build123d0.10.0 pinned CAD environment, then system Python3 NumPy/Matplotlib for rendering:

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-timing-thrust-land-candidate.py
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-timing-thrust-land-helical-endpoints.py
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/prepare-timing-thrust-land-render.py
MPLCONFIGDIR=/tmp/truck-gear-mpl python3 scripts/render-timing-thrust-land-candidate.py
```

All sources/outputs use repo paths. Restore bound prior-core/refined-gear artifacts under repository artifact policy; no private source image is redistributed. Logs are `generated/timing-thrust-land-check.log` and `timing-thrust-land-helical-check.log`. The new render shows actual exported meshes and an actual CAD axial section, not a proposed sketch. Browser NOT RUN; installed block/cover interfaces remain FAIL from the prior core, with no attempt to fill old block bores.

| Gate | Scope |
|---|---|
| Application/coverage | Estimated backside correction; no factory claim; incomplete crank key remains |
| Dimensions/coordinates | Preserved source-classified plate/spacer/axial inputs; proposed land explicit estimate |
| CAD/export | PASS new gear and inherited unchanged exports |
| Internal axial interfaces | PASS all49 non-helical affected-pair interval certificates, stop faces and fault controls |
| Helical engagement | Separate25-pose axial endpoint/interval report required; no continuous rotation/load claim |
| Visual fidelity | Actual mesh/section review required; production backside comparison unavailable |
| Installed interfaces | FAIL/unadapted block/cover; no new acceptance |
| Motion/disassembly | Bounded axial/gear scope only; full system and disassembly NOT RUN |
| Learning/diagnostics | N/A developer candidate; not service guidance |
| Browser | NOT RUN |
| Reproduction/review | Hash-bound reports; root review pending |

Next action: root review of completed new reports and actual section/render before any further geometry. Issue32 stays open. No canonical promotion. Usage/model-effort unavailable.

## Completed delivery and integration tracking

Both reports completed and their bound dependency hashes were rechecked unchanged:

- Core/land report SHA256 `b5ccd40a0c2190918b1b586e79e18f9e7d6bb7342f2ebf78f2edd2e7f6beb928`.
- Helical endpoint report SHA256 `4eb7c3732b0b29c9565d7aa60d43bea87729dc0f9e819290a10f1eb7d82f6436`.

Shifted endpoint has zero overlap at all25 angles; local surface gaps range0.063162894–0.064800731 mm. The smallest full axial-interval gap lower bound at those sampled rotations is0.003283966 mm. This lower bound is geometric/numerical, not a service backlash specification. Endpoint0 remains inherited by the recorded proof chain. All50 affected pairs therefore have their declared bounded coverage; continuous rotation remains unproved.

New gear export:10,380 triangles, valid single solid, watertight; maximum mesh bounds error0.000334988 mm, STEP roundtrip volume difference8.74e-11 mm³. World STEP SHA256 `7fbfd7fbb3f3f31834847400b3cddde56a9a4619aa948682f2e8c24f2f169bc4`; GLB SHA256 `787d78d23105d797d5fb4912f7bb2aab52578014c476817c9a7f604c287afb36`.

Worker directly inspected `generated/timing-thrust-land-candidate/thrust-land-render.png`: front-core mesh, revised gear backside and actual planar CAD section make the land/plate/shaft arrangement and0.1-mm rest gap visible. The first3D section presentation overflowed its view; only the render was corrected to show actual section-face triangles in2D. Geometry/proof files did not change. Syntax checks passed. Root review of this new revision remains pending.

Root subsequently merged rear-only PR95 as `705c4683c199d8c5e28addba018bc8d1bdd399b1` and moved shared work to `engine/timing-core-pan-joint`. Current manifest remains `ab99fff2f63ad5dfc21fde8d12a32fc2a3d65832e6c8664baefd99d94403f7bf`; timing geometry unchanged. This is integration tracking only; historical proof inputs were not rebound. No CAD/check process remains running at delivery.
