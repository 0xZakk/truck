# Component contract and handoff: inclined valvetrain neighbor motion

## Contract

- Assigned engine issue #32; root integration owner accepted the earlier scoped uninstalled candidate and requested broader neighbor motion checks. Baseline branch `engine/timing-clearance-revisions`, commit `4e480f8e40458384986b9e1792597e87e56daad7`; frozen candidate and earlier reports remain unchanged.
- Research/checker-only scope. Own new `scripts/check-timing-valvetrain-inclined-neighbors.py`, `inventory/engine/timing-valvetrain-inclined-neighbors-validation.json`, this handoff and separate diagnostic renders if needed. No geometry edits, no canonical writes, no installation.
- Inputs: actual exported inclined rocker/head/block/gasket and canonical rod/valve/lifter/spring/retainer/keeper/seal/cover/hardware STEP plus manifest and frozen candidate poses. Hash every actual source/shape. World millimeters, current explicit frames unchanged.
- Stage1 triage: cylinder1 intake/exhaust at their event-relative rest(-150 crank) and maximum-lift(0) poses, axial0; targets rocker/pushrod/lifter-body/valve against head/block/cover/gasket, own branch spring/retainer/keepers/seal/mounting hardware, and neighboring branches. Reject positive exact overlaps above0.1 mm³; independently seek strict interior witnesses for reported conflicts. Expected tangent contacts are not automatically excluded from overlap checks.
- Stage2 only after triage: all twelve branches at five event-relative phases(-150,-96,0,96,150) and both axial endpoints0/-0.1. This is120 target-branch poses, not continuous motion. Adjacent-branch separation can be certified continuously by preserved X intervals because all present motion is translation inYZ and rotation aboutX with fixed stationX. No X-axis axial shift is applied to these branches by the inherited linkage contract.
- Springs: frozen poses intentionally do not deform rest spring STEP. Actual spring STEP is checked at rest; dynamic spring clearance uses a conservative annular envelopeR11–15 from the actual seat to installedHeight minus unscaled valve lift. Envelope intersections are inconclusive, not physical collisions; then detailed dynamic spring CAD is required. Existing generator rejects lifts above10.0330001 mm, below inclined exhaust peak10.033202687, so no silent clipping/scaling or source edits are allowed. No force/rate claim.
- Critical controls: deliberately move the actual rocker into a known solid cover region and require a strict interior witness/positive intersection; move an adjacent-branch envelope into the targetX interval and require the separating bound to fail. Track actual CAD bound separation separately from exact Boolean tests and preserve Boolean failures/uncertain results.
- Existing thresholds retained:0.1 mm³ overlap,0.002 mm contact where checked. Positive envelope overlap is only a request for refinement. CAD geometry is estimated; physical factory clearances are unknown.

## Delivery / validation / restart

Pending bounded triage. All broad-motion checks presently NOT RUN; previous scoped candidate reports retain their separate accepted scope. Source comparison, production valve timing, disassembly and browser remain out of this checker and NOT RUN. No model/effort or usage figures available. Next command: `.venv-cad/bin/python scripts/check-timing-valvetrain-inclined-neighbors.py --triage`. No previous files will be changed.

## Delivered triage — physical valve-cover conflict

Stage1 completed with **FAIL physical conflicts found**. Stage2 was not launched because a real roof collision already blocks the candidate. Earlier lower-passage acceptance is unaffected and remains scoped; it does not establish cover clearance.

