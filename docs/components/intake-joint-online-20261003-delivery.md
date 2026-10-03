# Intake joint independent gasket evidence

## Result

**An applicable replacement gasket independently supports revising the joint's equal-spacing assumption and aperture pattern. No exact millimeter layout is established.** Fel-Pro MS93838 is identified by the manufacturer catalog for the relevant4.9MFI application. Its actual product photo has six large apertures and nine small apertures, including two paired locations. The shorter terminal interval is approximately0.894 of the mean of the other four in the image.

This is useful research for a coordinated `efi-upper-intake` / `efi-lower-intake` / `efi-upper-intake-gasket` / upper-fastener layout revision. No geometry, transform, shared metadata or frozen ACT study was changed. Seven retaining fasteners remain the prior service-supported quantity; nine gasket apertures do **not** mean nine bolts. The two extra aperture functions are unassigned. Actual casting photos show two protruding features at corresponding paired locations, but their hardware class and dimensions remain unresolved.

## Contract and source ledger

Issue82/system1 intake dependency; contributor `act_second_view`, root integration owner; baseline4f1fe9da2ec177e1ff61668df66ca422e37b0b7c; focused shared branch `engine/source-host-interfaces-20261002`. Research-only scope, ownership and checks were recorded before extraction in `intake-joint-online-20261003-contract.md`. Units here are pixels/dimensionless ratios; CAD mm/origin/transform are unassigned. No parametric CAD API, STEP or GLB applies.

| Claim | Evidence / classification | Limit |
|---|---|---|
| F1502WD4.9 VINY model applicability | Fel-Pro master catalog PDF305/printed279, visually inspected | Replacement application, not owner's installed brand |
| MS93838 upper joint | Same catalog PDF354/printed328, engine42 | No drawing dimensions or gasket thickness |
| Six large/nine small apertures | Actual1500×1500 identified MS93838 image linked from its product page | Retailer-hosted product photo; manufacturer-original authorship unverified |
| Short terminal interval | Independent photo extraction, three topology-valid thresholds | Dimensionless image proportion; no factory tolerance |
| ACT/front end mapping | Paired small holes, opposite terminal ears and shorter interval compared with identified casting | Inferred right photo end; no FRONT mark, opposite-face viewing possible |
| Physical length/spacing | Unknown | Reseller packaging dimensions deliberately excluded |

Manufacturer catalog: <https://www.drivparts.com/content/dam/marketing/North-America/catalogs/fel-pro/pdf/fel-pro-master-gasket-900-16.pdf>. Product: <https://www.carid.com/fel-pro/upper-fuel-injection-plenum-gasket-set-mpn-ms-93838.html>. Actual image: <https://images.carid.com/fel-pro/items/ms-93838.jpg>. Exact hashes, sizes, access outcomes and leads are in `reference/engine/intake-joint-online-20261003-evidence.json`.

Local root-review conveniences: `/tmp/intake-joint-online-20261003-ms93838.jpg`, `/tmp/intake-joint-online-20261003-catalog305.png`, `/tmp/intake-joint-online-20261003-catalog354.png`. All were actually viewed. Originals and rendered source pages are excluded from Git/archives. Public URLs plus SHA256 values support reacquisition without personal credentials; no owner photo dependency.

## Measurement and meaning

The image threshold selects the connected gasket silhouette, fills its holes and labels enclosed white apertures. Expected topology is six large openings plus nine small ones. A threshold150 extraction only recovered four large openings and is explicitly rejected. Thresholds180/210/235 recover6+9; their short-gap/other-gap-mean ratios are0.894019/0.893410/0.893802. This narrow numerical extraction spread is **not** a manufacturing tolerance or camera calibration.

Large-aperture centers are projected onto their fitted image row. The measurement JSON preserves pixel centers, moment-axis ratios, all small-hole centers, interval lengths and normalized front-to-rear stations. The authored landmark figure contains only reconstructed center markers and labels, not source pixels. No camera optimization was rerun, and no photographic package length was converted to a part dimension.

The gasket result and earlier casting fit both support a shorter end interval. Their different numerical ratios must not be averaged into a specification; each has different projection and shape assumptions. Future geometry must use one coordinated interface contract for both castings, gasket, seven fasteners and the two additional aperture interfaces. Gasket clearance openings do not directly equal casting bore diameters or sealing lands. A ruler/dimensioned drawing or an explicitly accepted global scale estimate is still required for millimeters.

## Delivery, reproduction and checks

Owned files: contract/delivery, evidence JSON, measurement script/report, authored landmark PNG, two observation captures, two KB source pages and two atomic notes; normalized raw captures follow the KB pipeline. Root handles shared embedding and Git/PR. The delivery hash ledger records runtime and all authored members. No commit/PR or asset publication by worker.

```sh
curl -L 'https://images.carid.com/fel-pro/items/ms-93838.jpg' -o /path/outside/repository/ms93838.jpg
MPLCONFIGDIR=/path/to/writable/cache python3 scripts/intake-joint-online-20261003-measure.py --image /path/outside/repository/ms93838.jpg
curl -L 'https://www.drivparts.com/content/dam/marketing/North-America/catalogs/fel-pro/pdf/fel-pro-master-gasket-900-16.pdf' -o /path/outside/repository/felpro.pdf
pdftoppm -f 305 -singlefile -r 120 -png /path/outside/repository/felpro.pdf /path/outside/repository/catalog305
pdftoppm -f 354 -singlefile -r 120 -png /path/outside/repository/felpro.pdf /path/outside/repository/catalog354
```

Verify reacquired SHA256 against the evidence ledger before using changed source pixels. macOS/Python/NumPy/SciPy/Pillow/Matplotlib and Poppler used; actual package versions captured in delivery ledger. Model/effort and usage unavailable. MAHLE secondary cross-reference was a lead only: its catalog download returned HTML, so no unsupported second manufacturer verification is claimed. Other failed hosts are recorded without repeated retries.

| Gate | Status | Scope |
|---|---|---|
| Application | PASS replacement | Actual manufacturer catalog pages inspected |
| Photo/topology | PASS scoped | Actual six-port/nine-hole product photo inspected |
| Dimensionless extraction | PASS scoped | Three6+9 runs; malformed4+9 segmentation rejected |
| Metric coordinates/thickness | NOT VERIFIED | No physical scale or dimensioned outline |
| CAD/export | N/A | Research only |
| Installed interface/contact | NOT RUN | No candidate geometry |
| Motion/disassembly | NOT RUN | No installed candidate |
| Learning/evidence | PASS scoped | Two source→atomic-note chains; limits stated |
| Browser | NOT RUN | No installed changes |
| Reproduction | PASS local | Script/input hashes, reports, authored diagram |
| Root independent review | PENDING | Review identified image, catalog pages and aperture roles |

Research is ready for preservation; issue82 and coordinated intake scope remain open. Next action: root reviews the6+9 pattern and end mapping, then defines a shared joint layout contract with physical scale and extra-hole roles explicitly estimated or sourced. No numerical ACT axes promoted, no background process remains.
