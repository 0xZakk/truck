# Component contract and handoff: timing rotating clearance candidate

## Contract

- Issue #32; engine timing dependencies. Worker owns this isolated study; root owns integration.
- Assigned baseline 28ba18f; actual checkout at construction 3079300, branch engine/timing-coupled-fit. Canonical manifest remains 91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6.
- Candidate motion audit only: migrated camshaft including actual lobes versus actual crankshaft and all six piston/rod group occurrences, including caps, bearings and fasteners. No new geometry, phase calibration, installation, block/cover or valve-linkage acceptance.
- Owned new files: cad/engine/timing_rotating_clearance_candidate.py, scripts/check-timing-rotating-clearance-candidate.py, inventory/engine/timing-rotating-clearance-candidate-validation.json, this handoff; ignored generated/timing-rotating-clearance-candidate directory.
- Millimeters, world X shaft axes. Cam axis YZ=(95.1098209901611,76.08785679212888), estimated 121.8 mm spacing. Complete keyed group uses frozen coupled-core frame: cam angle=-crank/2+k*axial, k=-tan(25 degrees)/81.2 rad/mm; axial [-0.1,0]. No gear slipping or new lobe phase.
- Crank/rod/piston transforms come from assembly_math.transforms and current manifest. Stroke101.092 mm; rod length157.7 mm explicitly unverified; idealized zero-offset slider crank. Existing lobe shape/timing is a replacement-based hypothesis, not confirmed installed cam identity.
- Inputs: canonical STEP definitions, manifest, shared motion helper, frozen coupled-core camshaft STEP/module/report. Bind bytes before and after checking.
- Acceptance: conservative support containment and positive separation where possible; otherwise deterministic phases with explicitly bounded coverage, exact overlap tolerance0.1 mm3. A failed conservative bound is not a physical collision. Negative controls must detect changed axis/phase or actual interference. Preserve failures and report any geometry task.

## Evidence ledger

| Claim | Evidence class | Source / limit |
|---|---|---|
| Timing relationship must be retained to avoid possible crank/cam lobe interference | Applicable service caution | Retained exact1994 Timing Gear procedure; identified in backlash/coupled-core handoffs |
| Actual motion law and cylinder phases | Model contract | assembly_math.py and full-assembly.json; not measured production motion |
| New cam spacing, helix, axial compensation | Estimated candidate | Frozen coupled-core report; preserved as supplied |
| Rod forging, counterweight shape, piston skirt | Estimated | Current definition unresolved fields remain applicable |

## Delivery / validation

In progress. No installed or continuous-clearance claim yet. No new shape export required: study consumes existing exact STEP bytes. Browser, source-shape revalidation and learning edits N/A to this isolated clearance audit; prior source comparisons remain historical, not new verification.

## Tracking and restart

Run `.venv-cad/bin/python scripts/check-timing-rotating-clearance-candidate.py` after checker construction. No shared or canonical changes. Usage unavailable.

## Completed delivery

- Readiness: **candidate, not installed**. No geometry modified or new shape exported. Ninety-one actual occurrences covered: crankshaft, 42 piston-group parts and 48 rod-group parts. Piston scope includes skirts, rings, expander and wrist pins; rod scope includes caps, bearing shells, bolts and nuts.
- Entry points: `inputs()` returns restricted manifest, actual definition STEP shapes and frozen world camshaft; `posed(manifest, shapes, cam, theta=0, axial=0)` uses the shared motion helper and frozen coupled-core frame.
- Run from repository root: `XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-timing-rotating-clearance-candidate.py`.
- Report: `inventory/engine/timing-rotating-clearance-candidate-validation.json`, SHA-256 **665e30f5300347f05c8db7cd2fe0f68fcbecd3c3924be31fa9d80a93bf4ea33b**. Input bytes are bound before/after the run. Log: `cad/engine/generated/timing-rotating-clearance-candidate/check.log`.
- Environment: macOS, Python3.13, build123d0.10.0 / OCP7.8.1.1.post1. Model/effort and usage unavailable. Issue CLI read attempted but GitHub API connection failed; assignment and existing repository issue32 context supplied by integration owner were used.

### Continuous coverage and mathematical contract

The entire supplied camshaft, including all lobes, is contained by exact CAD difference in a coaxial radius25.622251 mm cylinder. The complete crankshaft is contained in radius87.546001 mm about the crank axis. Their 121.8 mm spacing therefore proves **8.631748 mm** radial separation at every angle, independently of phase. Piston-group motion translates only along Z; the nearest full group Y envelope remains at least **18.687925 mm** from the cam support at every piston height. Ancestor transforms and motion roles are explicitly checked.

