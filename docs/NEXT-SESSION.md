# Engine work in progress

## Desktop continuation: parallel candidates and QC

User explicitly authorized three parallel agents on2026-09-25. Root owns integration;
independent candidates are belt layout, valve motion/rocker datum, and oil-pan
fasteners. These candidates are not published or complete. Root additionally
authored rear_manifold_mounts.py and its candidate checker for bolts15/16;
provisional stations and1996 comparison dimensions are explicitly limited.

Manifest90807873 remains frozen for candidate/installed audits. Root current
whole-static audit is terminal PASS:4542 exact checks,0overlaps above0.1mm3.
Rear installed audit terminal PASS; front regression terminal PASS. Navigation
1244parts/1438links and162capture hashes PASS. Root browser refreshed an old
679-part page and verified1244parts, exhaust navigation and actual rear mesh.
Exhaust assembly learning no longer incorrectly says the lifting eye/EGR joint
is entirely absent.

Root jobs still pending:54354 (dowel then explosion; its earlier eye invocation
was candidate-only, not installed),52952 (sampled core motion),96974 (rear bolts
candidate). Logs use /private/tmp/truck-*-current.log and
/private/tmp/truck-rear-mounts-candidate.log. Do not infer a pass from a running
job. Existing goal is usageLimited; user-side /goal resume was requested while
work continues in the current turn. Do not mark the engine complete.

## Latest build: rear entries and fitting published, installed audits passed

Build31395 is terminal PASS:688 definitions /1,244 occurrences. Manifest
`90807873b8c58234650e03b08557e524044f800d8fc3de97e212dd644e816cb9`.
Navigation1,244 parts /1,438 links and162 source capture hashes PASS.
Three revised definitions are published: rear casting, head and EGR manifold
fitting. No part-count inflation. The rear collector shape, auxiliary bosses,
factory EGR takeoff/routing and production dimensions remain unfinished.

Completed jobs (published-geometry holds released):
-81984 installed rear audit then front regression:
 `/private/tmp/truck-rear-entries-installed.log`, `/private/tmp/truck-rear-entries-front-regression.log`.
-54208 whole-static: `/private/tmp/truck-rear-entries-static.log`.
-24701 eye (`--rectangular`), dowel and explosion regressions:
 `/private/tmp/truck-rear-entries-eye.log`, `/private/tmp/truck-rear-entries-dowel.log`, `/private/tmp/truck-rear-entries-explosion.log`.
-95471 actual saved-STEP EGR half-section, then published exhaust render:
 `/private/tmp/rear-egr-fit-installed.log`. Terminal PASS; both output PNGs viewed.
Rear phase of81984 passes on90807873:three actual STEP matches,212 neighbor
checks,36 passage checks,24 corner controls and six positive rim bands. Front
phase is now terminal PASS as well. Whole-static54208 is terminal PASS:4,542
exact checks, zero overlaps above0.1mm³. Eye/dowel/explosion24701 is terminal PASS.
All reports refer to90807873. The engine itself remains unfinished.
No running audit is a pass. Older checkpoint current-revision language below
refers to its recorded manifest, not this new build.

## New isolated rear mounting candidate

`cad/engine/rear_manifold_mounts.py` implements bolts15/16 and four attachment
interfaces. Ford1994 text installs these bolts before the intake. The manufacturer
rear head-facing photograph shows both end holes on the same side of their
respective mouths; unlike the front, do not mirror its lugs symmetrically.
The numbered Ford sequence places both rear bolt stations forward of their
associated outer rear ports. Candidate offsets+40mm andZ315, lug sections and
socket geometry are explicit assumptions; bolt3/8-16x1.31 is a1996 comparison.
14356 passes validity and STEP roundtrips for all six changed/new definitions.
Full audit92934 is live (`/private/tmp/rear-mounts-qc.log`); it checks all saved
neighbors, positive seat/socket-wall/socket-floor material and all six exhaust
entry/runner passages. Candidate source is frozen during this audit.
Rear mounting export/render is also running (`/private/tmp/rear-mounts-preview.log`).
No rear mounting integration or clearance/visual pass is claimed yet.

## Rear manifold evidence checkpoint

Candidate42470 is terminal PASS:three STEP roundtrips,212 exact neighbor checks,
36 passage checks,24 circular/corner controls, six positive rim bands and head
contact. Fitting cutaway98315 is terminal and viewed; its bore connects into the
collector without the former protrusion. Tolerances were not relaxed.
Integration now has a `--refresh-rear-entries` path, composes the three adapters
after the front profile, and loads the source/learning records in builder, viewer
and navigation checker. Syntax and whitespace checks pass. Build31395 is running in
`/private/tmp/truck-rear-entries-build.log`; do not run installed validation until
it is terminal. Candidate geometry is not yet proof of installed composition.
Use `check-exhaust-front-profile.py --rear-entries --installed` afterward, then
front/eye/dowel regressions, navigation/source integrity and full-static checks.

Audit90100 is terminal FAIL, not live: three rear/head passages, all24 corner
controls, all six rims and212 exact neighbor checks pass, but the existing EGR
fitting obstructs the rear runner probe18.971609mm³ and the collector network
probe1493.884786mm³. The cause is its provisional19mm insertion envelope ending
6mm inside the old collector cavity. Current candidate includes a third changed
definition: fitting insertion12.5mm, ending0.5mm before the inner wall. Tube OD,
bore and external fitting/tube datum are unchanged. This fixes an assumed
geometric intrusion, not production routing or verified threaded retention.
`egr_tube.manifold_fitting` accepts the optional length but retains19mm by default,
so unrelated callers keep their existing geometry. Full candidate audit42470 log:
`/private/tmp/truck-rear-entries-qc-v4.log`. Its pass and visual inspection are
recorded above; its earlier pending status is superseded.

Current candidate revision rebuilds the rear casting consistently from shared
analytic runner transitions, preserving the provisional box collector and EGR
datum. It no longer unions new analytic transitions into imported runner faces.
Prototype65388 passed validity and STEP volume:403532.3587891267 versus
403532.35878893005mm³ (delta-0.000000197), without relaxed tolerance. The code
is now in `rear_casting()`; later casting changes must be composed afterward.
Prior full audit90100 log is `/private/tmp/truck-rear-entries-qc-v3.log`,
and export/render79782 is terminal PASS (`/private/tmp/rear-entries-preview-v3.log`).
The new PNG was viewed: all three rounded-rectangular rims are present; the
unfinished box collector is intentionally still visible, not a finished casting.
Keep the candidate, front profile, EGR module, checker and manifest frozen.
Prior58860 is terminal FAIL: the old overlaid candidate differed from its STEP
by1228.474mm³; directed-difference integration also failed convergence. Prior
75014 render is terminal and viewed, but shows only the rejected old candidate.
These failures motivated reconstruction rather than tolerance exemptions.

