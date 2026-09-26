# Oil-fill neck illustrative mate: contract and handoff

## Contract

- Issue: #15, engine oil filler cap; integration owner is the parent engine task.
- Baseline: `2cc2000f876901d76a12fbe251f03103a0e516de`, branch `engine/next-interface-contracts`. Exact manifest and CAD input hashes are recorded by the checker.
- Scope: isolated candidate feasibility study. No installed cap, cover, assembly manifest or browser assets are changed. Own this document, `cad/engine/oil_fill_neck_candidate.py`, `scripts/check-oil-fill-neck-candidate.py`, and `inventory/engine/oil-fill-neck-candidate-validation.json`; evidence is in the two oil-fill-neck research files.
- Identity: exact 1994 archive cover service number F3TZ6582H; current illustrative shape is not a manufacturing drawing of that part. EC743-style pilot cap retains its existing assumed 4.5 mm pitch.
- Coordinates: millimeters, world CAD Z up. Cap origin `(240,-12,419)`, neck axis `(240,-12)`, top Z413, bottom Z399. Study geometry is world placed; no production occurrence IDs are assigned.
- Interfaces: existing valve-cover roof, pilot cap male helix, annular seal, fill passage and all twelve installed rockers. Neck is fused into the cover service assembly; this does not settle integral forming versus welded/insert construction.
- Inputs: restored generated valve-cover and rocker STEP, current assembly JSON, pilot cap source and shared motion engine. Available locally; generated STEP restoration remains an access dependency.
- Acceptance: exact Boolean overlap threshold 0.1 mm³ follows the existing audit convention, contact distance 0.002 mm. These are numerical checks, not leak, torque, fatigue or production tolerance specifications. Test straight pull against an oversized female bore negative control, sampled screw removal, continuous attachment and open fill passage before the full rocker sweep.

## Evidence ledger

| Feature | Value | Class / limitation |
|---|---|---|
| Male cap screw and annular seal | Ford cap bottom photo | Source-supported topology; see oil-fill-neck-research.md and source hashes |
| Cap thread major diameter | 31.24 mm | MotoRad replacement comparison, not Ford metrology |
| Pitch and female groove | 4.5 mm, matching existing cap phase | Assumed study variant; no OEM or M32 designation |
| Neck extent / outer radius | Z399–413 / 17.8 mm | Assumed interface geometry |
| Bore / groove clearance | R14.62 / groove outer R15.85 | Assumed fit clearances, not production specification |
| Continuous service assembly | Fused neck and cover roof | Illustrative load path; manufacturing process unknown |
| Factory neck and baffle | No section available | Unresolved; exact manual overview does not expose these internals |

## Delivery

- Readiness: failed installation candidate, not installed; no commit or PR created by this worker.
- API: `candidate(cover)` returns world-placed `(cover_with_neck, neck)`; `cap_at(angle=0., lift=None)` returns unchanged pilot cap and seal under the screw displacement. Default lift is `4.5*angle/360` mm.
- Reproduce: `.venv-cad/bin/python scripts/check-oil-fill-neck-candidate.py` from repository root.
- Isolated ignored artifacts: `cad/engine/generated/oil-fill-neck-study/{cover-with-neck,neck}.step`. No restricted manual images or owner photographs redistributed.
- Environment and input hashes: machine-readable validation report. Model/effort and usage unavailable.

## Validation and review

**Final verdict: FAIL for installation.** The matched neck is mechanically feasible in isolation, but the unchanged cap hits the current upper-intake floor during service withdrawal at1035° /12.9375 mm lift. The collision occupiesX211.40–268.60,Y-40.60–16.60,Z445.00–445.0375 mm. Stem tip is stillZ406.9375 below the Z413 neck exit. First overlap is110.19 mm³; it grows thereafter. No cap shortening or cap-shaped intake notch is justified by this failure.

