---
title: "EEC DTCs 311-341, 558-572 — EGR and Emissions Codes (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/A%20L%20L%20%20Diagnostic%20Trouble%20Codes%20%28%20DTC%20%29/Testing%20and%20Inspection/Manufacturer%20Code%20Charts/221-326/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags: [dtc, egr, secondary-air-injection, evp, emissions, canister-purge]
processed: true
---

## Summary

The 300-series and several 500-series DTCs cover the emissions hardware: the secondary air
injection (thermactor) system, the Exhaust Gas Recirculation (EGR) system, the evaporative
canister purge, and the octane-adjust pin. Secondary air injection codes 311-314 come out
of the KOER self-test and split by failure mode: 311 inoperative (bank #1), 312 misdirected,
313 not bypassed, and 314 inoperative (bank #2), all routing to KC1. The KOEO-only thermactor
circuit codes 552 (bypass circuit) and 553 (diverter circuit) route to KC9.

EGR has two sensing variants on these engines, and the chart calls out which codes apply to
which. Codes 326, 335, and 336 reference the EGR valve **pressure** sensor (the PFE/DPFE
style) and explicitly do not apply to vehicles with an EGR Valve Position (EVP) sensor.
Codes 327, 328, 334, and 337 reference the EGR valve **position** (EVP) sensor — its circuit
below minimum voltage (327), above maximum voltage (337), and closed-voltage out of range
(328 low, 334 high). DTC 332 is insufficient EGR flow detected, and 558/571/572 are EGR
solenoid (vacuum regulator / EGRA / EGRV) circuit failures during the KOEO self-test. DTC 565
and 569 are canister purge circuit failures, 338/339 are coolant-temperature thermostat
tests, and 341 is the octane-adjust service pin open.

## Key Points

- Secondary air injection (KOER): 311 inoperative bank #1, 312 misdirected, 313 not bypassed, 314 bank #2.
- Thermactor circuit (KOEO): 552 bypass, 553 diverter → KC9.
- EGR **pressure** sensor codes 326/335/336 do NOT apply if an EVP sensor is fitted.
- EGR **position** (EVP) sensor: 327 low, 337 high, 328 closed-V low, 334 closed-V high.
- 332 = insufficient EGR flow; 558/571/572 = EGR solenoid circuit failures (KOEO).
- 341 = octane adjust service pin open; 565/569 = canister purge circuit failure.

## Notable Excerpts

> "DTC 326 — Exhaust Gas Recirculation (EGR) valve pressure sensor circuit voltage lower than
> expected. This code does not apply to vehicles equipped with EGR Valve Position (EVP) sensors."

> "DTC 332 — Insufficient exhaust gas recirculation flow detected."

> "DTC 311 — Secondary air injection system inoperative during KOER self-test (bank #1)."

> "DTC 341 — Octane adjust service pin open."

Source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/A%20L%20L%20%20Diagnostic%20Trouble%20Codes%20%28%20DTC%20%29/Testing%20and%20Inspection/Manufacturer%20Code%20Charts/ (pages 221-326, 327-336, 337-459, 556-568, 569-624)
