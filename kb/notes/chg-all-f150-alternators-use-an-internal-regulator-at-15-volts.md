---
title: "All F-150 alternators use an internal regulator set near 15 volts"
kind: spec
source: "[[sources/chg-alternator-specifications|Alternator — Specifications (FSM)]]"
related:
  - "[[notes/chg-alternator-brush-and-slip-ring-wear-limits|Alternator brush and slip-ring wear limits depend on the unit's amperage rating]]"
  - "[[notes/charging-system-works-through-three-circuits|The charging system works through three circuits: A (sense), B+ (output), and S (feedback)]]"
tags:
  - alternator
  - voltage-regulator
  - charging-system
  - spec
---

Across the whole family of alternators Ford fitted to the 1994 F-150 — 40, 40HE, 60, 65,
75, 95, and 130 amperes — the **voltage regulator is internal (integral)** to the
alternator. There is no separately mounted regulator to test or replace; the regulator is
part of the alternator assembly. For the 40-through-95 A units the regulated set-point is
spec'd at **15.0 volts** (the 130 A unit's volt figure is not listed).

This is why charging diagnosis on this truck centers on the alternator as a unit and on the
A/S/B+ circuits feeding it, rather than on an external regulator box. The 15.0 V figure is
the regulator's target; a charging system holding well above or below the in-vehicle test
band points back to this internal regulator or its sense/feedback wiring.

> "Alternators With Current Ratings of: 40, 40HE, 60, 65, 75, and 95 Amperes: Volts 15.0"

This relates to truck inventory system `electrical-charging`.

## Related Concepts

- [[notes/chg-alternator-brush-and-slip-ring-wear-limits|Alternator brush and slip-ring wear limits depend on the unit's amperage rating]]
- [[notes/charging-system-works-through-three-circuits|The charging system works through three circuits: A (sense), B+ (output), and S (feedback)]]

## Source

- [[sources/chg-alternator-specifications|Alternator — Specifications (FSM)]]
