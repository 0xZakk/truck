# Component contract and handoff: bounded rocker crest candidate

## Contract and evidence

- Issue #32, root integration owner; branch `engine/timing-clearance-revisions`, baseline `4e480f8e40458384986b9e1792597e87e56daad7`. Root approved a separately bounded crest study after the actual roof collision. Own new `timing_rocker_crest_candidate.py`, dedicated checks/reports/render and this handoff only. Old failed rocker, reports, cover and canonical assets stay frozen.
- Research/candidate, not source-accurate production geometry. The exact-model Fig24 rocker assembly (source ledger `reference/engine/oil-fill-neck-review.json`, image hash `e8d649d620ad2f789983e1ba37a36ec0a62a90917803d10ceb59bd2e23c9b1d0`) was inspected: a formed open trough, separate fulcrum, guide and attachment bolt. It supplies no scale, stamping thickness, socket backing dimension or upper crest height. Restricted original is not copied or redistributed.
- `valve_source_layout.py:rocker` creates an unmeasured8 mm-thick solid pushrod-end profile, a broad approximation of that anatomy. `valve_cover.py` explicitly calls its roof/offsets visual clearance assumptions; local roof35 mm/world410 and3 mm thickness are not measured. The old cover report certifies only static clearance against older inputs. Current transforms are internally consistent; no evidence proves the cover or rocker datum physically correct for the truck.
- Current primary replacement comparison [EngineQuest EQ-VC300N](https://enginequest.com/product/ford-valve-cover-4-9-300-87-to-98-new/) reviewed2026-10-01 lists1987–1998 Ford4.9L, tall filler neck and C5AZ6582K/F1TZ6582C interchange, but no internal roof dimensions. [Melling valve-train overview](https://melling.com/aftermarket/valve-train/) distinguishes stamped/cast designs generally and supplies no applicable thickness. No numerical dimension is transferred from these pages.

## Alternatives and selected bounded hypothesis

1. Raise/reshape the cover roof: unresolved source dimensions and potential intake, filler/PCV and sealing-interface consequences. Not selected; an arbitrary upward move would hide uncertainty and alter unrelated established interfaces.
2. Change lifter/rod/valve/pivot datums or lift: conflicts with the frozen source-sized lengths, contact geometry and keyed phase contract. Not selected.
3. Reduce estimated material only above the pushrod socket: smallest affected part/interface scope. Select a **2 mm crest reduction** in the existing educational approximation, changing the unmeasured8 mm end-profile thickness to6 mm with a taper into the original upper surface at localY20. This is an explicit geometric study, not a manufacturer dimension or strength certificate. The source figure supports a non-block-like formed rocker but does not establish this particular reduction.

The local removal mask isX[-8.6,8.6],Y[20,45.205263216],Z[-2.5,10.114385932] mm in the frozen rocker frame. Added material must be zero. The complete fulcrumR15.05 neighborhood, socketRball+0.05 neighborhood centered(0,39.105263216,-1.385614069), valve pad patch and actual socket backing cap must remain unchanged or meet the separately declared backing bound. No contact surface, lower beam, fastener relief, cover or transform changes.

Declare minimum **4 mm of modeled backing above the socket sphere's top**, at the socket axis, and a preserved continuous diskR2 through that4 mm vertical thickness. This is a conservative CAD material-continuity check, not stress/fatigue or production design validation. Compute actual candidate distance from sphere top to crest and verify cap material, not only contact-neighborhood equality. Surface topology, forming radii and oil path remain inherited approximations.

## Planned checks

- Build from the exact frozen inclined rocker STEP. One valid connected solid, zero addition and exact removal containment at1e-5 mm³.
- Exact protected contact neighborhoods; socket backing axial thickness and solid-cap probe; STEP roundtrip and GLB watertight/bounds checks.
- Actual exported rest/peak poses for all twelve branches and both axial endpoints;0.1 mm³ collision and0.002 mm contact thresholds. Retain old peak overlap as a negative control. Independent point/shape probes around the old failed region.
- Full crank sample of numeric top bounds (integer0–720, both endpoints, all branches) may conservatively separate the entire rocker from the cover roof plane but does not prove side-wall clearance. Actual bounded contact/neighbor sweep only after local gates pass. Never treat a top-plane bound as whole-cover proof.
- Actual section/old-new contour render, worker inspection and independent root review. No source-original composite redistribution.

## Delivery and restart

Pending construction; installed acceptance, structural capacity, exact source comparison, broader spring/cover sweep and browser NOT RUN. Frozen failures remain authoritative for their exact inputs. Next command will be `.venv-cad/bin/python scripts/check-timing-rocker-crest-candidate.py`. Model/effort and usage unavailable.

## Delivery — scoped uninstalled candidate

The selected crest revision passes its declared local and sampled-neighbor gates. It remains **candidate**, not accepted installed or production-correct. Source review is preserved in `reference/engine/timing-rocker-crest-source-review.json`, including actual local source hashes and current primary-page retrieval limits. All prior failed rockers/cover reports and canonical geometry remain untouched.

- Entry point `cad/engine/timing_rocker_crest_candidate.py:build(old=None)` returns a rocker in its unchanged local frame, starting from the frozen inclined rocker STEP. The former `c.poses` and all other part definitions remain unchanged. Do not call a whole-engine builder to apply this study.
- Outputs: `cad/engine/generated/timing-rocker-crest-candidate/rocker-arm.step`, `.glb`, `rocker-crest-cover-comparison.png`, plus separate `intake-spring-peak.step` / `exhaust-spring-peak.step` study poses. These spring poses are not replacement canonical definitions.
- The worker inspected the actual exported old/new rest/peak section. The image uses the same X slice for both rockers: only the declared upper crest/taper differs; the new peak clears the unchanged roof. No restricted source image was copied into the output.
- Final report index: `inventory/engine/timing-rocker-crest-delivery-validation.json` binds all four component reports, complete transitive local CAD source imports, source-review record and actual STEP/GLB/PNG hashes. Root handles the next private artifact checkpoint; publication URL is not yet available.

Run from repository root:

```sh
.venv-cad/bin/python scripts/check-timing-rocker-crest-candidate.py
.venv-cad/bin/python scripts/check-timing-rocker-crest-neighbors.py
.venv-cad/bin/python scripts/check-timing-rocker-crest-springs.py
PYTHONPATH=.venv-cad/lib/python3.13/site-packages MPLCONFIGDIR=/tmp/truck-mpl XDG_CACHE_HOME=/tmp/truck-cache python3 scripts/render-timing-rocker-crest-candidate.py
.venv-cad/bin/python scripts/check-timing-rocker-crest-delivery.py
```

Existing macOS Python3.13/build123d0.10.0 environment; no dependency changes. Public pages were read through the web tool; source page-body hashes are unavailable and not invented. The saved local diagram hash remains a source access dependency, not a redistributed original.

| Gate | Result and limits |
|---|---|
| Source/application | Source-informed hypothesis only; exact crest thickness, cover height, production shape and structural capacity unknown |
| Coordinates/kinematics | PASS unchanged source-sized rods/valves, frozen pivot/ball/valve axes and unscaled lift law |
| Material change | PASS698.789474675 mm³ removed, zero added, zero removed outside declared mask |
| Contact preservation | PASS exact zero symmetric difference in socket, fulcrum and valve-pad neighborhoods |
| Socket backing | PASS4.5376 mm axial distance from sphere top to crest; the R2×4 mm cap above the socket contains50.265482457 mm³ with zero missing material. This certifies that declared cap, not a global wall minimum around the open socket mouth or fatigue capacity |
| CAD/export | PASS single valid STEP with roundtrip check; watertight3,602-triangle GLB, maximum bounds error0.000000375 mm |
| Fixed-cover rest/peak | PASS48 actual exported poses: twelve branches × rest/peak × two axial endpoints; minimum distance0.643426562 mm; old-rocker peak overlap remains a failing control |
| Broader neighbors | PASS120 target-branch poses,7,440 pair comparisons:4,776 bounding-box separations and2,664 exact tests; zero physical conflicts or spring-envelope refinement requests |
| Adjacent branches | PASS66 invariant X-interval separations, minimum7.5566 mm; continuous only under the frozen fixed-X/YZ-motion contract |
| Actual springs | PASS60 sampled seat/retainer levels: all twelve stations × five scalar lifts. Rest regenerated spring solids match imported canonical STEP by zero symmetric difference. Actual guard extended from10.0330001 to10.033202786604 mm via one AST constant; geometry law and4 mm wire unchanged |
| Ideal spring coil spacing | PASS continuous lift-range bound for the assumed constant-pitch helix: minimum wire gaps intake1.259561697 mm, exhaust0.543752772 mm. Pitch monotonically decreases with compression, so the minimum is at declared peak. This is not production coil-bind, spring-force or stress evidence |
| Controls | PASS old crest collision; clear rocker raised10 mm hits roof; shifted branch interval overlaps; spring raised0.1 mm opens0.1 mm seat gap; compressed3.9 mm pitch gives negative0.1 mm same-angle wire gap |
| Visual fidelity | Actual exported geometry inspected; still a simplified solid profile, not a faithful formed trough; manufacturer dimensional comparison NOT RUN |
| Full continuous motion/disassembly | NOT RUN; finite phase samples do not certify every intermediate crank/axial phase or staged removal |
| Thread/whole engine/browser | True thread engagement unresolved; unrelated engine neighbors and combined installation/browser NOT RUN |

The spring checker uses actual event-relative rest retainer frames before applying scalar lift; absolute crank0 is not rest for every branch. Conservative operand bounding-box volume bounds handle tangency where the upper bound is already below0.1 mm³, retaining the existing threshold. Adaptive Boolean integration is still required for larger possible intersections; no failed integral is silently reported as zero. In the completed run54 spring comparisons were certified by that conservative bound and no volume-measurement fallback was needed. These distinctions are recorded in the report.

The source evidence cannot decide whether the real truck's rocker crest or cover height differs from the model. This candidate selects the smaller isolated correction, preserves all established interfaces and reports the uncertainty. It must not be promoted as factory geometry merely because it clears the current cover.

Root review and artifact preservation are the next actions. Issue #32 remains open. New-file Python syntax passes; no canonical navigation content changed, so navigation was not rerun for this isolated candidate. All worker processes have finished; usage/billing unavailable, no continued background work claimed.
