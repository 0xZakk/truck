# Engine integration — 2026-10-03

**Engine unfinished; full goal active.** Preserve all eight systems in `inventory/engine/completion-plan.json`. Counts, isolated checks and candidate preservation are not completion percentages. The previous goal turn made progress: checked source/model deliveries were merged and artifacts published. No owner photograph is a prerequisite for continuing public-source research.

## Current checkout and integration ownership

Latest reviewed merge: [PR124](https://github.com/0xZakk/truck/pull/124), `aca7a20a98804563f90647c98d2ddfd89dcca184` (CI17s/18sPASS). Focused branch: `engine/fuel-exhaust-hosts-20261003`. Root alone edits shared manifests/builders/viewer and serializes integration. Preserve unrelated untracked electrical merge audits, aborted v4 reports and timing rear-flange review. Do not broad-add files.

Latest installed-content checkpoint remains PR110; later commits preserve research/candidates. Canonical `inventory/engine/full-assembly.json`: **741 definitions /1,349 occurrences**, SHA256 `91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6`. Navigation passes1,349parts/1,548links. The last installed static audit covers5,287 comparisons at one pose, not continuous motion or production accuracy. Combined STEP roundtrip maximum bounds difference0.000351mm. Rear exhaust-neck blend is latest installed geometry. Electrical lessons and oil-pump learning corrections are installed; no later pump, carrier, sensor or duct candidate is installed.

Private `inventory/engine/corrected-engine-stage-v4.json`: **747 definitions /1,361 occurrences**, SHA256 `9da33ca507e31cf6d906d4ee2c92b87a64ba01db7abea8f14b72f244631f9fe9`. It includes corrected crank/cam/drive direction and phase, inclined linkage, front-joint/seal changes, shifted ignition and estimated accessory carriers. It is not loaded by the viewer. Preserve `clockwise-inclined-v1`; reject mixed legacy motion metadata. V4 checks cover971 affected q0 pairs and8,166 pose frames; root reconciliation retains four older pump/cover/gasket conflicts. Six rod-bolt/block motion conflicts, tool access and source-fidelity gaps remain. See `accessory-stage-v4-integration.md`, `engine-clockwise-pose-candidate.md`, `rod-fastener-architecture-contract.md` under `docs/components/`.

## Active work — verify live registry and handles before action

Three assigned workers were running at the last checkpoint; do not infer that from this file alone or restart after an observation timeout.

| Worker | Scope and current evidence | Owned prefix |
|---|---|---|
| `pump_functional_junction` | Approved isolated coordinated pump/cover option B; build and affected checks running. Explicit estimated pose/footprint; original-size internals/hardware. | `pump-cover-candidate-20261003` |
| `act_second_view` | Intake candidate and whole-static validation frozen. One new rear-ear/return-line conflict plus old stud positions; researching fixed fuel-return interfaces. | `intake-return-interface-20261003` |
| `airbox_screw_finish` | 27-region HO2S candidate and conditional Walker host research frozen. Seeking bounded second view and reconciling actual manifold receivers before numeric pipe contract. | `ho2s-host-layout-20261003` |

Root approved the new pump **estimated**3mm functional backing contract after inspecting Carter rear/side views. This does not erase the historical14mm-slab FAIL or establish factory wall thickness. Keep nominal98.43mm replacement mounting height and98.552mm conversion sensitivity distinct. Do not carve pump geometry around an estimated carrier to obtain clearance.

## Current source/model checkpoints

- **ACT specimen:** six material regions, visible threads and source-compared probe/connector. Actual thread removal102.4705467mm³ and536 profile probes reject the failed smooth predecessor. Hidden leads/potting/chip, female gauge fit, engagement and installed pose remain unresolved. `act-online-20261002-delivery.md` and `act-host-online-20261002-contract.md`.
- **Paired intake ducts:** rounded bellows/shoulders, shaped bridge and retainer;12 exports, fresh passage/contact/section checks pass. Numeric contours, circular cuffs and body pose remain estimates. Exact-year host contract distinguishes two box screws/grommets from four body screws and records cuff stops/clocking. `airbox-refined-20261002-handoff.md`, `airbox-host-online-20261002-contract.md`.
- **Body screw:** Auveco13019/N610959-S2 isolated candidate;80body/20tip/936envelope probes and controls pass, export bounds0.00114mm. Four future occurrences have no accepted body coordinates/pilot/clip/stack. Root inspected actual catalog/render;56-member archive verified. `airbox-screw-online-20261002-handoff.md`.
- **Pump height trial3:** full52-part height candidate explicitly FAILS integration: four overlaps, protected rear-stock changes and six mesh-bound failures/open spring. Frozen studies remain unchanged; newer functional trial above supersedes neither whole-engine nor source acceptance. `pump-height-20261002-delivery.md`, `pump-junction-online-20261002-contract.md`.
- **Oil pump:** source-supported raised-neck mount/separate pickup flange contradict installed feet/inserted tube. Army C5AZ comparison distinguishes mounting/cover/inlet hardware and annular pin depiction. Ford hardware catalog verifies378644-S diameter12.7mm/length10.31875mm, not bore/split or exact truck applicability. Gasket aperture functions, block discharge and full pressure path remain unresolved. `oil-pump-topology-study.md`, `oilpump-dowel-20261002-evidence.md`.
- **Other unresolved scope:** production BOM/dimensions, rod fastener/seat and block cavity, bearing internals, pan/cover joints, accessory carriers/belt/tool access, airbox/body hosts, coolant/vacuum/fuel routes, MAP/cowl host, HO2S/exhaust-pipe host, harness/terminals, EGR outlet identity and manifold attachment stations. Consult the completion plan and relevant handoff; no system is Done.

## Verification, artifacts and tracking

Browser automation previously rejected localhost under its security policy; do not bypass via another surface. Browser selection/isolation/explosion/reset and recent installed content/motion remain **NOT RUN**. Historical preview server port8001/session47993 is not a current liveness claim. Test before reporting it running.

Restore exact generated artifacts via `docs/CAD-ARTIFACTS.md` and each package ledger. Published/server-digest verified: online research401293444; ACT401897025; refined ducts/failed pump-height401907524; host sensitivity402592725; body screw402597976. All are preservation releases, not installed acceptance. Source photographs, purchased manuals and raw manufacturer pixels are excluded. URLs/hashes and explicit access limitations remain in source ledgers. `kb/maps/online-engine-reconstruction-evidence.md` indexes the research.

Engine parent#1; active components include#32 timing/rods,#47water pump,#73oil pump,#80airbox,#82electrical. CLI issue/PR/release updates work. Project-column writes lack Projects scope; `project-status-pending.json` records intent with `applied:false`, not observed board state. No Done promotion without integration/browser evidence. No routine owner approval is needed for authorized work.

CAD environment: `.venv-cad`, Python3.13/build123d0.10/OCP7.8.1.1. Renderer uses system NumPy/Matplotlib; cached semantic model works with `HF_HUB_OFFLINE=1`. Model/effort/usage measurements unavailable; do not invent billing. Common exporter maps mmXYZ to meter(X,Z,−Y). Run only affected checks and verify actual inputs; never lower thresholds to accept a candidate.

Historical state is preserved in `docs/history/engine-state-through-20261003-pr120.md`. Read it only for a specific missing fact; current contracts and actual files/processes take precedence.

Pump preservation: root verified69 authored/135 generated/839 guarded hashes and streamed204-member archive; package ledger `reference/engine/pump-functional-20261003-package.json`. Published/server-verified release402605936. Do not install the five-clash/open-spring candidate.

## Reviewed successors preserved in PR124

- **Spring mesh:** original illustrative STEP unchanged; native full/segmented sweeps fail tessellation. Selected analytic tube/clip-cap GLB is one connected watertight component;500 original-STEP samples max0.005690mm, bounds0.0000569mm, ideal-surface interpolation bound0.010427mm. Adaptive STEP mass157.367943mm³ replaces unreliable default180.818697; selected mesh156.859991 differs0.323%. Earlier rejected flap mesh is5.56% low against adaptive mass. No installed spring or pump acceptance. See `pump-spring-sweep-20261003-handoff.md`.
- **HO2S:**27 exterior regions, finite geometry/thread/slot checks pass. Root inspected sensor/connector and verified107 archive members.22mm hex primary; other dimensions estimated. No target internals, complete lead, host or installed pose. Two swapped generic render captions recorded for next revision; frozen files preserved. `ho2s-specimen-20261003-handoff.md`.
- **Intake:** three coordinated valid solids/meshes with unequal source-derived joint spacing at estimated existing scale. Full gasket silhouette and omitted upper details remain gaps. Validation covers4062 static pairs;15 bounded head/injector/rail seats unchanged. Broad curved-region Boolean comparison genuinely fails.16 overlaps comprise15 old-stud conflicts plus295.587319mm³ rear H9-ear/fuel-return interference. Proposed stud poses are unaccepted hypotheses. Source-informed return routing next; no ear deletion to fit a provisional tube. `intake-joint-validation-20261003.md`.
- **Pump source registration:**18 authored/25 guarded hashes verified; proper45.124deg camera roll, source inlet arm broader/longer. Joint study14 authored/14 guarded verified; root inspected datum plot. Approved option B retains crank/pan/cover, estimates pumpYZ(-22.156967,193.467476), clock−5.641351deg and footprintscale1.061626. Outer-arch cam margin does not prove inner gasket/cavity clearance. Worker must check actual axial geometry. No shared integration change.

All candidate archive manifests and restoration instructions are in `docs/CAD-ARTIFACTS.md`. Release402624102 published; all five server hashes/bytes verified. No Done promotion. Root completed archive integrity and actual render review; three workers continue the next bounded tasks above. Check live registry before reporting ongoing work.

New host evidence: Ford1994 V5855-F and physical1987rail agree on front-side regulator, adjacent return run and paired upturned rear couplings. The current centered regulator/half-length line is contradicted; worker preparing coordinated numeric rail/regulator/coupling contract with protected injector/head mounts. Walker45166 primary dimensions/applicability and spherical joints are recorded; host remains conditional non-California, receiver3D/seat study active. New sources/notes indexed through the KB map.
