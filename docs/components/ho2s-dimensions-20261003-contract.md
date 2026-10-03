# Pre-CAD dimension contract: identified Bosch HO2S exterior

## Contract and ownership

Issue #82 under engine #1; contributor `airbox_screw_finish`, integration owner root. Continuation of the frozen `ho2s-online-20261003` research. Baseline remains `6b14e88527295d56ef234113ccc3065c57db4e3b` for inherited source scope; root serializes branch changes on `engine/source-host-interfaces-20261002`. No manifest read or edited; hash N/A.

Own only `ho2s-dimensions-20261003*` docs/reference/KB files. No edits to the nine frozen prior files, shared index, CAD or viewer. Task is a concrete estimated exterior dimension contract, not a thread drawing or installed model. Public originals stay excluded; no generated STEP/GLB or release archive is required.

Identity remains Bosch 15718/0258005718, qualified replacement for the prior Ford F4UZ-9F472-C source chain. Four future electrical contacts retain unknown cavity mapping. Exhaust-pipe/bung host, parent transform, installed connector frame, hot-neighbor clearances and lead route remain absent. This contract does not authorize a manifold placement.

## Primary-source results

NTK's 2019 manufacturer catalog PDF 529/printed 530 explicitly maps Bosch 15718 to 22503, alongside other alternatives; its guide-only interchange caveat applies. Actual PDF 258/printed 259 illustrates 22503 and specifies558 mm lead length. The NTK shell/protection-tube appearance differs from the Bosch target. The reviewed catalog contains no mounting pitch or diameter specification; the bridge is useful for a future NTK technical sheet, not for transferring every dimension.

Bosch's 15729 universal product page supplies 22 mm hex and a 25.8 in sealing-surface/connector length, but no thread pitch. Its linked `F00HL00055IN00WHCO0000.PDF` is a harness-connection instruction sheet and does not close that gap. No generic LSM11, package-size or retail listing is promoted to target-primary dimensional evidence. Exact captures/URLs/hashes are in `reference/engine/ho2s-dimensions-20261003-evidence.json`.

## Projection method and uncertainty

The actual manufacturer side photo is 1400×1400 px, SHA256 `1773573055fbf53cd0d7f742e5f51ab869dc9a564f2066786fe02391619a92b2`. Front/rear photos were used to identify features, not to assume a shared calibrated camera. Pixel origin is top-left; explicit endpoints are in `ho2s-dimensions-20261003-landmarks.json`.

The primary 22 mm hex is the sole metric anchor. Its vertical silhouette is picked as 302±6 px. Depending on rotation, a regular22 mm-AF hex may present22–25.403 mm across its silhouette. Scale bounds before camera sensitivity are therefore 22/308 to25.403/296 mm/px. The central scale averages those physical widths over 302 px; it is not a measured camera solution.

Additional **analyst-selected sensitivity scenarios** are relative depth scale 0.95–1.05 and axis tilt 0–20° for the sensor; the separate connector uses 0.85–1.15 and 0–35°. Axial lengths divide by the cosine of tilt; radial spans do not. Manual-pick allowances are listed per feature. These scenarios are not calibrated uncertainty, factory tolerances, guaranteed physical bounds or a statistical confidence interval. They assume uniform image scaling; a distorted/composited marketing photograph can violate that assumption. Rows are correlated through the common scale, so extremes must not be assembled independently as if every feature had independent tolerance.

The three visible crest picks are X 1104,1122,1137 px, giving two complete intervals and a mean 16.5 px. The resulting 0.984–1.774 mm sensitivity range includes both 1.25 and1.5 mm. It does not establish a standard. **M18×1.5 may be a declared visual-model choice only**, with root/profile/class/fit still estimates. The thread diameter's broad photo range is 14.046–20.095 mm. Do not manufacture or accept a bung from either range.

## Proposed exterior dimensions

All values below except the manufacturer22 mm hex are **inferred working choices**. Ranges are the conditional sensitivity analysis above. They provide a reproducible starting point for an isolated exterior candidate, not accepted installation geometry.

