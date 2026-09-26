# Component contract and handoff: IAC attachment candidate

## Contract

- Issue [#44](https://github.com/0xZakk/truck/issues/44), engine parent #1; throttle interface #43. Contributor pump_seal_finish, integration owner root.
- Baseline commit `5567d751abcf6a9bfac84bdf87ce0d7f0d4dac5c`; candidate report records manifest hash and scoped poses/artifacts. Unrelated manifest edits are permitted only when relevant dependency hashes and poses remain unchanged.
- Isolated educational candidate: two mounting screws, mating flange/gasket/receiver modifications, illustrative return spring and armature/stem contact sleeve. Excludes actual thread geometry, forces, valve calibration, installed variant identification, new electronics, shared installation.
- Own `cad/engine/iac_attachment_candidate.py`, `scripts/check-iac-attachment-candidate.py`, `inventory/engine/iac-attachment-candidate-validation.json`, `reference/engine/iac-attachment-review.json`, this handoff. No shared builders, manifest or viewer edits.
- Identity: factory 9F715 valve and 9F670 gasket topology. Archived service number FOTZ9F715CA has ambiguous O/zero; no inspected replacement specimen establishes the truck's valve identity.
- Millimeters; candidate frame is installed `idle-air` frame at CAD (397,25,540), +X toward solenoid. Throttle input is transformed into that frame. A later whole-subtree translation must move all parts/receiver changes together.
- Two estimated screw axes at local(-16,-21) and(16,21), +Z withdrawal. Head bearing plane Z=-10, flange bottom=-13, gasket=-14..-13, receiver mouth=-14, blind bottom=-24, screw tip=-23. These dimensions are model-derived estimates.
- Neighbors: all eight original IAC parts, throttle casting and nearby installed components. Original gasket underside world Z526 matches casting pad top. Two bypass centers remain X±12,Y0; no routing shift.
- Inputs: canonical per-definition STEP, relevant manifest poses, original IAC/throttle source and exact1994 local factory pages/images. Images reviewed locally; not redistributed.
- Planned checks: exact pair overlap <=1e-5 mm³, planar contacts, ports, blind-hole tip clearance, spring/pintle trial travel and armature linkage, STEP/GLB roundtrip/bounds <=0.2mm, negative oversized and lifted screws, blocked ports, missing spring linkage. Export/render under ignored `cad/engine/generated/iac-attachment-candidate/`.

## Evidence ledger

See `reference/engine/iac-attachment-review.json` for reviewed source paths and SHA-256. Factory images 442080900/442083839 establish two diagonal retaining bolts and a separate two-port gasket. 441899701 depicts the unvented reverse-seated design; 441904883 depicts a different vent/filter design. The installed truck variant remains unresolved. All fastener dimensions, added casting contour, sleeve joint and spring construction are estimated. No spring force, factory preload or calibrated valve travel is claimed.

## Delivery

Local candidate checks passed; isolated educational candidate, not installed or Done. Entry point `build(body, gasket, throttle, armature)` receives IAC-frame shapes and returns changed/new shapes. Original parts remain unchanged on disk. Spring builder accepts illustrative pintle travel, not commanded duty cycle.

## Validation and review

Checker and actual render review completed below. Browser and installed engine acceptance NOT RUN. Source fidelity remains provisional regardless of geometry checks.

## Tracking and restart

Issue remains open/in review. No commits or external posts. CAD runtime `.venv-cad` uses build123d0.10/OCP7.8, Python3.13; rendering uses system Python with matplotlib. Usage/billing unavailable.

## Integration proposal (not performed)

Preserve the existing four definition IDs `iac-valve-body`, `iac-gasket`, `iac-armature`, `throttle-housing`. Pass the actual installed shapes to `build` after placing them in the IAC frame. The returned throttle housing is **IAC-local**: transform it back with the current `idle-air` frame before defining it in the throttle parent, whose housing geometry is currently world-coordinate. The three IAC definitions remain in their existing local frame. Do not apply the IAC transform twice.

Define one reusable `iac-mount-screw-estimated` using `screw()`, and add two occurrences `iac-mount-screw-1-estimated` / `iac-mount-screw-2-estimated` under `idle-air` at (-16,-21,0) and (16,21,0). The checker exports those placed occurrences separately for inspection. Add `iac-return-spring-estimated` under `idle-air` at identity. Expected installation delta is **two definitions and three occurrences**, plus four replaced definitions. Keep the existing standalone IAC source available as historical study; update active learning descriptions so the restoring mechanism is no longer called absent, while preserving variant, dimension and construction uncertainty.

If the coordinated intake/throttle subtree moves -167mm X, move the receiver and all IAC parts together. Re-run against the translated frame; do not copy this candidate's (397,25,540) origin into the new assembly. `build` itself is frame-local and does not need an absolute-origin change; the checker’s explicit frame assertion intentionally rejects an unreviewed relocation.

Use the shared exporter, first clearing cached triangulation and tessellating these changed shapes at 0.05mm / 0.1rad (as the candidate checker does). Bind the exported STEP and mesh to the checked candidate solids; a source hash or successful export alone does not establish that match. Then run installed neighbors, motion, navigation, learning and browser review before any installed acceptance.

## Geometry interpretation and remaining scope

- Screw geometry: estimated5mm nominal smooth shank,13mm underhead length,4mm hex head,5.6mm flange/gasket clearance and5.1mm blind receiver envelope. There is9mm axial engagement envelope and1mm tip-to-bottom clearance. **No helical thread or torque/load capacity is modeled**; the factory8–11Nm text is not a rating for this invented screw.
- Body flange is3mm thick; original1mm gasket is extended to the two ears. Receiver material stays above the main throttle bore envelope. Original two bypass routes and both IAC chambers remain open.
- The spring is illustrative:0.8mm wire,3mm mean radius,5.75 helical turns, idealized annular closed ends. Its end surfaces meet the original end plug and pintle. End-ring radii2.5/3.5mm and thickness0.8mm are constructive approximations, not factory measurements. The modeled spring could push toward the closed seat, but rate/preload, stress and dynamic behavior are not validated.
- An estimated sleeve brings armature inner radius to1.5mm over X36..53.5, contacting the stem. This represents a bonded educational joint. The manual supports direct linkage, not this attachment construction or its strength.
- The three trial positions are relative offsets -1/0/+1mm, with axial valve-seat gaps2/1/0mm. They are not calibrated production travel or duty-cycle states. At +1mm the reverse-pintle disc contacts the seat annulus.
- The existing end plug still has0.1mm radial clearance to its bore; its actual retention/sealing construction is unresolved. The entire valve is **not certified leak-tight**. Electrical terminals, installed variant identity and possible variant-specific diaphragm/vent/filter remain open scope; no speculative electronics were added.
- Actual render comparison: two opposite diagonal fasteners, separate two-port gasket and reverse-seated stem match factory topology. The inherited rectangular chamber/body contour and horizontal teaching pose differ from the service illustration; they are not a reconstructed production casting or measured installation angle.


## Final local validation — 2026-09-26

- PASS report: `inventory/engine/iac-attachment-candidate-validation.json`, SHA-256 `aaf9dcaf33714d10333d9e4a703776e655487336a4fd4d2478e5439a46e28041`.
- Baseline718 definitions /1322 occurrences; manifest `bfab1f2596991d27fe5e52e90f02d070eb034f9de8c2cd72d3dd44666d6c8bb9`. Relevant source/artifact hashes and actual definitions, occurrences and ancestor transforms are recorded and unchanged during the run. The full manifest hash is provenance, not a demand that unrelated components stay frozen.
- Twelve local assembled solids valid/single; seven changed/new solids exported and reimported as STEP and watertight GLB. Maximum CAD-to-reloaded-mesh bound discrepancy0.002177mm (limit0.2mm); maximum STEP volume discrepancy1.1e-9mm³ (limit0.001mm³).
- All66 internal pairs clear of positive-volume overlap. Eleven installed nearby occurrences selected from the full manifest mesh bounds; changed-part comparisons clear. Nineteen throttle positions0–90° and six axial withdrawal positions per screw0–40mm clear. These are bounded geometric checks, not a tool-access or service-clearance certification.
- Head bearing area27.980957mm² each; gasket contact1555.598235mm² on each face. Spring seats18.849556mm² each; armature/stem gap0, overlap0. Closed trial pintle-seat area95.001762mm². Two bypass probe volumes, both original chamber probes and both main-bore probes report zero obstruction.
- Fault controls reject6.2mm oversized shank (104.544350mm³ intersection), lifted head (1mm bearing gap), blocked port (75.429640mm³), original disconnected armature (0.1mm gap), shifted spring (1mm lost seat contact).

| Quality gate | Result | Scope and remaining limits |
|---|---|---|
| Application/coverage | Partial | Exact1994 mounting topology; actual installed variant and specimen dimensions unresolved |
| Dimensions/coordinates | PASS locally | Explicit model-derived estimates and source/pose guards; no factory dimensional acceptance |
| CAD/export | PASS | Seven changed/new STEP and GLBs; source-bound output hashes |
| Source/visual comparison | Reviewed | Factory pixels and actual candidate mesh render; topology only, casting/pose discrepancies documented |
| Installed interfaces | NOT RUN | Candidate replaces required interfaces locally; canonical assembly untouched |
| Motion/disassembly | PASS locally |19 throttle poses,3 illustrative pintle poses,6 withdrawal poses per screw; no force/elastic simulation |
| Learning/diagnostics | Pending integration | Descriptions/limits in handoff; no active viewer lesson edits |
| Browser integration | NOT RUN | No canonical meshes/manifest changes authorized in this task |
| Reproduction/review | Reproducible candidate | Commands below; integration-owner acceptance pending |

```sh
.venv-cad/bin/python scripts/check-iac-attachment-candidate.py
MPLCONFIGDIR=cad/engine/generated/iac-attachment-candidate/.mpl-cache python3 scripts/check-iac-attachment-candidate.py --render
python3 -m py_compile cad/engine/iac_attachment_candidate.py scripts/check-iac-attachment-candidate.py
```

Ignored artifacts: `cad/engine/generated/iac-attachment-candidate/` contains seven STEP files, seven individual GLBs, combined candidate GLB, `preview.npz`, and `candidate-review.png`. Combined candidate GLB contains the seven changed/new components; the context render also shows unchanged local IAC geometry. Assets use CADmm to viewer[X,Z,-Y]/1000 conversion. No factory images or manuals are redistributed.

Actual rendered mesh review: `candidate-review.png`, SHA-256 `0f98493cae030199d5a40377749cb583622cabc2ec77854a307a8655312613d8`, reviewed from the generated image pixels. Left panel shows throttle context, gasket and two screw seats; right panel exposes the stem/armature and spring seats. The reviewer inspected actual pixels after the final geometry check. No production dimensional comparison can be made without an identified specimen.

Handoff: candidate files frozen after this report. No running process. Root may preserve the candidate code, but must review the conditional integration proposal and active assembly behavior before installation. Issue44 remains open; no board or GitHub status was written. Next action is root review of this handoff and render, then an isolated integration adapter/installed revalidation if the educational scope is accepted.

## Integration adapter follow-up (staged and checked)

Additional owned files: `cad/engine/iac_attachment_integration.py`, `scripts/install-iac-attachment.py`, `scripts/check-iac-attachment-installed.py`, `inventory/engine/iac-attachment-learning.json`. Root owns shared hooks, canonical install and browser review. The candidate source and original report remain frozen.

The adapter derives the IAC frame from actual ancestry and converts each incoming definition through its occurrence frame. Throttle-to-IAC remains (-397,-25,-540) locally even when the entire throttle subtree translates -167mm X. The returned housing converts back into its original definition frame. The adapter preserves all existing positions, rotations and explode vectors; only relevant descriptions and four definitions change. Repeated application reuses the same geometry and refreshes the two reusable definitions/three occurrences without duplicates. Changed candidate evidence after an existing install is rejected pending a fresh upstream-base review, preventing parameter changes from silently accumulating material on previously modified shapes.

Default `scripts/install-iac-attachment.py` prints a write-free plan. `--stage` writes only the ignored integration-stage directory. `--apply` is reserved for the integration owner and requires successful stage checker, frozen source/artifact guards and unchanged input manifest before a bounded backup/rollback write. Unrelated manifest changes since the historical candidate report are allowed because current stage neighbors and affected motion are independently checked; source/geometry identity for the actual candidate parts remains required.

Commands after root's compact-intake checkpoint:

```sh
.venv-cad/bin/python scripts/install-iac-attachment.py --stage
.venv-cad/bin/python scripts/check-iac-attachment-installed.py
# Integration owner only, after reviewing stage and shared hooks:
.venv-cad/bin/python scripts/install-iac-attachment.py --apply
.venv-cad/bin/python scripts/check-iac-attachment-installed.py --installed
```

Shared hook, owned by root: call `iac_attachment_integration.install(define, add, group, defs, occurrences, assemblies, shapes)` after the base IAC/throttle and coordinated intake frame changes. Merge `iac_attachment_integration.sources()` into sources, merge `inventory/engine/iac-attachment-learning.json` into learning, and add `iac-attachment` to the shared viewer learning-module list. These shared changes are not performed by this worker. Full-engine rebuilds must refresh the six IDs in `CHANGED_IDS` when any adapter/candidate/review input changes; the installer stages all six unconditionally. Installed definition descriptions remain provisional and issue44 remains open.

Stage validation passed on the root's settled relocated-intake manifest; no canonical writes by this worker.


### Adapter handoff — frozen after staged PASS

Root reviewed the original candidate render and accepted the provisional educational scope subject to installed checks. The compact intake was installed first. Stage input:719 definitions /1323 occurrences, manifest `36e05dfee7ea0ee12761295851c8fbe804ea0d3a516502e069f1059e77bc131b`. Staged result:721 definitions /1326 occurrences, manifest `af0f6b5da21483ac6a71bba33ba20cf8e54130383a5f530d92374cb8f7307f07`.

`cad/engine/generated/iac-attachment-integration-stage/validation.json` is **PASS**, SHA-256 `fa72ee374995c5f1874973289dbe53072534fa09a76e9a68b86803dcd5f0b483`. All six reusable STEP definitions match their placed candidate references with symmetric difference below0.02mm³; all six translation negative controls reject a1mm shift. The two screw occurrences use one definition at their distinct reviewed positions. Twenty-five actual current neighboring occurrences were discovered from all manifest mesh bounds and checked, including the relocated compact intake; no positive-volume interference was found internally, with neighbors, through19 throttle positions, or through six axial withdrawal positions per screw.

Both ordinary adapter replay and replay after an additional synthetic-17mm X whole-throttle-subtree shift return **zero** symmetric geometry difference for all six definitions, with identical definition callback metadata and occurrence/group inventory. These controls exercise the actual moved frame and prevent a double-transform or duplicate-definition interpretation. Source, artifact and relevant pose guards remained stable throughout the check.

The shared GLB exporter preserves duplicate vertices at CAD face seams. The checker welds coincident positions at1e-8m precision solely for its topology test; all six are watertight, with no degenerate/duplicate triangles and no faces added or removed. Canonical/staged GLBs are not rewritten by the checker. Largest CAD-to-mesh bound discrepancy remains0.002177mm against0.2mm. The installer records model bounds explicitly for all six definitions.

The stage inspector, default write-free installer mode, and Python syntax checks passed. Installed checks and browser review are the integration owner's next actions. `--apply` always regenerates a stage and reruns the checker before its guarded canonical writes; a stale stage cannot be promoted directly. Adapter, installer, checker and learning files are frozen for root's apply/check. No running process remains in this worker and no canonical artifact, shared builder, viewer file, commit or external post was modified here.
