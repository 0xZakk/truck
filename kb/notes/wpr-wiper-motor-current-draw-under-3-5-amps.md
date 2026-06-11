---
title: "A healthy wiper motor draws no more than 3.5 amps at either low or high speed"
kind: spec
source: "[[sources/wpr-wiper-motor|Wiper Motor — Testing, Service, and Upgraded Kits (FSM)]]"
related:
  - "[[notes/wpr-wiper-motor-magnets-can-shatter-from-physical-shock|The wiper motor's ceramic magnets can shatter from a physical shock and kill the motor]]"
  - "[[notes/wpr-washer-pump-current-draw-window-is-1-7-to-4-amps|The washer pump must draw between 1.7 and 4 amps while pumping]]"
tags:
  - wiper-motor
  - spec
  - electrical-body
---

The FSM's wiper motor current-draw test feeds battery voltage through a tester to the
motor, first at the low-speed terminal and then at the high-speed terminal. In either
case the current draw should not exceed 3.5 amps. The test can be run on the bench or
in the vehicle with the wiper linkage disconnected so the motor turns freely.

A draw above 3.5 amps points to a binding or failing motor (worn brushes, dragging
armature, or partial short). Because the test is done with the linkage off, a high
reading isolates the motor itself rather than a seized linkage or pivot — useful when
deciding whether to replace the motor (`electrical-body`) or chase a mechanical bind
in the linkage.

## Related Concepts

- [[notes/wpr-wiper-motor-magnets-can-shatter-from-physical-shock|The wiper motor's ceramic magnets can shatter from a physical shock and kill the motor]]
- [[notes/wpr-washer-pump-current-draw-window-is-1-7-to-4-amps|The washer pump must draw between 1.7 and 4 amps while pumping]]
- [[notes/wpr-circuit-breaker-needs-two-bench-tests-to-pass|A wiper circuit breaker passes only if it survives the rated-hold test and trips within 20 seconds at double current]]
- [[notes/wpr-wiper-circuit-breaker-is-rated-8-25-amps|The wiper/washer system is protected by an 8.25-amp circuit breaker in the fuse junction panel]]

## Source

- [[sources/wpr-wiper-motor|Wiper Motor — Testing, Service, and Upgraded Kits (FSM)]]