| Feature | Proposed mm | Conditional range mm | Boundary |
|---|---:|---:|---|
| Hex across flats |22|Primary catalog value|No manufacturing tolerance supplied|
| Main cylindrical shell OD | 20 | 16.6–23.0 | Estimated; sensor projection |
| Main cylinder between rear collar and hex neck | 30 | 25.4–37.8 | Estimated; sensor projection |
| Hex axial thickness | 5.2 | 4.1–6.9 | Estimated; sensor projection |
| Annular seat ring OD | 21.5 | 17.8–25.1 | Estimated; sensor projection |
| Visible ring axial envelope, not compressed thickness | 2 | 1.4–3.1 | Estimated; sensor projection |
| Thread crest envelope diameter | 18 | 14.0–20.1 | Estimated; sensor projection |
| Visible threaded axial envelope | 7.5 | 5.5–9.7 | Estimated; sensor projection |
| Mean crest separation, only two complete intervals | 1.5 | 1.0–1.8 | Estimated; sensor projection |
| Protective nose outside diameter | 11.5 | 9.4–13.6 | Estimated; sensor projection |
| Nose exposed beyond thread envelope | 17.5 | 13.9–21.2 | Estimated; sensor projection |
| Selected visible ring plane to nose tip | 25 | 20.4–30.8 | Estimated; sensor projection |
| Rear large collar envelope diameter | 20.5 | 17.2–24.1 | Estimated; sensor projection |
| Rear reducer diameter | 16.5 | 13.7–19.6 | Estimated; sensor projection |
| Rear reducer axial span | 10 | 8.3–13.3 | Estimated; sensor projection |
| Rear metal wire-exit cylinder OD | 12.5 | 10.1–14.7 | Estimated; sensor projection |
| Rear metal wire-exit cylinder axial span | 10 | 7.8–12.6 | Estimated; sensor projection |
| Wire-exit plane to selected ring plane | 66 | 55.9–81.3 | Estimated; sensor projection |
| Metal tip to wire-exit plane overall span | 91 | 77.2–111.0 | Estimated; sensor projection |
| Visible insulated individual wire OD | 1.3 | 0.9–1.7 | Estimated; sensor projection |
| Housing back to mouth along projected centerline | 44 | 31.7–67.8 | Estimated; connector projection |
| Shroud transverse projected span | 17 | 11.2–21.2 | Estimated; connector projection |
| Approximate latch above local shroud surface | 4 | 2.1–6.4 | Estimated; connector projection |

## Coherent provisional stations and separate regions

For a future isolated specimen only, choose mm and a local Z axis along the sensor, positive toward the exhaust tip. Z0 is a **selected nominal bearing plane**, based on the ring-side photograph, not a measured compressed seat. The following rounded stations reconcile the dimensional choices; preserve them as a single proposal rather than mixing independent range extremes.

| Exterior region | Provisional local Z mm | Radial/section choice | Qualification |
|---|---|---|---|
| Slotted protective nose |+7.5 to+25|OD11.5|Rounded end; wall, hidden slots and exact attachment unknown |
| Visible thread envelope |0 to+7.5|Major18; pitch1.5|Inferred designation only; flank/root/class and true engagement unverified |
| Annular ring |−2 to0|OD21.5|Visible envelope; compression/material/actual sealing faces unknown |
| Hex |−7.8 to−2.6|AF22, axial5.2|AF primary; height/clocking estimated |
| Main cylindrical shell |−38.5 to−8.5|OD20|Small join/neck regions remain explicit modeling details, not empty unexplained gaps |
| Rear large collar |−45 to−38.5|OD20.5|Exterior collar/seam, not verified removable part |
| Rear reducer |−55 to−45|OD16.5|Stepped metal shell, not an invented rubber boot |
| Wire-exit cylinder |−65 to−55|OD12.5|Metal region with a pale insulating exit face |
| Rear terminal/exit plane |about−66|Envelope only|Insert thickness, wire-hole diameters and individual seals not dimensioned |

Thus proposed metal envelope length is 91 mm, with 66 mm above and 25 mm below the selected plane. Neither the 25 mm reach nor the 91 mm total is obtained by subtracting511 mm and 481 mm. The axial datum plane has at least the manual feature-identification uncertainty recorded in the landmark file.

