# Desktop engine continuation

Updated: 2026-09-25T16:32:48.350034-05:00

The engine is unfinished. The live manifest is90807873 (688definitions,1244occurrences).
Current static, sampled core-motion, rear entry, front profile, lifting-eye, dowel
and exploded joint checks all match that manifest; the report index is
`inventory/engine/desktop-continuation-qc.json`. Crank/lubrication motion checks
do not establish valve motion or continuous collision freedom.

## Integration ownership

The earlier CLI task still has an active writer and independently authored a rear
mounting checker while this task authored a similarly named candidate. Both
threads detected the collision. The user was asked to stop the earlier task.
This task now builds accepted candidates in an isolated copy at
`/private/tmp/truck-desktop-integration-20260925`; it has independent CAD, meshes,
inventory, scripts and viewer files. Its reference/manual/KB symlinks are used
read-only. Do not copy its outputs back over newer live work without reconciling
the live baseline hash and ownership.

The existing persistent goal is still usageLimited. Creating another was rejected;
user-side /goal resume is needed for automatic continuation. No goal completion
is claimed.

## Active work

- Root: revised rear mounting candidate passes336neighbor and54passage checks.
  Six STEP roundtrips and positive seat/socket material checks pass. The first
  version blocked two runners and was rejected; the new module is
  `cad/engine/rear_manifold_mounts_desktop_candidate.py`. Render viewed. Separate
  source-supported topology from provisional1996comparison dimensions/stations.
  Isolated builder has a --refresh-rear-mounts path; installed audits pending.
- Valve agent: separate timing study passes17292kinematic samples and73isolated
  cam/follower contacts. The first two-station static correction passes154local
  intersections. Actual station motion/clearance tests continue. Candidate files
  live under `cad/engine/candidates/valve-station`; main viewer motion unchanged.
- Belt agent: tensioner alone cannot reconcile the length discrepancy. Several
  numerical routes were rejected for collisions or Forddiagram-order conflict.
  Source-ordered accessory layout is being refined with explicit support redesign
  and dimension uncertainty. No belt is newly published.
- Pan agent: initial13/12side-rail pattern rejected by exact OS34601R image;
  observed topology is10+10longrail and3+2endholes. The original audit was
  interrupted after seating controls; no complete neighbor pass. Revised matched
  pan, gasket, end lands and25fastener assemblies are in development.

## Browser review

Refreshed the user viewer from a stale679-part model to1244parts. Verified rear
part navigation and rendered mesh. Separate `/viewer/valvetrain-study.html` was
reviewed at468degrees intake peak and with play/pause/cylinder selection. It is
an explicitly hypothetical replacement-catalog teaching study, not installed
Ford cam geometry.

## Later checkpoint

Rear mounting increment accepted in isolatedmanifest4854f352:690definitions/1246parts.
Installed336neighbors/54passages, whole-static4558checks, sampled explodedposes,
navigation1246parts/1441links and162sourcehashes pass. Browserassembled/exploded
exhaust reviewed. Integrationpatch and per-file hashes are in
`docs/candidate-patches/rear-mounts-desktop.patch` and its provenanceJSON.
Six changed STEPshapes and accepted reports saved under
`cad/engine/candidates/rear-mounts-desktop/accepted/`.

Outlet flange candidate in `exhaust_outlet_flanges_desktop.py` passes47neighbor
checks, two STEProundtrips, four hole/bearing-band checks and two outlet probes
on4854f352. Render reviewed. New isolated --refresh-exhaust-outlets build38239
is running in /private/tmp/truck-desktop-outlets-build.log; no installed passyet.

Valve agent's coherent two-station layout passes154staticchecks and228peak-pose
checks/30contacts. Full18pose check and smoother cam representation pending.
Pan newer jointV5 still fails timingcover/starterneighbors; continuous inset
upperneck revision underway. Belt agent recoveredFordTSB94-10-19 Fig4 exact1994
sharedcarrier architecture; newcarrier's firstneighborsweep fails25pairs and
needs revision. These are all unpublished candidates, not completed systems.

## Carrier and pan checkpoint

Isolated carrier manifest951d4189:696definitions/1252parts. Installed195exact
intersections,17saved-shape comparisons,8tensioner poses and joint controls pass.
Whole-static4634checks,0overlaps>0.1mm³; navigation1252/1448links and163source
hashes pass. Browser group/attachments reviewed; stale cached lessons had broken
a removed-part link, corrected with no-store JSON and manifest-hashed mesh URLs.
Carrier accepted artifacts/reports saved in cad/engine/candidates/carrier-1994-desktop/accepted.

Outlet installed41a87e03:47neighbor checks,4mounting-hole bands,2openoutlets,
2STEP matches pass. Both integral flange shapes saved with accepted report.

