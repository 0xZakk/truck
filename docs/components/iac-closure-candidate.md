# Component contract and handoff: illustrative IAC closure

## Contract

- Issue44 / engine parent1. Contributor pump_seal_finish; integration owner root. Current focused branch `engine/next-interface-contracts`; baseline commit5567d751abcf6a9bfac84bdf87ce0d7f0d4dac5c. Checker records actual input manifest and relevant source/geometry/pose hashes.
- Scope: isolated educational closure candidate resolving the inherited0.1mm radial gap and absent geometric retention. Not factory identification, manufacturing design, leak-rate certification or installed acceptance.
- Own `cad/engine/iac_closure_candidate.py`, `scripts/check-iac-closure-candidate.py`, `reference/engine/iac-closure-review.json`, this handoff. Generated reports/STEP/GLB/render remain in ignored `cad/engine/generated/iac-closure-candidate/`. No frozen attachment adapter, shared builder, manifest or canonical artifact edits.
- Identity/applicability: same unresolved unvented IAC study under issue44; exact1994 manual also illustrates a vent/filter variant. Actual owner's valve not identified.
- Interface: IAC-local millimeters, X along stem; current ancestor may translate. Preserve body front X=-24, spring seat X=-23, original8.5mm chamber radius and existing end-plug occurrence. New returned plug is IAC-local; later integration must undo its occurrence's local(-23.5,0,0) transform before defining it.
- Proposed retained flange: X=-23.7..-23.3, radius9.2; short inner portion X=-23.3..-23, radius8.5. An integral body lip ahead of the flange and a rear shoulder capture it. All these dimensions and the formed-lip choice are estimates.
- Expected changes: two existing definitions, no new material parts. No separate seal is inferred. Body groove and plug surfaces meet without overlap, and there is an unbroken modeled metal contact path around the circumference.
- Required checks: actual current body/plug/spring transforms and artifacts; exact pair contacts/collisions, continuous ring contact, same spring seat, retained flange in both axial directions, deliberate radial/axial gap faults, unchanged chambers/bypass ports, nearby geometry, STEP/GLB bounds and actual render. Tolerances remain0.01mm pose,1e-5mm³ intersection,0.2mm mesh bounds; no threshold reduction.

## Evidence ledger

`reference/engine/iac-closure-review.json` records reviewed exact1994 image/text hashes. The circular closure/rim is visible, but the images/text cannot establish whether its retention is pressed, crimped or threaded. Absence of depicted thread detail is not proof of absence. The candidate is an explicitly illustrative mechanically captured metal closure, not a claim that Ford used this construction. No separate elastomer or seal service item is supported by the reviewed page.

## Delivery / validation

Local candidate checks passed; not installed or Done. Entry point `build(body, radial_gap=0)` returns two IAC-local shapes; radial_gap is a fault-control input. The hypothetical lip is shown in its assembled form; the plug would be inserted before forming the lip. No elastic/plastic forming process, assembly force or reusability is simulated. Source/render discrepancies and final checker results follow below.

## Tracking

Issue remains open; no posts/commits. Root owns any later shared integration and browser review. Exact restart: run the isolated checker after the attachment installation is stable, then render and inspect its output. Python3.13/build123d0.10/OCP7.8; system Python supplies matplotlib. Usage/billing unavailable.


## Final isolated delivery — 2026-09-26

The reviewed factory images do **not** resolve whether the closure is pressed, crimped/staked or threaded. The study therefore uses a clearly labeled formed-lip choice with no added seal part. It supplies a geometrically closed, captured plug while preserving the spring datum; it does not identify or certify the actual truck's construction.

- PASS report: `cad/engine/generated/iac-closure-candidate/validation.json`, SHA-256 `4fcacfd1da5f1bf0edb07a3d1777b337bbe05b9e62b4bb6b807bdf2e1c1b8f5a`.
- Input manifest: `af0f6b5da21483ac6a71bba33ba20cf8e54130383a5f530d92374cb8f7307f07` (721 definitions / 1,326 occurrences). Relevant definitions, occurrence ancestry, source and artifact hashes remained unchanged during checking. Unrelated manifest changes are not silently treated as changed local geometry.
- Body change removes **15.569733 mm³**, entirely within the declared flange recess. No body material is added; original chambers and bypass port probes remain clear. The external body envelope does not grow.
- Flange has **38.924333 mm²** axial contact on each retaining face, **77.848666 mm²** total. Radial contact is **39.144244 mm²**; 72 circumference samples agree within5.2e-15mm. Spring contact remains **18.849556 mm²**, at the original X=-23 seat.
- Moving the candidate plug±0.1mm in X produces3.892433mm³ interference in either direction, demonstrating a captured flange. The old plug moved by the same amount has zero retaining interference and the original0.1mm radial gap.
- A deliberately undersize, axially floating plug leaves a continuous0.04mm-diameter witness passage from outside to chamber, with zero obstruction. The same passage intersects the candidate plug by0.002630mm³. This is a topology fault control, **not a fluid-flow or leak-rate calculation**. The floating plug also loses0.1mm of spring-seat contact.
- All local part pairs are free of positive-volume overlap in the assembled state. The current compact intake and throttle gasket selected by nearby geometry are clear; the throttle housing is also included among local parts.
- Both changed parts are valid single solids, survive STEP roundtrip, and export as watertight GLBs. Maximum mesh bound error **0.001819 mm**, below0.2mm; STEP volume error below0.001mm³. The report records hashes for two individual STEP/GLB pairs and one combined GLB.

