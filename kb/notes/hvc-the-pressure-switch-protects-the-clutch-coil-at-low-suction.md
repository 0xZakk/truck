---
title: "The refrigerant pressure switch cuts the clutch coil below 24.5 psi suction"
kind: how-it-works
source: "[[sources/hvc-compressor-clutch-controls|A/C Compressor Clutch Controls — Relay and Pressure Switch (FSM)]]"
related:
  - "[[notes/hvc-the-wot-relay-cuts-ac-at-wide-open-throttle|The WOT A/C relay drops the compressor clutch at wide-open throttle]]"
  - "[[notes/hvc-pcm-trims-idle-air-when-the-ac-clutch-engages|The PCM raises idle air when the A/C clutch engages]]"
tags: [hvac, pressure-switch, compressor-clutch, refrigerant]
---

The refrigerant pressure sensor/switch on the 1994 F-150 (inventory id `hvac`) cuts power to
the A/C clutch field coil when suction pressure is too low — protecting the compressor from
running with insufficient refrigerant. It has built-in hysteresis: it closes (allowing the
clutch) at 293 kPa (43.5 psi) with pressure rising, and opens (disconnecting the clutch) at
169 kPa (24.5 psi) with pressure falling.

This switch is also the "clutch cycling" switch that the system cycles on and off in normal
operation, and it is the connector that gets jumpered during charging so refrigerant can be
drawn in before pressure builds. A clutch that will not engage at all on an empty or low
system is often this switch correctly doing its protective job.

## Related Concepts

- [[notes/hvc-the-wot-relay-cuts-ac-at-wide-open-throttle|The WOT A/C relay drops the compressor clutch at wide-open throttle]]
- [[notes/hvc-pcm-trims-idle-air-when-the-ac-clutch-engages|The PCM raises idle air when the A/C clutch engages]]
- [[notes/hvc-charging-from-14-oz-cans-jumper-the-pressure-switch|Charge from cans by jumpering the pressure switch and running the A/C to 2.0 lb]]
- [[notes/hvc-compressor-clutch-air-gap-spec|The A/C compressor clutch air gap must be 0.018–0.033 in]]
- [[notes/rly-wot-ac-relay-cuts-the-compressor-at-wide-open-throttle|The WOT A/C relay drops the compressor at wide open throttle to free up power]]

## Source

- [[sources/hvc-compressor-clutch-controls|A/C Compressor Clutch Controls — Relay and Pressure Switch (FSM)]]
