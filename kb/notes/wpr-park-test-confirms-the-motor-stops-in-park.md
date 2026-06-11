---
title: "The park test confirms the wiper motor cycles once and stops in the Park position"
kind: procedure
source: "[[sources/wpr-diagnostics-and-precautions|Wiper/Washer Diagnostics, Park Test, and Air Bag Service Precautions (FSM)]]"
related:
  - "[[notes/wpr-wiper-motor-current-draw-under-3-5-amps|A healthy wiper motor draws no more than 3.5 amps at either low or high speed]]"
  - "[[notes/wpr-wiper-control-module-drives-all-wiper-modes|The wiper control module, not the switch, drives all wiper and washer modes from switch signals]]"
tags:
  - park-switch
  - wiper-motor
  - procedure
  - electrical-body
---

The park switch inside the wiper motor is what lets the wipers finish their sweep and
return to the bottom of the windshield when switched off. The FSM's bench Park Test
checks it directly: jumper the motor's low-speed terminal to the park switch's park
return terminal, jumper both the motor and park switch ground terminals to the battery
ground cable, then feed battery positive to the park feed terminal. A good motor will
cycle once and then stop in the Park position.

This isolates the park function from the control module. If the wipers run but stop
mid-windshield instead of parking, and the motor passes this Park Test, the fault is
upstream in the module or switch wiring rather than in the motor's park switch
(`electrical-body`).

## Related Concepts

- [[notes/wpr-wiper-motor-current-draw-under-3-5-amps|A healthy wiper motor draws no more than 3.5 amps at either low or high speed]]
- [[notes/wpr-wiper-control-module-drives-all-wiper-modes|The wiper control module, not the switch, drives all wiper and washer modes from switch signals]]

## Source

- [[sources/wpr-diagnostics-and-precautions|Wiper/Washer Diagnostics, Park Test, and Air Bag Service Precautions (FSM)]]
