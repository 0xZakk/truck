# Component contract and handoff: oil-filler-cap

## Contract

- Issue: #15; engine system; integration owner is coordinating agent, component worker cap_interface_finish. GitHub issue fetch was unavailable; assignment and existing pilot supplied scope.
- Baseline: `d410ca6666d764b02b392e07e05befd1c4309e9c`; manifest SHA-256 `821f7d3bb47d49a00ffb2975fa5faffcd306fe90bea48ce7c0d6308cd636653f`.
- Scope: candidate interface investigation and reproducible installed-rocker clearance check; no production dimensions inferred from appearance. Factory retention remains critical.
- Owned paths: `cad/engine/pilot/oil-cap/`, `scripts/pilot/oil-cap/`, `inventory/engine/pilot/oil-cap/`, this handoff. Shared assembly changes reserved to integration owner.
- Identity: EC743 / Ford service number F3AZ6766B; exact 1994 F-150 4.9 Gas catalog applicability is captured in existing evidence, but actual truck identity is unverified.
- Coordinates: CAD Z-up millimetres; cap local origin at `(240,-12,419)` in closures, seal underside local Z=-6 touches cover world Z413. Standalone GLB uses metres `(X,Z,-Y)`. Existing explode vectors retained.
- Neighbors: valve-cover smooth radius17 fill bore, cap annular seal, all twelve installed rocker occurrences; c1 intake is nearest in rest pose. No geometry changes authorized to cover in this worker.
- Inputs available: current manifest, generated rocker/cover STEP, current shared motion dispatcher, candidate source/STEP and primary-source captures. STEP restoration follows `docs/CAD-ARTIFACTS.md`; no temporary baseline required.
- Checks: portable static export/interface checker; dynamic 0–720 crank sweep at 5° plus each valve peak and event endpoint; exact BREP distance and overlap within 15 mm broad phase. Overlap audit threshold 0.1 mm³, positive geometric clearance required with 0.002 mm numerical floor. These are numerical checks, not manufacturing allowance. Negative control lowers cap into closest rocker and must detect overlap.

## Evidence ledger

| Feature | Value / datum | Class | Source | Limits |
|---|---|---|---|---|
| Screw retention | Male screw / nonvented | Replacement comparison + Ford image topology | `inventory/engine/pilot/oil-cap/evidence.json`; Ford EC743 page; MotoRad MO100 | Factory thread profile/lead absent |
| Candidate size | Neck 31.24, shell 69.09, height 38.10 mm | Replacement comparison | MotoRad MO100 | Not Ford production metrology |
| Thread pitch/root | 4.5 / 28.84 mm | Inferred | Candidate Parameters | Must not transfer into production cover |
| Seal | OD44, ID31.6, thickness3 mm | Inferred | Candidate Parameters | Compression, groove and rubber unknown |
| Cover seat | Z413, smooth bore34 mm | Verified model geometry | Current cover STEP hash in report | No retention load path |

## Delivery

Delivered candidate investigation; branch `engine/finish-component-interfaces`, no worker commit. Geometry unchanged pending evidence. Parametric API `oil_cap.parts(Parameters())` and `oil_cap.build((define, add), Parameters())`. Existing export and visual artifacts remain in candidate directory. Machine-readable reports and final scope follow below.

### Reproduction

Run from repository root with the CAD lock environment and restored baseline STEP files:

```sh
XDG_CACHE_HOME=/private/tmp/truck-cache .venv-cad/bin/python scripts/pilot/oil-cap/build_check.py > inventory/engine/pilot/oil-cap/build-check.log 2>&1
XDG_CACHE_HOME=/private/tmp/truck-cache .venv-cad/bin/python scripts/pilot/oil-cap/check_motion.py > inventory/engine/pilot/oil-cap/motion-check.log 2>&1
.venv-cad/bin/python -m py_compile scripts/pilot/oil-cap/build_check.py scripts/pilot/oil-cap/check_motion.py
```

The cache directory is disposable, not a required artifact. `build_check.py` now uses the repository root as baseline, eliminating the old private temporary checkout dependency. Run it before the motion checker to regenerate the candidate STEP inputs, which are excluded from Git by artifact policy. The source and committed GLBs remain sufficient for rebuilding the candidate. Shared STEP restoration is documented in `docs/CAD-ARTIFACTS.md`; motion report hashes identify the exact current baseline assets. `motion-validation.json` records Python/build123d/platform and all local motion input hashes. Model/effort and token billing figures unavailable to worker.

### Retention decision and exact neighbor request

