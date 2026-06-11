---
title: "The oil pressure warning lamp is ground-switched by an engine-mounted pressure switch"
kind: how-it-works
source: "[[sources/ipc-oil-pressure-warning-lamp|Oil Pressure Warning Lamp / Indicator — Testing and Inspection (FSM)]]"
related:
  - "[[notes/ipc-grounding-the-oil-lamp-wire-isolates-bulb-from-sender|Grounding the oil-lamp sender wire isolates a bad bulb from a bad pressure switch]]"
  - "[[notes/ipc-oil-level-warning-is-separate-from-oil-pressure-warning|The Check Oil low-level warning is a separate system from the oil pressure warning lamp]]"
tags:
  - oil-pressure-warning-lamp
  - lubrication
  - warning-indicators
---

The oil pressure warning lamp on the 1994 F-150 is a simple idiot light completed to ground
through an engine-mounted pressure switch the FSM calls the "engine unit." With the ignition
ON and oil pressure below the switch's threshold, the switch is grounded and the bulb
lights; once the engine builds pressure, the switch opens and the lamp goes out. This is why
the lamp glows at key-ON as a prove-out before the engine is running.

A consequence of this ground-switched design is a normal quirk: at idle the lamp may light
or flicker even with adequate pressure, but it should go out as engine speed (and thus
pressure) increases. A lamp that stays lit when it should be out warrants replacing the
engine unit before chasing an actual low-pressure cause. Also, sealing compound on the
engine-unit threads causes a poor ground and can produce false readings, since the switch
relies on a good thread ground.

This sits in the `electrical-body` wiring and engine `lubrication` warning domain.

## Related Concepts

- [[notes/ipc-grounding-the-oil-lamp-wire-isolates-bulb-from-sender|Grounding the oil-lamp sender wire isolates a bad bulb from a bad pressure switch]]
- [[notes/ipc-oil-level-warning-is-separate-from-oil-pressure-warning|The Check Oil low-level warning is a separate system from the oil pressure warning lamp]]
- [[notes/mnt-low-oil-indicator-trips-at-1-5-quarts-low-with-drain-back-delay|The low-oil indicator trips when oil is about 1.5 quarts low and waits five minutes for drain-back]]
- [[notes/ipc-check-engine-message-signals-eec-iv-fmem-mode|The CHECK ENGINE message signals the EEC-IV has entered a backup (FMEM) operating strategy]]

## Source

- [[sources/ipc-oil-pressure-warning-lamp|Oil Pressure Warning Lamp / Indicator — Testing and Inspection (FSM)]]
