# Fuel rail candidate: pre-CAD path amendment

Research candidate under #82; baseline aca7a20a. Own fuel-rail-candidate-20261003-prefixed CAD/scripts/generated/docs only. No canonical writes. Parent approved q=.75 and BOTH transverse study signs, not installed geometry. Prior layout/source deliveries remain frozen. Every dimension below is an explicit educational estimate; neither sign is selected by clearance.

## Frame and exact tangent paths

Let s=+1 or−1; regulator origin G=(174.136,−163+24s,385). Coordinates are engine mm. Preserve six injector axes/cups and all three rail seat/hardware interfaces. Main supply tube OD12/ID9 atY−163,Z369. Adjacent return OD8/ID5.6 atY=Gy,Z369. Keep source ear and all nine apertures.

**Forward supply loop:** extend main supply rail along+X to A=(280.618,−163,369). A tilted semicircle has center C=(280.618,−163+12s,364), radius13, and equation C+(13 sinθ,−12s cosθ,5 cosθ), θ=0…π. It ends B=(280.618,Gy,359), with tangent−X; front tip remainsX293.618. This replaces the earlier schematic horizontalR18 loop with a tiltedR13 loop to bridge the two estimated levels with exact tangents, not to avoid neighbors. Straight−X to D=(204.136,Gy,359). Quarter-circle center E=(204.136,Gy,377), radius18: E+(−18 sinθ,0,−18 cosθ), θ=0…π/2. End F=(186.136,Gy,377), tangent+Z. Straight+Z to flange supply entry S=(186.136,Gy,381). Last4mm transitions bore radius4.5→3; outside radius6 unchanged. R13/R18 are geometric estimates, not manufacturer bend limits; no branch is optimized against clearance.

**Return path:** central outlet starts T=(174.136,Gy,383.5), tangent−Z, straight to U=(174.136,Gy,381). Quarter-circle center V=(162.136,Gy,381), radius12, V+(12 cosθ,0,−12 sinθ), θ=0…π/2. End W=(162.136,Gy,369), tangent−X. Continue toward rear upturn. Separate return stem outer radius4.5 fromZ377 to383.5, central bore2.8, transitions to OD8 below; subtract groove major radius4.25/minor.25 atZ378 for retained regulator O-ring study. Never join supply and return bores directly.

**Rear supply:** straight atY−163/Z369 to(−336.997,−163,369), quarterR18 centered(−336.997,−163,387), parameter center+(−18 sinθ,0,−18 cosθ). End(−354.997,−163,387), straight+Z to coupling datum(−354.997,−163,410). Straight sealing lead23mm.

**Rear return:** straight atGy/Z369 to(−320.238,Gy,369), quarterR12 centered(−320.238,Gy,381), same parameter form. End(−332.238,Gy,381), straight+Z to datum(−332.238,Gy,410). Lead29mm. Both tube end faces coincide with existing scaled male-neck localZ=0 plane; bores match supplyr4.5/returnr2.8. GroupRy90deg composes with childRy−90deg to yield exit+Z. Preserve children, seals and relative construction; roll remains an estimate. No 15mm stub addition is silently inserted into fitting engagement.

## Independent supply and valve-controlled return

Replace the existing central-bore regulator flange. Proposed flange topZ383, bottomZ377.5, radius20 plus existing three screw ears at local radius24. Supply annular gallery radii7…16 occupiesZ379…383; feedr3 at(Gx+12,Gy) opens into it. Central return stemr4.5 is isolated by solid land to galleryinnerR7; minimum radial land2.5mm. Flange central socketr4.55 remains separate from gallery; nominal radial fit.05mm is an estimate, not a pressure seal specification.

The retained gasket atZ383…384 and lower housing floor atZ384…386 currently block an annular inlet. Rebuild their existing stable definitions with eight inlet holes radius2.5 centered on radius11.5 at45deg increments, aligned across both parts. They connect gallery to the lower pressure chamber, retaining central seal land. Existing lower-housing occurrence+Z1 is accounted for when authoring its local geometry. No accidental floor is claimed as an inlet.

Retain regulator-valve-seat: annularR4.4/r1.8 atZ383.5…384.5, and its seated ball/stem as the illustrative control. Supply enters the chamber outside the central seat, then may pass only through the seat'sr1.8 opening into central return. Pressure chamber extends to diaphragm undersideZ389.1. Replace the solid inlet-screen envelope with eight through holesr1.2 onradius11.5 at45deg increments, aligned to floor passages; it is an illustrative perforated screen, not production mesh. Preserve screen ID and position. Diaphragm/spring/upper housing/internal relative positions otherwise remain, all illustrative.

Required topology tests: gallery→eight inlet holes→pressure chamber connected; pressure chamber→return closed with seated valve and open with an explicitly displaced valve study. Do not confuse shared chamber adjacency with a bypass. Closed-state zero-volume contact at the seat is idealized, not leakage validation. A sealed diaphragm separates pressure chamber from vacuum chamber. Quantitative hydraulic performance, screen pressure drop, O-ring compression and valve calibration are NOT modeled. Blocking one inlet and directly drilling gallery-to-return are distinct negative controls; the second must fail the isolation check even if overall fuel continuity improves.

## Vacuum and review boundary

Use the approved layout's moved nipple/start and fixed manifold fitting with mirroredY start for s−1; retain end tangent+Y and upper port unchanged. Exact hose geometry may be constructed after this amendment is approved but must report curvature/interference without moving endpoints to fit. Diagnostic port remains(100,−163,378), three mount seats and injector seals unchanged. All13 regulator occurrences, both coupling groups and vacuum hose remain in coordinated context scope.

This amendment requires root review before CAD construction. Builder scaffolding may prepare path sampling and hash checks meanwhile. Minimum geometric bend checksR>outerradius, tangent continuity, hollow continuity and self-intersection required; no production forming claim. Full context/ear/fastener/tool access and export/source render gates remain required for both signs. No shared installation or side acceptance.
