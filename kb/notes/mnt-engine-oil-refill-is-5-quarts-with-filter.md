---
title: "The 4.9L engine oil refill is 5.0 quarts including the filter"
kind: spec
source: "[[sources/mnt-engine-oil|Engine Oil Capacity and the Low Oil Level Indicator (FSM)]]"
related:
  - "[[notes/mnt-low-oil-indicator-trips-at-1-5-quarts-low-with-drain-back-delay|The low-oil indicator trips when oil is about 1.5 quarts low and waits five minutes for drain-back]]"
tags:
  - engine
  - engine-oil
  - capacity
  - spec
---

The FSM gives the 4.9L `engine` oil refill as 5.0 quarts (4.7 L), with a note to add 1 quart when
the filter is changed. In practice a routine oil-and-filter service takes the full 5 quarts; a
drain without filter change takes about 1 quart less.

This capacity is what you measure refills against and what the low-oil sensor logic is calibrated
to — knowing it lets you cross-check that the dipstick FULL mark corresponds to a correct fill. For
the recommended viscosity and grade, see the existing owner's-guide note on 5W-30 meeting Ford spec
ESE-M2C153-E.

## Related Concepts

- [[notes/mnt-low-oil-indicator-trips-at-1-5-quarts-low-with-drain-back-delay|The low-oil indicator trips when oil is about 1.5 quarts low and waits five minutes for drain-back]]
- [[notes/49l-uses-5w30-oil-meeting-ford-spec-ese-m2c153-e|The 4.9L uses 5W-30 oil meeting Ford spec ESE-M2C153-E]]

## Source

- [[sources/mnt-engine-oil|Engine Oil Capacity and the Low Oil Level Indicator (FSM)]]
