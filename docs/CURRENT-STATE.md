# Current engine integration — 2026-09-30

Repository root is authoritative. Preview: http://127.0.0.1:8081/viewer/engine.html. Active branch: `engine/exhaust-timing-joints`. [PR #95](https://github.com/0xZakk/truck/pull/95) is in integration review; prior merged checkpoint is PR #94 / `124aa7c345af352459a800343ffc50f1e931367c`. **Engine unfinished. Browser acceptance for these batches remains NOT RUN.**

## Current installed checkpoint

**741 definitions / 1,349 occurrences.** Manifest SHA-256: `ab99fff2f63ad5dfc21fde8d12a32fc2a3d65832e6c8664baefd99d94403f7bf`.

The rear exhaust manifold now has a source-compared rounded collector and repaired runner exterior, retaining checked head, bolt, outlet and provisional EGR interfaces. Exact target STEP binding, watertight export, metadata preservation, baseline/target replay, rollback tests and 27 fresh neighbor comparisons pass. Ten promotion controls include changed canonical STEP/GLB rejection. The actual candidate/source comparison and section were reviewed. Its long neck, thin bolt lands and end EGR arrangement still differ from replacement photographs; no factory-casting acceptance or Done claim.

The earlier runner exterior, eleven-part illustrative EVR with five matched disc/spring poses, and illustrative throttle stops remain installed. Their historical reports retain their own input hashes and scopes. The four-part air-cleaner housing/filter/seal candidate is uninstalled.

- Current whole-engine static audit: **5,287 exact overlapping-bound comparisons, zero overlaps above 0.1 mm³**. Artifact, scale and hierarchy checks pass. This is one static pose, not continuous whole-engine motion or factory validation.
- Combined STEP: **1,349 unique occurrence names**, valid solids and matching world bounds; maximum roundtrip difference 0.000351 mm against 0.01 mm tolerance.
- Navigation: **1,349 parts / 1,548 links**, including the new source-linked exhaust lesson. Python syntax and existing numeric crank-motion checks pass. CI initially caught stale generated parts checklists; those were refreshed and the checks now pass.
- Browser automation rejected the localhost preview under its security policy. No alternate-surface bypass was attempted. CAD renders and Node checks do not replace selection, explosion/reset or installed-motion browser acceptance.

Root review: `inventory/engine/exhaust-timing-review.json`. Installed report: `inventory/engine/exhaust-rear-collector-installed-validation.json`. Detailed component handoffs preserve commands, hashes, assumptions and rejected trials. Full clean-clone CAD rebuild remains unproven. Production dimensions, calibration, mounting/routing and the remaining physical BOM stay open; part count is not a completion percentage.

## Separate timing studies and next work

Reviewed studies remain uninstalled:

- Manufacturer comparisons support a 58/29 replacement timing pair rather than the current 48/24 model. Its independent helical-pair and hub/key/mark studies pass scoped export and sampled engagement checks. Profile, helix, 121.8 mm shaft spacing and its direction remain estimates. The 122.0216 mm forum value is an unverified lead, not an adopted dimension.
- The cam-axis dependency audit covers bearings, tunnel, retention, rear plug, all twelve valve linkages, distributor/pump drive and surrounding passages. A common-rocker numerical hypothesis preserves pushrod length and closes the sampled linkages; nominal peak and full-curve differences remain unresolved. It does not prove CAD fit.
- Manufacturer images support a seven-hole open-bottom cover gasket and recessed shell. The original registration failed pan-terminal contact by 13.625/37.228 mm. The newer aperture-based estimate requires a wider/asymmetric front pan corridor; photo depth uncertainty remains unbounded. Manufacturer instructions distinguish front-segment service replacement from stacking a strip on an intact one-piece gasket.

Three workers own isolated files; root alone edits shared assembly/viewer data:

1. Timing core (#32): coordinated shaft/bearing/gear/retention candidate. The inherited gear-back relief fails to establish the stated endplay; an estimated rear thrust-land correction is being checked before any installation.
2. Cover/pan joint (#32): coordinated cover, gasket and local front-pan seating candidate using the explicitly estimated registration. Preserve the supported 25 pan-fastener count; prove sealing contacts, not merely absence of overlap.
3. Exhaust exterior (#46): an additional source-compared outlet blend candidate is undergoing exact interface/flow/neighbor checks. The port review found conflicting exact-year oxygen-sensor references; no spare boss is automatically labeled AIR or oxygen sensor.

Do not install these candidates or overwrite their files. Failed trials remain useful evidence. Worker completion alone does not establish accepted installation.

## Restoration and tracking

The [current private CAD archive](https://github.com/0xZakk/truck/releases/tag/checkpoint-2026-09-30-exhaust-timing) is published, with checksum and scope in `docs/cad-exhaust-timing-checkpoint.json`. It includes the installed rear collector and reviewed timing studies, but excludes ongoing timing-core and coordinated pan-joint candidates. Follow `docs/CAD-ARTIFACTS.md`. Browser meshes are committed. Source originals/composites, purchased manuals and owner photographs are excluded from Git and release archives.

CLI issue #46 has a verified refreshed parts checklist and installation update; #32 records the timing findings. PR #95 tracks the reviewed checkpoint. Project-column writes still lack Projects authorization. `inventory/engine/project-status-pending.json` records desired changes, **not observed board statuses**. No component was newly marked Done.