Pan V8 re-audit against carrier951d4189 passes687exact checks,5STEProundtrips,
25seat/bore/floor controls. Baseline frozen at /private/tmp/truck-desktop-pan-baseline-951d4189.
Pan build37853 running at /private/tmp/truck-pan-joint-build.log. Installed and
full-engine checks still required. Working integration patch/provenance saved as
docs/candidate-patches/desktop-integration-working.*; do not apply blindly.

## Valve train and cooling checkpoint

Pan V8 installed static comparison and whole-engine4828checks passed on922ac5c8,
697definitions/1301occurrences. Its exploded trajectories failed; V9 corrects the
shallow pan end walls and stages axial hardware extraction before lateral display
separation. V9 passes candidate checks but is not yet installed. Do not conflate
V8 static acceptance with motion acceptance.

The alternator source-order correction passed29STEP roundtrips,93neighbor checks,
three saved-definition comparisons and26absolute poses; accepted artifacts are in
cad/engine/candidates/alternator-carrier-desktop/accepted. Belt length/routing still
fails and has not been accepted.

First-stage coordinated all12valve geometry built isolated4b847d7b (697/1301).
Whole-engine4850checks found3clashes: gasket/c2exhaustpushrod, rearcamjournal and
bearing/c6intakefollower. A separate rear_cam_clearance_desktop candidate preserves
journal radial dimensions and assumed widths, shifting journal/bearing together
4mmrearward; gasket gains revised-axis openings. Its30neighbor and588pushrod
passage checks pass. Integrated rebuild74459 is running in
/private/tmp/truck-valve-clearance-build.log. Full static acceptance is pending.
All firststage absolute heights are provisional; its234.2mm pushrod contradicts
the257.556mm catalog part. The valve agent is developing a replacement with sourced
valve, pushrod and lifter-body lengths as hard constraints.

Browser now shows each complete cylinder as40parts with valves and both actuation
chains in one navigation group. Verified246degree scrub and playback/pause in the
isolated preview on8081. Explicit module revisions resolve stale navigation cache.
The main8080 viewer is unchanged. Learning text discloses the dimensional conflicts.

Pump agent's56changed-part candidate passes neighbors/local interfaces and8STEP
roundtrips, pending visual and root integration. Outlet agent's20part candidate
includes heater-supply elbow and ECT; first extension failed sleeve/taper interference
and is being corrected. Neither cooling candidate is installed. Goal remains
usageLimited; earlier CLI integration ownership remains unresolved.

## Recovery inspection — 2026-09-26

All three subagents stopped with backend authentication errors (HTTP401), not CAD
validation failures. Their files and reports survived. The source-sized two-station
valve motion sweep finished despite the interruption:1407intersections,288contact
checks, no failures; ten other stations still require integration/animation.

The last launched panV9 build completed: isolated manifest0dec59b992b57c09ae14545eed8aba6e5e7cda70810fc6de9ba810c7f24034be,
697definitions/1301occurrences. InstalledV9comparison and whole-static on this hash
have NOT run. Prior6b11c0f8 remains last whole-static accepted checkpoint (4849checks).
V9 candidate static685checks and sampled motion/explosion passed before build.
Frozen comparison baseline is /private/tmp/truck-desktop-pan-v9-baseline-6b11c0f8.

Pump candidate re-audit on6b11 passed157checks for56changedsolids. Outlet expanded
candidate passed265checks/20STEProundtrips on6b11. Both remain uninstalled. Next:
run installedpanV9comparison against frozenbaseline, then integrate cooling changes
with composable block/head adapters and new whole-engine checks. Continue source-sized
all12valve integration and conditional belt reconciliation with the three existing
agents once their authentication succeeds. Mainmanifest remains90807873/1244parts;
new1301partpreview is isolated. Existing goal still reports usageLimited; do not
create another goal or declare completion. User says app already treats goal asactive.

## Resumed integration — 2026-09-26

Three existing agents resumed successfully. Authoritative wait_threads snapshot
shows earlier task01a0d91a-d6cc-7e02-b515-f0fe10ae1321 is notLoaded, its latestturn
completed and finalmessage explicitly stopped for conflicting-edit ownership.
This task continues isolated integration under the user's instruction; no active
competing writer is reported.

PanV9 installedcomparison passed all5definitions (zero symmetricdifference),50
hardwareposes andstagecontracts on0dec59b9. Saved acceptedpan artifacts in
cad/engine/candidates/pan-joint-v9-desktop/accepted. Whole-static atthisrevision
notrun; latest whole-static remains6b11. Pumpcandidate re-audit on0dec59b9 passed,
alongwith fullgasket/socket/cylinderretentioncontrols. Frozenpre-pumpbaseline:
/private/tmp/truck-desktop-pump-baseline-0dec59b9. Pumpintegration build74595 running
in /private/tmp/truck-pump-joint-build.log; newidempotentadapter is
cad/engine/water_pump_joint_integration_desktop.py. No installedpumpPASS yet.