An isolated incremental rear-entry candidate now exists in
`cad/engine/exhaust_rear_entries.py`; it changes the three entry transitions and
matching head entries, not the unresolved collector/EGR routing. It is not
registered in the build or published. `check-exhaust-front-profile.py --rear-entries`
audits saved neighbors, positive rims, corner controls, STEP roundtrips and the
retained collector/EGR passage. Source compiles and diff whitespace checks pass.
Standalone diagnostic37417 exited137 before producing a shape result. Audit52336
was sampled after six minutes: active CPU in ShapeUpgrade_UnifySameDomain during
subtraction, not waiting for permissions. Root intentionally terminated it;
terminal143 confirmed, cell644 closed. No pass. Candidate now cuts only the
entry transition, not an almost-coincident full existing runner, with SkipClean
pending strict validity checks. Isolated diagnostic24870 is terminal PASS:
valid single solid and STEP export, log `/private/tmp/rear-entry-isolated.log`.
Full candidate audit93092 is terminal FAIL at the exhaust-rear STEP adaptive
volume comparison, log `/private/tmp/truck-rear-entries-qc-v2.log`; cell668 closed.
No neighbor, passage, corner, rim or installed pass is claimed. Volume diagnostic
58860 log is `/private/tmp/rear-entry-volume.log`; its failure is summarized above.
Initial preview exporter27440 succeeded but renderer failed due to missing CLI
assembly, then60449 failed because metadata had four colors for one shape.
Exporter now skips unnecessary front geometry and uses one rear color. The old
candidate render was inspected; the reconstructed candidate has now also been
visually reviewed as noted above. Full installed/neighbor verification is pending.
Five rear manufacturer source records have been registered and their capture
hashes checked. The matching unpublished learning JSON validates; neither it nor
the sources are in the published manifest yet.

Reviewed manufacturer674-186 front/back/overview photos and the Dorman2006
catalog PDF page130 (printed128). The F-100/1504.9L1994-90 row explicitly lists
674-186 rear. Live application iframe returned CAPTCHA, not fitment evidence;
the public manufacturer catalog mirror supplies the verified application instead.
See `reference/engine/dorman-674186-profile-reviewed.json` for source hashes.
Rear rectangular entries and blended branches need correction, but do not simply
mirror the front: two auxiliary plugged bosses are near the discharge neck in
the photographs, while the present EGR connection is an assumed collector-end
station. Identify the applicable takeoff/other port functions before relocating
the tube and jointly validating the rear casting. No rear geometry is changed yet.
No subagents remain live. Earlier worker usage-limit failures remain;
root is continuing directly. Current published manifest remains da6f293 below.

## Latest build: front exhaust profile published, audits passed

Build33140 is terminal PASS:688 definitions /1,244 occurrences, manifest
`da6f293a5c09498513ef4453a0fcba38b0b7ec4a11aa9a511c954269d0e4ee0a`.
Navigation1,244 parts/1,438 links and157 source capture hashes PASS.
Source/learning registration adds four manufacturer records. Root83367 verified
that the composed eye→dowel→profile head adapters repeat with empty directed
differences and connected valid solids. Full and partial builds apply the
profile LAST; it completely regenerates the front casting with retained eye
lugs and cuts the rectangular voids after those lugs exist.

Completed root audit jobs (shared-geometry holds released):
-28083 profile installed audit then rectangular-mode eye audit:
  `/private/tmp/truck-exhaust-profile-installed.log`, `/private/tmp/truck-exhaust-profile-eye.log`.
-83717 whole-static: `/private/tmp/truck-exhaust-profile-static.log`.
-85441 installed dowel, joint explosion, then actual exhaust render:
  `/private/tmp/truck-exhaust-profile-dowel.log`, `/private/tmp/truck-exhaust-profile-explosion.log`.
Use `--rectangular` for the eye checker on this revision; its older circular
runner probes intentionally do not describe the new openings. Installed profile
and full-engine render inspection remain required. No pending job is a pass.
Profile phase of28083 has passed on the current revision, including two actual
STEP matches,225 neighbor/35 flow checks,24 corner controls and six rim bands;
its eye phase is now terminal PASS as well. Job85441 is terminal PASS for installed
dowel,joint explosion and exhaust render; that render has been viewed. Whole-engine
render76254 is terminal and viewed. Regression47678 is terminal PASS: matching
the new casting and rejecting0.01,1and100mm displacements without relaxing
tolerances. Full-engine static83717 is terminal PASS:4,542 exact intersection
checks, zero overlaps above0.1mm³ on the current manifest. All listed audits
are terminal. Next: verify rear-manifold manufacturer photos/application and
preserve its EGR interface while correcting the rear casting profile.
The profile checker uses the actual prior circular STEP as its candidate
negative control; installed mode uses an explicitly labeled historical analytic
15mm circular envelope. It retains positive rim bands so missing inlet material
cannot masquerade as a successful open-port check. No tolerance exemptions.

## Latest integration: intake locating dowel

Build76221 is terminal PASS:688 definitions /1,244 occurrences. The completion
plan and matching manifest omission text were then synchronized without changing
geometry. Current manifest:
`716eb2b349aec8b75a44300738b594e3a073a3c0cb2fea6902b5b92101b8a22a`.
Navigation1,244 parts/1,438 links and153 local source-record hashes PASS.
The dowel has its own induction branch/page and loaded learning notes. Full and
partial generators compose its three interfaces after the lifting-eye adapters.
Candidate cutaway87599 was viewed; all three repeated adapters pass connected
validity, adaptive-volume comparison and empty directed differences.

Root9123 is terminal PASS:four saved-STEP matches,three exact joint/neighbor
checks,two full wall/two floor probes. Actual-STEP cutaway is terminal and viewed.
Root77940 joint explosion is terminal PASS:four targets against1,244 parts at
60/100percent,three exact checks,zero collisions. Root97132 whole-static audit
is terminal PASS4,542 checks/zero overlaps in `/private/tmp/truck-dowel-static.log`.
All root audits and downloads are terminal; holds released. The7.9375×25.4mm
pin is a1996 comparison;1994 identity, station, press/sliding fits and production
gallery compatibility remain unverified. Fourteen manifold attachment stations
and shared clamping details remain unfinished; this is not complete attachment.

### Next correction: source-supported front exhaust profile

Root has an isolated two-definition candidate in
`cad/engine/exhaust_front_profile.py`:three28×28mm rounded-rectangular entries,
matching head transitions into existing round internal passages, a capsule-form
collector and the retained lifting-eye lugs/outlet datum. All dimensions remain
explicit assumptions. Neither the candidate nor its head adapter is integrated.

First Boolean attempts failed validity or silently discarded inlet rims while
returning a valid solid. A visual review caught the missing rims. Root corrected
the transition/sweep joint to share the same0.27 curve station, instead of
overlapping almost-coincident surfaces; all three branches are constructed in
one local frame before translation. Diagnostic91032 passes connected validity
and preserves the rim. Updated render42431 was viewed: rectangular mouths and
curved collector now appear; rear casting and final mounting contours are untouched.

Audit19477 is terminal PASS in `/private/tmp/truck-exhaust-profile-qc-v2.log`.
It tests two STEP roundtrips, all saved neighbors,24 old-circle/new-corner
controls,six positive rim-material bands and complete connected collector/outlet
flow probes. Prior50951 failed three0.0564mm³ probe overlaps and is historical.
All candidate failures are empty. Subsequent composition, source registration,
installed/interface checks and current learning remain necessary before publication.
Important future composition constraint: apply the profile correction AFTER
the old lifting-eye adapter. Reapplying its circular lug relief after carving
rectangular passages may restore unwanted corner material. Update old circular
passage validators explicitly rather than exempting their collisions.

New Dorman674-185 front/back photos were saved and viewed. The manufacturer
application table explicitly lists1994F1504.9L Front; specifications say
rectangular ports and cross-reference F5TZ9430-A/F. The current circular entry
bores and box collector are a known form mismatch, not just dimension uncertainty.
Evidence: `reference/engine/dorman-674185-mounting-profile-reviewed.json`.
Prior inspection had reviewed only the three-quarter photograph and missed the
actual linked head-facing view. It shows three separate rounded-rectangular
entry pads,two end wings with enclosed holes and other projecting/scalloped lands.
Do not infer fourteen complete clamp stacks or manufacturing dimensions from it.

