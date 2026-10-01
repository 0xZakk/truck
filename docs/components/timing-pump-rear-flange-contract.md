# Component contract and handoff: timing-pump-rear-flange-contract

## Contract

Issue32/47 coordinated front interfaces; pump_foot_resume proposes, root integrates. Baseline8c2d2d9a1400acf784e04581a61e6a6ede38d3ba, engine/timing-drive-fit. This is an analytical feasibility contract with in-memory diagnostic geometry, **not exported replacement assets or accepted factory geometry**. Original shell/front-joint/v2/2692/main7/pan21 failures remain frozen. No private/canonical manifest or existing CAD file changes.

Owned files: this handoff; scripts/check-timing-pump-rear-contract-preflight.py; inventory/engine/timing-pump-rear-contract-preflight.json; generated/timing-pump-rear-contract-preflight/. Coordinates and all numerical dimensions below are estimated millimeter engineering hypotheses. Scope is rear cover/pump/gasket only. Forward inlet remains a separate known conflict.

## Applicable evidence and shared datums

The1994 service text identifies a removable pump attached by bolts, with its fan/pulley and hoses separate. It provides no rear footprint dimensions. The exact-year timing-cover text identifies a replaceable gasket and front crank seal but gives no metric flange outline. Ford1986 4.9L external exploded Figure10, PDF62/printed21-11-9, was re-viewed beside Figure10A's key: pump29/8501, cover2/6019 and front gasket3/6020 register against the block front. The drawing groups a pump-ring and lower cover-gasket outline; it is a historical illustration and does not establish1994 one-piece gasket ownership, metric scale or offset. The applicable Fel-Pro13816 pump gasket and TCS45829/45830 cover kit images support retaining the separately modeled physical gasket identities.

Ford PDF URL and SHA are preserved in `reference/engine/ford-1986-main-cover-fastener-comparison.json`; original SHA6be1705f0675e07c6c124d91fabee82e877696ea26e36aeaf8d6c0b87d534ea0 reverified. Original PDF/pages are excluded from delivery. Source images can be reacquired from ledger URLs and reviewed atPDF62/63. The front photo of ATKDFF8 supports separate pump and timing interfaces on the block; perspective/parallax prevents measuring the needed offset. The original Ford exploded drawing and the block photograph support the architecture but do not settle the exact1994 casting contour.

|Interface|Retained value|Evidence class / reason|
|---|---|---|
|Crank/cam/gear/seal frames|Existing fitted core and2692 stage|Bound candidate interfaces; unchanged|
|Seven main-cover axes, headseats, cavities|Existing seven-fastener candidate|Source-positioned holes with estimated registration; protected in full|
|Pump shaft/hub/impeller axis|Y−32/Z170|Inherited estimate retained to avoid introducing belt/fan/shaft changes|
|Pump block seat / gasket / casting rear|X373 /373..375 /375|Source-supported direct-block architecture, estimated axial registration/thickness|
|Pump rear bore / housing radius|R59 /R66|Inherited estimates; retained exactly|
|Four pump mounting axes and fifth aperture|Existing installed pattern|Applicable replacement topology; coordinates unmeasured and unchanged|
|Cover-to-block seat / main gasket|X373 /373..373.8|Retained estimated registration; positive actual contact required|

## Concrete bounded correction proposed

The weaker features are the **estimated outer flange widths and lug caps**, not the fixed hole or rotating-axis datums. Use the same algebraic construction for both owners; do not subtract an actual neighboring solid.

1. At the lower pump mount (worldY−24.3/Z103.5), retain the completeR8.75 cylindrical support region and existingR4.3 clearance bore. Remove only the portion of the oldR11.5 lug annulus outsideR8.75 **and outside** the retained pump-axisR66 cylinder, overX375..389. TheR66 exclusion preserves the existing chamber-side stock; this is an exterior lug-cap refinement, not a claim that the full resulting boss becomes a pureR8.75 cylinder.
2. At the matching pump-gasket lug, replace only its oldR9.5 external cap beyondR8.75 and outside the existingR65 gasket outer disk, overX373..375. Retain theR5.2 hole. The completeR8.75 support radius gives a nominal3.55mm radial gasket ligament at the lower hole; it is an estimated geometric requirement, not a pressure/strength specification.
3. Define a shared analytical separation boundary about the unchanged pump axis: radius66.25mm, clipped toX373..386,Y−25..35,Z90..150. Remove this boundary's interior only from the current timing cover and its main gasket. It gives0.25mm geometric separation from theR66 rear housing and1.25mm from theR65 pump-gasket ring. No block, pump bore, gear, seal, pan or main-hole center is moved or cut.
4. Leave the existing block face intact. Both narrowed gasket footprints remain on their existing block backing; the removed sliver becomes external dry face between two distinct gaskets. No functional wet passage is assigned to the sliver. No assertion of deeper coolant-jacket correctness is added.

