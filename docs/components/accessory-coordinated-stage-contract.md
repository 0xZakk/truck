# Coordinated accessory stage contract

## Contract and evidence

Root owns composition under engine #1, accessory/timing #34/#32. This is a guarded private-stage contract only. Owned files are this document and `inventory/engine/accessory-coordinated-stage-contract.json`. Baseline commit and exact dependencies are in that JSON. No CAD, manifest, viewer, archive or frozen report changed.

Target only frozen `inventory/engine/corrected-engine-stage-v3.json`, SHA `f512d6024ed4d3d0d86c45c39492b4ab525e039a9c50fb71b67940633b8a2055`. Abort on any different input or before-row mismatch. Both final carrier deliveries and constrained-layout delivery were checked: 193 file/hash claims match. PS/AC delivery SHA is `354af3408e8c8c41bd618d19345aabe340ea65d72822e308097f7dd4ba84761e`.

The selected accessory centers, carrier dimensions and routes remain inferred. Existing reports establish bounded candidate fit, not factory casting identity, complete retention, structural strength, belt fit or connected plumbing. Applicable source topology and replacement comparisons retain their original transfer limits.

## Exact carrier frames

| Stable definition and occurrence ID | Original parent | Original definition assets | Replacement |
|---|---|---|---|
| `alternator-thermactor-common-carrier` | `accessory-drive` | `/cad/engine/generated/alternator-thermactor-common-carrier.step`, `/models/engine/alternator-thermactor-common-carrier.glb` | `cad/engine/generated/accessory-matched-carriers/trial6-carrier.{step,glb}` |
| `ps-ac-support-bracket` | `accessory-support-brackets` | `/cad/engine/generated/ps-ac-support-bracket.step`, `/models/engine/ps-ac-support-bracket.glb` | `cad/engine/generated/accessory-psac-carrier/trial1-carrier.{step,glb}` |

Both occurrence transforms are position `[0,0,0]`, rotation `[0,0,0]`. Their complete parent chains through accessory-drive and engine have identity transforms and no motion. Both replacements are already **world CAD millimeters**. Preserve occurrence identity, parent and explode vectors. GLB vertices already use `(X,Z,-Y)/1000`; do not recenter them or convert units twice. The JSON records full original definition/occurrence rows, parent chains and replacement hashes. Root must refresh definition geometry metrics and estimated-layout wording rather than retain stale original bounds or claims that all old stations remain unchanged.

## Guarded pose changes

Apply the 17 full before/after rows in JSON as one operation with both carrier replacements: six assembly positions and eleven occurrence positions. Preserve other fields. The five ownership groups contain ALT 28, AP 17, PS 49, AC 71 and TENS 8 occurrences, totaling 173.

| Group | World translation X,Y,Z in mm |
|---|---|
| ALT | 0, 62.98796098825028, −76.43015331067244 |
| AP | 0, 78.16748851222079, 24.39372811097425 |
| PS | 0, 9.501109043944268, −63.43625338556751 |
| AC | 0, 57.43537535946626, 40 |
| TENS | 0, −37.50181014323476, −33.72225338556751 |

AC parent changes from `[373.56,280,100]` to `[373.56,337.43537535946626,140]`. Its children retain local geometry, phases and motion axes. Adding the same shift to its children would double-translate them. Tensioner pulley and support are separate sibling roots and both move once. Nine separately parented ALT/PS/AC bolts move with their accessory. The two `thermactor-engine-bolt-*` occurrences counter-transform the AP parent translation, preserving their fixed engine seats.

Do not shift either new carrier: its moved ear coordinates and fixed engine feet are already built into the exported solid. World deltas can be added to local positions only because the relevant ancestors are unrotated here; a future rotated ancestor would require inverse-frame conversion.

## Independent review and minimum combined checks

Read-only replay of the root checker calculation, stopping before its write operation, reproduced all 8,166 occurrence-frame comparisons across six frozen motion states and matched recorded edits and both fault dictionaries. Direct parent-chain inspection independently confirms the carrier identity frames. The checker is sound for its declared pose scope. It does not inspect replacement geometry or establish continuous motion.

The JSON provides a concrete checker scope:

1. Guard exact manifest, full before rows, carrier assets and final delivery hashes. Reject duplicate ownership or missing definitions.
2. Replay all frames at six declared states. Keep missing fixed-bolt counter-transform and double AC translation controls. Add a world-carrier double-translation control.
3. Inspect actual STEP/GLB placement, units, world bounds and topology after composition; reuse original export tolerances without weakening them.
4. Recompute affected broadphase for all 173 moved occurrences plus both carriers against the whole frozen stage and one another. Test surviving STEP pairs; keep 0.1 mm³ overlap threshold and 1 mm nonmating carrier reserve. Explicitly classify mates and suspicious metric zeros. Same rigid-branch invariants may be reused only with unchanged hashes/relative frames.
5. Rebind eight ALT/AP seats, twelve PS/AC seats, fifteen PS/AC clamp annuli, holes and blind floors. Replay separated-seat controls and all tool witnesses. Include actual opposite-carrier separation.
6. Review actual exported assembled views. Keep new pump and rear-cover variants in separate conditional checks; use the actual v3 pump for the primary stage. No rejected heater route installation.

Relevant neighbors include block/head, v3 cover/pan/seal, pump/pulley, accessory hardware, and nearby ignition/exhaust/intake. Whole-stage broadphase prevents a short manually chosen list from missing newly approached parts. External interfaces also move: AC suction/discharge, PS outlet, Thermactor plumbing and ALT/AC wiring need later endpoint contracts. No complete connected belt, hoses or harness is established here.

## Retained failures and acceptance

- Three PS and four AC installed straight tool approaches hit pulleys. Conditional pulley removal does not prove a service procedure.
- ALT/AP lower engine bolt approach fails all three new pump inlet hypotheses; current v3 pump approach clears.
- Six inherited rod-bolt/block motion conflicts remain outside this change. The 26 v3 static conflicts are a baseline requiring affected-pair reclassification, not the new stage's presumed final count.
- Preserve the PS/AC invalid raw pump distance result. Only its independent exact partition/bounds certificate may support clearance, with unchanged inputs and frames.
- Factory silhouette, threaded retention, loads, tensioner stops/preload/travel, effective belt geometry, hoses/wiring and source-supported service removal remain open.

Frame/guard review: PASS scoped. New combined solid/contact/export checks: NOT RUN. Source fidelity: estimated, not promoted. Browser: NOT RUN under existing restriction. No installed acceptance or automatic component completion.

## Delivery and restart

The JSON is the machine-readable contract; it includes exact input hashes, full before/after pose rows, original carrier metadata and a minimal checker specification. No standalone modeling or build entry point is introduced. Environment for read-only pose replay: existing Python 3.13 CAD venv; standard Python for hash/contract checks. No package installation. Usage/model effort unavailable.

Root next action: compose a distinct private stage using the guarded rows and both assets, then run the combined checker and review actual export views. Do not mutate v3 or supersede its failures merely because pose parity passes. No process remains running.
