---
title: "The ECT sensor is an NTC thermistor whose voltage the PCM reads as coolant temperature"
kind: how-it-works
source: "[[sources/eng-coolant-temperature-sensor|Engine Coolant Temperature (ECT) Sensor — Operation, Values & DTCs (FSM)]]"
related:
  - "[[notes/eng-a-bad-ect-connection-reads-colder-than-actual|A bad ECT connection or added resistance reads colder than actual]]"
tags:
  - cooling
  - ect-sensor
  - pcm
  - how-it-works
---

The Engine Coolant Temperature (ECT) sensor is a two-lead negative-temperature-coefficient
(NTC) thermistor: its resistance falls as the coolant warms. The PCM applies a 5.0-volt
reference to the signal lead against a common sensor ground, so as resistance drops the voltage
across the sensor drops too. The normal operating range runs from 3.50 V at 50 deg F down to
0.35 V at 230 deg F.

The PCM doesn't just drive a gauge with this — it uses coolant temperature to trim the
fuel-injection base pulse width, EGR flow, and ignition timing. That makes the ECT a key input
shared between the `cooling` and `engine` inventory systems: a wrong reading skews fueling and
timing, not just the temperature display.

> "The PCM applies a 5.0 volt reference voltage to the ECT signal lead ... As the temperature of
> the engine coolant increases the resistance of the ECT sensor decreases and correspondingly the
> voltage drop across the ECT sensor is reduced."

## Related Concepts

- [[notes/eng-a-bad-ect-connection-reads-colder-than-actual|A bad ECT connection or added resistance reads colder than actual]]
- [[notes/sen-ect-resistance-falls-as-coolant-warms|The ECT is a negative-coefficient thermistor whose voltage drops as the engine warms, and a bad ground reads falsely cold]]
- [[notes/eec-ect-and-iat-are-ntc-thermistors-on-a-5v-reference|The ECT and IAT are negative-coefficient thermistors whose voltage drop falls as temperature rises]]
- [[notes/eec-ntc-temp-sensors-read-falsely-cold-with-bad-grounds|A bad ground or corroded connection makes the ECT and IAT read falsely cold]]
- [[notes/dtc-temperature-sensor-codes-pair-low-and-high-voltage|Temperature sensor DTCs come in low/high pairs that mean shorted (254°F) or open (-40°F)]]

## Source

- [[sources/eng-coolant-temperature-sensor|Engine Coolant Temperature (ECT) Sensor — Operation, Values & DTCs (FSM)]]
