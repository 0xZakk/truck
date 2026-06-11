---
title: "The distributor-mounted CMP sensor produces the PIP signal that times both spark and injection"
kind: how-it-works
source: "[[sources/eec-camshaft-position-sensor|Camshaft Position (CMP) Sensor and PIP Signal — Operation and Specs (FSM)]]"
related:
  - "[[notes/eec-base-timing-is-10-btdc-set-with-spout-disconnected|Base ignition timing is 10 deg BTDC, set with the SPOUT connector disconnected]]"
tags:
  - cmp
  - camshaft-position-sensor
  - pip
  - hall-effect
  - ignition
---

On the 4.9L the Camshaft Position (CMP) sensor lives inside the distributor and uses a Hall
effect switch reading a camshaft-driven 6-bladed shutter plate. Each blade corresponds to a
crankshaft position; as the plate passes the Hall switch the output alternates between 0.0 and
12.0 V in a square wave. This signal goes to the Ignition Control Module (ICM), which converts
it to the Profile Ignition Pickup (PIP) signal sent to the PCM.

PIP is the backbone timing reference: from it the PCM gets crank position, base timing, and
engine speed, and uses them for fuel injector timing and for calculating ignition advance and
dwell. So a single distributor sensor underpins both the `ignition` and `fuel` systems — losing
PIP loses spark and injection timing together. Spec checks: PIP at KOEO reads >8.0 V DC with the
Hall switch shut, and 3.0-8.5 V AC while cranking.

## Related Concepts

- [[notes/eec-base-timing-is-10-btdc-set-with-spout-disconnected|Base ignition timing is 10 deg BTDC, set with the SPOUT connector disconnected]]
- [[notes/sen-cmp-is-camshaft-driven-and-serviceable-in-the-distributor|The camshaft position / cylinder ID sensor lives inside the distributor and is camshaft-driven, so it can be serviced separately]]
- [[notes/sen-pip-is-a-hall-switch-driven-by-a-6-vane-shutter|The PIP signal is a 0–12 V square wave a distributor Hall switch makes as a 6-vane shutter passes through it]]
- [[notes/sen-narrow-1-shutter-gives-cylinder-identification|A narrower number-1 shutter creates a signature PIP pulse that tells the PCM which cylinder is which]]
- [[notes/mnt-distributor-has-no-mechanical-advance-uses-pip-and-spout|The 4.9L distributor has no mechanical advance and relies on PIP and SPOUT signals]]
- [[notes/eng-distributor-uses-hall-effect-pip-no-mechanical-advance|The distributor uses a Hall-effect PIP signal and has no mechanical advance]]

## Source

- [[sources/eec-camshaft-position-sensor|Camshaft Position (CMP) Sensor and PIP Signal — Operation and Specs (FSM)]]
