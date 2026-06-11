---
title: "Cruise control has several independent deactivation paths so braking always disengages it"
kind: how-it-works
source: "[[sources/crz-brake-deactivation-switches|Cruise Control Brake Switches — Brake On/Off Switch and Brake Pressure (Deactivator) Switch (FSM)]]"
related:
  - "[[notes/crz-brake-pressure-switch-opens-at-5-to-10-pounds|The brake pressure switch is a redundant deactivator that opens at 5-10 lbs of pedal pressure]]"
  - "[[notes/crz-clutch-switch-deactivates-cruise-when-pedal-depressed|On manual trucks the clutch switch deactivates cruise the moment the pedal is depressed]]"
  - "[[notes/lgt-brake-light-switch-feeds-pcm-cruise-shift-lock-and-abs|The brake light switch feeds the PCM, cruise control, shift lock and ABS, not just the stop lamps]]"
tags:
  - cruise-control
  - deactivation
  - safety
  - how-it-works
---

Cruise control is built with redundant ways to drop out, because the one thing it must always
do is release when the driver wants control back. Three inputs can deactivate it: the brake
on/off (stop-lamp) switch sends a brakes-applied signal to the speed control system, the brake
pressure switch is a redundant safety device that removes power from the servo clutch under
brake pedal pressure, and on manual trucks the clutch switch deactivates the system when the
clutch is depressed.

For diagnosis on the `electrical-body` system this redundancy cuts two ways. It means a single
failed switch usually won't leave cruise dangerously stuck on — but it also means the system
can be disabled by any one of these switches failing in the "applied" state, producing a
"cruise won't engage or won't hold" complaint with no obvious cause. The FSM even gives this a
dedicated pinpoint test, J: "Speed Control Does Not Disengage When Brakes Applied," for the
worst case where the brake path fails to deactivate.

> "It also provides a brakes-applied signal to the speed control system (for deactivation) ...
> A redundant safety device used to deactivate the speed control system."

## Related Concepts

- [[notes/crz-brake-pressure-switch-opens-at-5-to-10-pounds|The brake pressure switch is a redundant deactivator that opens at 5-10 lbs of pedal pressure]]
- [[notes/crz-clutch-switch-deactivates-cruise-when-pedal-depressed|On manual trucks the clutch switch deactivates cruise the moment the pedal is depressed]]
- [[notes/lgt-brake-light-switch-feeds-pcm-cruise-shift-lock-and-abs|The brake light switch feeds the PCM, cruise control, shift lock and ABS, not just the stop lamps]]
- [[notes/crz-control-switch-sends-set-coast-accel-resume-to-amplifier|The steering-wheel speed control switch tells the amplifier to set, hold, coast, or accelerate]]
- [[notes/lgt-a-failed-brake-light-switch-can-disable-cruise-and-torque-converter-unlock|A failed brake light switch shows up as cruise or torque-converter symptoms, not just dark stop lamps]]

## Source

- [[sources/crz-brake-deactivation-switches|Cruise Control Brake Switches — Brake On/Off Switch and Brake Pressure (Deactivator) Switch (FSM)]]
