---
title: "Melling catalog identifies distinct 300 intake and exhaust springs"
source: "https://images.carid.com/melling/info/pdf/melling-engine-parts-catalog.pdf"
type: pdf
date: 2026-10-03
author: "Melling; hosted by CARiD"
tags: [engine, valve-springs, replacement-comparison]
processed: true
---

## Summary

The Ford Truck 300 application table lists VS-2215 intake and VS-2216 exhaust springs for 1992–1996. This is replacement application evidence, not identification of the springs physically installed in the owner's truck. The separate dimension table supplies different free heights, wire diameters and turn counts.

The catalog's outside diameter, inside diameter and wire diameter do not close geometrically: both rows differ by 0.009 inch (0.2286 mm). Candidate modeling prioritizes outside diameter and wire diameter and explicitly derives a different inside diameter. Ground end transitions remain inferred; the table is not a complete manufacturing drawing.

## Key Points

- Application: PDF page 111, printed page 116.
- Dimensions: PDF page 263, printed page 268; inch values are the reference, not rounded whole-millimeter lookup fields.
- Atomic interpretation: [[notes/melling-300-intake-exhaust-springs-differ|Intake and exhaust springs require different geometry]].
- Earlier [[sources/melling-spring-specifications|Spring kit table]] remains a rejected source for these stock replacement part numbers.

## Captured Content

PDF SHA-256: `547973b73b028a0e2b4115a6129975a9bc3505211dd2a9dfc9410576dd9b7d7b`.

Normalized local captures: `kb/.raw/melling-300-spring-application-20261003-111-111.txt` and `kb/.raw/melling-300-spring-dimensions-20261003-263-263.txt`. Reproduce with `tools/ingest.py` on the downloaded PDF using `--type pdf --pages 111-111` and `--pages 263-263`. PDF and raw captures are excluded from Git. Source dimensions and candidate limitations are recorded under `reference/engine/valve-spring-reconciliation-20261003*` and the corresponding component handoffs.
