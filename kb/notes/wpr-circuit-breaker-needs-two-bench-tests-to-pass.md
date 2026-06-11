---
title: "A wiper circuit breaker passes only if it survives the rated-hold test and trips within 20 seconds at double current"
kind: procedure
source: "[[sources/wpr-circuit-breaker|Wiper Circuit Breaker — Rating and Two-Part Test (FSM)]]"
related:
  - "[[notes/wpr-wiper-circuit-breaker-is-rated-8-25-amps|The wiper/washer system is protected by an 8.25-amp circuit breaker in the fuse junction panel]]"
tags:
  - circuit-breaker
  - procedure
  - electrical-body
---

The FSM requires two separate bench tests to confirm the wiper circuit breaker is
good. First remove the breaker from the fuse junction panel, and before each test
short the tester leads together to set the current draw.

Test 1 (rated hold): set the tester to the breaker's rated current (8.25 amps) and
hold it there for 10 minutes. If the breaker opens at any point during those 10
minutes, it is too sensitive — replace it.

Test 2 (overcurrent trip): set the tester to twice rated current and connect the
breaker. The ammeter reading should drop to zero within 20 seconds as the breaker
opens. If it takes longer than 20 seconds to open, the breaker is too slow — replace
it. A breaker must pass both tests to be considered good (`electrical-body`).

## Related Concepts

- [[notes/wpr-wiper-circuit-breaker-is-rated-8-25-amps|The wiper/washer system is protected by an 8.25-amp circuit breaker in the fuse junction panel]]
- [[notes/wpr-wiper-motor-current-draw-under-3-5-amps|A healthy wiper motor draws no more than 3.5 amps at either low or high speed]]

## Source

- [[sources/wpr-circuit-breaker|Wiper Circuit Breaker — Rating and Two-Part Test (FSM)]]
