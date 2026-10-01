# Component contract and handoff: oil-pump production topology reconstruction

## Contract

Engine #32; inclined-linkage worker, root integration owner. Baseline `3dcbd364ac24396e671d5d16b930571713b7be0a`, branch `engine/timing-drive-fit`. Own only this new handoff and `reference/engine/oil-pump-topology-evidence.json`. Scope is a source-supported interface contract. Detailed CAD is conditional on dimensional evidence; none is submitted. Preserve existing pump, frozen pickup connection study, drive stages, stable IDs and shared manifests. Root owns any block changes.

The exact-year service identity is C5AZ6600A, with E3TZ6622F pickup. The industrial book uses the same pump service assembly but a different pickup; industrial tube routing and casting revision cannot silently become 1994 truck geometry. Existing `oil-pump-housing`, rotor, cover, relief and pickup IDs remain reserved. New distinct physical items would require root-coordinated IDs for pump-to-block gasket, pickup flange gasket and locating dowel. A flange integral to housing is not a separate fabricated part.

## Evidence ledger

| Claim | Source / actual review | Evidence class and limit |
|---|---|---|
| Pump gasket and retaining attachment | Exact-year Oil Pump Service and Repair, retained source in preceding audit | Applicable procedure; no outline or bolt coordinates |
| Installed neck and pickup arrangement | Ford CSG649 PDF28 / printed1-24, Fig51 A2164-A, actual rendered page inspected | Primary Ford industrial comparison; front arrow left in this view; hidden block seat unresolved |
| Separate inlet opening and outlet opening | Same PDF28 installation text | Distinct hydraulic roles; no drilled-path dimensions |
| Pickup attaching gasket and screws | PDF36 / printed1-32, Fig65 A2165-B, actual page inspected | Inlet tube6622, gasket6626, screw20346-S/washer34806-S; separate from cover6616 and rotor/shaft6608 |
| Raised drive neck; independent relief branch | Same Fig65 | Visible topology. Does not give neck height, mount-plane normal, or bore separation |
| Pump-to-block dowel | Ford industrial parts PDF18 / printed15; prior frozen visual review | 378644-S, 1/2 × 13/32 notation; no proven lumen or installed orientation |
| Manufacturer M74 comparison | Melling industrial catalog search index | 300 application, M74 and M74HV separate; original PDF unavailable; no accepted dimensional drawing |

