---
title: "EEC DTCs 617-998 — E4OD Transmission Codes (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/A%20L%20L%20%20Diagnostic%20Trouble%20Codes%20%28%20DTC%20%29/Testing%20and%20Inspection/Manufacturer%20Code%20Charts/625-639/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags: [dtc, transmission, e4od, shift-solenoid, torque-converter-clutch, electronic-pressure-control]
processed: true
---

## Summary

The 600-series and 998 DTCs apply to the electronically controlled E4OD automatic
transmission, whose PCM-driven solenoids, sensors, and switches are diagnosed through the
same EEC self-test. (On the 4.9L the M5OD-R2 manual is standard, so these codes are only
relevant if the truck is so equipped.) Shift-control faults include 566 (3-4 shift solenoid),
621 (SS1) and 622 (SS2) and 641 (SS3) circuit failures during the KOEO self-test, plus the
shift-error codes 617 (1-2), 618 (2-3), and 619 (3-4) and the gear-ratio codes 645-648
(incorrect ratio obtained for first through fourth gear).

Torque converter clutch and pressure-control faults make up another block: 624/625/649/651
(electronic pressure control circuit / driver / out of range), 627/629/643/652 (TCC solenoid
circuit), 628 and 656 (converter clutch slippage/continuous slip), and 626 (coast clutch
solenoid). Sensor and switch codes include 634/654/667/668/675 (transmission range sensor
voltage out of range or not in Park), 636/637/638 (transmission fluid temperature higher/
lower than expected, open, or shorted), 639 (insufficient transmission speed sensor input),
657 (over-temperature condition occurred), and 659 (high vehicle speed in Park). The
transmission control switch and indicator-lamp codes are 623/631 (TCIL circuit) and 632/653
(TCS did not change states during the KOER self-test). DTC 998 routes to TC10.

## Key Points

- Shift solenoids (KOEO): 566/641 = SS3/3-4, 621 = SS1, 622 = SS2 → TC1.
- Shift errors: 617 (1-2), 618 (2-3), 619 (3-4); 645-648 = incorrect ratio for gears 1-4.
- TCC / pressure control: 624/625/649/651 EPC, 627/629/643/652 TCC solenoid, 628/656 slip.
- Transmission range sensor: 634/654/667/668/675 voltage out of range or not in Park.
- Fluid temp: 637 open (-40°F indicated), 638 shorted (290°F indicated), 657 over-temp occurred.
- 639 = insufficient transmission speed sensor input; 623/631 = TCIL circuit; 632/653 = TCS.

## Notable Excerpts

> "DTC 637 — Transmission fluid temperature sensor circuit above maximum voltage, -40 degrees C
> (-40 degrees F) indicated, circuit open."

> "DTC 638 — Transmission fluid temperature sensor circuit below minimum voltage, 143 degrees C
> (290 degrees F) indicated, circuit shorted."

> "DTC 645 — Incorrect gear ratio obtained for first gear."

> "DTC 657 — Transmission over temperature condition occurred."

Source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/A%20L%20L%20%20Diagnostic%20Trouble%20Codes%20%28%20DTC%20%29/Testing%20and%20Inspection/Manufacturer%20Code%20Charts/ (pages 556-568, 569-624, 625-639, 641-998)