Commands, from repository root:

```sh
.venv-cad/bin/python scripts/check-iac-closure-candidate.py
MPLCONFIGDIR=cad/engine/generated/iac-closure-candidate/.mpl-cache python3 scripts/check-iac-closure-candidate.py --render
python3 -m py_compile cad/engine/iac_closure_candidate.py scripts/check-iac-closure-candidate.py
```

Actual generated render reviewed: `cad/engine/generated/iac-closure-candidate/candidate-review.png`, SHA-256 `e5f657110691921c8e201fd0824f308525633f1a1d6b00da29e910da202d5e4c`. The left image is an actual CAD cutaway window showing the preserved spring seat. The right is a0.02mm-thick CAD section centered at Y=0, projected at equal X/Z scale, showing the flange between integral lip and body shoulder. No factory pixels are embedded or redistributed. Factory comparison supports only a distinct circular closure/rim; this candidate's stepped internal detail and formed lip are **not resolved by that source**.

| Quality gate | Result | Limit |
|---|---|---|
| Application / source identity | Partial | Exact1994 images reviewed; actual variant and closure process unresolved |
| Dimensions / coordinates | PASS locally | Explicit estimates, preserved spring datum and external envelope |
| CAD / export | PASS | Two valid single solids; roundtrip and watertight meshes |
| Source / visual comparison | Reviewed | Actual mesh and section inspected; no factory dimensional claim |
| Contacts / attachment / passage | PASS locally | Continuous contact, axial capture, negative channel and gap controls |
| Motion / disassembly | Bounded | Spring seat preserved; formed lip intentionally blocks straight plug withdrawal. Forming and destructive/service removal NOT RUN |
| Learning / diagnostics | Documented locally | No shared viewer metadata edits |
| Installed / browser acceptance | NOT RUN | Candidate only; root owns any integration |
| Reproduction / handoff | PASS locally | Source, input, output and render hashes; deterministic checker |

## Conditional integration guidance

This is **two existing definition replacements**, no extra part or occurrence. Keep the body's IAC-local frame. Preserve the end-plug occurrence at local(-23.5,0,0); the returned plug is already placed in the IAC frame, so move it +23.5mm X before assigning its definition. Its definition-local bounds then run X=-0.2..+0.5. Do not double-translate the plug or move the spring.

Apply the closure after the attachment adapter, then run a revised combined installed check. The prior attachment checker correctly binds `iac-valve-body` to the older no-groove candidate and **will become stale** after this intentional15.569733mm³ change; do not waive that mismatch or silently relabel its old PASS. A combined checker must bind the final closure body/plug and replay the retained screw/gasket/armature/spring contacts, current neighbors and sources. Only the obsolete0.1mm geometric-gap statement should be updated; manufacturing, material, thermal/contact-pressure, leak-rate and valve-variant uncertainties remain.

No canonical geometry, frozen attachment source, integration adapter, shared builder, manifest, viewer file, commit or external post was changed. Candidate files are ready for root review; no process is running. Issue44 remains open.

## Combined integration adapter follow-up

Root accepted the actual closure cutaway/section for provisional integration, subject to final artifact binding. The current722-definition checkpoint is being committed separately; this closure remains an isolated next-batch stage. **No apply is authorized to this worker.**

Additional owned files: `cad/engine/iac_closure_integration.py`, `scripts/install-iac-closure.py`, `scripts/check-iac-closure-installed.py`, `inventory/engine/iac-closure-learning.json`. The frozen attachment adapter and checker are unchanged.

The adaptation chain is explicit: base IAC/throttle → `iac_attachment_integration.install` → `iac_closure_integration.install`. Geometry replacement is limited to body and end plug. Five other attachment definitions receive only a targeted source/uncertainty update superseding the exact obsolete0.1mm end-plug-gap sentence; all their geometry, dimensions, names, colors and functions remain unchanged. No new definition/occurrence is added, and no occurrence position, rotation or explode vector changes. All IAC occurrence poses and ancestry are guarded, including unchanged internal parts and both screws.

