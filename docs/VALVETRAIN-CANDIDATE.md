# Valvetrain motion candidate — 2026-09-25

This isolated study does not modify the installed engine or declare its valvetrain
finished. Open `/viewer/valvetrain-study.html` to inspect the six-cylinder timing
and solved pushrod/rocker linkage. The source is the locally acquired Melling
SYB-38 replacement table on PDF page13, recorded in
`kb/sources/melling-camshaft-specifications.md`; replacement applicability does not
identify the installed cam.

## Concrete candidate and checks

`viewer/engine-valve-motion.js` provides a720° cycle with cylinder1 firing at0°,
order1–5–3–6–2–4, intake center468° and exhaust center246° relative to each firing.
Those centerlines mean108° after /114° before the exchange TDC. A smooth compact
bump matches .247in peak cam lift and192° duration at .050in. Its270° zero-lift
support is an explicit hypothesis: the advertised checking height is unknown.
It is not a production acceleration law. The flat-tappet cam surface is the
support-function envelope `p=h*n+h'*t`, not a radial polar plot of lift.

The isolated solver checks17,292 half-degree valve poses, exact catalog threshold
crossings,720° periodicity, closed valves at firing and rigid pushrod closure.
The lobe remains convex and its contact offset remains below10.343mm. The CAD
candidate exports a real15mm-wide cam lobe and revised asymmetric rocker into
`cad/engine/candidates/valve-motion/`. Its checker verifies STEP roundtrip
validity and samples flat-follower contact at73 cam angles. These are isolated
checks, not installed cam/head/piston/spring-clearance verification.

## Required integration sequence

1. Retain valve axisY=-16 and pushrod/lifter axisY=90. Move rocker pivot, fulcrum,
   guide and bolt axis fromY36 toY49.230769 to obtain nominal1.6 lever ratio.
   The current lateral ratio is52/54≈0.963. The dedicated rocker candidate retains
   the current overall end extents while moving the pivot and pushrod cup in its
   local frame. Rebuild the matching head pedestal and blind bolt socket, checking
   surrounding ports/galleries and rocker-cover sweep before publication.
2. Reconcile cup and valve-pad Z offsets with the linkage solver. The current CAD
   has cupZ=-8 and a finite lower pad, whereas this isolated solver assumes coplanar
   joint centers at rest. Do not apply its rotations to the candidate rocker STEP
   until this contact geometry is solved. Its226.6mm pushrod length is provisional.
3. Replace twelve union-of-cylinder lobes using the sampled support envelope,
   respecting cam rotation sign, cylinder cycle phases, oil-drive adapter and
   retention journals. Existing lobes are phased but not derived from this law.
   The18mm base-circle radius is an assumption. Current lifter base isZ102 versus
   cam axisZ72: even the candidate maximum radius24.2738mm leaves a gap. Lifter
   placement and pushrod length must therefore be reconciled as a coupled change.
4. Move the entire hydraulic-lifter assembly together for the rigid teaching
   stage; independently retain body/plunger internals and do not claim hydraulic
   pressure simulation. Move valve/keepers/retainer as a rigid set. A spring needs
   regenerated/compressed geometry with coil-bind checks, not rigid translation.
5. Run exact installed sampled STEP checks: cam/lifter, pushrod/head/block,
   rocker/fulcrum/guide/cover, valve/head/piston, spring/retainer/seal. Scope and hash
   those reports to the installed manifest. Only then connect main viewer motion.

## Reproduction

```
node scripts/check-valve-motion-candidate.mjs
.venv-cad/bin/python cad/engine/valve_motion_candidate.py
```

Reports: `inventory/engine/valve-motion-candidate-validation.json` and
`inventory/engine/valve-motion-candidate-cad-validation.json`. Neither changes
whole-engine completion status. The study page is intentionally separate from the
assembly so an assumed motion law cannot silently become installed Ford geometry.


## Installed-coordinate two-station candidate

`cad/engine/valve_station_candidate.py` now creates a separate cylinder1 intake /
exhaust fit study from snapshotted saved STEP neighbors. Its baseline files and
manifest hash are retained in `cad/engine/candidates/valve-station/baseline/`.
This must not be mistaken for the current installed manifest after another build.
The candidate does not overwrite installed solids.

The actual spherical fulcrum center isZ383.5,8mm above the rocker body center.
The new cup center is thereforeZ=-16 in the rocker pivot frame. A12mm-radius
curved valve pad, centred atZ=-1.5, replaces the flat contact patch and gives a
unique tangent point on the flat valve tip. Its1.6 lateral lever ratio is nominal;
the real motion solver includes the cup's vertical offset and finite pushrod.
These contact shapes and dimensions are engineering assumptions, not Ford drawings.

