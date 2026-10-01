# Component handoff: corrected combined-motion review

## Contract before checks

Issue #32, root integration owner. Baseline `1440853952cd132e17693c6355c38bcb0f9276b4`; branch subsequently advanced to `engine/timing-drive-fit` after PR103. Own NEW `cad/engine/engine_corrected_combined_candidate.py`, `scripts/check-engine-corrected-combined-motion.py`, `inventory/engine/engine-corrected-combined-motion-validation.json`, this handoff and `cad/engine/generated/engine-corrected-combined-candidate/`. Frozen corrected cam/crank/helper reports remain unchanged. No canonical mutation.

Inputs: root corrected crank, corrected cam and scoped linkage API, frozen 58/29 timing core, crest rocker, inclined head/gasket, expanded-seat block v3 (`66917915...`) and pan v2 (`d7f495ec...`), plus preserved rod/piston definitions and actual fixed covers. Block/pan unresolved aggregate gates remain unresolved here. Crossed distributor/oil-drive region remains pending the other worker; no compatibility acceptance by this snapshot.

Planned bounded coverage: rebind existing continuous cam/crank radial and cam/rod/piston support proofs only after fresh actual new-shape containment and unchanged local-part/frame verification. Reversed/reflected event phase traverses the same complete rod motion set, so the frozen Lipschitz lower bounds can transfer if all defining geometry and station slices remain valid. Verify a phase-independent cam/block support if possible, and declared source-derived crank swept stock against current block/pan; an overlapping conservative stock is inconclusive and triggers focused actual pose checks, never an automatic real-conflict verdict. Check actual rod-group constituents at six critical local phases per cylinder against block/pan with bounds prefiltering; finite coverage only. Evaluate piston/valve vertical gap across declared sampled cycle and check actual worst poses where needed. Reuse crest/head/cover event-pose evidence at nominal axial registration only when actual inputs and unchanged upper-linkage transform law match. Produce a selected, named actual combined STEP snapshot plus pose/asset manifest for root integration.

Thresholds: inherited support containment <1e-5 mm³; stationary actual-pair overlap >0.1 mm³ is a candidate conflict requiring strict material witness. Positive shape distance and separate bounds are recorded. No lowering thresholds to accept a failed support. Inject shifted-axis/enlarged-stock or translated-part controls. Coverage and omissions must be explicit. No exhaustive whole-engine/brute-force or continuous whole-neighbor claim; browser NOT RUN.

## Evidence and delivery

This is an uninstalled diagnostic candidate under engine #32. Stable occurrence IDs and millimeter world coordinates are preserved; no replacement part identity or production dimension is asserted. Assembly manifest SHA-256: `91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6`. Contributor: inclined-linkage worker; integration owner: root. The frozen source-supported/estimated classifications of every input remain unchanged.

Entry point `engine_corrected_combined_candidate.load()` returns the selected manifest/shapes/source mapping; `frames(manifest, event_degrees, axial_mm)` supplies corrected world poses. The crank uses actual measured physical rest phases from the corrected-crank report. Upper linkage uses the frozen cam state law. Axial cam domain is −0.1..0 mm. The snapshot is event 55°, axial 0. No installed inventory, viewer, dimensions, source geometry or shared transforms changed.

Owned companion files also include `scripts/export-engine-corrected-combined-snapshot.py`, `scripts/check-engine-corrected-rod-bolt-conflict.py`, `scripts/render-engine-corrected-combined.py`, `scripts/bind-engine-corrected-combined-delivery.py` and corresponding `inventory/engine/engine-corrected-*` reports. All generated outputs reside in `cad/engine/generated/engine-corrected-combined-candidate/`.

**Mechanical result: FAIL, inherited rod-bolt head/block interference.** Six cylinder samples each overlap by 2.716027965 mm³ at local physical crank angle 55°. A strict interior witness lies in actual bolt-head stock and actual block stock. The original canonical block and original motion at 55° reproduce exactly the same overlap as the revised block and corrected event 305° for cylinder 1. Actual bolt source replay and local old/new block differences are zero. A focused 45..65° scan finds 13.345377973 mm³ at its 45° endpoint; this is not a global maximum. Neither the estimated bolt nor the estimated R98 crankcase is silently changed.

