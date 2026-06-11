---
title: "A bad ground or corroded connection makes the ECT and IAT read falsely cold"
kind: troubleshooting
source: "[[sources/eec-temperature-sensors-ect-iat|ECT and IAT Temperature Sensors — Operation, DTCs, and Specs (FSM)]]"
related:
  - "[[notes/eec-ect-and-iat-are-ntc-thermistors-on-a-5v-reference|The ECT and IAT are negative-coefficient thermistors whose voltage drop falls as temperature rises]]"
tags:
  - ect
  - iat
  - troubleshooting
  - grounds
  - engine
---

Both the ECT and IAT are negative-temperature-coefficient thermistors, meaning resistance
falls as temperature rises. Because added series resistance and a falling sensor resistance look
the same to the PCM, the FSM explicitly warns that poor electrical connections or minor harness
and ground resistance produce temperature readings *lower* than actual — sometimes much lower for
the IAT.

This matters because the PCM uses temperature to set fuel pulse width, EGR flow, and ignition
timing: a falsely-cold reading can drive a needlessly rich mixture and altered timing, causing
poor economy or driveability complaints with no obvious failed part. When chasing a temperature
DTC (ECT 21/116/61/117/51/118, IAT 24/114/64/112/54/113) on the `engine` system, inspect the
sensor grounds and connector pins before condemning the sensor.

## Related Concepts

- [[notes/eec-ect-and-iat-are-ntc-thermistors-on-a-5v-reference|The ECT and IAT are negative-coefficient thermistors whose voltage drop falls as temperature rises]]
- [[notes/sen-ect-resistance-falls-as-coolant-warms|The ECT is a negative-coefficient thermistor whose voltage drops as the engine warms, and a bad ground reads falsely cold]]
- [[notes/sen-iat-shares-the-ect-thermistor-design|The IAT sensor is the same negative-coefficient thermistor as the ECT but measures incoming air rather than coolant]]
- [[notes/eng-a-bad-ect-connection-reads-colder-than-actual|A bad ECT connection or added resistance reads colder than actual]]
- [[notes/dtc-temperature-sensor-codes-pair-low-and-high-voltage|Temperature sensor DTCs come in low/high pairs that mean shorted (254°F) or open (-40°F)]]

## Source

- [[sources/eec-temperature-sensors-ect-iat|ECT and IAT Temperature Sensors — Operation, DTCs, and Specs (FSM)]]
