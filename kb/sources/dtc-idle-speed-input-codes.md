---
title: "EEC DTCs 411-539 — Idle Speed, Vehicle Speed, and Switch Input Codes (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/A%20L%20L%20%20Diagnostic%20Trouble%20Codes%20%28%20DTC%20%29/Testing%20and%20Inspection/Manufacturer%20Code%20Charts/337-459/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags: [dtc, idle-air-control, vehicle-speed-sensor, park-neutral, power-steering, cruise-control]
processed: true
---

## Summary

These codes cover idle-speed control, the vehicle speed signal, the integrated vehicle speed
(cruise) control, and the discrete switch inputs the PCM reads during the self-test. The
Idle Air Control (IAC) codes are 411 (cannot control RPM during the KOER low-RPM check) and
412 (cannot control RPM during the high-RPM check), plus the adaptive-limit codes 415 (IAC
at maximum lower adaptive limit) and 416 (IAC at upper adaptive learning limit). DTC 452 is
insufficient input from the vehicle speed sensor to the PCM, and 381 is frequent A/C clutch
cycling.

The 453-459 block is the KOER/KOEO Integrated Vehicle Speed Control (IVSC) self-test: 453
servo leaking down, 454 servo leaking up, 455 insufficient RPM increase, 456 insufficient
RPM decrease, 457 speed control command switch not functioning, 458 switch stuck or grounded,
459 ground circuit open — all deferring to the Cruise Control section. The switch-input codes
include 519/521 (power steering pressure switch circuit open / did not change state), 522 and
527 (vehicle not in Park/Neutral or PNP circuit open / A/C on during self-test), 525 (vehicle
in gear or A/C on), and 528 (clutch pedal position switch circuit failure). DTCs 511 and 513
are PCM internal failures during the KOEO self-test that call for PCM replacement, while 512
is a Keep Alive Memory test failure (route to QB1). DTC 536 is the brake on/off switch
circuit failure or not actuated during the KOER self-test, and 539 is A/C or defrost left on
during the self-test.

## Key Points

- IAC: 411 can't control low RPM, 412 can't control high RPM; 415/416 = IAC adaptive limits.
- 452 = insufficient vehicle speed sensor input to PCM → DS1.
- 453-459 = Integrated Vehicle Speed Control (IVSC) self-test faults → Cruise Control section.
- PSP switch: 519 circuit open (KOEO), 521 did not change states (KOER).
- 522/525/527 = not in Park/Neutral, in gear, or A/C on during self-test → TA1; 528 = clutch switch.
- 511/513 = PCM internal failure → replace PCM; 512 = KAM test failure → QB1.
- 536 = brake on/off switch not actuated during KOER self-test → FD1.

## Notable Excerpts

> "DTC 411 — Cannot control RPM during KOER self-test low RPM check."

> "DTC 452 — Insufficient input from vehicle speed sensor to powertrain control module."

> "DTC 522 — Vehicle not in 'PARK' or 'NEUTRAL' during KOEO or Park/Neutral switch circuit open."

> "DTC 536 — Brake On/Off circuit failure or not actuated during KOER self-test."

Source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/A%20L%20L%20%20Diagnostic%20Trouble%20Codes%20%28%20DTC%20%29/Testing%20and%20Inspection/Manufacturer%20Code%20Charts/ (pages 337-459, 511-528, 529-554)
