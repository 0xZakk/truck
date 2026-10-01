# Component contract and handoff: oil-pump physical coverage

## Contract

Engine #32; root owns integration. Baseline `fbd453c66cff813cfc84fb18f88e1d1ecc560ee4`, shared focused branch `engine/timing-drive-fit`. Own only this file and `reference/engine/oil-pump-coverage-evidence.json`. Research/BOM audit, no geometry or shared edits. Preserve previous topology, pickup and electrical deliveries. Millimetres for conversions; no new origin, transforms, host bore or mounting mask. Inputs are available locally and individually hashed in the evidence file.

Compare completion-plan Lubrication and work-breakdown oil-pump against canonical definitions/occurrences and applicable exact-year service evidence, using Ford industrial exploded diagrams only as explicitly qualified comparisons. Actual PDF pages reviewed following PDF skill; no purchased artwork redistributed. Source quantities are not automatically exact1994 quantities.

## Evidence and coverage

Canonical oil-pump work group has10 definitions/14 occurrences. Intermediate shaft and drive retainer add2, pickup tube/bell/screen add3: **19 selected occurrences**, all with unresolved construction/application limits. The work-breakdown's broad rotor/gallery/mount tasks do not enumerate the missing gasket, dowel and pickup hardware below. Completion-plan correctly rejects the old feet and inserted-tube architecture. No completion percentage follows from either count.

Primary comparison sources: `reference/engine/ford-industrial-parts.pdf`, PDF18/printed15; `reference/engine/ford-csg649.pdf`, PDF36/printed1-32, Fig65 A2165-B. Exact-year pump service C5AZ6600A matches the industrial service identity; exact-year pickup E3TZ6622F differs from industrial C5TZ6622B. Thus pickup bends, support details and screw stack cannot be transferred as factory specifications.

| Proposed stable identity | Status / source quantity | Evidence and missing prerequisite |
|---|---|---|
|oil-pump-block-gasket|Absent; one service gasket|Exact-year removal/installation requires new pump gasket. Outline, holes, thickness and block seat unknown. No gasket around existing feet.|
|oil-pickup-flange-gasket|Absent canonical; separate estimated topology asset exists; one comparison gasket|Parts table D5TZ6626A and Fig65 callout6626. Truck applicability and dimensions unknown.|
|oil-pump-block-dowel|Absent; one comparison dowel|378644-S, raw1/2×13/32in (12.7×10.31875mm). Roles/order, construction and fit not established.|
|oil-pickup-flange-screw|Absent; two comparison attachment stations|Fig65 screw20346-S. Thread, length, truck pattern and stack unknown.|
|oil-pickup-flange-lockwasher|Absent; two conditional on those stations|Fig65 washer34806-S. Dimensions/revision unknown.|
|oil-pickup-support-nut|Absent; one industrial comparison|33799-S8, nominal3/8-16. Actual truck support/stud, nut height and across-flats unknown.|
|oil-pickup-support-washer|Absent; one industrial comparison|34807-S8, nominal3/8. OD/ID/thickness and truck support unknown.|
|oil-pump-cover-lockwasher|Absent; truck quantity unknown|Fig65 calls34805-S; parts table separately lists four42911-S cover bolts without washer row. Four washers is conditional, not established exact-year count.|
|oil-pump-relief-cap|Already modeled provisional; one|Fig65 cap6666 and staked-cap removal. Retention construction incomplete; not a new missing plug.|
|oil-pump-drive-retainer|Already modeled provisional; one|Parts table C4AZ6629A. Working grip/retention unknown; not absent.|

Housing, inner/outer rotor, rotor shaft, cover, four cover bolts, relief plunger and spring are also present provisional. The two existing mount bolts are estimates on rejected mounting feet, not proof of correct mounting hardware. The rotor-and-shaft6608 service assembly must not be added on top of the two represented pieces. The integral drive neck and pickup flanges are construction corrections, not necessarily new independent plates. The separate illustrative topology study is not installed and supplies no production dimensions.

The CSG cover screw20324-S plus lockwasher34805-S differs from parts-table bolt42911-S (1/4-20×5/8). Preserve this revision/source difference instead of merging the references into a fictitious exact stack. The cap extraction screw and drilled1/8in hole in CSG disassembly are service tools/actions, not installed factory components. No extra pump gallery plug, rotor pin or relief retaining pin is established by these reviewed sources. Keep unknowns open without adding generic fasteners.

## Independently buildable next piece

**No newly absent pump piece is yet dimensionally specified enough for an unqualified standalone model.** The most actionable is378644-S: it has an explicit identity, quantity and two nominal dimensions, independent of mounting placement. Obtain its drawing or measure a sample to resolve diameter/length order, split construction, wall/slit and end chamfers. Then build a separate uninstalled dowel, leaving host fit/axis open.

One focused search found an older [Ford parts catalog index](https://squarebirds.org/Manuals/1965/1965-72FordPartsTextCatalog/09-1965Text-Engine.pdf) describing378644-S as a split dowel with the same nominal pair. Direct PDF access returned403, so this remains an unreviewed older-car lead, not adopted geometry or1994 applicability. In particular, do not model a solid pin from the current table. Nominal3/8 nut/washer data alone likewise do not specify a complete standalone shape. Existing fully dimensioned intermediate-shaft envelope is already represented and is not an omitted-part opportunity.

For a usable pump, measure the raised mount face relative to the drive axis, bolt/dowel/outlet coordinates, gasket interfaces, and distinct discharge path to the block. Root must coordinate all block changes. A separate pickup gasket needs applicable flange geometry; producing a polished blank would not resolve the architectural gap.

## Delivery and validation

Evidence JSON binds current manifest, completion-plan, work-breakdown and frozen source studies. Canonical extraction confirms19 selected occurrences and checks proposed absent IDs against definitions. Actual primary page visual review PASS for the stated comparison; exact-year full physical BOM and dimensional acceptance remain unresolved. CAD/export, motion and dimensional tolerances N/A for evidence-only delivery. Installed interfaces, learning integration and browser NOT RUN. No new CAD, rerouted passage or changed existing asset.

Reproduce source review using `pdftoppm -f 18 -l 18 -scale-to 2400 -png -singlefile reference/engine/ford-industrial-parts.pdf /tmp/oil-pump-coverage-parts` and correspondingCSG page36. JSON can be parsed with Python3; compare bound file SHA-256 before reusing counts. macOS/Poppler/Python3; model/usage unavailable. Root review pending. Next action is the scoped dowel drawing/sample request above, followed by coordinated mount survey; #32 remains open. No running processes. Research may merge without installation acceptance.
