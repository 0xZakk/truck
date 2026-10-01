# Online airbox paired-duct specimen — contract

## Contract

Issue #32; worker inclined_linkage_resume; integration owner root. Baseline `d4a4ce94089e148e66d4fc27e91b6d056195baf4`. This is an uninstalled local specimen candidate, not a replacement for the existing airbox/throttle studies. Owned files: this handoff, `cad/engine/online_airbox_duct_specimen.py`, `scripts/check-online-airbox-duct-specimen.py`, `reference/engine/online-airbox-duct-specimen.json`, and its generated folder. Frozen research remains `reference/engine/online-airbox-research.json` and its six KB pages.

Source topology: two unequal tubes, joined web, localized corrugations near large cuffs, four worm-drive clamps and an external open retainer. Actual E7TE molding and seller application are bound in the research ledger. Manufacturing separation of the web/retainer is not established; named CAD regions do not assert a production BOM. No fabricated body bracket or generic shelf is included.

Millimeters. Local X runs from large airbox cuffs toward smaller throttle cuffs; Y separates tubes; Z is the specimen's up direction. This is a display frame, with no parent/world placement. Long projected X extent 559 mm; short 533 mm. These are estimates within the photographed 22 ± 2 and 21 ± 2 inch projected envelopes. They are not hose centerline lengths or installed reach. Both large cuff outer radii 42.5 mm, small radii 28.5 mm, nominal radial wall 3 mm, corrugation rise 5 mm and pitch 12 mm are explicit estimates. Circular sections, a planar bend and piecewise-linear transitions simplify the observed oval/free-state shape. No source-supported insertion diameter is available. Retainer/clamp dimensions are estimated. Parameters are frozen before clearance checks; they must not be tuned to existing engine neighbors.

Interfaces: only local bridge/tube and clamp/cuff surfaces. Clamp band inside radius equals estimated cuff outside radius (idealized contact, no preload). Both tube lumens remain open and separate. The bridge attaches externally without entering a lumen. Existing box tips (OD60) and throttle interfaces (OD48) are NOT claimed compatible with these new estimates. Vehicle installed interfaces and neighboring engine checks are NOT RUN because no body/world frame is established.

Checks: STEP validity/single intended solid per named region; mesh watertightness/winding/positive volume; STEP-to-GLB bounds within 0.05 mm with mm-to-meter Y-up mapping; actual tube mid-plane section probes at every constructed station; lumen/skin controls (deliberately solid cuff and undersized wall); local unintended overlaps above 0.1 mm³. Contact is intentional for bridge/retainer and zero-clearance clamps. Actual exported source-view render, with source URLs and explicit contour limits, precedes integration review. Full continuous flexibility, insertion sealing and removal are NOT RUN.

## Delivery

Pending separate local candidate. Sources are available publicly by URL; originals are excluded. Root independently reviews. No canonical or shared manifest writes. Browser NOT RUN. Learning observations are in the frozen KB notes; no installed lesson is changed. Build command and final hashes will be added after verification. Usage/model accounting unavailable.

## Source comparison and candidate limitations

