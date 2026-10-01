# Current engine integration — 2026-10-01

Active branch: `engine/timing-drive-fit`, baseline merged [PR108](https://github.com/0xZakk/truck/pull/108), `2c4c65de787834445ec999757cb7a2572a1f1bde`. Root is the sole shared assembly/viewer integration owner. **Engine unfinished; current timing/motion candidates are not installed.**

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

Root v2 sealing delta checked62 fresh pairs: seal/hub affected static neighbors clear, but the new main gasket has seven conflicts (water-pump gasket and six compressor parts). Seventy-five unchanged v1 failures remain, for82 known v2 static conflicting pairs. See `corrected-stage-v2-sealing-summary.json`.

V3 now incorporates the28 ignition definition corrections with unchanged transforms. Root replay passes28 world mesh/STEP checks (max0.006735mm), four corruption controls and all navigation/learning checks. Its365 clear affected-neighbor comparisons supersede56 ignition pairs, leaving26 known static pairs. See `corrected-stage-v3-remaining-conflicts.json`. Canonical remains unchanged.

Three workers currently handle engine-control learning, a constrained accessory layout, and water-pump heater-route source reconciliation. Root owns shared assembly/runtime, evidence review, preservation and CLI tracking. No source uncertainty may be hidden by moving neighboring parts.

- Closure coverage: PR107 preserves MPS126/MPS59A isolated cup candidates and an MPE107R replacement-kit comparison. Five MPS126, one MPS59A and two MPP554 are missing from installed coverage; existing MPC147 is counted once. Cup walls are estimated; plug sites/host interfaces remain unknown. This is not a complete OEM BOM.
- Oil pump: the source-supported raised-neck/flanged-pickup architecture contradicts the current installed mounting-foot/tube-insertion assumptions. The new topology study deliberately omits unknown discharge and mount details and is noninstallable. Rod-fastener architecture remains measurement-dependent; see `rod-fastener-architecture-contract.md`.
- Electrical map: root independently inspected EVTM pages74–78/81/82/298 and accepted14 connector interfaces/33 contact mappings as bounded research. Supply361, sensor return359, oxygen ground89 and heater ground57 remain distinct. The manual's conflicting S122/S136 supply reference is preserved explicitly. See `engine-control-electrical-map-root-review.json`.
- Water pump: corrected heater root/contact/wall and all four pump-tool envelopes pass locally. The frozen source-estimated tube intersects the head, rail, exhaust, lifting eye and stud13. Side-photo axial calibration is uncertain; source reconciliation precedes another route. See `waterpump-heater-source-delivery.json`. Earlier inlet-angle/offset sensitivities and main3 tool failure remain open.
- Accessories: both source gasket images corroborate the broad cover contour, so narrowing it to clear the compressor was rejected. A new coupled center-layout study has47 clear scoped STEP comparisons, but replacement carriers are excluded obligations and belt effective-radius/tensioner assumptions remain inferred. No layout has been installed.

Root reviewed actual composed cam, front-joint, gasket/terminal and pickup renders. Scoped review records are `cam-composed-drive-root-review.json` and `composed-stage-root-visual-review.json`. Appearance does not waive collisions, unknown production contours or browser checks.

## Archives and GitHub tracking

Installed checkpoint: [neck-core](https://github.com/0xZakk/truck/releases/tag/checkpoint-2026-09-30-neck-core). Follow the ordered private study archive chain in `docs/CAD-ARTIFACTS.md`; these preserve candidates, not accepted installations.

Latest merged PR104 is `8c2d2d9a1400acf784e04581a61e6a6ede38d3ba`. Its cam/cover archive is published: 62 files / 22,441,296 bytes; SHA `f67121592b2de92346eecb1d750cd49bc2bbfc3cb35bbc14a95dfd8c2b075b3f`. PR105 merged after both CI checks passed (16 seconds each). Its [composed-engine archive](https://github.com/0xZakk/truck/releases/tag/studies-2026-10-01-composed-engine) is published; server digest/size verified: 181 files / 60,749,763 bytes, SHA `11596222af342b6bdfc461bdbe9b52f39a358a30966879eeac6e30fa208b33d0`. Supplemental guard render is a separate verified release asset. Its exact file allowlist and hashes are in `docs/cad-composed-engine-checkpoint.json`.

Project-column writes lack Projects token scope. `inventory/engine/project-status-pending.json` holds desired changes, not observed statuses. CLI issue/PR/release updates work. No new component is Done. Do not imply autonomous execution continues after the goal/session actually stops.

Latest merged checkpoint: PR106 head `68205ab3b258c0fdd74719f79165d1c4a0d8523c`, squash `e6dc8fcd68e28ff201ee2cd9b69aee0bb8a588eb`. CI19s/16sPASS. Ignition archive64files/17,370,033bytes, SHA `25bae3deb1d29d8395c9f17b2cf035f959b0c6b7b51d166de32766fb7919d920`, published and verified. V3 remains a private candidate, not loaded in atlas; canonical741/1349unchanged. CLI issues32/47/51/73/76 updated; Projects scope rechecked2026-10-01 and still absent.


Latest preservation checkpoint: PR107 merged at `6b1608257e8c2eaa12512ac0c256d882854f3996` after both CI checks passed. The block-closures/oil-pump topology archive is published and server-verified:13files/361,986bytes, SHA `9def0caead5bf2cb64711df05cbfccf47ac909fe78a8cae8dc998c7d9eddb96a`. It preserves candidate assets, not new installed geometry.

Electrical viewer content now adds11 existing component lessons without replacing mechanical content or changing the canonical manifest. Page-specific manual links and navigation pass automated checks. Browser verification remains NOT RUN; see `docs/components/engine-control-electrical-integration.md`. MAP/IAT/O2 physical models remain missing.

PR108 electrical-content integration merged after CI22s/18sPASS and independent runtime review. Five prior mechanical lessons preserved, six injector lessons added;30 supplemental part links resolve in canonical and privatev3. Both geometry manifests unchanged. Local preview is listening at127.0.0.1:8001 (server session47993); this process observation is not browser acceptance. Three workers continue ALT/AP carrier geometry, pump-bearing coverage and frozen pump artifact preservation.
