---
title: "The manual-trans cooling system holds 13-15 quarts of 50/50 coolant depending on A/C"
kind: spec
source: "[[sources/eng-cooling-system-capacity-and-pressure|Cooling System — Capacity, Coolant Type, Radiator Cap & Thermostat (FSM)]]"
related:
  - "[[notes/eng-radiator-cap-holds-13-psi|The radiator cap holds the cooling system to 13 psi]]"
tags:
  - cooling
  - coolant
  - capacity
  - specifications
---

The cooling-system capacity for the manual-transmission 4.9L F-150 varies with accessory
content: 13 qts (US) without A/C, 14 qts with A/C, and 15 qts with A/C plus Super Cooling.
The variation reflects the larger radiator and heater circuit volume that comes with air
conditioning and the heavy-duty cooling option. The coolant is a 50% mix of premium Ford
coolant (Ford spec ESE-M97B44-A) with water, and the FSM explicitly warns not to mix coolant
types.

These numbers, on the `cooling` inventory system, are the refill targets after a drain-and-fill
or flush, and set how much 50/50 premix to prepare for a complete fill. Knowing which options
the truck has (A/C, Super Cooling) tells you whether to target 13, 14, or 15 quarts so the
system ends up properly full and at the correct concentration. Because the block and heater core
retain coolant, the actual amount that goes back in after a partial drain is usually less than
the full system capacity; the figure is the total system volume.

> "Manual Transmission Without A/C 13 qts (US) ... With A/C 14 qts (US) ... With A/C & Super
> Cooling 15 qts (US)."

## Related Concepts

- [[notes/eng-radiator-cap-holds-13-psi|The radiator cap holds the cooling system to 13 psi]]
- [[notes/mnt-coolant-is-ford-premium-50-50-and-types-must-not-be-mixed|Coolant is Ford Premium at a 50/50 mix and types must not be mixed]]

## Source

- [[sources/eng-cooling-system-capacity-and-pressure|Cooling System — Capacity, Coolant Type, Radiator Cap & Thermostat (FSM)]]
- [[sources/mnt-coolant|Coolant — Capacity and Fluid Type (FSM)]]
