---
title: "The washer pump must draw between 1.7 and 4 amps while pumping"
kind: spec
source: "[[sources/wpr-washer-pump|Windshield Washer Pump — Current Draw Test (FSM)]]"
related:
  - "[[notes/wpr-wiper-motor-current-draw-under-3-5-amps|A healthy wiper motor draws no more than 3.5 amps at either low or high speed]]"
tags:
  - washer-pump
  - spec
  - electrical-body
---

The windshield washer pump is tested by reading its current draw with a volt-ohmmeter
while the pump is actively pumping fluid. The FSM specifies a two-sided window: draw
should not exceed 4 amps and should not be less than 1.7 amps.

The two limits catch different failures. A reading above 4 amps suggests a binding or
obstructed pump pulling excess current. A reading below 1.7 amps suggests a weak,
worn, or partially open pump that is not doing real work — it may run but move little
fluid. Either way the pump is the suspect part (`electrical-body`). Make sure the
reservoir has fluid and the pump is primed before judging a low reading.

## Related Concepts

- [[notes/wpr-wiper-motor-current-draw-under-3-5-amps|A healthy wiper motor draws no more than 3.5 amps at either low or high speed]]
- [[notes/wpr-circuit-breaker-needs-two-bench-tests-to-pass|A wiper circuit breaker passes only if it survives the rated-hold test and trips within 20 seconds at double current]]

## Source

- [[sources/wpr-washer-pump|Windshield Washer Pump — Current Draw Test (FSM)]]
