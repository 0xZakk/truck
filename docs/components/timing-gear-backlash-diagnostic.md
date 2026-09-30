# Component handoff: timing-gear backlash diagnostic

## Contract

Issue #32 under engine #1. Root is investigator and integration owner. Branch `engine/timing-core-pan-joint`, baseline `705c4683c199d8c5e28addba018bc8d1bdd399b1`; canonical manifest `ab99fff2f63ad5dfc21fde8d12a32fc2a3d65832e6c8664baefd99d94403f7bf` remains unchanged. This is a research diagnostic of the frozen independent 58/29 gear pair, not new CAD or installed acceptance.

Owned files: this handoff, `reference/engine/timing-gear-backlash-review.json`, `scripts/check-timing-gear-backlash-diagnostic.py`, its `inventory/engine/timing-gear-backlash-diagnostic.json` report and generated log. The source HTML capture is ignored. Earlier gear/core/thrust reports and geometry remain frozen. No shared geometry changes are authorized by this diagnostic.

Inputs are the original isolated crank/cam STEP pair and parameter module, restored via the private September 30 exhaust/timing archive. CAD axes remain X longitudinal; crank at YZ0 and estimated cam YZ95.109821/76.087857. Millimeter units. Crank orientation is fixed at each sampled phase; cam moves toward both flank contacts with axial position held. A previously proven tip-cylinder overlap lens limits expensive comparisons. The checker records source and STEP hashes and requires free configurations with positive gap and interfering configurations with overlap above 1e-5 mm³. It does not treat the engine's unrelated 0.1 mm³ whole-assembly threshold as a tooth-contact threshold.

## Evidence

Exact-year service information specifies 0.002–0.004 inch backlash (0.0508–0.1016 mm), checked by dial indicator while holding the gear against the block. The excerpt does not state the indicator radius or direction; the pitch-circle comparison remains an explicit interpretation. The separate crankshaft timing key is source-supported; its dimensions and shape remain unknown.

[KHK's gear reference](https://khkgears.net/new/gear_knowledge/gear_technical_reference/gear_backlash.html) distinguishes pitch-circle rotational travel from normal clearance and adds the two gears' tooth-thinning contributions. The current module subtracts 0.12 mm from each gear's pitch-circle tooth thickness: ideal pair play is consequently 0.24 mm. An unloaded single-pose nearest-surface gap is not a service backlash measurement. The actual polygonal helical CAD must be evaluated independently.

Source paths, hashes, applicability and interpretation are in `reference/engine/timing-gear-backlash-review.json`. Factory excerpts, manufacturer captures and diagrams are not redistributed.

## Delivery and validation

Command: `XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-timing-gear-backlash-diagnostic.py`. Existing locked macOS Python 3.13/build123d environment; no dependency changes. Log: `cad/engine/generated/timing-gear-backlash-diagnostic.log`.

The diagnostic uses two crank phases, four signed cam offsets per phase and exact CAD intersections. Its negative conditions are the deliberately interfering offsets on both sides. This brackets angular lost motion and converts it using the hypothesized cam pitch radius. It neither proves continuous contact nor predicts loaded gear behavior.

| Gate | State and scope |
|---|---|
| Application/coverage | PASS exact-year service range; indicator setup still incompletely documented |
| Dimensions/coordinates | Existing estimated pair frame; pitch-circle interpretation explicitly provisional |
| CAD/export | N/A new export; read-only frozen STEP diagnostic |
| Visual fidelity | N/A new shape; previous source comparisons remain limited |
| Installed interfaces | NOT RUN; pair remains uninstalled |
| Motion | PASS finite two-sided contact bracketing; FAIL service-range comparison under the stated interpretation |
| Learning/diagnostics | Research evidence only, not yet a user lesson |
| Browser | NOT RUN; no browser claim |
| Reproduction/review | PASS input hashes stable and report reviewed by root |

## Tracking and restart

Issue remains open. The report brackets total angular play at 0.16–0.18 degrees, or 0.226753–0.255097 mm at the estimated 81.2 mm cam pitch radius, at both sampled crank phases. Both signs have a free and an interfering witness. This exceeds the service range under the stated measurement interpretation. Root reviewed the report; the calculation is not a production-gear acceptance. Preserve the old pair as a rejected service-clearance hypothesis; create a distinct candidate if revision is needed. Any revision invalidates tooth engagement and axial travel proofs for that gear, while unrelated core/block checks remain reusable by hash. Model/effort/usage unavailable. No production manufacturing specifications are inferred from a successful clearance fit.
