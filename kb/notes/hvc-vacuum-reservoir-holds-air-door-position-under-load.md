---
title: "The vacuum reservoir keeps the air doors in position when manifold vacuum drops"
kind: how-it-works
source: "[[sources/hvc-vacuum-control-system|HVAC Vacuum Control System — Reservoir and Harness (FSM)]]"
related:
  - "[[notes/hvc-vacuum-reservoir-leak-down-test|Leak-test the HVAC vacuum reservoir: under 0.5 in Hg loss in 60 seconds]]"
  - "[[notes/hvc-control-assembly-runs-blower-air-doors-and-clutch|The dash control assembly runs the blower, air-door vacuum, and (with the PCM) the A/C clutch]]"
tags: [hvac, vacuum-reservoir, air-doors, mode-control]
---

The HVAC air doors on the 1994 F-150 (inventory id `hvac`) are moved by engine vacuum, but
manifold vacuum collapses under load and during acceleration — exactly when the doors should
stay put. The vacuum reservoir solves this by storing a charge of vacuum so the signal lines
don't fluctuate or suddenly drop, keeping the mode doors in their selected position.

This is why a failed reservoir or check valve typically shows up as the vents defaulting to
defrost (the no-vacuum position) under acceleration or while climbing a hill — the doors lose
their stored vacuum just when the engine stops supplying it.

## Related Concepts

- [[notes/hvc-vacuum-reservoir-leak-down-test|Leak-test the HVAC vacuum reservoir: under 0.5 in Hg loss in 60 seconds]]
- [[notes/hvc-control-assembly-runs-blower-air-doors-and-clutch|The dash control assembly runs the blower, air-door vacuum, and (with the PCM) the A/C clutch]]

## Source

- [[sources/hvc-vacuum-control-system|HVAC Vacuum Control System — Reservoir and Harness (FSM)]]
