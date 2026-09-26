# Component research and interface handoff: engine-oil-dipstick-tube

## Contract and result

Issue [#78](https://github.com/0xZakk/truck/issues/78), engine parent #1. Research-only assignment, integration owner root. Baseline at delivery: `24a023b5313bda64a50f0a36356220f05a731eb8`. Owned files are this document and `reference/engine/dipstick-tube-review.json`. No CAD, shared manifest, current seal, issue or PR changes.

The useful result is a **two-anchor tube assembly**: a threaded lower attachment at a block entry and an upper bracket at the pushrod-cover retainer. This is a better-supported starting architecture than a generic push-fit tube, an invented pan fitting, or a bore drilled along the rejected dipstick candidate. Exact 1994 identity and mounting coordinates remain unresolved; readiness is **research**, not integration-ready or Done.

## Source-supported findings and limits

The [Ford 1995 4.9L service manual](https://www.scribd.com/document/720481789/1995-FORD-F-150-F-250-F-350-BRONCO-F-SUPER-DUTY-POWERTRAIN-DRIVETRAIN), section 03-01A, Oil Level Indicator Tube, identifies a lower nut and an upper bracket as parts of tube assembly **6754**. Its bracket mounts to pushrod-cover retainer **6C517**, with separate stamped nut **370786-S8**; dipstick **6750** and cover **6519** appear in the same callout table. Relevant figure locator is **A23872-A**, around printed page 03-01A-37. Indexed procedure/callout text was inspected, but the figure pixels were not retrieved. This is adjacent-year primary documentation, not verified 1994 interchange. Do not infer a thread size or retainer dimension from OCR or transfer its service torques into this task.

A [1994 F-150 4.9L replacement-engine listing](https://carpartplanet.com/engines/ford/f-150/1994/4.9l-vin-y-8th-digit-air-in-head-without-e4od-transmission) describes a rear-side tube entry through the block. A [1996 manifold-AIR replacement](https://reman-engine.com/remanufactured-engines/ford/f-150/1996/4.9l-vin-y-8th-digit-gasoline-air-in-manifold-without-e4od-transmission) agrees. These are supplier descriptions of replacement configurations, not proof of this truck's casting or coordinates. They support investigating a **rear-side block entry**, with the tube staying on the pushrod-cover face. Existing project coordinates call that face **+Y**; front is +X. Do not yet assign a measured X station, RH/LH label, entry angle or oil-pan penetration.

**Exact service part number is still unknown.** [E7TZ-6754-A](https://www.fordpartsgiant.com/parts/ford-tube-oil-level-indicator_e7tz-6754-a.html) is a lead, not a selected part: current broad catalog fitment does not establish the target 4.9L/1994 application. The [1994 category page](https://www.fordpartsgiant.com/oem-1994-ford-f_150-dipstick_tube.html) includes V8 tubes and transmission base number 7A228, which must not be substituted. Econoline-specific tubes, 1980–82 pan-entry arrangements and 7.3L diesel pan adapters are also unsuitable evidence for this interface. Catalog package dimensions are unusable as tube geometry.

A [used tube-and-indicator listing, item 307070141153](https://www.ebay.com/itm/307070141153), was found through its category page. Its title claims 1987–95 4.9L F-series, but its page was inaccessible. No shape, stamping or measurement claim is made from that lead. The existing E9TE-6750-DA blade specimen remains a comparison only; it does not identify the tube or establish calibrated insertion length.

Both owner bay photographs were inspected again at their original local paths. Neither provides a secure view connecting the handle, tube, upper bracket and lower entry. The low-resolution archived EFI exploded image likewise cannot establish the small fitting details. Hashes and access limits are in the JSON ledger; restricted owner photos have not been copied into distributable outputs.

## Component and interface plan

1. **Establish lower datum first.** Inspect the rear portion of the block's pushrod-cover side. Identify the actual entry and photograph its relationship to the pan rail and rear block face. Measure seat center, insertion axis, shoulder depth and fitting section. Do not choose whichever point clears the trial blade.
2. **Establish upper datum independently.** Locate the tube bracket at the pushrod-cover retainer. The existing model has six generic cover-bolt stations. Determine the actual station and whether its hardware must become a stud/retainer assembly corresponding to 6C517. Do not add a free-floating nut to the modeled bolt head.
3. **Identify physical pieces without inflating the BOM.** Proposed teaching occurrences are the formed hollow guide tube, its attached support bracket, lower retaining nut and upper stamped nut. Keep bracket/nut service association with 6754, but verify actual joint and nut captivity before separating or animating them. Add a separate seal, ferrule or washer only if a diagram or specimen demonstrates one. Absence from a callout table is not proof that none exists.
4. **Fit a measured centerline between the anchors and mouth.** Record straight lengths, bend radii/planes, tube OD/ID and the mouth seating plane. Constrain the route to the pushrod-cover side, around its retainer and neighboring ignition leads/distributor/coil, with engine-mount and pan-rail clearance checked at the lower end. All numerical values are currently unknown.
5. **Reconcile the matched blade afterward.** Measure stop-to-tip length, blade section and the original reading band from the matched pair. The existing -8.5° trial pose and 692.15 mm approximate specimen blade length cannot define the tube route, oil plane or full/add calibration. No oil-level marks should be invented.

Suggested stable IDs for a future candidate are `engine-oil-dipstick-tube`, `engine-oil-dipstick-tube-bracket`, `engine-oil-dipstick-tube-retaining-nut`, and `engine-oil-dipstick-tube-support-nut`, grouped under lubrication. These are proposed IDs only; component count and service association remain subject to specimen confirmation. The existing `engine-oil-dipstick` ID stays reserved for its separate indicator candidate.

## Acceptance plan

| Gate | Present state | Evidence required next |
|---|---|---|
| Application/coverage | PARTIAL research | Exact-year catalog/diagram or matched owner specimen; actual 6754 identity |
| Dimensions/coordinates | NOT RUN | Independently measured lower seat, upper support and mouth; millimeter datum table |
| CAD/export | NOT RUN | Hollow single tube solid, physical hardware split, STEP roundtrip and CAD/GLB bounds |
| Source/visual comparison | PARTIAL | Inspect figure A23872-A pixels and applicable specimen, including both ends and bracket |
| Installed interfaces | NOT RUN | Coaxial entry/seat, actual bracket bearing area and retention stack; no arbitrary holes |
| Motion/disassembly | NOT RUN | Flexible blade insertion/withdrawal through bore, retained nut release and crank/rod clearance over 720° |
| Learning/diagnostics | PLAN | Explain matched tube/indicator seating and mismatch risk without invented calibration or service specifications |
| Browser integration | NOT RUN | Individual selection, grouped isolation, actual mounting context and staged reset |
| Reproduction/review | PASS research package | JSON ledger with local hashes, public source URLs, access failures and evidence classes; integration-owner review pending |

Critical future negative controls: deliberately offset the tube from its seat; move the upper bracket off its retainer; narrow or obstruct the guide bore; mismatch indicator seating length. Each must fail the corresponding contact, support, passage or calibration-consistency check. Static external clearance alone cannot validate flexible withdrawal or sump calibration.

## Restart

Next action is to obtain the actual figure and/or an identifiable matched tube specimen, then document the two anchor measurements. If the owner inspects the truck, the useful photographs are the lower threaded entry with nearby pan rail visible, the upper bracket/retainer, and the complete indicator seated at the tube mouth; include an independent length reference. No new owner input was requested during this research task. No process remains running. #78 remains open. Model/effort/usage were not available; no cost figure is inferred.

## Exact-year offline archive follow-up

The local 1994 CHARM bundle was searched again with ignored files included (`rg --files --no-ignore manuals/factory-service-manual`), and the ZIP directory was checked for pages absent from extraction. The bundle has 14,278 entries. Searches covered dipstick/oil-level-indicator names and text, 6754, 6C517 and A23872. **No engine-oil tube installation page or attachment diagram was found in this bundle.** This is a finding about the available archive, not evidence that the tube or a Ford procedure did not exist.

The engine removal procedure, lifter/pushrod-cover removal procedure, oil-pan procedure and lubrication diagram were read. The lifter page gives no tube retainer detail. Four downloaded images were visually inspected: `288847252.png` (lifter), `350370598.png` (rear pan seal), `350379654.png` (pan installation) and `354634388.png` (lubrication passages). None identifies the dipstick tube's fitting, bracket or route. The pan drawing's omission of a tube is not evidence for or against a pan port. The electrical oil-level warning pages and automatic-transmission dipstick parts entries were also checked and excluded; their indicators cannot identify this engine-oil tube.

Exact source paths, SHA-256 hashes, per-image observations and reproducible search scope are recorded under `offline_1994_archive_review` in the JSON ledger. No manual content was copied or redistributed. **Applicability has not been promoted:** the two-anchor retention architecture is still adjacent-1995 Ford evidence, and exact 1994 attachment confirmation remains open before geometry work.
