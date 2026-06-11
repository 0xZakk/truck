---
title: "A narrower number-1 shutter creates a signature PIP pulse that tells the PCM which cylinder is which"
kind: how-it-works
source: "[[sources/sen-distributor-hall-effect-pip-cmp-sensor|Distributor Hall-Effect Sensor — PIP, Camshaft Position, and Cylinder Identification (FSM)]]"
related:
  - "[[notes/sen-pip-is-a-hall-switch-driven-by-a-6-vane-shutter|The PIP signal is a 0–12 V square wave a distributor Hall switch makes as a 6-vane shutter passes through it]]"
tags:
  - cylinder-identification
  - pip
  - ignition
  - fuel
---

A bare square wave from the PIP sensor tells the PCM the crank is turning and how fast, but not
*which* cylinder is coming up. Ford solves this cleverly with one extra piece of geometry: on
the 6-vane shutter plate, the blade corresponding to cylinder number 1 is cut narrower than the
other five. That produces a shorter "signature" PIP pulse once per camshaft revolution.

The ICM passes this signature pulse through to the PCM as the Cylinder Identification (CID)
signal, letting the PCM recognize when number 1 is on its compression stroke. In a multiport
fuel-injection system the injectors fire in two banks, so the PCM needs that reference to
sequence the banks in the correct order — this is where the `ignition` and `fuel` systems meet
on a single sensor.

If the CID circuit fails, DTC 214 sets. The engine may still run (it can fall back on PIP alone)
but injector sequencing and full sequential timing are compromised, which can hurt driveability
and emissions.

## Related Concepts

- [[notes/sen-pip-is-a-hall-switch-driven-by-a-6-vane-shutter|The PIP signal is a 0–12 V square wave a distributor Hall switch makes as a 6-vane shutter passes through it]]
- [[notes/sen-cmp-is-camshaft-driven-and-serviceable-in-the-distributor|The camshaft position / cylinder ID sensor lives inside the distributor and is camshaft-driven, so it can be serviced separately]]
- [[notes/eec-cmp-in-distributor-produces-the-pip-signal-for-spark-and-injection|The distributor-mounted CMP sensor produces the PIP signal that times both spark and injection]]
- [[notes/dtc-211-and-226-point-to-the-pip-and-idm-crank-signals|DTCs 211 and 226 point at the PIP and IDM crank-timing signals the PCM needs to fire the ignition]]
- [[notes/mnt-distributor-has-no-mechanical-advance-uses-pip-and-spout|The 4.9L distributor has no mechanical advance and relies on PIP and SPOUT signals]]

## Source

- [[sources/sen-distributor-hall-effect-pip-cmp-sensor|Distributor Hall-Effect Sensor — PIP, Camshaft Position, and Cylinder Identification (FSM)]]
