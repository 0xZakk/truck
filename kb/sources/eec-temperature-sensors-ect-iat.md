---
title: "ECT and IAT Temperature Sensors — Operation, DTCs, and Specs (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Powertrain%20Management/Computers%20and%20Control%20Systems/Coolant%20Temperature%20Sensor%2FSwitch%20%28For%20Computer%29/Description%20and%20Operation/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - ect
  - iat
  - coolant-temperature-sensor
  - intake-air-temperature
  - thermistor
  - eec-iv
processed: true
---

## Summary

The Engine Coolant Temperature (ECT) and Intake Air Temperature (IAT) sensors are both
two-lead, negative-temperature-coefficient thermistors that feed the PCM. The PCM uses each to
adjust fuel injection base pulse width, EGR flow, and ignition timing. The PCM applies a 5.0 V
reference to the signal lead with the return lead on a common sensor ground; as temperature
rises, resistance falls and the voltage drop across the sensor decreases.

The ECT's normal range is 3.50 V (50 deg F) to 0.35 V (230 deg F). The IAT's range is 3.50 V
(50 deg F) to 1.02 V (158 deg F). Because both have a negative coefficient, the FSM stresses
that poor connections or added resistance in the harness/ground read out as temperatures
*lower* than actual — a key diagnostic gotcha.

Each sensor sets its own family of self-test DTCs covering out-of-range, below-minimum, and
above-maximum outputs. Coolant temperature must be above 50 deg F to pass KOEO and above
180 deg F to pass KOER self-tests.

## Key Points

- Both are two-lead NTC thermistors on a 5.0 V reference; resistance drops as temperature rises.
- ECT range: 3.50 V at 50 deg F to 0.35 V at 230 deg F. IAT range: 3.50 V at 50 deg F to 1.02 V at 158 deg F.
- PCM uses temperature data for fuel pulse width, EGR flow, and ignition timing.
- High harness/ground resistance reads as falsely COLD due to the negative coefficient.
- ECT DTCs: 21/116 out-of-range, 61/117 below min (0.2 V), 51/118 above max (4.6 V).
- IAT DTCs: 64/112 below min (0.2 V), 54/113 above max (4.6 V), 24/114 out-of-range.
- Self-test prerequisites: coolant >50 deg F for KOEO, >180 deg F for KOER.
- Torque: ECT 13-20 Nm (10-15 ft lb); IAT 16-24 Nm (12-18 ft lb).

## Notable Excerpts

> "Due to its negative temperature coefficient, poor electrical connections or minor increases in resistance across the ECT circuit harness and ground connections can result in temperature values that are lower than actual."

> "The normal operating range of the ECT is 3.50 volts (50 deg F) to 0.35 volts (230 deg F)."

Relates to truck inventory system `engine`.

Source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Powertrain%20Management/Computers%20and%20Control%20Systems/Coolant%20Temperature%20Sensor%2FSwitch%20%28For%20Computer%29/Description%20and%20Operation/index.html
