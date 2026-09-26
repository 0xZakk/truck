---
title: "The 1994 EVTM identifies the oil-pressure input as a switch"
source: manuals/evtm/1994-Bronco-F-Series-EVTM.pdf
type: pdf
date: 2026-09-24
author: "Ford Motor Company"
tags: [lubrication, oil-pressure, evtm, instrumentation]
processed: false
---

## Summary

EVTM printed page 60-2 (PDF page 183) shows a pressure switch, a fixed 20-ohm resistor in the instrument cluster and circuit 31, white/red. The accompanying description says the switch closes at normal oil pressure and opens at low pressure. The gauge therefore indicates a switch state rather than continuously measuring pressure. This application-specific circuit resolves the ambiguity in the archived generic magnetic-gauge description, which discusses a variable-resistance sender.

Printed page 151-1 (PDF page 312) locates connector C135 on the 4.9L engine. The location index, printed page 152-9 (PDF page 344), identifies the switch at the lower left rear near the oil filter. The factory parts listing gives E9TZ9278A. Switch internals, dimensions and operating threshold still need part-specific evidence; the circuit drawing does not establish them.

## Captured Content

Pages 60-2 and 151-1 visually reviewed. Facts and limitations are saved in `reference/engine/oil-pressure-switch-reviewed.json`. The existing purchased PDF was read locally without another download.

## Key Points

- Use switch behavior in the engine explanation; do not animate a proportional pressure sender.
- A normal dashboard indication is not a numerical pressure measurement.
- Diagnose the indication circuit separately from actual oil pressure.
- The schematic's short caption says oil level, but its operational note explicitly identifies pressure; do not turn this into a level-sensor model.
