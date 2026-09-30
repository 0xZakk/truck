# Rear-seat Boolean construction repair

## Contract

Issue #32; root integration owner. New isolated revision on `engine/timing-interface-reconciliation`, checkpoint `eb502ce755d12fe896b3ea915f3ada4361e52a9c`. Previous failed fixed-stock and shifted-stock proofs remain untouched. No canonical/shared files or machining/support dimensions change.

Root authorized explicit repair of the first invalid operation before further machining. Reuse exact `expansion_plugs.machine_block_seat` boss/tunnel/seat operand expressions by AST extraction. Compare Boolean construction orders on valid incoming stock; choose an original-CAD-valid result, then require valid full original CAD, watertight direct mesh, and valid STEP readback with geometric agreement. STEP export healing cannot stand in for builder validity. Cam axis remains the estimated same-ray 121.8 mm hypothesis; all source dimensions and frames remain classified as in prior handoffs.

Owned module `timing_block_rear_seat_repair_candidate.py`, local/full checkers, reports and generated directory. Proposed repair distributes the identical tunnel/seat cuts over stock and rear support before their union. This changes CSG evaluation order, not the intended set of material. Original 79 broad and 91 physical protections remain binding; existing fit/support failures are not waived. Carrier redesign and final machining remain unapproved.

## Delivery and checks

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-timing-block-rear-seat-repair-local.py
```

macOS, Python3.13/build123d0.10.0. Required input is the valid pre-seat prefix STEP from the frozen fixed-stock study and unchanged source modules. Exact hashes captured by checker. No dependencies installed.

## Review and restart

Local construction comparisons are complete and preserved. Active full topology revision passes the bounded repair gates. No production or installed acceptance. Browser NOT RUN, isolated revision/root security block. Support and mating-interface deficiencies remain explicit. No automatic next machining step. Usage/billing unavailable.

## Preserved construction comparisons

- First distributed-cut attempt produced a valid but incorrect rear-support-only solid (~9636 mm³ instead of ~19.78 million mm³); rejected by material comparison. Its module/report remain unchanged.
- Skipping the already-empty stock tunnel cut and fusing the cutter operands did not repair validity; those separate attempts remain preserved.
- Disabling build123d's `ShapeUpgrade_UnifySameDomain` only for rear-seat Booleans produces a locally valid solid, but later adapters repeat simplification and recreate the invalid tunnel wire. That full failed attempt is preserved.
- Active NEW module `timing_block_boolean_topology_candidate.py` retains exact source operands and disables that optional same-domain simplification from rear-seat through the ordered downstream adapters. It restores the original function and process flag in `finally`. No STEP healing constructs its original CAD. Verification Booleans use the same explicit topology-preserving mode so the previously failed simplification cannot corrupt the comparison itself.

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-timing-block-boolean-topology-full.py
```

This checker binds all frozen fixed-stock inputs, produces original-CAD/direct-mesh/readback evidence, and compares material against the prior valid fixed-stock STEP readback. A topology-only success cannot promote existing support or interface failures. No final machining or carrier change is authorized by this construction experiment.


## Final delivery and review

Active module: `cad/engine/timing_block_boolean_topology_candidate.py`; API `regenerate(delta=DELTA, stage=None, feature_capture=None)`. This is a construction repair, not a new casting or machining design. All five original-CAD stages are valid single solids. Direct mesh is watertight (72,050 triangles); STEP readback is valid. Exact extra and missing volumes are both zero against its own readback AND the frozen fixed-stock STEP. Verification disables the same optional simplifier that caused the defective topology; its extra/missing results are empty and valid. Consequently the frozen fixed-stock support and interface diagnostics transfer by exact material equality, without treating the earlier invalid original builder as accepted.

Direct mesh `cad/engine/generated/timing-block-boolean-topology-candidate/block.glb` and STEP `block.step` are isolated outputs. Actual mesh render `block-render.png` was inspected by worker; journal deficits remain visible. The report binds source, baseline and generated input hashes. Canonical block/timing geometry was never replaced.

