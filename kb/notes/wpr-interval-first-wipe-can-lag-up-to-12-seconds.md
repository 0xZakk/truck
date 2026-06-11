---
title: "The first interval wipe can lag up to 12 seconds, which is normal"
kind: how-it-works
source: "[[sources/wpr-wiper-control-module|Wiper Control Module and Interval Wipe Operation (FSM)]]"
related:
  - "[[notes/wpr-wiper-control-module-drives-all-wiper-modes|The wiper control module, not the switch, drives all wiper and washer modes from switch signals]]"
tags:
  - interval-wipers
  - wiper-control-module
  - electrical-body
---

In the Interval (INT) position the 1994 F-150's wipers make single sweeps separated
by a pause, and a control knob on the end of the wiper switch sets that pause from
roughly 1 to 12 seconds. Because the wiper control module times the pause before the
first sweep, the FSM notes that the first wipe may not occur until after a pause of
as long as 12 seconds.

This is worth remembering during diagnosis: a customer complaint of "interval wipers
are slow to start" or "didn't wipe right away" can simply be the knob set to its
longest pause, not a fault. Confirm by turning the interval knob to its shortest
setting before chasing a problem in the module (`electrical-body`).

## Related Concepts

- [[notes/wpr-wiper-control-module-drives-all-wiper-modes|The wiper control module, not the switch, drives all wiper and washer modes from switch signals]]

## Source

- [[sources/wpr-wiper-control-module|Wiper Control Module and Interval Wipe Operation (FSM)]]
