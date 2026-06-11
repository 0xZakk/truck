---
title: "The IAT sensor is the same negative-coefficient thermistor as the ECT but measures incoming air rather than coolant"
kind: how-it-works
source: "[[sources/sen-intake-air-temperature-sensor|Intake Air Temperature (IAT) Sensor — Description, Operation, and DTCs (FSM)]]"
related:
  - "[[notes/sen-ect-resistance-falls-as-coolant-warms|The ECT is a negative-coefficient thermistor whose voltage drops as the engine warms, and a bad ground reads falsely cold]]"
tags:
  - iat
  - thermistor
  - fuel
---

The IAT and ECT are the same kind of part: a two-lead, negative-temperature-coefficient
thermistor fed 5.0 V on the signal lead with a common SIG RTN ground. The FSM even reuses one
"descriptive schematic" for both. The only functional difference is what they sit in — the IAT
is mounted in the intake air-flow path and reports incoming air temperature, while the ECT is in
the coolant and reports engine temperature.

Air temperature matters because cold air is denser and carries more oxygen per unit volume. The
PCM uses IAT to correct the `fuel` base pulse width, EGR flow, and ignition timing for that air
density. The IAT's normal output spans about 3.50 V at 50°F to 1.02 V at 158°F.

Knowing the two sensors are electrically identical is a handy diagnostic shortcut: with the
engine cold and soaked overnight, IAT and ECT should read nearly the same temperature. A large
split between them at cold start points to a bad sensor or a high-resistance circuit on one of
the two, the same falsely-cold failure mode the ECT page warns about.

## Related Concepts

- [[notes/sen-ect-resistance-falls-as-coolant-warms|The ECT is a negative-coefficient thermistor whose voltage drops as the engine warms, and a bad ground reads falsely cold]]
- [[notes/eec-ect-and-iat-are-ntc-thermistors-on-a-5v-reference|The ECT and IAT are negative-coefficient thermistors whose voltage drop falls as temperature rises]]
- [[notes/eec-ntc-temp-sensors-read-falsely-cold-with-bad-grounds|A bad ground or corroded connection makes the ECT and IAT read falsely cold]]
- [[notes/dtc-temperature-sensor-codes-pair-low-and-high-voltage|Temperature sensor DTCs come in low/high pairs that mean shorted (254°F) or open (-40°F)]]
- [[notes/eng-a-bad-ect-connection-reads-colder-than-actual|A bad ECT connection or added resistance reads colder than actual]]

## Source

- [[sources/sen-intake-air-temperature-sensor|Intake Air Temperature (IAT) Sensor — Description, Operation, and DTCs (FSM)]]