```sh
MPLCONFIGDIR=/tmp/truck-gear-mpl python3 scripts/render-timing-block-boolean-topology-candidate.py
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-timing-carrier-machining-proposal.py
```

| Quality gate | Result |
|---|---|
| Scope/application | Estimated 121.8 mm study; not a verified Ford axis datum |
| CAD construction / export | PASS valid original CAD, valid STEP, watertight direct mesh |
| Material equivalence | PASS exact zero added/removed volume against own readback and fixed-stock STEP |
| Actual render | Worker viewed new direct mesh; root review pending |
| Support / interfaces | FAIL inherited fixed-stock journal, shaft/bearing/guide and protected-interface deficiencies |
| Motion / installed acceptance | NOT RUN for this construction-only revision; no integration authorized |
| Browser | NOT RUN, isolated candidate and root-reported browser block |
| Learning | N/A; installed learning untouched |
| Reproduction | Bound reports, commands, staged geometry and preserved failed attempts |

## Next geometry proposal — review required

No further material has been added or machined. First address journal supports: all four center sections lack support on the outer +Y arc, sampled every 5° at 330..355° and 0..30°. Journal 4 additionally lacks support at 195..240°; journal 1 has that extra deficiency at its front sample X−323.1. Exact missing-shell STEP witnesses, bounds and volumes are in `timing-block-fixed-stock-support-regions.json`; the actual sections are `timing-block-fixed-stock-candidate/journal-support-sections.png`. These witnesses identify deficient material only within the declared thin shells. They do not specify a production boss, wall thickness, oil groove or load capacity.

The source-sized supports and attachments must stay explicit. Current carrier boss radius14/socket radius5.2 give nominal radial wall8.8 mm; current blind backing is7 mm. These are existing provisional CAD dimensions, not manufacturer wall requirements. The proposed final tunnel/guide removals would take458.124607 mm³ from support X292 and427.110106 mm³ from X340. Exact nearest distance from either prospective removal to its existing socket surface is5.668275 mm; distance to the declared 2 mm mating-seat backing guard is19.437498 mm. Existing seat atY135 and socket axis/extent stay fixed. The proposed 2 mm guards are untouched, but the earlier whole-support guards remain FAILED and are not replaced in their reports.

Root may review a bounded carrier interior-support redesign using those fixed mating/attachment datums and an explicit remaining-wall criterion. A 5 mm geometric separation criterion would have a measured0.668275 mm margin here, but neither5 mm nor the prior2 mm has manufacturer strength evidence; neither is a production specification or automatic approval. Recheck actual carrier/stud contact and support continuity after any approved redesign. Retain gasket seats, all fastener socket/support masks, filter fluid/attachment, dipstick and pan protections; the small pan-socket8 failure remains unresolved. Final tunnel/guide machining must be a distinct candidate with predeclared guards, not blanket neighbor subtraction. Root alone combines front land.

No processes remain. Root review is the next action. Candidate code/evidence can be preserved independently of installation; no installation acceptance or production fidelity is claimed.

### Frozen delivery hashes

- `inventory/engine/timing-block-boolean-topology-full.json`: `54efce493492269a6f0e7c7661c02d68ce4ed19914b523ca077d7e3430bd690e`
- `inventory/engine/timing-block-fixed-stock-validation.json`: `1c756f687838c5bbea606687db3649d196917e16bc3240955c74c368569d474f`
- `inventory/engine/timing-block-fixed-stock-attribution.json`: `a5d6e93a6ed00ddc5f010fe49bfb8899cb671bfa1e35785264869a3db7a27d1b`
- `inventory/engine/timing-block-fixed-stock-support-regions.json`: `5264c968103e7df753d8df34d0a23709a77f1f0fa6b028a88b88ff4d99c3a0db`
- `inventory/engine/timing-carrier-machining-proposal.json`: `6b3bc41bb5945a71b578b01cfab389588b63ed37bc6c5129a710ec9559158345`
- `cad/engine/generated/timing-block-boolean-topology-candidate/block-render.png`: `0e0dd7e6d6b6a11a5eb9f39712c11476d5aa42f1385d062c1a2f5ea943680e8a`
