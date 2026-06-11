---
title: "Speedometer / Programmable Speedometer-Odometer Module (PSOM) — Description and Operation (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair and Diagnosis/Instrument Panel, Gauges and Warning Indicators/Speedometer Head/Description and Operation/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - speedometer
  - odometer
  - psom
  - instrument-cluster
  - abs
processed: true
---

## Summary

The 1994 F-150 uses an electronic Programmable Speedometer/Odometer Module (PSOM), not a
cable-driven speedometer head. The PSOM contains the speedometer, the LCD odometer, and the
trip odometer, all controlled by a programmable integrated microprocessor. The microprocessor
receives a speed signal from the Differential Speed Sensor (DSS) / anti-lock brake sensor and
uses a programmed conversion constant to produce a standard 8000-pulses-per-mile speed signal
output. The module is serviceable only as a unit.

The LCD odometer combines a total odometer (normally displayed) and a trip odometer.
Pressing/releasing the SELECT button (upper right) shows the trip odometer; pressing/releasing
RESET (upper left) while the trip is displayed zeroes it; SELECT returns to total. The
speedometer also supplies the speed signal for the EEC module and speed control, which is why
the internal conversion constant MUST be changed whenever tire size changes — both to keep the
speed signal correct for those systems and to preserve factory-set speedometer accuracy.

Note that the "Speedometer Cable" and "Speedometer Module" testing pages defer to the
system-level Testing and Inspection / Pinpoint Tests (symptoms E-H: erroneous reading, noisy,
inoperative), since the truck is electronic rather than cable-driven.

## Key Points

- Electronic PSOM: speedometer + LCD total odometer + trip odometer, one microprocessor.
- Input is the Differential Speed Sensor (DSS) / anti-lock brake sensor, not a cable.
- Microprocessor outputs a standard 8000 pulses-per-mile speed signal.
- Serviceable only as a complete unit.
- Trip: SELECT (upper right) shows it; RESET (upper left) zeroes it; SELECT returns to total.
- Also feeds speed signal to the EEC module and speed control.
- Conversion constant MUST be reprogrammed on tire-size changes to keep accuracy and correct EEC/speed-control signals.

## Notable Excerpts

> "The microprocessor receives a speed signal input from the Differential Speed Sensor (DSS),
> and uses a programmed conversion constant to convert the signal to the standard 8000 pulses
> per mile speed signal output."

> "Because of this, it is VERY IMPORTANT to change the speedometer's internal conversion
> constant if the size of tires on the vehicle is changed."

Source: FSM — Instrument Panel, Gauges and Warning Indicators / Speedometer Head / Description and Operation and Relays and Modules - Instrument Panel / Speedometer Module / Description and Operation (PSOM).
