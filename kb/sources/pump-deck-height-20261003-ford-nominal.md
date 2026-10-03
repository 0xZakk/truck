---
title: "Ford Racing lists the 300 inline-six nominal deck height as 10.000 inches"
source: https://www.trackey.ford.com/download/pdfs/EngineDimensions.pdf
type: pdf
date: 2026-10-03
author: "Ford Racing"
tags: [engine, block, dimensions, water-pump, primary-source]
processed: true
---

## Summary

Ford's public two-page Basic Engine Dimensions document gives a nominal deck height of 10.000 inches for the 300 I-6 covering 1965–96. Page 1's table header and row were checked in an actual raster of the downloaded PDF, so the figure is associated with deck height rather than a neighboring column. The nominal conversion is 254.000 mm.

This is a manufacturer family reference applicable to 1994, not a measurement of the owner's particular block, a casting tolerance, a machining limit, or evidence of a block-front mounting pattern. It supports retaining the reconstruction's nominal 254 mm deck datum. A photograph-based pump/cover registration that implies a roughly 290 mm deck under its inherited scale must be reconsidered; it does not justify raising the deck.

## Key Points

- PDF page 1, row `300 I-6`, years `1965-96`, column `DECK HEIGHT`: `10.000` inches.
- Download SHA256: `0e81983110834897b86bbb06023f5f1df4381ab9e9174c35a18a425f4430049c`.
- Retrieval and raster review: 2026-10-03. Raw PDF and manufacturer pixels are excluded from Git and generated-candidate archives.
- Ingestion ran through `tools/ingest.py --type pdf --pages 1-1`; normalized extraction is locally ignored under `kb/.raw/pump-deck-height-20261003-1-1.txt`. Authored capture here suffices to reproduce the claim from the public URL.
- Derived numeric comparison: `reference/engine/pump-cover-candidate-20261003-deck-registration.json`; no new CAD or assembly change follows automatically.

## Captured Content

The row identifies the engine family, year span, and nominal deck height above. The complete nominal row is retained for a separate future core audit; no rotating geometry is changed here.

| Field | Catalog inches | Converted mm |
|---|---:|---:|
| Bore | 4.000 | 101.600 |
| Stroke | 3.980 | 101.092 |
| Bore spacing | 4.480 | 113.792 |
| Main journal diameter | 2.399 | 60.9346 |
| Rod journal diameter | 2.123 | 53.9242 |
| Connecting rod length, mean | 6.210 | 157.734 |
| Deck height | 10.000 | 254.000 |
| Piston compression height | 1.757 | 44.6278 |

All entries are nominal family references; none supplies production tolerances. A first system-Python ingestion failed because pypdf was absent; the bundled artifact Python succeeded, without changing project dependencies.
