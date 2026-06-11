---
title: "The MAP sensor outputs a frequency proportional to load and doubles as a barometric sensor"
kind: how-it-works
source: "[[sources/eec-map-sensor|Manifold Absolute Pressure (MAP) Sensor — Operation, DTCs, and Range (FSM)]]"
related:
  - "[[notes/eec-pcm-cross-checks-tps-map-and-pulse-width-for-in-range-failures|The PCM cross-checks TP, MAP, and injector pulse width to catch in-range sensor failures]]"
tags:
  - map-sensor
  - manifold-absolute-pressure
  - frequency
  - engine-load
  - fuel
---

Unlike a typical analog MAP sensor, the 1994 4.9L's Manifold Absolute Pressure sensor outputs a
frequency-modulated square wave, not the 0–5 V analog signal used on many other engines. A
vacuum line connects it to the intake manifold, and a pressure-sensitive piezoelectric disc plus
onboard circuitry converts manifold vacuum into that frequency. Output varies directly with
engine load and inversely with vacuum, ranging 159 Hz at 0.0 in Hg (no vacuum, full load) down
to 95 Hz at 24.0 in Hg (high vacuum, light load). The PCM uses this load reading to set fuel
injection base pulse width, ignition timing advance, and EGR flow. Because the output is a
frequency, you can't diagnose it with a plain DC voltmeter the way you would an analog MAP; you
need a meter that reads Hz (or a scan tool) to verify it tracks vacuum correctly.

The same sensor doubles as a Barometric Pressure (BP) sensor: when the key is on with the engine
off, and at wide-open throttle, it reads atmospheric pressure so the PCM can compensate for
altitude and weather. Its three wires are VREF (5.0 V), MAP/BARO SIG (output), and SIG RTN
(ground). Relevant DTCs are 22/126 (out of range during self-test), 81/128 (vacuum did not
change >2 in, e.g. a plugged vacuum line or lazy sensor), and 72/129 (no change during the
snap-throttle test) — the latter two catching a lazy sensor rather than a hard open or short.
This is central to the `engine`, `fuel`, and `ignition` systems.

## Related Concepts

- [[notes/eec-pcm-cross-checks-tps-map-and-pulse-width-for-in-range-failures|The PCM cross-checks TP, MAP, and injector pulse width to catch in-range sensor failures]]
- [[notes/sen-map-doubles-as-a-barometric-pressure-sensor|The MAP sensor doubles as a barometric pressure sensor to correct fueling for altitude]]
- [[notes/sen-pcm-reads-throttle-mode-and-rate-from-tps|The PCM derives idle, cruise, WOT, and acceleration-pump action from TP angle and its rate of change]]

## Source

- [[sources/eec-map-sensor|Manifold Absolute Pressure (MAP) Sensor — Operation, DTCs, and Range (FSM)]]
- [[sources/sen-manifold-absolute-pressure-sensor|Manifold Absolute Pressure (MAP) Sensor — Description, Operation, and DTCs (FSM)]]
