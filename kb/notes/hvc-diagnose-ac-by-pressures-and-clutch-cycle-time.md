---
title: "Diagnose A/C performance by comparing pressures and clutch cycle time to the FSM charts"
kind: troubleshooting
source: "[[sources/hvc-system-performance-diagnosis|A/C System Performance Test and Pressure Diagnosis (FSM)]]"
related:
  - "[[notes/hvc-a-refrigerant-leak-shows-as-oily-residue|A refrigerant leak usually shows up as oily residue at the leak point]]"
  - "[[notes/hvc-the-pressure-switch-protects-the-clutch-coil-at-low-suction|The refrigerant pressure switch cuts the clutch coil below 24.5 psi suction]]"
tags: [hvac, diagnosis, system-performance-test, pressures, clutch-cycle]
---

The FSM's A/C System Performance Test for the 1994 F-150 (inventory id `hvac`) diagnoses
refrigerant-system problems by reading the high- and low-side pressures and the compressor
clutch cycle rate and times, then comparing them against the normal pressure/temperature and
clutch-cycle charts. The conditional test requirements (engine speed, doors, blower, ambient)
must be met or the readings are meaningless.

When the measured values fall outside the chart bands, you cross-reference the A/C System
Pressure Evaluation Charts (A and B) to identify the component at fault — for example an
overcharge, undercharge, restriction, or failed compressor. After the repair, re-run the test
under the same conditions to confirm the readings are back in band.

## Related Concepts

- [[notes/hvc-a-refrigerant-leak-shows-as-oily-residue|A refrigerant leak usually shows up as oily residue at the leak point]]
- [[notes/hvc-the-pressure-switch-protects-the-clutch-coil-at-low-suction|The refrigerant pressure switch cuts the clutch coil below 24.5 psi suction]]

## Source

- [[sources/hvc-system-performance-diagnosis|A/C System Performance Test and Pressure Diagnosis (FSM)]]
