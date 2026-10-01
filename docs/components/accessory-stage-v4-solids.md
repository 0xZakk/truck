# Component contract and handoff: accessory stage v4 solids

## Contract

- Issues #32/#34 under engine #1; integration owner: root. Baseline `ddcfeee76009f1666be55098f6a0baf8c8049377`.
- Read-only candidate audit of `corrected-engine-stage-v4.json`, SHA `9da33ca507e31cf6d906d4ee2c92b87a64ba01db7abea8f14b72f244631f9fe9`; canonical is unchanged.
- Owned: `scripts/check-accessory-stage-v4-solids.py`, this handoff, `inventory/engine/accessory-stage-v4-solids*`, `cad/engine/generated/accessory-stage-v4-solids*`.
- Exact coordinated contract supplies 173 moved occurrences, two replacement carriers, full guarded pose rows and delivery hashes. World CAD units mm; q=0, axial=0, default compressor state. Actual local STEP assets are transformed with the opt-in clockwise adapter, including deformed spring CAD.
- Whole-stage broadphase uses actual STEP conservative bounds with 2 mm pair padding. Surviving affected pairs receive exact intersections. Historical threshold remains 0.1 mm³. No mate whitelist. Internal rigid relations require identical STEP hashes and relative matrices; inherited classification does not mean accepted geometry. The completed run had already tested all 705 unchanged same-group pairs before the reuse instruction arrived; their hash/relative-frame classification remains explicit and no repeat run is needed.
- Cube-overlap control checks detection. Every intersection/metric exception remains explicit. No distance, support contact, thread, tool, continuous motion, belt or containment acceptance is claimed.
- Shape and frame fidelity remain the estimates and unknowns in the coordinated contract. No new factory dimensions or production claims.

## Delivery

Run `.venv-cad/bin/python scripts/check-accessory-stage-v4-solids.py` from repository root. Uses existing macOS Python 3.13/build123d 0.10 environment; no installation. Report binds checker, manifests, contract, adapter dependencies and actual STEP inputs; final hash recheck detects mid-run changes. Generated collision STEP files use world millimeters and retain pair IDs. Original interrupted loading pass is preserved; it performed no pair checks and is not evidence of acceptance.

Completed session 71863, exit 0; log `cad/engine/generated/accessory-stage-v4-solids.log`. The redundant restart session 59690 was stopped during loading, exit 130. No process remains running. No geometry changes or canonical writes. Report scope is finite static affected solids only. Browser remains NOT RUN under the existing restriction. Learning content unchanged; source fidelity, service, structure and external connections remain open.


## Validation and review

`inventory/engine/accessory-stage-v4-solids.json`, SHA `ad84a41d2137b22b54ba91ce025b1533a7dcef699bd32c7db4b3fa4bdd9244bb`, binds 769 inputs, all rechecked unchanged. Summary: `inventory/engine/accessory-stage-v4-solids-summary.json`.

971 exact STEP pairs completed: 266 changed interfaces and 705 already-computed unchanged internal relations. All measured overlap volumes are zero; no metric errors. The 2 mm padded broadphase separated another 221,804 affected pairs using actual conservative STEP bounds. Unaffected pairs are outside this audit, so unrelated v3 failures remain. The deliberately coincident 1 mm cubes measure 1 mm³ and trigger the unchanged 0.1 mm³ criterion.

| Gate | Result | Evidence / limitation |
|---|---|---|
| Application/coverage | NOT RUN | Existing inferred accessory identities/geometry retained; no production survey |
| Dimensions/coordinates | PASS scoped | Guarded full pose rows, all q0 frames, exact carrier asset hashes; mm units |
| CAD/export | PASS scoped | All 1,361 actual posed solids valid/nonempty; no export change |
| Source/visual comparison | NOT RUN | Existing carrier reviews remain separate; no new assembled render |
| Installed interfaces | PASS static solids only | 266 fresh and 705 inherited exact pairs; contact and 1 mm reserve not tested here |
| Motion/disassembly | NOT RUN | q0 only; seven PS/AC installed tool failures and alternate-pump lower-bolt failures remain |
| Learning/diagnostics | N/A unchanged | This audit does not change user-facing content |
| Browser integration | NOT RUN | Existing browser restriction; no installation |
| Reproduction/review | PASS reproduction; review pending | Hash bindings and Python syntax verified; root review pending |

No replacement shape, support, manifest or runtime was written. Current-v3 pump is used, not alternate inlet hypotheses. Six inherited rod-bolt/block motion conflicts, unrelated v3 static conflicts, tool access, incomplete retention, belt travel and external connections remain open. Root owns combining this evidence with contact/export/service reports and deciding any further private-stage use. Static zero overlap does not close those gates.

## Tracking and restart

Study complete; no further solver or geometry search authorized by this handoff. Root next action: review the summary and coordinate other gate reports. No process running. Model/effort and usage unavailable. Both loading-only aborted reports/logs are preserved and are not acceptance evidence.


Root-requested actual-pipeline control is separate from the frozen 971-pair report: `scripts/check-accessory-stage-v4-solids-fault.py` restores only the AC front cylinder to its old v3 frame, retaining actual v4 cylinder/cover assets. It enters the same 2 mm padded broadphase and measures **17,596.474199263692 mm³** overlap, detecting the pose fault. Report `inventory/engine/accessory-stage-v4-solids-fault.json` binds both manifests/assets and exports the exact world STEP witness under the main output folder. Session 40199 completed exit 0; no process running. This supplements the original cube control without changing the completed audit.
