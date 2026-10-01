# Timing right contour: independent source and common-corridor feasibility

## Contract

Issues #32/#34; integration owner root, contributor pan_access_resume. Baseline8c2d2d9a1400acf784e04581a61e6a6ede38d3ba, branch engine/timing-drive-fit. Research only; canonical and all candidate solids untouched. Root approved bounded A feasibility before a replacement contour, including main gasket and fasteners. Physical question: does the broad registered lobe result from an indexing/handedness/datum error, and can a source-supported narrower route preserve current gears and pump/pan interfaces?

Owned files: three new scripts `check-timing-right-contour-feasibility.py`, `study-timing-flat-photo-registration.py`, `check-timing-flat-photo-landmarks.py`; their same-named inventory JSON reports; generated `timing-right-contour-feasibility/`, `timing-flat-photo-registration-study/`; this handoff and delivery JSON. No shared API changes. Previous onset and axial studies remain distinct.

Required inputs available locally: primary Fel-Pro outline/holes; original Dorman002/009 correspondence report; actual Dorman009 pixels; corrected cam axis and inherited tip/cavity radii; exact-year timing-cover removal instructions; pump worker's frozen rear contract. Source photos/manual originals are not redistributed.

Preserve main3 Y−6.62794049/Z98.99106944 R9 land X373.8..379.8; pump axisY−32/Z170/R59 opening, R66 housing and local rear modification domainX373..386/Y−25..35/Z90..150; pan terminals and all five relocated lower axes; crank/cam axes, retention and gear envelopes. No station moved. Millimeter YZ feasibility plane; no new local/world asset frames.

## Evidence ledger and findings

| Question | Evidence | Finding / limitation |
|---|---|---|
| Are009 holes misidentified? | Direct grayscale70/100/130 connected-component hole extraction | Seven enclosed holes at every threshold; intended seven-hole order best RMS1.341938px |
| Could reversed/cyclic order fix it? | All14 cyclic/reversed order hypotheses | Next-best RMS69.126756px; simple ordering error rejected. All transforms retained |
| Is the broad silhouette merely a bad primary trace? | 1785 transferred primary-outline samples versus actual009 gasket boundary | Median2px,95th5.099px,max7px; broad asymmetric lobe corroborated independently |
| Does image correspondence prove metric shape? | Existing similarity versus projective fit | No.009 similarity RMS24.946px versus projective1.462px; projection/photography affects metrics. Aperture is out of flange plane |
| Do trace-pick perturbations fix station6? | Four original registration corner cases | Still25.236..62.147mm inboard change to new analytic corridor; systematic parallax remains unbounded |
| Is accessory removal a valid tool state? | Exact1994 timing-cover Service and Repair, removal step3 | Belt and PS/AC/bracket assembly removed before cover screws. This supports service-state tooling; installed-tool failures remain recorded under their original scope |

No front/rear compressor inversion was found in the separate actual STEP axial study. No evidence establishes a40mm compressor relocation or a40mm source-contour correction as a factory dimension.

## Common analytic corridor

At fixed compressor axisY280/Z100 with estimated R65 barrel, define a9mm half-land,6mm wall outside cam cavityR84.947 and crank cavityR44.18, and1mm exterior clearance. These assumptions are explicit feasibility reserves, not newly accepted manufacturing tolerances. The protected pump circle is also included. Both material sides use common analytic circles; no neighbor-shaped Boolean is used.

At station6 Z74.423690 the centerline corridor is Y195.042965..209.495728, width14.452762mm. The existing axisY251.916807 is42.421079mm beyond its upper limit. At Z100 the interval is192.154204..205.000000, width12.845796mm. Positive local intervals show that a mathematical wall/land route could fit. They do **not** prove a continuous source-faithful gasket route, actual hardware fit, station support, retained pan transitions or a pressure seal. Original actual broad rail and station6 failures remain.

## Independent photo-frame hypotheses

