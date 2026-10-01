# Coordinated pan21 lateral datum: pre-build contract

## Contract

Issue32/34 under Engine1; integration owner root. Baseline dafb8175e4e7b328d2a16bdc47914307f044b0c8 on `engine/timing-motion-integration`. Research/preflight only; no part geometry has changed. Preserve frozen V3 block, expanded-seat v2 pan/gasket, seal2692, uniform main-seatX379.8 failed trial and station1X377.8 failed trial. Owned files are this proposal, `scripts/research-timing-pan21-lateral-datum.py`, and its inventory report. Exact STEP input hashes are in that report. Assembly manifest N/A for isolated preflight.

Proposed weak-datum revision: pan21 under-head translation(390,−110,−32.1)→(390,−95,−32.1)mm, with unchanged vertical axis, screw length, nominal thread, washer and seat stack. Keep all seven main axes and uniform estimated seatX379.8 unchanged. This is a15mm lateral feasibility estimate, not a measured Ford coordinate. No source original is redistributed. Source hierarchy and actual image comparison are in `timing-cover-station1-pan21-datum-audit.md`.

## Preflight result: cavity prerequisite fails

The new fullR10 socket envelope clears the actual station1 screw and declaredR10.5 axial tool envelope with zero intersection. Its lateral interval−105..−85 has3.699515mm separation from the main1 access envelope. It clears the central pan23 stock and the analytic front-arch radial boundary by25.6mm. Its Xminimum380 lies2mm forward of the current pan upper-wall outerX378, so it occupies the same front dry flange corridor in plan view.

Plan-view clearance is insufficient. The complete socket requiresR10 stock fromZ−24.5 to−8.5. Existing cover material does not fill1671.694445mm³ of that envelope; even theR6.2 wall/floor envelope has695.888389mm³ absent. Reconstructing the original cover's declared inner cavity shows the full proposed envelope inside that pre-pad cavity. The cavity volume presently empty within the proposed support is separately measured in the report. This source-construction cavity is an estimated geometric region, not validated fluid CFD or a factory internal drawing, but adding socket stock there violates a strict unchanged-cavity prerequisite. No candidate is built under that prerequisite.

## Conditional patch proposal for root composition

If root explicitly accepts a local blind socket support intruding into this declared cavity after appropriate motion/flow/containment guards, the coordinated patch must perform all following steps in NEW files. Otherwise this proposal stops at preflight failure.

- Bind the uniform main-seat379.8 cover STEP, matched expanded-seat v2 pan/gasket STEP, reusable actual pan male/washer/female, and shared seat API hashes. Keep the block unchanged; all changes stay nearX380..400 and the two station21 neighborhoods.
- Retire the old21 clearance hole in pan/gasket by restoring their declared analytic flat layersZ−30.5..−26.5 and−26.5..−24.5, respectively. Re-cut the same radius4.3 clearance atY−95. The front strip is already flat at both lateral positions; do not move the central arch or alter the other24holes.
- Retire the old cover socket with an explicitly bounded oldR10 neighborhood and restore only the declared dry upper bandZ−24.5..−14.5 there. Remove the obsolete local boss/thread feature; do not fill an arbitrary16mm column or retain a phantom female cavity. Preserve unaffected casting outside the union of old/new pad masks and the existing main1 access mask.
- Construct the new21 support and nominal female cavity from the same declared analytic bore/source female method after all stock unions, preserving actual female material, complete bore wall and floor. Do not copy a translated slice of the old cover: that slice can contain unrelated main-cover-hole geometry. Do not carve with the assembled male.
- Reapply the unchanged main1 access cylinder in the vacated old21 neighborhood, now excluding the NEW pan21 guard. This is essential: the failed baseline pocket intentionally retained old21 stock. Keep the main1 axis, seat, length, head and tool envelope unchanged. No head/tool clipping.
- Relocate actual oil-pan-mounting-screw-21 and washer-21 by(0,+15,0), maintaining stable occurrence IDs. Exactly25pan screws and25washers remain; no added/deleted mount or duplicate old21 feature. Seven main-cover screws remain separate BOM entries with1986 comparison applicability limits.

