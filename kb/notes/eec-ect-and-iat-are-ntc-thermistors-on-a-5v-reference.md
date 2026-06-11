---
title: "The ECT and IAT are negative-coefficient thermistors whose voltage drop falls as temperature rises"
kind: how-it-works
source: "[[sources/eec-temperature-sensors-ect-iat|ECT and IAT Temperature Sensors — Operation, DTCs, and Specs (FSM)]]"
related:
  - "[[notes/eec-ntc-temp-sensors-read-falsely-cold-with-bad-grounds|A bad ground or corroded connection makes the ECT and IAT read falsely cold]]"
tags:
  - ect
  - iat
  - thermistor
  - engine
---

The Engine Coolant Temperature (ECT) and Intake Air Temperature (IAT) sensors are both two-lead
thermistors with a negative temperature coefficient. The PCM applies a 5.0 V reference to the
signal lead with the return on a common sensor ground. As the medium (coolant or intake air)
warms, sensor resistance drops, so the voltage drop across the sensor decreases — the PCM reads
temperature as a voltage.

Their normal voltage ranges differ because they track different media: the ECT runs 3.50 V at
50 deg F down to 0.35 V at 230 deg F, while the IAT runs 3.50 V at 50 deg F down to 1.02 V at
158 deg F. The PCM combines both with MAP and TP data to set fuel injection base pulse width,
EGR flow, and ignition timing for the `engine`. They share the same self-test value table, and
coolant must exceed 50 deg F (KOEO) or 180 deg F (KOER) to pass.

## Related Concepts

- [[notes/eec-ntc-temp-sensors-read-falsely-cold-with-bad-grounds|A bad ground or corroded connection makes the ECT and IAT read falsely cold]]
- [[notes/sen-iat-shares-the-ect-thermistor-design|The IAT sensor is the same negative-coefficient thermistor as the ECT but measures incoming air rather than coolant]]
- [[notes/sen-ect-resistance-falls-as-coolant-warms|The ECT is a negative-coefficient thermistor whose voltage drops as the engine warms, and a bad ground reads falsely cold]]
- [[notes/eng-ect-sensor-is-an-ntc-thermistor-the-pcm-reads-as-voltage|The ECT sensor is an NTC thermistor whose voltage the PCM reads as coolant temperature]]
- [[notes/dtc-temperature-sensor-codes-pair-low-and-high-voltage|Temperature sensor DTCs come in low/high pairs that mean shorted (254°F) or open (-40°F)]]

## Source

- [[sources/eec-temperature-sensors-ect-iat|ECT and IAT Temperature Sensors — Operation, DTCs, and Specs (FSM)]]
