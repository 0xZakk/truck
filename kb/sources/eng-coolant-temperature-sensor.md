---
title: "Engine Coolant Temperature (ECT) Sensor — Operation, Values & DTCs (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Engine%2C%20Cooling%20and%20Exhaust/Cooling%20System/Sensors%20and%20Switches%20-%20Cooling%20System/Engine%20-%20Coolant%20Temperature%20Sensor%2FSwitch/Coolant%20Temperature%20Sensor%2FSwitch%20%28For%20Computer%29/Description%20and%20Operation/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - cooling
  - ect-sensor
  - pcm
  - sensors
  - diagnosis
processed: true
---

## Summary

The Engine Coolant Temperature (ECT) sensor is a two-lead, negative-temperature-coefficient
(NTC) thermistor that feeds coolant temperature to the Powertrain Control Module (PCM). The
PCM uses that input to adjust fuel-injection base pulse width, EGR flow, and ignition timing.
The PCM applies a 5.0-volt reference to the ECT signal lead against a common sensor ground;
as coolant warms, sensor resistance drops and the voltage across it falls. The normal
operating range is 3.50 V at 50 deg F down to 0.35 V at 230 deg F.

Because of the NTC behavior, poor electrical connections or added resistance in the harness
or ground will read as a *lower-than-actual* temperature. The FSM lists EEC-IV diagnostic
trouble codes for this circuit and notes that the on-board test pinpoint steps live in the
system-level Testing and Inspection (DA - Intake Air and Engine Coolant Temperature Sensors).

This source backs the `cooling` and `engine` inventory systems.

## Key Points

- ECT is a two-lead NTC thermistor; resistance falls as coolant temperature rises.
- PCM uses ECT to trim fuel pulse width, EGR flow, and ignition timing.
- Circuit: 5.0 V reference on the signal lead, signal return to common sensor ground.
- Normal range: 3.50 V (50 deg F) to 0.35 V (230 deg F).
- Bad connections / added resistance bias the reading LOW (colder than actual).
- DTCs: 21/116 = out of self-test range (0.3-3.7 V); 61/117 = below minimum (<0.2 V);
  51/118 = above maximum (>4.6 V).
- Self-test gating: coolant must be >50 deg F (10 deg C) to pass KOEO and >180 deg F (82 deg C)
  to pass KOER; calculated values can vary ~16% with sensor and VREF variation.

## Notable Excerpts

> "The ECT is a two lead thermistor type sensor with a negative temperature coefficient."

> "The normal operating range of the ECT is 3.50 volts (50degF) to 0.35 volts (230degF).
> Due to its negative temperature coefficient, poor electrical connections or minor increases
> in resistance ... can result in temperature values that are lower than actual."

> "DTC 21/116 - The ECT sensor output is out of self-test range, 0.3-3.7 volts."

Source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Engine%2C%20Cooling%20and%20Exhaust/Cooling%20System/Sensors%20and%20Switches%20-%20Cooling%20System/Engine%20-%20Coolant%20Temperature%20Sensor%2FSwitch/ (Description and Operation, Testing and Inspection, Electrical Specifications)
