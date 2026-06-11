---
title: "The low-oil indicator trips when oil is about 1.5 quarts low and waits five minutes for drain-back"
kind: how-it-works
source: "[[sources/mnt-engine-oil|Engine Oil Capacity and the Low Oil Level Indicator (FSM)]]"
related:
  - "[[notes/mnt-engine-oil-refill-is-5-quarts-with-filter|The 4.9L engine oil refill is 5.0 quarts including the filter]]"
tags:
  - engine
  - engine-oil
  - warning-indicator
  - oil-level-warning-indicator
  - lubrication
---

The low oil-level warning uses a float-type sensor in the oil pan, an electronic control module,
and a dash "Check Oil" lamp. The lamp proves out (lights) in START, then the module reads the
sensor in RUN: if the level is adequate the lamp goes out, but if oil is approximately 1.5 quarts
or more low the relay turns the lamp on and holds it until the ignition is switched off. This
low-level warning is a separate system from the oil pressure warning lamp.

A key behavior is the timing: the module deliberately does not re-read the pan sensor immediately
after shutoff. After the ignition is turned OFF it will not reset for approximately five minutes,
allowing oil to drain back into the pan so the float gives a settled, accurate reading. Without
this delay, oil clinging to the upper engine right after shutdown would fool the sensor. If the
engine is restarted within that window, the module simply displays its last reading rather than
taking a fresh one, so a Check Oil lamp state right after a quick restart reflects the previous
key cycle, not the current oil level.

This timing also underlies the FSM functional test. To test the system on the `engine`, start with
oil at FULL and warm, confirm the bulb prove-out, drain two quarts, wait roughly five minutes,
restart, and the lamp should come on and stay on; if not, check the fuse, relay, sensor, and lamp.
The module lives in the `electrical-body` system alongside the rest of the warning electronics.

## Related Concepts

- [[notes/mnt-engine-oil-refill-is-5-quarts-with-filter|The 4.9L engine oil refill is 5.0 quarts including the filter]]
- [[notes/ipc-functional-test-of-the-oil-level-warning-by-draining-two-quarts|Functional-test the oil level warning by draining two quarts and waiting five minutes]]
- [[notes/ipc-oil-level-warning-is-separate-from-oil-pressure-warning|The Check Oil low-level warning is a separate system from the oil pressure warning lamp]]
- [[notes/ipc-grounding-the-oil-lamp-wire-isolates-bulb-from-sender|Grounding the oil-lamp sender wire isolates a bad bulb from a bad pressure switch]]
- [[notes/ipc-oil-pressure-lamp-is-ground-switched-by-the-engine-unit|The oil pressure warning lamp is ground-switched by an engine-mounted pressure switch]]

## Source

- [[sources/mnt-engine-oil|Engine Oil Capacity and the Low Oil Level Indicator (FSM)]]
- [[sources/ipc-oil-level-warning-indicator|Oil Level Warning Indicator — Description, Operation and Testing (FSM)]]
