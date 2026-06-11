---
title: "A bad ECT connection or added resistance reads colder than actual"
kind: troubleshooting
source: "[[sources/eng-coolant-temperature-sensor|Engine Coolant Temperature (ECT) Sensor — Operation, Values & DTCs (FSM)]]"
related:
  - "[[notes/eng-ect-sensor-is-an-ntc-thermistor-the-pcm-reads-as-voltage|The ECT sensor is an NTC thermistor whose voltage the PCM reads as coolant temperature]]"
tags:
  - cooling
  - ect-sensor
  - troubleshooting
  - diagnosis
---

Because the ECT is a negative-temperature-coefficient sensor, extra resistance anywhere in its
circuit adds to the sensor's own resistance and the PCM interprets the higher total resistance as
a *colder* engine than it really is. The FSM specifically calls out poor electrical connections,
corroded harness pins, and weak ground connections as causes of temperature values that read
lower than actual. That false-cold input can make the PCM over-fuel (a cold-running rich
condition) even though the engine is at temperature.

The EEC-IV self-test flags ECT circuit faults with DTC 21/116 (output out of the 0.3-3.7 V
self-test range), 61/117 (below the 0.2 V minimum, e.g. a shorted-to-ground signal), and 51/118
(above the 4.6 V maximum, e.g. an open circuit). When chasing these on the `cooling`/`engine`
inventory systems, inspect connections and grounds before condemning the sensor.

> "Due to its negative temperature coefficient, poor electrical connections or minor increases in
> resistance across the ECT circuit harness and ground connections can result in temperature values
> that are lower than actual."

## Related Concepts

- [[notes/eng-ect-sensor-is-an-ntc-thermistor-the-pcm-reads-as-voltage|The ECT sensor is an NTC thermistor whose voltage the PCM reads as coolant temperature]]
- [[notes/sen-ect-resistance-falls-as-coolant-warms|The ECT is a negative-coefficient thermistor whose voltage drops as the engine warms, and a bad ground reads falsely cold]]
- [[notes/eec-ntc-temp-sensors-read-falsely-cold-with-bad-grounds|A bad ground or corroded connection makes the ECT and IAT read falsely cold]]
- [[notes/dtc-temperature-sensor-codes-pair-low-and-high-voltage|Temperature sensor DTCs come in low/high pairs that mean shorted (254°F) or open (-40°F)]]
- [[notes/sen-iat-shares-the-ect-thermistor-design|The IAT sensor is the same negative-coefficient thermistor as the ECT but measures incoming air rather than coolant]]

## Source

- [[sources/eng-coolant-temperature-sensor|Engine Coolant Temperature (ECT) Sensor — Operation, Values & DTCs (FSM)]]
