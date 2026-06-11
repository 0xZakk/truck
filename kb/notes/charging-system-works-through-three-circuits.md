---
title: "The charging system works through three circuits: A (sense), B+ (output), and S (feedback)"
kind: how-it-works
source: "[[sources/alternator-description-and-operation-fsm|Alternator — Description and Operation (FSM)]]"
related:
  - "[[notes/charge-light-staying-on-points-to-regulator-or-stator-circuit|A charge light that stays on points to the regulator or stator circuit, not always a dead alternator]]"
tags:
  - alternator
  - charging-system
  - voltage-regulator
---

The 1994 F-150's charging system is best understood as three circuits working together.
The **A (sensing) circuit** carries current to the alternator field coil once the regulator
is energized, which is what makes the alternator start generating. The **B+ output terminal**
delivers the alternator's power to the truck after an internal rectifier converts the
alternator's AC into DC. The **S (stator) circuit** feeds a voltage signal — typically about
half battery voltage — back to the regulator.

Holding this three-circuit model in mind turns charging diagnosis from guesswork into a
process: is the field being energized (A), is DC actually coming out (B+), and is the
feedback signal present (S)? Each circuit fails differently, and the warning lamp behaviour
is driven by the S signal rather than by raw output.

> "The alternator generates an AC output, which is converted to a DC output by a rectifier
> assembly internal to alternator; this DC output is then supplied to the vehicle through the
> B+ terminal."

This relates to truck inventory system `electrical-charging`.

## Related Concepts

- [[notes/charge-light-staying-on-points-to-regulator-or-stator-circuit|A charge light that stays on points to the regulator or stator circuit, not always a dead alternator]]

## Source

- [[sources/alternator-description-and-operation-fsm|Alternator — Description and Operation (FSM)]]
