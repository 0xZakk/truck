# Engine measurement priorities

Engine #32, root integration owner. Evidence-acquisition plan only; no owner request has been sent and no vehicle disassembly is requested. Owned files: this plan and `inventory/engine/engine-measurement-priorities.json`. The JSON binds the current evidence and failure reports by hash, records the baseline, and lists detailed datums, affected components and alternatives. Existing CAD, reports and shared inventory remain unchanged.

Engineering priority is oil-pump architecture, rod fasteners, heater routing, ACT, then bearing internals. Acquisition can proceed differently: accessible heater/ACT photos are the smallest useful owner request, while pump and rod evidence needs identified spare parts or drawings.

## Minimal owner evidence bundle

If root later asks, request only:

1. One wide view of the water pump/heater tube and nearby intake/fuel rail/exhaust landmarks, plus accessible front and side views showing the tube entry and hose end.
2. One ACT/IAT location view and an accessible close view of its connector, hex and any readable tag/stamp.
3. Any existing pump/rod-bolt replacement receipts, box labels or prior service photos, if available.

Use an off, cool engine and accessible views only. No removal, unplugging or reaching past moving/hot components. A ruler is useful only if it can be placed beside the subject safely in the same depth plane; an unscaled photo still establishes topology. Do not ask the owner to dismantle the truck to satisfy this plan.

## 1. Oil-pump mounting and discharge

The old feet and inserted-tube joint contradict the source-supported raised mounting neck and pickup flange. The pressure route is incomplete. See [topology contract](oil-pump-topology-contract.md), [coverage audit](oil-pump-coverage-contract.md) and [topology delivery](../../inventory/engine/oil-pump-topology-delivery.json).

Acquire a dimensioned applicable pump drawing or an identified C5AZ6600A/M74 spare and matching donor block seat. Use drive axis as the primary datum, mounting face as axial zero and marked engine-front direction for clocking. Measure face outline; drive-axis-to-face distance; bolt, dowel and discharge centers; opening sizes; gasket thickness; and the independent pickup flange/bolt/inlet stack. Photograph each face square-on plus two perpendicular elevations. The block receiver/gallery must be surveyed relative to crank axis/front face; the pump alone cannot prove the hidden block route.

This unlocks housing, two gasket interfaces, dowel, mounting hardware, pickup and block-gallery connection, with possible drive-shaft engagement implications. Exterior owner photographs cannot expose these internal interfaces. Exact installed revision requires records or an identified original specimen; a measured replacement remains a replacement comparison.

## 2. Rod fastener and shoulder architecture

Preserve the six inherited motion failures in [rod-bolt conflict validation](../../inventory/engine/engine-corrected-rod-bolt-conflict-validation.json) and [combined-motion report](../../inventory/engine/engine-corrected-combined-motion-validation.json). The [architecture contract](rod-fastener-architecture-contract.md) supports bolt direction but leaves head/seat construction unresolved.

Survey an identified spare rod/cap/bolt assembly or obtain applicable manufacturer drawings. Use big-end bore axis, split plane and small-end axis; mark front and numbered/cam side. Capture head plan and two elevations, then measure asymmetric outline/height/clocking, under-head radius and seat plane, press shoulder/grip/thread extents, bolt axes and local rod shoulder. A matching donor block section near the frozen witness is needed to distinguish bolt error from the estimated crankcase cavity.

Bolt removal and rod inspection belong to a qualified spare-part survey, not the owner photo bundle. OEM and ARP152-6002 geometry must not be mixed. Existing receipts or prior teardown images may identify the installed hardware; without them, exact internal identity stays unknown until separately planned service. A donor can unlock a coherent comparison without cutting the modeled block for clearance.

## 3. Heater return tube routing

The [source candidate](waterpump-heater-source-candidate.md) has local contact/passage checks but its route collides with head, fuel rail, front manifold, lifting eye and stud13. Preserve [delivery](../../inventory/engine/waterpump-heater-source-delivery.json), [neighbor failures](../../inventory/engine/waterpump-heater-source-neighbors.json) and [stud follow-up](../../inventory/engine/waterpump-heater-source-stud.json).

Owner context photos can resolve actual departure direction and which neighbors the tube passes. Keep the pump shaft, rear mounting face and bolt pattern visible as common landmarks. A single oblique view cannot fix depth. For a dimensional candidate, obtain front/side/top views and measurements of an identified pump/tube specimen: OD, entry coordinates, bend stations, terminal axis/reach, bead and insertion. The current projected agreement does not define a manufacturing tolerance; perspective dominates the weak axial endpoint.

An identified assembled VIN-Y donor or manufacturer orthographic drawing is an alternative. Actual-truck routing or modifications still require owner evidence. Do not use a collision-free invented route as a substitute for the missing observation.

## 4. ACT/IAT sensor

The [identity study](act-sensor-identity.md) establishes F2DZ12A697A service listing with “Order By Tag Number” and a documented MTE5041 replacement bridge. Supported replacement data include3/8-18NPTF and25mm hex; probe reach, overall length and connector dimensions remain unknown. The [electrical map](../../reference/engine/engine-control-electrical-map.json) establishes C164, not its physical cavity orientation.

Owner location/tag photos can identify the actual sensor without unplugging it. Measure an identified spare or obtain the manufacturer's drawing: tip reach relative to a declared thread gauge plane, hex thickness, keyed connector shape, terminal spacing/recess and mating connector. The host manifold needs port axis/gauge-plane and internal wall/airflow clearance. Torque cannot establish installed depth or prove the hex seats on the manifold.

MTE5041 or Walker210-1002 drawings/specimens are useful alternatives with documented interchange. Exact original engineering stamp still depends on owner/identified-original evidence. Package dimensions remain excluded. A complete replacement specimen can support a separate comparison even if the original tag cannot be read.

## 5. Water-pump bearing internals

The [bearing coverage contract](waterpump-bearing-coverage-contract.md) and [evidence ledger](../../reference/engine/waterpump-bearing-coverage-evidence.json) confirm a cartridge placeholder and no applicable bearing identity. Generic standard sizes do not justify a selected internal design.

First obtain pump revision and bearing supplier/marking. An applicable manufacturer internal drawing is preferable; otherwise use an identified spare or retired pump for a qualified bench survey. Record ring OD/length, stepped shaft and hub/impeller/seal stations, row types/counts, elements, cages and end seals, all relative to shaft axis and rear mounting face. Any teardown/sectioning is a separate spare-part task, with damage recorded. External photos cannot reveal bearing rows.

This unlocks a real component breakdown while protecting housing, pulley, impeller, coolant seal and weep interfaces. Exact installed internals require traceability or an identified retired original. No request to remove a functioning pump is part of this plan.

## Evidence quality and stopping rule

Keep one specimen identity across views. Record units inmm, instrument type/resolution and repeat readings; list inaccessible features explicitly. Camera scale and instrument display resolution are not guaranteed measurement accuracy. Use in-plane scale and perpendicular views; preserve signed orientation to avoid reflected or re-clocked geometry. Root should accept each measurement's uncertainty before CAD changes, according to the interface it controls.

Do not repeat broad image/catalog searches for these gaps. Restart only when the named datum/identity evidence arrives, or root explicitly authorizes a bounded illustrative study. Public drawings and identified donors can avoid owner disassembly, but cannot prove the truck's actual modifications or unseen installed revision. This plan makes that boundary explicit rather than converting missing evidence into dimensions.

Validation: all referenced repository paths exist and are hash-bound in the JSON. No new research or source copies; no CAD/installation/browser checks applicable to this planning delivery. Root review pending, #32 remains open. No running processes; usage unavailable.