Fresh continuous conservative supports establish crank/block/pan clearance, cam/block/pan clearance, cam/crank clearance ≥8.631748 mm, and piston/cam lateral clearance ≥18.687925 mm. Frozen cam/rod whole-motion certificates transfer only after unchanged local inputs, exact motion-set reparameterization, and new cam section containment; minimum bound 4.657228 mm. The initial crank swept support omitted the rear flywheel register, failed containment by 2473.596295 mm³, and is retained separately. Adding the source-defined register to the diagnostic support repaired that proof without changing any component.

Rod/block/pan coverage is 576 pair samples at six local physical crank phases per cylinder, with 384 exact CAD comparisons after bounds exclusion. Piston/valve coverage is 721 event samples × 6 cylinders × 2 valve kinds × both axial endpoints plus 12 actual minimum-pose CAD checks; minimum sampled vertical gap is 6.737085 mm. These finite samples are not whole-motion neighbor acceptance. The prior nominal upper-linkage contact law remains unchanged; a full upper-linkage check against the latest block is not supplied here.

The usable export is `combined-q55-named.step` (SHA-256 `1bb3b288c2a1b3b165b89404d3baa6a92f153f68c2186b68dc48e75dbd86759c`), with 328 unique occurrence names, valid single solids and maximum roundtrip bounds error 2.14e-11 mm. Its layout is `combined-q55-layout.json`. The initial `combined-q55.step` is retained as REJECTED: shared topology caused only 51 distinct exported names. The named-export sidecar supersedes that naming failure only; the mechanical FAIL remains. The existing assembly export helper's copy-before-placement convention fixes occurrence identity.

`combined-motion-review.png` shows actual exported moving meshes and the actual intersecting bolt/block section. The worker inspected it on 2026-10-01: crank/rod/piston poses and cam/upper-linkage arrangement are coherent; the highlighted section exposes the inherited head collision. This image is a CAD diagnostic, not a photograph or factory-fidelity comparison.

## Reproduction and gates

From repository root, with existing `.venv-cad` (Python 3.13.12, build123d 0.10.0, OCP 7.8.1.1.post1; macOS 15.6.1 arm64):

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-engine-corrected-combined-motion.py --supports
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-engine-corrected-combined-motion.py --triage --piston-valves --snapshot
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/export-engine-corrected-combined-snapshot.py
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-engine-corrected-rod-bolt-conflict.py
PYTHONPATH=.venv-cad/lib/python3.13/site-packages MPLCONFIGDIR=/tmp/truck-mpl XDG_CACHE_HOME=/tmp/truck-cache python3 scripts/render-engine-corrected-combined.py
python3 scripts/bind-engine-corrected-combined-delivery.py
```

Temporary cache locations contain no required evidence. Inputs must be restored from the repository's artifact policy/releases before reproduction. No additional packages were installed. Model/effort and token billing are unavailable.

| Gate | Result | Evidence / limitation |
|---|---|---|
| Application/coverage | Scoped candidate | Existing #32 inputs; no new factory claim |
| Dimensions/coordinates | PASS scoped | Actual rest axes, unchanged dimensions, explicit world transforms |
| CAD/export | PASS revised export | Named-export report; original naming failure retained |
| Source/visual comparison | Limited | Actual CAD image inspected; bolt and cavity remain estimates |
| Installed interfaces | FAIL | Six witnessed rod-bolt/block samples; unchanged baseline reproduction |
| Motion/disassembly | Partial / FAIL | Continuous supports and finite checks distinguished; no disassembly study |
| Learning/diagnostics | PASS diagnostic | Failure source replay and actual section; no installed lesson migration |
| Browser integration | NOT RUN | No canonical installation |
| Reproduction/review | PASS integrity only | Delivery binder rechecks recorded input/artifact hashes |

Crossed-drive teeth/phase compatibility remains pending the independent composed-cam delivery. Compressed valve springs, continuous rod/block/pan clearance, full latest-block upper-linkage neighbors and the rest of the engine are omitted. This candidate cannot close #32 or support an all-engine collision-free claim. Code/diagnostic archival may proceed independently of installation acceptance.

Next action: source/datum audit of rod bolt, head, press-fit shoulder, mating rod boss and crankcase before a bounded replacement contract. No clearance-only block carving. No process remains running; root owns board/PR integration and final review.
