---
title: "The PCM cross-checks TP, MAP, and injector pulse width to catch in-range sensor failures"
kind: troubleshooting
source: "[[sources/eec-throttle-position-sensor|Throttle Position Sensor (TP) — Operation, DTCs, Service, and Specs (FSM)]]"
related:
  - "[[notes/eec-tps-is-a-potentiometer-reading-06v-closed-to-45v-wot|The TP sensor is a potentiometer reading about 0.6 V closed to 4.5 V at wide-open throttle]]"
  - "[[notes/eec-map-sensor-outputs-a-frequency-and-doubles-as-a-baro-sensor|The MAP sensor outputs a frequency proportional to load and doubles as a barometric sensor]]"
tags:
  - tps
  - map-sensor
  - troubleshooting
  - in-range-failure
  - fuel
---

A sensor can fail without going out of its electrical limits — it reads a plausible value that is
simply wrong. The EEC-IV PCM catches this for the throttle signal with DTCs 124 (TP higher than
expected) and 125 (TP lower than expected). Rather than checking the TP voltage against fixed
limits, the PCM compares three related signals — the TP sensor, the MAP (load) signal, and the
fuel injector pulse width — and flags an in-range code if any one disagrees with the other two.

This is a useful diagnostic mental model: an in-range TP code does not always mean the TP itself
is bad; it means the throttle-vs-load-vs-fueling picture is inconsistent, so a MAP problem or a
fueling problem can also set it. On the original 4.9L the system uses MAP rather than a MAF
sensor for load. Treat DTC 124/125 on the `fuel`/`engine` system as a prompt to verify all three
inputs together.

## Related Concepts

- [[notes/eec-tps-is-a-potentiometer-reading-06v-closed-to-45v-wot|The TP sensor is a potentiometer reading about 0.6 V closed to 4.5 V at wide-open throttle]]
- [[notes/eec-map-sensor-outputs-a-frequency-and-doubles-as-a-baro-sensor|The MAP sensor outputs a frequency proportional to load and doubles as a barometric sensor]]
- [[notes/sen-pcm-reads-throttle-mode-and-rate-from-tps|The PCM derives idle, cruise, WOT, and acceleration-pump action from TP angle and its rate of change]]
- [[notes/dtc-rationality-codes-flag-readings-that-disagree-with-other-sensors|Rationality DTCs flag a sensor reading that disagrees with the rest of the engine picture rather than a broken circuit]]
- [[notes/eec-install-the-tps-clockwise-only-or-idle-runs-high|Install the TP sensor by rotating it clockwise only, or idle speed runs high]]
- [[notes/sen-eec-iv-sensors-share-vref-and-sig-rtn|Most EEC-IV sensors share a common 5.0 V VREF and SIG RTN ground, so one bad reference skews many readings]]

## Source

- [[sources/eec-throttle-position-sensor|Throttle Position Sensor (TP) — Operation, DTCs, Service, and Specs (FSM)]]