Next geometry must coordinate actual open rectangular-to-runner transitions with
head and gasket boundaries, preserving the checked eye and locating pin; no
cosmetic rectangular cover over circular holes. Completion plan now records this
new mismatch. Its new text will enter manifest omissions on the next build;
current716eb2 geometry and QC hash remain unchanged. The public1995 Scribd preview
HTML was retrieved under30MB but did not recover the target A24051-A figure.
No protected download was attempted; do not treat its text as visual evidence.

## Latest build: corrected manifold exploded spacing

Build58405 is terminal PASS,687 definitions /1,243 occurrences, manifest
`760d3f21ad0b38695f41ccf5409d011c08bdb0c715329b30154caf86f6c7d9bc`.
The three corrected display offsets are published. Navigation1,243/1,436 and
all152 source capture hashes pass. Geometry remains provisional; full scope
and production limits are unchanged.

Current-revision jobs are terminal PASS:49934 installed exploded-pose check
(three targets against1,243 parts at60/100percent),60515 installed seven-shape
matching/335 neighbor checks/20 interface measurements,92591 whole static
4,539 checks/zero overlaps. Exhaust render49934 and whole-engine render62114
are terminal and viewed. They remain offline visual inspections, not browser QC.

Next isolated work: intake locating dowel now uses the recovered1996 factory
comparison size7.9375×25.4mm instead of an arbitrary6×23.5mm. This is NOT proof
of1994 applicability. Assumed stationX0/Z298 remains; matching sockets now have
13mm head and9.9mm intake engagement,2/.5mm bottom clearances. Initial revised
audit65514 passes including full socket-wall/floor probes. Report metadata was
corrected and all loaded STEP hashes added; rerun35156 is terminal PASS in
`/private/tmp/truck-dowel-final-comparison.log`:four STEP roundtrips,five exact
overlap checks,zero collisions,two wall/two floor probes. Learning notes and
evidence reflect the revised comparison. All root jobs are terminal and holds
released. No dowel integration or new production-fit claim yet; visual candidate
inspection, repeat-adapter behavior and installed publication/QC remain next.

## Current integration: front manifold lifting-eye study

Build16767 is terminal PASS:687 definitions /1,243 occurrences, manifest
`afefab8a952178c0a7ac88b22294f427144ba56615b399ec9378b09ad98293e7`.
Three separate eye/stud13/bolt14 parts and four adapted casting/gasket
definitions are published. Navigation passes1,243 parts/1,436 deep links;
152 local source captures pass hash checks. Per-part learning is loaded.
Primary1994 installation sequence, later1996 figure and later fastener table
are registered separately; no later-year production identity is asserted.

Preintegration repeated-adapter audit50876 passed all four definitions:
second application stays valid, connected and unchanged in volume. Full and
partial generators retain the same adapters, not only the one-off saved mesh.
The head socket/foot study passed isolated audits, including explicit boss
walls and blind floors; this is not real thread retention or lifting strength.
Geometry, coolant-gallery compatibility and all other fourteen manifold
attachment stations remain incomplete/unverified.

Root43476 whole-static audit is terminal PASS4,539 checks/zero overlaps in
`/private/tmp/truck-eye-static.log`. Installed45066 failed only its
front-casting shape comparison: nonadaptive common-volume integration falsely
exceeded the shape volume by3.352mm³. Diagnostic15018 is terminal: both directed
differences are empty and adaptive actual/expected/common volumes are
402810.50808108/402810.50808107/402810.50812647mm³. The checker now uses converged
adaptive volumes without relaxing0.01mm³ tolerance. Installed rerun76755 is
terminal PASS7 saved-shape matches/335 neighbor checks/20 local interface
measurements. Regression67195 also passes: adaptive casting comparison rejects
0.01,1and100mm displaced geometry while matching the unchanged shape.

Explosion27410 is terminal FAIL: at60percent the eye intersects injector1 upper
and injector3 lower seals. Its chained installed render did not run. Isolated
offset trial65978 is terminal PASS against all1,243 exploded parts at60/100percent:
eye(0,-350,-100), stud(0,-440,-100), bolt(0,-500,-100). No bbox intersections
remain. All audits have terminated and those offsets are now in the generator.
A display-fix rebuild is running in `/private/tmp/truck-eye-display-build.log`;
its new manifest must be checked before the next shared-assembly edit.
Earlier checkpoints below
are historical and their hashes must not be substituted for this revision.

## Current verified checkpoint: starter motor feed integrated

Build23418 is terminal PASS:684 definitions /1,240 occurrences, manifest
`550892c05fd3bf618674d89a8be4b5556205ae1f98f08ccd2a65875476526fce`.
Navigation passes1,240 parts/1,432 links;149 local source hashes pass.
Whole static97400 passes4,515 exact checks with no overlaps above0.1mm³.
Motor-feed installed26889 passes14 saved-STEP matches,13 nonpenetrating
contacts,286 directed overlap checks and218 clearance checks. Starter97436
is terminal PASS:132 rest parts/848 checks and17 stroke poses/945 checks.
Installed explosion59467 passes; starter and whole-engine58219 offline
renders were viewed. These are not live-browser or production-fit certification.
All shared-assembly verification jobs are terminal. Two agents reached the
account usage limit; root continues direct integration and QC.

The isolated lifting-eye candidate is not installed. Raised provisional bolt
stations preserve the connected intake gasket and eliminate initial overlaps.
Automatic fusion cleanup invalidated two front-casting faces; preserving the
uncleaned fusion now passes single-solid validity and STEP roundtrip for all
seven candidate/interface shapes. Whole-engine audit4645 found1.7265mm³ of
bolt14/injector3 connector overlap. The provisional bolt station and its eye
foot moved from X45 to X49; this is a clearance assumption, not a Ford datum.
Recheck17721 is terminal PASS; see the frozen neighbor report. All three full
front runner probes remain unobstructed and both fastener shoulders contact
the eye, which contacts the front casting. No lifting strength, thread
retention or production-fit claim follows from these geometric checks.
The revised X49 offline preview was viewed. Expanded socket audit54607
correctly FAILED: the simplified head wall did not surround the proposed
blind sockets or supply complete bottom faces. Root added explicitly assumed
radius8mm head bosses, worldY-133..-109, preserving socket floorY-111.
Whole-engine recheck23302 is terminal PASS335 interference checks,12 occupied/
clear socket-and-foot probes plus two original-head diagnostic probes. Source
SHA is `0e7ee5506a6bbae66bb580b2ec372d9997c689f2d274d23895f9e849f734ef53`.
These bosses are not verified production coolant-gallery geometry. The updated
offline preview89517 is terminal and viewed. Individual foot/pad/shoulder/head
contact audit17180 is terminal PASS, including all six local contacts, in
`inventory/engine/manifold-lifting-eye-initial-validation.json`.
The learning file is authored but not loaded or published. Integration has not begun.
Do not interpret the older checkpoints below as the current assembly state.

## Verified checkpoint: compressor routes restored

