---
title: "Set base timing by disconnecting the SPOUT connector and using the key to start"
kind: procedure
source: "[[sources/eng-ignition-timing-and-distributor|Distributor & Ignition Timing — Hall-Effect Operation and Timing Procedure (FSM)]]"
related:
  - "[[notes/eng-distributor-uses-hall-effect-pip-no-mechanical-advance|The distributor uses a Hall-effect PIP signal and has no mechanical advance]]"
  - "[[notes/eng-49l-firing-order-is-1-5-3-6-2-4|The 4.9L firing order is 1-5-3-6-2-4]]"
tags:
  - engine
  - ignition-timing
  - spout
  - procedure
---

Because the PCM normally adds computed advance, you must isolate the base setting before you can
check or set it. The procedure: put the transmission in neutral (this is the manual-trans truck)
with A/C and heater off, connect an inductive timing light, and disconnect the single-wire in-line
SPOUT connector (or pull the shorting bar from the double-wire connector). Start the engine, let
it reach operating temperature, and set initial timing to 10 degrees BTDC at timing rpm. Then
reconnect SPOUT and confirm the timing advances past the base setting, proving the PCM advance is
working. Remove the test gear.

A critical caution for the `engine` inventory system: start the engine with the ignition key only.
Using a remote starter, or disconnecting the start wire at the starter relay, forces the ignition
module into start-mode timing that will not self-correct even after the engine is running and the
wire is reconnected — so the timing you set would be wrong.

> "To set timing correctly, a remote starter should not be used. Use the ignition key only to start
> the vehicle. Disconnecting the start wire at the starter relay will cause Ignition Control Module
> (ICM) to revert to start mode timing after the vehicle is started."

## Related Concepts

- [[notes/eng-distributor-uses-hall-effect-pip-no-mechanical-advance|The distributor uses a Hall-effect PIP signal and has no mechanical advance]]
- [[notes/eng-49l-firing-order-is-1-5-3-6-2-4|The 4.9L firing order is 1-5-3-6-2-4]]
- [[notes/eec-base-timing-is-10-btdc-set-with-spout-disconnected|Base ignition timing is 10 deg BTDC, set with the SPOUT connector disconnected]]
- [[notes/mnt-octane-jumper-removed-retards-timing-three-degrees|Pulling the octane-adjust jumper retards computed timing about three degrees to fight detonation]]
- [[notes/mnt-base-timing-is-10-degrees-btdc-firing-order-1-5-3-6-2-4|Base ignition timing is 10° BTDC and the 4.9L firing order is 1-5-3-6-2-4]]

## Source

- [[sources/eng-ignition-timing-and-distributor|Distributor & Ignition Timing — Hall-Effect Operation and Timing Procedure (FSM)]]
