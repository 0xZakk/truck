---
title: "The power steering pressure/flow test isolates pump, gear, or hose faults"
kind: procedure
source: "[[sources/sus-power-steering-pump|Power Steering Pump (Ford CII) (FSM)]]"
related:
  - "[[notes/sus-power-steering-pump-is-a-belt-driven-cii-slipper-pump-with-swiveling-pressure-fitting|The power steering pump is a belt-driven Ford CII slipper pump]]"
  - "[[notes/sus-cii-pump-relief-is-1300-1530-psi-and-min-flow-1-4-gpm|CII pump relief pressure is 1300-1530 psi with min flow around 1.4 GPM]]"
tags:
  - steering
  - power-steering
  - diagnosis
---

For "hard steering" or "lack of assist," the FSM uses a power steering analyzer (Rotunda
014-207 or equivalent) spliced in at the pump outlet, torquing the adapter connections to
15 ft lb. The analyzer reads backpressure, pump flow, gear internal leakage, and control-
valve/cylinder leakage, which together separate a weak pump from a restricted hose, a sticking
gear valve, a sticking relief valve, or even a binding suspension.

Key readings: run two minutes at idle and record flow; at 170 degrees, idle backpressure
above 150 psi points to a hose restriction or the gear. Partially close the gate valve to
build 740 psi (CII) or 620 psi (Saginaw) and recheck flow — a drop means a worn cam pack.
At the steering stops, flow should fall below 0.5 GPM and pressure should reach max pump
output; if it does not, there is excessive internal leakage in the gear's control valve.
Safety bound: system pressure can exceed 1500 psi, so never hold the gate valve closed more
than five seconds. This is the master diagnostic for the `steering` system's hydraulics.

## Related Concepts

- [[notes/sus-power-steering-pump-is-a-belt-driven-cii-slipper-pump-with-swiveling-pressure-fitting|The power steering pump is a belt-driven Ford CII slipper pump]]
- [[notes/sus-cii-pump-relief-is-1300-1530-psi-and-min-flow-1-4-gpm|CII pump relief pressure is 1300-1530 psi with min flow around 1.4 GPM]]

## Source

- [[sources/sus-power-steering-pump|Power Steering Pump (Ford CII) (FSM)]]
