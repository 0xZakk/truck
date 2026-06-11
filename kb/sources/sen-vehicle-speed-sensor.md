---
title: "Vehicle Speed Sensor / PSOM and Differential Speed Sensor — Description and Operation (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Sensors%20and%20Switches/Sensors%20and%20Switches%20-%20Powertrain%20Management/Sensors%20and%20Switches%20-%20Computers%20and%20Control%20Systems/Vehicle%20Speed%20Sensor/Description%20and%20Operation/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - vehicle-speed-sensor
  - psom
  - speedometer
  - electrical-body
processed: true
---

## Summary

On the 1994 F-150, vehicle speed reaches the PCM through a two-stage path. A Differential Speed
Sensor (DSS) at the rear axle produces a raw speed signal. The Programmable
Speedometer/Odometer Module (PSOM) reads the DSS (pin 4 input, pin 5 return) and converts it
into a standardized **8000 pulses-per-mile** speed signal, which it outputs to the PCM (pin 3
PSOM+, pin 6 PSOM-). The PSOM also feeds the speed-control servo amplifier and the instrument
cluster.

The PCM uses vehicle speed to determine transmission shift points and torque-converter-clutch
operation (on automatic-equipped trucks). The PSOM has two power inputs: pin 1 is continuous
12 V, and pin 2 is 12 V only with the ignition switch in Run. Related DTC: 29/452, set when the
PCM detects an error in the PSOM output signal. Pinpoint diagnosis lives in the system-level
test routine **DS – Programmable Speedometer/Odometer Module**.

## Key Points

- Two-stage: rear-axle Differential Speed Sensor → PSOM → 8000 pulses-per-mile signal to the PCM.
- PSOM also drives the speed-control servo and the instrument cluster speedometer/odometer.
- PCM uses speed for shift scheduling and torque-converter-clutch control.
- PSOM power: pin 1 continuous 12 V, pin 2 switched 12 V (ignition Run).
- DTC 29/452: PCM detected an error in the PSOM output signal.
- Pinpoint tests are in system-level DS – Programmable Speedometer/Odometer Module.

## Notable Excerpts

> "The PSOM receives a vehicle speed signal from the Differential Speed Sensor (DSS) on pin 4
> DSS input, and pin 5 DSS return. It converts this signal to a standard 8000 pulses-per-mile
> speed signal output."

> "The speed signal is used by the PCM to determine transmission shift points and torque
> converter clutch operation."

Source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Sensors%20and%20Switches/Sensors%20and%20Switches%20-%20Powertrain%20Management/Sensors%20and%20Switches%20-%20Computers%20and%20Control%20Systems/Vehicle%20Speed%20Sensor/Description%20and%20Operation/index.html
