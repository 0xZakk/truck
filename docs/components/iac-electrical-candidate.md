# Component contract and handoff: IAC engine-side electrical interface

## Contract

- Issue44 / engine parent1. Contributor pump_seal_finish; integration owner root. Candidate-only work on `engine/next-interface-contracts`; baseline commit and actual scoped input hashes recorded by checker. No shared/frozen closure or attachment edits.
- Owned files: `cad/engine/iac_electrical_candidate.py`, `scripts/check-iac-electrical-candidate.py`, `reference/engine/iac-electrical-review.json`, this handoff. Reports/STEP/GLB/render in ignored `cad/engine/generated/iac-electrical-candidate/`.
- Scope: engine-side keyed insulating connector, two conductive terminal/tail studies, insulating coil carrier and revised winding envelope. No harness routing or mating production connector. Diode remains supported circuit explanation, not an invented physical package.
- Exact1994 EVTM identifies C1007, two terminals, black connector, circuit361 red VPWR and264 white/light-blue PCM control. The symbol contains a diode in parallel with the coil. FSM KE4 explicitly identifies a diode; these are source-supported topology, not inferred variant electronics.
- Frame: existing IAC local X axis, connector opens toward+X. Isolated component-face view looks from+X toward-X with+Z shown up. Following FSM engine-side image563186997, control contact is displayed above VPWR. Harness image442501993 is separately labeled looking into the harness mating face; do not transfer its left/right key geometry unmirrored. No connector cavity numbers are established; breakout21/37/57 are PCM/test-box pins, not terminal numbering.
- Engine mounting clocking and all connector dimensions remain estimated. Two contact positions share a polarized shroud, with separate insulating feedthroughs. A central upper guide rib is an illustrative interpretation of asymmetry, not a measured latch/key.
- Five candidate solids: revised `iac-connector-cap`, revised `iac-coil` winding envelope, new coil insulator/carrier, control terminal/tail, VPWR terminal/tail. Actual terminal alloy/plating, wire gauge, turns, coil-end termination, molded retention process and diode package/location unresolved. Functional render colors are not wire-color/material evidence.
- Proposed datum: winding remains X26.5..65.5; conductor envelope radii4.4..9.3 with estimated surrounding insulating carrier inside existing can. Carrier bears against fixed front and rear faces. Terminals have insulating capture shoulders and continuous estimated tails to two distinct points on the winding end face. The annular coil remains a winding envelope, not a literal homogeneous shorted ring or computed winding resistance.
- Checks: conductor single-solid continuity, terminal-to-winding contact, distinct terminal/case/armature isolation, insulator capture, keying witness, short/open fault controls, export binding and actual cutaway render. Geometry cannot certify electrical resistance, dielectric strength, duty-cycle response or a production coil design.

## Evidence ledger

See `reference/engine/iac-electrical-review.json`. Exact1994 EVTM printed23-2 (PDF75) and152-25 (PDF360) were rendered and visually inspected; purchased pages are not redistributed. FSM engine-side connector image563186997 and harness image442501993 were separately inspected. Parts catalog identity remains the archived ambiguous FOTZ9F715CA transcription; C1007 is a circuit connector identifier, not a replacement part number. No replacement specimen dimensions were transferred.

## Delivery / validation

Proposal approved by root for a bounded educational candidate. Candidate geometry, export checks and actual render complete; root accepted the explicitly illustrative candidate for isolated integration staging. Original IAC closure/attachment stages remain frozen. Record final checks, render and explicit limitations below before handoff.

## Tracking

Issue remains open. No commits or external posts. Input manuals are locally available but ignored/purchased; developer must obtain authorized source access or use the evidence ledger for review. Python3.13/build123d0.10/OCP7.8; matplotlib for render. Usage/billing unavailable.

## Validation and review

