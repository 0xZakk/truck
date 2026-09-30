# Rear exhaust collector exterior candidate

## Contract

Issue46 under engine1 / exhaust9. Worker `evr_install_resume`; root integration owner. Research reviewed and isolated candidate authorized. Baseline commit `796b621244d8e341fe2f3c4de7af99488af01548`, branch `engine/runner-stops-and-evr`; frozen baseline manifest SHA256 `d748bcc9a38a592dc058bcf9c3a792a0dc59821a3bbd442cbcd73705a18569b9`. Source changes elsewhere are expected; scoped geometry/source hashes must remain stable.

Owned: `cad/engine/exhaust_rear_collector_candidate.py`, `scripts/check-exhaust-rear-collector-candidate.py`, `reference/engine/exhaust-rear-collector-review.json`, `inventory/engine/exhaust-rear-collector-validation.json`, this handoff and isolated ignored `cad/engine/generated/exhaust-rear-collector-candidate/`. No canonical exporter, assembly or component writes.

Scope: replace the flat-sided box collector with a continuous rounded, varying-section collector and blend toward the existing middle discharge. Preserve three head entry/land interfaces, two bolt15/16 mounts, outlet/flange below the collector and the provisional EGR end-bore. Do not relocate the EGR line, identify auxiliary bosses by guesswork, add plugs or certify the entire casting. All new dimensions remain estimated; Dorman674-186 is replacement comparison, not installed casting identification.

Units mm; baseline part geometry is already in its existing CAD coordinates. Use existing occurrence and ancestor transforms exactly once. Named interfaces: `cylinder-head`, `efi-lower-intake`, `efi-head-intake-gasket`, `rear-manifold-bolt15`, `rear-manifold-bolt16`, `egr-tube-manifold-fitting` and attached EGR tube; downstream two-hole flange retained. Fresh spatial neighbor discovery uses every current occurrence, then freezes relevant STEP/GLB inputs.

Evidence: actual source pixels inspected in `reference/engine/dorman-674186-{front,back,three-quarter}.jpg`; application and manufacturer source hashes in `reference/engine/dorman-674186-profile-reviewed.json`. Views show three rounded-rectangular entries, rounded branches and a bulky blended central neck; auxiliary plugged bosses lie near the outlet. They do not provide dimensional scale. The retained left-end EGR connection is an explicit source discrepancy.

Planned checks before acceptance: valid single solid; STEP roundtrip symmetric difference<0.02mm3 and GLB watertight/bounds<0.2mm; protected interface symmetric differences<0.001mm3; connected open gas-witness network obstruction<0.001mm3; sampled positive wall material with missing-wall fault; deliberately blocked passage and shifted-interface controls; candidate/current-neighbor overlaps<=0.1mm3 (historical engine audit convention, not production tolerance). Inspect actual CAD/mesh source comparison and section; no claim of continuous wall-thickness proof, CFD, thermal performance or pressure sealing. Browser/installed acceptance NOT RUN.

## Status and accepted scope

**PASS isolated candidate; root review pending. Not installed.** Valid one-solid BRep and STEP roundtrip difference0 mm³. Exact head/bolt, outlet/flange and EGR protected-region differences0 mm³; independently derived full EGR end-wall/seat difference0 and full bore obstruction0. Connected gas witness and all three original runner-lumen obstructions0. All32 collector wall samples and18 additional repaired-runner sidewall samples pass. Blocked passage, removed wall and shifted interface controls remain active. All27 exact current-neighbor overlaps0 (29 spatial candidates), including tube, fitting, sleeve and bolts15/16. Full continuous wall thickness, CFD and installed/browser checks were NOT RUN.

Final refined GLB: watertight,64,894 triangles,0 degenerate faces,0 duplicate faces; CAD/mesh bounds error0.002314 mm. CAD volume change from tessellation cleanup0. Standard coarse export is retained as `standard-export.glb`:15,800 triangles and4 degenerate faces, not watertight. The candidate checker uses the existing exporter, preserves that raw output, then clears triangulation with `BRepTools.Clean_s`, tessellates at .05 mm/.1 rad and merges vertices/removes degenerate and duplicate faces/unreferenced vertices. It reopens and validates the resulting GLB. No hole filling or shared exporter edit was made. Final triangle metadata is bound in validation.

## Runner repair and EGR interface proof

