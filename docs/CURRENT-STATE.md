# Current engine integration — 2026-10-01

Active branch: `engine/timing-drive-fit`, baseline merged [PR104](https://github.com/0xZakk/truck/pull/104), `8c2d2d9a1400acf784e04581a61e6a6ede38d3ba`. Root is the sole shared assembly/viewer integration owner. **Engine unfinished; current timing/motion candidates are not installed.**

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

Frozen private stage v2 (`inventory/engine/corrected-engine-stage-v2.json`) has **747 definitions / 1,361 occurrences**, 13 new lessons and seven source records. It composes corrected crank/cam, inclined linkage poses, relocated drive branch, coordinated front joint, seven main-cover screws, gasket/terminal sealant and a three-part 2692 front seal. Canonical remains unchanged. The stage is an incomplete candidate, not an installed engine.

- Corrected CAD runtime passes 3,696 independent frame checks; staged manifest checks pass 2,788 comparisons, including 180 distributor/pump branch checks. JS helper matches CAD over 3,768 valve/linkage states, 942 slider frames and 314 shaft pairs. Neither candidate JS helper nor navigation is loaded by atlas.
- Candidate navigation passes 1,361 parts / 1,561 nodes, 174 resolved lessons and 417 links. Old `front-seal` links resolve to its new three-part assembly. `stage=timing` links are preparatory, not a live viewer mode. See `docs/components/engine-stage-navigation.md`.
- Independent v1 changed-neighbor audit finished **2,212 exact comparisons / 77 positive overlaps / zero metric exceptions**. All 74 comparable pairs freshly clear in canonical; three new screw pairs have no canonical equivalent. Private stage remains FAIL. See `docs/components/corrected-engine-changed-neighbor-audit.md`; preserve its v1 input hash.
- Failures comprise 56 shifted distributor/lead pairs, six block/compressor pairs, twelve cover-neighbor pairs and three main-screw-neighbor pairs. Block/compressor conflicts are mostly inherited from earlier V3 candidate stock; one piston conflict is entirely new station-six support and shaft conflict is mixed. Canonical is not implicated by those candidate overlaps.
- Combined moving geometry also confirms six inherited rod-bolt/block collisions. Exact-year/ARP comparison research indicates the current assumed bolt architecture needs revision; no defensible complete dimensional repair exists yet.
- Pickup reconnection study passes its bounded geometric gates, but later Ford pump drawings show a flange/gasket architecture missing from the current pump. It remains an illustrative study. See `oil-pump-discharge-source-audit.md` under component handoffs.

Three workers currently handle distributor-end ignition connections, compressor/block interface provenance, and bounded water-pump rear-flange geometry. Root owns combined manifest/runtime, visual review, archival preservation and CLI tracking. Rear pump/cover contact estimates must preserve axes and complete attachment lands; forward inlet interference remains separate. Active repairs cannot overwrite frozen audit inputs.

Root reviewed actual composed cam, front-joint, gasket/terminal and pickup renders. Scoped review records are `cam-composed-drive-root-review.json` and `composed-stage-root-visual-review.json`. Appearance does not waive collisions, unknown production contours or browser checks.

## Archives and GitHub tracking

Installed checkpoint: [neck-core](https://github.com/0xZakk/truck/releases/tag/checkpoint-2026-09-30-neck-core). Follow the ordered private study archive chain in `docs/CAD-ARTIFACTS.md`; these preserve candidates, not accepted installations.

Latest merged PR104 is `8c2d2d9a1400acf784e04581a61e6a6ede38d3ba`. Its cam/cover archive is published: 62 files / 22,441,296 bytes; SHA `f67121592b2de92346eecb1d750cd49bc2bbfc3cb35bbc14a95dfd8c2b075b3f`. The next composed-engine archive is locally packaged; publication is not yet confirmed. Its exact file allowlist and hashes are in `docs/cad-composed-engine-checkpoint.json`.

Project-column writes lack Projects token scope. `inventory/engine/project-status-pending.json` holds desired changes, not observed statuses. CLI issue/PR/release updates work. No new component is Done. Do not imply autonomous execution continues after the goal/session actually stops.
