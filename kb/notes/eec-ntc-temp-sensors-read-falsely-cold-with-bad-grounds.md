---
title: "A bad ground or added resistance makes the NTC ECT and IAT read falsely cold, driving a needless rich condition"
kind: troubleshooting
source: "[[sources/eec-temperature-sensors-ect-iat|ECT and IAT Temperature Sensors — Operation, DTCs, and Specs (FSM)]]"
related:
  - "[[notes/eec-ect-and-iat-are-ntc-thermistors-on-a-5v-reference|The ECT and IAT are identical two-lead NTC thermistors on a 5.0 V reference whose voltage drops as temperature rises]]"
tags:
  - ect
  - iat
  - troubleshooting
  - grounds
  - fuel
  - engine
---

Because the ECT and IAT are negative-temperature-coefficient thermistors (resistance falls as
temperature rises), *any* extra series resistance in the circuit — a corroded connector pin, a
poor SIG RTN ground, minor harness resistance — adds to the sensor's own resistance and looks
identical to a colder sensor. The FSM explicitly warns that poor electrical connections or minor
increases in harness and ground resistance produce temperature values *lower* than actual,
sometimes much lower for the IAT.

This matters because the PCM uses temperature to set fuel-injection pulse width, EGR flow, and
ignition timing. A falsely-cold reading makes the engine look colder than it is, so the PCM
commands warm-up enrichment that never ends: a needlessly rich mixture, fouled plugs, poor fuel
economy, delayed closed-loop entry, and driveability complaints with no obvious failed part —
often with no stored code, because the reading is still "in range." When chasing a rich
condition or a temperature DTC on the `fuel`, `cooling`, or `engine` inventory systems, inspect
the sensor grounds and connector pins before condemning the sensor.

Self-test codes only catch gross faults. For ECT: 21/116 (output out of the 0.3–3.7 V range),
61/117 (below the 0.2 V minimum, e.g. shorted to ground), and 51/118 (above the 4.6 V maximum,
e.g. an open circuit). The parallel IAT codes are 24/114, 64/112, and 54/113.

> "Due to its negative temperature coefficient, poor electrical connections or minor increases in
> resistance across the ECT circuit harness and ground connections can result in temperature values
> that are lower than actual."

## Related Concepts

- [[notes/eec-ect-and-iat-are-ntc-thermistors-on-a-5v-reference|The ECT and IAT are identical two-lead NTC thermistors on a 5.0 V reference whose voltage drops as temperature rises]]
- [[notes/dtc-temperature-sensor-codes-pair-low-and-high-voltage|Temperature sensor DTCs come in low/high pairs that mean shorted (254°F) or open (-40°F)]]
- [[notes/drv-m5od-tot-sensor-is-part-of-solenoid-body|The transmission temperature (TOT) sensor is a thermistor in the solenoid body, replaced only as an assembly]]
- [[notes/sen-eec-iv-sensors-share-vref-and-sig-rtn|Most EEC-IV sensors share a common 5.0 V VREF and SIG RTN ground, so one bad reference skews many readings]]

## Source

- [[sources/eec-temperature-sensors-ect-iat|ECT and IAT Temperature Sensors — Operation, DTCs, and Specs (FSM)]]
- [[sources/eng-coolant-temperature-sensor|Engine Coolant Temperature (ECT) Sensor — Operation, Values & DTCs (FSM)]]
- [[sources/sen-engine-coolant-temperature-sensor|Engine Coolant Temperature (ECT) Sensor — Description, Operation, and DTCs (FSM)]]