The permitted material scope must be recorded before modeling. Old/new coverR10 neighborhoods overlap; implement retirement, analytic stock reconstruction and cavity cutting in deterministic order so overlap cannot refill the new female void. This proposal is not permission to remove material from pan22/23 or source-backed main1.

## Required gates if later authorized

Compare full old/new stock outside declared masks exactly; preserve24other pan interfaces, full rear/transition/front arch, main gasket, seal2692 and all block material. Prove actual screw/washer seat contact and complete gasket backing on both faces at25stations; unchanged original failure controls must still detect old21/main1 collision. Check source female, full wall/floor, tip reserve, male contact and zero unintended overlap. Verify actual tool paths and disassembly; actual pan/cover/gasket, crank/cam swept envelopes, oil-retention boundary and any mapped wet flow volumes must clear. The modeled cavity intrusion needs explicit acceptance criteria before a build; a positive-volume boss cannot be described as unchanged cavity. Require valid connected solids, direct STEP/mesh checks, actual rendered review and all input/output hashes. No factory/strength/torque/whole containment/browser claim.

## Delivery and restart

Read-only commands: `.venv-cad/bin/python scripts/research-timing-pan21-lateral-datum.py`. Report: `inventory/engine/timing-pan21-lateral-datum-preflight.json`. macOS/Python3.13.12/build123d0.10.0. Strict volume requested1e-9, convergence ceiling1e-7; no relaxed gates. No generated revised part exports or candidate render because prerequisite fails. Browser N/A, installation NOT RUN, measured datum unknown. Next action: root reviews whether local cavity occupation is allowed and specifies its guards, or supplies a different evidenced datum. Worker model/effort/usage unavailable. No background work after handoff.

## Authorized build extension

Root subsequently authorizes the bounded blind boss to occupy the local inferred shell cavity, superseding only the unchanged-cavity prerequisite. Preserve that original failed preflight report. This is a new estimated local cavity occupation, not an untouched source-confirmed passage. Functional wet connectivity and actual moving-core clearance remain mandatory; the female bore must be fully enclosed from the wet side by real wall/floor.

New module `cad/engine/timing_pan21_lateral_candidate.py` imports frozen uniform-seat cover and expanded-seat v2 pan/gasket. Explicit stock mask is old/newR10 cylindersZ−24.5..−8.5. Old hole refills useR4.31 to provide0.01mm overlap with existing flange stock before recutting newR4.3 clearance; these refills lie inside the declared oldpad mask. Cover restores only the existing analytic10mm upperband at the retired socket and reconstructs new source female/cavity after union. Existing main1R10.5 access is reapplied with the new21 guard. Inputs are hash-asserted. No block rewrite or other hardware movement.

## Candidate delivery

Delivery branch `engine/timing-drive-fit`, integration baseline26d0fdc4e7cdd3de0c621309499d1535d8c5131e; creation baseline remains above. Root owns packaging/PR, no canonical assembly changes. `build()` returns threeparts plus analytic/reference details. Exports in `cad/engine/generated/timing-pan21-lateral-candidate/`: cover.step SHA c27ac0620982322ae414ed277518d87c5611d3c91b9a253dd8599b003cc69f40; pan.step SHA ab542e57be0d1b99373e481839b507aa8041a262d7d3649f7b0c6a83bbf8a20a; pan-gasket.step SHA f6aa000aaf72b27b682509dafeee73b2cf7580fd78d6e8661e1b44916b403fe5. Same-namedGLBs are millimeter→meter, Z-up→Y-up exports. `review.png` displays actual meshes and actualX390 section; exploded vertical offsets are display-only.

