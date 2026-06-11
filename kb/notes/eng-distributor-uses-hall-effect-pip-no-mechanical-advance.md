---
title: "The 4.9L distributor uses a Hall-effect PIP signal and has no mechanical advance"
kind: how-it-works
source: "[[sources/eng-ignition-timing-and-distributor|Distributor & Ignition Timing — Hall-Effect Operation and Timing Procedure (FSM)]]"
related:
  - "[[notes/eng-set-base-timing-by-disconnecting-the-spout-connector|Set base timing by disconnecting the SPOUT connector]]"
tags:
  - engine
  - distributor
  - ignition
  - eec-iv
  - how-it-works
---

The 4.9L `engine`'s gear-driven distributor has a Hall Effect stator and no centrifugal or vacuum
advance — every degree of timing advance is computed electronically by the PCM. The Hall-effect
stator generates the Profile Ignition Pickup (PIP) signal, which tells the PCM crankshaft position.
The PCM returns a Spark Output (SPOUT) signal to the ignition module, which switches the coil
primary on and off to fire the plugs; each interruption fires the secondary to as high as ~40,000
volts, routed through the cap to the plugs.

Two variants exist, identified by ignition control module (ICM) color: a gray ICM is the
push-start system (which actually allows a manual-transmission truck to be push-started), and a
black ICM is the computer-controlled-dwell system where the PCM also manages coil charge time.
Because advance is PCM-controlled, ignition diagnosis follows the signal chain rather than
mechanical parts: confirm PIP from the distributor, confirm SPOUT from the PCM, and check the
ignition control module. There are no weights or vacuum diaphragms to inspect, so a timing or
no-spark problem lives in the Hall sensor, wiring, ICM, or PCM strategy — and timing is set by
isolating SPOUT rather than twisting the distributor against a mechanical advance curve.

> "A Hall Effect stator assembly is used to trigger the ignition coil. This system does not use
> either centrifugal or vacuum advance mechanisms."

## Related Concepts

- [[notes/eng-set-base-timing-by-disconnecting-the-spout-connector|Set base timing by disconnecting the SPOUT connector]]
- [[notes/mnt-base-timing-is-10-degrees-btdc-firing-order-1-5-3-6-2-4|Base ignition timing is 10° BTDC and the 4.9L firing order is 1-5-3-6-2-4]]
- [[notes/sen-cmp-is-camshaft-driven-and-serviceable-in-the-distributor|The camshaft position / cylinder ID sensor lives inside the distributor and is camshaft-driven, so it can be serviced separately]]
- [[notes/sen-pip-is-a-hall-switch-driven-by-a-6-vane-shutter|The PIP signal is a 0–12 V square wave a distributor Hall switch makes as a camshaft-driven 6-vane shutter passes through it]]
- [[notes/mnt-octane-jumper-removed-retards-timing-three-degrees|Pulling the octane-adjust jumper retards computed timing about three degrees to fight detonation]]
- [[notes/mnt-manual-trucks-with-gray-icm-can-be-push-started|Manual-transmission trucks with a gray push-start ICM can be push started]]
- [[notes/sen-narrow-1-shutter-gives-cylinder-identification|A narrower number-1 shutter creates a signature PIP pulse that tells the PCM which cylinder is which]]

## Source

- [[sources/eng-ignition-timing-and-distributor|Distributor & Ignition Timing — Hall-Effect Operation and Timing Procedure (FSM)]]
- [[sources/mnt-distributor|Distributor and Distributor Ignition (DI) System (FSM)]]
