# Regulator seal architecture research — r7 proposal preparation

Issues #40/#42 under engine #1; #41 hose independent, #36 intake neighbor. Root owns integration. Research begins on root branch engine/component-fit-followup-20261003, base5c5a11d. Owned files use `fuel-rail-candidate-20261003-seal-research-r7` prefix. No r7 CAD or shared change authorized yet. The r2–r6 package is separate and preserves its failed regulator seal architecture.

## Source transfer chain

1. Exact1994 service page, Fuel Pressure Regulator/Service and Repair, image651545921: underside shows larger offset port with O-RING leader, smaller separate port, two-port gasket, triangular three-hole mounting plate. Page text uses singular O-ring and separately identifies gasket. No dimensions. Image182380006 confirms exact-year rail installation context.
2. Exact1994 Description and Operation page, image651252932, explicitly **Typical**: larger offset supply inlet carries two illustrated groove positions; separate central return; captured diaphragm, spring/seat and inlet screen. Two grooves in a Typical diagram do not prove two rings on the truck. This cutaway supports architecture, not ring count or dimensions for PR18.
3. Primary manufacturer [DS1125](https://www.ds.ind.br/pt/produtos/regulador-de-pressao/1125) cross-references PR18, CM4763 and F4TZ9C968A and lists F1504.9 gasoline1987–94. Actual manufacturer photos2/3 show one visible green ring on the larger offset stem and a separate smaller bare tube, plus black two-port gasket and three mounting holes. This corroborates service illustration geometry. It does not establish unseen secondary seals or factory dimensions. DS is a replacement comparison.

Original manual/manufacturer pixels are excluded from publication. Public image URLs, hashes and authored observations are in the paired evidence JSON; downloaded temporary files are not reproducibility dependencies. Raw manufacturer page retrieval confirms identifiers/application independently of seller crossrefs. The DS technical PDF describes separated fuel/vacuum chambers but provides no seal dimensions.

## Finding and rejected assumptions

The r2–r6 single tiny O-ring on the **central return** stem is not supported by the service/photographic transfer chain. Do not repair its leak by merely enlarging the ring. Current free ring CS0.5mm lies in a0.6mm radial gland and cannot be called compressed. A proposed volume-preserving geometric seal with only0.1mm squeeze was **rejected by root before CAD**, since it conflicts with general primary seal-design guidance and preserves an unsupported size/location.

[Parker ORD5700](https://www.parker.com/content/dam/Parker-com/Literature/O-Ring-Division-Literature/ORD-5700.pdf), section3.6–3.7, provides general squeeze/fill guidance, not a Ford part specification: typical gland fill60–85%, minimum void10%, static maximum squeeze30%, general minimum absolute squeeze about0.2mm, installed stretch above5% not recommended. Material, temperature, fluid swell and tolerances still matter. Do not pick dimensions solely to pass those ranges.

No applicable manufacturer seal ID/cross-section was found in the reviewed PR18/CM4763/F4TZ9C968A sources. Ford's unrelated36.5mm-ID product listing has no verified transfer and is rejected. PR15/PR22 searches also do not establish this4.9L application.

## Next coordinated hypothesis — not a numeric approval

Preserve six injector seats, three rail mounts, existing exterior regulator envelope and flange screw axes. Replace the unsupported central-return-ring arrangement with a **larger offset supply stem carrying one explicitly modeled service O-ring**, plus a **smaller bare return outlet** and a two-port sealing gasket. Determine lower-floor/seat attachment and source-compared port proportions together; do not merely move an O-ring between two otherwise unchanged invented paths.

A numerical proposal must separately state: free seal ID/CS/evidence, groove root/width/corners and capacity, receiving bore/chamfer and assembly direction; installed shape preserving free elastomer volume; inner/outer contact areas and radial squeeze; tolerance/swell limits; source-vs-render port/gasket comparison. If exact dimensions remain unavailable, propose a physically coherent **estimated** package with transparent source-proportional ranges, not a factory specification. Coordinate the supply tube and return socket transitions while preserving protected rail interfaces. Keep both transverse layout hypotheses.

Readiness research; no seal acceptance. Exact next action: digitize manufacturer view2/3 normalized port/stem/ring proportions with uncertainty, compare independent service diagram, then submit full numerical inlet/return/gasket/seal contract to root before CAD. R6 hose was a failed truncated export, preserved with explicit correction. Separate r6b successor restores complete geometry and confirms upper-intake collision in both signs; route remains unresolved.
