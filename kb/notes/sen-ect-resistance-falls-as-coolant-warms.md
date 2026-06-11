---
title: "The ECT is a negative-coefficient thermistor whose voltage drops as the engine warms, and a bad ground reads falsely cold"
kind: troubleshooting
source: "[[sources/sen-engine-coolant-temperature-sensor|Engine Coolant Temperature (ECT) Sensor — Description, Operation, and DTCs (FSM)]]"
related:
  - "[[notes/sen-iat-shares-the-ect-thermistor-design|The IAT sensor is the same negative-coefficient thermistor as the ECT but measures incoming air rather than coolant]]"
  - "[[notes/sen-closed-loop-fuel-control-targets-14-7-1|Closed-loop fuel control on the 4.9L trims injector pulse width toward 14.7:1 using the HO2S feedback]]"
tags:
  - ect
  - thermistor
  - fuel
  - troubleshooting
---

The ECT is a two-lead thermistor with a *negative* temperature coefficient: hotter coolant
means lower resistance. The PCM puts 5.0 V on the signal lead through a fixed internal resistor,
so as the sensor's resistance falls the voltage measured across it falls too — from about
3.50 V at 50°F down to about 0.35 V at 230°F.

The diagnostic consequence the FSM calls out: because the coefficient is negative, *any* extra
resistance in the circuit — a corroded connector, a poor SIG RTN ground — adds to the sensor's
own resistance and makes the PCM read a lower temperature than reality. The engine looks colder
than it is, so the PCM commands warm-up enrichment that never ends: rich running, fouled plugs,
poor fuel economy, and delayed closed-loop entry, often with no stored ECT code because the
reading is still "in range."

For the `fuel` system, this makes ECT circuit cleanliness a first-look item when chasing a
rich condition. Self-test codes only catch gross faults: 21/116 (out of 0.3–3.7 V range),
61/117 (below 0.2 V), and 51/118 (above 4.6 V).

## Related Concepts

- [[notes/sen-iat-shares-the-ect-thermistor-design|The IAT sensor is the same negative-coefficient thermistor as the ECT but measures incoming air rather than coolant]]
- [[notes/sen-closed-loop-fuel-control-targets-14-7-1|Closed-loop fuel control on the 4.9L trims injector pulse width toward 14.7:1 using the HO2S feedback]]
- [[notes/eng-a-bad-ect-connection-reads-colder-than-actual|A bad ECT connection or added resistance reads colder than actual]]
- [[notes/eng-ect-sensor-is-an-ntc-thermistor-the-pcm-reads-as-voltage|The ECT sensor is an NTC thermistor whose voltage the PCM reads as coolant temperature]]
- [[notes/eec-ntc-temp-sensors-read-falsely-cold-with-bad-grounds|A bad ground or corroded connection makes the ECT and IAT read falsely cold]]
- [[notes/eec-ect-and-iat-are-ntc-thermistors-on-a-5v-reference|The ECT and IAT are negative-coefficient thermistors whose voltage drop falls as temperature rises]]

## Source

- [[sources/sen-engine-coolant-temperature-sensor|Engine Coolant Temperature (ECT) Sensor — Description, Operation, and DTCs (FSM)]]
