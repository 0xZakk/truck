---
title: "At least two sensors — one primary plus the safing sensor — must close together to deploy the air bag"
kind: how-it-works
source: "[[sources/rst-air-bag-impact-and-safing-sensors|Air Bag Impact (Crash) Sensors and Safing Sensor — Description, Operation, Specs (FSM)]]"
related:
  - "[[notes/rst-air-bag-deploys-in-four-steps-in-a-fraction-of-a-second|The air bag deploys in four steps in a fraction of a second]]"
  - "[[notes/rst-undamaged-srs-sensors-reset-and-can-be-reused|Undamaged SRS sensors reset automatically and can be reused]]"
tags:
  - air-bag
  - impact-sensor
  - safing-sensor
  - srs
---

The SRS uses three sensors, each an electrical switch that closes in response to impact direction and force:
a primary crash sensor at the center of the radiator support, a primary sensor on the right frame rail, and
a safing sensor at the right cowl side trim panel. Deployment requires at least two of them — one primary
sensor AND the safing sensor — to be closed at the same time. This two-of-three "safing" logic is a
deliberate guard: a single sensor closing from a pothole, a minor knock, or a fault cannot fire the bag on
its own.

For diagnosis and crash repair this matters because the deployment decision is hard-wired through these
sensors, not made by the diagnostic monitor. Their mounting orientation on the radiator support, frame rail,
and cowl (`body-cab`) is therefore critical, and bracket deformation can quietly defeat the system. These
sensors sit at the boundary of the `body-cab` structure and the `interior` SRS.

> "At least two sensors (one primary sensor and one safing sensor) must be closed to inflate the air bag."

## Related Concepts

- [[notes/rst-air-bag-deploys-in-four-steps-in-a-fraction-of-a-second|The air bag deploys in four steps in a fraction of a second]]
- [[notes/rst-undamaged-srs-sensors-reset-and-can-be-reused|Undamaged SRS sensors reset automatically and can be reused]]
- [[notes/rly-air-bag-monitor-diagnoses-but-does-not-deploy-the-air-bag|The air bag diagnostic monitor only diagnoses the SRS; hard-wired sensors deploy the air bag]]
- [[notes/rst-srs-supplements-belts-and-runs-from-battery-in-any-key-position|The air bag SRS supplements the belts and runs straight from the battery in any key position]]
- [[notes/rst-use-the-2-ohm-air-bag-simulator-not-a-zero-ohm-jumper|Diagnose the SRS with a 2-ohm air bag simulator, never a zero-ohm jumper]]

## Source

- [[sources/rst-air-bag-impact-and-safing-sensors|Air Bag Impact (Crash) Sensors and Safing Sensor — Description, Operation, Specs (FSM)]]
