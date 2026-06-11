---
title: "The PCM raises idle air when the A/C clutch engages to keep idle speed from sagging"
kind: how-it-works
source: "[[sources/hvc-compressor-and-clutch|A/C Compressor and Clutch (FSM)]]"
related:
  - "[[notes/hvc-the-wot-relay-cuts-ac-at-wide-open-throttle|The WOT A/C relay drops the compressor clutch at wide-open throttle]]"
  - "[[notes/hvc-the-pressure-switch-protects-the-clutch-coil-at-low-suction|The refrigerant pressure switch cuts the clutch coil below 24.5 psi suction]]"
tags: [hvac, compressor-clutch, pcm, idle-air]
---

On the 1994 F-150 (inventory id `hvac`), engaging the A/C compressor clutch adds a sudden
mechanical load to the engine that would otherwise pull idle speed down. The Powertrain
Control Module avoids this by monitoring the A/C Clutch (ACC) apply signal: the moment the
clutch is commanded on, the PCM knows the load is coming and adjusts the Idle Air Control-
Bypass Air (IAC-BPA) valve to admit more air and hold the proper idle speed.

This is why a rough or stalling idle that appears only when the A/C is switched on points at
the idle-air control path or the ACC signal the PCM uses, not necessarily at the A/C system
itself. The clutch and the idle-air strategy are deliberately coupled.

## Related Concepts

- [[notes/hvc-the-wot-relay-cuts-ac-at-wide-open-throttle|The WOT A/C relay drops the compressor clutch at wide-open throttle]]
- [[notes/hvc-the-pressure-switch-protects-the-clutch-coil-at-low-suction|The refrigerant pressure switch cuts the clutch coil below 24.5 psi suction]]
- [[notes/hvc-compressor-clutch-air-gap-spec|The A/C compressor clutch air gap must be 0.018–0.033 in]]
- [[notes/hvc-charging-from-14-oz-cans-jumper-the-pressure-switch|Charge from cans by jumpering the pressure switch and running the A/C to 2.0 lb]]
- [[notes/eec-iac-meters-air-around-the-throttle-plate-via-pcm-duty-cycle|The IAC valve sets idle by metering air around the throttle plate via a PCM-controlled duty cycle]]

## Source

- [[sources/hvc-compressor-and-clutch|A/C Compressor and Clutch (FSM)]]
