# Paired intake duct refinement — candidate handoff

## Contract and identity

Issue #80 under engine #1. Baseline `54c2abf7aae73a8a5818321ee48ad81c8b7346ad`. Root integrates; inclined_linkage_resume owns this separate revision. See the pre-CAD [contract](airbox-refined-20261002-contract.md). Stable local region names are retained. No canonical/world assembly placement or existing candidate changes. Readiness: **candidate, local estimated specimen only**.

The identified E7TE source photographs4/6/12 support rounded bellows, bulged cuffs, gradual shoulders, a shaped bridge and an open flared retainer. Source URLs, image hashes and application limits remain in `reference/engine/online-airbox-research.json`; originals are excluded. Root compared the actual render and source views and found the contour revision visibly improved. This does not establish exact molded dimensions, material, insertion fit or a vehicle route.

## Delivered geometry

`cad/engine/airbox_refined_20261002.py`: `build()` returns the same twelve named regions as the predecessor. Two new tube skins use rational quadratic circular sections with cubic axial interpolation, then exact surface subdivision for manageable meshing. Tube centerlines, radii and contours remain estimates. Long/short projected X extents stay559/533mm; radial wall stays3mm. Straight cuff intervals and frames remain unchanged, so all eight clamp band/screw regions are imported from the exact frozen source STEPs. The web and retainer are new exterior-contact shapes. Manufacturing separation of those molded regions remains unknown.

No measured elliptical insertion profile can be inferred from the oblique photographs. Circular cuff sections therefore remain explicit assumptions. Bellows pitch/depth, free-state bend, collar bulge, web thickness/outline and retainer details are not factory dimensions. Four clamp screw mechanisms still omit functional threads and band slots. No dimensions were selected to fit the old airbox or throttle.

New outputs: `cad/engine/generated/airbox-refined-20261002/`. Individual GLBs use meters and `(X,Z,-Y)` mapping; STEP uses local CAD millimeters. The actual render `airbox-refined-20261002-source-view.png` shows the prior and new plan views at the same metric scale and a new oblique view. It contains no original photograph pixels.

## Checks and limits

| Gate | Result and scope |
|---|---|
| Application / physical coverage | Identified comparison specimen topology; owner-specific application/calibration and molded production details remain unknown. |
| Dimensions / frame | Explicit local estimated dimensions; no installed transform. Prior straight cuff regions retained for clamp reuse. |
| CAD / exports |12 valid single-solid STEP regions;12 watertight/winding-consistent positive meshes. Maximum CAD/GLB bounds discrepancy0.007150mm, below unchanged0.05mm gate. |
| Fresh passage / skin |936 long-tube and984 short-tube radial probes plus80 axis probes at80 declared sections; blocked-cuff and thin-wall controls detected. This is fresh evidence, not reuse of the old tube checks. |
| Continuous undeformed construction | Independent spline coefficient check proves positive inner radius bound25.499752mm and exactly3mm radial offset with the same axis. This bound is for the declared undeformed CAD construction, not flow pressure, sealing or flexible motion. |
| Independent volume | Adaptive STEP surface integration agrees with independent annular section integration to less than1e-12 relative error. Default nonadaptive volume differs by0.1213%/0.1079% and is retained as a numerical diagnostic; it is not the precise accepted volume metric. |
| Local neighbors |19 actual potentially overlapping pairs: zero intersection volume. Four band/cuff, both web/tube and retainer/long-tube contact distances are zero. Additional actual boundary-contact samples and shifted-contact control are bound by the section checker. |
| Source / visual |Actual depth-buffered GLB comparison reviewed. Rounded bellows, shoulders and waisted bridge improve the frozen baseline; circular sections, simplified lips, wall and all numeric contour estimates remain limitations. |
| Installed interfaces |NOT RUN: body/world frame and insertion fit unestablished. No airbox/throttle relocation, engine collision claim or installation. |
| Motion / disassembly |NOT RUN: no flexible material simulation, preload or extraction trajectory. |
| Learning |Frozen source/atomic notes remain valid; no installed lessons changed and no new unsupported repair thresholds. |
| Browser |NOT RUN; prior browser restriction remains. |
| Reproduction |Source/report/asset hashes in delivery and package metadata. Existing CAD runtime; no originals required for rebuild, but public views remain needed for independent source comparison. |

The initial native loft produced expensive degree14 polynomial circle approximations and a native export exit139. Historical source/log remain in the generated folder. Rational circular skins plus exact local patch subdivision resolved it without increasing mesh tolerances. A later relative-deflection export missed the retainer bounds gate by0.152389mm; switching to explicit absolute0.02mm mesh deflection passed the original gate. These failed attempts are not accepted geometry. A boundary `is_inside` diagnostic at the tube seam was inconsistent; actual point-to-solid distances and an offset-point negative control are used for contact evidence, with that diagnostic retained.

## Reproduction

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-airbox-refined-20261002.py
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-airbox-refined-20261002-sections.py
MPLCONFIGDIR=/tmp/truck-mpl XDG_CACHE_HOME=/tmp/truck-cache python3 scripts/render-airbox-refined-20261002.py
```

The main checker checkpoints export/probe stages. `--resume` requires exact module/contract/research/asset hashes, and only skips already completed stages. Fresh builds remain the default. The renderer uses the existing depth-buffered `scripts/engine_qc_raster.py`, system NumPy/Matplotlib/Numba, and trimesh from the pinned CAD environment. No threshold was loosened. Current model/usage accounting unavailable.

Preservation is authorized as an improved local specimen. Installed acceptance is not requested. Remaining work needs source-supported cuff/host registration and actual support/route evidence. No truck disassembly or owner input was requested in this task. No live process remains after the package completion reported in its separate metadata.
