---
title: "The wiper/washer system is protected by an 8.25-amp circuit breaker in the fuse junction panel"
kind: spec
source: "[[sources/wpr-circuit-breaker|Wiper Circuit Breaker — Rating and Two-Part Test (FSM)]]"
related:
  - "[[notes/wpr-circuit-breaker-needs-two-bench-tests-to-pass|A wiper circuit breaker passes only if it survives the rated-hold test and trips within 20 seconds at double current]]"
tags:
  - circuit-breaker
  - spec
  - electrical-body
---

The wiper/washer circuit on the 1994 F-150 is protected by a self-resetting circuit
breaker rated at 8.25 amps, located in the fuse junction panel. Knowing the rating and
location is the starting point for any "wipers completely dead" diagnosis: because it
is a breaker rather than a fuse, an intermittent overload (such as a binding motor or
frozen wipers) will cause the wipers to cut out and then return rather than blow
permanently.

This breaker rating also frames the component tests: the breaker should hold 8.25 amps
indefinitely but trip quickly at twice that current. It ties into the truck inventory
system `electrical-body`.

## Related Concepts

- [[notes/wpr-circuit-breaker-needs-two-bench-tests-to-pass|A wiper circuit breaker passes only if it survives the rated-hold test and trips within 20 seconds at double current]]
- [[notes/wpr-wiper-motor-magnets-can-shatter-from-physical-shock|The wiper motor's ceramic magnets can shatter from a physical shock and kill the motor]]
- [[notes/wpr-wiper-motor-current-draw-under-3-5-amps|A healthy wiper motor draws no more than 3.5 amps at either low or high speed]]

## Source

- [[sources/wpr-circuit-breaker|Wiper Circuit Breaker — Rating and Two-Part Test (FSM)]]
