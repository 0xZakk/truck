---
title: "Manifold Absolute Pressure (MAP) Sensor — Description, Operation, and DTCs (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Sensors%20and%20Switches/Sensors%20and%20Switches%20-%20Powertrain%20Management/Sensors%20and%20Switches%20-%20Computers%20and%20Control%20Systems/Manifold%20Pressure%2FVacuum%20Sensor/Description%20and%20Operation/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - map-sensor
  - engine-load
  - fuel
  - eec-iv
processed: true
---

## Summary

The Manifold Absolute Pressure (MAP) sensor produces a signal proportional to engine load by
measuring manifold vacuum. Low vacuum means high load; high vacuum means light load. The PCM
uses this load data to set fuel injection base pulse width, ignition timing advance, and EGR
flow. On the 1994 4.9L this is a frequency-output (Ford "MAP/BARO") sensor, not the analog
voltage MAP found on many other vehicles.

The sensor uses a pressure-sensitive piezoelectric disc whose electrical characteristics change
with applied pressure. A vacuum line connects its sensing port to the intake manifold; internal
circuitry converts the disc signal into a frequency-modulated output. Output varies directly
with load and inversely with vacuum, running about 159 Hz at 0.0 in Hg to 95 Hz at 24.0 in Hg.

The same sensor doubles as a Barometric Pressure (BP) sensor whenever the key is on with the
engine off and at wide open throttle, letting the PCM compensate for altitude and weather. It
is a three-wire device: VREF (5.0 V power), MAP/BARO SIG output, and SIG RTN ground. DTCs:
22/126 out of range during self-test (140–160 Hz), 81/128 vacuum changed less than 2 in Hg in
normal operation, and 72/129 output didn't change enough during the snap-throttle dynamic test.

## Key Points

- Frequency-output (not analog-voltage) MAP sensor; ~159 Hz at 0 in Hg to ~95 Hz at 24 in Hg.
- Piezoelectric disc; output rises with load and falls with vacuum.
- Reports engine load for fuel base pulse width, ignition advance, and EGR flow.
- Doubles as Barometric Pressure sensor at key-on-engine-off and at WOT for altitude correction.
- Three wires: VREF 5.0 V, MAP/BARO SIG, SIG RTN.
- DTCs: 22/126 out of range (140–160 Hz); 81/128 <2 in Hg change; 72/129 no change on snap throttle.

## Notable Excerpts

> "The output frequency of the MAP sensor varies directly with engine load and indirectly with
> manifold vacuum. The normal operating range of the MAP sensor is 159Hz (0.0 in Hg) to 95Hz
> (24.0 in Hg)."

> "The MAP sensor also acts as a Barometric Pressure (BP) sensor when the key is on and the
> engine is not running and at Wide Open Throttle (WOT)."

Source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Sensors%20and%20Switches/Sensors%20and%20Switches%20-%20Powertrain%20Management/Sensors%20and%20Switches%20-%20Computers%20and%20Control%20Systems/Manifold%20Pressure%2FVacuum%20Sensor/Description%20and%20Operation/index.html
