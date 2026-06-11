---
title: "Heated Oxygen Sensor (HO2S) — Description, Operation, and Testing (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Sensors%20and%20Switches/Sensors%20and%20Switches%20-%20Powertrain%20Management/Sensors%20and%20Switches%20-%20Computers%20and%20Control%20Systems/Oxygen%20Sensor/Description%20and%20Operation/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - oxygen-sensor
  - ho2s
  - fuel
  - eec-iv
  - closed-loop
processed: true
---

## Summary

The Heated Exhaust Gas Oxygen Sensor (HO2S) is the feedback element of the 1994 F-150's
closed-loop fuel control. It detects oxygen in the exhaust and generates a variable voltage
the Powertrain Control Module (PCM) reads to trim each injector's fuel pulse width toward the
stoichiometric 14.7:1 air/fuel ratio. The sensor is a zirconium-dioxide ceramic thimble with
a platinum surface electrode, threaded into the exhaust manifold with its sampling tip in the
exhaust stream.

The cell works on the oxygen difference between its outside (vented to atmosphere) and its
inside (exposed to exhaust). A rich mixture leaves little oxygen in the exhaust, producing a
large oxygen difference and a high output voltage; a lean mixture leaves more oxygen, a small
difference, and a low voltage. The output swings roughly 0.0 V (lean) to 1.1 V (rich). The
sensor must be above 600°F to read correctly, so an internal heating element shortens warm-up.

This is a 4-wire HO2S: a signal wire (HO2S), a signal return / sensor ground (SIG RTN), a
12 V heater supply from the Ignition Run circuit, and a heater ground. Pinpoint diagnosis is
not on the component page — it lives in the system-level test routine **H – Fuel Control**.

## Key Points

- Output range: ~0.0 V (lean) to 1.1 V (rich); rich exhaust = low O2 = high voltage.
- Closed-loop target is 14.7:1; the PCM adjusts injector pulse width from the HO2S signal.
- Must reach >600°F to function; an internal heater speeds light-off.
- 4 wires: HO2S signal, SIG RTN ground, 12 V heater supply (Ignition Run), heater ground.
- Construction: zirconium-dioxide ceramic thimble with platinum electrode, in the exhaust manifold.
- Pinpoint tests are in system-level Testing and Inspection **H – Fuel Control**.

## Notable Excerpts

> "When operating in closed loop the Powertrain Control Module (PCM) monitors this input and
> correspondingly changes the duration of the fuel injection pulse width to achieve an air/fuel
> ratio of 14.7:1."

> "A rich fuel mixture will result in a low level of oxygen present in the exhaust... which will
> result in a higher voltage being produced."

> "The HO2S temperature must be above 600°F to operate properly. To minimize heat up time, a
> heating element is incorporated into the sensor."

Source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Sensors%20and%20Switches/Sensors%20and%20Switches%20-%20Powertrain%20Management/Sensors%20and%20Switches%20-%20Computers%20and%20Control%20Systems/Oxygen%20Sensor/Description%20and%20Operation/index.html
