---
title: "Base ignition timing is 10 deg BTDC, set with the SPOUT connector disconnected"
kind: procedure
source: "[[sources/eec-tune-up-and-engine-checks|Tune-up and Engine Performance Checks — Timing, Firing Order, Compression, Valve Clearance, Spark Plugs (FSM)]]"
related:
  - "[[notes/eec-cmp-in-distributor-produces-the-pip-signal-for-spark-and-injection|The distributor-mounted CMP sensor produces the PIP signal that times both spark and injection]]"
  - "[[notes/eec-firing-order-is-1-5-3-6-2-4|The 4.9L I6 firing order is 1-5-3-6-2-4]]"
tags:
  - ignition-timing
  - spout
  - procedure
  - ignition
---

The 4.9L's base ignition timing is 10 deg BTDC. To set it you must first stop the PCM from
adding computed advance: disconnect the in-line single-wire Spark Output (SPOUT) connector (or
pull the shorting bar from the double-wire connector). Put a manual transmission in NEUTRAL with
A/C and heater off, connect an inductive timing light, start the engine, bring it to operating
temperature, and check/adjust initial timing at timing rpm.

Two cautions matter. Start the engine with the ignition key only — a remote starter or a
disconnected start wire leaves the Ignition Control Module in start-mode timing, and reconnecting
the wire after starting will not correct it. After setting, reconnect SPOUT and confirm the
distributor advances beyond the initial setting, which verifies the computed-advance path works.
This is the foundational `ignition`-system adjustment.

## Related Concepts

- [[notes/eec-cmp-in-distributor-produces-the-pip-signal-for-spark-and-injection|The distributor-mounted CMP sensor produces the PIP signal that times both spark and injection]]
- [[notes/eec-firing-order-is-1-5-3-6-2-4|The 4.9L I6 firing order is 1-5-3-6-2-4]]
- [[notes/eng-set-base-timing-by-disconnecting-the-spout-connector|Set base timing by disconnecting the SPOUT connector and using the key to start]]
- [[notes/mnt-base-timing-is-10-degrees-btdc-firing-order-1-5-3-6-2-4|Base ignition timing is 10° BTDC and the 4.9L firing order is 1-5-3-6-2-4]]
- [[notes/mnt-octane-jumper-removed-retards-timing-three-degrees|Pulling the octane-adjust jumper retards computed timing about three degrees to fight detonation]]
- [[notes/eng-49l-firing-order-is-1-5-3-6-2-4|The 4.9L firing order is 1-5-3-6-2-4 with a 10-degree BTDC base timing and 0.042-0.046 in plug gap]]

## Source

- [[sources/eec-tune-up-and-engine-checks|Tune-up and Engine Performance Checks — Timing, Firing Order, Compression, Valve Clearance, Spark Plugs (FSM)]]
