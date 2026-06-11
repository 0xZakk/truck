---
title: "Disarm the air bag before servicing the steering-wheel cruise switches"
kind: procedure
source: "[[sources/crz-speed-control-system-overview|Cruise Control (Speed Control) System — Description, Operation, Service Precautions (FSM)]]"
related:
  - "[[notes/crz-control-switch-sends-set-coast-accel-resume-to-amplifier|The steering-wheel speed control switch tells the amplifier to set, hold, coast, or accelerate]]"
  - "[[notes/sus-disarm-the-air-bag-and-wait-one-minute-before-column-work|Disarm the air bag and wait one minute before steering column or wheel work]]"
  - "[[notes/bdy-battery-disconnect-forces-the-pcm-to-relearn-over-ten-miles|Any cab battery disconnect forces the PCM to relearn its adaptive strategy over about ten miles]]"
tags:
  - cruise-control
  - air-bag
  - safety
  - procedure
---

Because the cruise control driver switches live in the steering wheel — ahead of the driver
air bag module — the FSM's cruise Service Precautions require disarming the air bag before any
steering-wheel work. The sequence: record radio presets, disconnect the battery negative then
positive cable, wait at least one minute for the air bag back-up power supply to deplete its
stored energy, then remove the air bag module nuts, disconnect the module, and connect the
Rotunda Air Bag Simulator 105-00010 (or equivalent) before reconnecting the battery. Arming
reverses the process.

This matters on the `electrical-body` system because replacing or testing a cruise switch is
not a low-voltage job — skipping the wait or the simulator risks an inadvertent deployment.
Also note a side effect of the battery disconnect: the PCM loses its adaptive strategy and the
truck may need 10+ miles of driving before drive quality returns to normal.

> "Wait at least one minute for back-up power supply to deplete its stored energy. ... Connect
> Rotunda Air Bag Simulator 105-00010, or equivalent, to vehicle harness at top of steering
> wheel."

## Related Concepts

- [[notes/crz-control-switch-sends-set-coast-accel-resume-to-amplifier|The steering-wheel speed control switch tells the amplifier to set, hold, coast, or accelerate]]
- [[notes/sus-disarm-the-air-bag-and-wait-one-minute-before-column-work|Disarm the air bag and wait one minute before steering column or wheel work]]
- [[notes/bdy-battery-disconnect-forces-the-pcm-to-relearn-over-ten-miles|Any cab battery disconnect forces the PCM to relearn its adaptive strategy over about ten miles]]
- [[notes/wpr-disarm-the-air-bag-before-working-on-the-column-switch|Disarm the air bag before removing the column-mounted wiper/washer switch]]
- [[notes/chg-disarm-the-air-bag-before-battery-work-on-starting-and-charging|Disarm the air bag system before disconnecting the battery for starting/charging work]]
- [[notes/gls-glass-work-near-the-column-requires-disarming-the-air-bag|Glass or window work that touches the steering column requires disarming the air bag and waiting one minute]]

## Source

- [[sources/crz-speed-control-system-overview|Cruise Control (Speed Control) System — Description, Operation, Service Precautions (FSM)]]
