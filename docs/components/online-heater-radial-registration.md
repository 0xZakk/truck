# Component handoff: online heater radial registration

## Contract

Engine #47/#32 under engine #1; root integration owner. Read-only source follow-up to frozen online heater axial candidate. Own only `online-heater-radial-registration*` reports/reference directory/handoff and scripts with that prefix (renderer named `render-online-heater-radial-registration.py`). Baseline `dbe1e3c435c137fe2d30f6420db28476127c0f55`. No geometry, prior candidate, assembly, KB source or manifest changes.

Question: can four new actual GMB125-1810 manufacturer views identify radial length/azimuth, or do inherited dimensions and camera ambiguity prevent it? Existing source URLs and image hashes are bound through `reference/engine/online-heater-research.json`. Images are a replacement comparison; all millimeter normalization inherits estimated pump geometry.

## Findings

**The photos do not validate the frozen candidate's physical scale.** It remains a conditional axial-routing hypothesis with bounded static fit, not a dimensioned reconstruction. No new CAD is justified by this study alone.

The side photo gives a hub rim major axis approximately140px, minor22px, and mounting-to-pulley plane separation180px. For a scaled orthographic view of a circular hub normal to the shaft, `H/D = axial_projection / (major_diameter × sqrt(1 − (minor/major)²))`. NominalH/D is1.302. Explicit landmark perturbations (axial172..188, major134..146, minor16..28px) give1.185..1.435. The inherited143mm reference span and70mm modeled hub diameter give2.043 and predict282.45px axial separation. That discrepancy is much larger than the declared pixel uncertainty.

This rejects **that joint camera-plus-inherited-proportion model**, not every perspective camera or possible pump. The143mm input was an earlier photo reference span, not a measured face-to-face height; moving its endpoint from the modeled hub center to its seating face would not close this large ratio gap. Lens perspective, differing replacement proportions, hub-rim selection and estimated model dimensions remain alternatives. Do not attribute the whole0.687 radial factor to camera azimuth or adopt a replacement distributor dimension silently.

The rear photograph is the strongest mounting registration. All four small holes and distinct larger fifth opening are visible. Their declared IDs yield1.502px RMS against the inherited estimatedYZ pattern using an affine planar map. The next best small-hole permutation with fifth fixed has19.864px RMS; a direct swapped-hole control has51.201px. This supports the declared rear correspondence within this model, rather than an arbitrary near-fourfold hole permutation.

A conditional weak-perspective reconstruction of this rear view gives approximately230mm radial root-to-tip distance. In2,048 deterministic perturbations (mount centers±4px, tube centers±8px, prior axial endpoint range), radial length spans203.894..264.287mm and radial azimuth108.033..130.462°. These are **finite conditional sensitivity results**, not guaranteed physical bounds or manufacturing tolerances. The inherited205.901mm route is near the lower edge of this conditional range; the unforeshortened141.411mm side interpretation is not supported by this rear model.

Rear tube depth is still ambiguous: three axial tip depths −100,−26.967,+60mm relative to the mounting plane produce distinctYZ endpoints while projecting to the same observed rear tip within9e−14px. They are ambiguity witnesses for the rear camera only, not three proven all-view fits or installable alternatives.

The two front/oblique photos have hub/casting occlusion. Final overlay review corrected the oblique hole centers to (350,201), (502,263), (388,320)px and removed the mistaken fifth-hole assignment. Its visible pilot center is labeled separately from the hidden seating-plane center. Three tentative mounting correspondences merely interpolate an affine map and cannot validate it. Their incompatible conditional root estimates are retained as diagnostics; no low-residual claim hides the missing degrees of freedom. The side photograph lacks visible usable bolt centers and is tested through the separate circle/axis ratio. Thus all four views were used according to visible evidence, but an all-four calibrated metric registration was **not** achieved.

## Delivery and checks

- Run `python3 scripts/online-heater-radial-registration.py` for deterministic numerical report.
- Run `python3 scripts/render-online-heater-radial-registration.py` for the actual source landmark overlay.
- Report: `reference/engine/online-heater-radial-registration.json`; visual binding: `reference/engine/online-heater-radial-registration-visual.json`.
- Actual reviewed overlay: `reference/engine/online-heater-radial-registration/landmarks.png`. It contains manufacturer imagery and remains local-review-only, not approved redistribution.
- Environment: existing Python3.13/NumPy/Matplotlib. No package installation. Source image frames600×600pixels; local estimates explicitly separated from source observations. No engine-neighbor metric enters fitting.

| Gate | Result | Limit |
|---|---|---|
|Application/coverage|PASS scoped source use|Identified GMB product gallery; not owner's specimen identity|
|Dimensions/coordinates|FAIL common inherited weak-perspective model|H/D contradiction; conditional rear estimates only|
|CAD/export|N/A|No CAD changed|
|Source/visual|PASS inspected correspondences; full3D match NOT RUN|Four actual views, tentative occluded front IDs explicitly labeled|
|Installed interfaces|N/A new work|Frozen axial candidate's static gates unchanged; no acceptance promotion|
|Motion/disassembly|NOT RUN|No geometry/service claim|
|Learning/diagnostics|N/A unchanged|Existing new-source KB pages unchanged|
|Browser|NOT RUN|No installation|
|Reproduction/review|PASS local; root pending|Bound inputs, deterministic seed and index controls|

## Decision and next action

Keep the frozen axial candidate and its old failure history intact. Before a new metric route, jointly fit perspective cameras while allowing explicitly declared pump-proportion uncertainty, or obtain an applicable primary face-to-face/hub-diameter reference. The photos can guide topology and proportions but do not justify a measured tube length. No engine-clearance fitting, globalscale change, radial shortening or reclocking was made. No process remains running after render completion. Usage/model effort unavailable.
