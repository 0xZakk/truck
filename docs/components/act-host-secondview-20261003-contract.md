# ACT host second-view specimen contract

## Contract

- Issue82 under system1; contributor `act_second_view`, integration owner root. Baseline `4f1fe9da2ec177e1ff61668df66ca422e37b0b7c`, shared focused branch `engine/source-host-interfaces-20261002`. Root alone handles Git, tracking and shared integration.
- Research only: identified public casting photographs and a bounded registration proposal. No CAD, sensor-pose, frozen candidate, manifest, builder or clearance changes. Owned prefix `act-host-secondview-20261003` in docs/components, reference/engine, scripts, KB source/note/raw.
- Canonical manifest SHA256 `91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6` is context from current state; no assembly acceptance rerun.
- Interface owner remains `efi-lower-intake`; sensor local+Z runs probe→connector. Millimeter world placement remains unassigned. Preserve six runners, head/upper flange, seven upper studs, injectors and three rail supports. Actual specimen dimensions are not inferred from neighbor clearances.
- Inputs: prior `act-host-online-20261002-contract.md`, `act-host-estimate-20261002-delivery.md`, host `cad/engine/efi_intake.py`, identified specimen gallery. No owner photo or purchased manual dependency for this new delivery. Prior exact-year evidence supports ACT station independently.

## Evidence ledger and actual visual finding

The gallery at <https://www.ebay.com/itm/197661687342> shows a physical lower intake. **View11 clearly reads RF-E7TE-9K461-A5E**, matching the seller title. Treat this engineering casting number separately from service E7TZ9424D in the current model. The seller's compatibility table includes unrelated4.6/5.4L V8s, so it does not independently verify1994 application.

Views1,3,5,6,9 show a light keyed electrical connector, metal hex and mounting boss projecting from the front terminal runner's lateral side near the head end. It appears consistent with ACT at the prior service location, rather than a plain vacuum fitting. **No readable sensor number, exposed probe or female bore proves exact sensor identity or thread geometry.** Do not assume the existing replacement specimen is the item in the photograph.

Views1 and5 provide different elevations of the upper/head side; view6 adds obliquity. Six circular upper ports, staggered flange holes, head ports, rail bosses, rear asymmetric opening and shield attachments can be matched. Backside views4,7,8 show different surfaces but conceal the ACT. These are multiple views of one specimen, independent of the service drawing; they are not independent specimens or a calibrated near-orthogonal stereo pair.

All ten full1600×1200 images were inspected. Exact URLs, hashes, sizes and observations are in `reference/engine/act-host-secondview-20261003-evidence.json`. Best local review conveniences are `/tmp/act-host-secondview-20261003-view1.webp` (overview), `...-view5.webp` (lower elevation/head flange), `...-view6.webp` (oblique), and `...-view11.webp` (casting identity). These temporary paths are conveniences only; the fetch script restores exact pixels into any caller-selected directory. Originals must remain outside Git and distributed archives.

## Frozen proposal for bounded multi-view registration

This source contract freezes the following **next task**, not a fitted result:

1. Use views1/5/6. Define a specimen frame with upper port1 center as origin; longitudinal axis follows port1→port6; upper machined flange defines the plane and normal; transverse axis completes the frame toward the head flange. Register that frame to the existing manifold's first upper center, runner direction and upper-flange plane. The service location and rear asymmetric opening fix front/rear; reject a mirrored solution.
2. Scale by the existing explicitly provisional113.792mm consecutive-runner pitch. Do not call it a measured casting dimension. Fit upper port contours as common circles and the staggered bolt-hole pattern in their shared plane, with separate perspective cameras per image. Six port centers alone are nearly collinear and cannot identify a planar camera; contour samples and off-line holes are required. Camera principal point/image center, lens distortion zero and image square pixels would be declared assumptions; compare constrained and free focal estimates before accepting a fit.
3. Hold out the head-port centers and at least one upper flange hole per view. Use head-port plane orientation and both flange traces to test camera/geometry consistency. Existing circular head ports differ from the photograph's noncircular head openings; fit their centers/plane separately and do not silently reshape the manifold to fit a camera. The existing25mm longitudinal head offset and flange separation are model assumptions, not photographic calibration.
4. Once cameras have independent flange support, use visible sensor hex/base center and connector center in all three images to estimate an axis line in the specimen frame. The ledger preserves manual pixel seeds only; repick full contours at native resolution. Initial±8px picking budget is a proposed review threshold, not a factory tolerance. Freeze all fitted cameras/scale before evaluating engine neighbors; clearance must never be an objective.
5. Accept a bounded estimate only if held-out landmark residuals stay within the predeclared8px budget, alternative camera starts produce the same axis/center within a separately declared modeling budget, and axis/boss projections agree in every view. Otherwise preserve the concrete camera/shape mismatch and seek a direct end view. No repeat single-image nullspace exercise is required. No port penetration/gauge depth or connector roll can be obtained merely by fitting the visible axis.

An accepted fit would authorize only a separately reviewed host boss/port candidate; probe exposure, host stock, actual sensor contact, female thread/gauge, seven studs, injector/rail interfaces, wrench/removal and installed neighbors remain mandatory. No transform or installation is proposed in this delivery.

## Delivery and commands

Research ready for root source review; no commit/PR made. Files comprise this contract, JSON evidence, authored capture, KB source/atomic note/raw and fetch verifier. Source→atomic-note pipeline completed; root owns global semantic processing. No parametric geometry API, STEP, GLB or CAD render applies to research-only scope.

```sh
python3 tools/ingest.py reference/engine/act-host-secondview-20261003-capture.txt --type local --title act-host-secondview-20261003-casting
python3 scripts/act-host-secondview-20261003-fetch.py --directory /path/outside/repository --download
python3 scripts/act-host-secondview-20261003-fetch.py --directory /path/outside/repository
```

Direct listing fetch returned an eBay error page; web reader exposed the listing and gallery URLs; CDN fetch succeeded. A second listing257569855998 had a search hit but failed web open and was not used. GitHub issue read failed due sandbox network; root retains issue ownership. No repeated blocked-host loop. macOS/Python3 and Pillow used for metadata/inspection; model/effort and usage unavailable.

## Validation and review

| Gate | Status | Evidence / limitation |
|---|---|---|
| Application/coverage | PASS qualified comparison | Actual casting identifier and six-runner specimen; exact-year fitment not reverified |
| Dimensions/coordinates | NOT RUN | No camera/metric fit; explicit next-task assumptions above |
| CAD/export | N/A | Research-only, no geometry generated |
| Visual source review | PASS source inspection | Ten actual image views inspected and hash bound; no CAD fidelity claim |
| Installed interfaces | NOT RUN | No host port or installed sensor transform |
| Motion/disassembly | NOT RUN | No installed candidate |
| Learning/evidence | PASS bounded | Source→atomic note with identity/metric limits; no new diagnostic claims |
| Browser integration | NOT RUN | Research-only delivery |
| Reproduction | PASS local | Ten stored originals verified against ledger; public URL restoration provided |
| Independent review | PENDING | Root must inspect named views and contract |

This improves physical topology/registration evidence and is suitable for preservation as research. Issue82 stays open. Next action: root review views1/5/6/11, then authorize a separate bounded camera registration or prioritize a clearer end view. No active background process; no engine changes or acceptance claims.
