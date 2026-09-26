# Component contract and handoff: illustrative cable integration

## Contract

Issue #43 under engine #1. Integration lead owns shared `full_engine.py`, atlas, navigation, application and browser acceptance. This worker owns the new cable adapter, installer, installed checker, learning file, motion exporter/module/table/checks/reports and this handoff. The historical candidate report and its temporal-provenance addendum remain unchanged. This is an educational engine-end mechanism, not a verified Ford cable reconstruction or service specification.

The initial requested integration baseline was 725 definitions / 1,333 occurrences. During preparation, the integration lead's unrelated distributor update produced current manifest `d172e97a054c37cbbb3d51a9117fae7c43624e2e4667750d7386dbf9d1a3b014`, 726 / 1,334. Staging uses that actual current manifest and adds exactly seven definitions/occurrences, giving **733 / 1,341**, plus replacement geometry for `accelerator-cable-bracket`. Existing occurrence IDs, local poses and all assemblies remain unchanged. No canonical application by this worker.

All new components use identity local occurrence transforms under `throttle-assembly`. Their neutral shapes already use parent-local CAD millimeters; the current −167X ancestor shift is not baked in. The seven IDs are `throttle-cable-{snap-retainer,sheath-stub,socket,swivel-seat,fixed-guide,core,compression-spring}-illustrative`. `throttle_cable` occurrence metadata is `{model: 'illustrative-cable-v1', kind: ...}` with fixed, socket, seat, guide, core or compression-spring kind. Explode offset is parent-CAD `[0,75,0]`, separate from operating motion.

## Evidence ledger

See `docs/components/throttle-cable-candidate.md` and `reference/engine/throttle-cable-review.json` for source URLs, inspected figures/specimens, hashes, selected proportions, exact proposed bracket change and gaps. Exact1994 documentation establishes the accelerator cable's ball attachment and distinct cable-end compression spring. Replacement photographs support the long socket/stem, overlapping guide/coil and bulky retainer topology. Dimensions,24 turns, hidden spherical joint/guide retention, materials, force, rate and owner-installed identity remain unverified. C6 hardware, unverified cruise equipment and full firewall/pedal routing are excluded.

The full candidate passed47 exact CAD poses and2,360 collision pairs. Its checker accidentally sampled the manifest hash at finish rather than load; that limitation is preserved explicitly in the original report. A separate final-current addendum bound selected STEP hashes and47 poses to the identified pre-electrical snapshot. The derived `inventory/engine/throttle-cable-candidate-proof-scope.json` preserves those original relative pose probes and candidate-report hash; the installer embeds them in its installation record, allowing subsequent installed checks to tolerate a rigid ancestor shift without needing the old snapshot at check time.

## Delivery

Files:

- Adapter `cad/engine/throttle_cable_integration.py`; installer `scripts/install-throttle-cable.py`; checker `scripts/check-throttle-cable-installed.py`.
- Last-loaded lesson module `inventory/engine/throttle-cable-learning.json`, using registered source ID `throttle-cable-engine-end-illustrative-study`.
- CAD motion exporter `scripts/export-throttle-cable-motion.py`; data `viewer/throttle-cable-motion.json`; pure JS helper `viewer/throttle-cable-motion.js`; Node check `scripts/check-throttle-cable-motion.mjs`.
- Reports `inventory/engine/throttle-cable-motion-validation.json`, `throttle-cable-viewer-validation.json` and staged report described below.
- Ignored stage `cad/engine/generated/throttle-cable-integration-stage/`, including baseline manifest/STEP, staged manifest/STEP/GLB and installation record. Root applies and publishes artifacts under the repository artifact policy. No release created by this worker.

Environment: macOS, Python3.13.12, build123d0.10.0, trimesh4.7.4, project Node runtime. CAD mm, viewer meters `[X,Z,-Y]`, existing display scale. Model/effort/usage unavailable.

From repository root:

```sh
# Read-only plan; no canonical changes.
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/install-throttle-cable.py
# Isolated staging and checks.
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/install-throttle-cable.py --stage
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-throttle-cable-installed.py --stage-dir cad/engine/generated/throttle-cable-integration-stage
# Reproduce exact-CAD motion table and pure JS validation.
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/export-throttle-cable-motion.py
node scripts/check-throttle-cable-motion.mjs
# Integration lead only: restage, check and guarded apply with rollback.
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/install-throttle-cable.py --apply
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-throttle-cable-installed.py
```

The installer validates candidate and motion report hashes, snapshots actual current inputs, scopes inventory mutations, and checks prior-install artifacts before idempotent reapplication. `--apply` always runs staged preflight before writing canonical artifacts. Existing component IDs/poses and all unrelated inventory are preserved. First-time staging loads the tracked proof-scope data; later installed checking uses its embedded probes. A future clean rebuild must obtain the reviewed candidate STEP/GLB artifacts through the project's artifact release, or regenerate a new full current candidate proof. The original snapshot is identified by hash for auditing but is not required by the installed checker.

## Exact shared hook plan

In the shared engine builder, after existing throttle bracket/linkage/shield/shaft-spring and plate adapters have supplied their final shapes:

```python
import throttle_cable_integration as throttle_cable
throttle_cable.install(define, add, defs, occurrences, assemblies, shapes)
sources.update(throttle_cable.source())
```

Append `'throttle-cable'` last in `engineLearningModules`. Its `throttle-assembly` lesson preserves the plate/IAC context while adding the cable-end spring distinction and explicit limits. All nine lesson targets/source references were checked against the staged manifest.

