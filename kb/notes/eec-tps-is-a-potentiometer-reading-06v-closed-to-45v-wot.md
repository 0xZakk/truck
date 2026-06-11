---
title: "The TP sensor is a potentiometer reading about 0.6 V closed to 4.5 V at wide-open throttle"
kind: how-it-works
source: "[[sources/eec-throttle-position-sensor|Throttle Position Sensor (TP) — Operation, DTCs, Service, and Specs (FSM)]]"
related:
  - "[[notes/eec-install-the-tps-clockwise-only-or-idle-runs-high|Install the TP sensor by rotating it clockwise only, or idle speed runs high]]"
  - "[[notes/eec-pcm-cross-checks-tps-map-and-pulse-width-for-in-range-failures|The PCM cross-checks TP, MAP, and injector pulse width to catch in-range sensor failures]]"
tags:
  - tps
  - throttle-position-sensor
  - potentiometer
  - fuel
---

The Throttle Position (TP) sensor is a rotary potentiometer linked to the throttle shaft and
wired as a voltage divider: a 5.0 V reference (VREF) feeds one end of a curved resistor, the
other end is grounded (SIG RTN), and a wiper arm taps off an output proportional to throttle
angle. At closed throttle the wiper sits near the ground end, giving about 0.6 V at 0% throttle;
at wide-open throttle it sits near the reference end, giving about 4.5 V at 85% throttle angle.

From this single voltage the PCM derives several operating modes: closed throttle
(idle/deceleration), part throttle (cruise), wide-open throttle (max acceleration, dechoke on
crank, A/C cutout), throttle-angle rate (an accelerator-pump-type enrichment), and the
transmission shift schedule. A clean, monotonic sweep is therefore central to the `fuel` and
`engine` systems and to driveability.

## Related Concepts

- [[notes/eec-install-the-tps-clockwise-only-or-idle-runs-high|Install the TP sensor by rotating it clockwise only, or idle speed runs high]]
- [[notes/eec-pcm-cross-checks-tps-map-and-pulse-width-for-in-range-failures|The PCM cross-checks TP, MAP, and injector pulse width to catch in-range sensor failures]]
- [[notes/sen-tps-is-a-voltage-divider-06-to-45-volts|The TP sensor is a potentiometer that outputs about 0.6 V at closed throttle and 4.5 V at wide open throttle]]
- [[notes/sen-pcm-reads-throttle-mode-and-rate-from-tps|The PCM derives idle, cruise, WOT, and acceleration-pump action from TP angle and its rate of change]]

## Source

- [[sources/eec-throttle-position-sensor|Throttle Position Sensor (TP) — Operation, DTCs, Service, and Specs (FSM)]]