Build22141 is terminal PASS,676 definitions /1,232 occurrences, manifest
`11937fe65dcc38f83431f95b0ee67c6a72d19c239c4e4dc156f9822f8beaac5a`.
Navigation1,232 parts/1,424 links and146 source hashes PASS. Root197-check
installed passage audit and1,687-check combined eight-phase compressor audit
both PASS, including both complete flow networks. API checks424 poses/120
analytic shoe constraints PASS. Whole static1374 PASS4,467 checks/zero overlaps.
Whole-engine offline render45299 is terminal and viewed; production castings,
missing belt/hoses and other declared gaps remain apparent, not hidden by QC.
All root11937fe verification jobs are terminal and holds released.

Root is validating the saved motor-feed integration adapter in
`/private/tmp/truck-motor-feed-metadata.log` before any publication. It remains
an isolated8-addition/6-replacement candidate, not installed. Lifting-eye initial
validator found an invalid self-crossing outline, disconnected front casting and
gasket, plus joint overlaps. Root fixed the outline; the remaining casting/gasket
and intake interferences still fail. Do NOT integrate that unfinished candidate.
Report: `inventory/engine/manifold-lifting-eye-initial-validation.json`.

## Live work: publishing the compressor passage correction

Root starter5389 is terminal PASS:124 rest parts/752 checks and17 stroke poses,
153 comparisons/945 moving-neighbor checks. All04c78259 holds are released.
The motor-feed agent's candidate neighbor report has no failures; after its
usage-limit error, escalated process inventory confirms its checker is no longer
running. Do not mistake the motor-feed candidate for published geometry.

Root is now running `--refresh-ac-compressor`, log
`/private/tmp/truck-passage-fix-build.log`, to publish the isolated checked
`ac_compressor_manifold_passages` correction. Root validators accept `--passages`.
After publication run own installed passage checker, combined compressor motion
and API checks, navigation/sources and full static QC. Count remains676/1,232.

Two agents reported account usage-limit errors. Root remains able to run tools;
do not claim parallel work continues unless agent status confirms it. Preserve
their candidates: motor-feed14solids/8additions has source/evidence/metadata and
an installed checker, but has not been integrated or root-reviewed as a complete
composition. Tensioner recovered factory figureA10700-E from the public PDF and
started a separate lifting-eye/stud13/bolt14 candidate; inspect files before
resuming, because its turn ended on the usage limit. Do not invent missing work.

## Current saved revision: corrected wiring and radial supports published

Build55402 is terminal PASS:676 definitions /1,232 occurrences, manifest
`04c782593eefbea5a6b43ad68eceac6df87ab77186e2ad68899ab8c48c6e5a81`.
Starter124 / compressor67. Navigation passes1,232 parts /1,424 deep links;
all146 source captures match. Whole static45677 is terminal PASS:4,467 exact
checks, zero overlaps above0.1mm3. Rest-stage5389 passes124 starter parts/752
checks; its subsequent17-pose stroke audit remains running. Wiring fit74687
passes10 actual saved shapes,eight face contacts,146 directed checks and0.35mm
minimum unintended conductor clearance, with no overlap exemptions. The prior
overlapping sleeves are replaced, not waived. Installed explosion/render41159
passes17 additions against124 parts at60/100%;29-part solenoid render viewed.

Compressor shaft-support86721 passes actual four revised/new solids,451 checks,
201 API poses and32 nominal contacts. Root combined API stage76823 passes, but
its full-route clearance stage FAILS: suction-network overlap2.862820mm3 with
the revised rear head. Agent compressor_review confirmed the analytic geometry
also blocks that path near the new bolt boss; this is not just STEP comparison.
An isolated correction must restore the entire old route without opening the
blind retaining-bolt socket. Narrow manifold-port and shaft-support passes do
not override this failure. No pressure-tight or full-flow acceptance is claimed.

Current holds: root stroke5389; ask agents for any newly started frozen-neighbor
jobs before rebuilding. All previously reported root/agent checks except5389
are terminal. Motor-feed agent works an isolated14-solid/8-addition candidate;
accepted starter geometry remains frozen. Manifold hardware agent is obtaining
an actually downloadable factory exploded illustration; no unsupported clamps
are installed. Intake dowel remains a separate checked candidate.

Browser inventory still has no enabled browser surfaces. Offline renders are
not live WebGL interaction proof. User asks for progress updates every few
minutes and at milestones; continue without requesting interim review.

## Latest saved revision: manifold integrated, starter correction pending

Build34194 is terminal PASS:674 definitions /1,230 occurrences, manifest
`70ad7d96946fbb9b053f4b52314e2246778a75f03fd8510f3c2a130892ca5a02`.
The FS10 now has65 parts, including rear manifold, two sourced-size comparison
seals and retaining bolt. Navigation passes1,230 parts /1,422 deep links and
145 source captures. Root installed manifold/API job13944 remains running.
Offline65-part compressor render42208 is terminal and viewed; a rear camera
render66332 is pending because the default view hides the rear interface.

Starter geometry is unchanged from the failed302200fd static audit below.
Root rest49631 also failed those same eight overlap pairs; its full-stroke stage
passed only moving-neighbor scope. All302200fd holds are released.
Corrective `starter_wiring_fit.py` passes isolated17-pose checks without overlap
exemptions; agent full-neighbor38738 holds70ad7d pending terminal release.
Its integration wrapper is pending. The corrected eight-wire explosion layout
is also staged, not published. Do not claim current whole-assembly static PASS.

Other isolated work: intake dowel77538 passed; head/intake/gasket adapters have
not been integrated. Fuel valve motion87713 passed; viewer-ready learning schema
is being prepared. Agents continue compressor radial support and16-station
manifold hardware research. No complete-engine or production-fit claim.

## Current checkpoint: coil leads and sized FS10 bearing published

Sequential build45385 is terminal PASS,670 definitions /1,226 occurrences.
Manifest SHA256 `302200fd628564389445450404d1ff463ae4b59e9b82821e288ae487a565cba0`.
Starter has124 components; the compressor retains61. Navigation passes1,226
parts /1,418 deep links, and all142 local source captures match their hashes.
Wiring installed audit82823 passes10 saved shapes,100 overlap checks,eight
contacts and171 clearance checks; minimum unintended conductor clearance0.35mm.
Compressor installed API/clearance job86897 passes412 pose and120 analytic shoe
checks plus its eight-phase clearance/route audit. Offline compressor render12682
at90degrees was inspected; it is not live-browser verification.

Full static87741 is terminal FAILURE:4,463 checks find eight overlaps. Six are
embedded lead endpoints, one is the shared-S copper overlap, and one is a23.623mm3
overlap between distinct lead sleeves. Wiring82823 allowed intended junctions;
that narrow pass does not override the whole-assembly failure. Agent starter_wiring
now owns isolated `starter_wiring_fit.py` to separate S routing and create face
contacts rather than waive overlaps. Current saved geometry is NOT accepted.
Root stroke49631 passes17 poses/153 comparisons/951 moving-neighbor checks;
its chained rest audit is still running. Agent manifold67086 and dowel77538
have both passed and released their holds. No result is claimed for a live job.

Installed explosion QC39309 correctly failed: a new lead intersects the exploded
hold-winding at60%. Root staged `starter_explanations.wiring_api` to move eight
lead/sleeve parts into a separate spaced column. Candidate73719 passes all17
new solenoid components against124 starter parts at60/100%, with disjoint bounds.
The metadata correction is NOT YET published. Wait for all holds, refresh starter,
rerun installed explosion QC and render/review solenoid. Physical geometry is
unchanged; do not present candidate explosion proof as installed proof.

