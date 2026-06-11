---
title: "Engine Coolant Temperature (ECT) Sensor — Description, Operation, and DTCs (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Sensors%20and%20Switches/Sensors%20and%20Switches%20-%20Powertrain%20Management/Sensors%20and%20Switches%20-%20Computers%20and%20Control%20Systems/Coolant%20Temperature%20Sensor%2FSwitch%20%28For%20Computer%29/Description%20and%20Operation/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - ect
  - coolant-temperature-sensor
  - thermistor
  - fuel
  - eec-iv
processed: true
---

## Summary

The Engine Coolant Temperature (ECT) sensor is a two-lead thermistor with a negative
temperature coefficient. It feeds coolant temperature to the PCM, which uses it to adjust the
fuel injection base pulse width, EGR flow, and ignition timing — so a wrong ECT reading skews
warm-up enrichment, spark advance, and emissions control simultaneously.

The PCM applies 5.0 V reference to the signal lead and grounds the return through a common
sensor ground. As coolant warms, the thermistor's resistance falls and the voltage across it
drops; as it cools, resistance and voltage rise. The normal operating range runs from about
3.50 V at 50°F down to 0.35 V at 230°F. Because the coefficient is negative, any added
resistance from corroded connectors or a poor ground makes the engine look *colder* than it is,
driving the PCM to add fuel it doesn't need.

The page lists self-test DTCs (21/116 out of range 0.3–3.7 V, 61/117 below 0.2 V minimum,
51/118 above 4.6 V maximum). The Specifications page adds that coolant must exceed 50°F to pass
the KOEO self-test and 180°F to pass the KOER self-test; the detailed resistance/voltage-vs-
temperature table is provided only as an image.

## Key Points

- Two-lead negative-temperature-coefficient thermistor; resistance falls as it heats.
- 5.0 V VREF on the signal lead, common SIG RTN ground.
- Normal output ~3.50 V at 50°F to ~0.35 V at 230°F.
- Drives fuel base pulse width, EGR flow, and ignition timing.
- A high-resistance connection reads falsely cold and over-fuels the engine.
- DTCs: 21/116 out of range (0.3–3.7 V), 61/117 below 0.2 V, 51/118 above 4.6 V.
- Must be >50°F to pass KOEO and >180°F to pass KOER self-test.

## Notable Excerpts

> "As the temperature of the engine coolant increases the resistance of the ECT sensor decreases
> and correspondingly the voltage drop across the ECT sensor is reduced."

> "The normal operating range of the ECT is 3.50 volts (50°F) to 0.35 volts (230°F)."

> "Due to its negative temperature coefficient, poor electrical connections or minor increases
> in resistance across the ECT circuit harness and ground connections can result in temperature
> values that are lower than actual."

Source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Sensors%20and%20Switches/Sensors%20and%20Switches%20-%20Powertrain%20Management/Sensors%20and%20Switches%20-%20Computers%20and%20Control%20Systems/Coolant%20Temperature%20Sensor%2FSwitch%20%28For%20Computer%29/Description%20and%20Operation/index.html
