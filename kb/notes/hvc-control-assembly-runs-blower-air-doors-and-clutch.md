---
title: "The dash control assembly runs the blower, air-door vacuum, and (with the PCM) the A/C clutch"
kind: how-it-works
source: "[[sources/hvc-blower-and-controls|Blower Motor, Resistor, Switch, and Control Assembly (FSM)]]"
related:
  - "[[notes/hvc-blower-resistor-sets-the-lower-fan-speeds|The blower resistor drops voltage for the lower fan speeds]]"
  - "[[notes/hvc-vacuum-reservoir-holds-air-door-position-under-load|The vacuum reservoir keeps the air doors in position when manifold vacuum drops]]"
  - "[[notes/hvc-pcm-trims-idle-air-when-the-ac-clutch-engages|The PCM raises idle air when the A/C clutch engages]]"
tags: [hvac, control-assembly, blower-motor, air-doors, vacuum]
---

The dash Control Assembly is the operator's single interface to three otherwise separate
subsystems on the 1994 F-150 HVAC system (inventory id `hvac`). Working with vacuum valves,
it controls the vacuum that positions the system air doors (selecting panel/floor/defrost
mode). Its switch also controls blower motor operation, and — together with the powertrain
control module — the A/C clutch.

Because one assembly drives electrical (blower, clutch request) and vacuum (mode doors)
functions at once, a single control fault can present as several unrelated-looking symptoms.
The FSM provides component-test, terminal-identification, and schematic figures for diagnosing
it.

## Related Concepts

- [[notes/hvc-blower-resistor-sets-the-lower-fan-speeds|The blower resistor drops voltage for the lower fan speeds]]
- [[notes/hvc-vacuum-reservoir-holds-air-door-position-under-load|The vacuum reservoir keeps the air doors in position when manifold vacuum drops]]
- [[notes/hvc-pcm-trims-idle-air-when-the-ac-clutch-engages|The PCM raises idle air when the A/C clutch engages]]

## Source

- [[sources/hvc-blower-and-controls|Blower Motor, Resistor, Switch, and Control Assembly (FSM)]]
