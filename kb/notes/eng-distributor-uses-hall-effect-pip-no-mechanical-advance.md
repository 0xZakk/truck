---
title: "The distributor uses a Hall-effect PIP signal and has no mechanical advance"
kind: how-it-works
source: "[[sources/eng-ignition-timing-and-distributor|Distributor & Ignition Timing — Hall-Effect Operation and Timing Procedure (FSM)]]"
related:
  - "[[notes/eng-set-base-timing-by-disconnecting-the-spout-connector|Set base timing by disconnecting the SPOUT connector]]"
tags:
  - engine
  - distributor
  - ignition
  - how-it-works
---

The 4.9L's gear-driven distributor has no centrifugal or vacuum advance — all timing advance is
computed by the PCM. A Hall-effect stator inside the distributor generates the Profile Ignition
Pickup (PIP) signal, which tells the PCM crankshaft position. The PCM returns a Spark Output
(SPOUT) signal to the ignition module, which switches the coil primary on and off to fire the
plugs, producing secondary voltage as high as 40,000 V.

Two variants exist, identified by ignition control module (ICM) color: a gray ICM is the
push-start system (which actually allows a manual-transmission truck to be push-started), and a
black ICM is the computer-controlled-dwell system where the PCM also manages coil charge time.
This is central to how the `engine` inventory system's ignition behaves and why timing is set by
isolating SPOUT rather than twisting the distributor against a mechanical advance curve.

> "A Hall Effect stator assembly is used to trigger the ignition coil. This system does not use
> either centrifugal or vacuum advance mechanisms."

## Related Concepts

- [[notes/eng-set-base-timing-by-disconnecting-the-spout-connector|Set base timing by disconnecting the SPOUT connector]]
- [[notes/mnt-distributor-has-no-mechanical-advance-uses-pip-and-spout|The 4.9L distributor has no mechanical advance and relies on PIP and SPOUT signals]]
- [[notes/sen-pip-is-a-hall-switch-driven-by-a-6-vane-shutter|The PIP signal is a 0–12 V square wave a distributor Hall switch makes as a 6-vane shutter passes through it]]
- [[notes/sen-cmp-is-camshaft-driven-and-serviceable-in-the-distributor|The camshaft position / cylinder ID sensor lives inside the distributor and is camshaft-driven, so it can be serviced separately]]
- [[notes/eec-cmp-in-distributor-produces-the-pip-signal-for-spark-and-injection|The distributor-mounted CMP sensor produces the PIP signal that times both spark and injection]]
- [[notes/mnt-manual-trucks-with-gray-icm-can-be-push-started|Manual-transmission trucks with a gray push-start ICM can be push started]]

## Source

- [[sources/eng-ignition-timing-and-distributor|Distributor & Ignition Timing — Hall-Effect Operation and Timing Procedure (FSM)]]