Actual CAD review artifacts: `cad/engine/generated/oil-fill-neck-study/review.svg` (assembled and section) and `removal-failure.svg` (full intake and local failure). PNG previews were visually inspected locally; SVGs are deterministic checker outputs. GLB round-trip bounds errors were below0.000014 mm and all three meshes watertight. Input before/after hashes matched for this completed run. Later unrelated manifest changes do not erase the recorded old-intake failure; the snapshot remains explicitly identified.


| Gate | Result / evidence | Limits |
|---|---|---|
| Application / coverage | Candidate only: exact cover identity in research ledger | Neck manufacture, original pitch and baffle remain unknown |
| Dimensions / coordinates | PASS for explicit study datums | All new neck dimensions are inferred |
| CAD / export | Exact candidate is one connected solid | STEP and GLB results in validation report |
| Source / visual comparison | Actual CAD section generated for review | Source photographs hide the female neck; no factory fidelity claim |
| Installed interfaces | Study PASS: 262.39 mm³ neck-to-cover union, zero cap/seat interference, open 20 mm diameter flow probe | Not installed; no preload, leak, strength or full-flow capacity simulation |
| Motion / disassembly | Added neck sweep PASS, min 6.3754 mm to c1 intake rocker; 181 crank phases and all twelve rockers | Sampled, not continuous proof; separate removal result in report |
| Learning / diagnostics | Explanation below | Browser learning content NOT RUN |
| Browser integration | NOT RUN | Isolated study intentionally not installed |
| Reproduction / review | Checker and hashes retained | Parent integration review pending |

The existing roof provides a coplanar sealing annulus outside radius17 at Z413. The cap seal spans radius15.8–22, so the roof alone supports an annular contact region of 612.61 mm²; the candidate adds support inward of radius17. This is nominal geometric contact, not compression or fluid-tightness proof.

Straight lift by 1.125 mm generates 149.91 mm³ interference against the female thread; enlarging the female bore to radius16.1 removes that interference entirely. The intended matching screw path rotates +45° per 0.5625 mm lift, sampled through five turns /22.5 mm. The closed male stem clears the neck at the final position. The cap's existing pitch and profile are left unchanged. Incorrect pitch, stripped female material or missing sealing contact would defeat different aspects of this joint; the study models geometric retention and seating only.

The neck passes all sampled rocker phases; lowering it10 mm produces253.79 mm³ interference and proves the collision check detects a relevant bad location. Existing cap/rocker motion evidence remains in the separate pilot report. Removal uses the engine-off crank-zero neighbor poses and checks nearby geometry along the screw path; fingers, tools, hood and a further carrying path are outside this scope.

Production sealing/preload and factory thread fidelity remain unresolved. No installed acceptance is claimed.

## Tracking and restart

Issue #15 remains open. The upstream intake proposal is separate and hypothesis-classed; neck installation is not approved. Integration owner must review the final report and resolve production thread and neck geometry before factory-faithful installation. Re-run the checker after any input changes; no report survives changed hashes without a fresh check.

## Proposed integration, subject to parent review

Do not add the neck as a floating occurrence. The cover definition must include its continuous female material. In `valve_source_layout.cover()`, the study's world neck maps to cover-local axis `(240,0)`, bottom Z24 and top Z38; the helical groove starts at local Z20.5. Apply the current smooth bore cuts first, then fuse the annular, grooved neck into the existing roof. This preserves the existing cover occurrence transform and cap datum. An equivalent implementation may inverse-transform the world study neck into cover-local coordinates before fusing it.

Install the pilot cap and its separate seal together using their existing stable IDs and `POSITION`; retaining the older cap definition would test a different male mate. Update the affected source metadata to say explicitly that the matched 4.5 mm thread is illustrative and factory pitch remains unresolved. Rebuild only affected assets and rerun installed cap/neck/cover motion and removal checks against the final manifest. Check browser selection, isolation, reset and disassembly separately before any installed acceptance.

The cap remains nonvented: ventilation belongs to the separate cover/PCV circuit. The open probe demonstrates one central fill path after cap removal; it does not establish the production baffle arrangement or oil flow capacity. No production baffle was invented to fill the evidence gap.
