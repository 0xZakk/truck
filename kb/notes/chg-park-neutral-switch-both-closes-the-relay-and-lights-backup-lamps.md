---
title: "On automatics, the park/neutral switch both closes the starter relay and lights the backup lamps"
kind: how-it-works
source: "[[sources/chg-starting-interlock-switches|Starting Interlock Switches (Clutch / Neutral Safety) — Description and Operation (FSM)]]"
related:
  - "[[notes/chg-clutch-switch-is-an-in-series-interlock-to-the-starter-relay|The starting interlock switch sits in series between the start signal and the starter relay]]"
  - "[[notes/clutch-pedal-position-switch-is-the-start-interlock-on-manual-f150|The clutch pedal position switch is the start interlock on a manual F-150]]"
tags:
  - starting-system
  - neutral-safety-switch
  - how-it-works
---

On automatic-transmission F-150s the same switch handles two jobs. In **PARK or NEUTRAL** it
directs current to **close the starter motor relay**, allowing the engine to crank. In
**REVERSE** it instead directs current to **illuminate the backup lamps**. Ford calls this
component the **park/neutral position switch** on the C6 and the **manual lever position
sensor** on the 4R70W and E4OD transmissions, but the logic is identical.

This dual role is useful when diagnosing: a truck that cranks only when you jiggle the
shifter, or one whose backup lamps fail, can point to the same switch or its adjustment.
The manual transmission F-150 (this 4.9L truck) uses the clutch pedal position switch
instead, so it has no park/neutral switch in its start path.

> "With the transmission in 'PARK' or 'NEUTRAL' the park/neutral position switch directs
> current to close the starter motor relay. … With the transmission in 'REVERSE' … directs
> current to illuminate the backup lamps."

This relates to truck inventory system `electrical-starting`.

## Related Concepts

- [[notes/chg-clutch-switch-is-an-in-series-interlock-to-the-starter-relay|The starting interlock switch sits in series between the start signal and the starter relay]]
- [[notes/clutch-pedal-position-switch-is-the-start-interlock-on-manual-f150|The clutch pedal position switch is the start interlock on a manual F-150]]
- [[notes/lgt-on-automatics-the-range-switch-shares-backup-lamps-and-starter-relay|On automatics the same range switch lights the backup lamps and closes the starter relay]]
- [[notes/lgt-backup-lamp-source-depends-on-the-transmission|What powers the backup lamps depends on which transmission the truck has]]
- [[notes/sen-clutch-switch-is-the-manual-start-interlock|On the manual F-150 the clutch pedal switch is the start interlock and feeds the starter relay only when the pedal is down]]

## Source

- [[sources/chg-starting-interlock-switches|Starting Interlock Switches (Clutch / Neutral Safety) — Description and Operation (FSM)]]
