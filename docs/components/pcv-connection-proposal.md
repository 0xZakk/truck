# Component contract and handoff: PCV vacuum-return connection

## Contract

- Issue55 / engine parent1; air-cleaner continuation crosses issue7. Contributor pump_seal_finish; root is integration owner.
- Baseline commit `3e53f117146fe1746ef882abbeabf6542bcba0d2`, branch `engine/intake-exterior-iac-detail`. Exact manifest/relevant-input hashes are in `inventory/engine/pcv-connection-interface-audit.json`.
- Research and read-only interface proposal first. Owned files: this handoff, `reference/engine/pcv-connection-review.json`, `scripts/check-pcv-connection-interfaces.py`, `inventory/engine/pcv-connection-interface-audit.json`. No shared geometry, manifest, IAC artifacts or canonical assets changed.
- Proposed first physical connection: rear PCV valve → upper-intake vacuum-return hose and its receiving interface. This is distinct from the front cover → air-cleaner fresh-air hose. Hose routing, cross section, receiver station and actual valve identity remain unknown.
- Millimeters, existing engine world axes. PCV assembly frame is(-240,-12,416); the existing head's two outlets point toward-Y. These coordinates are model-derived, not production measurements.

## Evidence ledger

All reviewed source files and images are hashed in `reference/engine/pcv-connection-review.json`; owner photographs and purchased/manual artifacts are not redistributed.

| Feature | Evidence | Classification / limit |
|---|---|---|
| Fresh-air endpoints | Exact1994 `PCV Valve Hose / Service and Repair` disconnects the vent connector/hose at cover and air cleaner | Source-supported functional endpoints; page title must not cause this hose to be mistaken for manifold vacuum return |
| Vacuum-return endpoints | Exact1994 `Oil Separator / Service and Repair` disconnects the hose at PCV valve and upper intake | Source-supported missing connection; actual contour/port station unspecified |
| Center branch | Same oil-separator page disconnects an emission-vacuum control hose at the hose center | Must remain in the topology review; not permission to plug it or silently omit its role |
| EVAP applicability | Typical system diagram620350918 and PCV3 conditional instructions | Variant-dependent; not proof the second V219 outlet is unused on this truck |
| Owner's visible front connector | Driver/passenger engine-bay photographs dated2026-09-23 show a black cover connector and descending hose near the oil-fill cap | Truck-specific visible topology; the distant terminal and rear valve/underside manifold joint are obscured |
| Valve identity | Existing V219 replacement exterior and archived PCV part information | Comparison only; installed identity, calibration and second-outlet use unresolved |
| Baffle / unused-outlet cap | No reviewed source exposes these on the owner's valve/cover | Unknown; no fabricated baffle or plug proposed |

The generic vacuum distribution figure explicitly warns that vehicle details differ; it cannot locate this PCV port. Chassis fuel/vapor routing figures establish no hidden engine-side hose contour. Web catalog searches surfaced unrelated V8/industrial examples and were not transferred into geometry.

## Proposed bounded geometry

No receiver or hose geometry is authorized yet. The former lower-outlet/plenum-floor trial is rejected because it does not locate a source-observed manifold connection. The next candidate requires identification of the actual manifold connector and PCV port assignment first. Keep the existing small outlet unchanged and visibly unresolved. The candidate must not claim a sealed or fully reconstructed ventilation system while that outlet and the center emission-vacuum branch remain unresolved.

Existing model outlet centers at the mouth:

- Lower large outlet: (-240,-31,428), bore radius3mm, outward axis-Y.
- Upper small outlet: (-240,-31,440), bore radius2.5mm, outward axis-Y.

Exact small-radius bore witnesses at both mouths have zero obstruction. Their diameters come from provisional `pcv.py`, not a factory dimension.

Rejected trial datum: (-100,25,445), axis+Z through the plenum floor. The existing4mm floor was confirmed by a small obstruction witness, but that geometric feasibility did not establish a real PCV receiver. **Do not model, drill or install this arbitrary receiver.** The recorded probe is historical feasibility evidence only.

New source review locates a shared vacuum tree on the runner-facing plenum wall, centrally between the middle runner roots, in the identified seller specimen. A large hose descends between the runners; its hidden terminal and assignment cannot be established from the current front closeup. The reproduced Ford “TYPICAL4.9L” hose drawing labels an intake manifold connector and a hose assembly associated with the intake, but the available565×409pixel composite does not justify selecting a specific tree nipple. No V8 thread size or hose dimension is transferred from adjacent panels.

Fresh-air alternative: owner's cover-side black connector is visible, but the air-cleaner terminal is concealed/too indistinct in the supplied1024pixel photos to establish both actual end locations. The front-hood-open image adds no detail. Thus a full fresh-air hose is not yet a defensible alternative candidate either.

