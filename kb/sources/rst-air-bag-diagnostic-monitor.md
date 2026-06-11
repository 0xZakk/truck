---
title: "Air Bag Diagnostic Monitor and Trouble Codes — Description, Operation, and Diagnostics (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Restraints%20and%20Safety%20Systems/Air%20Bag%20Systems/Description%20and%20Operation/Air%20Bag%20Diagnostic%20Monitor/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - air-bag
  - diagnostic-monitor
  - trouble-codes
  - srs
  - diagnosis
processed: true
---

## Summary

The air bag diagnostic monitor continuously watches all SRS components and wiring for faults whenever the
ignition is in RUN. Its main purpose is diagnostics — it does NOT deploy the bag. The center and RH front
air bag sensors and the RH cowl-side safing sensor are "hard wired" to the air bag and are what determine
deployment. At key-on the monitor lights the air bag indicator for about six seconds as a bulb check, then
turns it off; if the indicator fails to light, stays on, or flashes, a fault has been detected. Trouble
codes may not appear for up to about 30 seconds after key-on, the time the monitor needs to run all tests
and verify faults.

Codes are two-digit, flashed by the indicator (e.g. code 32 = three flashes, one-second pause, two flashes,
three-second pause), and each code is displayed at least twice. Codes are prioritized numerically; with
multiple faults the highest priority shows first, and the next appears only after the first is corrected.
If the indicator itself is malfunctioning while a fault exists, a tone of five sets of five beeps sounds —
this is NOT a code 55, just an audible "indicator dead, service needed" alert. Codes clear automatically
once the fault is corrected; there is no manual erase step.

Two protective features matter for service. The monitor contains an internal thermal fuse that blows open
to cut all power to the deployment circuit if a fault makes unwanted deployment possible — it does NOT blow
from overcurrent, and must never be jumpered. The monitor also contains an internal backup power supply
that can deploy the bag if the battery or cables are damaged in a crash before the sensors close; that
backup energy depletes about one minute after the positive battery cable is disconnected, which is why the
disarm procedure requires a one-minute wait. Diagnosis uses the Rotunda Air Bag Simulator (105-0008 or
equivalent), a 2-ohm resistor; a zero-ohm jumper must not be used or a fault may be displayed.

## Key Points

- Monitor diagnoses only; deployment is decided by the hard-wired center/RH front sensors plus safing sensor.
- Indicator lights ~6 seconds at key-on as a self-test; codes appear within ~30 seconds.
- Two-digit flash codes, displayed at least twice, prioritized numerically.
- Five-sets-of-five-beeps tone means the indicator is inoperative AND a fault exists (not code 55).
- Internal thermal fuse opens to disable deployment on a dangerous fault; never jumper it (it is not an overcurrent fuse).
- Internal backup power supply depletes ~1 minute after the positive cable is disconnected.
- Codes clear automatically when the fault is corrected.
- Diagnostics require the Rotunda Air Bag Simulator 105-0008 (a 2-ohm resistor); no zero-ohm jumpers.

## Notable Excerpts

> "The air bag diagnostic monitor does not deploy the air bag in the event of a crash. The center and RH
> front air bag sensors are 'hard wired' to the air bag..."

> "The thermal fuse does not blow (open) because of excessive current flowing through It. DO NOT attempt
> to Jumper out the thermal fuse with a circuit breaker or any other type of fuse."

> "The air bag simulator is a 2-ohm resistor that must be used to simulate an air bag connection in the
> system. It is not acceptable to jump the air bag connection with a zero ohm jumper wire."

Relevant truck inventory systems: `interior`, `body-cab`.

Source FSM path: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Restraints%20and%20Safety%20Systems/Air%20Bag%20Systems/Description%20and%20Operation/Air%20Bag%20Diagnostic%20Monitor/index.html
