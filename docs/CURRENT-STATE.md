# Engine integration — 2026-10-03 resumed

Engine unfinished; goal verified ACTIVE after user resume. Latest merged main is PR126, `5584306a595f87b60b29eca9ea82b527ade5ae98`. Current branch `engine/resume-integrations-20261003`. Root owns shared geometry, manifests, viewer and Git. Preserve unrelated local audits/candidates. Prior modeling cycle made concrete progress through source/candidate preservation in PR124/125 and measured CAD experiment PR126; none establishes engine completion.

## Installed versus candidate

Canonical `inventory/engine/full-assembly.json`:741 definitions/1,349 occurrences, SHA256 `91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6`. Latest installed-content checkpoint remains PR110. Later work is source research and separate candidates. Counts are not a completion percentage.

Private v4:747 definitions/1,361 occurrences, SHA256 `9da33ca507e31cf6d906d4ee2c92b87a64ba01db7abea8f14b72f244631f9fe9`. Corrected direction/phase/linkage, joints, ignition and accessory supports are not installed. Preserve `clockwise-inclined-v1`; six rod-bolt/block motion conflicts and source/interface gaps remain. Four older pump/cover/gasket overlaps are not the total failures in newer pump trials.

## Current bounded assignments

Live registry confirmed three newly dispatched workers; prior modeling processes were absent before dispatch. Check registry/processes before claiming continued work.

| Owner | Scope | Current action |
|---|---|---|
| resume_pump_fit | pump-cover-candidate-20261003 | Diagnose source registration versus block deck.59parts/788neighbor comparisons had14clashes. New block land crosses head/deck; no clearance-driven carving authorized. |
| resume_fuel_fit | fuel-rail-candidate-20261003 | Preserve both source-contract transverse hypotheses. r2 geometry exists; prior flow report is stale after failed bypass-control union. Repair and rerun checks against actual STEP. |
| resume_exhaust_fit | ho2s-host-candidate-20261003 | Resume approved conditional Walker pipe/spherical receivers and finite gas junction; inspect saved outputs before rebuild. |
| root | intake-gasket-outline-20261003 | Diagnose failed tessellation of full traced gasket before actual land/contact validation. |

Workers own their prefixes only; root reviews significant interface amendments before coupled CAD. Use public source research where evidence is missing. Source dimensions, replacement comparisons, estimates and unknowns remain distinct. Existing contracts are under `docs/components/`; original source images/manuals are excluded from commits/releases.

## Remaining engine scope

`inventory/engine/completion-plan.json` retains eight open systems. Key gaps: block/head passages and production contours; rod/fastener/cavity motion; bearing internals; oil-pump architecture and passages; pan/cover/pump joints; source-backed accessory mounts/belt/tool access; intake/fuel/vacuum/coolant routes; airbox/body mounting; sensors/hosts; harness/terminals; EGR/exhaust variant and joints. Candidate sensor/duct models exist even where older completion-plan prose still says absent; they are not accepted installations.

## Checks, preview and tracking

Viewer restarted on127.0.0.1:8001 via scripts/serve.py, process session26022; HTTP200 verified18:39UTC. This is a checkpoint, not perpetual liveness. Browser interaction acceptance remains NOT RUN after earlier browser security denial; do not bypass it. Native text-to-cad viewer worked for the isolated plug, not the engine website.

Navigation lastPASS1,349parts/1,548links. Whole-model counts/static passes do not prove factory fidelity or dynamic acceptance. Recheck input hashes before reusing reports. Use `.venv-cad` and existing exporter mmXYZ→meter(X,Z,-Y); plugin runtime differs and is optional, not a silent kernel replacement.

GitHub issue/PR/release operations work. Project-column writes remain unapplied without Project scope; do not claim column changes. Issues remain open until actual installed acceptance. Root can merge reviewed checked PRs without owner review.

CAD plugin comparison and measured tokens/time: `docs/benchmarks/text-to-cad-20261003/RESULTS.md`. Both isolated cups passed; first-run plugin slower/more total tokens with setup friction and denser mesh. Retain existing pipeline; use plugin inspection selectively. Generated archive release402640308 checksum verified. Earlier artifacts/reproduction are indexed in `docs/CAD-ARTIFACTS.md` and component handoffs.

Prior detailed checkpoint, including original failure history and source dependencies: `docs/history/engine-state-before-resume-20261003-pr126.md`. Read selectively. No system is Done.
