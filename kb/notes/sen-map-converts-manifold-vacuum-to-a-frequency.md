---
title: "The MAP sensor reports engine load as a frequency that falls as manifold vacuum rises"
kind: how-it-works
source: "[[sources/sen-manifold-absolute-pressure-sensor|Manifold Absolute Pressure (MAP) Sensor — Description, Operation, and DTCs (FSM)]]"
related:
  - "[[notes/sen-map-doubles-as-a-barometric-pressure-sensor|The MAP sensor doubles as a barometric pressure sensor to correct fueling for altitude]]"
  - "[[notes/sen-pcm-reads-throttle-mode-and-rate-from-tps|The PCM derives idle, cruise, WOT, and acceleration-pump action from TP angle and its rate of change]]"
tags:
  - map-sensor
  - engine-load
  - fuel
---

A point worth flagging for the 1994 4.9L: its MAP sensor is a **frequency-output** device, not
the 0–5 V analog MAP used on many other engines. A piezoelectric disc senses manifold vacuum
through a vacuum line, and onboard circuitry turns that into a frequency-modulated square wave.
Output runs about 159 Hz at 0.0 in Hg (no vacuum, full load) down to 95 Hz at 24.0 in Hg (high
vacuum, light load) — so frequency rises with load and falls with vacuum.

The PCM treats this frequency as its measure of engine load and uses it to set the `fuel` base
pulse width, ignition timing advance, and EGR flow. Because the output is a frequency, you can't
diagnose it with a plain DC voltmeter the way you would an analog MAP; you need a meter that
reads Hz (or a scan tool) to verify it tracks vacuum correctly.

A MAP whose vacuum doesn't change enough during operation sets DTC 81/128, and one that fails to
respond to a snap-throttle test sets 72/129 — both aimed at catching a plugged vacuum line or a
lazy sensor rather than a hard open or short.

## Related Concepts

- [[notes/sen-map-doubles-as-a-barometric-pressure-sensor|The MAP sensor doubles as a barometric pressure sensor to correct fueling for altitude]]
- [[notes/sen-pcm-reads-throttle-mode-and-rate-from-tps|The PCM derives idle, cruise, WOT, and acceleration-pump action from TP angle and its rate of change]]
- [[notes/eec-map-sensor-outputs-a-frequency-and-doubles-as-a-baro-sensor|The MAP sensor outputs a frequency proportional to load and doubles as a barometric sensor]]
- [[notes/sen-tps-is-a-voltage-divider-06-to-45-volts|The TP sensor is a potentiometer that outputs about 0.6 V at closed throttle and 4.5 V at wide open throttle]]
- [[notes/eec-pcm-cross-checks-tps-map-and-pulse-width-for-in-range-failures|The PCM cross-checks TP, MAP, and injector pulse width to catch in-range sensor failures]]

## Source

- [[sources/sen-manifold-absolute-pressure-sensor|Manifold Absolute Pressure (MAP) Sensor — Description, Operation, and DTCs (FSM)]]
