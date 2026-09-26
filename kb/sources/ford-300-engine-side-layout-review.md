---
title: "Ford 300 exploded drawings establish opposite manifold and pushrod-cover sides"
source: reference/engine/engine-side-layout-reviewed.json
type: local
date: 2026-09-24
author: "Ford; local diagram review"
tags: [engine, geometry, block, valvetrain, lubrication]
processed: false
---

## Summary

The Ford industrial parts book's external and internal exploded drawings (PDF pages 7–8, printed 4–5) place the pushrod cover, camshaft, oil filter and distributor on the side opposite the intake/exhaust manifolds. The archived EFI engine exploded drawing corroborates the cover/manifold relationship, and the 1994 lubrication schematic places the filter on the cam/gallery side. These establish a relative arrangement, not surveyed coordinates or industrial-part interchangeability.

The earlier CAD core had its cam and pushrods on the manifold side, despite putting the distributor and spark plugs on the opposite face. The correction retains the manifold face at negative Y and assigns the cam, lifters and pushrods to positive Y. Matching bores, rocker supports, gear centers and lubrication studies must move together. Their distances and detailed production interfaces remain provisional.

## Key Points

- A clear static interference check cannot prove that components occupy the correct sides of an engine.
- The previous filter placement review correctly associated the filter with the cam, but inherited the core's incorrect side assignment. Its earlier negative-Y coordinate is superseded by this layout correction.
- The missing pushrod-cover study should follow the corrected cam side, with a real block opening and gasket interface rather than a floating cover over a solid wall.
- Industrial printed page 14 (PDF 17) lists C5AZ-6519-B cover, C5AZ-6521-A gasket, six B9A-6570-A grommets and six 20386-S8 bolts described as 5/16-18 × 1.0. These are comparison search targets, not confirmed 1994 identities or dimensions of the cover.

## Captured Content

`reference/engine/engine-side-layout-reviewed.json` records the diagram paths and coordinate decision. `kb/.raw/ford-300-engine-side-layout-review.txt` contains the ingestion capture.

See [[sources/fel-pro-vin-y-engine-gasket-applications|VIN-Y gasket applications]] for the applicable replacement catalog's six pushrod-cover grommets and alternative gasket sets.
