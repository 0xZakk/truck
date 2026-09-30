# Fixed-stock timing block revision

## Contract

Issue #32, root integration owner. NEW isolated revision after the failed translated-stock trial; old files and reports remain frozen. Historical baseline commit `705c4683c199d8c5e28addba018bc8d1bdd399b1`; active checkpoint `eb502ce755d12fe896b3ea915f3ada4361e52a9c`, branch `engine/timing-interface-reconciliation`; current bound manifest and source hashes recorded in report. No canonical/shared edits or front-land integration.

Only geometry-policy change is retaining the original cam-side stock expression. Tunnel, guides, retention/rear seat and connected drive features retain the prior same-ray estimated 121.8 mm translation, with X references fixed. Additional instrumentation saves before/after shapes for unchanged source rail, filter and carrier features. Source identity, application uncertainty, dimensions and units are inherited explicitly from the first-trial handoff; 121.8 is not a selected factory datum.

Owned new module `timing_block_fixed_stock_candidate.py`, physical interface contract `timing_block_physical_interface_contract.py`, fixed-stock checker/attribution checker, reports, renders and this handoff. Exact zero-delta check and unchanged original 79 masks are mandatory. Physical masks are supplemental and predeclared before inspecting the new build; they cannot erase broad-mask failures.

Proposed supplemental protections: full original side-cover fastener webs; actual sealing-profile region plus explicit 2 mm backing guard; filter seat/face and all fluid ports with explicit 2 mm surrounding guards; entire carrier support bosses; original dipstick/pan and unrelated crank/cylinder/head/accessory masks. These thickness margins are review proposals, not measured production specifications. No later feature is cut in this revision.

## Delivery / reproduction

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-timing-block-fixed-stock-candidate.py
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-timing-block-fixed-stock-attribution.py
```

macOS, Python3.13/build123d0.10.0. Requires restored source STEP artifacts. Outputs `cad/engine/generated/timing-block-fixed-stock-candidate/`. Module API `regenerate(delta=DELTA, stage=None, feature_capture=None)` returns shape/edit counts; observer hooks have no geometric effect. No new dependency installation. Usage/billing unavailable.

## Validation / review

**Completed failed diagnostic, preserved.** Exact feature-local ablation compares each feature's before/after on identical incoming stock, identifies added material inside new tunnel/guides, and tests persistence in the final block. Prospective final-machining removals are intersected with predeclared physical guards without exporting or applying any cut block. Four journals receive exact support-shell volume comparisons and radial samples every5° at three axial sections; samples locate deficient regions but do not prove continuous full support.

No installed acceptance; source/production fidelity estimated. Browser NOT RUN because this is isolated and root reports browser security block. No new bosses, blind neighbor subtraction, hidden bore fills, altered protected thresholds or scope expansion. Root alone later combines front land. Report concrete results before requesting approval of any final-machining contract.

## Tracking

Issue #32 remains open. Finish fixed-stock and source-feature attribution diagnostics; preserve broad and physical failures. Next machining revision requires root review. No fixed-stock diagnostic processes remain. Root has authorized a NEW explicit rear-seat construction repair before considering machining; original invalid results remain frozen.


## Completed results

- Zero-delta baseline difference0; fixed-stock geometry changes only the approved stock policy relative to first trial. Original79 masks:75 pass,4 fail (side-cover removed6554.808031, carrierX292 removed419.799752, carrierX340 removed323.003516, pan socket8 added0.004783591 mm³). No mask relaxed.
- Actual fixed gasket and cover overlaps are now both zero. All original side rail and bolt-web material stays unchanged. Direct rendered mesh and actual side sections viewed by worker.
- CAD validity FAIL begins at rear-seat operation. Local reconstruction returns `BRepCheck_InvalidImbricationOfWires` on the cam tunnel face. All saved STEP readbacks are valid, but direct GLB has144 nonmanifold edges and original CAD is invalid. No repaired/round-tripped geometry replaces this trial.
- Repeated instrumented original-CAD versus valid STEP Boolean symmetric difference returns20070396.356643 mm³. This is a failed equivalence check on invalid topology, not evidence of a valid repeat. Downstream valid STEP measurements are diagnostic and do not validate the original builder.
- Exact before/after feature attribution: rail adds1831.731349 mm³ into guides; filter adds7559.923192 mm³ into tunnel; carrier adds854.220211 mm³ into tunnel and31.032502 into front guide. Ordered trace additionally identifies5082.816565 mm³ tunnel intrusion from connected oil-drive feature. Source functions/operands remain unmodified.
- Predeclared91 physical masks:90 unchanged, pan socket8 fails by0.004783591 mm³. Hypothetical final machining would preserve89 masks but cut entire protected carrier supports: X292 tunnel427.110105 +guide31.032502 mm³, X340 tunnel427.110106 mm³. No final machining applied. Carrier support redesign needs coordinated review, not blanket approval.
- Journal thin-shell support volumes (of184.051184 mm³ each): X−334145.337988, X−110148.759792, X110161.186299, X360.5143.853145. Every center section lacks sampled support at angles330..355 and0..30° about+Y toward+Z. Additional missing angles195..240° occur at journal1 front sampleX−323.1 and journal4centerX360.5. Exact missing-shell STEP witnesses and bounds are in support-regions report; they are diagnostic regions, not proposed full bosses.

Reports: `timing-block-fixed-stock-validation.json`, `timing-block-fixed-stock-attribution.json`, `timing-block-fixed-stock-core-validation.json`, `timing-block-fixed-stock-side-cover.json`, `timing-block-fixed-stock-validity.json`, `timing-block-fixed-stock-feature-order.json`, `timing-block-fixed-stock-rear-seat.json`, `timing-block-fixed-stock-support-regions.json` under `inventory/engine/`. Each dedicated checker shares its report stem; `check-timing-block-fixed-stock-candidate.py` produces the main validation report. Render commands: `render-timing-block-fixed-stock-candidate.py`, `render-timing-block-fixed-stock-side-cover.py`, `render-timing-block-fixed-stock-support.py` using system Python/Matplotlib and CAD subprocess extraction. All generated artifacts remain in the fixed-stock directory.

Quality verdict: candidate research only; CAD/export FAIL, support FAIL, interfaces FAIL, production source fidelity unresolved, motion/install/browser NOT RUN. No canonical changes, learned-content changes or part-count promotion. All missing material and topology failures remain visible for root review.