`completion-reconciliation.json` audits all63 checklist items;14 stale absence
entries were clarified in the plan without dropping production-fit/internal gaps.
Fuel-valve motion87713 passes six states,38 STEP roundtrips and139 checks, but is
an isolated adapter/learning overlay, not integrated viewer animation. Manifold
candidate has four new parts and a rear-head revision; frozen-neighbor QC passes.
Its builder, three sources, learning loaders and root `--manifold` validators
are now staged for the next compressor refresh, NOT yet published. Navigation
checker is consequently staged for65 compressor parts and will not pass the
current61-part compressor until that refresh. Single intake locating-dowel
candidate also passes frozen-neighbor checks but remains separate, not published.

All sections below describe earlier checkpoints.

## Latest checkpoint: linkage integrated; wiring and bearing staged

Saved assembly remains 662 definitions / 1,218 occurrences, manifest SHA256
`73dd4bdab67fc7fbc3a36c502b0cf079f4fe4641aa0d0454ed8b097ce2eea63e`.
Eight starter linkage replacements and the corrected solenoid explosion are
published. Full static QC passes 4,390 exact checks with no overlaps above0.1mm3.
The offline whole-engine and solenoid renders were inspected at preceding
revision f46a4631, not the current linkage revision. Live browser QC is unverified.

Two saved-STEP pose checks initially failed on the lever. Investigation found
matching bounds, volume and topology, but OpenCascade returned an empty common
between analytic and serialized coincident surfaces. Independently STEP-roundtripping
the expected shape restores the comparison without relaxing0.02mm3 tolerance.
`check-step-comparison.py` passes and rejects0.01mm,1mm and100mm displacements.
The rerun rest audit56103 passes116 parts and628 neighbor checks. Full-stroke
audit30838 is terminal PASS:153 pose comparisons across17 samples and639 exact
neighbor checks, no overlaps. Agent tensioner still holds the current manifest
for fuel-valve audit87713; wait for its explicit release before rebuilding.

Root staged wiring and bearing integration, source registry and lesson loaders,
but has NOT rebuilt them. Wiring adds eight parts and replaces two feedthroughs;
candidate tests pass17 poses,1196 intersections, eight contacts and0.35mm minimum
unintended conductor clearance. The FS10 bearing envelope revision reconciles
eight interfaces to the sourced30×55×23mm cartridge, retaining61 compressor IDs.
Neither revision establishes production fit or complete electrical/bearing internals.
After holds release, run separate starter and compressor refreshes, then current
static, navigation, source, installed motion/wiring audits and new visual renders.
Use `--wiring --engagement` for starter rest QC and `--bearing` for compressor QC.

Parallel work continues on rear compressor manifold evidence and fuel-test-valve
opening continuity. The clutch agent established the10-inch R2 baseline from
owner confirmation, door code M and the1994 decoder; its isolated clutch remains
non-installable until diaphragm/damper load-path details are resolved.

All checkpoints below are historical, not current build or live-process claims.

## Current checkpoint: solenoid internals integrated, installed audits passed

Build 24795 is terminal PASS: 662 definitions / 1,218 occurrences. Manifest SHA256
`9eebd4578c112926b994566965ca61c6e2634fa280b660c1ab1d7ada0cf5c15c`.
The starter now has 116 components, 51 role-specific functions and 113 distinct
explosion vectors. The aggregate solenoid coil is replaced by pull/hold envelopes,
bobbin, fixed pole, insulated moving contact/rod, and separate S terminal. Four
existing definitions are revised; net addition is eight parts. B/M terminal faces
and the contact bridge close in an isolated geometric stroke test, not a complete
starter engagement or physical electrical-circuit simulation.

Navigation passes 1,218 parts / 1,410 deep links; all 139 source captures match
hashes. Root saved and read the Ford patent HTML; only its Figure 1 conventional
background is used, not the proposed single-terminal invention. Solenoid candidate
audits pass 13 STEP solids, 39 internal checks, 20 neighbor checks and 17 contact
stroke samples including spring spacing and rod/bridge insulation clearance.

Root installed solenoid/full-starter audit 43818 is terminal PASS: 13 revised/new
saved solids match expected poses, 58 solenoid checks and 628 full-starter checks,
zero overlaps. Full static audit 25443 is terminal PASS: 662 valid definitions,
1,218 assembled STEP solids and 4,390 exact intersection checks, zero overlaps.
Root manifest holds are released. Solenoid offline render 1967 is terminal and
was visually inspected. Existing plunger/lever linkage remains static;
oil_drive agent now investigates a separate mechanically coherent engagement
revision. Other agents retain bearing/internal-construction research ownership.

Visual QC found the newly added winding/bobbin explosion offsets too close.
Root staged `starter_explanations.solenoid_api` and its full-engine call to separate
those nine additions radially from the old shell and axially from one another.
`scripts/check-starter-explosion.py` (38384) passes: all nine additions have disjoint
bounding boxes from other parts at 60% and 100% explosion. This metadata correction
is NOT YET in the saved manifest; publish with the next `--refresh-starter`, then
re-export/review the solenoid render. Accepted physical geometry is unchanged.

All checkpoints below describe earlier saved assemblies and historical tests.

## Current checkpoint: starter integrated, installed QC passed

Starter build 37121 is terminal PASS: 654 definitions / 1,210 occurrences.
Manifest SHA256 `604a0e6809ea8c8d28b12d5a776f951535c60af73a3c0ad9957e368750a05b9c`.
The 108 starter components have 43 role-specific explanations and 105 distinct
explosion vectors via `starter_explanations.api`; geometry remains accepted
`starter_motor.py` SHA3841a065c9bb465306a2b257e0329da021d4886324c127c17a47a3ecf274a433.
Five starter lessons and three factory diagnostic sources are connected. Root also
added two factory compressor diagnostic sources/lessons. Navigation passes 1,210
parts / 1,402 deep links, and all 138 local source captures match their hashes.

Installed starter STEP/pose/neighbor check 15681 is terminal PASS: all 108 saved
solids agree with expected placements, 572 exact checks, zero overlaps. Full
static check 18502 is terminal PASS: 654 valid definitions, 1,210 assembled STEP
solids and 4,362 exact intersections with zero overlaps. Root manifest holds are
released. Offline starter export/render 59135 is terminal and was visually
inspected. Candidate starter checks passed 108 STEP solids,
283 internal checks, 31 reducer poses and 17 engaged pinion/flywheel poses;
candidate neighbor check found six broad-phase pairs with zero overlaps.

Starter stays stationary/retracted during normal engine animation. Bellhousing,
index plate, mounting bolts/support, installed station, S terminal, pull/hold
circuits, contact bridge, overrunning internals and complete actuation remain
unresolved. A separate solenoid extension is the oil_drive agent's next task.
Compressor agent investigates bearing decomposition; tensioner agent investigates
Gates bearing/spring/damper internals. Three rejected belt-layout sweeps and their
constraints are preserved; no speculative shortened layout was installed.

Offline QC now uses `scripts/engine_qc_raster.py`, a depth-buffered orthographic
renderer rather than painter-order triangles. Tests cover per-pixel intersection
visibility, ordering, winding, degenerate faces and framing. Starter re-render
91634 passes and was inspected: the earlier striped surface artifacts disappear,
and exploded motor/gear/solenoid components remain distinct. Rendering uses system
Python with NumPy, Numba and Matplotlib; CAD mesh export still uses `.venv-cad`.
This improves offline geometry inspection but does not verify browser interactions.

The earlier checkpoint below describes the previously verified 1,102-part build.

## Current checkpoint: filter mount and compressor revision integrated

