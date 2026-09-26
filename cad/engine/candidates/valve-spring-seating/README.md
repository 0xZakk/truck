# Spring seating study

Separate second-stage candidate. No installed file mutations and no first-stage
STEP replacements. Reproduce with `cad/engine/valve_spring_seating_candidate.py`
and `scripts/check-valve-spring-seating.py` under `.venv-cad/bin/python`.

Local audit passes257 exact intersections,30 contacts and20 planar-ground-end
checks over5lift values. Exact outside-material tests replace OCC's unreliable
extrema bound on trimmed helix surfaces. Each end has positive planar area and
zero gap to its support. The retained failure report shows the earlier checker
using a stationary crank0piston against unrelated arbitrary lifts; that invalid
combination is excluded from this spring-stack-only audit. Phase-aware piston
clearance remains an integration check. This is not a continuous full-engine proof.

The factory1994service table constrains installed heights41.656mm intake and
37.338mm exhaust, guide bore8.73252mm and selected diametral clearance0.04699mm.
Six turns,4mmwire,26mmmean diameter and end construction are assumptions. Added
seat bosses are generated from inherited floor/retainer heights; absolute casting
geometry remains provisional. No spring-force/coil-bind specification is claimed.

Important: first-stage pushrod overall234.2mm contradicts application-confirmed
MPR-306 length257.556mm. Inherited valve overall109mm also differs from newly
acquired Melling V1505/V1504 comparison lengths120.6246/120.65mm. Resolve the
whole cam/lifter/rocker/valve datum chain before promoting production accuracy.
New manufacturer stem0.342in=8.6868mm nearly matches the derived8.68553mm here;
use the catalog value in the next coordinated dimensional revision.

`qc-render.png` shows actual exported candidate geometry at rest, visually inspected.
Composable hook: `head_adapter(current_head, [intake_x, exhaust_x])` operates in
head definition coordinates; spring positions are `363-INSTALLED[kind]` in the
current provisional installed coordinates. Do not replace an incrementally
modified current head with the saved full-head STEP.