A full-length maximum-radius cam cylinder intersects the swept rod region, but that is an inconclusive support, not an actual collision. At each of the 48 rod-part X intervals, the actual cam material is contained in radius15.001 mm. Each baseline interval extends through the full axial motion: `[neighbor xmin, neighbor xmax + 0.1]`, with a numerical clipping margin. This support remains valid for every cam angle and every axial displacement in [-0.1,0]. The exact cut reports zero material outside each support.

For each of eight distinct rod roles, actual CAD-to-support distances were measured at 72 crank phases, every5 degrees. The minimum sampled distance is reduced by a rigorous displacement allowance for the nearest sample, at most2.5 degrees away. For a local point of radial norm at most rho, the slider-crank rigid-body speed is bounded by `R + R/sqrt(L²-R²) * rho` millimeters per crank radian. Here R=50.546, L=157.7; rho comes from the complete local CAD bounds including occurrence offset. Set distance is1-Lipschitz under that displacement. Thus the result is a continuous certificate, not a claim that sparse samples alone exclude intervening collisions. All six cylinders reuse each role only after verifying identical geometry/local offsets, pure X station differences and phase-shifted copies of the same rod law.

The smallest certified gap is **4.657228 mm**, for the connecting rod. Its nearest sampled pose is305 degrees, distance9.533706 mm before the between-sample allowance. Positive-side rod bolt minimum certified gap is6.059579 mm. Caps, nuts and bearings also pass. The complete720-degree engine cycle is covered because all crank angles and all cam angles are covered independently. The certificate does not require inventing a new lobe phase or moving a gear independently of its keyed group.

The supplied cam geometry retains the existing `valve_layout_candidate.cam_adapter` phases `(468+firing_deg)/2` and `(246+firing_deg)/2`, with firing-order stations from `valve_layout_integration`; those remain hypothetical replacement-based timing, not owner calibration. The posed API preserves the inherited opposite half-speed rotation and axial helical compensation. Four-part keyed-group attachment remains the separately frozen coupled-core proof; this audit does not re-establish valve-linkage or distributor/pump coupling.

### Sensitivity and preserved failures

- Six actual rod small ends coincide with their piston pin origins within1e-7 mm at0,90,180,270,360,540 and720 degrees.
- Wrong rod-tilt sign produces **101.092 mm** closure error.
- Moving the actual camshaft60 mm toward the crank along Y produces **26,447.369657 mm³** exact crankshaft overlap. Both the radial support certificate and actual collision test reject this fault.
- Initial broad support results and a diagnostic role-filter exception remain in ignored probe logs and `rejected-role-filter.log`. The exception included the single crank ID in a cylinder-prefix lookup; the corrected filter is restricted to rod-group occurrences. No geometry or acceptance tolerance was changed.

### Quality gates

| Gate | Result | Evidence / limit |
|---|---|---|
| Application and coverage | PASS scoped model audit | All91 named occurrences listed; production identity remains uncertain |
| Dimensions and coordinates | PASS | Input hashes, actual helper, group/ancestor assertions and pin closure |
| CAD/export integrity | N/A new export | No new CAD or GLB; exact existing STEP bytes bound, CAD support differences checked |
| Visual/source fidelity | N/A new shape | Frozen prior comparisons remain historical; no new production-fidelity claim |
| Interfaces | PASS scoped clearance | Cam versus crank and complete piston/rod groups only |
| Motion | PASS continuous support certificate | Explicit radial/Y containment and Lipschitz interval bounds; no loaded dynamics |
| Learning/diagnostics | N/A isolated audit | Existing exact-year timing caution motivates retention of phase, no repair specification added |
| Browser | NOT RUN | No installation or viewer edits |
| Reproduction/review | Worker checks PASS; root review pending | Checker, input bindings and proof rationale preserved |

No measured production clearances are inferred from these margins. Counterweight contours, rod forging, rod length, piston skirts, lobe timing and new cam spacing remain estimated. Block/tunnel, cover, valve linkage, distributor and pump still require their separate checks. No rotating-clearance geometry correction was needed for the supplied inputs. Next action: root review this certificate and retain its hashes while advancing the other timing interfaces. Process finished; no background task remains.
