---
title: "Grounding the oil-lamp sender wire isolates a bad bulb from a bad pressure switch"
kind: troubleshooting
source: "[[sources/ipc-oil-pressure-warning-lamp|Oil Pressure Warning Lamp / Indicator — Testing and Inspection (FSM)]]"
related:
  - "[[notes/ipc-oil-pressure-lamp-is-ground-switched-by-the-engine-unit|The oil pressure warning lamp is ground-switched by an engine-mounted pressure switch]]"
tags:
  - oil-pressure-warning-lamp
  - troubleshooting
  - lubrication
---

Symptom: the oil pressure warning lamp does not light when the ignition is turned ON (it
should, as a prove-out). Because the lamp is ground-switched through the engine-mounted
pressure switch, the FSM's first move is to disconnect the wire from the engine unit and
ground that wire directly to the frame or cylinder block.

- If the lamp now lights, the bulb and the wiring up to that point are good, so the fault is
  the engine unit or its ground. Check the unit for being loose or poorly grounded; if it is
  tight and properly grounded, replace it. Remember that sealing compound on the threads
  causes a poor ground.
- If the lamp still does not light with the wire grounded, the bulb (or the circuit feeding
  it) is at fault — replace the bulb.

Conversely, if the lamp stays lit when it should be out, replace the engine unit before
investigating further for a genuine low-pressure indication. This quick ground test cleanly
separates a cluster/bulb problem from a sender problem in the `electrical-body` circuit.

## Related Concepts

- [[notes/ipc-oil-pressure-lamp-is-ground-switched-by-the-engine-unit|The oil pressure warning lamp is ground-switched by an engine-mounted pressure switch]]
- [[notes/ipc-oil-level-warning-is-separate-from-oil-pressure-warning|The Check Oil low-level warning is a separate system from the oil pressure warning lamp]]
- [[notes/ipc-charge-lamp-jumper-test-from-terminal-1-to-battery-negative|A jumper from regulator terminal 1 to battery negative proves the charge lamp bulb and circuit]]
- [[notes/ipc-functional-test-of-the-oil-level-warning-by-draining-two-quarts|Functional-test the oil level warning by draining two quarts and waiting five minutes]]
- [[notes/mnt-low-oil-indicator-trips-at-1-5-quarts-low-with-drain-back-delay|The low-oil indicator trips when oil is about 1.5 quarts low and waits five minutes for drain-back]]

## Source

- [[sources/ipc-oil-pressure-warning-lamp|Oil Pressure Warning Lamp / Indicator — Testing and Inspection (FSM)]]
