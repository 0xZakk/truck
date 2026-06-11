---
title: "The MAP sensor doubles as a barometric pressure sensor to correct fueling for altitude"
kind: how-it-works
source: "[[sources/sen-manifold-absolute-pressure-sensor|Manifold Absolute Pressure (MAP) Sensor — Description, Operation, and DTCs (FSM)]]"
related:
  - "[[notes/eec-map-sensor-outputs-a-frequency-and-doubles-as-a-baro-sensor|The MAP sensor outputs a frequency proportional to load and doubles as a barometric sensor]]"
tags:
  - map-sensor
  - barometric-pressure
  - fuel
---

The 4.9L doesn't carry a separate barometric sensor — the single MAP sensor pulls double duty.
At two moments when manifold vacuum equals atmospheric pressure, the PCM reads the MAP output as
a Barometric Pressure (BP) reference: with the key on and the engine not running, and at wide
open throttle (where the throttle is open enough that manifold pressure ~ atmospheric).

Capturing barometric pressure lets the PCM compensate the `fuel` calculation, ignition advance,
and EGR flow for altitude and weather. At high elevation the air is thinner, so the same
manifold vacuum corresponds to less actual air mass; without a BP correction the engine would
run rich. Re-sampling BP at every WOT event keeps that correction current as the truck climbs
or descends.

This is why a single frequency sensor named "MAP/BARO" can stand in for what other systems split
into two sensors, and why a MAP problem can show up as altitude-dependent driveability rather
than a constant symptom.

## Related Concepts

- [[notes/eec-map-sensor-outputs-a-frequency-and-doubles-as-a-baro-sensor|The MAP sensor outputs a frequency proportional to load and doubles as a barometric sensor]]

## Source

- [[sources/sen-manifold-absolute-pressure-sensor|Manifold Absolute Pressure (MAP) Sensor — Description, Operation, and DTCs (FSM)]]
