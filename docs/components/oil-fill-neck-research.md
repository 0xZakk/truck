# Oil-fill neck research and next interface contract

## Contract and result

Research-only continuation of engine component issue #15, performed on 2026-09-26 for the coordinating integration owner. Research checkpoint commit: `aa3b3ed488ade3c4462e1bb530db5ec8b575e152`. Owned files are this handoff and `reference/engine/oil-fill-neck-review.json`. No cap, cover, manifest or checker changed; no posts or commits made.

**The required female screw interface is supported, but the production neck's manufacturing construction is still unknown.** Available applicable cap evidence does not distinguish a neck formed from the cover sheet from a separate permanently attached collar/insert. The subsequently inspected exact-model CHARM archive identifies cover service part **F3TZ6582H** and depicts the neck/opening within the cover service assembly; it still provides no defensible numerical neck depth, shoulder height or oil-fill baffle dimensions. The next candidate can model a coherent screw seat with explicitly inferred geometry; it must not be presented as a verified factory cover reconstruction.

## Evidence ledger

| Source / feature | Supported observation | Class / limits |
|---|---|---|
| [Ford EC743 / F3AZ6766B](https://www.ford.com/product/engine-oil-filler-cap-p4000083484), existing captured underside photo | Closed male stem with multiple rounded external screw ridges, surrounding seal and annular underside relief | Primary Ford image; exact 1994 F-150 4.9 Gas application already captured in pilot evidence. Not a drawing of the female neck; pitch, starts and engagement cannot be measured reliably from perspective |
| Owner engine-bay driver/passenger photos, 2026-09-23 | Oil cap occupies a round seat on the forward exposed cover area adjacent to a separate dark ventilation fitting; no long remote fill tube is visible | Exact vehicle visual evidence. Cap is installed, concealing the neck interior and connection. Cover surface/shoulder is visible but there is no scale or cap-off/underside view |
| [EngineQuest EQ-VC300N manufacturer page](https://enginequest.com/product/ford-valve-cover-4-9-300-87-to-98-new/) | Manufacturer lists Ford L6 4.9/300, 1987–1998, a tall filler neck, and interchange codes C5AZ6582K / F1TZ6582C | Replacement comparison. Broad year/application listing includes industrial coverage; does not identify the owner's installed cover or confirm neck is integral, welded, pressed or brazed |
| [EngineQuest 2021 catalog](https://enginequest.com/wp-content/uploads/2020/08/EQ2021_Catalog.pdf), printed pp. 20 and 39 | Repeats EQ-VC300N tall-neck description and both interchange codes | Primary corroboration of replacement identity; no dimensioned section or joint detail. No manufacturing inference from the word “neck” |
| [Mishimoto additional-fitment PDF](https://www.mishimoto.com/mwdownloads/download/link/id/2131), PDF page 4 | MMOFC-MUS1-BK/RD family lists Ford F-Series engines including 4.9L within 1985–2008 | Primary broad replacement-family applicability, not a VIN-specific or individual engine/year metrology record |
| [Mishimoto-sold MMOFC-MUS1-BK listing](https://www.walmart.com/ip/125860720) | Manufacturer marketplace listing gives M32 × 3.5 thread, 1.35-inch height and 2.32-inch overall OD | Replacement comparison lead. Listing identifies Mishimoto as seller; it also mixes Mustang/Powerstroke wording. Do not silently transfer these dimensions to EC743 or the actual truck neck |
| Existing [MotoRad MO100](https://motorad.com/part/MO100/) evidence | Male screw replacement, neck diameter 31.24 mm, separate rubber seal and nonvented cap | Replacement comparison; does not publish female-neck construction. Nominal M32 and this 31.24 mm catalog number are different specifications and must not be averaged |

The JSON ledger stores local photo/capture hashes and retrieval limitations. Owner photographs remain excluded from Git and are not reproduced in these files. Public links and independent replacement evidence permit continuation without those private photos, but exact-truck visual confirmation requires authorized access.

## Construction decision

- **Female screw retention:** required by applicable male screw cap. A smooth 34 mm aperture is mechanically insufficient.
- **Cover-to-neck joint:** unresolved. Neither a formed integral thread nor a separate insert is established. Do not invent a separate factory insert part number, weld, clip or fastener. For an illustrative study, a continuous neck region fused to cover geometry represents the load path while leaving the manufacturing process explicitly unresolved.
- **Visible shoulder:** owner images support a local cap seat at the front of the cover, not a dimensional annular-land specification. The installed cap hides its seat edge. “Tall filler neck” is an EngineQuest replacement description, not a measured owner-truck height.
- **Depth:** cap images establish a protruding male stem; they do not establish how much enters the cover or the axial position of the mating female thread. No millimetre neck-depth estimate is promoted from unscaled photographs.
- **Baffle:** no applicable cap-off underside view was obtained. Its existence, attachment, offset and drain openings remain unknown. An invented closed plate under the fill opening would risk blocking oil flow or rocker travel. Do not borrow a PCV baffle or a V8 neck from an unrelated engine.
- **Codes:** The exact-model archived parts entry identifies **F3TZ6582H / F3TZ-6582-H** as the cover service part; actual truck stamping remains unverified. EC743/F3AZ6766B is the applicable cap identity. EQ-VC300N, C5AZ6582K and F1TZ6582C are replacement-cover search leads, not a verified engineering stamping on the owner's cover. E7TZ-6582 variants surfaced in broad catalog searches, but exact target attribution was not established; do not use those codes as accepted identification.

## Mechanically coherent illustrative candidate

Yes: a matched male/female screw pair can be mechanically coherent while factory dimensions remain unverified. That would close a modeled retention gap for an expressly agreed educational scope; it would not establish factory fidelity or service interchangeability.

Build the cap and female neck from one parameter set: pitch/lead, starts, handedness, major/minor dimensions, profile, radial/flank clearance, axial phase and engaged span. Keep the measured/source-supported vs inferred fields separate. Two distinct options are defensible for a future study: retain the current cap's explicitly assumed 4.5 mm pitch and design its mate as an assumption, or develop a separate M32 × 3.5 replacement-comparison variant following the Mishimoto lead. Do not combine the 31.24 mm MO100 dimension, M32 thread label and arbitrary root/profile into a supposedly manufacturer-specified standard.

Preserve existing CAD axis `(240,-12)` and record any proposed change from the provisional Z413 sealing datum. Build material continuously from the female flanks through the neck to the cover; merely subtracting a thread from the existing thin roof may leave insufficient engagement, and a floating threaded ring has no load path. Use a finite sealing land and separate seal, with declared illustrative compression. Leave a connected fill/drain passage when the cap is removed. Neck wall, root clearance, seal groove, compression and attachment construction remain inferred until measured.

Required checks before proposing installation:

1. Valid connected solids, units/axes, STEP and GLB agreement; axial sections reveal actual female material and flank overlap.
2. Positive engaged length at the seated seal, radial/root clearance and mating-flank relationship. A deliberately oversized female bore must fail retention. A straight axial pull should meet the threaded restraint; matching screw rotation/translation should release without unintended intersections.
3. Screw removal sampled through disengagement, then physical withdrawal clearance; cap orientation at seal contact must not be adjusted by eye to conceal thread-phase errors.
4. Seal seat contact plus explicitly modeled compression; no unsupported pressure/leak-tightness claim.
5. Oil-fill passage continuity, including any later evidenced baffle and drain gaps.
6. Neck **and** cap versus all rocker poses. The prior cap-only 1.3754 mm clearance cannot certify a larger female sleeve or a baffle. Check cover wall, ventilation fitting, upper intake and withdrawal path as affected neighbors; retain meaningful collision negative controls.
7. Integration-owner review and browser selection, section, explode/reset and removal demonstration. Factory-retention evidence stays visibly unresolved even if an educational pair passes geometry checks.

## Measurements needed to resolve factory construction

Obtain one identified applicable cover with the cap removed. Record a top-down opening view, grazing side view and underside view with a scale in the same plane. Include the cover's stamped/cast engineering number and cap markings. These views should reveal whether a seam, weld/braze, pressed flange or continuous drawn wall exists and whether a baffle is present.

Measure neck height from adjacent cover roof to seal land, land OD/ID/flat width, wall thickness, cap stem insertion depth, female thread axial endpoints, major/minor diameters, pitch/lead/starts and profile. Record gasket free/compressed dimensions and installed cap angular orientation. Measure underside/baffle distance to the cover datum and opening/drain sizes. No teardown instruction, torque specification or production dimension is supplied by this research.

## Validation, limits and restart

Research source/application review completed; manufacturing topology and dimensions remain OPEN. Geometry/export/motion/browser checks are N/A for this research-only diff: no CAD was changed. JSON parse and file review passed. Integration-owner review remains pending. Model/effort/usage unavailable.

An unrelated image-search hit resolved to a Renault valve cover and was rejected. Ford V8/Powerstroke neck images were not transferred to the 4.9L cover. A matching-year owner teardown page could not be decoded by the web reader; a replacement image URL could not be fetched, and computer browser surfaces were unavailable. These are evidence-access limits, not proof of any neck design. Search captions were not treated as visual observations.

Next action: choose whether the next sub-issue is an explicitly illustrative matched pair or production-topology capture. For the former, declare its parameter variant and limits before CAD work; for the latter, acquire the identified cap-off/underside specimen views and measurements above. No process remains running.

## Exact-model offline archive follow-up

The ignored archive at `manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L` was discovered with `rg --files --no-ignore` and reviewed directly. Originals remain local; only identifiers, hashes and paraphrased findings are recorded. Another reviewer needs authorized access to this archive to reproduce the image inspection; the delivery does not redistribute the manual.

| Reviewed page/image | Finding | Interface consequence |
|---|---|---|
| Parts and Labor → Engine → Valve Cover → Parts Information | Manufacturer FOR; OEM part **F3TZ6582H** | Prefer this exact-model application lead over broad replacement interchanges when locating a specimen |
| Parts and Labor → Engine → Images; `images/DM05Q313/ford10/1860036218.png` | Actual exploded 4.9L engine image inspected: cover callout 3 and gasket 4. Top openings belong to the depicted cover; no separate neck/insert/baffle callout | Supports keeping the neck within the cover service assembly. Does not distinguish integral forming from permanent joining, nor prove absence of hidden subcomponents |
| PCV → Description and Operation; `620350918.png` | Actual schematic inspected: cap at one end of rocker cover, closure hose nearby, PCV connection at the other end | Keep fill cap and ventilation connections distinct; this schematic gives no thread or joining section |
| Rocker Arm Assembly → Service and Repair, Fig. 24; `289449564.png` | Actual rocker/fulcrum/guide/pedestal view inspected | No filler baffle evidence. Rocker oil-deflector terminology is not a specification for a cover baffle |
| Engine Lubrication → Diagrams; `354634388.png` | Actual lubrication image inspected | Upper-train oil-feed illustration does not specify the fill-neck underside |
| PCV → Oil Separator → Service and Repair | Text describes PCV-to-upper-intake hose connections | Do not reinterpret this hose/ventilation entry as a separately identified filler-neck baffle |

Full repository-relative HTML/image paths and SHA-256 values are in the JSON ledger. No separately listed neck/insert was found in these relevant pages; this is a scoped search result, not proof that such a manufacturing subpart never existed. The drawing is a service assembly overview, not a dimensioned manufacturing drawing. **Formed female neck versus attached collar therefore remains unknown.** A continuous female-seat region within the cover service assembly remains a reasonable illustrative modeling choice, explicitly labeled as such. The measurement plan and required clearance/retention checks above still apply.