The saved assembly is 546 definitions / 1,102 occurrences, manifest SHA256
`631eded833ee58db78882ee1182c7f732d6dcb5be8205db19c3ac7d9c57903ec`.
Filter build 70332 and installed audit 98472 are terminal PASS. The audit uses
saved STEP solids and manifest placements, checking eight inlet corridors,
separated inlet/outlet routes, continuous gasket support and static neighbors.
Navigation passes 1,102 parts / 1,289 deep links; all 129 registered local source
captures match their hashes. These checks do not establish production accuracy.

Prior accessory, oil-drive motion and ignition explosion builds all completed.
The previous 1,101-part manifest passed full static QC (4,057 broad-phase pairs,
zero overlaps) and installed pump motion (25 poses, 933 exact checks). Those full
assembly reports predate the filter addition; do not label them current audits.

Compressor follow-on candidate is accepted: 61 STEP solids, 1,625 exact checks,
eight phases, two connected/disjoint channel probes and 20 reed-window checks.
Shared-transform callback verification passes 412 shape and 120 analytic checks.
Root compressor rebuild 4133 is terminal PASS. The saved assembly now includes
17 FS10 motion groups, new sources and lessons. Actual installed STEP/motion and
passage audit 88299 is terminal PASS: 61 STEP solids, eight phases, 1,625 exact
checks, zero overlaps, two connected/disjoint probe networks and 20 reed checks.
The subsequent installed API audit passes 412 shape and 120 analytic checks.
Full static audit 76469 is terminal PASS: 546 valid definitions, 1,102 assembled
STEP solids, matching mesh bounds and 4,073 broad-phase pairs with zero overlaps.
Offline compressor phase-90 render 68467 completed
and was visually inspected: role-based explosion separates case/head stacks,
pistons and clutch pieces. Matplotlib surface-order artifacts remain, so this is
layout evidence rather than verified live WebGL surface appearance.
Root audit freezes are released; coordinate any rebuild with active agent audits.
Browser inventory remains
empty; offline renders are not a substitute for live viewer interaction checks.

Agents remain active: starter construction, compressor bearing decomposition,
and belt-layout reconciliation. The accepted long belt/support candidate is not
integrated and is not a verified fit for the catalog 2,491 mm belt. A numerical
shorter-layout hypothesis is not evidence of factory accessory coordinates.
Its first exact sweep 4376 is terminal and rejected: the belt hits a Thermactor
bolt at all three tested angles and the coolant outlet at two. Failures remain
recorded; no rejected stations were installed.
Refined sweep 91589 also rejected: moving the compressor inward strikes the
timing cover/cam gear and the belt still hits the outlet at one travel endpoint.
Both agent freezes are released. Numerical near-matching outside-radius length
does not establish the belt's actual effective or cord length.
The filter's open gallery boundaries are not a complete lubrication circuit;
the E4TZ anti-drainback service insert remains unreconstructed.

Root additionally reviewed industrial manual PDF page 100 (printed 8-03): its
6.2082-6.2112 inch rod center-distance range includes the existing 157.7 mm model.
The dimensions ledger now cites that comparison but retains assumed status and
`rod_length_verified: false`; 1994 truck applicability and pin offset remain open.
No core geometry changed. Review record: `reference/engine/ford-csg649-rod-length-reviewed.json`.

Sections below are chronological work history, not current process status.

## September 25 accessory/support and pump-motion batch in progress

Root accessory rebuild 96821 is LIVE. It uses the accepted compressor module
`a642b8c9e89de926db61f3515bf4eee31743bb599c280318f05c7c88f0931799`,
imported and hash-checked before assembly work to isolate it from follow-on edits.
This batch adds 15 support parts, 61 compressor parts and 20 Thermactor exterior/
support objects to the 1,005-part assembly. Expected count is 1,101 occurrences /
545 definitions; do not treat that expectation as a completed build.

All candidate freezes were released: oil-drive installed audit 35869 PASS 25 poses,
933 exact checks; isolated 12994 PASS 73 rotor/socket poses and 17 gear samples;
callback 29694 PASS. Compressor final candidate PASS 61 STEP solids, 1,257 checks,
eight poses; interfaces/brackets PASS 61 transforms and 50 checks. Thermactor
38326 PASS 21 STEP solids (20 components plus adapted block), 48 checks.

After 96821 terminates, run `--refresh-oil-drive` to install the composed
`oil_pump_motion.pump_api`/`drive_api` wrappers already staged in `full_engine.py`.
Then run `--refresh-ignition-leads` for the corrected explosion vectors. Hold
new installed audits until these serial builds complete. Navigation accessory
expectation is now 176 parts. Re-run navigation, source hashes, installed static,
sampled motion and offline visual checks on the final stable manifest.

Agent follow-on ownership: oil_drive now models filter mounting/adapter interfaces;
pump_pulley handles compressor fluid-network and rigid-motion corrections in a
separate follow-on module (keep accepted base frozen); tensioner handles belt
tangent routing and tensioner support. Belt diagnostic currently finds 2,785.4 mm
outside-radius path versus catalog 2,491 mm effective length and inconsistent
assumed pulley groove pitches. Do not force a belt onto those mismatched profiles.
Thermactor cartridge remains unresolved; current exterior is not complete internals.

## September 25 steering and secondary-ignition integration

Current assembly: 449 definitions / 1,005 occurrences. Manifest SHA256:
`9c2a4d13a70d0bbc9343598dc09c56286de7e25b60351d1cfaea7e2b061d6c71`.
Accessory build 72872 and ignition-lead build 77464 are terminal PASS. The 46-part
CII pump and corrected top-center tensioner are integrated. Seven six-part leads
and seven coil-mount parts are integrated with cap contact pockets and head bosses.
Navigation passes 1,005 parts / 1,168 deep links. Full installed static audit
29761 is terminal PASS all 3,626 broad-phase pairs, zero overlaps. Artifact/scale/
hierarchy checks passed. Core-motion audit 34579 is terminal PASS four poses,
zero overlaps. Navigation and 1,441-sample idealized mechanism checks also pass.

Root added generic `rotary` motion descriptors (`axis`: CAD x/y/z, `ratio`: shaft
degrees per crank degree, optional shaft `phase_deg`). CAD and viewer implement
the same local rotation after the assembly base tilt. Independent checks passed
441 CAD poses and 1,305 viewer-axis cases. This infrastructure does not yet animate
the pump: oil-drive agent is preparing conjugate 4/5 rotor profiles, D-flat drive
and composable pump/intermediate wrappers. Initial isolated audit 2357 failed and
was corrected; final isolated audit is 29578 and frozen installed audit is 35869.
Final isolated 29578 passed six STEP solids, 73 socket/rotor poses, and 17 gear
samples; adapter check 69716 passed. Installed 35869 is still live, last observed
by agent at 90 degrees with 149 checks and no collisions. Agent owns these handles;
they cannot be polled from the root terminal runtime.

Tensioner agent owns accessory brackets with explicit dry block/head boss and
blind-hole adapters, then Thermactor pump research. Bracket audit 77223 is terminal
PASS 17 STEP solids and 97 exact checks, zero overlaps against this manifest;
compressor cross-check remains pending. Pump/pulley agent owns FS10 compressor, adding ten
piston rings and sourced 145 mm six-groove clutch envelope before final QC.
No root rebuild until all installed audits release the manifest. Active agents
have isolated work available while checks run; no user review is requested.

