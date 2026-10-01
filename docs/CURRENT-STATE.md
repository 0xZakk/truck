# Current engine integration — 2026-10-01

Active branch: `engine/timing-drive-fit`, baseline merged [PR103](https://github.com/0xZakk/truck/pull/103), `26d0fdc4e7cdd3de0c621309499d1535d8c5131e`. Root is the sole shared assembly/viewer integration owner. **Engine unfinished; current timing/motion candidates are not installed.**

## Installed baseline

741 definitions / 1,349 occurrences. Canonical manifest SHA-256 `91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6`.

Rear exhaust neck blend is the latest installed geometry. Source-compared runner exterior, eleven-part illustrative EVR, throttle stops and earlier detailed components remain installed with their recorded limitations. The four-part air-cleaner candidate remains separate. Production dimensions, complete physical BOM, emissions calibration and owner-photo fidelity are unresolved; modeled count is not completion percentage.

- Last whole-engine static audit: 5,287 exact comparisons, zero overlaps above 0.1 mm³ in one pose. `rear-neck-static-reuse.json` binds 740 unchanged definitions/frames plus fresh checks for the changed rear manifold. No continuous whole-engine motion inference.
- Combined STEP has 1,349 uniquely named occurrences; maximum world-bounds roundtrip difference 0.000351 mm. Current navigation checks pass 1,349 parts / 1,548 links.
- Browser automation rejected localhost under its security policy. No alternate-surface bypass. Browser selection/isolation/explosion/reset and installed motion remain NOT RUN for recent batches.
- A full clean-clone CAD rebuild remains unproven; restore exact artifacts via `docs/CAD-ARTIFACTS.md`. Purchased manuals and owner photographs are not distributed.

## Frozen timing preparation

The 58/29 replacement-comparison gear pair, revised cam-axis/core placement, inclined valve linkages, corrected rocker crests, pump-foot support, front-block/pan candidates and 2692 seal remain separate. Their scoped results and failures are bound to exact inputs; do not install an isolated piece into incompatible old geometry. `inventory/engine/timing-integration-map.json` lists 188 affected valve-train poses, core/drive dependencies and relocated pan fasteners.

PR102 preserves the coordinated block v3 / pan v2 joint. Actual block/pan/gasket and both relocated block-owned screws have zero overlap; backing, female cavities, floors, protected interfaces and exports pass. Aggregate block validation remains FAIL because two total-volume metrics do not converge at the unchanged strict criterion. Preserve that limitation and the rejected earlier trials.

The separate 2692 case/elastomer/garter-spring study has source-sized replacement envelopes and explicitly estimated internals/registration. It passes scoped contacts, exports and continuous local hub rotation with conservative axial sensitivity. Five cover/hub/seal assets are localized for later integration; old `front-seal` links need an assembly alias. Three individual lessons are drafted. This is not whole-engine thrust, seal-pressure or factory-contour acceptance.

## Reviewed work preserved in PR103

- **Crank correction:** exact original-source replay matches canonical geometry. The candidate reverses four throw rest phases, preserves end and main-journal interfaces, and exports a valid single solid/watertight mesh. Actual crank/rod/piston axes close over 721 poses × 6 cylinders, maximum error 8.30e-12 mm; wrong-direction control separates them by 101.092 mm. All 48 sampled block/pan comparisons clear; whole-engine continuous motion remains open. Root inspected actual full old/new meshes. See `docs/components/crank-clockwise-candidate.md`.
- **Direction evidence/helper:** qualified exact-year diagram and corroborating Ford front-face drawing support clockwise crank rotation from the front. Keep positive event time and firing order while correcting physical crank/cam phases; distributor remains clockwise from its cap. The helper rejects the old crank's cylinders 2–5. Twenty-six corrected timing-gear samples clear, with wrong-sign/axial/double-phase controls failing. See `engine-rotation-convention-research.md` and `engine-clockwise-pose-candidate.md` under `docs/components/`.
- **Pan contact:** a conservative 1.2813 mm lower contact route surrounds the wet opening and excludes all 25 bolt holes. Upper joined contact is a manifold annular surface with local retained support and a terminal sealant bridge. Full-face unsupported overhang remains recorded; rear arch is illustratively owned by block extension rather than rear main cap. No pressure/containment/production ownership claim. Root inspected actual route/section renders. See `timing-pan-perimeter-contact-study.md` and `timing-pan-upper-contact-study.md`.
- **Pan integration stage:** guarded proposal changes three assets and ten fastener poses, preserves IDs/parents/other occurrences and the existing washer. Serialized replay checks 52 world STEP/mesh bounds and rejects stale inputs. No canonical changes. See `docs/components/timing-pan-integration-stage.md`.

Root review: `inventory/engine/timing-motion-contact-root-review.json`. New motion/contact archive metadata: `docs/cad-motion-contact-checkpoint.json`; publication and uploaded digest/size verified after PR103 CI passed.

## Current integration work

Frozen corrected cam/contact/sections and crossed-drive pair/endplay are candidate deliveries. Root reviewed actual cam, crossed-gear and pan21 renders plus bound reports. Corrected pair clears 17 nominal samples and nine endplay samples; wrong-phase controls penetrate. The bounded −0.1 mm rear-stop correction is −0.351213° at the distributor. This is inferred gear registration, not a production setting.

Root's isolated JS helper matches CAD across 3,768 valve/linkage states, 942 rod/piston frames and 314 shaft-angle pairs. It is not loaded by atlas. See `docs/components/clockwise-browser-motion-candidate.md`.

Three workers remain active: combined moving assembly/rod-bolt conflict, full cam composition with corrected crossed gear, and broader seven-main-cover-block guards. Six repeated rod-bolt/block collisions were found and confirmed in the inherited baseline; assumed bolt geometry is being audited before repair. Pan21 Y−95 candidate passes its local gates, but main-cover support changes touch broader protected stock zones and require explicit review. No failure is waived or silently repaired.

Root owns eventual combined manifest, placement, lessons and runtime. Installation still requires matched complete neighborhood and affected checks; browser acceptance remains NOT RUN. No promotion from worker PASS.

## Archives and GitHub tracking

Current installed archive: [neck-core](https://github.com/0xZakk/truck/releases/tag/checkpoint-2026-09-30-neck-core). Published study chain: timing-fit → timing-proof → timing-support → timing-clearance → timing-interfaces → [pan-seal](https://github.com/0xZakk/truck/releases/tag/studies-2026-10-01-pan-seal). Restore instructions/checksums: `docs/CAD-ARTIFACTS.md`.

PR102 final-head CI passed; private pan/seal archive digest/size and non-draft publication verified (123 files / 33,127,925 bytes; SHA-256 `5b46ae082c6ea9fe23d67b44b26578e1473fe2d2a13ac92cbae8953904b52fe8`). Issues [32](https://github.com/0xZakk/truck/issues/32#issuecomment-5934674332) and [34](https://github.com/0xZakk/truck/issues/34#issuecomment-5934687416) record that checkpoint.

Project-column writes lack Projects token scope. `inventory/engine/project-status-pending.json` holds desired changes, not observed statuses. CLI issue/PR/release updates work. No new component is Done. Do not imply autonomous execution continues after the goal/session actually stops.


Latest checkpoint: PR103 head `1440853952cd132e17693c6355c38bcb0f9276b4` merged as `26d0fdc4e7cdd3de0c621309499d1535d8c5131e`. Published motion/contact archive has 89 files / 6,756,376 bytes, SHA-256 `2be3c16b8274c0b06c30eb0aa78c2e3ead383d80eb009fc46ae82368c6468f93`. Canonical manifest remains unchanged.

Next preservation checkpoint: cam/cover archive prepared with 62 files / 22,441,296 bytes; publication pending. Active combined motion, composed cam and broader block guards are excluded. Last issue32 CLI update: https://github.com/0xZakk/truck/issues/32#issuecomment-5935432381 .