## Combined cooling checkpoint — 2026-09-26

Pump b2495a95 installedcomparison passed8definitions and affected rigidposes;
actual-installed fullrotationimpeller envelope passed. Accepted8STEPs/manifest/
reports saved cad/engine/candidates/pump-joint-desktop/accepted. Adapter initially
referenced nonexistent support.SOURCES/GAPS; corrected to pump sources plus explicit
support uncertainty before successful build51497. Absolute impeller rear datumX-71
prevents repeated59mm translation onrefresh.

Outlet build50264 finished: c2ea58608b4f6e24a72c0d7b3c862202230fde7cce9dc5292774cb7635359fb1,
698definitions/1305occurrences. Navigation1502links and168source captures pass.
Installed20partoutlet audit62746 running /private/tmp/truck-outlet-installed.log;
combinedwhole-static43678 running /private/tmp/truck-pan-pump-outlet-static.log.
No mutation of isolatedmodel until these finish. It includes heaterelbow+5ECTposes.

Localservers had stopped during prior interruption; authoritative oldhandlemissing
and lsof no listeners. Restored127.0.0.1-only8081server60937 and8080server99079.
Browser testtab46 (CUAbindingpreview) shows pan54parts at60% stagedexplosion; rendered
and reviewed. Earlier tab45 is gone; usertab13 also gone by later lookup. Testtab46
needs markHandoff if preserving acrossturn. Mainviewerdata still1244parts.

InletV3 ready, notinstalled: module water_pump_inlet_v3_candidate.py, SHAe22fe3d9ad01e1d146b12ade6ec510c8bb26f4b5b107119cd6687320488749f4;
162neighbors/flow/material/rotation/STEPcontrols pass; docs/water-pump-inlet-v3-integration.md.
Agent engine_gaps now researching seal/bearing decomposition. Valveagentall12
source-sizedcandidate staticrunning; belt_fit examines shared ALT/Thermactor
casting identity. Connectedbelt diagnostic stillfails233mm3outlet/57mm3heater
collisions andlength; inletV3itselfclearsit7.04mm. No beltacceptance.

## Inlet installed and parallel integration — 2026-09-26

Combined cooling c2ea5860 passed 4,890 exact whole-static checks with no overlaps above0.1mm³. The20-part outlet installed audit passes265 checks, contact/head/flow probes and STEP symmetric differences. Its original default-volume check was sensitive to export integration; the new desktop checker retains default/adaptive metrics and tests actual symmetric difference (all zero), without relaxing clearance tolerance.

Inlet build completed: manifest2032a3dae31b2ae012752e79ba814e616c5406fb0a940336383358a91f8dc421,698definitions/1305occurrences. Actual installed inlet passes23neighbor checks, idempotence, STEP roundtrip, unobstructed passage, retained neck wall and blocked-flow negative control. Accepted housing, manifest and report saved cad/engine/candidates/pump-inlet-desktop/accepted. Production contours and dimensions remain assumptions.

Current parallel work: belt_fit owns isolated full_engine.py common-carrier integration; engine_gaps finishes mechanism-based pump-seal decomposition; valve_motion runs all12 phase audits and reviews browser spring performance. Root added conditional source-v2 browser motion dispatch, pending matching CAD regeneration. Shared main model has not been overwritten. Working preview8081 verified in tab48 with1305parts; main8080 remains older.

## Common carrier accepted; source-sized valve build running

Common carrier manifest3e450e499cd7ef66a97c0d659924f84a1ed729f853c637779c80024a0e5f50e0 has697definitions/1304occurrences. Installed39collisionpairs/12contacts/4seats/STEPdifference0 pass. Navigation initially found real stale learning links to removed brackets; corrected damper-learning and added common-carrier lessons to viewer/checker. Navigation1304parts/1501deep links and170capture hashes now PASS. Root visually reviewed candidate versus seller photo: broad cast webs/pockets/fork still missing; belt_fit owns independent fidelity followup.

Root added source-v2 motion dispatch and persistent definition adapter; source-valve narrow build42364 running in /private/tmp/truck-source-valves-build.log. Eleven definitions already exported, final assembly pending. Baseline manifest and four changed input STEP files saved cad/engine/candidates/valve-source-installed-desktop/baseline. Do not start another model mutation until build terminal and installed audits finish. Original code/manifest evidence retained.

Viewer now supports v2 global-axis translation, non-indexed ground-ended spring triangles, and geometry buffer-size changes. valve_motion is optimizing clipped-mesh update cost; candidate all12 dynamic collision audit still pending. No v2 installed/browser PASS yet. Working patch/provenance updated; not promoted to main. Mechanical-seal readiness against inlet2032a3da passed, awaiting integration; engine_gaps assigned next Thermactor internals research.
