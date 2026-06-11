---
title: "The charge lamp lights because the regulator grounds it through terminal 1 until the S-circuit voltage is reached"
kind: how-it-works
source: "[[sources/ipc-charge-lamp-indicator|Charge Lamp / Indicator — Description, Operation and Testing (FSM)]]"
related:
  - "[[notes/ipc-charge-lamp-jumper-test-from-terminal-1-to-battery-negative|A jumper from regulator terminal 1 to battery negative proves the charge lamp bulb and circuit]]"
  - "[[notes/charge-light-staying-on-points-to-regulator-or-stator-circuit|A charge light that stays on points to the regulator or stator circuit, not always a dead alternator]]"
  - "[[notes/charging-system-works-through-three-circuits|The charging system works through three circuits: A (sense), B+ (output), and S (feedback)]]"
tags:
  - charge-lamp
  - charging-system
  - voltage-regulator
  - instrument-cluster
---

The charge warning lamp is not switched by the alternator's output directly; it is
ground-switched inside the integral voltage regulator. With the ignition in START or RUN,
battery current flows from the battery through the warning indicator bulb into the regulator
at terminal "1" and then to ground through the regulator's internal indicator switch. That
completed ground is what lights the bulb at key-ON before the engine is charging.

As the alternator comes up, the regulator energizes the field (sensing low voltage at
terminal A, closing the field switch, feeding the field via terminal F), and the spinning
rotor makes the stator produce voltage at terminals B and S. Once a predetermined voltage
appears at terminal S, the regulator opens the indicator switch, removing the lamp's ground
and turning it OFF. So the lamp going out is a direct report that the S-circuit feedback
voltage has been reached — which is why charging diagnosis keys on terminal S. This warning
circuit lives in the `electrical-body` and `interior` cluster domains.

## Related Concepts

- [[notes/ipc-charge-lamp-jumper-test-from-terminal-1-to-battery-negative|A jumper from regulator terminal 1 to battery negative proves the charge lamp bulb and circuit]]
- [[notes/charge-light-staying-on-points-to-regulator-or-stator-circuit|A charge light that stays on points to the regulator or stator circuit, not always a dead alternator]]
- [[notes/charging-system-works-through-three-circuits|The charging system works through three circuits: A (sense), B+ (output), and S (feedback)]]
- [[notes/ipc-voltmeter-normal-range-is-13-5-to-14-volts|A normal voltmeter reading on the F-150 is 13.5 to 14.0 volts]]

## Source

- [[sources/ipc-charge-lamp-indicator|Charge Lamp / Indicator — Description, Operation and Testing (FSM)]]