Offline PS/ignition exports and PNG renders 59432/12934 are terminal and visually
inspected. The PS offline render has painter-order surface artifacts, so it is
layout evidence rather than proof of live-viewer surface appearance.
Ignition visual QC exposed identical explosion offsets hiding the cable internals.
Root corrected per-component offsets in `ignition_leads.py` (geometry unchanged),
but this is not yet in the saved manifest. Re-run `--refresh-ignition-leads` after
the current frozen audits release, then render again to verify visible separation.
Browser inventory rechecked through CUA: no connected browsers; do not substitute
offline mesh renders for a live viewer interaction check.

## September 25 cooling integration and accessory-layout correction

Current assembly: 354 definitions / 910 occurrences, manifest SHA256
`95236469efc7b11aab9423bc2426fb7a94143fa8f2bab152e05e0e1620e199f1`.
Cooling build 59327 is terminal PASS. Seven new occurrences represent two hollow
heater takeoffs and the two-wire ECT; the pump housing receives an open return port.
Candidate checks passed seven STEP solids, 34 exact checks, four open-bore probes
and seven API placement comparisons. Navigation passes 910 parts / 1,063 links.
Installed audits 52496 and 6339 are terminal PASS: 3,029 static broad-phase pairs
and four core/lubrication poses, zero overlaps; artifacts/scale/solid counts pass.
Offline cooling export/render also completed and was visually inspected.

Agent ownership continues: tensioner agent revises PS and tensioner together;
oil-drive agent resolves ignition-lead crossings; pump/pulley agent now builds
FS10 A/C compressor internals. All have the 910-part manifest for frozen checks.
Upper-LH steering-pump placement passed, but the first top-center tensioner
placement collided with the throttle/outlet and was rejected before integration.
Revised candidate wheel is (473.56,0,435), pivot (433.56,-75,435). Combined PS and
tensioner QC 90536 passed 54 STEP solids and 183 exact pairs against this manifest.
Root staged shared source/learning integration for the 46-part steering pump and
relocated tensioner. Do not run the accessory build until ignition-lead frozen
audit 17388 releases the manifest. Source generation already includes the pump,
but the saved 910-part manifest does not yet contain it. Navigation accessory
count must become 80 after that build (currently 34).
Do not integrate a collision-free accessory arrangement that contradicts the
reviewed belt routing merely because it is easier to fit.

Root reviewed Ford routing image 212084317.png and DENSO compressor catalog page
42. New `ac-compressor-evidence.json` records FS10/471-8130 factory-A/C application,
Ford clutch air-gap limits and explicitly nontruck construction comparisons.
The separated-parts comparison photo was visually inspected. Installed compressor
identity, all production dimensions and coherent moving internals remain open.
Distributor assembled/exploded offline render was also visually inspected; no
live browser review is claimed. Engine completion remains false.

## September 25 second integration batch

The current assembly contains 348 definitions / 903 occurrences. This adds the
26-part alternator, 35-occurrence fan/clutch, two-part regulator vacuum connection
and a connected oil-drive layout. The old uninstalled `oil_pump_drive.py` candidate
described below is superseded by `oil_drive_layout.py`: the manufacturer-size shaft
now connects provisional distributor and pump sockets along a common tilted axis.
Block passages/mounting columns, cam gear, pickup tube and pump/distributor geometry
are adapted together. Production dimensions and coordinated pump motion are still
unresolved. Do not describe the illustrative mounting architecture as factory fit.

Navigation currently passes with 903 parts and 1,054 deep links; nested group
rotation passes 49 poses. Whole-assembly audits are terminal PASS: 348 valid STEP
definitions, 903 assembled solids, GLB bounds within 0.5 mm, zero overlaps among
3,011 static broad-phase pairs and four sampled core/lubrication motion poses.
Both reports match manifest SHA256
`8452ed8bfbe050a2f55bcb20384195f564b2c4c1c1d95eea82d62e6ae86dbdad`.
The idealized crank mechanism also passes 1,441 samples; valve and pump motion
are not covered by that result.
Offline mesh-render QC visually inspected tensioner, alternator and fan/clutch
assembled/exploded views. This does not substitute for live browser review.

Agents continue power steering (neighbor check 71799 passed, but routing evidence
requires revised upper-LH placement and coordinated top-center tensioner), cooling/heater connections,
and ignition leads/coil bracket. Manifest is frozen for their neighbor audits.
Only root integrates shared files. Project `.codex/config.toml` selects automatic
approval review with workspace-write sandbox; the live session now confirms that
review mode. macOS computer-use permissions remain separate.

All earlier counts and failed oil-drive candidates below are historical.

## September 25 parallel modeling batch

Three modeling agents delivered tensioner support, water-pump pulley and oil-pump
intermediate-drive candidates. The root integrates shared files and runs combined
QC; agents own separate generator/evidence/check files. User authorized this workflow.

Accessory integration adds 13 occurrences and 10 definitions relative to the
September 24 build, for 836 occurrences / 304 definitions. The two pulley envelope
parts are in `tensioner_pulley.py`; six support parts in `tensioner_arm.py`; five
pump-pulley occurrences in `water_pump_pulley.py`. Use `--refresh-accessory-drive`.
The assumed common belt plane is X473.56; the initial X465 tensioner placement
was corrected after cross-agent QC. No measured factory alignment is asserted.

Oil drive remains an UNINSTALLED candidate in `oil_pump_drive.py`. Its manufacturer
dimensions expose 134.678 mm axis offset, an undersized pump socket and six core
overlaps. Reconcile drive axis/cam engagement/block passage/pump mounting together;
do not simply force the shaft through existing geometry. Supporting evidence and
candidate-validation reports are in `inventory/engine/oil-pump-drive-*.json`.

Candidate QC passed for accessory solids/STEP, individual installed neighbors and
40 cross-agent pairs. Combined installed QC passed: 304 valid definitions, 836 STEP
solids, GLB bounds within 0.5 mm, 2,728 static candidate pairs without overlap,
four sampled core-motion poses without overlap, and 982 navigation links reaching
all 836 parts once. Idealized mechanism check also passed at 1,441 samples.
Installed manifest SHA256:
`7d11501cee5e4a6ba06898ea0af1fa3ca0f020a35ed55e2c3eca7dcefa365dfa`.
Both atlas reports match this manifest. All batch CAD/check jobs are terminal.
Visual browser review was blocked: no connected browser and computer-use permissions
pending. Do not claim that these additions have been reviewed in the live viewer.

Older session history follows; its counts and live-process statements are historical.

User requests sustained iteration through the complete 1994 4.9L engine before review, then whole truck. Engine is NOT complete. User explicitly authorized parallel modeling subagents with an integration/QC step on September 25. Assign separate generator/evidence/check files; one integrator owns shared manifests/builds. Preserve the dirty tree. Do not confuse occurrence counts or interference checks with production accuracy. The previous session's goal tool reported `usageLimited`; do not claim its autonomous continuation is active without checking.

## Current installed build

291 definitions / 820 occurrences / 962 navigation links.
Manifest SHA256: `c35fa2cc41ecdd2d030df627b8b1c447de6382145ea60ca53b7b139fba3dbdd7`.

Flywheel and pilot-bearing construction studies are installed, and navigation passes. Pilot build77646 terminal0. Core motion57095 terminalPASS (0/90/180/270, zero overlaps). Static1351 terminalPASS2691pairs/zerooverlaps. Both installed report hashes verified against currentmanifest. No live CAD jobs. Previous flywheel-only static30429 and core61769 terminalPASS, but those reports described the earlier801-occurrence build. Retention report is older; not rerun because cam hardware was unchanged.

