# Component contract and handoff: throttle mechanical stop proposal

## Contract

Issue #43 under engine #1. Integration lead owns installed geometry and shared assembly/viewer files. Worker owns this proposal, `reference/engine/throttle-stop-review.json`, `cad/engine/throttle_stop_candidate.py`, `scripts/check-throttle-stop-candidate.py` and `inventory/engine/throttle-stop-candidate-validation.json`. Isolated feasibility CAD is now present; no canonical edits and the frozen cable package is untouched. The ledger records baseline commit, actual manifest hash, 733 definitions / 1,341 occurrences and hashes of the inspected local STEP parts.

Scope: identify evidence-supported idle and wide-open mechanical stop topology, inventory actual existing geometry and propose a bounded next candidate. Exclude factory calibration, repair adjustment instructions, idle-air simulation, production screw dimensions/torque and unverified automatic/cruise mechanisms. Stop existence does not establish production travel angle.

Inherited millimeter frame: throttle shaft parent-local origin `(394,25,490)`, axis Y; lever lies approximately Y89–91. The positive-Y ball remains `(394,95,514)` at neutral. Existing ancestor −167X is separate. Stationary boss/screw/lug would inherit `throttle-assembly`; moving contact lands remain part of `throttle-lever-estimated` under `throttle-moving`. Keep all current ball/cable, key/pin, spring-anchor, shield and bracket datums fixed.

## Evidence ledger

| Feature | Evidence and actual observation | Limits |
|---|---|---|
| Idle screw-to-pad contact | Exact-year archive Idle Speed/Adjustments explicitly requires the plate-stop screw to touch a lever pad. Figure186295596 labels the external plate-stop screw beside the twin-bore body. | Shared multi-application procedure; no dimensions, axis or production stop angle. This is not an internal plate-retaining screw. |
| Cable-side location | Factory689805816 labels the external set screw on the lever side, opposite TPS. Directly reviewed again with690090240. | No distinct WOT contact is labeled in these views. |
| WOT stop existence | Applicable Throttle Body/Description and Operation names a preset WOT stop. | Does not establish a separate WOT screw, lug contour, number of stop parts or numeric travel angle. |
| Replacement comparison | Prior ledger recorded a screw on a casting pad beside the lever in an F2TE-FA comparison image. | Application was unverified; attempted image/listing refetch returned cache misses in this task. No new specimen observation is claimed. |
| Rejected archive result | M/T TPS adjustment page discusses a diesel fuel-injection-pump lever/FIPL system. | Its0.515-inch gauge and maximum-travel screw are inapplicable to the gasoline4.9 throttle body despite appearing under the selected archive tree. |

