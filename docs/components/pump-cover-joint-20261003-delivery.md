# Pump / cover joint common-face research handoff

## Contract and ownership

Engine#47 under#1, coordinated timing cover#32. Worker`pump_functional_junction`; root integrates and reviews. Baseline`0e9d513794e7bab3dfcab45c7da06a669bb44878`. Scope and full proposed pre-CAD contract: [pump-cover-joint-20261003-contract.md](pump-cover-joint-20261003-contract.md). Own only this new prefix; no shared/CAD/frozen/spring edits. Readiness: **research, contract ready for root review; no CAD acceptance**.

The improvement is a common-face pump/cover hole registration instead of separately fixed, contradictory layout estimates. A joint camera fit uses11holes, with the fifth pump aperture held out. Source/measurement uncertainties are explicit. The proposed educational frame preserves crank origin and horizontal pan. OptionB preserves prior source-proportioned cover scale, derives pumpcenterYZ(-22.156967,193.467476), clock-5.641351degrees and transverse mounting-footprint scale1.061626. It does not scale screws, bearings or the whole assembly. Axial98.43mm replacementheight remains separate from transverse scale. No manufacturer metric anchor was found in the same face.

## Evidence and outputs

- Measurements and source hashes: `reference/engine/pump-cover-joint-20261003-measurements.json`.
- Joint fit / independent held-outs / controls: `reference/engine/pump-cover-joint-20261003-joint-fit.json`.
- Exact frame alternatives, axes and dependency list: `reference/engine/pump-cover-joint-20261003-datums.json`.
- Authored source-landmark plot: `reference/engine/pump-cover-joint-20261003-review.png`.
- Proposed educational datum comparison: `reference/engine/pump-cover-joint-20261003-datum-options.png`.
- Contract contains primary ATK2016/Dorman URLs, source identity restrictions and current screw-stack provenance. ATKblockfront, Carterrear and Fel-Pro/Dormanoriginal photographs remain excluded; existing source ledgers retain URLs/hashes. No originals embedded in authored plots.

ATKDFF8 is a listed1987–96 VINY4.9 replacement family; primary catalog also distinguishes its no-exhaust-smog-hole head configuration. This does not settle the owner's emissions calibration. Both exact application gaskets and public cover photos support separate pump/cover block joints, not shared fasteners. Precise pad depths and1994fastener head geometry remain unknown.

## Reproduction

From repository root, after restoring source originals by their existing cited URLs/hashes:

```sh
python3 scripts/pump-cover-joint-20261003-measure.py > reference/engine/pump-cover-joint-20261003-measure.log
python3 scripts/pump-cover-joint-20261003-fit.py > reference/engine/pump-cover-joint-20261003-fit.log
python3 scripts/pump-cover-joint-20261003-datums.py > reference/engine/pump-cover-joint-20261003-datums.log
python3 -m py_compile scripts/pump-cover-joint-20261003-*.py
python3 scripts/pump-cover-joint-20261003-freeze.py --verify
```

SystemPython with NumPy/SciPy/Matplotlib, macOS. Package versions recorded by freeze ledger. Model/effort/usage unavailable. No CADentrypoint/STEP/GLB/release in this research scope. Temporary Matplotlib cache warnings did not prevent plotted output; use a writableMPLCONFIGDIR if needed. No installed package changes.

## Validation and review

| Gate | Result | Evidence and limits |
|---|---|---|
| Application/coverage | PASS bounded research | Primary ATK family/variant and Dorman cross, exact gasket ledgers; not exact truck configuration or factorydimensions. |
| Dimensions/coordinates | PASS relative research; absolute UNKNOWN |11hole fit1.0409pxRMS; withheld fifth2.0415px; leave-one-cover-out0.49–2.99px.400trials selection sensitivity; no calibrated camera or mmreference. |
| CAD/export | NOT RUN | No new CAD. Prior52part export and spring failure remain immutable. |
| Source/visual | PASS bounded research | Actual public source pixels inspected; both authored plots inspected. Carter camera roll remains separate from physical whole-pump clock. |
| Installed interfaces | NOT RUN | Two protected-region conflicts have a source-led replacement layout hypothesis, not a cleared assembly. Current source-independent pad depth estimates retained. |
| Motion/disassembly | NOT RUN | Nominal boss/head radial margin is analytical only; complete socket, withdrawal, actual affected-neighbor checks pending. |
| Learning/diagnostics | N/A | Research contract only, no component learning page changed. |
| Browser | NOT RUN | No shared installation. |
| Reproduction/review | PASS authored freeze; root review pending | Hash ledger and exact scripts; no hidden source redistribution. |

Finite geometric screening: optionA fixedpump-scale/flatpan fails360sample cam+wall margin-1.9242mm. PreferredB fixedcover-global-scale gives+2.3544mm in that same bounded screen, not wholepartPASS. The11hole fit objective never reads clashes. Both swapped-side correspondence and shifted-fifth controls remain reported. Forward crank/cam hubs were excluded as noncoplanar: early apparent~85pxcrank discrepancy is **not** accepted as metric evidence of axis error.

Current stack: pumpseat389, smoothlength31.75→tip357.25; coverseat379.8, historicalcomparisonlength22.225→tip357.575. Their nominal15.75/15.425mmengagement arithmetic is not proof of actual female threads or production hardware. Newpumpframe must carry complete protected3mmbacking, fullR11.5bosses/bores/seats, fifthopening and actualrotorenvelope independently. No carved-cover or shrunk-boss clearance fix.

## Tracking and restart

Issue remains open. Root reviews the frozen contract before CAD. Preferred next scope: isolated optionB joint/casting candidate with explicit new pump footprint, rigidly relocated internal/hardware stack, corresponding block cavity/socket changes and unchanged crank/cam/cover/pan datum conventions. Perform actual affected-neighbor/tool/flow/solid checks, source renders and full mesh QC. Accessory carriers, belt/fan/pulley and hoses need separately recorded endpoint/host consequences; never silently move those anchors. Root owns spring work. No live processes. No new generatedassetarchive required; all authored assets are small and source originals excluded.
