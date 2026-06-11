---
title: "Compression is acceptable when the lowest cylinder reads within 25% of the highest"
kind: spec
source: "[[sources/mnt-compression-check|Compression Check — Testing and Specifications (FSM)]]"
related:
  - "[[notes/mnt-compression-check-procedure-warms-engine-then-cranks-five-strokes|The compression-check procedure warms the engine, pulls all plugs, and cranks five strokes per cylinder]]"
tags:
  - engine
  - compression
  - spec
---

Ford does not publish an absolute cranking-pressure target for the 4.9L I6; the spec is
relative. Indicated compression is within specification if the lowest-reading cylinder is
within 25 percent of the highest-reading cylinder. A spread greater than 25 percent indicates
an improperly seated valve or worn/broken piston rings.

This makes the compression test a quick triage on the `engine` system: you do not need a known
"good" number, only consistency across cylinders. One markedly low cylinder (more than 25% below
the best one) localizes the fault to valves or rings in that hole, which a follow-up wet test or
leak-down can then separate.

## Related Concepts

- [[notes/mnt-compression-check-procedure-warms-engine-then-cranks-five-strokes|The compression-check procedure warms the engine, pulls all plugs, and cranks five strokes per cylinder]]
- [[notes/eec-compression-is-acceptable-if-lowest-cylinder-is-within-25-percent|Compression is acceptable if the lowest cylinder reads within 25% of the highest]]

## Source

- [[sources/mnt-compression-check|Compression Check — Testing and Specifications (FSM)]]
