# Component contract and handoff: timing-cover-attachment-candidate

## Contract

Issue #32 / Engine #1. Contributor air_cleaner_candidate; root is integration owner. Baseline 705c4683c199d8c5e28addba018bc8d1bdd399b1 on engine/timing-core-pan-joint. The root-approved estimated sealing joint is frozen; its validation hash is 6a4490ed3d50956e9fd0db1297fa17a217c363e15d1b453bd64b2a8c94d11116. No canonical/shared edits or block union.

Own new `cad/engine/timing_cover_attachment_candidate.py`, checker/renderer scripts, review/validation records, this handoff and isolated generated timing-cover-attachment-candidate directory. Inspect seven cover screws, five relocated pan screw/washer pairs and the unchanged front seal. Preserve existing stable pan IDs, all 25 stations in total and 20 unchanged transforms. No new cover washers unless evidence establishes them. Millimeter engine world frame; the fixed seal remains X 414, crank Y/Z zero. Existing damper/hub stays fixed.

Acceptance scope: actual reusable pieces and bound proposed transforms; head/washer contact, shank clearance, thread/socket limitations, material support, export checks and actual section renders. A smooth clearance hole is not female-thread engagement. Incompatible frozen seats are reported rather than modified. Manufacturer dimensions versus model conventions remain distinct. Seven main-cover fastener count follows the source-supported holes; exact hardware nominal data/length mix remain subject to research. Installation, learning and browser gates stay NOT RUN.

## Evidence ledger

The exact 1994 oil-pan drawing 350379654 was inspected at full image resolution. Its callout supports 25 screw-and-washer assemblies, 5/16-18 × 0.87 in (diameter 7.9375 mm, pitch 1.411111 mm, under-head length 22.098 mm). Existing separate washer pieces illustrate that assembly; their dimensions and captive construction remain model conventions. The new study reuses those physical definitions.

The exact-year timing-cover procedure and torque table were read. They name attaching screws/bolts but do not establish nominal thread, length mix, head shape, seven-position mapping or a separate washer. Seven source-supported mounting holes are therefore retained as axis records, not seven invented finished screws. Mixed-engine and 1987 catalog search leads are not transferred to this truck. Source files, hashes and unavailable search results are recorded in `reference/engine/timing-cover-attachment-review.json`.

The exact-year front-seal parts entry lists E6DZ6700A without seal dimensions or a lip-track datum. The existing model is a plain R21–27 mm annulus at X410…418. The unchanged damper hub starts X419. The 1 mm axial gap is a model incompatibility to resolve through a separately reviewed seal/hub proposal, not a reason to move the damper silently.

## Delivery

New module `timing_cover_attachment_candidate.build()` imports the six frozen joint STEP files and existing pan screw/washer STEP definitions. It returns revised parts, ten distinct fastener occurrences, reusable definitions, proposed transform records and original parts. It never rebuilds or writes the frozen candidate. Revised female material is part of the copied cover or future block land, not an installed threaded insert.

Stable station mapping, with engine-world `(X,Y,Z)` under-head coordinates in mm:

| Existing screw/washer index | Proposed position | Socket material |
|---|---|---|
| 20 | (365.5, −132, −32.1) | Future block land |
| 10 | (365.5, 196, −32.1) | Future block land |
| 21 | (390, −110, −32.1) | Cover |
| 23 | (390, 0, −67) | Cover |
| 22 | (390, 180, −32.1) | Cover |

Each keeps its `oil-pan-mounting-screw-N` / `oil-pan-mounting-washer-N` ID, parent `oil-pan-fastener-assembly`, zero rotation and reusable definitions. The other 20 pairs retain their existing transforms; total count stays 25. All positions remain estimates inherited from the accepted local joint.

The original Ø8.3 mm pan sockets surround the nominal Ø7.9375 mm screws with 0.18125 mm radial clearance, so they provide insertion space but no female thread. The new socket form is an explicitly ideal, zero-clearance conjugate of the current modeled male thread. It is an educational representation, not a production thread class, manufacturing tolerance, clamp-load or material-strength model. The checker must demonstrate actual helical contact, zero unintended overlap, seating, surrounding wall and interference under a deliberately wrong axial phase. Original cover/main-gasket/terminal/pan interfaces remain frozen except the bounded five socket interiors.

The seven cover axes propose stable future IDs `timing-cover-mounting-screw-1` through `-7` without adding occurrences. Frozen cover bores are R4.2 mm through X373.8…415; future land bores are R3.3 mm over X366…373. Those dimensions are not evidence of a nominal screw thread. A production hardware identification and actual mating threads remain required.

