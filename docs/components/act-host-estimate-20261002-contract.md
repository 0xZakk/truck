# ACT host registration estimate — pre-CAD contract

## Scope recorded before modeling

Issue82; integration owner root, worker pump_foot_resume. Root authorizes a separate estimated host/sensor candidate only with declared source registration; if metric pose is not constrained, an explicit sensitivity study is authorized instead. This revision tests registration before any CAD mutation. Owned files use `act-host-estimate-20261002*`; canonical lower manifold, prior ACT specimen and all shared manifests remain frozen.

Inputs: exact-year service image736×328, `DM05Q313/ford10/147826554.png`; frozen ACT host evidence; canonical lower-manifold STEP and `efi_intake.py`; canonical manifest and private corrected-engine-stage-v4.json. The latter is context only, never an optimization target. Expected v4 hash `9da33ca507e31cf6d906d4ee2c92b87a64ba01db7abea8f14b72f244631f9fe9`.

## Declared registration and uncertainty

Manual source pixel picks, image origin upper-left: adjacent upper-port projected centers A(49,127), B(147,196); ACT boss center P(267,241); depicted sensor probe end T(420,156), connector center C(478,103). Each coordinate receives independent±4pixel sensitivity; this represents a deliberately broad image-picking bracket, not production tolerance. These approximate picks are preserved in the report for independent review.

A→B defines a projected longitudinal basis. Only under the explicit consecutive-runner correspondence assumption can it be assigned the provisional project pitch113.792mm. Its image-plane perpendicular is not a worldY or worldZ axis. Converted projected values are therefore illustrative projected-pitch units, never a recovered metric port center. The existing host uses front upper-runner center(284.48,−228,355..360), inferred geometry; registering P onto a chosen host surface is an additional assumption, not evidence from this basis.

Compare the exploded correspondence line P→T with actual sensor depiction T→C. Preserve disagreement; do not quietly choose the one that yields clearance. Show the standard orthographic nullspace explicitly: positions may translate along the viewing ray without changing pixels, and multiple out-of-plane sensor axes give the same projected direction. Numerical depth/axis samples illustrate nonuniqueness and are not claimed uncertainty endpoints from Ford.

## Gate before CAD

A port pose needs a supported camera/frame relation or a separately accepted explicit axis/depth assumption tied to actual host wall and air passage. If the source cannot supply that, deliver the reproducible sensitivity result with CAD/contact/flow/tool/neighbor checks NOT RUN. Do not fill the missing axis by clearance fitting. Preserve host flange/studs/injectors/rail and keep NPTF gauge plane, pressure sealing, connector clocking and hidden sensor circuitry unresolved.

## Planned checks

Deterministic pixel-corner sensitivity, projection nullspace residuals, and negative control with a visible image-plane offset. Source image and CAD/manifest hashes, actual host bounds and prior6-region specimen hashes will bind the report. No source pixels included in generated authored diagrams. No CAD edits unless this registration yields a defensible declared frame.
