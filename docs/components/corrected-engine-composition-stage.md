# Component contract and handoff: corrected engine composition stage

## Contract and scope

Issue #32 under Engine #1. Root integration owner; baseline PR104 `8c2d2d9a1400acf784e04581a61e6a6ede38d3ba`. Canonical manifest SHA `91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6` remains unchanged. Owned composer, private manifest, dedicated frame checker/reports and this handoff. Workers own their source patches; root alone combines them.

Combine reviewed core, corrected physical slider phases, conditional drive relocation, front-joint, neutral linkage and head/gasket/rocker proposals without overwriting canonical meshes or inventory. Reject duplicate ownership, stale before values and changed asset hashes. Use original IDs/parents and definition-local STEP/GLB sources. This is an incomplete integration candidate, not a fallback definition of engine completion.

## Delivery

`python3 scripts/compose-corrected-engine-stage.py` writes `inventory/engine/corrected-engine-stage.json`: 742 definitions / 1,356 occurrences, including seven new main cover screws. Applies 21 definition proposals, 17 assembly proposals and 250 occurrence proposals; changes asset URLs only in private manifest to the bound staged files. No assets copied into canonical locations. All referenced occurrence parents/definitions resolve; IDs unique. Exact input hashes in `corrected-engine-stage-composition.json`.

`XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-corrected-engine-stage-frames.py` uses `assembly_clockwise_candidate.transforms`, not the old runtime. It compares actual staged core neutral matrices, corrected linkage frames, and distributor/oil branch phase relations over six event angles and two axial endpoints. 2,788 checks including 180 branch checks pass; maximum residual 5.685e-14. This checks geometry placement mathematics, not geometric clearance. Exact report bindings in `corrected-engine-stage-frame-validation.json`.

## Acceptance status and next work

| Gate | Result |
|---|---|
| Composition / identities / hashes | PASS for private stage |
| Motion matrices | PASS scoped comparisons above |
| Individual export integrity | Inherited bound candidate reports; whole combined STEP not yet exported |
| Actual neighboring geometry | FAIL: completed v1 audit has 77 overlaps across 2,212 pairs; inherited rod-bolt interference remains |
| Complete physical assembly | NOT COMPLETE: see open dependencies below |
| Learning / diagnostics | V2 adds 13 lessons and seven source records; navigation/reference checks pass |
| Browser | NOT RUN; no live viewer installation |
| Source / factory fidelity | Existing source classifications preserved; many estimates unresolved |

Open dependencies: main-cover gasket and terminal sealant; three-part 2692 seal and hub replacement; shifted pickup connection; missing pump gasket/discharge joint; inherited rod-bolt/block interference and unsourced bolt dimensions. Remaining whole-engine completion-plan items are not superseded by this stage.

The private manifest explicitly declares these limits. Do not point the legacy runtime at it: it requires the corrected motion revision, physical crank rest fields and new valve metadata. Next root step is to combine the missing dependency patches, re-run invalidated checks and connect the matching browser runtime. Independent worker checks may operate on this frozen manifest hash; regenerate invalidates them. No claim of installed acceptance or continuous collision-free operation.

Test environment: repository CAD lock on macOS and existing Node for source-patch generation. No purchased references or owner photographs copied. Model/effort and per-task billing unavailable. No process from these two commands remains running.

## Frozen v2 and audit follow-up

`compose-corrected-engine-sealing-stage.py` creates a separate v2 manifest with 747 definitions / 1,361 occurrences, without changing v1. It adds the main gasket, two terminal sealant deposits and the three-part seal/hub proposal. Composition checks bind every upstream patch and reject changed before-values. Candidate navigation checks all parts and the old seal alias; see `engine-stage-navigation.md`. Neither stage is loaded in atlas. The completed v1 audit and subsequent classification are preserved in `corrected-engine-changed-neighbor-audit.md`; v2-specific seal changes do not waive the other collisions. Follow-up repair work uses new files, preserving both frozen manifests.
