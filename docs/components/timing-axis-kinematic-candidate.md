# Timing-axis numeric feasibility candidate

## Contract

Issue #32 under #1; root integration owner requested a bounded same-ray121.8-mm study after reviewing `timing-axis-migration-plan.md`. Worker owns only `cad/engine/timing_axis_kinematic_candidate.py`, `scripts/check-timing-axis-kinematic-candidate.py`, `inventory/engine/timing-axis-kinematic-candidate-validation.json` and this handoff. Baseline commit124aa7c345af352459a800343ffc50f1e931367c / branch engine/exhaust-timing-joints; exact numeric source hashes are in the report. Root concurrently integrates rear exhaust. This work does not depend on its changed solids.

Readiness: **numeric research candidate**, not selected production datum or CAD installation. The121.8-mm center and same-ray direction are estimates; the122.0216-mm forum value remains an unused lead. Units are mm/degrees; X remains longitudinal. CamYZ95.109820990/76.087856792 gives deltaYZ5.109820990/4.087856792. Cover worker was notified; gear external envelope, X385.259375 and width14 are unchanged.

Fixed constraints: current head/valve axes Y-12 and valve baseZ261; replacement valve lengths120.6246/120.65; pushrod overall257.556 and modeled ball centers250.003354434; Melling intermediate shaft114.808; cam lift peak6.2738 and requested valve peak10.033. Source evidence remains replacement comparison, not verified installed identity. Rocker pad radius12, pad offset-1.5, current lifter cup construction, absolute valve/head datums and drive20°tilt/36-mm spacing remain existing estimates.

## Method and freedoms

Module `layout(shift=False)` extracts only the original `rest`/`solve` numeric function ASTs from `valve_source_layout.py`. It imports no CAD and never rewrites baseline sources. The checker verifies the reproduced baseline pivot51.0718402496 and rod ball-center length before evaluating the candidate. Cam law/firing order follows `valve_layout_integration.py`: twelve stations,1–5–3–6–2–4,720°cycle. Each station receives721 samples at1°including event peaks/edges/check-height phases. Sampling is discrete, not a continuous proof. Numeric closure/peak acceptance is1e-8 mm; shaft/drive arithmetic1e-9 mm. These are numerical identities, not manufacturing tolerances.

Candidate freedoms are lateral rocker pivot, rocker cup localZ and therefore lever arm/cup geometry. Lift and catalog rod length are not adjusted. The cup rises by4.087856792 from -5.421245566 to -1.333388773 relative to the rocker frame; lower ball rises to143.787856792 and moves toY95.109820990. Calibrating the intake gives pivotY54.008533957, approximately2.936694 mm outboard of current. Intake pivotZ stays395.1246; the common-rocker exhaust rest pivotZ is approximately395.134347. Thus this hypothesis does **not** call for translating the whole head or raising its valve seats.

One common calibrated pivot produces exhaust peak10.033134436 mm,0.000134436 above10.033; the current baseline already has0.000403853-mm excess. Neither residual is silently waived. Root rejected separate intake/exhaust pivots as a physical candidate. The active report now retains COMMON pivotY54.008533957 and identical rocker geometry. The prior separate-pivot comparison is archived under generated/timing-axis-kinematic-candidate/separate-pivot-rejected-comparison.json only. Exhaust peak and full-curve differences remain UNRESOLVED comparisons, not an exact source-lift pass or a tolerance waiver.

## Results and comparison

Report: `inventory/engine/timing-axis-kinematic-candidate-validation.json`.

- All12×721 numeric samples close within5.69e-14 mm; baseline worst error8.53e-14 mm. Intake calibrated peak10.033 mm within4.1e-14 mm; common-rocker exhaust10.033134436 mm; zero-lift residuals are floating-point scale.
- Full lift curves are **not identical**: maximum change0.021809698 mm intake /0.021947975 mm exhaust versus current. Catalog peak scalar and assumed cam law do not constrain the entire production lift curve. No full-curve preservation claim.
- Intake angle0–8.757946°; exhaust approximately-0.013587–8.744269°. These are equations of the estimated pad/cup linkage, not measured rocker travel.
- Keeping an old rocker top with the shifted lower rod ball causes at least4.034747-mm rod-length error across sampled cases. Leaving a bearing or drive frame unmoved creates6.543764-mm axis/frame mismatch. All three deliberate bad cases are detected; these are analytical consistency controls, not collision tests.

`drive(shift=False)` reproduces the current connected branch equations. Translating all branch frames by the same delta retains20°tilt,36-mm cam-to-drive spacing, fixed114.808-mm shaft and assumed socket engagements. Candidate distributor origin[227.584,158.010467521,143.649004399]; pump[224.084,65.730696691,-109.887582230]. Endpoint length error2.85e-14 mm. Rotating at current half-crank-speed leaves these axes invariant; valid crossed-helical tooth engagement/phase is still unproven. No torque, axial thrust or physical shaft fit claim.

## Required geometry changes and remaining gates

The dependency audit remains controlling: move/rebuild all four bearing interfaces and continuous block cam tunnel, rear plug seat, front stationary thrust plate sockets, complete lifter stacks/guide cutters. Head/gasket pushrod passages move outboard5.109821 mm; head pedestal axes move about2.9367 mm and need new socket/foot geometry. Revise rocker cup/arm and check its actual pad contact, guide, fulcrum/bolt, stem scrub and valve-cover clearance. Translating the distributor branch requires block boss/tunnel/clamp/pump feet, pickup start/outlet connection and ignition lead routing work. Fixed-length shaft preservation does not guarantee those new locations fit the block/pan.

| Quality gate | Status | Bound |
|---|---|---|
| Application/coverage | PASS bounded dependency/numeric scope | Dimensions remain comparisons/estimates |
| Dimensions/coordinates | PASS numeric constraints with declared freedoms | Production axes unknown; common-rocker nominal lift comparison unresolved |
| CAD/export; source/visual | N/A for numeric-only artifact | No solids or new render produced |
| Installed interfaces | NOT RUN | No CAD contact/clearance evaluation |
| Motion/disassembly | PASS sampled numeric closure only; disassembly NOT RUN | Neither continuous physical motion nor gear mesh certified |
| Learning/diagnostics | N/A developer feasibility study | Not service guidance |
| Browser | NOT RUN | No installed/browser changes; root security restriction remains |
| Reproduction/review | PASS execution and baseline numeric reproduction; root reviewed; common-rocker correction applied | Existing baseline tests/reports preserved untouched |

## Reproduction, review and restart

From repo root, standard Python3 only:

```sh
python3 scripts/check-timing-axis-kinematic-candidate.py
python3 -m py_compile cad/engine/timing_axis_kinematic_candidate.py scripts/check-timing-axis-kinematic-candidate.py
```

All outputs/inputs use repository paths; no credentials/private captures/CAD environment required. Root selected the common-rocker hypothesis for further isolated study, retaining unresolved nominal lift differences. Next action is bounded timing-core interface geometry, not canonical promotion. Issue32 remains open; no processes running. Model/effort/usage unavailable. No existing source-sized geometry, motion authority or tests modified.