## Latest additions

- `cad/engine/flywheel.py`: LFW132-family comparison body, 164-tooth ring and6 bolts;8occurrences3defs. Position(-393,0,0),rotation(0,-90,0),local+Zrearward. HICENGINE FFM68 constrainsOD362,bore44.5,thickness25,crank6x11onPCD76,coverPCD295. Recesses,ringwidth10,coverholes6/angularindex,thread/profile/fit are provisional. Ring initialsharedgearhelper generatedinvalidsolid at164teeth; replaced with local correctedroot-angle profile. Shape/STEPvalid andcandidate18953PASS107checks. Build88668terminalPASS.
- `cad/engine/pilot_bearing.py`: FC65662 study,case/cage/seal+16illustrative needles (19occurrences4defs). Position(-381,0,0),rotation(0,-90,0),OD36.576,bore17.07134,width17.018 fromTimkenneedle-table. Internal16count,3mmrollers,11mmlength,racesection,cage,seal andseatdepth provisional. Candidate95877terminalPASS130checks. `--refresh-pilot-bearing` modifiescrankbore andadds19parts. Fullbuildappliesflywheelinterface thenpilotinterface. Refreshflywheelreappliespilotbore ifpilotpresent, toavoidrefillingregister.
- Lessons in `damper-learning.json`; comparison-source entriesregistered. Viewerghostcovers includespilotcase/seal. Browser43 flywheelReview verifiedflywheelassembled/exploded70%,pilotassembled/ghost/exploded40%; currentlypilotpageopen. Browser42fromearlierEGRreviewmaystillopen. Bothagent-created; close orhandoffproperly. Usertabsuntouched.
- New scripts `check-flywheel-candidate.py`, `check-pilot-bearing-candidate.py`. They export/reimport candidate solids and checkinternal+installedneighboroverlap againstfrozenmanifest.

## Saved sources

- LuK2012 `reference/engine/luk-repset-2012.pdf`: PDF105printed103 LFW1324.9L1975–96; PDF102printed100 clutch07-1281993–94five-speed11in and07-0981994ten-inch. Both1 1/16inch10splines. Installedclutchdiameterunknown. InitialLFW112leadWRONG. KBsourceandreviewJSONsaved.
- HICENGINE `reference/engine/hicengine-flywheel-catalog.pdf`: PDF1headers/PDF6FFM68visuallyreviewed, dimensionsabove plusdisc-facingOD270 (NOTinstalledclutchdiameterproof). AuthorHICENGINE;replacementcomparisononly. KBsourceand`hicengine-ffm68-reviewed.json` saved. AESPythonreaderfailed; systemPopplerworked, capturedpages1+6ingestedaslocaltext.
- ATPGraywerks `reference/engine/atp-graywerks-catalog.pdf`: PDF435printed433shows103024pan1983–96Ford4.9crossF6TZ6675LA. PhotoandKBsourceacquired. No dimensions; futurepancontourreference.
- Timken `reference/engine/timken-1990-newer-bearings.pdf`: PDF184printed166FC65662for1990–2002half-ton6cylincluding4.9;release6141691993–99hydraulicfive-speed. Visuallyreviewed/ingested.
- Timken `reference/engine/timken-bearing-specification-guide.pdf`: PDF150printed147needle-tableFC65662. PDF102printed99pilot-tableinsteadgivesbore.671/OD1.450/width.669in; preserveconflict. Bothvisuallyreviewed. PDFrenderhasgraycodecnoisebutrowsclear. DownloadfromAHRarchiveworkedaftermanuals.plus403. `pilot-bearing-evidence.json` retainsbothrows. KBsourcesprocessedfalse. No specificSPCLinternalsection. Retaildimensionsnotpromoted.

## Earlier installed EGR

EVR4exteriorparts only (coil/valveinternalsNOTmodeled), pluscontrolhose. EGR+EVP31parts,tube/sleeve/twofittings4parts. Sourcevacuumhose,mountinghardware,wiringstillunfinished. See moduleGAPS/sourcefiles. LastEGR-onlybuild284defs793occurrencespassedstatic/core/retention. Do notredownloadpaidEVTM; localPDFalreadyacquired. EVTM312printed151-1showsC180belowEVPatLHrear;75/77printed23-2/23-4givecircuitidentities.

## Continue

Substantive gaps remain infrontaccessorydrive/brackets/belt/pulleys/fan,hoses/wiring/sensors,hardware,coreplugs/galleries,castingcontours,andcoordinatedvalvemotion. `completion-plan.json` false, queueinprogress. ScalarMellingSYB38camdataalreadyexists; fullprofile/basecircleunknown, do notpretendscalarvaluesestablishproductioncurve. Clutchboundarymayremainseparatetransmissionscope; pilot/flywheelpartoftheengineinterface.

Use `.venv-cad/bin/python`; build123d/OCP/trimesh. No livebuildwhileauditsrun. Pollknownhandlesratherthanrestarttimeouts. Avoidbroadprocesscommandlisting; itcanexposeunrelatedprivateargs. CUAaftercompactionmustrewriteDocumentation. No newcommit/pushrequested.

## Subsequent damper work — latest installed build supersedes counts above

294 definitions / 823 occurrences / 965 links. Added `damper_attachment.py`: key, washer, center bolt, matching key pockets, front snout extension and smooth bolt bore. Hardware/shaft dimensions provisional. Candidate17592 PASS134checks. Damper refresh now also updates crankshaft, and fullbuild applies attachmentinterface. Two builds76087/39890 terminalPASS. Damper hub now has a front recess; outer rim six illustrative V grooves. Dorman photo `dorman-594-152-front.jpg` reviewed/saved: integrated serpentine pulley, keyway, recessedweb/pullerholes, timingmark. Noindependentbolt-onpulleyjustified. Paintcolorstillgenericgray, shouldmatchblackreference infuture. Groovecount/profile/indexstillprovisional.

Latest static56843 and motion48107 terminalPASS, zerooverlaps; report hashes verified. Static2702pairs, core4poses. ManifestSHA256 bbf8b19a79b3b0d8517b7055822d741423858b49e8419087075f4397eca56e22. No liveCAD jobs. Navigationtestupdateddampercount3->6andPASS. Browser43 nowdamperpage,assembledrenderreviewed. Browser42earlierEGRmaystillopen.

Gates2008 publiccatalogdownload9483terminalPASS `reference/engine/gates-2008-car-light-truck.pdf`. PDF473printed389visuallyreviewed/ingestedKBsource: 1994FSeries4.9K060980withAC/K060970without; tensionerpulley38022/assembly38131,upperradiator22417,lower20609factoryACor21236/26505dealerAC; manual5speedheaterbothentries18767. Metadata `gates-1994-drive-reviewed.json`. RoutingindexPDF119printed35S7004withAC/S6008without. DiagramS7004PDF163printed79visuallyreviewed:7points,schematicONLY. Usefornextaccessorylayout,don'ttreatasdimensionedcenters. NumericalbeltdataPDF965printed? notvisuallyreviewedyet; K06098020mmtopwidth/outside2505/40deg butnoinferredexactpulleyprofile.

Gates38022 manufacturerdimensions90OD/37.5width/17bore,steel,smoothbackside capturedandKBsourcewritten. Internalbearingidentity/ballcountunknown. Nexttensioner/pulley workhasconcreteenvelope.

Cleanup: temporary browser42and43 closed after visual verification; userengine tab13 remains. All CAD jobs terminal.
