---
title: "Functional-test the oil level warning by draining two quarts and waiting five minutes"
kind: procedure
source: "[[sources/ipc-oil-level-warning-indicator|Oil Level Warning Indicator — Description, Operation and Testing (FSM)]]"
related:
  - "[[notes/ipc-oil-level-module-has-a-five-minute-reset-delay|The oil level module waits about five minutes after key-off to allow oil drain-back before re-reading]]"
tags:
  - oil-level-warning-indicator
  - procedure
  - lubrication
  - troubleshooting
---

The FSM gives a concrete functional test for the Check Oil warning:

1. Start with oil at the FULL mark on the dipstick and the engine warm, so oil drains
   properly off the pan sensor.
2. Turn the ignition ON and start the engine. The warning lamp should come on briefly in
   START (bulb test) and then go out.
3. Turn the engine OFF and drain two quarts of oil from the engine.
4. Wait approximately five minutes (to clear the module's reset delay and let oil drain back).
5. Restart the engine. The warning lamp should now come on and stay on.

If the lamp does not come on after the two-quart drain, check the fuse, the low oil level
relay, the low oil level sensor, and the lamp. Two quarts comfortably exceeds the ~1.5-quart
trip threshold, so a healthy system must illuminate. This procedure exercises the
`electrical-body` warning circuit end-to-end.

## Related Concepts

- [[notes/ipc-oil-level-module-has-a-five-minute-reset-delay|The oil level module waits about five minutes after key-off to allow oil drain-back before re-reading]]
- [[notes/mnt-low-oil-indicator-trips-at-1-5-quarts-low-with-drain-back-delay|The low-oil indicator trips when oil is about 1.5 quarts low and waits five minutes for drain-back]]
- [[notes/ipc-grounding-the-oil-lamp-wire-isolates-bulb-from-sender|Grounding the oil-lamp sender wire isolates a bad bulb from a bad pressure switch]]
- [[notes/ipc-oil-level-warning-is-separate-from-oil-pressure-warning|The Check Oil low-level warning is a separate system from the oil pressure warning lamp]]

## Source

- [[sources/ipc-oil-level-warning-indicator|Oil Level Warning Indicator — Description, Operation and Testing (FSM)]]