The bounded candidate passes its numerical geometry checks. `build()` takes no arguments and returns five IAC-local millimeter solids. It replaces only the existing connector cap and winding envelope, adding two separately selectable terminals and one insulating carrier. The current installed shell, body, armature, pintle, spring and closure are inputs only. A later integration adapter must convert these IAC-local solids to each definition's current occurrence frame; do not apply the entire throttle transform twice.

Reproduce from repository root:

```sh
.venv-cad/bin/python scripts/check-iac-electrical-candidate.py
python3 scripts/check-iac-electrical-candidate.py --render
```

Outputs are ignored `cad/engine/generated/iac-electrical-candidate/{validation.json,candidate.glb,candidate-review.png}` plus five named STEP/GLB pairs. No asset release has been published. Reports bind source files, reviewed manual hashes, relevant STEP inputs and relevant definition/occurrence/ancestor records. Unrelated manifest changes are permitted only when that scoped snapshot is unchanged. Exact installed binding and viewer tests require a later integration stage.

| Gate | Result | Evidence and limits |
|---|---|---|
| Application/coverage | Bounded PASS | Exact1994 4.9L two-contact C1007/coil/diode topology; production terminal construction unknown. |
| Dimensions/coordinates | Estimated / checked | IAC-local mm, +X mating direction; source drawings establish topology, no connector dimensions. |
| CAD/export | PASS | Five valid single solids and watertight meshes, STEP round trips; GLB/CAD bounds threshold0.2mm. |
| Source/visual comparison | Bounded review | Two vertically arranged contacts and asymmetric keying match diagram topology only. Upper guide rib, rounded shroud, shoulders and tail routing are illustrative discrepancies/estimates. No production-shape acceptance. |
| Installed interfaces | Candidate PASS / installed NOT RUN | All affected pairs tested, carrier fixed axial seats, metal isolation and terminal capture. All-occurrence broad phase finds upper intake as external neighbor; exact intersections zero. |
| Motion/disassembly | Sampled PASS / production removal NOT RUN | Five armature positions across ±1mm clear; terminal shoulder ±1mm withdrawal obstructed. Captured insert molding/assembly process is unknown. |
| Learning/diagnostics | Bounded PASS | Two electrical nodes feed winding; diode suppression appears in source circuit only. Open tail and bridge fault controls exercise geometric connectivity; no resistance, dielectric or transient simulation. |
| Browser integration | NOT RUN | No canonical writes or learning-module installation. |
| Reproduction/review | Candidate ready for root review | Commands, hashes, source ledger, report and actual render available. No installed acceptance. |

Geometry thresholds are numerical: unintended overlap below0.00001mm³, STEP volume error below0.001mm³; these are not manufacturing fit specifications. The coil is an annular *winding envelope*: terminal-tail endpoint contact proves an illustrative interface to that envelope, not an actual winding topology, resistance or solder joint. Terminal net isolation excludes the intentional circuit connection through the coil. The source electrical resistance specification is not claimed as measured or simulated by CAD.

Carrier/body axial seat62.549110mm², carrier/cap238.171877mm² and coil/carrier planar end seats421.224743mm². Each terminal tail contacts the winding end face over0.282743mm². Terminal-to-terminal surface gap1.8mm; minimum terminal-to-case gap3.375445mm. Terminal withdrawal controls produce4.129554–4.351814mm³ obstruction. Correct key gauge has zero overlap; reversed gauge overlaps3.84mm³. A deliberate conductive bridge intersects each pin over0.66mm³, while a clipped tail produces0.3mm gap. The gauge is test-only and is not an exported harness component. All candidate solids remain inside the original can/connector envelope; this containment accompanies actual selected-neighbor checks rather than replacing them.

Remaining limits: terminal count/topology supported, internal terminal alloy/plating/gauge/join method and actual molded carrier/retainer/key dimensions unknown; coil turn count/insulation/thermal properties/diode package absent; unknown production clocking and actual-truck variant. Functional mesh colors are illustrative and do not turn wire colors into terminal material evidence. Root must review render, create scoped idempotent integration, rerun final body/closure compatibility and installed/browser checks. Issue44 remains open; this candidate is not Done.

