---
title: "A charge light that stays on points to the regulator or stator circuit, not always a dead alternator"
kind: troubleshooting
source: "[[sources/alternator-description-and-operation-fsm|Alternator — Description and Operation (FSM)]]"
related:
  - "[[notes/charging-system-works-through-three-circuits|The charging system works through three circuits: A (sense), B+ (output), and S (feedback)]]"
tags:
  - charging-system
  - charge-light
  - voltage-regulator
  - diagnosis
---

The charge warning lamp on this truck is controlled by the **stator (S) circuit feeding back
to the voltage regulator**, not directly by whether the battery is being charged. The
regulator uses that S signal (around half battery voltage when the alternator is spinning) to
decide whether to turn the lamp off.

So a charge light that stays on with the engine running does **not** automatically mean the
alternator is dead. It can equally mean the regulator isn't seeing a valid S-circuit signal —
a broken stator connection, a regulator fault, or wiring in the feedback path. Before
replacing the alternator, measure actual output at B+ and check the S and A circuits; the
lamp is a symptom of the signalling, not a direct readout of charging.

This relates to truck inventory system `electrical-charging`.

## Related Concepts

- [[notes/charging-system-works-through-three-circuits|The charging system works through three circuits: A (sense), B+ (output), and S (feedback)]]

## Source

- [[sources/alternator-description-and-operation-fsm|Alternator — Description and Operation (FSM)]]
