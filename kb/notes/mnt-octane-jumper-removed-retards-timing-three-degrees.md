---
title: "Pulling the octane-adjust jumper retards computed timing about three degrees to fight detonation"
kind: how-it-works
source: "[[sources/mnt-ignition-timing|Ignition Timing, Octane Connector, and Firing Order (FSM)]]"
related:
  - "[[notes/mnt-base-timing-is-10-degrees-btdc-firing-order-1-5-3-6-2-4|Base ignition timing is 10° BTDC and the 4.9L firing order is 1-5-3-6-2-4]]"
tags:
  - engine
  - ignition
  - timing
---

The 4.9L `engine` has an in-line octane-adjust connector with a shorting-bar jumper that lets you
trade spark advance for knock resistance. With the jumper INSTALLED, the computed timing is normal.
With the jumper REMOVED, the PCM retards computed timing by approximately three degrees, reducing
detonation when lower-grade fuel is used.

This is a deliberate field adjustment, not a fault. If a truck pings on cheaper fuel, pulling the
octane jumper is the sanctioned way to calm it without changing base timing. Conversely, a missing
or removed jumper is worth checking when an engine seems lazy — it is quietly giving up three
degrees of advance.

## Related Concepts

- [[notes/mnt-base-timing-is-10-degrees-btdc-firing-order-1-5-3-6-2-4|Base ignition timing is 10° BTDC and the 4.9L firing order is 1-5-3-6-2-4]]
- [[notes/eec-base-timing-is-10-btdc-set-with-spout-disconnected|Base ignition timing is 10 deg BTDC, set with the SPOUT connector disconnected]]
- [[notes/eng-set-base-timing-by-disconnecting-the-spout-connector|Set base timing by disconnecting the SPOUT connector and using the key to start]]
- [[notes/eec-firing-order-is-1-5-3-6-2-4|The 4.9L I6 firing order is 1-5-3-6-2-4]]
- [[notes/eng-distributor-uses-hall-effect-pip-no-mechanical-advance|The 4.9L distributor uses a Hall-effect PIP signal and has no mechanical advance]]

## Source

- [[sources/mnt-ignition-timing|Ignition Timing, Octane Connector, and Firing Order (FSM)]]
