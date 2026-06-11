---
title: "The Check Oil low-level warning is a separate system from the oil pressure warning lamp"
kind: how-it-works
source: "[[sources/ipc-oil-level-warning-indicator|Oil Level Warning Indicator — Description, Operation and Testing (FSM)]]"
related:
  - "[[notes/ipc-oil-pressure-lamp-is-ground-switched-by-the-engine-unit|The oil pressure warning lamp is ground-switched by an engine-mounted pressure switch]]"
  - "[[notes/mnt-low-oil-indicator-trips-at-1-5-quarts-low-with-drain-back-delay|The low-oil indicator trips when oil is about 1.5 quarts low and waits five minutes for drain-back]]"
tags:
  - oil-level-warning-indicator
  - warning-indicators
  - lubrication
---

It is easy to conflate the two oil warnings, but on the 1994 F-150 they are independent. The
oil PRESSURE lamp is ground-switched by an engine-mounted pressure switch and warns of low
running oil pressure. The oil LEVEL ("Check Oil") indicator instead warns that the quantity
of oil in the pan is low, using a completely different set of parts: a float-type sensor on
the side of the oil pan, an electronic control module, and its own instrument-panel lamp.

The level system performs a bulb prove-out in START, then in RUN or START the control module
reads whether the pan sensor is grounded (oil low) or ungrounded (oil not low). With adequate
oil the lamp goes out in RUN; if the oil is approximately 1.5 quarts or more low, a relay
turns the lamp ON and keeps it on until the ignition is switched OFF. So a lit Check Oil lamp
means add oil, whereas a lit oil pressure lamp means stop and investigate pressure — distinct
meanings driven by distinct hardware in the `electrical-body` and engine `lubrication`
systems.

## Related Concepts

- [[notes/ipc-oil-pressure-lamp-is-ground-switched-by-the-engine-unit|The oil pressure warning lamp is ground-switched by an engine-mounted pressure switch]]
- [[notes/mnt-low-oil-indicator-trips-at-1-5-quarts-low-with-drain-back-delay|The low-oil indicator trips when oil is about 1.5 quarts low and waits five minutes for drain-back]]
- [[notes/ipc-grounding-the-oil-lamp-wire-isolates-bulb-from-sender|Grounding the oil-lamp sender wire isolates a bad bulb from a bad pressure switch]]
- [[notes/ipc-functional-test-of-the-oil-level-warning-by-draining-two-quarts|Functional-test the oil level warning by draining two quarts and waiting five minutes]]

## Source

- [[sources/ipc-oil-level-warning-indicator|Oil Level Warning Indicator — Description, Operation and Testing (FSM)]]
