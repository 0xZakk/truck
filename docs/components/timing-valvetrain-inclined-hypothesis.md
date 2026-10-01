# Component contract and handoff: inclined pushrod hypothesis

## Contract

- Issue32; root owns integration. Baseline8547c589d3c086bad91baf879219612bcd9a162f / engine/timing-support-joints; unchanged canonical manifest91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6.
- Root requested a bounded numerical alternative before sealing-land redesign: retain upper socket near existingY90, shift lower lifter socket to new axisY95.109820990, preserve source-sized rod length and valve axes, solve common rocker geometry without scaling lift. No new head/cover/gasket or rocker CAD.
- Own new timing_valvetrain_inclined_hypothesis.py, check-timing-valvetrain-inclined-hypothesis.py, timing-valvetrain-inclined-hypothesis-validation.json and this handoff. Frozen vertical hypothesis, pedestal-only candidate and reports unchanged.
- Compare upperY90 exactly and an explicitly unselectedY88 sensitivity case. Millimeters; compensated rigid cam phase remains inherited. Cup height follows actual ball-center length and inclined rest triangle; pivot follows nominal intake comparison through the geometric linkage equations. Exhaust residual remains explicit.
- Acceptance: reproduce zero-lash length closure across all12 branches and integer0..720 crank with both axial endpoints; quantify tube envelope at gasket/head-floor/cover planes. This is finite-phase numerical feasibility, not CAD contact, continuous clearance, production timing or selected geometry.

## Evidence

Source rod overall length, assumed ball/oil-bore geometry, hypothetical catalog-constrained cam profile and valve lengths remain those in the frozen contract. No evidence requires the modeled pushrod to be vertical at rest. Inclination is a new geometric hypothesis, not identification of owner hardware. ExistingR6/Y90 passage andY98 cover inner boundary are model constraints, not manufacturer measurements.

## Delivery

Run `.venv-cad/bin/python scripts/check-timing-valvetrain-inclined-hypothesis.py`. No geometry, exports, browser or installation. Results pending below.

## Reproduced numeric results and next scope

The checker completed for both hypotheses. Selected-for-review Y90 layout gives pivotY50.894736783789 and cup-localZ-1.385614068820; source rod length and valve axes remain unchanged. Across all twelve branches, integer crank0–720 and axial0/-0.1, maximum closure error is8.53e-14 mm. Intake nominal peak is10.033 mm; exhaust residual is+0.000202686604 mm. Maximum full-curve change from the frozen vertical hypothesis is0.005532872155 mm, not a claim that either law is production-accurate.

The existingR6/Y90 aperture sufficient gap is-0.878087055992 mm at worldZ254, -0.847297741818 at255.5, +0.145257029136 at304, and +0.747477838149 at333.5. Thus the inclined rod still requires a lower head/gasket change, while the unchanged upper passage clears its sampled tube envelope and its positiveY tube extent remains below the current cover land. These are numeric tube sections, not rocker/spring/cover CAD acceptance.

The separate [lower passage/deck scope proposal](timing-valvetrain-inclined-scope.md) records read-only actual lifter STEP bounds, a proposed local upper-guide transition and required protected-interface gates. Its report is `inventory/engine/timing-valvetrain-inclined-scope-validation.json`; no neighbor geometry has changed. Y88 remains an unselected sensitivity case. Browser, CAD export, physical mating and installation remain NOT RUN.