The combined checker does not waive the changed-body hash. It binds body/plug to the closure candidate, the other five attachment definitions to their original candidate references, and independently proves that the final body differs from the attachment body only by removal of the declared15.569733mm³ recess. This subset proof covers unaffected external body collisions for every pose. The new plug is tested against all IAC internals, the current nearby-geometry broad phase, and its actual spring seat. All local part pairs, attachment contacts, both port probes, screw withdrawal, and19 targeted throttle poses (including current plate fasteners) are checked. It does not repeatedly sweep the whole engine.

Default installer mode is write-free. `--stage` uses only ignored artifacts. Root's eventual `--apply` must regenerate and validate a stage, confirm frozen source/artifact inputs and unchanged canonical manifest, then perform bounded backed-up writes. The staged counts remain722 definitions /1330 occurrences. A source-registry-only manifest update after this staged snapshot does not change geometry evidence; root's installer will restage against the latest registry.

```sh
.venv-cad/bin/python scripts/install-iac-closure.py
.venv-cad/bin/python scripts/install-iac-closure.py --stage
.venv-cad/bin/python scripts/check-iac-closure-installed.py
# Root only in the later integration batch:
.venv-cad/bin/python scripts/install-iac-closure.py --apply
.venv-cad/bin/python scripts/check-iac-closure-installed.py --installed
```

Shared changes for root's later batch: call the closure adapter immediately after the attachment adapter, merge `iac_closure_integration.sources()`, then load `iac-closure-learning.json` after `iac-attachment-learning.json` (viewer module `iac-closure`). Keep all geometry refresh selectors aware of both geometry IDs, both adapter/candidate sources, and the evidence ledger. The local closure hook is idempotent and the combined checker replays both adapters, including an extra synthetic subtree translation, to detect resuscitated gap metadata or double transforms. Browser/installed acceptance remains pending and issue44 stays open.


### Frozen combined-stage result

**PASS** — `cad/engine/generated/iac-closure-integration-stage/validation.json`, SHA-256 `f9d934824186b2a9c63cbb341836c6e07b037d29acc5334d71d78e71f69dd078`. Input manifest `62dcb37f469b21a93a74baa1fb81e44b2c7d69c8344d1cf18c667ce72a4fdff7`; staged manifest `860a1622e614888e9edabcb3ed9bd9e64160a040c5baf5aff9a97b221c269fe4`. Counts stay **722 definitions / 1,330 occurrences**. No canonical apply was run.

- Seven strict reference bindings pass: final closure body/plug plus the five unchanged attachment definitions. The changed body is never compared permissively against its old hash.
- Localized proof: added volume0; removed15.5697331912mm³; removed outside declared recess0. This retains the original attachment-body collision evidence outside the closure region.
- All IAC internal pairs, attachment/closure/spring contacts, port probes and both screws' withdrawal positions pass. Nineteen targeted poses of ten current throttle-moving occurrences—including four plate screws—pass. New plug versus compact intake CAD overlap is0.
- Two new mesh exports are watertight after coincident-position seam welding at1e-8m; no triangles added/removed. Maximum bounds error0.001819mm.
- Attachment→closure replay and replay after an additional-17mm whole-throttle-subtree translation both produce zero geometry difference for all seven affected definitions. Final metadata is identical, with no duplicate definitions or occurrences and no resurrected obsolete-gap statement. Twelve IAC/housing occurrence poses plus ancestry are guarded.
- Learning references, exact source/evidence bindings, source/artifact stability and syntax checks pass. Viewer/browser/installed acceptance remains pending for the later batch.

Root may proceed with the unrelated source-registry-only checkpoint. The next closure action is root's guarded restage/apply after that batch, followed by the combined installed checker and browser review. This worker has finished, all adapter/checker/learning files are frozen, and no process is running.

### Exterior-neighbor adaptation

The accepted intake exterior replaces `efi-upper-intake.step`/GLB after the original closure candidate. Original candidate reports remain unchanged. The closure installer now accepts that specific downstream neighbor change only through the exterior installed report, its stage-report hash, stage source hashes and exact canonical intake STEP/GLB hashes. All other candidate input guards remain enforced. The staged checker rechecks final intake against all IAC parts, preserves the original relative closure-neighbor poses and retains attachment/closure reference and motion checks. Root owns canonical installation; this change does not claim factory fidelity or waive a stale neighbor hash.

Exterior-adapted isolated stage PASS; validation SHA-256 `51a6c109e9008370c8483a7c9b2288595e512aadd8e61669bb6a8a23e82557c3`. Current intake/IAC pair check and original relative-pose checks pass. Root may review/install; canonical unchanged by this worker.