The connector remains in its own frame: proposed exterior44 mm length / 17 mm cylindrical shroud and 4 mm latch projection. No connector-to-sensor pose or cable path is assigned from the bundled product photo. The front photo supports a separate colored seal/insert, latch and four round contacts, but **mouth insertion depth, pin diameter/protrusion/spacing, wall thickness, hidden keying and seal compression remain unmeasured**. Leave these as explicit unbound parameters until a model contract selects named educational estimates or obtains better evidence; do not claim a complete connector mate. The 1.3 mm individual insulated-wire OD is an exterior estimate and supplies no conductor gauge or current rating.

This supports separate exterior-region modeling, including the visible metal exit, rather than a smooth sensor rod and generic boot. The exact production breakdown of welded/formed/joined pieces is not verified. Thimble internals stay family-level illustration and are not reclassified as a target-exact BOM.

## Acceptance scope before CAD

Required model checks, if root authorizes an isolated candidate: retain 22 mm hex and all proposed parameters/evidence classes; valid intended connected regions; STEP roundtrip and CAD/GLB unit/bounds checks; actual visible thread and slot/passage checks with smooth/blocked controls; actual exported side/front/rear renders compared with these source features. Region interfaces and closure choices must be explicit. A smooth capped rod is not equivalent to the slotted protected probe. Exact manufacturing thread gauge, sealed connector mate and installed engagement remain outside the justified scope.

A scale-sensitivity checker cannot replace those geometric checks. Before installation, require the real pipe/bung seat/thread, probe intrusion and gas path, tool approach/removal, thermal envelope, routed lead slack and mating harness frame. No static collision or browser pass can supply that missing evidence.

## Delivery, reproduction and review

Readiness: **pre-CAD research/estimated contract**, not candidate geometry. Parametric CAD API, STEP/GLB, model renders and assembly transform: N/A. Owned computational artifact is `reference/engine/ho2s-dimensions-20261003-projection.py`, standard-library arithmetic only. Replay from repository root:

```sh
python3 reference/engine/ho2s-dimensions-20261003-projection.py
```

It verifies every working choice lies within its declared scenario range, rejects double-scale and 3 mm-pitch negative controls, and explicitly reports that 1.25 versus1.5 mm is not discriminated. The committed JSON contains all 22 feature spans and endpoints. No temporary image is needed for arithmetic; independent pixel re-review requires fetching the hash-identified public source. Original/photo-overlay images are excluded from the delivery.

Environment: macOS/systemPython3, curl and Poppler for public-source retrieval/rasterization. NTK PDF emitted an optional-content-group warning but text and actual page rendering succeeded; no protection bypass or source editing performed. Model/effort/usage unavailable. Source→notes pipeline used the committed authored observations with `tools/ingest.py`; two sources/two atomic notes pass frontmatter, no-H1 and prefixed-link checks. Shared semantic index is root-owned and was not run.

| Gate | Result | Limit |
|---|---|---|
| Application/coverage |PASS scoped research|Primary NTK bridge qualified; Bosch shape retained separately |
| Dimensions/coordinates |PASS arithmetic, estimated scope|Only 22 mm hex primary; all camera/scale choices declared |
| CAD/export |N/A|No CAD |
| Source/visual |PASS observations|Actual Bosch views and NTK pages inspected; no CAD comparison yet |
| Installed interfaces |NOT RUN|Pipe/bung/connector/route missing |
| Motion/disassembly |NOT RUN|No installed neighbor/tool envelope |
| Learning |PASS scoped dimensional limits|No repeated or invented electrical calibration |
| Browser |NOT RUN|No assets installed |
| Reproduction/review |PASS worker artifacts; root review pending|Frozen ledger binds sources, landmarks, arithmetic and authored notes |

Next concrete primary lead is the NTK 22503 manufacturer specification record/drawing giving diameter/pitch, now that the interchange bridge is verified. The reviewed NTK PDF and Bosch universal sheet do not supply it. This delivery already provides the bounded exterior table, so further broad searching is not a prerequisite to reviewing an explicitly estimated isolated study. Root decides the next modeling scope. #82 remains open, no issue/board/git write made, and no process remains running at handoff.
