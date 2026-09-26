# Component contract and handoff: distributor center contact

## Contract

- Issue: [#71](https://github.com/0xZakk/truck/issues/71), engine parent#1. Contributor: cap_interface_finish; integration owner: root.
- Baseline commit: `3e53f117146fe1746ef882abbeabf6542bcba0d2`; manifest SHA256 `80060a6dabed8f1f909e49852423fae03693aa3066e43a139438e240056aa8b2`.
- Scope: evidence-led isolated center-transfer candidate; no installed writes. Establish actual brush and spring topology before geometry. Exclude spark simulation, dielectric strength, ignition calibration and unsupported factory dimensions.
- Owned files: new `distributor-center-contact` research/handoff/check/report and `cad/engine/distributor_center_contact_candidate.py` only. No shared builders, manifest or current distributor edits.
- Identity: exact1994 manual cap E6AZ12106A and rotor E6FZ12200A; Ford current replacement listing maps rotor to DR375A. Current replacement revisions cannot prove original1994 details.
- Frames: millimeters, distributor native +Z shaft axis; preserve installed distributor assembly/rotation transforms, including current lean. Installed upper distributor geometry has a +50mm native lift relative to historical distributor.py: rotor-contact top134.5, brush134.5..137, coil terminal starts137. Candidate derives and restores this offset; checker requires50mm for this baseline.
- Neighbors: distributor cap, rotor insulator, rotor-contact, coil terminal, six peripheral terminals, shaft and bowl. Brush stays under cap parent; any supported rotor leaf moves with rotor.
- Inputs: local manifest/currentSTEPs, exact1994 offline manual (restricted), Ford replacement photographs (optional research captures; excluded from artifact release).
- Planned checks: valid intended solids; STEP roundtrip; GLB watertight/bounds; current contact/connectivity and support; full rotor cycle and cap axial removal; deliberate contact separation/collision negative controls. Existing overlap convention0.1mm³, contact distance tolerance1e-5mm; estimated fit is not electrical or production contact proof.

## Evidence ledger

See `reference/engine/distributor-center-contact-review.json` for source paths/hashes. Exact cap removal procedure identifies a rotor blade and spring. Viewed typical ignition drawing196152907 shows a raised/looped center leaf on the rotor. Current CAD uses a flat metal strip and simple separate central cylinder. Cap coil-spring construction is not yet supported.

## Delivery

- Readiness: **rotor-only integration-ready candidate**, pending canonical installation and browser acceptance. The wider cap-brush construction remains open under issue#71.
- Root reviewed and accepted the refined actual-mesh render: rounded free contact end, smooth folded transition into a central recess, open collar and captured outer pad. Bend/recess/stake dimensions and preload remain inferred.
- Three coordinated solids: existing `distributor-rotor`, existing `distributor-rotor-contact`, new selectable `distributor-rotor-center-leaf`. Preserve shaft seating, peripheral tip, existing occurrence frames and all cap geometry. No invented cap coil spring.
- Parametric API: `distributor_center_contact_candidate.baseline_parts()` reproduces the reviewed two original upper rotor solids with installed+50mm lift; `parts()` builds the revised three solids. The candidate checker proves the parametric baseline agrees with original canonicalSTEP geometry. No temporary or archived baseline fixture is needed for the adapter.
- Adapter API: `distributor_center_contact_integration.install(define, add, group, definitions, occurrences, assemblies, shapes)`. Call **after oil-drive/distributor adaptation**, then merge `sources()` into manifest sources. It recognizes original and reviewed revised solids independently, permitting repeat/partial refresh; it rejects unknown geometry and changed rotor-relative frames. Whole-distributor rigid translation/rotation is allowed. It does not move group frames.
- Learning: merge `inventory/engine/distributor-center-contact-learning.json` into the existing learning registration. All lesson part/source references are checked. Root owns shared entry points and browser registration.
- Owned code: `cad/engine/distributor_center_contact_{candidate,integration}.py`, `scripts/check-distributor-center-contact-{candidate,installed,promotion}.py`, `scripts/install-distributor-center-contact.py`; new evidence, learning, validation and this handoff. No canonical writes by contributor.
- Isolated STEP/GLB/render: `cad/engine/generated/distributor-center-contact-study/`. Staged manifest/exports/installation record/checks: `cad/engine/generated/distributor-center-contact-integration-stage/`. Restricted photo directory is excluded from any CAD release.
- Stage changes725definitions/1333occurrences to726/1334, with two replacements and one addition.

Reproduction/promotion commands from repository root:

```sh
.venv-cad/bin/python scripts/check-distributor-center-contact-candidate.py
.venv-cad/bin/python scripts/install-distributor-center-contact.py --stage
.venv-cad/bin/python scripts/check-distributor-center-contact-promotion.py
.venv-cad/bin/python scripts/install-distributor-center-contact.py
# Integration owner, after reviewing frozen stage:
.venv-cad/bin/python scripts/install-distributor-center-contact.py --apply
.venv-cad/bin/python scripts/install-distributor-center-contact.py --check-installed
```

The candidate command binds the pre-promotion canonical original context; after promotion use the installed checker. Parametric baseline geometry is retained in code for replay. Stage input/source hashes are checked before/after. Default installer is read-only preflight. Explicit apply uses the existing reviewed per-file atomic replacement helper with rollback on write/postcheck exceptions; nine outputs include the final validation record. This is not a crash-proof multi-file filesystem transaction. The isolated installed mirror tests asset/frame corruption and injected write failures1/3/9 plus postcheck failure.

`full_engine.py` is recorded as the historical stage exporter hash, not a continuing installed dependency: root may add the adapter/source/learning hook after promotion. Source/evidence/checker hashes, staged exports, distributor metadata and all scene pose fields remain enforced. Future geometry/pose changes invalidate dependent checks and require review/rerun; unrelated descriptive metadata does not silently alter geometric evidence.

## Validation and review

| Gate | Status | Evidence / limitation |
|---|---|---|
| Application/coverage | PASS bounded rotor topology | Exact1994 cap/rotor IDs, service rotor-spring wording, actual FordDR375A contact photo. Hidden cap brush remains unknown. |
| Dimensions/coordinates | PASS explicit estimates | Leaf0.4mm thick×6mm wide; collarR10/R8; inferred recess and folded centerline; installed native+50mm offset. No factory dimension claims. |
| CAD/export | PASS | Three valid single solids, STEP roundtrip, watertight GLB and CAD/GLB bounds checks. |
| Source/visual comparison | PASS bounded root review | Actual depth-buffered export render: assembled rotor and isolated leaf/conductor. Broad original rotor body remains simplified. |
| Installed interfaces | PASS staged; canonical pending | Four nominal interfaces have zero gap/overlap and positive planar contact area. Shaft-seat/outer-tip protected differences0. Whole-scene rest audit16exact pairs,3977AABB exclusions. |
| Motion/disassembly | PASS sampled | 37crank poses across720°,296exact local pairs, zero center gap; cap lift0..80mm sampled. No deflection/preload model. |
| Learning/diagnostics | PASS links and stated limits | Separate leaf, cap contact, outer conductor and insulator explanation; no invented resistance or repair specification. |
| Browser integration | NOT RUN | Root owns canonical installation, select/isolate/explode/motion/reset and console check. |
| Reproduction/review | PASS hashes and replay | Repeat, partial baseline refresh and whole-distributor rigid move replay with zero geometry differences; bad frame/geometry rejected. |

The raised leaf conducts toward the outer rotor tip while accommodating the center contact. The existing model transfers from coil terminal to a short center-contact envelope and then to this leaf. Geometric continuity is demonstrated, but brush attachment, material and contact pressure are not established. Source evidence supports a spring leaf in the rotor; it does not support a helical spring inside the cap.

Negative controls lower the leaf0.5mm to create a0.5mm gap and raise it0.5mm to create interference. Separate capture controls translate the leaf foot/conductor0.2mm into their retainers. These prove check sensitivity and idealized axial capture, not production fit or elastic force. Isolated promotion controls reject a corrupted leafGLB, shifted leaf frame and changed external scene frame, and verify rollback after injected failures.

## Tracking and restart

- Root may promote the accepted **rotor-only improvement** after final frozen report review, then hook the adapter and learning/source registration and run installed/browser checks. Do not label cap brush construction finished.
- Next source need: applicable cap section, close underside/profile, physical specimen or manufacturer drawing establishing center-contact projection/material/retention and coil-feed interface. Current replacement photo is insufficient.
- New leaf parent remains `distributor-rotation` with native zero pose and explodeZ225. Existing two IDs/frames/explode vectors stay stable. No mounting or timing datum is corrected by this scope.
- No background process should be assumed after handoff. Restricted originals are optional reviewer dependencies; no photos/manual originals are redistributed. Usage/model-effort unavailable.

Final frozen revision on `engine/cable-and-distributor-contact`, post-checkpoint `cccf3d8`: current canonical725/1333 SHA256 `4f98bbdad7fb1996487d17c4a651de588cef39254efe24e96384375dbdce0c07`. All commands above passed through preflight; contributor did not apply.

- `inventory/engine/distributor-center-contact-candidate-validation.json`: `6b3465099b438e8b25031d0da7d70ace0570644069d07c04cc7eb6d747fb2d75`
- `cad/engine/generated/distributor-center-contact-integration-stage/installation.json`: `4cd6a6fc7423d37c0ef5963c4d8060e7ae1c1f067dd64828179e44e8951321b5`
- `cad/engine/generated/distributor-center-contact-integration-stage/validation.json`: `8423736e7edc00e9da3355f614714a68d3071544638bbae344a85ec25ec042c6`
- `inventory/engine/distributor-center-contact-promotion-validation.json`: `3114e590813e8c7006e421fe3f6fc73c079c1339d54e819caf8647d81234586a`

Measured modeled planar contact areas: center12.5664mm², leaf-to-outer43.1969mm², leaf seat45.6907mm², outer-conductor seat65.0270mm². These are candidate CAD contact areas, not factory or electrical specifications.


## Integration-owner review — 2026-09-26

Root installed the frozen rotor-only package and verified exact shape equality/protected interfaces. The builder/source/learning hooks are installed. Browser review passed the29-part assembly, transparent50% explosion at180degrees crank, and direct leaf part page. Direct part HTML lacked the shared throttle control; that regression was repaired and checked. See `inventory/engine/cable-distributor-browser-review.json`. This accepts the stated illustrative rotor scope; hidden cap construction and production dimensions remain open.
