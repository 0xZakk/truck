---
title: "The blower resistor drops voltage for the lower fan speeds, so a failed resistor leaves only HIGH"
kind: how-it-works
source: "[[sources/hvc-blower-and-controls|Blower Motor, Resistor, Switch, and Control Assembly (FSM)]]"
related:
  - "[[notes/hvc-control-assembly-runs-blower-air-doors-and-clutch|The dash control assembly runs the blower, air-door vacuum, and (with the PCM) the A/C clutch]]"
tags: [hvac, blower-resistor, blower-motor, fan-speed]
---

The blower motor resistor on the 1994 F-150 (inventory id `hvac`) limits blower motor current
so the fan runs at LO, MED-LO, MED-HI, or HI. Each of the lower speeds routes the motor
current through more of the resistor's resistance elements, dropping more voltage and turning
the motor slower.

A practical consequence: the HIGH position normally bypasses the resistor and feeds the motor
full battery voltage. So when the resistor (or its thermal fuse) fails open, the truck loses
every speed except HIGH — the classic "only blows on 4" symptom — because only HIGH does not
depend on the resistor.

## Related Concepts

- [[notes/hvc-control-assembly-runs-blower-air-doors-and-clutch|The dash control assembly runs the blower, air-door vacuum, and (with the PCM) the A/C clutch]]

## Source

- [[sources/hvc-blower-and-controls|Blower Motor, Resistor, Switch, and Control Assembly (FSM)]]
