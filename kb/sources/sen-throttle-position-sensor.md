---
title: "Throttle Position (TP) Sensor — Description, Operation, and DTCs (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Sensors%20and%20Switches/Sensors%20and%20Switches%20-%20Powertrain%20Management/Sensors%20and%20Switches%20-%20Computers%20and%20Control%20Systems/Throttle%20Position%20Sensor/Description%20and%20Operation/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - throttle-position-sensor
  - tps
  - fuel
  - eec-iv
processed: true
---

## Summary

The Throttle Position (TP) sensor is a rotary potentiometer on the throttle body, directly
linked to the throttle shaft. It tells the PCM throttle plate angle, from which the PCM infers
operating mode: closed throttle (idle/decel), part throttle (cruise/moderate accel), and wide
open throttle (max accel, dechoke-on-crank, A/C cutout). The PCM also uses throttle *rate* of
change as an acceleration-pump function and as an input to the transmission shift schedule.

Electrically the TP sensor is a voltage divider: a 5.0 V reference (VREF) feeds one end of a
curved resistor, the other end is grounded through SIG RTN, and a wiper arm on the throttle
shaft picks off the output. At closed throttle the wiper sits near the ground end (about
0.6 V at 0% throttle); at wide open throttle it sits near VREF (about 4.5 V at 85% throttle).

The page lists self-test DTCs (23/121 out of range, 63/122 below minimum, 53/123 above maximum)
plus in-range codes 124/125, which the PCM sets by cross-checking the TP signal against the MAF
sensor and the injector pulse width — if one of the three disagrees with the other two, an
in-range fault is flagged.

## Key Points

- TP sensor = rotary potentiometer / voltage divider on the throttle shaft.
- VREF 5.0 V in, SIG RTN ground, wiper output proportional to throttle angle.
- ~0.6 V at closed throttle (0%) rising to ~4.5 V at wide open throttle (85%).
- PCM derives idle/decel, part-throttle, and WOT modes plus throttle-rate (accel pump) and shift scheduling.
- DTCs: 23/121 out of self-test range; 63/122 below minimum; 53/123 above maximum; 124/125 in-range failures.
- In-range fault logic compares TP against MAF and injector pulse width.

## Notable Excerpts

> "At closed throttle the TP wiper arm is nearer the ground side of the resistor resulting in a
> lower output, 0.6 volts at 0% throttle angle."

> "At wide open throttle the TP wiper arm is nearer the reference voltage side of the resistor
> resulting in a higher output, 4.5 volts at 85% throttle angle."

> "DTC 124, 125 were intended to detect in-range failures of the TP sensor. The PCM compares
> information from the Mass Air Flow (MAF) sensor, TP sensor, and fuel injection pulse width."

Source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Sensors%20and%20Switches/Sensors%20and%20Switches%20-%20Powertrain%20Management/Sensors%20and%20Switches%20-%20Computers%20and%20Control%20Systems/Throttle%20Position%20Sensor/Description%20and%20Operation/index.html