- Cylinder1 intake, crank468°, axial0: exact overlap **95.423338559624 mm³**. Point **(259.48,91.295322017261,410.443621163490) mm** is strictly inside both the reimported rocker and cover solids.
- Cylinder1 exhaust, crank246°, axial0: exact overlap **95.418426989712 mm³**. Point **(309.48,91.296989191754,410.443276048080) mm** is strictly inside both solids.
- Intake common bounds areX250.98–267.98,Y85.743593482–94.178925283,Z410–411.330863490 mm. The modeled cover roof begins atZ410 and ends at413; the peak rocker penetrates that roof. This does not establish a real truck clearance or a factory cover height.
- Rest(-150° event-relative) is clear for both tested branches. The two peak samples fail. Of248 declared pair comparisons,154 separate by actual bounding boxes and94 receive exact CAD common tests. Two physical conflicts and zero spring-envelope refinement requests are recorded. Other twelve-branch dynamic collisions are not certified by this triage.
- All66 cross-branch interval pairs have a positive invariant X gap, minimum **7.5566 mm**. Because the current linkage has fixed stationX and onlyYZ translation/X rotation, this is a conservative continuous separating bound for the included branch parts under the current contract. It does not cover unrelated engine systems or a revised axial-motion law.
- Controls pass: shifting a verified clear rest rocker upward10 mm creates925.510617938 mm³ overlap and a strict interior witness. Translating actual neighboring X intervals to a common minimum produces a negative separating gap of-39.5986 mm. These use actual bounds/solids, not invented fault results.

Reports: `inventory/engine/timing-valvetrain-inclined-neighbors-validation.json` and `inventory/engine/timing-valvetrain-inclined-neighbors-render-validation.json`. The worker inspected `cad/engine/generated/timing-valvetrain-inclined-neighbors/rocker-cover-conflict.png`: actual exported rest/peak rocker and cover sections with the exact common region shown in red. No source-photo comparison is claimed. The initial report construction needed a stronger witness search and a verified clear-to-fault cover control; final completed checker uses actual common-solid centers independently tested against both inputs.

Commands:

```sh
.venv-cad/bin/python scripts/check-timing-valvetrain-inclined-neighbors.py --triage
PYTHONPATH=.venv-cad/lib/python3.13/site-packages MPLCONFIGDIR=/tmp/truck-mpl XDG_CACHE_HOME=/tmp/truck-cache python3 scripts/render-timing-valvetrain-inclined-neighbors.py
```

The non-triage command (omit `--triage`) declares120 target-branch poses, but is **NOT RUN**. It must not be reported as passed or used to overwrite this failure before a separately authorized revision exists.

## Spring limitation and next work

This checker did not animate undeformed rest springs or clip exhaust lift. The declared annular envelope clears the tested moving parts. Actual compressed-spring CAD, seat/retainer contact and minimum coil gap across the declared lift range are **NOT RUN**. Root has allowed a future isolated wrapper with unchanged spring geometry law to extend the previous nominal parameter guard through the actual10.033202687 mm exhaust peak, if needed; frozen spring helpers must remain unchanged. That guard is presently a helper-domain limit, not evidence of physical coil bind. No spring force or rate is inferred.

Root must select a source-informed rocker/cover interface follow-up before any geometry changes. Possible variables must be researched and bounded; this checker does not authorize thinning the rocker, raising the cover, reducing valve lift or shortening the rod. Once an approved revision exists, rerun triage and then the declared broader sweep, with actual spring contact/coil checks added as needed.

| Gate | Verdict |
|---|---|
| Application/source geometry | Estimated inherited model; production fidelity unresolved |
| Coordinates/input binding | PASS actual STEP/source hashes, unchanged poses |
| CAD/export | N/A no new solids exported; existing STEP inputs are read only |
| Visual review | PASS actual conflict section inspected; source comparison NOT RUN |
| Installed interfaces/motion | FAIL sampled roof collision; only adjacent-branch X separation is continuous |
| Spring detailed motion | NOT RUN; conservative envelope is not a compressed-spring contact certificate |
| Learning | N/A checker-only research |
| Browser/disassembly | NOT RUN, no browser attempt |
| Reproduction | PASS completed report, checker, image and explicit commands; root review pending |

Issue #32 remains open. No prior source/report/geometry files or canonical assets changed. No processes remain running. New Python files pass syntax compilation. Usage unavailable; no background continuation claim.