Why the protected datums can coexist: main-hole3 is75.405634mm from the pump axis, leaving0.155634mm between itsR9 rear-land guard and the newR66.25 boundary. Its axis is18.238206mm from the lower pump axis;R9+R8.75 requires17.75mm. These are narrow but positive **estimated** layout margins, not manufacturing tolerances. The thin nominal separation makes this suitable only for a bounded candidate pending better dimensions, not installation approval.

## Preflight acceptance and required full candidate gates

The existing diagnostic preflight builds these exact analytic masks in memory. It exports section curves only; no replacementSTEP/GLB or installer is supplied. Final report records all input hashes and measured outcomes. Full candidate authorization must retain:

- Actual rear housing/cover and both gasket intersections≤0.1mm³; all original witnesses must remain positive controls against the unchanged baseline.
- All seven mainR9 rear lands unchanged, actual headseats/threads/floors and screw contacts unchanged. Head/tool clearances require direct checks, not just the radial estimate above.
- All four actual pump screws clear, complete lower headseat supported, bore and fifth aperture preserved; actual pump gasket upper/lower backing and full annular support required.
- Continuous main gasket strip, unchanged hole count/terminal topology, full backing. The preliminary transverse width samples are diagnostics only, not a certified global minimum sealing width.
- Exact changed stock confined to the declared masks; no neighbor Boolean used as a cutter; complete source bore, impeller, shaft and main/core/seal interfaces unchanged.
- Valid connected solids and watertight direct exports, plus actual assembled and section renders.
- Forward inlet conflict remains FAIL and cannot be removed by reclassifying this rear-only pass. Full private stage remains incomplete.

## Delivery / reproduction / tracking

Run `.venv-cad/bin/python scripts/check-timing-pump-rear-contract-preflight.py`. EnvironmentmacOS/Python3.13.12/build123d0.10.0. Required frozen local inputs and hashes are listed in its report; restore through existing artifact policy. Source originals are not redistributed. No canonical/private-stage edits. Root review and explicit bounded candidate decision remain next. Browser NOT RUN; flow/strength/production fidelity NOT RUN; no installation claim. Usage unavailable.

## Frozen preflight outcome

Report `inventory/engine/timing-pump-rear-contract-preflight.json`, SHA256 `db053b894617c4b988243aceca7501e256d5bddb72a75f52dd5cbbeb5a23fa70`:

- Rear housing/cover overlap0; cover/pump-gasket overlap0; main/pump-gasket overlap0. Source failures remain in the prior datum-audit report.
- Removed material in all sevenR9 main rear-land guards0; removed material in pumpR59 bore and full lowerR8.75 support guard0.
- Actual main screw3/pump overlap0 and lower pump screw/housing overlap0. Other hardware and full headseat/tool support still require full candidate checks.
- Main gasket contact: block11506.165723mm², cover11552.755964mm²; pump gasket contact: block/housing2877.391093mm² each. These all-face contact metrics are not a pressure calculation.
- Seven transverse samples atZ112/115/120/125/130/135/140 retain14.5..19.5mm projectedY material span,0.05mm sampling. This is not a global minimum width proof.
- All four trial parts remain valid and one connected solid. Diagnostic removed volumes: cover1021.209352, main gasket67.068957, housing1356.782498, pump gasket50.717360mm³ (default integrator estimates; final candidate must retain metric method/limits).

Source review ledger `reference/engine/timing-pump-rear-flange-contract-review.json`, SHA256 `d17a4395b7772f623a25bada8978a1fe5c4a5086e1e2660eb88d56ba8b2df354`, binds the exact-year service text, historical Ford review and replacement-source ledgers. Actual before/after sections reviewed at `cad/engine/generated/timing-pump-rear-contract-preflight/sections-review.png`, SHA256 `2c88fc7f8b67a3e111ad14a7c69906e20962ca3c87f20a42079dca4f20c2fb26`. Reproduce with `MPLCONFIGDIR=/tmp/truck-gear-mpl python3 scripts/render-timing-pump-rear-contract.py`. Original source images are not embedded in the distributable figure.

Verdict: feasible bounded estimated rear-only correction proposed for root decision. Full changed-contact, tool, continuous strip, STEP/GLB and installation gates remain pending. No existing geometry or manifest was modified; no processes remain running.