Primary-source review on 2026-09-26 again found male screw retention and replacement dimensions, but no applicable thread pitch/profile, usable engagement or production neck drawing. See `inventory/engine/pilot/oil-cap/retention-review.json`, [Ford EC743](https://www.ford.com/product/engine-oil-filler-cap-p4000083484) and [MotoRad MO100](https://motorad.com/part/MO100/). No new geometry is justified by that evidence.

Preserve the cap/neck axis `(240,-12)` and provisional sealing datum Z413. The required future shared change is to `valve-cover`: replace its smooth 34 mm bore with a measured female screw neck and sealing land, then reconcile the cap's male profile and gasket to the same pair of measurements. Do **not** transfer the assumed 4.5 mm pitch / 28.84 mm thread root into the cover as factory dimensions. Required measurements: cap/cover identity, thread diameter/lead/starts/profile, axial endpoints and engaged length with compressed seal, neck height/wall thickness and seal seat dimensions. A threaded appearance is not an engagement proof. Cover changes invalidate static cap contact/neighbor and dynamic rocker results and require whole-assembly checks.

To install a subsequently approved cap revision, the integration owner removes the original `oil-filler-cap` define/add pair and invokes `oil_cap.build((define, add))` in the closures scope after constructing the measured cover. Keep IDs `oil-filler-cap` and `oil-filler-cap-seal`; merge candidate evidence and learning content through the standard loader. This candidate is **not currently integration-ready**.

## Validation and review

| Gate | Verdict | Evidence / limits |
|---|---|---|
| Application/coverage | PASS within replacement candidate scope | Existing Ford exact application evidence; actual truck cap identity unknown |
| Dimensions/coordinates | PASS for explicit classes/datums | Replacement vs estimated dimensions remain labeled; no factory metrology claim |
| CAD/export | PASS | Regenerated `validation.json`; one valid solid each, STEP round trip and watertight local mesh |
| Source/visual comparison | Provisional, factory fidelity open | Existing `review.png` and `visual-review.json`; geometry unchanged, grips/markings still approximate |
| Installed interfaces | FAIL | Smooth bore provides zero female retention; 1.38 mm radial thread gap. Contact is not compression/seal-pressure validation |
| Motion/disassembly | PASS sampled rocker clearance; service removal NOT RUN | `motion-validation.json`; screw removal/engagement and other moving hardware remain unvalidated |
| Learning/diagnostics | Existing limited candidate content preserved | `learning.json` expressly identifies retention and seal uncertainty; no repair specifications invented |
| Browser integration | NOT RUN | Candidate remains separate; integration owner must review accepted installation |
| Reproduction/review | Local reproduction PASS; independent review pending | Repository-relative baseline, logs/reports/hashes; no worker commit or installation claim |

- Reviewer: coordinating integration agent pending. Code may be preserved as candidate; installed acceptance remains blocked by production retention and seal evidence; final restored-baseline motion status is recorded below.
- Source comparison: existing actual top/underside/cover views; sharper shoulders, approximated grip and missing markings remain unchanged.
- Shared geometry changed: none. A regenerated candidate does not invalidate unrelated assembly checks.
- Tracking: #15 stays open. Next action is integration-owner review of dynamic report and acquisition of cap/neck dimensions before shared cover editing. No ongoing background work after handoff.

### Baseline-restoration flaw discovered and corrected

The first portable rerun found 77.893 mm³ cap/rocker overlap at crank 0°, contrary to the historical 1.3754 mm gap. The manifest hash matched, but root STEP geometry did not match the authoritative desktop checkpoint. The coordinating integration owner restored all affected baseline STEP files; see `inventory/engine/cad-baseline-restoration.json`. This worker did not alter neighbor geometry. The superseded result is summarized in `stale-baseline-motion-diagnostic.json` solely as a provenance diagnostic, not acceptance evidence.

Before restoration the rocker hash was `73932891d47a486110ce8c63efd8b118a0481db7ef4f81db860f7427b717263d`; the restored authoritative value is `62ad3a2e8d018d99c864ae65f1eccc6a9c8b5c9d4ffdf4f5a055801827803c8f`. The cover similarly changed from stale `99c0f4af1d9f57c0c7baeeeaa6367adde721b382e2f2d36d0651557a8bca8398` to authoritative `17284e8d2aca7aae12d32fe4639c1b0bdfab26717b13af72f8f97d2716760df2`. Manifest identity alone is insufficient for evidence reuse. Static and motion checks were rerun after restoration and their final hashes supersede the diagnostic. The motion checker now rejects any input hash changing during its execution.

### Final restored-baseline motion result

**PASS sampled rocker clearance:** 181 crank phases from 0 through 720°, all twelve rockers, 362 exact nearby pairs and 1,810 AABB-separated pairs. Minimum gap **1.3754 mm** occurs at c1 intake/rest; no ordinary overlap exceeded the 0.1 mm³ audit threshold. The cap lowered 10 mm produces **352.671 mm³** overlap and correctly fails the same collision path. `motion-validation.json` contains all exact samples, environment and input hashes; `motion-check.log` records completion. This is not continuous coverage, production tolerance validation, or a measured factory cam law. Both endpoints, each valve's peak and support boundaries are explicitly sampled. Full versus focused shared-API transforms also matched at 0/246/468/720°.

The paired retention gate still **FAILS**. Neither this pass nor a valid export closes issue #15. Browser integration and screw removal remain NOT RUN because this is not an installable retained pair.

For subsequent unrelated manifest edits, `motion-input-scope.json` captures all rocker occurrences, ordered ancestor assemblies, definitions, mechanism and active valve-motion model set. The lightweight verifier checks that scope, the motion report hash and every non-manifest source/STEP input hash. It rejects a deliberately shifted rocker as a sensitivity check. It does not check newly added hardware, so the integration owner must separately audit cap clearance against such additions.

```sh
# Immediately after a fresh successful full motion run, before any inputs change:
python3 scripts/pilot/oil-cap/verify_motion_scope.py --capture > inventory/engine/pilot/oil-cap/motion-scope-validation.json
# After unrelated assembly additions, without replacing the captured scope:
python3 scripts/pilot/oil-cap/verify_motion_scope.py > inventory/engine/pilot/oil-cap/motion-scope-validation.json
```

The original capture and unchanged-scope verification both passed. If any relevant input changes, rerun the full motion checker and capture anew. The final worker checks were component build/export, dynamic BREP sweep with negative control, scope verifier with negative control, Python compilation, and whitespace review. No process remains running.

Actual CAD environment: python=3.13.12, platform=macOS-15.6.1-arm64-arm-64bit-Mach-O, build123d=0.10.0.
