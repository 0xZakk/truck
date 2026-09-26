---
title: "Oil filter construction and Ford 4.9L mounting references"
source: reference/engine/oil-filter-reviewed.json
type: local
date: 2026-09-24
author: "Ford, Motorcraft and WIX"
tags: [lubrication, oil-filter, ford-300, replacement-parts]
processed: false
---

## Summary

The factory catalog identifies D9AZ-6731-A / FL-1A. Ford bulletin 95-8-8 distinguishes the disposable filter from the E4TZ-6890-A anti-drainback mounting insert. These are separate components; the insert must not be conflated with the flexible anti-drainback valve inside the filter.

WIX publishes a 93 mm diameter, 132 mm height, 3/4-16 thread and 72/63/5 mm gasket for its 51515. These are replacement comparison dimensions, not a Ford production drawing. The manufacturer lists an anti-drainback valve and an 8–11 psi bypass range; the CAD spring is not calibrated to this pressure.

The Motorcraft cutaway document illustrates a steel shell, folded media, center tube, end caps, anti-drainback valve, bypass components and tension clip. Its comparison pages identify FL-820S, so their dimensions and pleat counts cannot establish FL-1A internals. The current model combines a published replacement envelope with provisional internal teaching geometry. Its block placement and mounting connection remain unresolved.

## Captured Content

- Reviewed evidence: `reference/engine/oil-filter-reviewed.json`.
- Motorcraft document: `manuals/manufacturer-catalogs/motorcraft-oil-filter-cutaway.pdf`; PDF page 2 visually reviewed.
- Factory bulletin: source `fsm-d975f341ee63` in the engine source index.
- Ford industrial CSG649, PDF page 33, figure 60: mounting illustration only, not a dimensioned 1994 truck reference.
- [WIX 51515 specifications](https://m.wixfilters.com/Search/PartDetail?PartID=193964+&Source=WESR).
- [Ford FL-1A product page](https://www.ford.com/product/engine-oil-filter-p4000045182).

## Key Points

- Filter bypass, pump pressure relief and adapter drainback control perform different functions.
- Exact internal shapes, pleat count, media properties and valve calibration remain unverified.
- Collision-free CAD does not establish production accuracy or filtration performance.

## Placement review

The archived 1994 factory lubrication schematic (image `354634388.png`, source
`fsm-6f023139b5f8`) shows the filter on the camshaft/main-gallery side. The CAD
camshaft is on negative Y; the original positive-Y staged filter was therefore on
the wrong side. Its placement has been mirrored to the cam side. This establishes
the side relationship only, not a measured station or angle. Evidence and explicit
limits are saved in `reference/engine/oil-filter-placement-reviewed.json`.
