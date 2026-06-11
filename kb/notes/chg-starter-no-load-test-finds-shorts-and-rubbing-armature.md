---
title: "The starter No-Load test finds shorted windings and a rubbing armature by reading current draw"
kind: procedure
source: "[[sources/chg-starter-motor-bench-tests|Starter Motor — Bench and Load Tests (FSM)]]"
related:
  - "[[notes/chg-starter-current-draw-specs-vary-by-starter-diameter|Starter current-draw specs vary by starter diameter]]"
  - "[[notes/chg-starter-load-test-feeds-the-relay-s-terminal-from-a-remote-switch|The starter Load Test cranks the engine by feeding the relay S terminal from a remote switch]]"
tags:
  - starter
  - starting-system
  - procedure
  - diagnosis
---

The starter No-Load test is a bench-only check that exposes open or shorted windings or a
rubbing armature. Using the Rotunda Starting and Charging Tester (No. 078-00005) with cables
the same gauge as in the vehicle, set the carbon-pile rheostat fully counterclockwise so no
current flows, then run the starter and record the exact voltmeter reading. Disconnect the
starter, reduce rheostat resistance until the voltmeter shows that same reading, and read the
no-load current off the ammeter.

Compare that current to the starter electrical specifications. If it **exceeds**
specification, suspect a rubbing armature, bent shaft, binding bearings, or shorts in the
armature or brushes — all mechanical or insulation faults that make the motor draw more than
it should even with nothing to turn.

> "The starter No-Load test will uncover such conditions as open or shorted windings, or
> rubbing armature. The starter can be tested, at no-load, on the test bench only."

This relates to truck inventory system `electrical-starting`.

## Related Concepts

- [[notes/chg-starter-current-draw-specs-vary-by-starter-diameter|Starter current-draw specs vary by starter diameter]]
- [[notes/chg-starter-load-test-feeds-the-relay-s-terminal-from-a-remote-switch|The starter Load Test cranks the engine by feeding the relay S terminal from a remote switch]]
- [[notes/chg-starter-solenoid-test-checks-continuity-s-to-m-and-s-to-ground|The starter solenoid test checks continuity from S to M and from S to ground]]

## Source

- [[sources/chg-starter-motor-bench-tests|Starter Motor — Bench and Load Tests (FSM)]]