Both fits use the independently observed Dorman009 hole coordinates and a terminal-line basis. Neither minimizes compressor overlap.

1. Transfer the crank aperture into009, assume009 near planar, then solve uniform scale solely for the actual-axis cam cavity plus6mm wall and2px edge reserve. This produces scale0.8046227255mm/009pixel and a wider right contour; station6 remains in the compressor region. It also moves protected stations/terminals. **Rejected as a replacement.** Near-planarity is an assumption, and aperture depth parallax is unbounded.
2. Fix actual main3 and mean terminalZ−24.5 instead of trusting the out-of-plane aperture. Uniform scale0.6590972196 narrows station6 toY228.748542/Z60.572719, but the cam guard is excluded by9.737665mm. Even shrinking that guard to the83.947mm tip envelope leaves an exclusion lower bound2.737665mm; this is a circular envelope statement, not an actual tooth-phase Boolean. TerminalY becomes−167.637088..164.003583 and Z−25.551701..−23.547539. **Rejected:** preserved gear/pan interfaces fail. The transferred aperture then disagrees with crank axis by (−14.986213,−1.020608)mm.

Independent pixel comparison now supports the transferred outline to within the recorded errors; it does not verify009 as orthographic. Both hypothesis transforms, original source registration and all rejected correspondence orders are retained. The current data support the broad lobe topology but cannot identify a unique metric correction.

## Actionable boundary for further work

A narrow route can only proceed as an explicit inferred **joint shape revision**, not as a recovered source registration. It must revise common block land/main gasket/cover and station6 together, retain7-hole/open-bottom topology, declare deviations from source silhouette, and preserve the protected pump/pan/retention interfaces. The positive analytic corridor is sufficient to justify a bounded candidate study if root chooses that approximation; it is not sufficient to label it source-faithful. Compare any such curve directly with the frozen registered source and both manufacturer silhouettes.

Alternatively, root can choose the complete compressor/carrier/belt-layout revision from the axial handoff. Existing evidence does not select the dimensional truth of either route. Do not disguise a source conflict by independent block or compressor cuts. Any future tool gate must distinguish installed solid clearance from the explicitly source-defined accessory-removed service state.

## Delivery / reproduction

Commands, from repository root:

```
python3 scripts/check-timing-flat-photo-landmarks.py
python3 scripts/check-timing-right-contour-feasibility.py --render
python3 scripts/study-timing-flat-photo-registration.py
```

System Python/numpy/scipy/Pillow/matplotlib; existing macOS environment. No new CAD exports or package installation. Inputs/results/renders are hash-bound in `inventory/engine/timing-right-contour-source-delivery.json`. Cache warnings used temporary caches, with no production dependency. Model/effort/usage unavailable. Actual generated plots inspected by contributor; root review pending. No asset release URL yet; root packages generated evidence under artifact policy.

## Validation

| Quality gate | Result / scope |
|---|---|
| Application/coverage | PARTIAL: applicable manufacturer comparisons and exact-year procedure; actual installed casting/compressor identity not measured |
| Dimensions/coordinates | FAIL for replacement acceptance: source and protected-datum hypotheses conflict |
| CAD/export | N/A: no replacement solids; analytic sections only |
| Source/visual comparison | PASS for bounded correspondence checks; no metric/factory fidelity claim |
| Installed interfaces | FAIL retained; local corridor feasible, whole revised interface NOT RUN |
| Motion/disassembly | Source removal order documented; actual candidate service tool/motion checks NOT RUN |
| Learning/diagnostics | NOT RUN; no viewer content changes |
| Browser | NOT RUN; no installation |
| Reproduction/review | Reports bind inputs; root review pending |

Wrong correspondence orders and both interface-breaking registrations are explicit negative controls. No production threshold was relaxed. Research is ready for preservation; #32/#34 and installed acceptance remain open. No running process after delivery. Next action: root reviews the source/geometry conflict and chooses whether to authorize an explicitly inferred common contour candidate or broader accessory-layout work.