The original rectangular-to-round entry transition and complete gas void export watertight independently; the inherited18 mm outer swept bend does not, despite BRep validity. `scripts/check-exhaust-rear-runner-seam.py` reproduces that diagnosis. A six-section ruled exterior loft at path parameters .27,.40,.55,.70,.85,1 replaces that provisional exterior while retaining the original gas void. Eighteen .35 mm-radius material samples at ±16.5 mm from branch centers verify sidewalls away from intended collector openings. This is finite sampling, not a global minimum-thickness certificate.

Root authorized a functional preservation-mask refinement, with independent feature checks: old EGR study box X[−318,−264],Y[−230,−130],Z[180,280] included the unrelated defective runner surface at Z255.923–256.978. New box X[−318,−264],Y[−205,−155],Z[204,255] retains the full actual interface with margin. Entire fitting bounds are X[−315.688,−280.188],Y[−193.856407,−166.143593],Z[214,246] (minimum margin2.312 mm). Bore bounds are X[−286.688,−269.688],Y[−192.1,−167.9],Z[217.9,242.1] (5.688 mm). Independently derived full end-wall/seat envelope is X[−286.688,−268.688],Y[−204,−156],Z[206,254] (1 mm). Its original/repaired symmetric difference0; full bore obstruction0. This alters the study's unrelated exterior repair scope, not check tolerances or the EGR connection.

Rejected first candidate/report/export and failed fine export are preserved in ignored `rejected-v1/`. Smooth/ruled replacements with oversized EGR patch failed BRep validity; logs and debug candidates remain beside it. No failure has been relabeled as a pass. A later coarse-export failure is preserved as `rejected-standard-repaired-validation.json`. Successful reports bind only the repaired candidate.

## Visual review and unresolved evidence

Actual final exported meshes and Dorman front/back/three-quarter pixels were inspected in `source-comparison.png` and `section-review.png`. Rounded arm walls and center swelling improve the old box silhouette. Retained long outlet neck, head lands, skinny bolt arms and end EGR patch still differ visibly from replacement casting photographs. All new section sizes and6 mm nominal radial wall reduction remain estimates; no calibrated photograph overlay or production dimension claim is made. The half-view clips triangles at Y−180; jagged cut edges are a rendering artifact, not an exact CAD section. Keep issue46 open.

## Reproduction and ownership

Additional owned scripts are `scripts/check-exhaust-rear-collector-export.py`, `scripts/check-exhaust-rear-runner-seam.py` and `scripts/render-exhaust-rear-collector.py`. No canonical/shared files were edited. Environment: Python3.13.12,build123d0.10.0,cadquery-ocp7.8.1.1.post1,trimesh4.7.4,numpy2.5.3; system matplotlib for renders.

```sh
.venv-cad/bin/python scripts/check-exhaust-rear-collector-candidate.py
.venv-cad/bin/python scripts/check-exhaust-rear-runner-seam.py
.venv-cad/bin/python scripts/check-exhaust-rear-collector-export.py
PYTHONPATH=.venv-cad/lib/python3.13/site-packages MPLCONFIGDIR=cad/engine/generated/exhaust-rear-collector-candidate/mpl python3 scripts/render-exhaust-rear-collector.py
```

All commands now pass. Numerical report: `inventory/engine/exhaust-rear-collector-validation.json`. Review binds the reports, render hashes, source hashes, exact interface bounds, failure history and limits: `reference/engine/exhaust-rear-collector-review.json`. Isolated ignored directory contains frozen baseline STEP/GLB/manifest, candidate exports, logs, diagnostics and renders. Source originals and source-comparison composites must not enter Git or releases.

Relevant input and neighbor artifacts plus scoped occurrence/definition/world transforms are frozen in validation. `full_engine.define` is hashed specifically because root concurrently changed unrelated integration hooks; this is scoped isolated exporter evidence, not a whole-builder rebuild claim. A fresh installation check remains mandatory.

Root next action: review this bounded exterior study and source limitations. If accepted for integration, a narrow rear-only .05 mm/.1 rad triangulation and mesh cleanup path is required, with independently verified CAD preservation and updated triangle metadata; unchanged coarse export is not accepted. Then restage against current neighbors and run installed/browser checks. No canonical apply command is supplied by this candidate worker.

Final STEP SHA256 `90b2a67a3288849aa019bbfc12b0dbeb86fa01a3eb5a2cd7e2ec10826cfd1b72`; GLB SHA256 `2525dc9ac3b0fba6d7a2c17e4f037eb8acd34ae46347865362640e0ec2408a5e`. Full hashes and limits remain in the bound reports.
