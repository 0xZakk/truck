---
title: "The starter Load Test cranks the engine by feeding the relay S terminal from a remote switch"
kind: procedure
source: "[[sources/chg-starter-motor-bench-tests|Starter Motor — Bench and Load Tests (FSM)]]"
related:
  - "[[notes/chg-starter-no-load-test-finds-shorts-and-rubbing-armature|The starter No-Load test finds shorted windings and a rubbing armature by reading current draw]]"
  - "[[notes/chg-starter-current-draw-specs-vary-by-starter-diameter|Starter current-draw specs vary by starter diameter]]"
tags:
  - starter
  - starting-system
  - procedure
  - diagnosis
---

The in-vehicle starter Load Test measures how much current the starter draws while actually
cranking. With the Rotunda Starting and Charging Tester connected and the carbon-pile
rheostat at maximum counterclockwise (no current), disconnect the push-on "S" terminal at
the **starter relay** and connect a remote-control starter switch from the positive battery
terminal to the relay's "S" terminal. Put the transmission in NEUTRAL/PARK (automatic) or
fully depress the clutch (manual), then crank with the ignition switch OFF and record the
voltmeter reading.

Stop cranking, reduce the carbon-pile resistance until the voltmeter matches that recorded
value, and read the load current off the ammeter. Compare it to the starter electrical
specifications. Bypassing the relay "S" terminal with the remote switch isolates the
starter and relay from the rest of the start circuit, so the test reflects the starter
itself rather than a weak interlock or ignition-switch signal.

> "Disconnect push on 'S' terminal at starter relay, then connect remote control starter
> switch from positive battery terminal and 'S' terminal of starter relay. … crank engine
> with ignition switch OFF."

This relates to truck inventory system `electrical-starting`.

## Related Concepts

- [[notes/chg-starter-no-load-test-finds-shorts-and-rubbing-armature|The starter No-Load test finds shorted windings and a rubbing armature by reading current draw]]
- [[notes/chg-starter-current-draw-specs-vary-by-starter-diameter|Starter current-draw specs vary by starter diameter]]
- [[notes/chg-starter-solenoid-test-checks-continuity-s-to-m-and-s-to-ground|The starter solenoid test checks continuity from S to M and from S to ground]]
- [[notes/chg-clutch-switch-is-an-in-series-interlock-to-the-starter-relay|The starting interlock switch sits in series between the start signal and the starter relay]]

## Source

- [[sources/chg-starter-motor-bench-tests|Starter Motor — Bench and Load Tests (FSM)]]
