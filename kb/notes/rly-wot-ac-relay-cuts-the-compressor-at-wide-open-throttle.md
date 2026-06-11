---
title: "The WOT A/C relay drops the compressor at wide open throttle to free up power"
kind: how-it-works
source: "[[sources/rly-wot-ac-compressor-clutch-relay|Compressor Clutch Relay (WOT A/C Relay) — Description and Operation (FSM)]]"
related:
  - "[[notes/rly-warning-chime-module-sounds-for-key-in-lights-on-and-unbuckled-belt|The warning chime module sounds for key-in-ignition, lights-on-with-door-open, and unbuckled belt]]"
tags:
  - compressor-clutch-relay
  - wot-ac-relay
  - air-conditioning
  - hvac
---

The Compressor Clutch Relay is the Wide Open Throttle A/C (WOT A/C) relay. When the driver floors
the throttle to wide open, this relay opens and suspends A/C compressor operation, then restores
it once normal (non-WOT) operation resumes. The point is to divert the power that would otherwise
drive the compressor to the drive wheels under heavy acceleration or load.

This explains a normal, non-fault behavior: brief loss of cold air during hard acceleration is by
design, not a failing compressor. In the `electrical-body` accessory-control distribution, this
relay ties HVAC operation to throttle position so it is worth knowing about before diagnosing an
intermittent A/C complaint.

## Related Concepts

- [[notes/rly-warning-chime-module-sounds-for-key-in-lights-on-and-unbuckled-belt|The warning chime module sounds for key-in-ignition, lights-on-with-door-open, and unbuckled belt]]
- [[notes/hvc-the-wot-relay-cuts-ac-at-wide-open-throttle|The WOT A/C relay drops the compressor clutch at wide-open throttle]]
- [[notes/hvc-pcm-trims-idle-air-when-the-ac-clutch-engages|The PCM raises idle air when the A/C clutch engages to keep idle speed from sagging]]
- [[notes/hvc-the-pressure-switch-protects-the-clutch-coil-at-low-suction|The refrigerant pressure switch cuts the clutch coil below 24.5 psi suction]]

## Source

- [[sources/rly-wot-ac-compressor-clutch-relay|Compressor Clutch Relay (WOT A/C Relay) — Description and Operation (FSM)]]
