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
- [[notes/ipc-charge-lamp-grounds-through-regulator-terminal-1|The charge lamp lights because the regulator grounds it through terminal 1 until the S-circuit voltage is reached]]
- [[notes/ipc-charge-lamp-jumper-test-from-terminal-1-to-battery-negative|A jumper from regulator terminal 1 to battery negative proves the charge lamp bulb and circuit]]
- [[notes/ipc-voltmeter-normal-range-is-13-5-to-14-volts|A normal voltmeter reading on the F-150 is 13.5 to 14.0 volts]]

## Source

- [[sources/alternator-description-and-operation-fsm|Alternator — Description and Operation (FSM)]]