Final validation: **PASS**; baseline commit `fb2a1e756cf5e0d6ed925975312231406fce18ed`; manifest `f1dc26ba64eb0ba1e8fede4ef42e23a5ae3e288dbeae3cc4b2558cf4148a4a70`; validation SHA-256 `f4fff650057ffff7def5e08e654f17375a04e52f8b64e0e6197ae0b2dd6009a7`. Maximum mesh/CAD bounds difference 0.002372074289416659mm. Actual render reviewed after final export, SHA-256 `185a0d62fb5c7be3598241483cbaf1c24432d636d891f82d2d312e0c446cd574`. No process remains running. No canonical assets, shared manifest or frozen closure/attachment files changed.

## Isolated integration adapter

New owned integration files: `cad/engine/iac_electrical_integration.py`, `scripts/install-iac-electrical.py`, `scripts/check-iac-electrical-installed.py`, and `inventory/engine/iac-electrical-learning.json`. Default installer invocation prints a plan without writing; `--stage` uses ignored `cad/engine/generated/iac-electrical-integration-stage/`; only the integration owner may invoke `--apply` after review. The final installed check is a distinct `--installed` run.

Dependency order is attachment → captured closure → electrical. Three new definitions/occurrences retain IAC-local identity frames. Existing cap and coil occurrences keep their stable IDs, poses and explode vectors. Their functions are refreshed so the obsolete “terminal geometry still missing” text no longer shadows the added terminals. Replay must preserve both metadata and geometry with no duplicate IDs, including a further17mm parent translation and13° parent rotation. A0.5mm independent cap-position fault must be rejected. Coil and terminals are still illustrative and uncalibrated.

The original electrical candidate report is preserved. Its original body/plug hashes are superseded only by exact final closure-candidate geometric bindings and the installed closure evidence chain. The intake neighbor hash is superseded only by the accepted exterior installed→stage evidence and exact current artifact hashes. The checker preserves all original relative IAC/neighbor poses, reruns current attachment/closure/electrical and intake intersections, confirms closure spring contact, terminal/carrier seats, armature clearance and short/open/key controls. A changed unrelated manifest hash does not invalidate otherwise identical scoped inputs. Original full-engine static and browser acceptance do not transfer automatically.

Stage commands, after root installs and checks closure:

```sh
.venv-cad/bin/python scripts/install-iac-electrical.py --stage
.venv-cad/bin/python scripts/check-iac-electrical-installed.py
```

Shared hook and source registration remain root-owned. Full original-base intake coordination/exterior chain replay is a separate pending integration test; this adapter tests the IAC attachment/closure/electrical chain only.

Final isolated integration stage **PASS** at725definitions/1333occurrences, source manifest binding `4f98bbdad7fb1996487d17c4a651de588cef39254efe24e96384375dbdce0c07`. Stage validation SHA-256 `8bab2e003db92652d9676e9101dc04b14bf83d3b4b6bcb5c207366a5544d637a`. All12 electrical/attachment/closure reference bindings pass, no IAC/intake collisions, all replay differences zero (single adapter, full IAC chain, parent translation and rotation); individual cap-pose fault rejected. Five staged exports are watertight with no degenerate/duplicate faces. Cap tessellation uses0.03mm/0.08rad after0.025mm produced two very thin triangles; geometry and acceptance thresholds unchanged. Current cad_metrics helper hash is bound in the installation record. Actual staged-GLB render `cad/engine/generated/iac-electrical-integration-stage/candidate-review.png` reviewed, SHA-256 `64fbcb36715933a971c5648dc6faa208144815027b3adc2373fc7731763509aa`. Canonical installation/browser remain root-owned and NOT RUN by this worker. Original candidate snapshots unchanged.
