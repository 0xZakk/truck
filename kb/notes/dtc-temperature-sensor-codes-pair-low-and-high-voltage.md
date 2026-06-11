---
title: "Temperature sensor DTCs come in low/high pairs that mean shorted (254°F) or open (-40°F)"
kind: troubleshooting
source: "[[sources/dtc-air-fuel-sensor-codes|EEC DTCs 112-195 — Air, Fuel, and Sensor Input Codes (FSM)]]"
related:
  - "[[notes/dtc-rationality-codes-flag-readings-that-disagree-with-other-sensors|Rationality DTCs flag a sensor reading that disagrees with the rest of the engine picture rather than a broken circuit]]"
  - "[[notes/dtc-hard-codes-vs-memory-codes-mean-present-vs-stored|A hard code is a fault present during the test, while a memory code was stored from earlier driving]]"
tags:
  - dtc
  - intake-air-temperature
  - engine-coolant-temperature
  - troubleshooting
  - engine
---

The intake air temperature (IAT) and engine coolant temperature (ECT) sensors are
thermistors whose resistance falls as they warm, so the PCM reads a falling voltage with
rising temperature. That physics is why their fault codes come in mirror-image pairs. A
**below-minimum-voltage** code means the circuit is effectively shorted to ground, which the
PCM interprets as impossibly hot — the FSM annotates it as "254 degrees F indicated." An
**above-maximum-voltage** code means the circuit is open, read as impossibly cold, annotated
"-40 degrees F indicated."

For IAT the pair is DTC 112 (low / 254°F) and 113 (high / -40°F); for ECT it is 117 (low /
254°F) and 118 (high / -40°F). The implausible temperature in the code text is the giveaway:
a real intake or coolant temperature of 254°F or -40°F almost never happens, so seeing that
number flags an electrical fault rather than a genuine thermal condition. The matching
transmission fluid temperature sensor uses the same scheme (637 open / -40°F, 638 shorted /
290°F).

On this truck's `engine`, these codes point straight at the sensor, its connector, or the
wiring rather than at an actual overheat or freeze condition.

## Related Concepts

- [[notes/dtc-rationality-codes-flag-readings-that-disagree-with-other-sensors|Rationality DTCs flag a sensor reading that disagrees with the rest of the engine picture rather than a broken circuit]]
- [[notes/dtc-hard-codes-vs-memory-codes-mean-present-vs-stored|A hard code is a fault present during the test, while a memory code was stored from earlier driving]]
- [[notes/eng-a-bad-ect-connection-reads-colder-than-actual|A bad ECT connection or added resistance reads colder than actual]]
- [[notes/eec-ect-and-iat-are-ntc-thermistors-on-a-5v-reference|The ECT and IAT are negative-coefficient thermistors whose voltage drop falls as temperature rises]]
- [[notes/sen-ect-resistance-falls-as-coolant-warms|The ECT is a negative-coefficient thermistor whose voltage drops as the engine warms, and a bad ground reads falsely cold]]
- [[notes/eec-ntc-temp-sensors-read-falsely-cold-with-bad-grounds|A bad ground or corroded connection makes the ECT and IAT read falsely cold]]
- [[notes/sen-iat-shares-the-ect-thermistor-design|The IAT sensor is the same negative-coefficient thermistor as the ECT but measures incoming air rather than coolant]]

## Source

- [[sources/dtc-air-fuel-sensor-codes|EEC DTCs 112-195 — Air, Fuel, and Sensor Input Codes (FSM)]]
