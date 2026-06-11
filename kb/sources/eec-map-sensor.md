---
title: "Manifold Absolute Pressure (MAP) Sensor — Operation, DTCs, and Range (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Powertrain%20Management/Computers%20and%20Control%20Systems/Manifold%20Pressure%2FVacuum%20Sensor/Description%20and%20Operation/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - map-sensor
  - manifold-absolute-pressure
  - barometric-pressure
  - eec-iv
  - engine-load
processed: true
---

## Summary

The Manifold Absolute Pressure (MAP) sensor produces a signal proportional to engine load. It
measures manifold vacuum through a vacuum line and converts it, via a pressure-sensitive
piezoelectric disc, into a frequency-modulated output. Low vacuum corresponds to high load and
high vacuum to light load. The PCM uses this load data to set fuel injection base pulse width,
ignition timing advance, and EGR flow.

The MAP sensor's output frequency varies directly with engine load and indirectly with
manifold vacuum, ranging 159 Hz (0.0 in Hg) to 95 Hz (24.0 in Hg). It doubles as a Barometric
Pressure (BP) sensor when the key is on with the engine not running, and at wide-open throttle,
letting the PCM compensate for altitude and atmospheric pressure changes.

The three-wire connection is VREF (5.0 V supply), MAP/BARO SIG (output), and SIG RTN (ground).

## Key Points

- Frequency output proportional to engine load; piezoelectric disc converts manifold vacuum.
- Range: 159 Hz (0.0 in Hg) to 95 Hz (24.0 in Hg).
- Doubles as barometric pressure sensor at key-on/engine-off and at WOT, for altitude compensation.
- PCM uses load data for fuel pulse width, ignition advance, and EGR flow.
- 3 wires: VREF (5.0 V), MAP/BARO SIG (output), SIG RTN (ground).
- DTCs: 22/126 out-of-range during self-test (140-160 Hz), 81/128 vacuum did not change >2 in, 72/129 output did not change enough during snap-throttle dynamic response test.

## Notable Excerpts

> "Low engine vacuum corresponds to high engine load and high vacuum corresponds to a light engine load."

> "The MAP sensor also acts as a Barometric Pressure (BP) sensor when the key is on and the engine is not running and at Wide Open Throttle (WOT)."

Relates to truck inventory systems `engine`, `fuel`, and `ignition`.

Source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Powertrain%20Management/Computers%20and%20Control%20Systems/Manifold%20Pressure%2FVacuum%20Sensor/Description%20and%20Operation/index.html
