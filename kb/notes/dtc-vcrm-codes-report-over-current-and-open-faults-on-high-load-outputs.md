---
title: "VCRM DTCs report over-current and open-circuit faults on the high-current loads the relay module manages"
kind: troubleshooting
source: "[[sources/dtc-actuator-pcm-codes|EEC DTCs 542-593 — Fuel Pump, Output Actuator, and VCRM Codes (FSM)]]"
related:
  - "[[notes/dtc-fuel-pump-codes-distinguish-relay-from-secondary-circuit|Fuel pump DTCs distinguish a relay primary-circuit fault from a pump secondary-circuit fault]]"
  - "[[notes/dtc-codes-may-be-shared-between-modules-so-confirm-the-source|DTC numbers may be shared between modules, so confirm which module a code came from before chasing it]]"
tags:
  - dtc
  - vcrm
  - cooling-fan
  - fuel-pump
  - troubleshooting
---

The Variable Control Relay Module (VCRM) is a smart relay pack that switches the truck's
high-current loads — the electric cooling fan, the fuel pump, and the A/C clutch — and reports
back to the PCM when one of those circuits draws too much or goes open. The 581-587 codes are
its diagnostics: 581 "Power to Fan" over-current, 582 fan circuit open, 583 power-to-fuel-pump
over-current, 584 VCRM power ground open (pin 1), 585 power-to-A/C-clutch over-current, 586
A/C clutch circuit open, and 587 VCRM communication failure.

The pattern is consistent — each managed load gets an over-current code (a short or a seized
motor pulling too much) and an open code (a broken wire or failed load). DTC 583, a fuel-pump
over-current, can present as a fuel delivery problem even though the fault is in the power
path, not the pump windings per se; it complements the conventional fuel-pump codes by adding
a current-monitoring view. DTC 584 (ground open) is worth singling out because a lost module
ground can cascade into apparent faults on every load the VCRM controls.

These codes link the truck's `fuel` system and its cooling fan through one shared module, so a
584 ground fault should be ruled out before chasing individual load codes.

## Related Concepts

- [[notes/dtc-fuel-pump-codes-distinguish-relay-from-secondary-circuit|Fuel pump DTCs distinguish a relay primary-circuit fault from a pump secondary-circuit fault]]
- [[notes/dtc-codes-may-be-shared-between-modules-so-confirm-the-source|DTC numbers may be shared between modules, so confirm which module a code came from before chasing it]]

## Source

- [[sources/dtc-actuator-pcm-codes|EEC DTCs 542-593 — Fuel Pump, Output Actuator, and VCRM Codes (FSM)]]