## Viewer contract

```javascript
import {createThrottleCableMotion} from './throttle-cable-motion.js';
const motion = createThrottleCableMotion(await response.json());
const frame = await motion.frame(throttleAngle);
```

Stable API: `frame(degrees)`, `angle(degrees)`, `cachedAngles()` and `clear()`. Angles snap to nearest integer and clamp0–90; invalid numbers throw. **No interpolation between incompatible triangulations.** Only requested frames decompress; concurrent/repeated requests share a cached promise. The9,037,954-byte table contains compressed exact-CAD tessellations for the core and spring at all91 integers, plus neutral-to-angle rigid transforms for socket/seat/guide. It retains the captive core terminal and grounded coil ends rather than replacing them with generic tubes. Normals are averaged for viewer shading; no material simulation is implied.

Each `frame.rigid[kind]` has `translation_cad_mm` and `quaternion_viewer_xyzw`. These operate on the complete neutral GLB in the throttle parent's frame, not on a recentered part. After the existing pose loop resets the occurrence and applies explode offsets, add `toView(translation_cad_mm)` to its position and apply the quaternion delta. Preserve the parent's transform and original object display scale. Fixed retainer/sheath receive no motion.

`frame.meshes.core` and `frame.meshes['compression-spring']` return typed positions/normals/indices. Positions already use viewer meters `[X,Z,-Y]` in the throttle parent frame. Replace the mesh geometry with these arrays, leaving the occurrence's neutral quaternion and its current exploded position intact. Vertex/index counts may vary by angle: replace attributes/index rather than assuming a fixed-size buffer. Dispose superseded dynamic geometry without disposing shared original GLBs. Keep neutral GLBs for0/reset if desired; retain their geometry references. Lazy fetch on first nonzero request is supported. Guard asynchronous responses against a stale requested angle/navigation state so a late frame cannot overwrite the user's newer selection.

## Validation and review

| Gate | State and coverage | Limits |
|---|---|---|
| Application/evidence | Candidate evidence preserved; source topology and estimates visible in learning | No factory count/dimension/rate or owner-cable identity claim |
| Coordinates/interfaces | Candidate equivalence, protected anchors and local-frame negative controls in staged checker | Rigid ancestor shifts allowed; changed local frames rejected |
| CAD/export | Staged checker verifies valid one-solid, welded watertight GLB, exact shape differences and bounds | Existing0.2mm bounds and1e-5mm³ difference/overlap gates retained |
| Motion | CAD table has91 valid exact-CAD mesh poses; original nearby CAD sweep47poses |91 mesh poses do not claim91 exact neighbor collision sweeps |
| Viewer geometry | PASS: closed oriented topology across all91 poses; max anchor error5.84e-12mm; max viewer bounds discrepancy0.090817mm | Tessellation parameters0.025mm/0.5rad; vertex quantization0.0001mm; no interpolation |
| Idempotence/scope | Adapter twice and bracket exact symmetric difference checked | Final staged results below |
| Learning | PASS:9 lessons, source IDs and links resolve in stage | Root must load the module last |
| Browser/root acceptance | NOT RUN by this worker | Root owns actual atlas hookup, motion/explosion/reset and browser review |

**Final staged PASS:** manifest `0656841ba587a3f05d193aa75fb711f320ddf732cc0343c68504836c9ea7537d`, 733 definitions / 1,341 occurrences; report `inventory/engine/throttle-cable-staged-validation.json`. All eight actual STEP shapes have exactly zero symmetric difference from the reviewed candidate after consistent STEP normalization. All eight GLBs are watertight after the documented position weld; maximum actual bounds discrepancy is0.002173mm. The twice-applied bracket has zero normalized symmetric difference, adapter twice preserves counts/unrelated inventory, and protected-anchor change is zero. The displaced-socket geometry negative control produces 604.961850mm³ difference; the wrong local bracket frame is rejected. No current nearby STEP or relative motion changes required additional exact pairs; the checked47-pose/2,360-pair candidate proof is inherited explicitly, not reported as a newly rerun sweep. The checker compares actual stage shapes against reviewed candidate geometry, repeats all-current broadphase, inherits unchanged47-pose exact pairs only after STEP and relative-pose equivalence, and reruns affected pairs if any neighboring shape/motion differs. It captures manifest hash at start and end through an input guard, avoiding the historical temporal bug. No generic collision exclusions or lowered thresholds.

## Tracking and restart

Issue #43 remains open. Root reviews staged evidence, applies, integrates viewer/learning hooks and performs browser acceptance. Code/candidate readiness is separate from installed acceptance. No source-photo composite may enter the shared archive. Worker has not applied or committed canonical changes. No worker processes remain. Final staged, CAD-motion and JS-motion checks PASS; root application/browser acceptance remain outstanding. The original candidate report and temporal addendum were not modified.


## Integration-owner review — 2026-09-26

Root applied the guarded installer against the rotor-integrated baseline, then verified canonical STEP/GLB equality and current neighbor scope. Shared builder, source and last-loaded learning hooks are installed. Browser acceptance passed assembled0/45/90degree views,50% explosion at90degrees, reset and individual spring selection. Asynchronous stale-response/reset/failure controls pass. See `inventory/engine/cable-distributor-browser-review.json` and `throttle-cable-installed-validation.json`. This accepts the stated educational engine-end scope; factory geometry, stops, rate/preload and full vehicle routing remain open.
