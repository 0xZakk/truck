---
title: "The A/C compressor clutch air gap must be 0.018–0.033 in"
kind: spec
source: "[[sources/hvc-compressor-and-clutch|A/C Compressor and Clutch (FSM)]]"
related:
  - "[[notes/hvc-pcm-trims-idle-air-when-the-ac-clutch-engages|The PCM raises idle air when the A/C clutch engages]]"
tags: [hvac, compressor-clutch, spec, air-gap]
---

The electromagnetic A/C compressor clutch on the 1994 F-150 (inventory id `hvac`) has a
specified air gap of 0.018–0.033 in between the clutch plate and pulley. If the gap is too
wide the magnetic field cannot pull the plate in reliably, causing slipping or no engagement;
too tight and the plate can drag on the pulley.

This is the gap to check or shim when a clutch slips, buzzes, or fails to engage even though
the coil is being energized.

## Related Concepts

- [[notes/hvc-pcm-trims-idle-air-when-the-ac-clutch-engages|The PCM raises idle air when the A/C clutch engages]]
- [[notes/hvc-the-pressure-switch-protects-the-clutch-coil-at-low-suction|The refrigerant pressure switch cuts the clutch coil below 24.5 psi suction]]
- [[notes/hvc-the-wot-relay-cuts-ac-at-wide-open-throttle|The WOT A/C relay drops the compressor clutch at wide-open throttle]]
- [[notes/hvc-charging-from-14-oz-cans-jumper-the-pressure-switch|Charge from cans by jumpering the pressure switch and running the A/C to 2.0 lb]]

## Source

- [[sources/hvc-compressor-and-clutch|A/C Compressor and Clutch (FSM)]]