Commands from repository root:

```sh
.venv-cad/bin/python scripts/check-timing-cover-attachment-candidate.py
python3 scripts/render-timing-cover-attachment-candidate.py
```

Outputs: `cad/engine/generated/timing-cover-attachment-candidate/`, individual world STEP/GLB files, reusable pan screw/washer STEP definitions, combined `candidate.glb`, `preview.npz`, names manifest and `attachment-review.png`. New validation is `inventory/engine/timing-cover-attachment-validation.json`. No candidate release is published; original source images/manuals must remain outside Git/releases.

Environment: macOS 15.6.1 arm64, CAD Python 3.13.12, build123d 0.10.0, trimesh 4.7.4; renderer uses system Python, NumPy and Matplotlib. Usage/model-effort metrics unavailable. No canonical/shared files are owned or modified.

## Validation and review

Use 0.1 mm³ overlap/support convention, 0.01 mm³ adaptive STEP roundtrip volume threshold and watertight meshes. Socket changes must remain within the five declared R4.18 mm cylindrical regions. Existing source geometry is hash-bound; current assembly context and imported hardware are also bound. The actual drawing and render are required review inputs.

| Gate | Scope/status |
|---|---|
| Application/coverage | Pan nominal data supported; main-cover hardware unresolved |
| Dimensions/coordinates | Estimated socket form and relocated transforms explicit; stable IDs preserved |
| CAD/export | Bound report supplies actual outcome |
| Source/visual comparison | Actual pan drawing inspected; exported attachment view required |
| Installed interfaces | NOT RUN; local five-stack checks only; main screws and seal/hub unresolved |
| Motion/disassembly | Wrong thread-phase fault control only; no full engine/removal sweep |
| Learning/diagnostics | NOT RUN |
| Browser integration | NOT RUN |
| Reproduction/review | Root review pending; commands, input/export hashes retained |

## Tracking and restart

Issue #32 remains open. Overall attachment readiness cannot pass while main-cover hardware and the seal/hub interface remain unresolved. Root coordinates the future block union and any canonical changes. The previous sealing candidate and its root review remain immutable.

Thread refinement: the first conjugate construction closed directly over the male tip, creating an unintended bottom contact. That rejected source/checker and interrupted log are preserved in generated `rejected-bottomed-thread/`. A 4.0 mm radius tip-relief cutter now leaves the original 0.502 mm tip clearance and 14.2 mm of modeled thread engagement. Exact overlap checks clip distant material before testing a local screw so unrelated helical faces do not dominate the Boolean calculation; the checks remain exact solids, not mesh collision proxies.

The frozen uniform cover bosses place every proposed head seat at X415, 42 mm ahead of the X373 block face. A bolt must exceed 42 mm under-head length to enter the current 7 mm land bore; it reaches the modeled blind bottom at 49 mm. That is a model-derived feasibility interval, not a hardware prescription. It may require revising boss heights or land depth after exact hardware identification. The front seal has a modeled rear outer-annulus shoulder; forward axial retention would require a verified press fit or case construction, which the plain annulus does not establish.

Integration checkpoint advanced during this study: PR96 merged as `eb502ce755d12fe896b3ea915f3ada4361e52a9c`; active branch is now `engine/timing-interface-reconciliation`. Root confirmed canonical timing/pan inputs unchanged and active files preserved. This is the current handoff base; earlier contract and frozen joint hashes remain historical evidence.

## Final rejection and next action

**REJECTED**, not integration-ready. `inventory/engine/timing-cover-attachment-validation.json` freezes the findings. The current male STEP reports CAD validity, but both the canonical GLB and this roundtrip mesh are non-watertight after welding. A deliberately wrong axial thread phase returns zero common volume while independent point classification finds common interior points. That inconsistency invalidates the interference gate. Imported compound transform handling and empty-intersection handling also made raw overlap numbers untrustworthy; they are retained as rejected diagnostics, not accepted collision results. Intended female engagement/tip dimensions above are design intent only. No physical thread retention is accepted.

The main-cover hardware and 1 mm seal/hub gap remain unresolved. The exact unchanged seal/crank distance is effectively zero; no real seal lip or press fit is demonstrated. Root authorized a **new** isolated reusable male revision with verified nominal 5/16-18 ×0.87 in, existing estimated head/washer conventions and stable identities preserved. Frozen sealing geometry and its accepted local proof remain unchanged. No process remains running.
