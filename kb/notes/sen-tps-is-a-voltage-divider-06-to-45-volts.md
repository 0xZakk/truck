---
title: "The TP sensor is a potentiometer that outputs about 0.6 V at closed throttle and 4.5 V at wide open throttle"
kind: spec
source: "[[sources/sen-throttle-position-sensor|Throttle Position (TP) Sensor — Description, Operation, and DTCs (FSM)]]"
related:
  - "[[notes/sen-pcm-reads-throttle-mode-and-rate-from-tps|The PCM derives idle, cruise, WOT, and acceleration-pump action from TP angle and its rate of change]]"
tags:
  - throttle-position-sensor
  - tps
  - fuel
  - spec
---

The TP sensor is wired as a voltage divider. The PCM supplies a 5.0 V reference (VREF) to one
end of a curved resistor, grounds the other end through SIG RTN, and reads the wiper output.
Because the wiper is mechanically tied to the throttle shaft, its voltage tracks throttle plate
angle continuously.

The FSM gives concrete endpoints for the `fuel` system: about **0.6 V at 0% throttle** (closed)
rising to about **4.5 V at 85% throttle** (wide open). These two numbers are the practical
bench/idle check — a healthy sensor sits near 0.6–1.0 V at idle and sweeps smoothly upward with
no dropouts as the throttle opens. A reading pinned at 0 V or 5 V, or a glitchy sweep, points at
a failed pot or a VREF/SIG RTN wiring fault rather than a calibration issue.

## Related Concepts

- [[notes/sen-pcm-reads-throttle-mode-and-rate-from-tps|The PCM derives idle, cruise, WOT, and acceleration-pump action from TP angle and its rate of change]]
- [[notes/eec-tps-is-a-potentiometer-reading-06v-closed-to-45v-wot|The TP sensor is a potentiometer reading about 0.6 V closed to 4.5 V at wide-open throttle]]
- [[notes/eec-install-the-tps-clockwise-only-or-idle-runs-high|Install the TP sensor by rotating it clockwise only, or idle speed runs high]]
- [[notes/eec-pcm-cross-checks-tps-map-and-pulse-width-for-in-range-failures|The PCM cross-checks TP, MAP, and injector pulse width to catch in-range sensor failures]]
- [[notes/sen-eec-iv-sensors-share-vref-and-sig-rtn|Most EEC-IV sensors share a common 5.0 V VREF and SIG RTN ground, so one bad reference skews many readings]]

## Source

- [[sources/sen-throttle-position-sensor|Throttle Position (TP) Sensor — Description, Operation, and DTCs (FSM)]]
