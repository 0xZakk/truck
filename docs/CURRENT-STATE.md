# Engine integration — 2026-10-03 resumed

Engine unfinished; goal verified ACTIVE after user resume. Latest merged main is PR129, `c5f9d81a877a9d53c2a45984a20f4f2736785796`. PR129 preserves source reconciliation and rejected fuel candidates; it changes no canonical geometry. Current branch `engine/pressure-spring-20261003`. Root owns shared geometry, manifests, viewer and Git. Preserve unrelated local audits/candidates. Prior modeling cycle made concrete progress through source/candidate preservation in PR124/125 and measured CAD experiment PR126; none establishes engine completion.

## Installed versus candidate

Canonical `inventory/engine/full-assembly.json`:741 definitions/1,349 occurrences, SHA256 `91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6`. Latest installed-content checkpoint remains PR110. Later work is source research and separate candidates. Counts are not a completion percentage.

Private v4:747 definitions/1,361 occurrences, SHA256 `9da33ca507e31cf6d906d4ee2c92b87a64ba01db7abea8f14b72f244631f9fe9`. Corrected direction/phase/linkage, joints, ignition and accessory supports are not installed. Preserve `clockwise-inclined-v1`; six rod-bolt/block motion conflicts and source/interface gaps remain. Four older pump/cover/gasket overlaps are not the total failures in newer pump trials.

## Current bounded assignments

Live registry confirmed three newly dispatched workers; prior modeling processes were absent before dispatch. Check registry/processes before claiming continued work.

| Owner | Scope | Current action |
|---|---|---|
| resume_pump_fit | valve-spring-reconciliation-20261003 | Manufacturer intake/exhaust specifications audited; current spring geometry and volume conservation need correction. Inferred end-form comparison now proceeds to continuous transitions and global contact checks; no installed change. |
| resume_fuel_fit | fuel-rail-candidate-20261003 | r6 hose rejected: exported STEP contained only a socket fragment, invalidating its apparent clearance improvement. r6b complete hose independently replayed; both779-input context guards match. Export/coverage pass but full hose collides with upper intake by2894.916/3968.147mm³ in the two hypotheses. Source-led routing review continues; installation rejected. Lower regulator seal architecture remains unresolved. |
| resume_exhaust_fit | ho2s-host-candidate-20261003 | Corrected runner mesh passes, but inherited outlet-neck opening fails wall integrity. Root reviewed and authorized a separate estimated additive transition at Z205…230, preserving gas and outlet interfaces; new CAD and checks pending. |
| root | integration and independent review | Viewer HTTP200 verified19:47UTC. Reviewed exhaust neck contract and actual section; spring continuous-transition study dispatched. Canonical installation remains unchanged. |

Workers own their prefixes only; root reviews significant interface amendments before coupled CAD. Use public source research where evidence is missing. Source dimensions, replacement comparisons, estimates and unknowns remain distinct. Existing contracts are under `docs/components/`; original source images/manuals are excluded from commits/releases.

## Remaining engine scope

`inventory/engine/completion-plan.json` retains eight open systems. Key gaps: block/head passages and production contours; rod/fastener/cavity motion; bearing internals; oil-pump architecture and passages; pan/cover/pump joints; source-backed accessory mounts/belt/tool access; intake/fuel/vacuum/coolant routes; airbox/body mounting; sensors/hosts; harness/terminals; EGR/exhaust variant and joints. Candidate sensor/duct models exist even where older completion-plan prose still says absent; they are not accepted installations.

## Checks, preview and tracking

Viewer restarted on127.0.0.1:8001 via scripts/serve.py, process session26022; HTTP200 verified19:47UTC. This is a checkpoint, not perpetual liveness. Browser interaction acceptance remains NOT RUN after earlier browser security denial; do not bypass it. Native text-to-cad viewer worked for the isolated plug, not the engine website.

Navigation lastPASS1,349parts/1,548links. Whole-model counts/static passes do not prove factory fidelity or dynamic acceptance. Recheck input hashes before reusing reports. Use `.venv-cad` and existing exporter mmXYZ→meter(X,Z,-Y); plugin runtime differs and is optional, not a silent kernel replacement.

GitHub issue/PR/release operations work. Project-column writes remain unapplied without Project scope; do not claim column changes. Issues remain open until actual installed acceptance. Root can merge reviewed checked PRs without owner review.

CAD plugin comparison and measured tokens/time: `docs/benchmarks/text-to-cad-20261003/RESULTS.md`. Both isolated cups passed; first-run plugin slower/more total tokens with setup friction and denser mesh. Retain existing pipeline; use plugin inspection selectively. Generated archive release402640308 checksum verified. Earlier artifacts/reproduction are indexed in `docs/CAD-ARTIFACTS.md` and component handoffs.

Prior detailed checkpoint, including original failure history and source dependencies: `docs/history/engine-state-before-resume-20261003-pr126.md`. Read selectively. No system is Done.
