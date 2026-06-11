---
title: "EEC DTCs 542-593 — Fuel Pump, Output Actuator, and VCRM Codes (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/A%20L%20L%20%20Diagnostic%20Trouble%20Codes%20%28%20DTC%20%29/Testing%20and%20Inspection/Manufacturer%20Code%20Charts/529-554/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags: [dtc, fuel-pump, fuel-pump-relay, vcrm, output-actuator, ho2s-heater, cooling-fan]
processed: true
---

## Summary

This block of 500-series DTCs covers the PCM's output side: the fuel pump and its relay, the
output-state self-test (which verifies the PCM can drive each actuator), the Variable Control
Relay Module (VCRM) that manages the electric cooling fan and several high-current loads, and
the heated oxygen sensor heater. The fuel pump codes are 542 and 543 (fuel pump secondary
circuit failure, routing to J10/J20 and the J90/J93 memory tests), 556 (fuel pump relay
primary circuit failure → J1), and 557 (low-speed fuel pump primary circuit failure → X70).
DTC 554 is a fuel pressure regulator control circuit failure during the KOEO self-test.

The VCRM codes (581-587) are over-current and open-circuit faults the module reports for its
managed loads: 581 power-to-fan over-current, 582 fan circuit open, 583 power-to-fuel-pump
over-current, 584 VCRM power ground open, 585 power-to-A/C-clutch over-current, 586 A/C clutch
circuit open, and 587 VCRM communication failure. Other output-state codes include 558 (EGR
vacuum regulator), 559 (A/C on relay), 562 (pusher fan), 563/564 (high fan / fan control),
565/569 (canister purge), and 552/553 (secondary air bypass/diverter) — all detected during
the KOEO self-test as the PCM commands each output on and off. DTC 593 is a heated oxygen
sensor heater circuit failure (→ H40).

## Key Points

- Fuel pump: 542/543 secondary circuit, 556 relay primary, 557 low-speed pump primary.
- 554 = fuel pressure regulator control circuit failure (KOEO).
- VCRM: 581 fan over-current, 582 fan open, 583 fuel-pump over-current, 584 ground open.
- VCRM: 585 A/C clutch over-current, 586 A/C clutch open, 587 communication failure.
- Output self-test circuit faults: 558 EGR VR, 559 A/C relay, 562-564 fans, 565/569 purge.
- 593 = HO2S heater circuit failure → H40.

## Notable Excerpts

> "DTC 556 — Fuel pump relay primary circuit failure."

> "DTC 554 — Fuel Pressure Regulator Control circuit failure."

> "DTC 583 — Power to Fuel pump over current."

> "DTC 593 — Heated Oxygen Sensor (HO2S) heater circuit failure."

Source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/A%20L%20L%20%20Diagnostic%20Trouble%20Codes%20%28%20DTC%20%29/Testing%20and%20Inspection/Manufacturer%20Code%20Charts/ (pages 529-554, 556-568, 569-624)
