---
title: "Throttle Position Sensor (TP) — Operation, DTCs, Service, and Specs (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Powertrain%20Management/Computers%20and%20Control%20Systems/Throttle%20Position%20Sensor/Description%20and%20Operation/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - tps
  - throttle-position-sensor
  - potentiometer
  - eec-iv
  - fuel
processed: true
---

## Summary

The Throttle Position (TP) sensor is a rotary potentiometer mounted on the throttle body and
linked to the throttle shaft. It acts as a voltage divider: a 5.0 V reference (VREF) feeds one
end of a curved resistor, the other end is grounded (SIG RTN), and a wiper arm produces a
continuously variable output proportional to throttle angle. Output runs about 0.6 V at 0%
throttle (closed) to 4.5 V at 85% throttle (wide open).

From this signal the PCM derives operating modes: closed throttle (idle/decel), part throttle
(cruise), wide-open throttle (max accel, dechoke on crank, A/C cutout), throttle-angle rate
(accelerator-pump function), and transmission shift scheduling. The FSM notes in-range failure
codes 124/125 are set by cross-checking TP against the MAF sensor and injector pulse width.

Service requires care: after sliding the rotary tangs over the throttle shaft, the sensor must
be rotated CLOCKWISE ONLY into position, or excessive idle speed can result.

## Key Points

- Rotary potentiometer / voltage divider on 5.0 V VREF; wiper output proportional to throttle angle.
- Output ~0.6 V at 0% (closed) to ~4.5 V at 85% (wide open).
- Defines operating modes: idle/decel, cruise, WOT, throttle-rate, transmission shift schedule.
- DTCs: 23/121 out-of-range, 63/122 below min, 53/123 above max, 124 higher than expected, 125 lower than expected.
- 124/125 are in-range failures detected by comparing TP, MAF, and injector pulse width.
- Service: rotate CLOCKWISE ONLY into position; wrong rotation causes excessive idle speed.
- Torque: 2-3 Nm (18-27 in lb). Battery disconnect requires a ~10-mile adaptive relearn.

## Notable Excerpts

> "At closed throttle the TP wiper arm is nearer the ground side of the resistor resulting in a lower output, 0.6 volts at 0% throttle angle. At wide open throttle... 4.5 volts at 85% throttle angle."

> "rotate TP sensor CLOCKWISE ONLY to installed position. Failure to install the TP sensor in this manner may result in excessive idle speeds."

Relates to truck inventory systems `fuel` and `engine`.

Source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Powertrain%20Management/Computers%20and%20Control%20Systems/Throttle%20Position%20Sensor/Description%20and%20Operation/index.html
