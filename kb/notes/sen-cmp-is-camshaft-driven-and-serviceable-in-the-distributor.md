---
title: "The camshaft position / cylinder ID sensor lives inside the distributor and is camshaft-driven, so it can be serviced separately"
kind: spec
source: "[[sources/sen-distributor-hall-effect-pip-cmp-sensor|Distributor Hall-Effect Sensor — PIP, Camshaft Position, and Cylinder Identification (FSM)]]"
related:
  - "[[notes/sen-pip-is-a-hall-switch-driven-by-a-6-vane-shutter|The PIP signal is a 0–12 V square wave a distributor Hall switch makes as a 6-vane shutter passes through it]]"
  - "[[notes/sen-narrow-1-shutter-gives-cylinder-identification|A narrower number-1 shutter creates a signature PIP pulse that tells the PCM which cylinder is which]]"
tags:
  - camshaft-position-sensor
  - distributor
  - ignition
---

The 4.9L's position sensing is packaged inside the distributor: the Hall-effect switch and its
6-vane shutter plate are driven by the camshaft, since the distributor turns at camshaft speed
(half crank speed). The FSM notes the camshaft position (CMP) / cylinder identification sensor
"is located within the distributor and can be serviced separately."

That serviceability detail is practical for the `ignition` system. Because the shutter is
camshaft-driven and the #1 vane is the narrow signature blade, the relationship between the
shutter and the distributor housing fixes cylinder identification — so the sensor's orientation
within the distributor matters, not just that it's electrically alive. Being separately
serviceable means a failed Hall sensor doesn't necessarily require a whole new distributor.

The square-wave output swings 0.0 to 12.0 V; the ICM conditions it into the PIP signal the PCM
uses for both spark timing (advance and dwell) and injector timing.

## Related Concepts

- [[notes/sen-pip-is-a-hall-switch-driven-by-a-6-vane-shutter|The PIP signal is a 0–12 V square wave a distributor Hall switch makes as a 6-vane shutter passes through it]]
- [[notes/sen-narrow-1-shutter-gives-cylinder-identification|A narrower number-1 shutter creates a signature PIP pulse that tells the PCM which cylinder is which]]
- [[notes/eng-distributor-uses-hall-effect-pip-no-mechanical-advance|The 4.9L distributor uses a Hall-effect PIP signal and has no mechanical advance]]

## Source

- [[sources/sen-distributor-hall-effect-pip-cmp-sensor|Distributor Hall-Effect Sensor — PIP, Camshaft Position, and Cylinder Identification (FSM)]]
