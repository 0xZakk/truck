---
title: "Base ignition timing is 10° BTDC and the 4.9L firing order is 1-5-3-6-2-4"
kind: spec
source: "[[sources/mnt-ignition-timing|Ignition Timing, Octane Connector, and Firing Order (FSM)]]"
related:
  - "[[notes/mnt-octane-jumper-removed-retards-timing-three-degrees|Pulling the octane-adjust jumper retards computed timing about three degrees to fight detonation]]"
  - "[[notes/mnt-distributor-has-no-mechanical-advance-uses-pip-and-spout|The 4.9L distributor has no mechanical advance and relies on PIP and SPOUT signals]]"
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
- [[notes/mnt-distributor-has-no-mechanical-advance-uses-pip-and-spout|The 4.9L distributor has no mechanical advance and relies on PIP and SPOUT signals]]
- [[notes/eec-base-timing-is-10-btdc-set-with-spout-disconnected|Base ignition timing is 10 deg BTDC, set with the SPOUT connector disconnected]]
- [[notes/eng-49l-firing-order-is-1-5-3-6-2-4|The 4.9L firing order is 1-5-3-6-2-4 with a 10-degree BTDC base timing and 0.042-0.046 in plug gap]]
- [[notes/eec-firing-order-is-1-5-3-6-2-4|The 4.9L I6 firing order is 1-5-3-6-2-4]]
- [[notes/eng-set-base-timing-by-disconnecting-the-spout-connector|Set base timing by disconnecting the SPOUT connector and using the key to start]]

## Source

- [[sources/mnt-ignition-timing|Ignition Timing, Octane Connector, and Firing Order (FSM)]]