A matching15mm spherical fulcrum plus short annular stem reaches the existing
flat guide. The moved head pedestal retains its original108mm local top: the
head's1.5mm gasket elevation is already in its occurrence transform. Raising the
boss another1.5mm was rejected by QC because it intersected the guide. The blind
bolt socket moves with the boss. Ideal matching spherical surfaces model zero-lash
contact, not a production clearance specification.

The lifter moves down12mm to body-centerZ116, giving cam contact atZ90 with the
assumed18mm base circle. All9 lifter subparts move together. The lower pushrod
ball center becomesZ140.9 and its upper center remainsZ367.5, producing226.6mm
center spacing. Both cup surfaces match the3.8mm pushrod ball radius. Two lobes
on the saved camshaft are replaced with the new profile; the other10 retain their
original geometry. New camshaft geometry is a single solid.

The current static candidate passes154 exact local intersections including the
saved block, head, cover, plug parts and piston. The exported STEP files are the
candidate camshaft, head, rocker, fulcrum, pushrod and lifter cup, plus an assembled
preview. The static and motion reports remain separate; a passed static report
alone never permits a motion claim.

```
.venv-cad/bin/python cad/engine/valve_station_candidate.py
.venv-cad/bin/python scripts/check-valve-station-motion.py
```

The second command checks18 crank poses using exported STEP, with a height-adjusted
6-turn spring helix. It checks the actual cup/pad linkage, cam/lifter contact,
valve/piston/head, rocker/fulcrum/bolt/cover and spring neighbors. Every contact is
checked geometrically as well as for overlap. Read `motion-validation.json` for the
result; no continuous sweep or production spring behavior is implied. First
integration should replace all matching12-station datums together and rerun the
whole-engine audit, rather than mixing two corrected stations with10 old ones.


## Preferred candidate: relocated seats and catalog-constrained peak

Use `cad/engine/valve_layout_candidate.py` and its outputs under
`cad/engine/candidates/valve-layout/`. The earlier valve-station candidate is a
rejected intermediate for motion: it demonstrated that the inherited valve axes
intersected the block bore and that the old pushrod passage fouled the moving rod.
Its rejection report is retained; it must not be published as working motion.

The preferred candidate keeps the axial stations and moves both complete valve
stacks to assumedY=-12. No block material is removed. It uses comparison head
diameters45.2882mm intake /39.5986mm exhaust from MellingV1505/V1504, retaining the
application-note caveat. The existing101.6mm bore then has approximately0.425mm
radial-envelope clearance to the larger intake head. This geometric constraint
sets a plausible layout, not the Ford production station. The Allied underside
photo reviewed on2026-09-25 establishes visible arrangement only. The evidence and
photo are in `reference/engine/valve-layout/`.

The head adapter rebuilds the affected seat/guide regions, with45° mating faces
and a1.8mm contact band inside both factory seat-width ranges. The mouth relief
continues through the chamber; an earlier shorter relief passed closed and peak
checks but failed an intermediate-opening check. The positive interface checker
probes actual material on both sides of16 seat-contact points and verifies the
head→guide→fulcrum→bolt support contacts. Port/chamber surfaces remain assumed.
The stem, keeper, spring free/installed heights and production rocker stamping
are still unresolved; matching a contact model does not verify these components.

A nominal1.6 rest arm ratio does not yield the catalog net lift once the actual
cup/pad vertical offsets and rigid pushrod are included. The candidate therefore
solves the provisional pivotY=51.62143599495mm from .247in cam lift → .395in net
valve lift. The initial lateral arm ratio is≈1.6577 and instantaneous leverage
varies through the cycle. The nominal catalog ratio remains1.6; it is not claimed
to be constant instantaneous leverage. PivotZ383.5, cupZ=-16 and pad-centerZ=-1.5
are assumed construction datums.

### Composable hooks

Call these functions on the **current** saved/rebuilt head and cam, not by replacing
those solids with the baseline STEP. This preserves independently added brackets,
ports and fastener bosses outside the two-station edit regions:

```python
from valve_layout_candidate import head_adapter, cam_adapter
head = head_adapter(head, [intake_x, exhaust_x])
cam = cam_adapter(cam, [intake_x, exhaust_x], firing_deg=0)
```

For all cylinders, pass firing offsets from order1–5–3–6–2–4 at120° intervals.
The cam adapter expects the original cam's local shaft frame; the head adapter
expects the original local head frame, whose installedZ is255.5mm. Repeat on each
pair of stations and run complete installed checks. Never replace the full current
head or cam with a baseline-derived candidate STEP. The `rocker()`, `fulcrum()`,
`pushrod()`, `cup()`, `revised_valve(old,kind)` and `solve(lift,pivot_y=None)` helpers
supply the coordinated geometry and linkage. Occurrence transforms are recorded
in `occurrence-layout.json`. Move each complete valve/retainer/keeper set toY=-12,
all9 lifter internals down12mm, and the guide/fulcrum/bolt to the calibrated pivot.