Original Ford PDF: [CSG649 source](https://www.coulsoncompression.com/resources/docs/194-210%20CSG649%20Service%20Manual.pdf). Local source and previous audit hashes are bound in the new ledger. Restricted source pages are not redistributed. Re-render PDF28 and36 locally using `pdftoppm -f 28 -l 28 -scale-to 2000 -png -singlefile reference/engine/ford-csg649.pdf /tmp/oil-pump-topology-installed` and the equivalent page36 command. Temporary renders are review aids; the source/page/hash is the reproduction dependency.

Focused primary search on 2026-10-01 reached [Melling's dimension lookup](https://melling.com/parts-lookup-part-number-dimension/) and its [specification portal](https://specsearch.melling.com/default.aspx). Visible categories include intermediate shafts but not oil pumps. Its official linked application portal `https://melling.mypartfinder.com/` returned403. No login/browser bypass or manufacturer contact was attempted. Current manufacturer technical/catalog searches supplied no M74 mounting drawing. Manufacturer Fel-Pro/MAHLE gasket leads from the preceding audit remain unresolved.

Secondary product metadata was used only to identify a reason to reject a dimensional shortcut: O'Reilly M74 listed height4.680in and124mm (4.680in converts to118.872mm), while .315in appears as inlet/pickup size there and as mounting-hole diameter in another listing. Those descriptions cannot identify a measured port or mounting datum. They are not adopted as authoritative dimensions, image scale, or CAD bounds. No secondary technical specification is accepted into the interface contract.

## Cross-part datum contract

All new geometry would be in millimetres and the existing shifted pump frame. Preserve `PUMP_FRAME` plus DELTA `[0,5.109820990161097,4.087856792128875]` as the current kinematic hypothesis, with rotor drive axis at pump-localX3.5/Y0 and direction+Z. This protects crossed-drive registration and intermediate-shaft engagement; it is not a surveyed Ford mounting datum. Distinguish five interfaces:

1. **Drive neck:** coaxial mechanical shaft support/clearance around the retained drive line. Required unknowns: neck OD/ID, bearing extent, height to mounting face. Shaft bore must not be labeled the discharge passage.
2. **Pump-to-block face:** one coherent gasketed flange carried by the raised neck/body, with mounting screws and locating feature. Required unknowns: face origin/normal, outline, bolt axes and thread/engagement, dowel axis/fit, drive opening, discharge aperture and gasket thickness. Existing cover-ear feet at localX±28/Y28 are rejected as its dimensional basis.
3. **Pressure outlet:** distinct open connection from pumping chamber to the block receiving passage, including relief-circuit relation. Required unknowns: aperture location/size, passage path and minimum wall. Do not assume the locating dowel is a hollow oil tube; do not connect discharge to the crankcase shaft-clearance bore.
4. **Pickup flange:** separate two-fastener inlet connection and gasket between tube and housing, as supported qualitatively by Ford diagrams. Required unknowns: face plane, inlet aperture, bolt spacing/thread and flange/gasket thickness. Current inserted-tube endpoint is a fit-study boundary only; its 12mm OD and 3mm insertion do not establish this flange.
5. **Block receiver:** mating seat/bolt/dowel pattern and continuous pressurized route to the existing filter/gallery architecture. Root must approve a bounded material/cut mask after these datums are known. Cylinders, main journals, crank/rod clearance, pan sealing and current filter interface are protected. No mask is authorized by this research contract alone.

These unknowns are explicit nulls in the ledger. A future constructor should require them as named parameters without plausible-looking defaults. If root elects an illustrative candidate, each estimated field and its rationale must be declared before CAD; passing contact checks must not upgrade it to production geometry.

## Delivery and validation

Research/contract only; no CAD assets, production correction or integration proposal. Existing housing source confirms a32mm cylindrical envelope, four cover ears, separate long relief bore, drive clearance and side inlet, but no raised gasketed mounting flange or named pressure outlet. A standalone gasket around those ears would preserve the wrong topology. The frozen pickup study remains a useful numeric fit control, not an accepted replacement for the flange.

| Gate | Result | Scope |
|---|---|---|
| Applicability | PASS limited | Exact-year identities; industrial pump comparison distinguished from truck pickup |
| Source visual | PASS qualitative | Actual Ford installed/exploded pages inspected; no dimensions extracted from perspective |
| Dimensions/coordinates | UNRESOLVED | Retained kinematic frame known, production mounting/flow datums absent |
| CAD/export/interfaces/motion | N/A research delivery | No geometry built; physical acceptance remains open |
| Learning/browser | NOT RUN | No canonical changes |
| Reproduction | Source hashes/pages | New ledger plus preserved prior audit; no restricted artwork redistributed |

Future candidate acceptance requires actual two-sided gasket contact/backing, dowel and fastener seating, shaft engagement, connected distinct inlet/outlet passages and minimum wall stock. Negative controls must detect blocked discharge, misregistered gasket and unsupported flange. Review actual section and exported mesh, changed stationary neighbors, crank/rod and pump motion, pan clearance and removal route. Code may merge as research; installed acceptance is explicitly withheld.

## Tracking and restart

Issue32 remains open; next input is a dimensioned applicable pump mounting face/block seat, manufacturer drawing or measured C5AZ6600A/M74 sample. Prioritize drive-axis-to-face distance and bolt/dowel/discharge coordinates; these jointly control block, pickup and intermediate shaft. Root must coordinate any departure from the retained kinematic frame. No running processes, no new CAD, no shared files modified. macOS15.6.1, Poppler source rendering; usage/billing unavailable.
