---
title: "The WOT A/C relay drops the compressor clutch at wide-open throttle"
kind: how-it-works
source: "[[sources/hvc-compressor-clutch-controls|A/C Compressor Clutch Controls — Relay and Pressure Switch (FSM)]]"
related:
  - "[[notes/hvc-pcm-trims-idle-air-when-the-ac-clutch-engages|The PCM raises idle air when the A/C clutch engages]]"
  - "[[notes/hvc-the-pressure-switch-protects-the-clutch-coil-at-low-suction|The refrigerant pressure switch cuts the clutch coil below 24.5 psi suction]]"
tags: [hvac, compressor-clutch, wot-relay, relay]
---

The compressor clutch relay on the 1994 F-150 (inventory id `hvac`) is the Wide Open Throttle
A/C (WOT A/C) relay. When the driver goes to wide-open throttle, this relay opens and suspends
A/C operation, releasing the compressor clutch so that maximum engine power reaches the drive
wheels under heavy acceleration or load. A/C resumes automatically once normal operation
returns.

This is normal behavior, not a fault: the A/C briefly cutting out during a hard, full-throttle
acceleration is the WOT A/C relay doing its job. It is one of several conditions (along with
low suction pressure) that can interrupt the clutch independently of the dash control.

## Related Concepts

- [[notes/hvc-pcm-trims-idle-air-when-the-ac-clutch-engages|The PCM raises idle air when the A/C clutch engages]]
- [[notes/hvc-the-pressure-switch-protects-the-clutch-coil-at-low-suction|The refrigerant pressure switch cuts the clutch coil below 24.5 psi suction]]
- [[notes/rly-wot-ac-relay-cuts-the-compressor-at-wide-open-throttle|The WOT A/C relay drops the compressor at wide open throttle to free up power]]
- [[notes/hvc-charging-from-14-oz-cans-jumper-the-pressure-switch|Charge from cans by jumpering the pressure switch and running the A/C to 2.0 lb]]
- [[notes/hvc-compressor-clutch-air-gap-spec|The A/C compressor clutch air gap must be 0.018–0.033 in]]

## Source

- [[sources/hvc-compressor-clutch-controls|A/C Compressor Clutch Controls — Relay and Pressure Switch (FSM)]]
