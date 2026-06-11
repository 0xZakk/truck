---
title: "Base ignition timing is 10° BTDC and the 4.9L firing order is 1-5-3-6-2-4"
kind: spec
source: "[[sources/mnt-ignition-timing|Ignition Timing, Octane Connector, and Firing Order (FSM)]]"
related:
  - "[[notes/mnt-octane-jumper-removed-retards-timing-three-degrees|Pulling the octane-adjust jumper retards computed timing about three degrees to fight detonation]]"
  - "[[notes/eng-distributor-uses-hall-effect-pip-no-mechanical-advance|The 4.9L distributor uses a Hall-effect PIP signal and has no mechanical advance]]"
tags:
  - engine
  - ignition
  - timing
  - spec
---

The 4.9L I6 base ignition timing is 10° BTDC, and the firing order is 1-5-3-6-2-4. These two
specs are the anchors for any ignition work on the `engine`: the firing order dictates plug-wire
routing on the cap, and 10° BTDC is the reference you set base timing to (with the SPOUT/octane
jumper handled per procedure) before letting the PCM compute advance.

Getting either wrong produces classic symptoms — a swapped pair of plug wires causes a stumble or
backfire, and incorrect base timing shifts the whole computed-advance curve, hurting drivability,
power, and knock margin.

## Related Concepts

- [[notes/mnt-octane-jumper-removed-retards-timing-three-degrees|Pulling the octane-adjust jumper retards computed timing about three degrees to fight detonation]]
- [[notes/eng-distributor-uses-hall-effect-pip-no-mechanical-advance|The 4.9L distributor uses a Hall-effect PIP signal and has no mechanical advance]]
- [[notes/eec-base-timing-is-10-btdc-set-with-spout-disconnected|Base ignition timing is 10 deg BTDC, set with the SPOUT connector disconnected]]
- [[notes/eng-49l-firing-order-is-1-5-3-6-2-4|The 4.9L firing order is 1-5-3-6-2-4 with a 10-degree BTDC base timing and 0.042-0.046 in plug gap]]
- [[notes/eec-firing-order-is-1-5-3-6-2-4|The 4.9L I6 firing order is 1-5-3-6-2-4]]
- [[notes/eng-set-base-timing-by-disconnecting-the-spout-connector|Set base timing by disconnecting the SPOUT connector and using the key to start]]
- [[notes/mnt-spark-plug-gap-is-042-046-inch-torque-10-15-ftlb|Spark plugs are gapped 0.042-0.046 in and torqued to 10-15 ft lb]]

## Source

- [[sources/mnt-ignition-timing|Ignition Timing, Octane Connector, and Firing Order (FSM)]]
