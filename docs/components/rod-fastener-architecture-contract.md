# Component contract and handoff: rod fastener architecture

Engine #32; root integration owner. Baseline `3dcbd364ac24396e671d5d16b930571713b7be0a`; branch `engine/timing-drive-fit`. Own this file and `reference/engine/rod-fastener-architecture-evidence.json`. Research only; no block, rod, fastener, frozen report, shared manifest or viewer changes. Preserve current journal/pin centers, bearing dimensions, rod length, corrected motion and stable IDs. Preserving these interfaces does not make every inherited dimension factory-verified.

**Decision: no coherent dimensional repair is supported yet.** The failure is a bolt-head witness against an estimated block cavity, but both the fastener seating architecture and crankcase contour need evidence. Do not cut the block, shrink the head or reverse the bolt to obtain clearance.

## Architecture findings

The actual exact-year image292722974 was re-inspected. It places the bolt head on the rod side above the split and the nut below the cap; this agrees with the current model's direction. The numbered rod side faces the camshaft and the piston notches face the engine front. The elevation shows a low head silhouette and rod shoulder, but supplies neither head plan outline nor under-head dimensions. It cannot justify a different clocking angle or head thickness.

ARP's manufacturer-authored [152-6002 instructions](https://www.tzr-motorsport.de/WebRoot/Store20/Shops/61911476/MediaGallery/PDF/ARP/Ford/152-6002.pdf) describe a press-fit replacement, an under-head radius requiring a rod-hole chamfer, and rod resizing following bolt installation. This is a bolt-and-rod seating problem, not merely a free-standing bolt envelope. No manufacturer fit diameter, shoulder length or seat dimensions were retrieved.

[ARP2026 page49](https://arpcatalog.com/49/) lists 4.9L kit152-6002 head styleM and separate240–300 kit152-6001 styleG, with explicit head-style verification against page46. The actual styleM photo was not obtained: kit page timed out, and text-only catalog retrieval omitted the photos. An older manufacturer-authored catalog excerpt surfaced with a different letterC for the same kit; its PDF timed out. Letter codes must therefore remain edition-bound, not treated as universal geometric specifications. Product-image searches returned other kits/generic charts; they were not accepted as an applicable photo. No reliable dimensional OEM/ARP head or rod-shoulder drawing emerged from this focused search.

The industrial Ford parts search index adds a **research lead**, E3TZ-6200-E rod with C4OZ-6214-B bolt, while exact-year service listing is E3TZ6200ERM. The indexed table was not visually verified and industrial applicability cannot establish the 1994 bolt identity. It is not sufficient to substitute either ARP kit or that bolt number.

Current source has boltØ8 in aØ8.4 rod hole:0.4mm diametral clearance rather than a modeled press shoulder. Its assumed head is a5mm-high regular hex prism atZ22..27, on the rod boss endingZ22. Rod bosses are14mm wide, centeredY±34.5; rod width23mm and outer radius39mm are also assumptions. The frozen diagnostic proves exact replay and the same collision in canonical/corrected geometry:2.716027965mm³ at local55°, with witness bolt-local `(0,−5.855617709,26.592893509)` and crank radial distance98.179965mm versus estimatedR98 cavity. The earlier21-pose scan is not a global maximum proof. A smaller observed side silhouette does not establish a safe physical correction.

## Exact evidence needed for the next candidate

Use one identified applicable rod, cap, both bolts and nuts; record engineering marks and whether OEM or replacement. Define rod coordinates with big-end bore axisX, small-end center toward+Z, split planeZ0 and numbered/camshaft side explicitly identified.

| Capture / measurement | Required result and purpose |
|---|---|
| Head plan and two orthogonal side views, scale reference in each plane | Full asymmetric outline, orientation relative to rod and head height; decides whether current hex envelope is wrong |
| Bolt and rod seat together | Under-head radius/chamfer, bearing footprint and seatZ relative to split; establishes real support instead of lowering an unsupported head |
| Press/grip/thread profile | Diameters and axial extents, matching rod/cap bores and nut plane; reconstructs the actual clamped stack |
| Rod shoulder/boss survey | Both bolt center coordinates, local forging contour and edge distances from big-end bore; prevents retaining guessed bosses around a new bolt |
| Applicable block crankcase section | Local surface near the frozen witness tied to crank axis and cylinder station; distinguishes wrong bolt from wrongR98 cavity |

A manufacturer dimensioned bolt-and-seat drawing can replace the relevant measurements. A packaged kit photograph alone cannot. Front/numbered-side orientation must accompany the survey so no reflected or re-clocked bolt is silently introduced.

## Candidate boundary and gates

Future allowed scope is the paired fastener/rod-seat architecture, after root review of the measured parameters. Preserve journal/pin/bearing datums and rod length; change neither block nor dimensions solely for clearance. Require source replay of the old failure, unchanged protected regions, actual head/seat contact and under-head relief, press/grip/nut-stack coherence, native exported checks and a new declared motion sweep. Retain original failure controls. Replacement fidelity and OEM fidelity are separate claims.

Application/source review: PARTIAL, with exact-year orientation and replacement architecture supported. Dimensional correction and inherited motion: UNRESOLVED/FAIL. CAD/export N/A; browser, installed tests and learning NOT RUN. No new CAD or running processes. Inputs and source retrieval limitations are bound in the companion ledger. Root owns tracking; #32 stays open. Exact next action: obtain the five datum-linked captures above or an applicable drawing, rather than repeat generic product searches. Usage unavailable.
