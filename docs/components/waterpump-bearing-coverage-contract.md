# Component contract and handoff: water-pump bearing coverage

Engine #47 under #32; root integration owner. Baseline9df77dd0cec845ab68722d387e708e9cdbf07fb4. Own this handoff and `reference/engine/waterpump-bearing-coverage-evidence.json`. Evidence and build contract only; no housing, tube, shaft, manifest or previous report edits. Existing source module and mechanical-seal report were inspected first. Hashes bind the relevant source, manifest and exported shapes.

**No applicable dimensioned bearing identity was found.** Existing F6TZ8501KB/Gates44009 application evidence identifies a pump assembly, not its bearing supplier, row arrangement or internal dimensions. Current Gates literature describes a unitized bearing/shaft, and GMB's queried product page supplies generic bearing claims and package sizes. Neither identifies this pump's internal bearing. The GMB part's application was not established and its package dimensions are rejected as bearing measurements.

## Existing physical coverage

Actual exported STEP bounds confirm the modeled bearing is a single annular cartridge: pump-localX34..68, OD47.8mm, bore16.1mm. The current separate shaft is Ø16mm, X−75..79. These are inherited estimates. The original water_pump.py shaft was shorter; water_pump_joint_candidate.py supplies the extended shaft now exported. Do not use the original104mm length as current geometry.

The cartridge has no individual rolling elements, cages, end grease seals or machined raceway detail. Existing shaft, slinger, drive hub and six-piece coolant mechanical-seal study are already present. Bearing seals are a separate function from the coolant face seal; this audit does not add another coolant seal assembly.

## Primary comparison and application limits

Actual Schaeffler TPI131 PDF7/printed5 Fig2, PDF8/printed6 Fig3 and PDF15/printed13 Fig9 were rendered and inspected following PDF skill. This manufacturer reference shows integral shaft raceways, a common outer ring, cages, rolling rows and seals; it offers multiple row arrangements. It does not connect a particular bearing to Gates44009 or Ford4.9L.

Its dimension table includes a15.918mm shaft/30mm outer diameter with34mm as one ring length. Its47mm outer-diameter entry instead uses24mm shaft and38/50mm lengths. Neither establishes the inherited47.8/16/34 model. Matching one dimension is not a bearing identification, and choosing the nearest size cannot justify changing the pump housing.

Sources: [Schaeffler TPI131](https://www.schaeffler.com/remotemedien/media/_shared_media/08_media_library/01_publications/schaeffler_2/tpi/downloads_8/tpi131_de_en.pdf), [Gates master catalog](https://www.gates.com/content/dam/documents-library/catalogs/masterproductscatalog.pdf), [queried GMB product](https://gmb.net/product/125-1420p/). The prior `water-pump-internal-construction-reviewed.json` remains authoritative for earlier source capture and limitations. No generic illustration is relabeled as a Ford section.

## Physical breakdown and build contract

| Proposed identity | Quantity / status | Requirement before detailed CAD |
|---|---|---|
|water-pump-shaft|One already modeled|Actual shaft steps, integral raceways if applicable, hub/impeller/seal stations|
|water-pump-bearing-outer-ring|One generic common-ring interpretation; refine cartridge|Applicable outer diameter, width, raceways and housing fit|
|water-pump-bearing-rolling-element-row-R-element-N|Unknown; absent|Actual row type/count, element size/count and pitch circle|
|water-pump-bearing-cage-row-R|Unknown; absent|Actual cage construction and retention per row|
|water-pump-bearing-seal-end-N|Unknown; absent|Actual end seal count, lips, seats and material stack|

These are reserved naming patterns, not new inventory parts or a claimed factory quantity. Preserve stable shaft/bearing IDs until root approves an assembly-alias migration. Do not retain the full cartridge overlapping newly built internals, duplicate the shaft as a second unitized part, or add separate inner rings merely because ordinary catalog bearings have them.

A defensible next input is the bearing marking or measured/sectioned applicable pump. Record supplier number; ring OD/length; complete shaft steps; row construction; seal stack; and housing fit. Preserve the pump-localX axis and current hub, impeller, coolant seal and weep interfaces until those measurements justify a coordinated revision. Parent must approve any neighboring changes. No fitting a convenient generic bearing by cutting the housing or moving the pulley plane.

Once evidence exists, acceptance should check separate valid/exported parts, actual race/rolling-element contacts and cage clearances, end seal seating, shaft/outer-ring retention, retained hub/impeller/seal datums and open weep cavity. Deliberately wrong row pitch/shaft station and blocked weep controls must fail. Sampled rotation is not a load, lubrication or fatigue simulation. An isolated generic teaching specimen is a possible separately authorized task, not an installable Ford-bearing correction.

## Validation and restart

Source/visual gate PASS only for generic architecture; applicability and production dimensions unresolved. Existing STEP bounds checked with build123d import/bounding_box; no new geometry. CAD/export, installed interfaces and motion NOT RUN for a replacement because none is proposed; browser NOT RUN. No factory BOM or completion claim. Reproduce PDF views with pdftoppm at the indexed pages; source and asset hashes are in the evidence JSON. Python3/build123d on macOS; usage unavailable. Root review pending. Next action is the narrow bearing-identity/sample request above, not another generic catalog search. No running processes.