The actual mesh view is `cad/engine/generated/online-airbox-duct-specimen/source-view-review.png`. Compare its plan view with specimen photo 4 and its oblique view with photos 6/12 at [the identified listing](https://www.ebay.com/itm/196038453283); exact image URLs/hashes are in the frozen research ledger. No source pixels are included in the project render. Matching topology: two unequal branches, localized bellows, long smooth narrow ends, four end clamps, external joining web and protruding retainer. Differences remain: circular rather than observed oval/free-state cuffs; straight circular section lofts rather than a measured molded section; faceted estimated bellows; rectangular web rather than rounded molded outline; simplified clip fingers; no clamp worm thread/slots or molded lettering. These differences are openly retained, not hidden by a collision PASS.

`build()` returns twelve named geometric regions. The web is a region of the molded assembly, not a claim that it was a separately serviced part; same uncertainty applies to retainer construction. Four band/housing regions and four unthreaded screws represent the clamp mechanisms only approximately. The witness `specimen-mm.glb` uses CAD millimeters and is strictly an inspection export; individual runtime GLBs use meters with `(X,Z,-Y)` mapping. Do not load the millimeter witness in the runtime loader.

Exact commands from repository root:

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-online-airbox-duct-specimen.py
MPLCONFIGDIR=/tmp/truck-mpl XDG_CACHE_HOME=/tmp/truck-cache python3 scripts/render-online-airbox-duct-specimen.py
```

CAD uses the pinned Python3.13/build123d0.10 environment. The render uses system Python/NumPy/Matplotlib and adds the existing CAD environment's site-packages for trimesh. No network or original source image is needed to rebuild the candidate or render. Public images remain needed for independent source comparison. Initial checker attempt completed radial probes but hit a Vector indexing bookkeeping exception before pair comparison; the corrected rerun is authoritative. No failed physical result was suppressed by that correction.

| Quality gate | Scoped result / limit |
|---|---|
| Application / coverage | Comparison specimen and exact-year catalog topology support only; owner calibration and exact parts unknown. |
| Dimensions / coordinates | Local mm frame explicit; all candidate dimensions estimated; tape envelopes are broad projected comparisons. |
| CAD / export | Final results in `reference/engine/online-airbox-duct-specimen.json`; no whole-engine acceptance. |
| Source / visual | Actual GLBs rendered and compared to named source views; deviations above retained. |
| Installed interfaces | NOT RUN: no body/world registration or measured cuff fit. |
| Motion / disassembly | NOT RUN: no flexible-material model, clamp preload, insertion or removal study. |
| Learning / diagnostics | Frozen KB observations explain topology and evidence limits; no new repair thresholds or installed lesson. |
| Browser | NOT RUN; previous local browser security limitation retained. |
| Reproduction / review | Inputs and outputs bound in report and render ledger; root review pending. |

This candidate may be preserved as an estimated local specimen. It is not integration-ready and does not close the installed air-cleaner task. Next useful evidence is a registered airbox/body support frame and measured cuff sections; a longer hose cannot solve those missing datums. No shared geometry, IDs or manifests changed.

## Frozen result

Final local candidate: 12 valid single-solid STEP regions; 12 watertight, winding-consistent positive-volume GLB meshes. Nineteen actual potentially overlapping local pairs have zero reported intersection volume; tube-to-tube distance is 9.623810 mm. Four band/cuff contacts, both web/tube contacts and retainer/long-tube contact have zero measured distance. Idealized screw bores have 0.1 mm radial clearance; functional thread engagement remains omitted.

The 3,968 long-tube and 4,224 short-tube actual radial probes completed before the pair-report bookkeeping exception. `completed-probes-recovery.json` binds the exact unchanged tube STEPs and historical checker/log; the final checker reports this as **reused completed evidence**, not newly executed probes. A subsequent pair run found **28.397164 mm³** of estimated retainer finger material inside the long tube. The preserved historical CAD/log retain that failed result. Only the retainer finger underside was trimmed to the actual tube exterior; final local pair checks passed afterward. No tube geometry changed.

Default check command performs the complete fresh build/probes. `--resume-pairs` verifies the recorded historical tube hashes and reuses those probe results while freshly checking meshes, negative controls and all local pairs. The recovery option exists for this recorded run, not as a substitute for validation after tube changes. The negative controls detect a blocked cuff and a 0.5 mm radial wall using the same empty-center/skin predicates.

Root reviewed the actual render and source photographs and accepted preservation as an explicitly estimated local specimen only. Circular cuffs, angular corrugations and rectangular web remain visible deviations. No vehicle installation authorized. Final exact allowlist/hashes: `reference/engine/online-airbox-duct-delivery.json`. No live build process remains. Further work requires the unresolved installation and section evidence; this study does not close the engine issue.
