# ACT host multi-view registration delivery

## Result and scope

**No installed ACT pose is accepted.** The completed bounded fit gives a useful casting correction: the first upper-port interval consistently fits shorter than the remaining intervals. It also demonstrates that the current camera/shape assumptions do not satisfy the independent head/sensor landmarks. No host CAD, manifest, sensor transform, candidate stage or neighbor geometry was edited or used as an objective.

Issue82/system1; baseline4f1fe9da2ec177e1ff61668df66ca422e37b0b7c; branch `engine/source-host-interfaces-20261002`; contributor `act_second_view`, integration owner root. Research-only scope and pre-fit assumptions/change are in `act-host-registration-20261003-contract.md`. Root reviewed source views before authorizing this stage. Source package `act-host-secondview-20261003-delivery.json` remains unchanged. No commit/PR made by worker.

## Method and evidence

Three actual1600×1200 photographs of identified castingRF-E7TE-9K461-A5E provide six upper apertures each, seven staggered upper holes, six head-port center estimates and two exterior sensor landmarks. Source URL/hash ledger and restoration script are in the preceding delivery. ACT identity remains visual/location comparison, not a readable sensor number.

Connected dark aperture components are reduced to64 outer-boundary samples each after filling interior bright islands. Three extraction thresholds120/140/160 test this choice. Projected-circle conics use signed pixel-distance approximations; camera fits never substitute ellipse centers for the contour. Initial radial threshold extraction was rejected after actual overlays exposed internal reflections and an escaped boundary; its failure summary is retained. The final original-overlay was actually inspected locally.

Equal-upper-pitch model:36 shared variables (three7-parameter perspective cameras, common circle radius, seven planar holeXY pairs). Free-upper-station model:40 variables, adding four shared intermediate longitudinal port positions. Both models fix upper endpoints0/568.96 only as a numerical scale gauge. The free model does **not** assert113.792mm actual upper spacing. Cameras assume centered principal point(800,600), square pixels and zero distortion, with focal bounds300–15,000px; all explicit numerical choices remain estimates.

Each equal single-view initialization uses12 starts (three initial focals900/1800/3600 and four signed tilts), followed by three shared fits testing tilt branches. The free fit restarts from those three shared camera solutions. Each threshold has its own results. The seventh hole in view5 is withheld. Head and sensor points are withheld from all camera/upper casting fits. After freezing cameras, a six-parameter equally spaced head row is fitted directly in image space; six separately triangulated head centers are also retained. This does not force the existing25mm head offset or flange separation.

## Numerical outcome

All errors below are pixels. Head value is maximum Euclidean error over18 held-out head landmarks. Sensor values are maximum Euclidean errors across the three views, not coordinate RMS. The frozen acceptance budget is8px per landmark.

| Model / threshold | Withheld flange hole | Head equal-row maximum | Sensor base maximum | Connector maximum |
|---|---:|---:|---:|---:|
| Equal /120 |26.74|209.04|119.94|106.02|
| Equal /140 |7.75|54.57|29.79|21.62|
| Equal /160 |26.39|145.43|96.36|94.67|
| Free /120 |34.05|115.07|54.98|46.12|
| Free /140 |5.09|20.96|16.76|10.78|
| Free /160 |28.61|85.83|38.62|30.86|

The middle free run improves the withheld flange prediction, but both head and sensor checks still fail. Its small fitted-circle residual cannot override those failures. One of three shared starts in each free threshold run reaches its400-evaluation limit; the other two report convergence. The preferred equal140 run also reaches that limit. The free120 view5 focal hits its15,000px bound; other thresholds give materially different focals. None establishes camera calibration.

The first interval divided by the mean of the other four is0.8672/0.8857/0.8643 across thresholds. This is **conditional source-registration evidence of unequal upper stations**, not a measured factory ratio or instruction to immediately change the host. Equal upper spacing is a suspect modeling assumption; cylinder/head pitch must not be silently equated with upper-flange pitch.

The three inferred sensor axes differ by as much as24.975°. Their temporary-frame components are retained only to diagnose failed fits; they are not candidate engine vectors. Head-row projection failure rejects metric normalization to113.792mm. Thread gauge, engagement, penetration, connector roll and exact exterior landmark centers remain unknown. No clearance study or repeated single-view nullspace demonstration was substituted for this fit.

## Deliverables and reproduction

- Scripts: `act-host-registration-20261003-fit.py` (equal), `...-free.py` (free stations), `...-review.py` (held-out review and authored plots).
- Evidence reports: matching `reference/engine/...-fit.json`, `...-free.json`, `...-fit-review.json`, `...-free-review.json`; include input/script hashes, full camera/contour results and multi-start outcomes.
- Distributable plots: `reference/engine/...-fit.png`, `...-free.png`; authored landmarks/fit lines only, no original pixels.
- Rejected extraction summary: `reference/engine/...-rejected-extraction.json`.
- Actual local source-overlay: `/tmp/act-host-registration-20261003-free-overlay.png`, excluded from distribution. Recreate using `--images` and `--local-overlay`; this path is a review convenience, not a required dependency.

```sh
python3 scripts/act-host-secondview-20261003-fetch.py --directory /path/outside/repository --download
OPENBLAS_NUM_THREADS=1 python3 scripts/act-host-registration-20261003-fit.py --images /path/outside/repository
OPENBLAS_NUM_THREADS=1 python3 scripts/act-host-registration-20261003-free.py
MPLCONFIGDIR=/path/to/writable/cache python3 scripts/act-host-registration-20261003-review.py --report reference/engine/act-host-registration-20261003-fit.json
MPLCONFIGDIR=/path/to/writable/cache python3 scripts/act-host-registration-20261003-review.py --report reference/engine/act-host-registration-20261003-free.json
```

The free script consumes the preserved equal fit; source originals are only needed to replay extraction/equal fitting. Review scripts need no originals for source-free figures. Runtime Python/NumPy/SciPy/Pillow/Matplotlib versions are captured in the delivery manifest. Fits may differ at floating-point precision; compare residuals and failure verdicts, not a claimed factory datum. Model/effort and usage unavailable. All processes finished.

## Validation and review

| Gate | Status | Reason |
|---|---|---|
| Application/coverage | PASS qualified | Prior actual casting identity inspection; exact truck/sensor identity caveats retained |
| Source contour review | PASS scoped | Actual original-overlay inspected; first failed extractor recorded/corrected |
| Camera/dimensions/coordinates | FAIL | Independent head/sensor residuals exceed8px; focal/axis sensitivity |
| Control sensitivity | PASS scoped | Withheld-hole+20pxX negative control is reported; middle free baseline5.09px passes and shifted case rejects |
| CAD/export | N/A | No geometry generated |
| Installed interfaces | NOT RUN | No accepted receiver or pose |
| Motion/disassembly | NOT RUN | No installed candidate |
| Learning/evidence | PASS bounded | Unequal upper-station atomic note, source/model limits preserved |
| Browser | NOT RUN | Research-only |
| Reproduction | PASS local | Input/script hashes, complete numeric reports and authored figures |
| Independent root review | PENDING | Review delivery/plots/failures before further work |

Preserve as research; issue82 remains open. The concrete next task is source-informed manifold station revision and improved camera evidence (clear end view or calibrated flange dimensions), or an explicitly bounded camera model review that addresses the recorded discrepancies. Do not start ACT host CAD from these failed axes. No owner-photo dependency or background-work claim.
