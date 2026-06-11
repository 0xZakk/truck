---
title: "Heated Oxygen Sensor (HO2S) — EEC-IV Description, Operation, and Specs (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Powertrain%20Management/Computers%20and%20Control%20Systems/Oxygen%20Sensor/Description%20and%20Operation/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - oxygen-sensor
  - ho2s
  - closed-loop
  - eec-iv
  - fuel
processed: true
---

## Summary

The Heated Exhaust Gas Oxygen Sensor (HO2S) detects oxygen in the exhaust and produces a
variable voltage according to how much is present. In closed loop the PCM monitors this input
and changes injector pulse width to hold the air/fuel ratio at 14.7:1. The sensor is a
zirconium-dioxide ceramic thimble with a platinum electrode, threaded into the exhaust
manifold with its tip in the exhaust stream.

Operation depends on the oxygen difference between the exhaust (inside) and atmosphere
(outside). A rich mixture leaves little oxygen in the exhaust, producing a large difference and
a higher voltage; a lean mixture leaves more oxygen, a smaller difference, and a lower voltage.
Normal output ranges 0.0 V (lean) to 1.1 V (rich). The sensor must be above 600 deg F to work,
so a heater element is built in to shorten warm-up.

The 4-wire connection carries the sensor output (HO2S), sensor ground (SIG RTN), a 12 V heater
supply from the Ignition Run circuit, and a heater ground.

## Key Points

- Closed-loop target air/fuel ratio is 14.7:1; PCM trims injector pulse width from the HO2S signal.
- Output 0.0 V (lean) to 1.1 V (rich); rich = low exhaust oxygen = high voltage.
- Sensor must exceed 600 deg F; integral heater speeds warm-up.
- 4 wires: output, SIG RTN ground, 12 V heater supply (Ignition Run), heater ground.
- Heater element resistance: 5.0-30.0 ohms hot-to-warm; 2.0-5.0 ohms at room temperature.
- HO2S switching after driving 55 mph for 5 minutes: signal swings 0.3-0.9 V within 3 seconds.
- Torque: 36-46 Nm (26-34 ft lb).

## Notable Excerpts

> "A rich fuel mixture will result in a low level of oxygen present in the exhaust... which will result in a higher voltage being produced."

> "Normal operating range for the HO2S is 0.0 volts (lean condition) to 1.1 volts (rich condition). The HO2S temperature must be above 600 deg F to operate properly."

Relates to truck inventory system `fuel`.

Source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Powertrain%20Management/Computers%20and%20Control%20Systems/Oxygen%20Sensor/Description%20and%20Operation/index.html
