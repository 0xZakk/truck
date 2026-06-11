---
title: "On automatics, the park/neutral switch both closes the starter relay and lights the backup lamps"
kind: how-it-works
source: "[[sources/chg-starting-interlock-switches|Starting Interlock Switches (Clutch / Neutral Safety) — Description and Operation (FSM)]]"
related: []
tags:
  - starting-system
  - neutral-safety-switch
  - park-neutral-switch
  - backup-lamp
  - reverse-lights
  - starter
  - how-it-works
---

On automatic-transmission F-150s the same switch handles two jobs. In **PARK or NEUTRAL** it
directs current to **close the starter motor relay**, allowing the engine to crank. In
**REVERSE** it instead directs current to **illuminate the backup lamps**. Ford calls this
component the **park/neutral position switch** on the C6 and the **manual lever position
sensor** — the transmission range (TR) sensor — on the 4R70W and E4OD transmissions, but the
logic is identical. So both the backup lamp circuit and the starter circuit pass through one
shared component on these automatics.

This dual role is a useful diagnostic clue. If both the reverse lights are dead and the
engine won't crank in Park/Neutral, suspect the range/PNP switch or its adjustment rather
than two unrelated faults. Likewise, a no-crank that is cured by jiggling the shifter, or
reverse lights that come on in the wrong gear, both point to the same switch being out of
adjustment. The manual transmission F-150 (this 4.9L truck) uses the clutch pedal position
switch instead, so it has no park/neutral switch in its start path.

> "With the transmission in 'PARK' or 'NEUTRAL' the park/neutral position switch directs
> current to close the starter motor relay. … With the transmission in 'REVERSE' … directs
> current to illuminate the backup lamps."

This relates to truck inventory systems `electrical-starting` and `electrical-body`.

## Related Concepts

- [[notes/lgt-backup-lamp-source-depends-on-the-transmission|What powers the backup lamps depends on which transmission the truck has]]
- [[notes/chg-clutch-switch-is-an-in-series-interlock-to-the-starter-relay|The starting interlock switch sits in series between the start signal and the starter relay]]
- [[notes/clutch-pedal-position-switch-is-the-start-interlock-on-manual-f150|The clutch pedal position switch is the start interlock on a manual F-150]]

## Source

- [[sources/chg-starting-interlock-switches|Starting Interlock Switches (Clutch / Neutral Safety) — Description and Operation (FSM)]]
- [[sources/lgt-backup-lamp-switch|Backup Lamp Switch / Park-Neutral Position Switch by Transmission (FSM)]]
