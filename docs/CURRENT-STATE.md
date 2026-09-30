# Current engine integration — 2026-09-30

Repository root is authoritative. Preview: http://127.0.0.1:8081/viewer/engine.html. Active branch: `engine/timing-core-pan-joint`. Saved checkpoint: merged [PR #95](https://github.com/0xZakk/truck/pull/95), commit `705c4683c199d8c5e28addba018bc8d1bdd399b1`. **Engine unfinished. Browser acceptance for these batches remains NOT RUN.**

## Current installed checkpoint

**741 definitions / 1,349 occurrences.** Manifest SHA-256: `91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6`.

The rear exhaust manifold now has a source-compared rounded collector and repaired runner exterior, retaining checked head, bolt, outlet and provisional EGR interfaces. Exact target STEP binding, watertight export, metadata preservation, baseline/target replay, rollback tests and 27 fresh neighbor comparisons pass. Ten promotion controls include changed canonical STEP/GLB rejection. The actual candidate/source comparison and section were reviewed. A further reviewed neck blend is now installed with 12 promotion controls, 65,670 watertight triangles and 27 fresh zero-overlap neighbor checks. Thin bolt lands, the end EGR arrangement and outlet dimensions still differ or remain unverified; no factory-casting acceptance or Done claim.

The earlier runner exterior, eleven-part illustrative EVR with five matched disc/spring poses, and illustrative throttle stops remain installed. Their historical reports retain their own input hashes and scopes. The four-part air-cleaner housing/filter/seal candidate is uninstalled.

- Previous whole-engine static audit: **5,287 exact overlapping-bound comparisons, zero overlaps above 0.1 mm³**. Artifact, scale and hierarchy checks pass. This is one static pose, not continuous whole-engine motion or factory validation. `rear-neck-static-reuse.json` verifies 740 unchanged STEP definitions/frames and fresh checks for the sole changed rear manifold; no redundant whole-engine audit is claimed.
- Current combined STEP: **1,349 unique occurrence names**, valid solids and matching world bounds; maximum roundtrip difference 0.000351 mm against 0.01 mm tolerance. Combined STEP regenerated successfully for the installed neck update.
- Navigation: **1,349 parts / 1,548 links**, including the new source-linked exhaust lesson. Python syntax and existing numeric crank-motion checks pass. CI initially caught stale generated parts checklists; those were refreshed and the checks now pass.
- Browser automation rejected the localhost preview under its security policy. No alternate-surface bypass was attempted. CAD renders and Node checks do not replace selection, explosion/reset or installed-motion browser acceptance.

Root review: `inventory/engine/exhaust-timing-review.json`. Installed report: `inventory/engine/exhaust-rear-collector-installed-validation.json`. Detailed component handoffs preserve commands, hashes, assumptions and rejected trials. Full clean-clone CAD rebuild remains unproven. Production dimensions, calibration, mounting/routing and the remaining physical BOM stay open; part count is not a completion percentage.

## Separate timing studies and next work

Reviewed studies remain uninstalled:

- Manufacturer comparisons support a 58/29 replacement timing pair rather than the current 48/24 model. Its independent helical-pair and hub/key/mark studies pass scoped export and sampled engagement checks. Profile, helix, 121.8 mm shaft spacing and its direction remain estimates. The 122.0216 mm forum value is an unverified lead, not an adopted dimension.
- The cam-axis dependency audit covers bearings, tunnel, retention, rear plug, all twelve valve linkages, distributor/pump drive and surrounding passages. A common-rocker numerical hypothesis preserves pushrod length and closes the sampled linkages; nominal peak and full-curve differences remain unresolved. It does not prove CAD fit.
- Manufacturer images support a seven-hole open-bottom cover gasket and recessed shell. The original registration failed pan-terminal contact by 13.625/37.228 mm. The newer aperture-based estimate requires a wider/asymmetric front pan corridor; photo depth uncertainty remains unbounded. Manufacturer instructions distinguish front-segment service replacement from stacking a strip on an intact one-piece gasket.

Three workers own isolated files; root alone edits shared assembly/viewer data:

1. Timing block (#32): baseline regeneration matches the installed block exactly. A bounded cam-side feature migration is being checked. The isolated thrust-land correction passed its limited core/endplay checks; all remain uninstalled.
2. Cover/pan joint (#32): coordinated cover, gasket and local front-pan seating candidate using the explicitly estimated registration. Preserve the supported 25 pan-fastener count; prove sealing contacts, not merely absence of overlap.
3. Gear backlash (#32): the exact-year manual calls for0.0508–0.1016mm; the old estimated pair gives0.22675–0.25510mm of sampled pitch-circle free play. Indicator setup interpretation is explicit. A distinct revised pair is being checked, including axial/rotational coupling; old evidence is preserved. Rear outlet blend (#46) is installed but its browser/production gates remain open. Port research found conflicting exact-year oxygen-sensor references; no spare boss is automatically labeled AIR or oxygen sensor.

Do not install these candidates or overwrite their files. Failed trials remain useful evidence. Worker completion alone does not establish accepted installation.

## Restoration and tracking

The [current private CAD archive](https://github.com/0xZakk/truck/releases/tag/checkpoint-2026-09-30-neck-core) is published, with checksum and scope in `docs/cad-neck-core-checkpoint.json`. It includes the installed rear-neck blend, isolated timing core/thrust land and rejected old-gear backlash diagnostic, but excludes ongoing shifted-block, coordinated pan-joint and revised-backlash candidates. Follow `docs/CAD-ARTIFACTS.md`. Browser meshes are committed. Source originals/composites, purchased manuals and owner photographs are excluded from Git and release archives.

CLI issue #46 has a verified refreshed parts checklist and installation update; #32 records the timing findings. PR #95 is merged; the next candidates remain separate and the further neck installation is saved in PR #96, whose checks pass; merge is pending the final checkpoint review. Project-column writes still lack Projects authorization. `inventory/engine/project-status-pending.json` records desired changes, **not observed board statuses**. No component was newly marked Done.