The cam profile is a periodic B-spline interpolating the1440 sampled support-envelope
points. Its73-pose follower check passes; the3-face lobe replaces the former1442-face
polygonal extrusion. Common analytic contact points are tested against both saved
STEP surfaces, with±0.1mm normal-displacement negative controls. This avoids a
known false nonzero shape-to-shape distance from OCC on trimmed tangent surfaces
without loosening the0.002mm contact or0.1mm³ overlap thresholds.

```
.venv-cad/bin/python cad/engine/valve_layout_candidate.py
.venv-cad/bin/python scripts/check-valve-layout-interfaces.py
.venv-cad/bin/python scripts/check-valve-layout-motion.py
```

Inspect the current `provenance.json`, `interface-validation.json` and
`motion-validation.json` for pass/fail and artifact hashes. Older peak reports
may refer to earlier geometry. Only the current full sweep can authorize a sampled
motion claim, and the whole-engine integration still needs its own QC.

## Frozen all-cylinder motion API handoff

`valve_layout_integration.py` supplies composable all-cylinder head/cam adapters,
idempotent occurrence metadata and corrected rest datums. Apply adapters to the
current installed solids so later head features survive. This is a teaching study;
installed cam identity, production cam curve and valve station coordinates remain unknown.

The sole CAD transform authority is `assembly_math.transforms`: lazily call
`apply_valve_transforms(manifest, poses, degrees)` at its return boundary when
occurrence metadata is present, and set `VALVETRAIN_TRANSFORMS_VERSION = 1`.
The compatibility `moving_transforms` wrapper calls that authority only once.
For assembled STEP export and static/motion placed-shape checks, first obtain
`occurrence_shape(occurrence, definition_shape, degrees)` and then apply the shared
placement. This matters at crank zero: other cylinders already have lifted valves
and compressed springs. Individual spring definition remains its rest geometry.

`viewer/engine-valve-layout.js` exposes equivalent occurrence poses. Reset each
mesh to its manifest pose before applying that frame's motion; never accumulate
rotations. CAD translations map to display `(x,z,-y)`. CAD X-axis rotation remains
display X-axis rotation. The spring mesh generator returns metres in GLB display
axes, for the existing 1000 display scale. Give each spring independent geometry;
its circular wire radius stays constant as helix pitch changes. Apply mechanical
pose before the existing explosion offsets; the assembly marker itself does not
move the assembly group.

`motion-api-validation.json`: 216 Python/JS fixtures, 5,832 comparisons with zero
numerical difference, 18,528 outward-facing triangle checks, constant-wire radius
error below 1.9e-9 metres. This is API/mesh validation, not all-cylinder installed
CAD clearance approval. The isolated two-station CAD candidate retains its prior
18-pose, 1,361-overlap and 180-contact audit. `qc-render.png` was rendered from the
final saved candidate STEP geometry and inspected at rest and peak lift.

Spring-to-seat contact is explicitly unresolved in this stage. The inherited open
helix, 51mm height, 9mm stems and 10mm guide holes are placeholders. The local
factory service specifications call for differing intake/exhaust spring heights
and smaller stem/guide dimensions. Those corrections belong in a separate next
candidate so this passing stage's geometry hashes and evidence remain reproducible.

### Known replacement pushrod conflict — do not promote as accurate geometry

The application-confirmed Melling MPR-306 replacement specification in
`inventory/engine/replacement-specs-2026-09-23.json` gives overall length257.556mm
(10.14in), diameter7.9248mm (0.312in), drilled H&H ends. The first-stage candidate's
ball-center length226.6mm and3.8mm-radius ends give overall length234.2mm, **23.356mm
shorter than that replacement envelope**. Its ball centers are30.956mm shorter
than the catalog overall length; those different measurement conventions must not
be conflated. Correcting the convention does not resolve the23mm physical conflict.
Its7.6mm outside diameter is also undersized by0.3248mm.

This is a known contradiction with available application evidence, not merely a
missing measurement. The candidate remains a mechanically closing teaching study,
not an accurate production valvetrain. The next datum study must solve cam/deck,
lifter cup, actual valve length and rocker cup height together under the sourced
pushrod envelope instead of retaining the current assumed absolute Z coordinates.
The spring/stem candidate separately improves service-range dimensions but retains
those provisional absolute datums and cannot by itself resolve this contradiction.
