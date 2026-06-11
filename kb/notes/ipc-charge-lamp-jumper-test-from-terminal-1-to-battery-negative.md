---
title: "A jumper from regulator terminal 1 to battery negative proves the charge lamp bulb and circuit"
kind: troubleshooting
source: "[[sources/ipc-charge-lamp-indicator|Charge Lamp / Indicator — Description, Operation and Testing (FSM)]]"
related:
  - "[[notes/ipc-charge-lamp-grounds-through-regulator-terminal-1|The charge lamp lights because the regulator grounds it through terminal 1 until the S-circuit voltage is reached]]"
tags:
  - charge-lamp
  - charging-system
  - troubleshooting
---

Symptom: the charge/alternator warning lamp does not light with the ignition ON and the
engine not running (it should). Because the lamp is ground-switched at regulator terminal
"1," the FSM test isolates whether the problem is upstream (bulb/feed) or in the regulator.

1. First check the indicator bulb. If the bulb is bad, replace it.
2. If the bulb is good, disconnect the regulator's electrical connector and jumper a wire
   from the connector's terminal "1" to the negative battery post clamp. With the ignition
   ON, the lamp should light.
3. If it lights with the jumper, the bulb and feed are good and the regulator (its internal
   indicator switch) was not grounding the lamp.
4. If it still does not light, repair the open in the circuit between the ignition switch and
   the regulator, or replace the 500-ohm resistor across the indicator lamp if the truck is
   so equipped.

This cleanly separates a cluster/bulb/wiring fault from a regulator fault in the
`electrical-body` charging circuit.

## Related Concepts

- [[notes/ipc-charge-lamp-grounds-through-regulator-terminal-1|The charge lamp lights because the regulator grounds it through terminal 1 until the S-circuit voltage is reached]]
- [[notes/charge-light-staying-on-points-to-regulator-or-stator-circuit|A charge light that stays on points to the regulator or stator circuit, not always a dead alternator]]
- [[notes/ipc-grounding-the-oil-lamp-wire-isolates-bulb-from-sender|Grounding the oil-lamp sender wire isolates a bad bulb from a bad pressure switch]]
- [[notes/ipc-voltmeter-normal-range-is-13-5-to-14-volts|A normal voltmeter reading on the F-150 is 13.5 to 14.0 volts]]

## Source

- [[sources/ipc-charge-lamp-indicator|Charge Lamp / Indicator — Description, Operation and Testing (FSM)]]