Reproduce in order from repository root, with `.venv-cad/bin/python`: `scripts/check-timing-pan21-lateral-candidate.py`, `scripts/check-timing-pan21-lateral-interfaces.py`, `scripts/check-timing-pan21-actual-gasket-contact.py`, `scripts/check-timing-pan21-lateral-neighbors.py`, `scripts/check-timing-pan21-main-joint.py`, and `scripts/render-timing-pan21-lateral-candidate.py --sections`. Render with `MPLCONFIGDIR=/tmp/truck-gear-mpl python3 scripts/render-timing-pan21-lateral-candidate.py`. Temporary paths are caches/log copies only, not required source inputs. Frozen source STEP assets must be reacquired through their earlier release/handoffs if absent.

| Gate | Result | Evidence / limits |
|---|---|---|
| Application/dimensions | ESTIMATED | Only21moves+15mmY; historical1986main bolt comparison and head/recess estimates remain unverified for1994. |
| CAD/mesh | PASS bounded | Three valid connected single solids; direct STEP, watertight consistent meshes, onecomponent, positive signed volume. GasketEuler−50 retains onecentralopening+25holes. |
| Actual attachment/contact | PASS local | All25male/washer-to-pan overlaps0 and complete nominalpan/gasket seat annuli. New female/sourcevoid/wall/floor checks0missing/filled. Complete actual gasket upper/lower backing inR12 aroundold/new21 is0missing. |
| Locality | PASS | Exact added/removed material outside declared masks0 for allthree parts. Other24axes unchanged. |
| Dry/wet separation | PASS bounded | New blindwall2.03mm andfloor1mm present; headoutsidepan; dry-to-wet path hits0.785398mm³ wall, deliberatebreachhits0. NominalTEKTONpan tool clear. Local positive-radius wet bypasses clear; blocked controls positive. Full oil containment NOT VERIFIED. |
| Actual neighbors | PASS static / bounded rotation | Corrected crank/cam, core gear/retention/bearings, seal2692/hub, trialblock, maingasket andterminalsealant overlaps0. Newstock conservativerotation separation lowerbounds24.358mmcrankgear,55.725mmcrank,80.265mmcamgear,176.533mmcam. No fullassembly continuous-motion claim. |
| Source/visual | SCOPED | Actual render andsection reviewed by worker, root review pending. No dimensional source fidelity claim. |
| Learning/browser/install | NOT RUN | Isolated candidate; no installed acceptance. |

Reports are `inventory/engine/timing-pan21-lateral-candidate-validation.json`, `timing-pan21-lateral-interfaces.json`, `timing-pan21-actual-gasket-contact.json`, `timing-pan21-lateral-neighbors.json`, `timing-pan21-main-joint.json`, and `timing-pan21-lateral-visual-review.json`. Final delivery binding checks report input hashes and exported units separately.

The initial fullR10 bottom-disk probe reported0.1174518138mm³ missing beyondactualfrontX399. It remains in the interface report. This probe asked for material where the actual gasket is absent; subsequent full actual gasket translation witnesses withinR12 aroundbothchangedstations pass without modifying geometry or tolerances. This is a corrected witness scope, not a waived physical contact failure.

Inherited limits remain explicit: pan/gasket are frozen expanded-seat v2, so later root rear/upper-contact repairs are NOT incorporated; inherited rear contact gaps persist unchanged. This candidate must be composed with those patches and rechecked. The seven-main-screw comparison block is unchanged and still lacks complete wet/core/material locality qualification against its own pre-thread baseline; the pan21 delta checks do not certify that broader block revision. Main hardware head/tool/thread clearance,1994BOM transfer and torque remain estimates/unknowns. Code may be reviewed as a candidate; installation is not accepted.

Final binding: `scripts/check-timing-pan21-lateral-delivery.py` returns **PASS scoped pan21 relocation; not installed**, with all13 scoped gates true and all recorded report inputs current. Report SHA256`f07238f0492da400fb26e4c21f547d397ece078f16cff0e5d90f0ae67b040e4f`. GLB units/bounds rechecked against actual mesh; no measurement errors. The complete seven-main-joint report now passes actual contacts/access and block/pan/gasket overlaps. Broader seven-screw block guards remain explicitly outside this pan21 delivery. No running processes; frozen for root review.