Required checks: continuous unobstructed lumen through both joints; explicit socket/contact/retention assumptions and positive engagement; receiver passage to actual plenum air; no new blocked runner/port; sleeve/branch collision checks and removal feasibility; wrong-port, blocked-bore and insufficient-engagement controls; exact STEP/GLB binding and actual rendered installed context. If receiver position or secondary-port usage proves incompatible with evidence, revise the proposal before promoting geometry.

## Delivery and validation

Readiness: **research/interface proposal**, not geometry-ready or installed acceptance. Resolve the source-observed receiver and branch assignment before any geometry. No new CAD solids have been generated, so STEP/GLB/export/render/browser gates are NOT RUN, not passed. Calibration/flow/duty-cycle/backfire simulation is outside this bounded proposal.

Reproduce the read-only model audit from repository root:

```sh
.venv-cad/bin/python scripts/check-pcv-connection-interfaces.py
```

Environment: Python3.13/build123d0.10/OCP7.8 on macOS. Report binds relevant STEP files, definitions, occurrences and ancestor transforms; unrelated IAC/manifests changes do not invalidate identical scoped PCV inputs. Source access is locally available but restricted/ignored; reviewers need authorized copies. No release, commit, PR, post or canonical write was made.

| Gate | Result | Limit |
|---|---|---|
| Application/coverage | Reviewed source topology | Actual valve/branch applicability unresolved |
| Dimensions/coordinates | Read-only model audit | All proposed dimensions/stations estimated |
| CAD/export | NOT RUN | No candidate geometry yet |
| Source/visual comparison | Reviewed exact manual diagrams and owner photos | Hidden rear connection and baffle not visible |
| Installed interfaces | Missing receiver documented | No socket or hose accepted |
| Motion/disassembly | NOT RUN | Future hose/receiver candidate required |
| Learning/diagnostics | Routing distinction documented | No repair/calibration claims |
| Browser integration | NOT RUN | Candidate-only scope |
| Reproduction/review | Audit command and source hashes recorded | Root proposal review pending |

## Tracking and restart

Issue55 remains open. Next action: inspect an underside or opposite-side specimen view that traces the PCV hose to its manifold connector, or obtain a legible applicable Ford hose diagram; then select a supported connection. No running process remains after the audit completes. Usage/billing unavailable. Existing six-part valve/grommet study, frozen IAC evidence and all shared files remain untouched.

Additional source distinction: the inspected Ford1987 intake-installation illustration explicitly labels **PCV connector390659-S100 separately from vacuum tree9D496**. Do not attribute the specimen's descending hose to a tree branch without tracing it. Root reviewed gallery7/9/12: no exposed underside endpoint; casting numberRF-F5TE-9425-BA conflicts with treating seller year90 as reliable identification. Its applicability is comparative, not exact1994 proof. Source files remain ignored and hash-addressed in the ledger.


## Source-first endpoint verdict

**Research complete for this bounded pass; no model-ready connection selected.** The inspected Ford drawingP-20657 is explicitly1987 6cylinder300(4.9L)EFI. It confirms rear-cover PCV6A666/grommet6A892 and the return hose curving toward the intake underside behind the runners. It also separately shows front cover filter6A768, fresh-air hose6A664 and air-cleaner termination. This narrows component relationships and front/rear orientation, but its manifold nipple is hidden and supplies no measured station. It does not establish exact1994 branch or hose dimensions.

The specimen gallery does not expose the hidden PCV endpoint, and itsF5TE casting mark preserves a model-year applicability caveat. The clearer1991 CHARM image620012007 could not be viewed; the standalone JustAnswer copy returned403. Neither unseen image nor generated search captions is evidence. The supplied owner photos do not resolve the air-cleaner-side fresh-air terminal well enough to select that full connection as an alternative.

The saved manufacturer V219 photograph visibly includes two small pieces on thin molded links between its outlets. This is a replacement closure-piece research lead; without instructions and truck applicability it does not authorize capping an outlet. No cover baffle is exposed by the reviewed sources.

Next useful evidence is one underside/opposite-side view that traces the PCV hose to its distinct manifold connector, preferably an identifiableE7TZ9424A/1994 specimen, or a legible applicable Ford connector drawing. For the fresh-air alternative, a view showing the actual air-cleaner attachment and its continuity to the front cover connector is required. The existing valve/grommet study and all IAC artifacts remain untouched. No arbitrary port, baffle, plug, hose or shared geometry was created.

Final read-only audit SHA-256 `8015a297786ddb3310ab399cf8fe188e263d8fb11f17c3467345351876238591`; all scoped inputs/source hashes stable. Audit status records the rejected trial and unresolved source endpoint, not an installed acceptance. No process running.