Primary manual pages: [throttle description](https://charm.li/Ford/1994/F%20150%202WD%20Pickup%20L6-300%204.9L/Repair%20and%20Diagnosis/Powertrain%20Management/Fuel%20Delivery%20and%20Air%20Induction/Throttle%20Body/Description%20and%20Operation/) and [idle-speed procedure](https://charm.li/Ford/1994/F%20150%202WD%20Pickup%20L6-300%204.9L/Repair%20and%20Diagnosis/Powertrain%20Management/Fuel%20Delivery%20and%20Air%20Induction/Idle%20Speed/Adjustments/). Local HTML/image paths, hashes, observations and exclusions are in the ledger. Restricted originals are not redistributed.

## Existing geometry inventory

No stop-specific definition or occurrence is present. The housing has no modeled idle screw receiver or dedicated WOT lug. The lever is the earlier inferred flat arm/hub with a spring anchor, without a source-shaped stop pad. The slider's0/90 endpoints are software commands.

Read-only exact CAD probes used the actual installed STEP lever against actual housing, cable bracket and shield at −2,0,2,88,90,92 degrees. All intersecting volumes were zero. Lever-to-housing minimum distance stayed2mm at every probe. At0 the bracket/shield distances were10/7mm; at90 they were12/18.439089mm. Thus these existing stationary surfaces do not provide either endpoint stop. The diagnostic overtravel does not authorize the cable or springs to operate beyond the checked0–90 range.

To reproduce against the current assembly using `.venv-cad/bin/python`, load the manifest and the four STEP paths named in `current_geometry`, compute `assembly_math.transforms(manifest, throttle_degrees=angle)` for each listed angle, move each local shape by its occurrence transform and evaluate `distance_to` plus `cad_metrics.solid_volume` with the adaptive method on every solid of the intersection. Compare the current input hashes before attributing these historical numbers to a later revision.

## Minimal candidate proposal

1. **Idle:** one separate retained plate-stop screw in a boss joined continuously to the housing; its tip contacts a pad integrated with the moving lever. Screw/pad contact is directly supported. Boss contour, screw axis/thread/size, locking construction and chosen neutral contact position must be explicit estimates. A tangential approach on the cable side is a model-space feasibility hypothesis, not a dimension taken from the drawing.
2. **WOT:** a minimal stationary casting lug meeting a separate lever land. Only stop existence is verified; an integral lug is the proposed educational construction. Do not add a second adjustment screw or call90 degrees a Ford calibration without further evidence.
3. Preserve the current0–90 demonstration and all cable/spring anchors. Model endpoint contacts at those existing educational positions rather than changing the motion table to conceal interference. Actual closed-plate airflow, plate bevel/orifices and factory stop settings remain unresolved.

The next step can proceed as a bounded illustrative candidate: first attach the proposed idle boss to actual housing material and locate contact lands away from the keyed hub, spring hooks, ball stem/socket and shield. Check cheap neutral/mid/open geometry before committing to screw retention or a full sweep. A screw floating beside the lever is not acceptable.

## Proposed validation

- At0: positive-area screw-tip/lever-pad contact; positive clearance once opening begins. A small negative-angle probe must interfere specifically with the intended idle stop.
- At90: positive-area WOT contact; clearance below90. A small positive overtravel probe must interfere specifically with that stop.
- Physical screw retention and boss-to-housing continuity. Negative controls detach the screw/boss and shift the pad; they must fail contact/capture.
- Full0–90 neighbor sweep with the actual cable/socket/guide/compression spring, shaft torsion spring, bracket, shield, studs and body. No generic collision exclusions.
- Exact unchanged-region tests preserve bores, plates, shaft support, D-key/pin and all fixed/moving cable and spring datums. Candidate geometry stays isolated until root review.

## Delivery and quality gates

| Gate | Result |
|---|---|
| Application/evidence | Idle screw/pad topology and WOT existence supported; construction/dimensions explicitly unresolved |
| Existing coordinate/interface inventory | PASS, read-only actual STEP probes bound by ledger hashes |
| Candidate CAD/export/contact/negative controls | PASS for cheap 0/45/90 feasibility; thread capture/advance and full sweep NOT RUN |
| Source-versus-candidate render | Created and directly inspected locally; integration lead review pending |
| Motion/learning/browser integration | NOT RUN; current accepted cable package untouched |
| Reproduction | Source paths/hashes, actual part hashes, angles, methods and results preserved in ledger |

No new commit, PR or asset release. Environment for CAD probes: macOS, Python3.13.12, build123d0.10.0 and existing `assembly_math`/`cad_metrics`. Model/effort/usage unavailable. No process remains running. Issue #43 stays open. Next action is integration lead visual review, then strict thread-retention controls and a full neighbor sweep before any installation proposal.

## Isolated feasibility checkpoint

Current candidate adds a casting-connected idle boss and WOT lug to a copy of the housing, contact lands to a copy of the lever, and one separate helical idle screw. All dimensions are estimates. The screw axis is parent +X at Y90/Z502, with tip X389; its estimated major diameter is2.9mm and pitch0.5mm. The WOT land ends at Y93.25 to preserve the existing shaft-spring lead. The lug contact plane is Z487. These dimensions fit the existing educational mechanism; the factory images do not establish them.

The report binds the actual733/1341 manifest and relevant STEP/module hashes. At0/45/90,54 exact pairs found no collision failures. Idle screw/pad contact at0 is3.694166mm²; WOT contact at90 is7mm². Both contacts are absent at45. Diagnostic−1° produces0.767432mm³ idle-stop overlap;91° produces1.447032mm³ WOT overlap. These diagnostics do not authorize cable/spring overtravel. Detaching the screw by10mm removes contact. Both new casting features overlap original housing material; original housing/lever removed volume, protected key/hook/ball changes and new material in the flow bores are zero. All three exported parts are valid one-solid STEP shapes with watertight GLBs.

Nominal screw/body clearance passes. An independent physical retention probe also passes using a radius0.03mm sphere exactly contained within both the housing and each screw shifted±0.125mm without rotation. This proves an overlap lower bound0.000113097mm³, above the unchanged0.0001mm³ capture threshold. The matching+90°/+0.125mm threaded advance has no intersection solids. This proof avoids the numerically ill-conditioned total volume of a thin trimmed helix; a preliminary total-volume calculation exceeded the unchanged1e−7 integration accuracy requirement and was not accepted. These controls are now encoded in the checker; the full47-pose sweep passes. No locking, strength, torque or production adjustment claim is made.

Reproduce from repository root:

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-throttle-stop-candidate.py
MPLCONFIGDIR=/tmp/truck-cable-mpl python3 scripts/check-throttle-stop-candidate.py --render
```

`--thread-retention` requests capture/advance controls; `--full` additionally expands the neighbor sweep. Those are next-stage gates, not current passes. The checker preserves original material and tests only added housing/lever material against external neighbors, plus complete candidate mutual pairs; it evaluates the actual deforming cable and shaft spring at each sampled angle.

Pure CAD visual: `cad/engine/generated/throttle-stop-candidate/candidate-endpoints.png`. Local restricted source comparison: `candidate-source-comparison.png` in the same directory, placing directly reviewed factory186295596/689805816 above the CAD endpoints. **Exclude that composite and manual originals from Git and shared artifacts.** The comparison confirms only external screw/pad topology; simple block contours and the WOT lug do not reproduce an observed production contour. STEP/GLB hashes and all input hashes are in the report; its checkpoint hash is in the source ledger. No assembly adapter, viewer integration or browser acceptance is delivered at this stage.

The integration lead reviewed the source comparison and requested modest casting edge relief. The revised idle boss/root have estimated0.65/0.4mm radii; the WOT base/upright have0.25mm radii. Contact planes and protected interfaces remain fixed. The rounded candidate repeated the cheap feasibility pass and was re-rendered and directly viewed before the full47-pose sweep began.

## Delivery

- Contributor: component worker; integration owner/reviewer: root engine lead. Issue43 under engine1 remains open. Baseline commit is `74ca5288bb543871b1cc550e191e3f54ed62a8f1`; no commit/PR or asset release is created by this worker.
- Entry point: `throttle_stop_candidate.parts(housing, lever)` accepts the current local STEP shapes and returns `(parts, features)`. Housing and screw use throttle-parent coordinates; lever uses the unchanged throttle-moving local coordinates. Parameters are exposed as `PARAMS`; no Ford service number is claimed for the illustrative screw.
- Future integration would replace the existing `throttle-housing` and `throttle-lever-estimated` definition shapes while preserving their IDs/poses, then add one stationary screw definition/occurrence under `throttle-assembly` with identity local transform. Expected count delta is+1 definition/+1 occurrence. This is a handoff plan only: no adapter or shared changes are included, and installed acceptance requires a fresh staged gate.
- Generated STEP/GLBs are under `cad/engine/generated/throttle-stop-candidate/`, with hashes in the validation report. Pure CAD endpoint render is distributable under normal artifact policy; source comparison is local-only. Learning content/browser checks: NOT RUN, deferred to integration. Force, thread locking, idle control simulation and production calibration: outside this candidate's scope.
- No changes are needed to the current cable tables, shaft-spring paths or protected bracket/shield/ball interfaces. Current all-occurrence broadphase and explicit dynamic cable/spring evaluation are required if any neighbor changes before installation.
- Environment: macOS, CAD Python3.13.12/build123d0.10.0/trimesh4.7.4; rendering system Python with matplotlib3.10.9. Usage/model-effort data unavailable. Restricted local manual originals are an evidence dependency, not an export dependency.

## Tracking and restart

Completed run: full47-pose candidate check PASS, log `cad/engine/generated/throttle-stop-full.log`. No candidate process remains running. Restart with `XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-throttle-stop-candidate.py --full`; this builds/exports/checks isolated outputs and writes only the owned candidate report. Root must review the staged evidence before any installation. The source-supported limits remain distinct from the geometric pass.


## Final isolated candidate result

The rounded candidate passes47 sampled poses (every2° plus45°),843 exact collision pairs, with all1,341 current occurrences considered in broadphase and no collision failures. Idle contact is3.694166mm²; rounded WOT contact is6.946350mm². Protected-region differences remain zero. Both axial capture witnesses and the matched quarter-turn clearance pass. All three STEP/GLB exports remain valid and watertight. The validation report supersedes the initial cheap checkpoint, while the numerical-integration limitation and witness method remain documented.

The integration lead directly reviewed the rounded endpoint render and accepted its explicitly illustrative topology for packaging. This is candidate acceptance only. Full-sweep input hashes and export hashes are frozen in the report; the source ledger records its SHA256. Next action is a scoped adapter/staged checker against the then-current assembly, followed by integration/browser review. No factory90° calibration, screw standard, locking method or production WOT-lug construction is established.
